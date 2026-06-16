from dataclasses import dataclass

from .common import Any, SEARCH_CANDIDATE_LIMIT, SEARCH_SELECTION_POOL_SIZE, json, random, re


PROACTIVE_FAST_RETRIEVAL_MODE = "user_message_fast_prefilter"
PROACTIVE_FAST_CANDIDATE_LIMIT = SEARCH_CANDIDATE_LIMIT
PROACTIVE_FAST_FALLBACK_MIN_SCORE = 6.0
PROACTIVE_FAST_SYSTEM_PROMPT = (
    "你是 AstrBot 的主动表情包多标签精排器。"
    "必须只输出严格 JSON，不要输出 Markdown 或解释。"
)

_FAST_STOPWORDS = {
    "a",
    "an",
    "and",
    "are",
    "for",
    "the",
    "this",
    "that",
    "you",
    "your",
    "me",
    "my",
    "我",
    "你",
    "他",
    "她",
    "它",
    "们",
    "的",
    "了",
    "啊",
    "呀",
    "吧",
    "呢",
    "吗",
    "嘛",
    "呗",
    "请",
    "求",
    "有",
    "给",
    "给我",
    "帮我",
    "看看",
    "找",
    "发",
    "发个",
    "发张",
    "来",
    "来个",
    "来张",
    "来点",
    "来一张",
    "一张",
    "一下",
    "这个",
    "那个",
    "图片",
    "图",
    "表情",
    "表情包",
    "照片",
}

_FAST_GENERIC_REQUEST_TERMS = {
    "图片",
    "图",
    "表情",
    "表情包",
    "照片",
    "梗图",
    "发图",
}

_FAST_REQUEST_PREFIXES = (
    "给我来一张",
    "给我来一个",
    "给我来个",
    "给我来张",
    "帮我来一张",
    "帮我来个",
    "帮我发一张",
    "帮我发个",
    "来一张",
    "来一个",
    "发一张",
    "给我",
    "帮我",
    "来个",
    "来张",
    "来点",
    "发张",
    "发个",
    "整点",
    "搞点",
)

_FAST_EMOTION_TAGS = {
    "positive": {
        "cues": ("哈哈", "笑死", "好笑", "开心", "快乐", "乐", "喜", "赞", "牛"),
        "tags": ("笑", "大笑", "开心", "快乐", "搞笑", "欢乐", "可爱", "赞", "牛"),
    },
    "sad": {
        "cues": ("难过", "伤心", "哭", "委屈", "破防", "emo", "悲"),
        "tags": ("哭", "流泪", "伤心", "难过", "委屈", "破防", "悲伤"),
    },
    "angry": {
        "cues": ("生气", "气死", "愤怒", "烦", "怒", "火大"),
        "tags": ("生气", "愤怒", "怒", "不满", "烦躁", "吐槽"),
    },
    "shock": {
        "cues": ("震惊", "惊讶", "离谱", "不懂", "懵", "啊？", "啊?"),
        "tags": ("震惊", "惊讶", "疑惑", "懵", "离谱", "问号"),
    },
    "awkward": {
        "cues": ("尴尬", "无语", "沉默", "汗", "绷不住"),
        "tags": ("尴尬", "无语", "沉默", "流汗", "汗", "吐槽"),
    },
}

_FAST_SEMANTIC_GROUPS = {
    "thanks": {
        "cues": ("谢谢", "感谢", "辛苦", "爱你"),
        "tags": ("谢谢", "感谢", "鞠躬", "比心", "爱心", "开心", "可爱"),
    },
    "apology": {
        "cues": ("抱歉", "对不起", "不好意思", "错了"),
        "tags": ("抱歉", "对不起", "道歉", "鞠躬", "委屈"),
    },
    "agree": {
        "cues": ("可以", "没问题", "好呀", "行", "同意", "支持"),
        "tags": ("可以", "没问题", "点头", "赞", "支持", "ok"),
    },
    "reject": {
        "cues": ("不要", "不行", "拒绝", "算了", "别"),
        "tags": ("拒绝", "不行", "不要", "摇头", "无语"),
    },
    "tired": {
        "cues": ("累", "困", "困死", "疲惫", "熬夜"),
        "tags": ("累", "困", "疲惫", "睡觉", "躺平"),
    },
}


