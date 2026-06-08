from .common import Any, GLOBAL_TAGS_CONFIG_KEY, Path, re


class TaggingMixin:
    def _extract_tags(self, text: str, limit: int = 7) -> list[str]:
        parsed = self._loads_json_object(text)
        if isinstance(parsed, list):
            raw_tags = parsed
        elif isinstance(parsed, dict):
            raw_tags = parsed.get("tags") or parsed.get("标签") or []
        else:
            raw_tags = re.split(r"[,\n，、；; ]+", text)
        return self._normalize_tags(raw_tags)[:limit]

    def _normalize_ids(self, raw_ids: Any) -> list[str]:
        if isinstance(raw_ids, str):
            raw_ids = re.split(r"[,\n，、；; ]+", raw_ids)
        if not isinstance(raw_ids, list):
            return []
        ids = []
        for raw_id in raw_ids:
            image_id = str(raw_id).strip()
            if image_id and image_id not in ids:
                ids.append(image_id)
        return ids

    def _tags_from_item(self, item: dict[str, Any]) -> list[str]:
        auto_tags = self._normalize_tags(item.get("auto_tags", []))
        manual_tags = self._normalize_tags(item.get("manual_tags", []))
        selected_global_tags = self._valid_global_tags(
            item.get("selected_global_tags", [])
        )
        if item.get("manual_tags_override"):
            return self._merge_tags(manual_tags, selected_global_tags)
        if auto_tags or manual_tags or selected_global_tags:
            return self._merge_tags(auto_tags, manual_tags, selected_global_tags)
        return self._normalize_tags(item.get("tags", []))

    def _global_tags(self) -> list[str]:
        return self._normalize_tags(self._config_get(GLOBAL_TAGS_CONFIG_KEY, []))

    def _valid_global_tags(self, raw_tags: Any) -> list[str]:
        global_tags = set(self._global_tags())
        return [tag for tag in self._normalize_tags(raw_tags) if tag in global_tags]

    def _merge_tags(self, *tag_groups: Any) -> list[str]:
        merged = []
        for group in tag_groups:
            for tag in self._normalize_tags(group):
                if tag not in merged:
                    merged.append(tag)
        return merged

    def _normalize_tags(self, raw_tags: Any) -> list[str]:
        if isinstance(raw_tags, str):
            raw_tags = re.split(r"[,\n，、；; ]+", raw_tags)
        if not isinstance(raw_tags, list):
            return []
        tags = []
        for tag in raw_tags:
            tag_text = str(tag).strip(" \t\r\n\"'`，。；;、")
            if tag_text and tag_text not in tags:
                tags.append(tag_text)
        return tags

    def _normalize_caption_tags(self, raw_tags: Any, filename: str) -> list[str]:
        tags = self._normalize_tags(raw_tags)
        if not tags:
            tags = self._filename_tags(filename)

        use_image_type = self._caption_category_enabled("image_type")
        use_image_text = self._caption_category_enabled("image_text")
        normalized = []
        image_type_count = 0
        if use_image_type:
            base_type = self._choose_base_image_type(tags, filename)
            normalized.append(base_type)
            image_type_count = 1

        for tag in tags:
            if tag in {"照片", "表情包"}:
                continue
            is_type_tag = self._is_image_type_tag(tag)
            if is_type_tag and not use_image_type:
                continue
            if use_image_type and is_type_tag and image_type_count >= 2:
                continue
            if is_type_tag:
                image_type_count += 1
            normalized.append(tag)
            if len(normalized) >= 7:
                break

        if len(normalized) < 5:
            for tag in self._filename_tags(filename):
                if tag in {"照片", "表情包"}:
                    continue
                if not use_image_type and self._is_image_type_tag(tag):
                    continue
                if tag not in normalized:
                    normalized.append(tag)
                if len(normalized) >= 5:
                    break

        for tag in tags:
            if tag in normalized:
                continue
            if use_image_text and self._looks_like_text_content_tag(tag):
                normalized.append(tag)
                break

        if not normalized:
            normalized.append("未分类")

        return normalized[:8]

    def _looks_like_text_content_tag(self, tag: str) -> bool:
        if any(prefix in tag for prefix in ("文字", "文本", "台词", "字幕", "内容", "标语")):
            return False
        return len(tag) >= 4 and bool(re.search(r"[\u4e00-\u9fffA-Za-z0-9]", tag))

    def _choose_base_image_type(self, tags: list[str], filename: str) -> str:
        if "表情包" in tags:
            return "表情包"
        if "照片" in tags:
            return "照片"
        text = f"{filename} {' '.join(tags)}".lower()
        meme_words = ("表情", "meme", "梗图", "斗图", "emoji", "gif")
        return "表情包" if any(word in text for word in meme_words) else "照片"

    def _is_image_type_tag(self, tag: str) -> bool:
        type_keywords = (
            "照片",
            "表情包",
            "图片",
            "插画",
            "漫画",
            "截图",
            "动图",
            "自拍",
            "头像",
            "壁纸",
            "海报",
            "二次元",
            "写实",
            "手绘",
        )
        return any(keyword in tag for keyword in type_keywords)

    def _filename_tags(self, filename: str) -> list[str]:
        stem = Path(filename).stem
        tokens = re.split(r"[_\-\s,，、.]+", stem)
        tags = [token for token in tokens if token]
        return (["图片"] + tags)[:7]

