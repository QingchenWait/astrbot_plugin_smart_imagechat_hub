from .common import (
    AUTO_COLLECTION_CONFIG_KEY,
    Any,
    DEFAULT_CAPTION_PROVIDER_CONFIG_KEY,
    IMAGE_TAGS_CONFIG_KEY,
    MANUAL_LIBRARY_SOURCE,
    MEME_COMBAT_CONFIG_KEY,
    PROACTIVE_EMOJI_CONFIG_KEY,
    PROGRESS_LINK_CONFIG_KEY,
    PROGRESS_PAGE_CONFIG_VALUE,
    SCHEDULED_BACKUP_CONFIG_KEY,
    SEND_IMAGE_STYLE_CONFIG_KEY,
    TAG_CATEGORY_CONFIG_KEY,
    json,
    logger,
    time,
)


class ConfigSchemaMixin:
    def _load_index(self) -> dict[str, Any]:
        if not self.index_path.is_file():
            return {"version": 1, "images": {}}
        try:
            with open(self.index_path, encoding="utf-8-sig") as f:
                data = json.load(f)
            if not isinstance(data, dict):
                raise ValueError("index root is not object")
            data.setdefault("version", 1)
            data.setdefault("images", {})
            if not isinstance(data["images"], dict):
                data["images"] = {}
            return data
        except Exception as exc:
            logger.warning(
                "astrbot_plugin_smart_imagechat_hub: failed to load image index: %s",
                exc,
            )
            return {"version": 1, "images": {}}

    def _save_index(self) -> None:
        self.data_dir.mkdir(parents=True, exist_ok=True)
        with open(self.index_path, "w", encoding="utf-8") as f:
            json.dump(self._index, f, ensure_ascii=False, indent=2)

    def _load_collection_pool(self) -> dict[str, Any]:
        if not self.collection_pool_path.is_file():
            return {"version": 1, "images": {}}
        try:
            with open(self.collection_pool_path, encoding="utf-8-sig") as f:
                data = json.load(f)
            if not isinstance(data, dict):
                raise ValueError("collection pool root is not object")
            data.setdefault("version", 1)
            data.setdefault("images", {})
            if not isinstance(data["images"], dict):
                data["images"] = {}
            return data
        except Exception as exc:
            logger.warning(
                "astrbot_plugin_smart_imagechat_hub: failed to load collection pool: %s",
                exc,
            )
            return {"version": 1, "images": {}}

    def _save_collection_pool(self) -> None:
        self.data_dir.mkdir(parents=True, exist_ok=True)
        with open(self.collection_pool_path, "w", encoding="utf-8") as f:
            json.dump(self._collection_pool, f, ensure_ascii=False, indent=2)

    def _load_discarded_collection(self) -> dict[str, Any]:
        if not self.discarded_collection_path.is_file():
            return {"version": 1, "digests": {}}
        try:
            with open(self.discarded_collection_path, encoding="utf-8-sig") as f:
                data = json.load(f)
            if not isinstance(data, dict):
                raise ValueError("discarded collection root is not object")
            data.setdefault("version", 1)
            digests = data.get("digests", {})
            if not isinstance(digests, dict):
                digests = {}
            normalized: dict[str, dict[str, Any]] = {}
            for digest, value in digests.items():
                digest = str(digest or "").strip()
                if not digest:
                    continue
                discarded_at = 0
                if isinstance(value, dict):
                    discarded_at = self._to_int(value.get("discarded_at"), 0)
                else:
                    discarded_at = self._to_int(value, 0)
                normalized[digest] = {
                    "discarded_at": discarded_at or int(time.time()),
                }
            data["digests"] = normalized
            return data
        except Exception as exc:
            logger.warning(
                "astrbot_plugin_smart_imagechat_hub: failed to load discarded collection history: %s",
                exc,
            )
            return {"version": 1, "digests": {}}

    def _save_discarded_collection(self) -> None:
        digests = self._discarded_collection.get("digests", {})
        has_digests = isinstance(digests, dict) and bool(digests)
        if not has_digests and not self.discarded_collection_path.is_file():
            return
        self.data_dir.mkdir(parents=True, exist_ok=True)
        with open(self.discarded_collection_path, "w", encoding="utf-8") as f:
            json.dump(self._discarded_collection, f, ensure_ascii=False, indent=2)

    def _migrate_reply_config(self) -> None:
        reply_cfg = self.config.get("reply_after_search")
        if not isinstance(reply_cfg, dict):
            reply_cfg = {}

        migrated = False
        already_migrated = self._cfg_bool("reply_config_migrated")
        legacy_map = {
            "use_custom_reply": "use_custom_reply",
            "custom_reply": "custom_reply",
            "llm_reply_when_not_found": "llm_reply_when_not_found",
            "not_found_reply": "not_found_reply",
            "empty_library_reply": "empty_library_reply",
        }
        if not already_migrated:
            for old_key, new_key in legacy_map.items():
                if old_key in self.config:
                    reply_cfg[new_key] = self.config.get(old_key)
                    migrated = True
            self.config["reply_config_migrated"] = True
            migrated = True
        else:
            for old_key, new_key in legacy_map.items():
                if old_key in self.config and new_key not in reply_cfg:
                    reply_cfg[new_key] = self.config.get(old_key)
                    migrated = True

        if self.config.get("reply_after_search") != reply_cfg:
            self.config["reply_after_search"] = reply_cfg
            migrated = True

        if migrated:
            self._save_plugin_config()

    def _migrate_progress_link_config(self) -> None:
        if self._config_get(PROGRESS_LINK_CONFIG_KEY) == PROGRESS_PAGE_CONFIG_VALUE:
            return
        self._config_set(PROGRESS_LINK_CONFIG_KEY, PROGRESS_PAGE_CONFIG_VALUE)
        self._save_plugin_config()

    def _migrate_auto_collection_config(self) -> None:
        current = self.config.get(AUTO_COLLECTION_CONFIG_KEY, {})
        normalized = self._normalize_auto_collection_config(current)
        if current != normalized:
            self.config[AUTO_COLLECTION_CONFIG_KEY] = normalized
            self._save_plugin_config()

    def _migrate_scheduled_backup_config(self) -> None:
        current = self.config.get(SCHEDULED_BACKUP_CONFIG_KEY, {})
        normalized = self._normalize_scheduled_backup_config(current)
        if current != normalized:
            self.config[SCHEDULED_BACKUP_CONFIG_KEY] = normalized
            self._save_plugin_config()

    def _migrate_send_image_style_config(self) -> None:
        current = self.config.get(SEND_IMAGE_STYLE_CONFIG_KEY, {})
        normalized = self._normalize_send_image_style_config(current)
        if current != normalized:
            self.config[SEND_IMAGE_STYLE_CONFIG_KEY] = normalized
            self._save_plugin_config()

    def _save_plugin_config(self) -> None:
        self._refresh_caption_tag_category_schema()
        self._refresh_meme_combat_schema()
        self._refresh_scheduled_backup_schema()
        self._refresh_model_fallback_schema()
        save_config = getattr(self.config, "save_config", None)
        if callable(save_config):
            save_config()

    def _config_get(self, key_path: str, default: Any = None) -> Any:
        current: Any = self.config
        for part in key_path.split("."):
            if not isinstance(current, dict) or part not in current:
                return default
            current = current.get(part)
        return current

    def _config_set(self, key_path: str, value: Any) -> None:
        parts = [part for part in key_path.split(".") if part]
        if not parts:
            return
        current: dict[str, Any] = self.config
        for part in parts[:-1]:
            next_value = current.get(part)
            if not isinstance(next_value, dict):
                next_value = {}
            current[part] = next_value
            current = next_value
        current[parts[-1]] = value

    def _nested_config_get(
        self,
        source: dict[str, Any],
        key_path: str,
        default: Any = None,
    ) -> Any:
        current: Any = source
        for part in key_path.split("."):
            if not isinstance(current, dict) or part not in current:
                return default
            current = current.get(part)
        return current

    def _refresh_image_tag_schema(self, rel_paths: set[str] | None = None) -> None:
        schema = getattr(self.config, "schema", None)
        if not isinstance(schema, dict):
            return
        image_tags_schema = schema.get(IMAGE_TAGS_CONFIG_KEY)
        if not isinstance(image_tags_schema, dict):
            return

        if rel_paths is None:
            rel_paths = set()
            raw_items = self.config.get(IMAGE_TAGS_CONFIG_KEY, [])
            if isinstance(raw_items, list):
                for raw_item in raw_items:
                    if not isinstance(raw_item, dict):
                        continue
                    rel_path = self._norm_rel_path(raw_item.get("image_path"))
                    if rel_path:
                        rel_paths.add(rel_path)
        else:
            rel_paths = {
                rel_path
                for rel_path in rel_paths
                if self._library_source_for_rel_path(
                    rel_path,
                    self._index_image_by_id(self._image_id(rel_path)),
                )
                == MANUAL_LIBRARY_SOURCE
            }

        templates = {}
        for rel_path in sorted(rel_paths):
            template_key = self._template_key_for_image(rel_path)
            templates[template_key] = self._image_tag_template(rel_path)

        image_tags_schema["templates"] = templates or {
            "image_tag": self._image_tag_template("")
        }

    def _refresh_proactive_emoji_schema(self) -> None:
        schema = getattr(self.config, "schema", None)
        if not isinstance(schema, dict):
            return
        group_schema = schema.get(PROACTIVE_EMOJI_CONFIG_KEY)
        if not isinstance(group_schema, dict):
            return
        items = group_schema.get("items")
        if not isinstance(items, dict):
            return
        provider_schema = items.get("analysis_provider_id")
        if not isinstance(provider_schema, dict):
            return
        provider_schema["options"] = [
            option["id"] for option in self._chat_provider_options()
        ]
        self._refresh_meme_combat_schema()

    def _refresh_scheduled_backup_schema(self) -> None:
        schema = getattr(self.config, "schema", None)
        if not isinstance(schema, dict):
            return
        group_schema = schema.get(SCHEDULED_BACKUP_CONFIG_KEY)
        if not isinstance(group_schema, dict):
            return
        group_schema["hint"] = (
            "每天在指定时间自动生成一份与 Page [导出配置] 完全相同格式的 ZIP "
            "备份，存放在 "
            f"{self._scheduled_backup_dir()}。原生 WebUI 可查看备份文件列表；"
            "如需下载或删除，请前往插件 UI Page 的导出配置窗口。"
        )
        items = group_schema.get("items")
        if not isinstance(items, dict):
            return
        backup_list_schema = items.get("backup_files")
        if not isinstance(backup_list_schema, dict):
            return
        backup_list_schema["hint"] = (
            "自动备份文件保存在插件数据目录："
            f"{self._scheduled_backup_dir()}。原生 WebUI 仅展示文件名和创建时间；"
            "如需一键下载，请前往插件 UI Page 的导出配置窗口。"
        )
        backup_list_schema["options"] = [
            f"{item['filename']} | {self._format_timestamp(item['created_at'])}"
            for item in self._scheduled_backup_files()
        ]

    def _refresh_caption_tag_category_schema(self) -> None:
        schema = getattr(self.config, "schema", None)
        if not isinstance(schema, dict):
            return
        provider_schemas = []
        top_level_provider_schema = schema.get(DEFAULT_CAPTION_PROVIDER_CONFIG_KEY)
        if isinstance(top_level_provider_schema, dict):
            provider_schemas.append(top_level_provider_schema)

        group_schema = schema.get(TAG_CATEGORY_CONFIG_KEY)
        if isinstance(group_schema, dict):
            items = group_schema.get("items")
            if isinstance(items, dict):
                nested_provider_schema = items.get(DEFAULT_CAPTION_PROVIDER_CONFIG_KEY)
                if isinstance(nested_provider_schema, dict):
                    provider_schemas.append(nested_provider_schema)

        if not provider_schemas:
            return

        provider_options = [
            option
            for option in self._chat_provider_options()
            if str(option.get("id") or "").strip()
        ]
        current_provider_id = self._caption_provider_id_for_ui()
        options = [
            {
                "title": (
                    "需要选择一个可用的图片转述模型"
                    if not current_provider_id
                    else "不使用默认图片转述模型"
                ),
                "value": "",
                "props": {
                    "class": (
                        "text-warning font-weight-bold"
                        if not current_provider_id
                        else ""
                    )
                },
            }
        ] + [
            {
                "title": str(option.get("label") or option["id"]),
                "value": str(option["id"]),
            }
            for option in provider_options
        ]
        for provider_schema in provider_schemas:
            provider_schema.pop("labels", None)
            provider_schema["options"] = options
            provider_schema["obvious_hint"] = not bool(current_provider_id)