@dataclass(frozen=True)
class ProactiveFastPrefilterResult:
    candidates: list[dict[str, Any]]
    fallback_item: dict[str, Any] | None
    profile: dict[str, Any]


def build_proactive_fast_prefilter(
    user_message: str,
    candidates: list[dict[str, Any]],
) -> ProactiveFastPrefilterResult:
    profile = _fast_query_profile(user_message, candidates)
    ranked = [_score_fast_candidate(profile, item) for item in candidates]
    ranked.sort(
        key=lambda item: (
            item.get("proactive_fast_score", 0.0),
            _fallback_rank(item),
            len(item.get("proactive_fast_hints", [])),
            str(item.get("filename") or ""),
        ),
        reverse=True,
    )
    prompt_candidates = ranked[:PROACTIVE_FAST_CANDIDATE_LIMIT]
    fallback_item = select_proactive_fast_fallback(prompt_candidates)
    return ProactiveFastPrefilterResult(
        candidates=prompt_candidates,
        fallback_item=fallback_item,
        profile=profile,
    )


def build_proactive_fast_prompt(
    user_message: str,
    prefilter: ProactiveFastPrefilterResult,
) -> str:
    compact_candidates = [_fast_prompt_item(item) for item in prefilter.candidates]
    return (
        "判断是否在普通回复后追加 1 张主动表情包。\n"
        "只看用户刚才的话和候选；候选不贴切就 matched=false。\n"
        "泛化请求、无明确情绪或无明确标签需求时不要硬选。\n"
        "可返回 1-3 个 image_ids，按贴切度排序；confidence 低于 0.35 返回 false。\n\n"
        f"用户消息：\n{user_message}\n\n"
        f"本地精排：{json.dumps(prefilter.profile, ensure_ascii=False)}\n\n"
        "候选：\n"
        f"{json.dumps(compact_candidates, ensure_ascii=False)}\n\n"
        "只输出 JSON："
        "{\"matched\": true/false, \"image_ids\": [\"候选id\"], "
        "\"image_id\": \"可为空\", \"need\": \"简短语境\", "
        "\"reason\": \"简短理由\", \"confidence\": 0.0}"
    )


def select_proactive_fast_fallback(
    candidates: list[dict[str, Any]],
) -> dict[str, Any] | None:
    strong = [
        item
        for item in candidates
        if item.get("proactive_fast_fallback")
        and float(item.get("proactive_fast_score") or 0.0)
        >= PROACTIVE_FAST_FALLBACK_MIN_SCORE
    ]
    if not strong:
        return None
    top_score = float(strong[0].get("proactive_fast_score") or 0.0)
    pool = [
        item
        for item in strong
        if float(item.get("proactive_fast_score") or 0.0) >= max(0.0, top_score - 1.2)
    ][:SEARCH_SELECTION_POOL_SIZE]
    return random.choice(pool) if pool else None


def _fast_query_profile(
    user_message: str,
    candidates: list[dict[str, Any]],
) -> dict[str, Any]:
    text = str(user_message or "").strip().lower()
    search_text = _fast_search_text(text)
    terms = _fast_terms(search_text)
    tag_index = _candidate_tag_index(candidates)
    direct_tags = _direct_tag_matches(text, terms, tag_index)
    filename_terms = [term for term in terms if term not in _FAST_GENERIC_REQUEST_TERMS]
    emotion_keys = [
        key
        for key, spec in _FAST_EMOTION_TAGS.items()
        if any(cue.lower() in text for cue in spec["cues"])
    ]
    semantic_keys = [
        key
        for key, spec in _FAST_SEMANTIC_GROUPS.items()
        if any(cue.lower() in text for cue in spec["cues"])
    ]
    specific_terms = [
        term
        for term in terms
        if term not in _FAST_GENERIC_REQUEST_TERMS and term not in direct_tags
    ]
    return {
        "terms": terms,
        "direct_tags": direct_tags,
        "specific_terms": specific_terms,
        "filename_terms": filename_terms,
        "emotions": emotion_keys,
        "semantics": semantic_keys,
        "generic_request": not direct_tags and not specific_terms and not emotion_keys and not semantic_keys,
        "message_length": len(text),
    }


