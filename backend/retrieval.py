from .common import (
    Any,
    AstrMessageEvent,
    CaptionGenerationError,
    COLLECTED_LIBRARY_SOURCE,
    DEFAULT_CAPTION_PROVIDER_CONFIG_KEY,
    Image,
    MessageEventResult,
    PENDING_PROACTIVE_EMOJI_EXTRA_KEY,
    Path,
    PROACTIVE_EMOJI_DECISION_EXTRA_KEY,
    SEARCH_CANDIDATE_LIMIT,
    SEARCH_QUERY_STOPWORDS,
    SEARCH_SELECTION_POOL_SIZE,
    SKIP_PROACTIVE_EMOJI_EXTRA_KEY,
    TAG_CATEGORY_CONFIG_KEY,
    USER_SEARCH_CONFIG_KEY,
    json,
    logger,
    random,
    re,
    traceback,
)


class RetrievalMixin:
    def _library_candidates(self) -> list[dict[str, Any]]:
        candidates = []
        images = self._index.get("images", {})
        if not isinstance(images, dict):
            return candidates
        hidden_rel_paths = self._hidden_rel_paths()

        for item in images.values():
            if not isinstance(item, dict):
                continue
            rel_path = self._norm_rel_path(item.get("rel_path"))
            if not rel_path:
                continue
            if item.get("caption_status") != "done":
                continue
            if (
                self._library_source_for_rel_path(rel_path, item)
                == COLLECTED_LIBRARY_SOURCE
                and not self._auto_collection_config().get("include_in_features")
            ):
                continue
            if rel_path in hidden_rel_paths:
                continue
            path = self._abs_plugin_data_path(rel_path)
            if not path.is_file():
                continue
            candidates.append(
                {
                    "id": item.get("id") or self._image_id(rel_path),
                    "filename": item.get("filename") or path.name,
                    "rel_path": rel_path,
                    "tags": self._tags_from_item(item),
                    "auto_tags": self._normalize_tags(item.get("auto_tags", [])),
                    "manual_tags": self._normalize_tags(item.get("manual_tags", [])),
                    "selected_global_tags": self._valid_global_tags(
                        item.get("selected_global_tags", [])
                    ),
                }
            )
        return candidates

    def _search_query_terms(self, message: str) -> list[str]:
        text = (message or "").strip().lower()
        if not text:
            return []

        for stopword in sorted(SEARCH_QUERY_STOPWORDS, key=len, reverse=True):
            if stopword:
                text = text.replace(stopword.lower(), " ")
        text = re.sub(r"[^\w\u4e00-\u9fff]+", " ", text)

        terms: list[str] = []
        for raw_term in text.split():
            raw_term = raw_term.strip()
            if not raw_term or raw_term in SEARCH_QUERY_STOPWORDS:
                continue
            if raw_term not in terms:
                terms.append(raw_term)
            if re.fullmatch(r"[\u4e00-\u9fff]{5,}", raw_term):
                for extra_term in self._split_chinese_term(raw_term):
                    if extra_term not in terms:
                        terms.append(extra_term)
                    if len(terms) >= 12:
                        return terms[:12]
        return terms[:12]

    def _split_chinese_term(self, term: str) -> list[str]:
        if not re.fullmatch(r"[\u4e00-\u9fff]{5,}", term):
            return []
        fragments: list[str] = []
        max_len = min(4, len(term))
        for size in range(max_len, 1, -1):
            for start in range(0, len(term) - size + 1):
                fragment = term[start : start + size]
                if fragment in SEARCH_QUERY_STOPWORDS or fragment in fragments:
                    continue
                fragments.append(fragment)
                if len(fragments) >= 8:
                    return fragments
        return fragments

    def _looks_like_name_query_term(self, term: str) -> bool:
        if not term or term in SEARCH_QUERY_STOPWORDS:
            return False
        if re.fullmatch(r"[a-z][a-z0-9_\-]{1,19}", term):
            return True
        if not re.fullmatch(r"[\u4e00-\u9fff]{2,4}", term):
            return False
        blocked = (
            "照片",
            "图片",
            "表情",
            "美图",
            "头像",
            "壁纸",
            "截图",
            "风景",
            "文字",
            "内容",
            "表格",
            "聊天",
            "搞笑",
            "可爱",
            "照片",
        )
        return not any(word in term for word in blocked)

    def _search_candidate_text(self, item: dict[str, Any]) -> str:
        pieces = [
            str(item.get("filename", "")),
            str(item.get("rel_path", "")),
        ]
        pieces.extend(self._normalize_tags(item.get("tags", [])))
        pieces.extend(self._normalize_tags(item.get("auto_tags", [])))
        pieces.extend(self._normalize_tags(item.get("manual_tags", [])))
        pieces.extend(self._valid_global_tags(item.get("selected_global_tags", [])))
        normalized = []
        for piece in pieces:
            text = str(piece).strip().lower()
            if text and text not in normalized:
                normalized.append(text)
        return " ".join(normalized)

    def _rank_search_candidates(
        self,
        message: str,
        candidates: list[dict[str, Any]],
    ) -> tuple[dict[str, Any], list[dict[str, Any]]]:
        profile = self._search_query_profile(message)
        scored: list[dict[str, Any]] = []
        for item in candidates:
            score, hints = self._search_candidate_score(profile, item)
            scored.append(
                {
                    **item,
                    "search_score": round(score, 3),
                    "search_hints": hints,
                }
            )
        scored.sort(
            key=lambda item: (
                item.get("search_score", 0.0),
                len(item.get("search_hints", [])),
                item.get("filename", ""),
            ),
            reverse=True,
        )
        return profile, scored[:SEARCH_CANDIDATE_LIMIT]

    def _search_prompt_item(self, item: dict[str, Any]) -> dict[str, Any]:
        return {
            "id": item["id"],
            "filename": item["filename"],
            "tags": item["tags"],
            "score": item.get("search_score", 0.0),
            "hints": item.get("search_hints", []),
        }

    async def _maybe_append_proactive_emoji(self, event: AstrMessageEvent) -> None:
        if event.get_extra(SKIP_PROACTIVE_EMOJI_EXTRA_KEY, False):
            return
        if event.get_extra(PROACTIVE_EMOJI_DECISION_EXTRA_KEY, False):
            return
        cfg = self._proactive_emoji_config()
        if not cfg["enabled"]:
            return

        result = event.get_result()
        if not isinstance(result, MessageEventResult) or not result.is_llm_result():
            return
        reply_text = result.get_plain_text().strip()
        if not reply_text:
            return
        if any(isinstance(comp, Image) for comp in result.chain):
            return

        event.set_extra(PROACTIVE_EMOJI_DECISION_EXTRA_KEY, True)
        probability = self._to_float(cfg.get("trigger_probability"), 0.25)
        if probability <= 0 or random.random() > probability:
            return

        await self._sync_library(caption_mode="none")
        candidates = self._proactive_emoji_candidates(bool(cfg["meme_only"]))
        if not candidates:
            return

        try:
            decision = await self._analyze_proactive_emoji(
                event,
                reply_text,
                candidates,
                str(cfg.get("analysis_provider_id") or ""),
            )
            image_item = self._select_proactive_emoji(decision, candidates)
            if not image_item:
                return
            image_path = self._abs_plugin_data_path(image_item["rel_path"])
            if image_path.is_file():
                if cfg["embed_in_conversation"]:
                    result.chain.append(Image.fromFileSystem(str(image_path)))
                    await self._after_plugin_sent_image_for_meme_combat(
                        event,
                        str(image_path),
                        source="proactive_emoji",
                        defer_burst=True,
                    )
                else:
                    event.set_extra(
                        PENDING_PROACTIVE_EMOJI_EXTRA_KEY,
                        {"image_path": str(image_path)},
                    )
        except Exception as exc:
            logger.warning(
                "astrbot_plugin_smart_imagechat_hub: proactive emoji selection failed: %s",
                exc,
                exc_info=True,
            )

    async def _send_pending_proactive_emoji(self, event: AstrMessageEvent) -> None:
        pending = event.get_extra(PENDING_PROACTIVE_EMOJI_EXTRA_KEY)
        if not isinstance(pending, dict):
            return
        event.set_extra(PENDING_PROACTIVE_EMOJI_EXTRA_KEY, None)
        image_path = Path(str(pending.get("image_path") or ""))
        if not image_path.is_file():
            return
        try:
            await event.send(MessageEventResult().file_image(str(image_path)))
            await self._after_plugin_sent_image_for_meme_combat(
                event,
                str(image_path),
                source="proactive_emoji",
            )
        except Exception as exc:
            logger.warning(
                "astrbot_plugin_smart_imagechat_hub: failed to send proactive emoji image: %s",
                exc,
                exc_info=True,
            )

    def _proactive_emoji_candidates(self, meme_only: bool) -> list[dict[str, Any]]:
        candidates = self._library_candidates()
        if not meme_only:
            return candidates
        return [
            item
            for item in candidates
            if "表情包" in self._normalize_tags(item.get("tags", []))
        ]

    async def _analyze_proactive_emoji(
        self,
        event: AstrMessageEvent,
        reply_text: str,
        candidates: list[dict[str, Any]],
        provider_id: str,
    ) -> dict[str, Any]:
        prompt = self._proactive_emoji_prompt(reply_text, candidates)
        resp = await self._llm_generate_with_provider_fallback(
            primary_provider_id=provider_id,
            umo=event.unified_msg_origin,
            use_current_when_primary_empty=True,
            operation_name="proactive emoji analysis",
            timeout_seconds=None,
            prompt=prompt,
            contexts=[],
            system_prompt=(
                "你是 AstrBot 的本地表情包语境匹配器。"
                "你必须只输出严格 JSON，不要输出 Markdown 或解释。"
            ),
        )
        return self._parse_decision(resp.completion_text)

    def _proactive_emoji_prompt(
        self,
        reply_text: str,
        candidates: list[dict[str, Any]],
    ) -> str:
        compact_candidates = [self._search_prompt_item(item) for item in candidates]
        return (
            "请在一次请求中完成两件事：\n"
            "1. 分析 bot 即将发送的 LLM 回复的语义、情绪、语气和适合追加的表情包氛围；\n"
            "2. 根据图库候选的特征标签，判断是否存在符合语境的表情包或图片。\n"
            "如果有多个候选都符合，请把这些候选 id 都放入 image_ids。\n\n"
            "bot 的 LLM 回复：\n"
            f"{reply_text}\n\n"
            "图库候选：\n"
            f"{json.dumps(compact_candidates, ensure_ascii=False)}\n\n"
            "输出严格 JSON，格式如下：\n"
            "{\"matched\": true/false, \"image_ids\": [\"候选 id\"], \"image_id\": \"兼容字段，可填首个候选 id 或空字符串\", "
            "\"need\": \"适合的表情包语境摘要\", \"reason\": \"简短理由\", "
            "\"confidence\": 0.0}\n"
            "只有当图库中确实有图片适合追加到这条回复后面时 matched 才为 true。"
        )

    def _select_proactive_emoji(
        self,
        decision: dict[str, Any],
        candidates: list[dict[str, Any]],
    ) -> dict[str, Any] | None:
        if not decision.get("matched"):
            return None
        if self._to_float(decision.get("confidence"), 0.0) < 0.35:
            return None
        candidate_by_id = {str(item["id"]): item for item in candidates}
        image_ids = self._normalize_ids(decision.get("image_ids", []))
        fallback_id = str(decision.get("image_id") or "").strip()
        if fallback_id and fallback_id not in image_ids:
            image_ids.append(fallback_id)
        matched_items = [
            candidate_by_id[image_id]
            for image_id in image_ids
            if image_id in candidate_by_id
        ]
        return random.choice(matched_items) if matched_items else None

    def _hidden_rel_paths(self) -> set[str]:
        rel_paths = set()
        raw_items = self.config.get("hidden_images", [])
        if not isinstance(raw_items, list):
            return rel_paths
        for raw in raw_items:
            rel_path = self._norm_rel_path(raw)
            if rel_path:
                rel_paths.add(rel_path)
        return rel_paths

    async def _caption_image(self, image_path: Path) -> list[str]:
        provider_id = self._default_image_caption_provider_id()
        if not provider_id:
            logger.warning(
                "astrbot_plugin_smart_imagechat_hub: "
                "default image caption provider is not configured; "
                "fallback providers will be used when available."
            )

        category_labels = self._caption_category_labels()
        category_text = "、".join(category_labels) if category_labels else "基础图像内容"
        category_rules = self._caption_category_prompt_rules()
        prepared_image_path, cleanup_paths = await self._prepare_caption_image_input(
            image_path
        )
        prompt = (
            "请为这张图片生成 5-7 个简短中文特征标签；如果图片中包含可辨认文字，"
            "再额外生成 1 个仅包含图片中文字内容的标签。\n"
            f"本次应优先基于这些标签类别生成：{category_text}。\n"
            "规则：\n"
            f"{category_rules}\n"
            "不要生成露骨、色情、未成年人性化或隐私推断类标签。\n"
            "只输出 JSON 数组字符串，例如 [\"照片\", \"黑发\", \"微笑\", \"身材匀称\", \"今天也要开心\"]。"
            "不要输出解释，不要输出 Markdown。"
        )
        try:
            resp = await self._run_image_caption_provider_request(
                lambda: self._llm_generate_with_provider_fallback(
                    primary_provider_id=provider_id,
                    operation_name=f"image caption {image_path.name}",
                    timeout_seconds=None,
                    allow_no_provider=True,
                    use_failure_cooldown=False,
                    direct_provider_call=True,
                    prompt=prompt,
                    image_urls=[prepared_image_path],
                    contexts=[],
                    system_prompt="",
                )
            )
            if resp is None:
                logger.warning(
                    "astrbot_plugin_smart_imagechat_hub: no available provider for image caption; "
                    "using filename fallback tags for %s.",
                    image_path.name,
                )
                return self._normalize_caption_tags([], image_path.name)
            completion_text = str(getattr(resp, "completion_text", "") or "")
            tags = self._extract_tags(completion_text, limit=8)
            return self._normalize_caption_tags(tags, image_path.name)
        except CaptionGenerationError:
            raise
        except Exception as exc:
            detail = "".join(
                traceback.format_exception(type(exc), exc, exc.__traceback__)
            )
            logger.error(
                "astrbot_plugin_smart_imagechat_hub: image caption failed for %s: %s",
                image_path,
                exc,
                exc_info=True,
            )
            raise CaptionGenerationError(
                f"Image caption generation failed for {image_path.name}: {exc}",
                detail=detail,
            ) from exc
        finally:
            for temp_path in cleanup_paths:
                try:
                    if temp_path != image_path and temp_path.is_file():
                        temp_path.unlink(missing_ok=True)
                except Exception:
                    pass

    def _search_query_profile(self, message: str) -> dict[str, Any]:
        terms = self._search_query_terms(message)
        lowered_message = (message or "").lower()
        type_terms = [
            term
            for term in ["表情包", "照片", "图片", "美图", "梗图", "头像", "壁纸"]
            if term in lowered_message
        ]
        name_terms = [
            term
            for term in terms
            if term not in type_terms and self._looks_like_name_query_term(term)
        ]
        return {
            "raw": message,
            "terms": terms,
            "name_terms": name_terms,
            "type_terms": type_terms,
        }

    def _search_candidate_score(
        self,
        profile: dict[str, Any],
        item: dict[str, Any],
    ) -> tuple[float, list[str]]:
        candidate_text = self._search_candidate_text(item)
        filename = str(item.get("filename", "")).lower()
        tags = [str(tag).lower() for tag in self._tags_from_item(item)]
        score = 0.0
        hints: list[str] = []
        name_terms = profile.get("name_terms", [])
        type_terms = profile.get("type_terms", [])
        query_terms = profile.get("terms", [])

        for term in name_terms:
            if term in candidate_text:
                score += 8.0
                hints.append(f"name:{term}")
            elif term in filename:
                score += 5.0
                hints.append(f"name-file:{term}")
            elif any(term in tag for tag in tags):
                score += 5.0
                hints.append(f"name-tag:{term}")
            elif any(
                tag in {"人物", "角色", "人名", "姓名", "昵称", "称呼"}
                for tag in tags
            ):
                score += 1.5
                hints.append("name-related-tag")

        for term in query_terms:
            if not term or term in name_terms:
                continue
            if term in candidate_text:
                score += 4.0 if len(term) >= 2 else 2.0
                hints.append(f"match:{term}")
            elif term in filename:
                score += 2.0
                hints.append(f"file:{term}")
            elif any(term in tag for tag in tags):
                score += 3.0
                hints.append(f"tag:{term}")

        for term in type_terms:
            if any(term in tag for tag in tags) or term in filename:
                score += 2.0
                hints.append(f"type:{term}")

        if not query_terms and not type_terms:
            score += 0.1

        score += min(len(self._tags_from_item(item)), 8) * 0.03
        return score, self._merge_tags(hints)[:6]

    async def _analyze_request(
        self,
        event: AstrMessageEvent,
        message: str,
        profile: dict[str, Any],
        candidates: list[dict[str, Any]],
    ) -> dict[str, Any]:
        provider_id = await self.context.get_current_chat_provider_id(
            event.unified_msg_origin
        )
        resp = await self._llm_generate_with_provider_fallback(
            primary_provider_id=provider_id,
            umo=event.unified_msg_origin,
            use_current_when_primary_empty=True,
            operation_name="image search request analysis",
            timeout_seconds=12,
            prompt=self._match_prompt(message, profile, candidates),
            contexts=[],
            system_prompt=(
                "你是 AstrBot 的本地图片检索器。只能输出严格 JSON，"
                "不要输出 Markdown、解释或多余文本。"
            ),
        )
        return self._parse_decision(resp.completion_text)

    def _match_prompt(
        self,
        message: str,
        profile: dict[str, Any],
        candidates: list[dict[str, Any]],
    ) -> str:
        compact_candidates = [self._search_prompt_item(item) for item in candidates]
        return (
            "请在一次请求中完成图片检索决策。\n"
            "1. 先理解用户需求，再看候选图片。候选中的 tags 已经合并了自动标签、手动标签和公用标签。\n"
            "2. 如果用户输入里出现像名字、昵称、称呼、角色名的词，优先匹配候选里文件名或标签中对应的名字字段、人物字段、角色字段或相关字段。\n"
            "3. 只从最相关的少量候选里选图，输出 1-"
            f"{SEARCH_SELECTION_POOL_SIZE} 个最相关的 image_ids，按相关性从高到低排序；如果只有 1 张最合适，就只给 1 个。\n"
            "4. matched 只有在候选里确实存在足够合适的图片时才为 true。\n"
            "5. confidence 表示“这些候选里确实有合适图片”的把握，范围 0-1。\n"
            "6. need 写简短的用户需求摘要，reason 写简短理由。\n\n"
            f"查询画像：{json.dumps(profile, ensure_ascii=False)}\n\n"
            f"用户消息：{message}\n\n"
            "候选图片（已按本地轻量规则预排，只需在这些图里选）：\n"
            f"{json.dumps(compact_candidates, ensure_ascii=False)}\n\n"
            "输出严格 JSON，格式如下：\n"
            "{\"matched\": true/false, \"image_ids\": [\"候选id\"], "
            "\"image_id\": \"image_ids 中的首个候选id\", "
            "\"need\": \"用户需求摘要\", \"reason\": \"简短理由\", \"confidence\": 0.0}\n"
        )

    def _parse_decision(self, text: str) -> dict[str, Any]:
        data = self._loads_json_object(text)
        if not isinstance(data, dict):
            raise ValueError(f"LLM did not return a JSON object: {text!r}")
        image_ids = self._normalize_ids(data.get("image_ids", []))
        fallback_id = str(data.get("image_id") or "").strip()
        if fallback_id and fallback_id not in image_ids:
            image_ids.append(fallback_id)
        image_ids = image_ids[:SEARCH_SELECTION_POOL_SIZE]
        return {
            "matched": bool(data.get("matched")),
            "image_id": image_ids[0] if image_ids else fallback_id,
            "image_ids": image_ids,
            "need": str(data.get("need") or "").strip(),
            "reason": str(data.get("reason") or "").strip(),
            "confidence": self._to_float(data.get("confidence"), 0.0),
        }

    def _select_image(
        self,
        decision: dict[str, Any],
        candidates: list[dict[str, Any]],
    ) -> dict[str, Any] | None:
        if not decision.get("matched"):
            return None
        min_confidence = self._cfg_float("match_confidence_threshold")
        if self._to_float(decision.get("confidence"), 1.0) < min_confidence:
            return None

        candidate_by_id = {str(item["id"]): item for item in candidates}
        image_ids = self._normalize_ids(decision.get("image_ids", []))
        fallback_id = str(decision.get("image_id") or "").strip()
        if fallback_id and fallback_id not in image_ids:
            image_ids.append(fallback_id)
        matched_items = [
            candidate_by_id[image_id]
            for image_id in image_ids[:SEARCH_SELECTION_POOL_SIZE]
            if image_id in candidate_by_id
        ]
        return random.choice(matched_items) if matched_items else None

    def _fallback_match(self, candidates: list[dict[str, Any]]) -> dict[str, Any] | None:
        scored_items = [
            item
            for item in candidates
            if self._to_float(item.get("search_score"), 0.0) > 0
        ]
        if not scored_items:
            return None
        top_score = max(
            self._to_float(item.get("search_score"), 0.0)
            for item in scored_items
        )
        pool = [
            item
            for item in scored_items
            if self._to_float(item.get("search_score"), 0.0)
            >= max(0.1, top_score - 0.8)
        ][:SEARCH_SELECTION_POOL_SIZE]
        return random.choice(pool) if pool else None

    def _render_custom_reply(self, item: dict[str, Any], decision: dict[str, Any]) -> str:
        template = self._cfg_str("custom_reply")
        values = {
            "filename": item.get("filename", ""),
            "tags": "、".join(self._tags_from_item(item)),
            "need": decision.get("need", ""),
            "reason": decision.get("reason", ""),
        }
        try:
            return template.format(**values)
        except Exception:
            return template

    def _found_prompt(
        self,
        message: str,
        item: dict[str, Any],
        decision: dict[str, Any],
    ) -> str:
        return (
            "用户刚刚请求机器人发送一张图片。"
            "你已经从本地图片库中找到了匹配图片，并且系统会在你的回复之后发送该图片。"
            "请用符合你当前人格的自然语气，简短告诉用户已经找到了对应图片。"
            "不要声称你正在生成图片，不要复述完整标签，不要输出 Markdown。\n\n"
            f"用户原话：{message}\n"
            f"匹配图片文件名：{item.get('filename', '')}\n"
            f"图片标签：{'、'.join(self._tags_from_item(item))}\n"
            f"匹配理由：{decision.get('reason', '')}"
        )

    def _not_found_prompt(self, message: str, candidates: list[dict[str, Any]]) -> str:
        return (
            "用户请求机器人发送图片，但本地图片库中没有找到足够符合要求的图片。"
            "请用符合你当前人格的自然语气，简短告诉用户目前没有找到合适图片。"
            "不要编造已经发送图片。\n\n"
            f"用户原话：{message}\n"
            f"图库数量：{len(candidates)}"
        )

    def _has_request_keyword(self, message: str) -> bool:
        keywords = self._request_keywords()
        return any(keyword in message for keyword in keywords)

    def _request_keywords(self) -> list[str]:
        raw_group = self.config.get(USER_SEARCH_CONFIG_KEY, {})
        if isinstance(raw_group, dict):
            keywords = raw_group.get("request_keywords", [])
        else:
            keywords = []
        if not keywords:
            keywords = self.config.get("request_keywords", [])
        if not isinstance(keywords, list):
            keywords = []
        keywords = [str(k).strip() for k in keywords if str(k).strip()]
        if not keywords:
            keywords = ["照片", "表情包", "美图", "图片"]
        return keywords

    def _set_user_search_config(
        self,
        enabled: Any = None,
        keywords: Any = None,
    ) -> None:
        current = self.config.get(USER_SEARCH_CONFIG_KEY, {})
        current = dict(current) if isinstance(current, dict) else {}
        if enabled is not None:
            current["enabled"] = self._to_bool(enabled, True)
            self.config["user_search_enabled"] = current["enabled"]
        if keywords is not None:
            current["request_keywords"] = self._normalize_tags(keywords) or [
                "照片",
                "表情包",
                "美图",
                "图片",
            ]
            self.config["request_keywords"] = current["request_keywords"]
        self.config[USER_SEARCH_CONFIG_KEY] = current

    def _ensure_caption_provider_setting_initialized(self) -> None:
        raw = self.config.get(TAG_CATEGORY_CONFIG_KEY, {})
        if not isinstance(raw, dict):
            raw = {}
        provider_ids = self._available_chat_provider_ids()
        provider_id = str(
            self.config.get(DEFAULT_CAPTION_PROVIDER_CONFIG_KEY) or ""
        ).strip()
        if provider_id and provider_id not in provider_ids:
            provider_id = ""
        if not provider_id:
            provider_id = str(
                raw.get(DEFAULT_CAPTION_PROVIDER_CONFIG_KEY) or ""
            ).strip()
            if provider_id and provider_id not in provider_ids:
                provider_id = ""
        system_provider_id = self._system_default_image_caption_provider_id()
        if system_provider_id and system_provider_id not in provider_ids:
            system_provider_id = ""
        if not provider_id and system_provider_id:
            provider_id = system_provider_id
        if provider_id:
            self._set_system_default_image_caption_provider_id(provider_id)
        if not provider_id:
            return
        self.config[DEFAULT_CAPTION_PROVIDER_CONFIG_KEY] = provider_id
        if raw.get(DEFAULT_CAPTION_PROVIDER_CONFIG_KEY) == provider_id:
            self._save_plugin_config()
            return
        raw = dict(raw)
        raw[DEFAULT_CAPTION_PROVIDER_CONFIG_KEY] = provider_id
        self.config[TAG_CATEGORY_CONFIG_KEY] = self._tag_category_settings_for_storage(
            raw
        )
        self._save_plugin_config()

    def _caption_provider_id_for_ui(self) -> str:
        provider_ids = self._available_chat_provider_ids()
        provider_id = str(
            self.config.get(DEFAULT_CAPTION_PROVIDER_CONFIG_KEY) or ""
        ).strip()
        if provider_id and provider_id in provider_ids:
            return provider_id
        raw = self.config.get(TAG_CATEGORY_CONFIG_KEY, {})
        if isinstance(raw, dict) and DEFAULT_CAPTION_PROVIDER_CONFIG_KEY in raw:
            provider_id = str(raw.get(DEFAULT_CAPTION_PROVIDER_CONFIG_KEY) or "").strip()
            if provider_id and provider_id in provider_ids:
                return provider_id
        provider_id = self._system_default_image_caption_provider_id()
        return provider_id if provider_id in provider_ids else ""

    def _available_chat_provider_ids(self) -> set[str]:
        return {
            str(option.get("id") or "").strip()
            for option in self._chat_provider_options()
            if str(option.get("id") or "").strip()
        }

    def _set_plugin_default_image_caption_provider_id(self, provider_id: str) -> None:
        raw = self.config.get(TAG_CATEGORY_CONFIG_KEY, {})
        raw = dict(raw) if isinstance(raw, dict) else {}
        provider_id = str(provider_id or "").strip()
        self.config[DEFAULT_CAPTION_PROVIDER_CONFIG_KEY] = provider_id
        raw[DEFAULT_CAPTION_PROVIDER_CONFIG_KEY] = provider_id
        self.config[TAG_CATEGORY_CONFIG_KEY] = self._tag_category_settings_for_storage(
            raw
        )

    def _set_system_default_image_caption_provider_id(self, provider_id: str) -> None:
        cfg = self.context.get_config()
        if not cfg:
            return
        provider_settings = cfg.setdefault("provider_settings", {})
        if not isinstance(provider_settings, dict):
            provider_settings = {}
            cfg["provider_settings"] = provider_settings
        provider_id = str(provider_id or "").strip()
        if str(provider_settings.get("default_image_caption_provider_id") or "") == provider_id:
            return
        provider_settings["default_image_caption_provider_id"] = provider_id
        save_config = getattr(cfg, "save_config", None)
        if callable(save_config):
            save_config()

    def _system_default_image_caption_provider_id(self) -> str:
        cfg = self.context.get_config()
        provider_settings = cfg.get("provider_settings", {}) if cfg else {}
        if not isinstance(provider_settings, dict):
            return ""
        return str(provider_settings.get("default_image_caption_provider_id") or "")

    def _default_image_caption_provider_id(self) -> str:
        provider_id = self._caption_provider_id_for_ui()
        if provider_id:
            self._set_system_default_image_caption_provider_id(provider_id)
        return provider_id

