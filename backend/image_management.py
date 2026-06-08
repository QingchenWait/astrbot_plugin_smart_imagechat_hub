from .common import Any, GLOBAL_TAGS_CONFIG_KEY, PLUGIN_NAME, Path, logger, time


class ImageManagementMixin:
    def _display_tags_from_item(self, item: dict[str, Any]) -> list[str]:
        manual_tags = self._normalize_tags(item.get("manual_tags", []))
        if item.get("manual_tags_override"):
            return manual_tags
        if manual_tags:
            return manual_tags
        auto_tags = self._normalize_tags(item.get("auto_tags", []))
        if auto_tags:
            return auto_tags
        return self._normalize_tags(item.get("tags", []))

    def _update_image_tags(
        self,
        image_id: str,
        tags: list[str],
        selected_global_tags: list[str],
        source: str = "",
    ) -> dict[str, Any] | None:
        item = self._index_image_by_id(image_id)
        if not item:
            return None

        rel_path = self._norm_rel_path(item.get("rel_path"))
        if not rel_path:
            return None
        if source and self._library_source_for_rel_path(rel_path, item) != source:
            return None

        allowed_global_tags = set(self._global_tags())
        selected = [tag for tag in selected_global_tags if tag in allowed_global_tags]
        manual_tags = tags

        item["manual_tags"] = manual_tags
        item["manual_tags_override"] = True
        item["selected_global_tags"] = selected
        item["tags"] = self._merge_tags(manual_tags, selected)
        item["updated_at"] = int(time.time())

        self._save_index()
        existing_rel_paths = self._all_existing_index_rel_paths()
        self._sync_config_image_files(existing_rel_paths)
        self._sync_config_tags(existing_rel_paths)
        self._refresh_image_tag_schema(existing_rel_paths)

        return self._caption_library_image_item(item)

    def _update_global_tags(self, global_tags: list[str]) -> None:
        old_global_tags = self._global_tags()
        next_global_tags = self._normalize_tags(global_tags)
        if old_global_tags == next_global_tags:
            self._refresh_image_tag_schema(self._all_existing_index_rel_paths())
            return

        self._config_set(GLOBAL_TAGS_CONFIG_KEY, next_global_tags)
        self._save_plugin_config()

        images = self._index.get("images", {})
        if isinstance(images, dict):
            allowed = set(next_global_tags)
            for item in images.values():
                if not isinstance(item, dict):
                    continue
                selected = [
                    tag
                    for tag in self._normalize_tags(
                        item.get("selected_global_tags", [])
                    )
                    if tag in allowed
                ]
                if selected == self._normalize_tags(item.get("selected_global_tags", [])):
                    continue
                item["selected_global_tags"] = selected
                item["tags"] = self._tags_from_item(item)
                item["updated_at"] = int(time.time())

            self._save_index()
            existing_rel_paths = self._all_existing_index_rel_paths()
            self._sync_config_image_files(existing_rel_paths)
            self._sync_config_tags(existing_rel_paths)
            self._refresh_image_tag_schema(existing_rel_paths)
            self._last_library_signature = self._library_signature_for_rel_paths(
                existing_rel_paths
            )

    def _delete_image(
        self,
        image_id: str,
        source: str = "",
        sync_after: bool = True,
    ) -> dict[str, Any] | None:
        item = self._index_image_by_id(image_id)
        if not item:
            return None

        rel_path = self._norm_rel_path(item.get("rel_path"))
        if not rel_path:
            return None
        if source and self._library_source_for_rel_path(rel_path, item) != source:
            return None

        try:
            image_path = self._abs_plugin_data_path(rel_path)
        except ValueError:
            image_path = None

        if image_path and image_path.is_file():
            try:
                image_path.unlink()
            except OSError as exc:
                logger.warning(
                    "astrbot_plugin_smart_imagechat_hub: failed to delete image file %s: %s",
                    rel_path,
                    exc,
                )

        images = self._index.get("images", {})
        if isinstance(images, dict):
            images.pop(str(item.get("id") or image_id), None)
            images.pop(self._image_id(rel_path), None)

        if sync_after:
            self._save_index()
            existing_rel_paths = self._all_existing_index_rel_paths()
            self._sync_config_image_files(existing_rel_paths)
            self._sync_config_tags(existing_rel_paths)
            self._refresh_image_tag_schema(existing_rel_paths)
            self._last_library_signature = self._library_signature_for_rel_paths(
                existing_rel_paths
            )
        return {
            "image_id": image_id,
            "rel_path": rel_path,
        }

    def _caption_library_image_item(self, item: dict[str, Any]) -> dict[str, Any]:
        rel_path = self._norm_rel_path(item.get("rel_path"))
        image_id = str(item.get("id") or self._image_id(rel_path))
        return {
            "id": image_id,
            "rel_path": rel_path,
            "filename": item.get("filename") or Path(rel_path).name,
            "library_source": self._library_source_for_rel_path(rel_path, item),
            "auto_tags": self._normalize_tags(item.get("auto_tags", [])),
            "manual_tags_override": bool(item.get("manual_tags_override", False)),
            "tags": self._display_tags_from_item(item),
            "selected_global_tags": self._normalize_tags(
                item.get("selected_global_tags", [])
            ),
            "merged_tags": self._tags_from_item(item),
            "captioned_at": self._to_int(item.get("captioned_at"), 0),
            "updated_at": self._to_int(item.get("updated_at"), 0),
            "mtime": self._to_int(item.get("mtime"), 0),
            "size": self._to_int(item.get("size"), 0),
            "thumbnail_url": f"/api/plug/{PLUGIN_NAME}/caption_image/{image_id}",
        }

    def _template_key_for_image(self, rel_path: str) -> str:
        return f"image_tag_{self._image_id(rel_path)}"

    def _rel_path_from_template_key(self, template_key: Any) -> str:
        if not isinstance(template_key, str):
            return ""
        prefix = "image_tag_"
        if not template_key.startswith(prefix):
            return ""
        image_id = template_key.removeprefix(prefix)
        images = self._index.get("images", {})
        if not isinstance(images, dict):
            return ""
        item = images.get(image_id)
        if not isinstance(item, dict):
            return ""
        return self._norm_rel_path(item.get("rel_path"))

    def _image_tag_template(self, rel_path: str) -> dict[str, Any]:
        title = f"图像标签：{rel_path}" if rel_path else "图像标签"
        return {
            "name": title,
            "hint": "图片路径由插件自动维护；手动修改后，检索会使用本条目标签 + 附加的公用特征标签。",
            "items": {
                "image_path": {
                    "description": "图片相对路径",
                    "type": "string",
                    "default": rel_path,
                    "invisible": True,
                },
                "tags": {
                    "description": "自动生成的特征标签 (可手动修改)",
                    "type": "list",
                    "items": {"type": "string"},
                    "default": [],
                },
                "selected_global_tags": {
                    "description": "附加的公用特征标签",
                    "type": "list",
                    "items": {"type": "string"},
                    "options": self._global_tags(),
                    "default": [],
                    "hint": "可从“全局特征标签”中选择一个或多个标签。检索时会与本条目标签合并。",
                },
                "auto_tags": {
                    "description": "LLM 自动特征标签",
                    "type": "list",
                    "items": {"type": "string"},
                    "default": [],
                    "invisible": True,
                },
                "manual_tags_override": {
                    "description": "Page 标签编辑状态",
                    "type": "bool",
                    "default": False,
                    "invisible": True,
                },
            },
        }