def _fast_search_text(text: str) -> str:
    ascii_terms = re.findall(r"[a-z0-9_\-]+", text, flags=re.I)
    compact = re.sub(r"\s+", "", text)
    if compact in _FAST_GENERIC_REQUEST_TERMS:
        return ""
    changed = True
    while compact and changed:
        changed = False
        for prefix in sorted(_FAST_REQUEST_PREFIXES, key=len, reverse=True):
            if compact.startswith(prefix):
                compact = compact[len(prefix) :]
                changed = True
                break
        if changed:
            continue
        if compact.startswith(("发", "来")) and compact[1:] in _FAST_GENERIC_REQUEST_TERMS:
            compact = compact[1:]
            changed = True
            continue
        for suffix in sorted(_FAST_GENERIC_REQUEST_TERMS, key=len, reverse=True):
            if compact.endswith(suffix):
                compact = compact[: -len(suffix)]
                changed = True
                break
    if ascii_terms:
        return " ".join([compact, *ascii_terms])
    return compact


def _fast_terms(text: str) -> list[str]:
    terms: list[str] = []
    for raw in re.findall(r"[a-z0-9_\-]+|[\u4e00-\u9fff]+", text, flags=re.I):
        token = raw.strip().lower()
        if not token or token in _FAST_STOPWORDS:
            continue
        if token not in terms:
            terms.append(token)
        if re.fullmatch(r"[\u4e00-\u9fff]{5,}", token):
            for fragment in _fast_chinese_fragments(token):
                if fragment not in terms and fragment not in _FAST_STOPWORDS:
                    terms.append(fragment)
                if len(terms) >= 16:
                    return terms[:16]
        if len(terms) >= 16:
            return terms[:16]
    return terms[:16]


def _fast_chinese_fragments(token: str) -> list[str]:
    fragments: list[str] = []
    max_size = min(4, len(token))
    for size in range(max_size, 1, -1):
        for start in range(0, len(token) - size + 1):
            fragment = token[start : start + size]
            if fragment not in fragments:
                fragments.append(fragment)
            if len(fragments) >= 8:
                return fragments
    return fragments


def _candidate_tag_index(candidates: list[dict[str, Any]]) -> set[str]:
    tags: set[str] = set()
    for item in candidates:
        for tag in _item_tags(item):
            normalized = str(tag).strip().lower()
            if normalized:
                tags.add(normalized)
    return tags


def _direct_tag_matches(
    text: str,
    terms: list[str],
    tag_index: set[str],
) -> list[str]:
    matches: list[str] = []
    for tag in sorted(tag_index, key=len, reverse=True):
        if not tag or tag in _FAST_GENERIC_REQUEST_TERMS:
            continue
        if tag in text or tag in terms:
            matches.append(tag)
        if len(matches) >= 8:
            break
    return matches


def _score_fast_candidate(
    profile: dict[str, Any],
    item: dict[str, Any],
) -> dict[str, Any]:
    scored = dict(item)
    tags = [str(tag).strip().lower() for tag in _item_tags(item) if str(tag).strip()]
    filename = str(item.get("filename") or "").lower()
    rel_path = str(item.get("rel_path") or "").lower()
    score = 0.0
    hints: list[str] = []
    fallback_reasons: list[str] = []

    direct_hits = []
    for tag in profile.get("direct_tags", []):
        if tag in tags:
            direct_hits.append(tag)
            score += 9.0
            hints.append(f"direct-tag:{tag}")
        elif any(tag in candidate_tag for candidate_tag in tags):
            direct_hits.append(tag)
            score += 7.0
            hints.append(f"direct-tag-part:{tag}")
    if direct_hits:
        score += min(len(direct_hits), 4) * 2.0
        fallback_reasons.append("direct_tag")

    filename_hits = 0
    for term in profile.get("filename_terms", []):
        if term and term in filename:
            filename_hits += 1
            score += 6.0 if len(term) >= 2 else 2.0
            hints.append(f"file:{term}")
    if filename_hits:
        fallback_reasons.append("filename")

    semantic_hits = 0
    grouped_semantic_hits = 0
    for term in profile.get("specific_terms", []):
        if not term:
            continue
        if any(term == tag for tag in tags):
            score += 6.0
            semantic_hits += 1
            hints.append(f"tag:{term}")
        elif any(term in tag for tag in tags):
            score += 4.0
            semantic_hits += 1
            hints.append(f"tag-part:{term}")
        elif term in rel_path:
            score += 2.5
            hints.append(f"path:{term}")

    for emotion_key in profile.get("emotions", []):
        spec = _FAST_EMOTION_TAGS.get(str(emotion_key), {})
        matched_tags = _matched_related_tags(tags, spec.get("tags", ()))
        if matched_tags:
            score += 4.5 + min(len(matched_tags), 3) * 1.2
            semantic_hits += len(matched_tags)
            grouped_semantic_hits += len(matched_tags)
            hints.append(f"emotion:{emotion_key}")

    for semantic_key in profile.get("semantics", []):
        spec = _FAST_SEMANTIC_GROUPS.get(str(semantic_key), {})
        matched_tags = _matched_related_tags(tags, spec.get("tags", ()))
        if matched_tags:
            score += 4.0 + min(len(matched_tags), 3) * 1.0
            semantic_hits += len(matched_tags)
            grouped_semantic_hits += len(matched_tags)
            hints.append(f"semantic:{semantic_key}")

    if semantic_hits >= 2 or grouped_semantic_hits >= 2:
        fallback_reasons.append("strong_semantic")

    if profile.get("generic_request"):
        score = min(score, 1.0)
        fallback_reasons = []

    if tags:
        score += min(len(tags), 8) * 0.03

    scored["proactive_fast_score"] = round(score, 3)
    scored["proactive_fast_hints"] = _dedupe(hints)[:6]
    scored["proactive_fast_fallback_reasons"] = _dedupe(fallback_reasons)
    scored["proactive_fast_fallback"] = bool(fallback_reasons)
    return scored


def _matched_related_tags(
    candidate_tags: list[str],
    related_tags: Any,
) -> list[str]:
    matches: list[str] = []
    for related in related_tags:
        text = str(related).strip().lower()
        if not text:
            continue
        if any(text in tag or tag in text for tag in candidate_tags):
            matches.append(text)
    return _dedupe(matches)


def _fallback_rank(item: dict[str, Any]) -> int:
    reasons = item.get("proactive_fast_fallback_reasons", [])
    if not isinstance(reasons, list):
        return 0
    if "direct_tag" in reasons:
        return 3
    if "filename" in reasons:
        return 2
    if "strong_semantic" in reasons:
        return 1
    return 0


def _fast_prompt_item(item: dict[str, Any]) -> dict[str, Any]:
    return {
        "id": str(item.get("id") or ""),
        "filename": str(item.get("filename") or ""),
        "tags": _item_tags(item)[:10],
        "score": item.get("proactive_fast_score", 0.0),
        "hints": item.get("proactive_fast_hints", [])[:5],
    }


def _item_tags(item: dict[str, Any]) -> list[str]:
    tags: list[str] = []
    for key in ("tags", "auto_tags", "manual_tags", "selected_global_tags"):
        value = item.get(key, [])
        if isinstance(value, (list, tuple, set)):
            for raw in value:
                text = str(raw or "").strip()
                if text and text not in tags:
                    tags.append(text)
    return tags


def _dedupe(values: list[str]) -> list[str]:
    result: list[str] = []
    for value in values:
        if value and value not in result:
            result.append(value)
    return result
