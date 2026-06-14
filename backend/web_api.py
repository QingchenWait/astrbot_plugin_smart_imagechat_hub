from .common import (
    AUTO_COLLECTION_CONFIG_KEY,
    Any,
    DEFAULT_CAPTION_PROVIDER_CONFIG_KEY,
    IMAGEBED_IMPORT_CONFIG_KEY,
    IMAGE_FILES_CONFIG_KEY,
    MEME_COMBAT_CONFIG_KEY,
    PLUGIN_NAME,
    PROACTIVE_EMOJI_CONFIG_KEY,
    Path,
    Response,
    SCHEDULED_BACKUP_CONFIG_KEY,
    SUPPORTED_IMAGE_EXTS,
    TAG_CATEGORY_CONFIG_KEY,
    asyncio,
    base64,
    jsonify,
    logger,
    mimetypes,
    request,
    send_file,
)


class WebApiMixin:
    def _register_web_apis(self) -> None:
        self.context.register_web_api(
            f"/{PLUGIN_NAME}/caption_progress",
            self.caption_progress_api,
            ["GET"],
            "Get smart image tag generation progress",
        )
        self.context.register_web_api(
            f"/{PLUGIN_NAME}/caption_start",
            self.caption_start_api,
            ["POST"],
            "Start smart image tag generation",
        )
        self.context.register_web_api(
            f"/{PLUGIN_NAME}/caption_library",
            self.caption_library_api,
            ["GET"],
            "Get smart image library tags",
        )
        self.context.register_web_api(
            f"/{PLUGIN_NAME}/caption_plugin_config",
            self.caption_plugin_config_api,
            ["GET", "POST"],
            "Get or update smart image sender plugin settings",
        )
        self.context.register_web_api(
            f"/{PLUGIN_NAME}/caption_tag_category_settings",
            self.caption_tag_category_settings_api,
            ["GET", "POST"],
            "Get or update smart image tag category settings",
        )
        self.context.register_web_api(
            f"/{PLUGIN_NAME}/proactive_emoji_config",
            self.proactive_emoji_config_api,
            ["GET", "POST"],
            "Get or update proactive emoji reply settings",
        )
        self.context.register_web_api(
            f"/{PLUGIN_NAME}/auto_collection_config",
            self.auto_collection_config_api,
            ["GET", "POST"],
            "Get or update auto image collection settings",
        )
        self.context.register_web_api(
            f"/{PLUGIN_NAME}/meme_combat_config",
            self.meme_combat_config_api,
            ["GET", "POST"],
            "Get or update group meme combat settings",
        )
        self.context.register_web_api(
            f"/{PLUGIN_NAME}/auto_collection_pool",
            self.auto_collection_pool_api,
            ["GET"],
            "Get pending auto-collected image pool",
        )
        self.context.register_web_api(
            f"/{PLUGIN_NAME}/scheduled_backup_config",
            self.scheduled_backup_config_api,
            ["GET", "POST"],
            "Get or update scheduled backup settings",
        )
        self.context.register_web_api(
            f"/{PLUGIN_NAME}/scheduled_backup_list",
            self.scheduled_backup_list_api,
            ["GET"],
            "List scheduled backup files",
        )
        self.context.register_web_api(
            f"/{PLUGIN_NAME}/scheduled_backup_download/<backup_id>",
            self.scheduled_backup_download_api,
            ["GET"],
            "Download scheduled backup file",
        )
        self.context.register_web_api(
            f"/{PLUGIN_NAME}/scheduled_backup_delete",
            self.scheduled_backup_delete_api,
            ["POST"],
            "Delete scheduled backup file",
        )
        self.context.register_web_api(
            f"/{PLUGIN_NAME}/scheduled_backup_create",
            self.scheduled_backup_create_api,
            ["POST"],
            "Create scheduled backup file",
        )
        self.context.register_web_api(
            f"/{PLUGIN_NAME}/auto_collection_accept",
            self.auto_collection_accept_api,
            ["POST"],
            "Accept pending auto-collected images",
        )
        self.context.register_web_api(
            f"/{PLUGIN_NAME}/auto_collection_discard",
            self.auto_collection_discard_api,
            ["POST"],
            "Discard pending auto-collected images",
        )
        self.context.register_web_api(
            f"/{PLUGIN_NAME}/external_import_tree",
            self.external_import_tree_api,
            ["GET"],
            "Get external plugin data directory tree",
        )
        self.context.register_web_api(
            f"/{PLUGIN_NAME}/external_import_stat",
            self.external_import_stat_api,
            ["POST"],
            "Count images under an external plugin data directory",
        )
        self.context.register_web_api(
            f"/{PLUGIN_NAME}/external_import_start",
            self.external_import_start_api,
            ["POST"],
            "Import images from an external plugin data directory",
        )
        self.context.register_web_api(
            f"/{PLUGIN_NAME}/external_import_status",
            self.external_import_status_api,
            ["GET"],
            "Get external image import status",
        )
        self.context.register_web_api(
            f"/{PLUGIN_NAME}/external_import_pending",
            self.external_import_pending_api,
            ["GET"],
            "Get external imported images waiting for tags",
        )
        self.context.register_web_api(
            f"/{PLUGIN_NAME}/external_import_thumb/<image_id>",
            self.external_import_thumb_api,
            ["GET"],
            "Get external import pending thumbnail",
        )
        self.context.register_web_api(
            f"/{PLUGIN_NAME}/external_import_delete_pending",
            self.external_import_delete_pending_api,
            ["POST"],
            "Delete pending external imported images",
        )
        self.context.register_web_api(
            f"/{PLUGIN_NAME}/external_import_warning_preference",
            self.external_import_warning_preference_api,
            ["POST"],
            "Update external import warning preferences",
        )
        self.context.register_web_api(
            f"/{PLUGIN_NAME}/external_import_pause_caption",
            self.external_import_pause_caption_api,
            ["POST"],
            "Pause external import tag generation",
        )
        self.context.register_web_api(
            f"/{PLUGIN_NAME}/external_import_start_caption",
            self.external_import_start_caption_api,
            ["POST"],
            "Start external import tag generation",
        )
        self.context.register_web_api(
            f"/{PLUGIN_NAME}/external_import_resume_caption",
            self.external_import_resume_caption_api,
            ["POST"],
            "Resume external import tag generation",
        )
        self.context.register_web_api(
            f"/{PLUGIN_NAME}/external_import_cancel_caption",
            self.external_import_cancel_caption_api,
            ["POST"],
            "Cancel external import tag generation and remove pending images",
        )
        self.context.register_web_api(
            f"/{PLUGIN_NAME}/imagebed_import_config",
            self.imagebed_import_config_api,
            ["GET", "POST"],
            "Get or update Cloudflare R2 imagebed import settings",
        )
        self.context.register_web_api(
            f"/{PLUGIN_NAME}/imagebed_import_test",
            self.imagebed_import_test_api,
            ["POST"],
            "Test Cloudflare R2 imagebed connection",
        )
        self.context.register_web_api(
            f"/{PLUGIN_NAME}/imagebed_import_status",
            self.imagebed_import_status_api,
            ["GET"],
            "Get Cloudflare R2 imagebed import status",
        )
        self.context.register_web_api(
            f"/{PLUGIN_NAME}/imagebed_import_start",
            self.imagebed_import_start_api,
            ["POST"],
            "Start Cloudflare R2 imagebed import",
        )
        self.context.register_web_api(
            f"/{PLUGIN_NAME}/imagebed_import_pending",
            self.imagebed_import_pending_api,
            ["GET"],
            "Get Cloudflare R2 imagebed images waiting for tags",
        )
        self.context.register_web_api(
            f"/{PLUGIN_NAME}/imagebed_import_thumb/<image_id>",
            self.imagebed_import_thumb_api,
            ["GET"],
            "Get Cloudflare R2 imagebed pending thumbnail",
        )
        self.context.register_web_api(
            f"/{PLUGIN_NAME}/imagebed_import_delete_pending",
            self.imagebed_import_delete_pending_api,
            ["POST"],
            "Delete pending Cloudflare R2 imagebed images",
        )
        self.context.register_web_api(
            f"/{PLUGIN_NAME}/imagebed_import_start_caption",
            self.imagebed_import_start_caption_api,
            ["POST"],
            "Start Cloudflare R2 imagebed tag generation",
        )
        self.context.register_web_api(
            f"/{PLUGIN_NAME}/imagebed_import_cancel_caption",
            self.imagebed_import_cancel_caption_api,
            ["POST"],
            "Cancel Cloudflare R2 imagebed tag generation",
        )
        self.context.register_web_api(
            f"/{PLUGIN_NAME}/imagebed_import_ack_error",
            self.imagebed_import_ack_error_api,
            ["POST"],
            "Acknowledge Cloudflare R2 imagebed import error",
        )
        self.context.register_web_api(
            f"/{PLUGIN_NAME}/caption_update_tags",
            self.caption_update_tags_api,
            ["POST"],
            "Update smart image tags",
        )
        self.context.register_web_api(
            f"/{PLUGIN_NAME}/caption_update_global_tags",
            self.caption_update_global_tags_api,
            ["POST"],
            "Update smart image global tags",
        )
        self.context.register_web_api(
            f"/{PLUGIN_NAME}/caption_upload_image",
            self.caption_upload_image_api,
            ["POST"],
            "Upload smart image library image",
        )
        self.context.register_web_api(
            f"/{PLUGIN_NAME}/caption_provider_config",
            self.caption_provider_config_api,
            ["GET", "POST"],
            "Get or update default image caption provider",
        )
        self.context.register_web_api(
            f"/{PLUGIN_NAME}/caption_delete_image",
            self.caption_delete_image_api,
            ["POST"],
            "Delete smart image library image",
        )
        self.context.register_web_api(
            f"/{PLUGIN_NAME}/caption_export_config",
            self.caption_export_config_api,
            ["GET"],
            "Export smart image sender backup zip",
        )
        self.context.register_web_api(
            f"/{PLUGIN_NAME}/caption_import_config",
            self.caption_import_config_api,
            ["POST"],
            "Import smart image sender backup zip",
        )
        self.context.register_web_api(
            f"/{PLUGIN_NAME}/caption_import_config_file",
            self.caption_import_config_file_api,
            ["POST"],
            "Import smart image sender backup zip by file upload",
        )
        self.context.register_web_api(
            f"/{PLUGIN_NAME}/caption_image/<image_id>",
            self.caption_image_api,
            ["GET"],
            "Get smart image thumbnail source",
        )
        self.context.register_web_api(
            f"/{PLUGIN_NAME}/caption_image_data/<image_id>",
            self.caption_image_data_api,
            ["GET"],
            "Get smart image thumbnail data",
        )
        self.context.register_web_api(
            f"/{PLUGIN_NAME}/collection_pending_image/<image_id>",
            self.collection_pending_image_api,
            ["GET"],
            "Get pending auto-collected image",
        )
        self.context.register_web_api(
            f"/{PLUGIN_NAME}/collection_pending_image_data/<image_id>",
            self.collection_pending_image_data_api,
            ["GET"],
            "Get pending auto-collected image data",
        )

    async def caption_progress_api(self):
        await self._sync_library_if_changed(caption_mode="background")
        return jsonify(
            {
                "status": "ok",
                "data": {
                    **self._caption_progress_snapshot(),
                    "external_import": self._external_import_status_snapshot(),
                    "imagebed_import": self._imagebed_import_status_snapshot(),
                },
            }
        )

    async def caption_start_api(self):
        await self._sync_library(caption_mode="background")
        return jsonify({"status": "ok", "data": self._caption_progress_snapshot()})

    async def caption_library_api(self):
        await self._sync_library_if_changed(caption_mode="background")
        return jsonify({"status": "ok", "data": self._caption_library_snapshot()})

    async def caption_plugin_config_api(self):
        if request.method == "GET":
            return jsonify({"status": "ok", "data": self._plugin_config_snapshot()})

        payload = await request.get_json(silent=True) or {}
        if not isinstance(payload, dict):
            return jsonify({"status": "error", "message": "Invalid config payload"})

        async with self._lock:
            self._update_plugin_config_from_payload(payload)
            self._save_plugin_config()

        return jsonify({"status": "ok", "data": self._plugin_config_snapshot()})

    async def caption_tag_category_settings_api(self):
        if request.method == "GET":
            return jsonify(
                {
                    "status": "ok",
                    "data": self._tag_category_settings_snapshot(),
                }
            )

        payload = await request.get_json(silent=True) or {}
        if not isinstance(payload, dict):
            return jsonify({"status": "error", "message": "Invalid settings payload"})

        recaption_all = self._to_bool(payload.get("recaption_all"), False)
        old_settings = self._tag_category_settings()
        new_settings = self._normalize_tag_category_settings(payload)
        provider_id = new_settings.get(DEFAULT_CAPTION_PROVIDER_CONFIG_KEY, "")
        provider_ids = {option["id"] for option in self._chat_provider_options()}
        if provider_id and provider_id not in provider_ids:
            return jsonify({"status": "error", "message": "provider not found"})
        category_changed = self._tag_category_generation_settings_changed(
            old_settings,
            new_settings,
        )
        provider_changed = old_settings.get(
            DEFAULT_CAPTION_PROVIDER_CONFIG_KEY,
            "",
        ) != new_settings.get(DEFAULT_CAPTION_PROVIDER_CONFIG_KEY, "")
        changed = category_changed or provider_changed
        if category_changed and recaption_all:
            await self._cancel_caption_task()

        async with self._lock:
            self.config[DEFAULT_CAPTION_PROVIDER_CONFIG_KEY] = new_settings.get(
                DEFAULT_CAPTION_PROVIDER_CONFIG_KEY,
                "",
            )
            self.config[TAG_CATEGORY_CONFIG_KEY] = (
                self._tag_category_settings_for_storage(new_settings)
            )
            self._set_system_default_image_caption_provider_id(
                new_settings.get(DEFAULT_CAPTION_PROVIDER_CONFIG_KEY, "")
            )
            self._save_plugin_config()
            self._refresh_caption_tag_category_schema()
            if category_changed and recaption_all:
                self._reset_all_caption_tags_for_new_categories()
                self._save_index()
                existing_rel_paths = self._all_existing_index_rel_paths()
                self._sync_config_image_files(existing_rel_paths)
                self._sync_config_tags(existing_rel_paths)
                self._refresh_image_tag_schema(existing_rel_paths)
                self._last_library_signature = (
                    self._library_signature_for_rel_paths(existing_rel_paths)
                )
                pending_count = len(self._pending_caption_rel_paths())
                self._set_caption_progress(
                    status="pending",
                    total=pending_count,
                    completed=0,
                    failed=0,
                    remaining=pending_count,
                    current_image="",
                    message="Image tag regeneration queued with updated category settings.",
                    error_detail="",
                    error_image="",
                    error_message="",
                    error_source="",
                )

        if category_changed and recaption_all:
            self._start_caption_background_task()

        return jsonify(
            {
                "status": "ok",
                "data": {
                    "settings": self._tag_category_settings_snapshot(),
                    "changed": changed,
                    "category_changed": category_changed,
                    "provider_changed": provider_changed,
                    "recaption_started": bool(category_changed and recaption_all),
                    "progress": self._caption_progress_snapshot(),
                    "library": self._caption_library_snapshot(),
                },
            }
        )

    async def proactive_emoji_config_api(self):
        if request.method == "GET":
            self._refresh_proactive_emoji_schema()
            return jsonify({"status": "ok", "data": self._proactive_emoji_snapshot()})

        payload = await request.get_json(silent=True) or {}
        if not isinstance(payload, dict):
            return jsonify({"status": "error", "message": "Invalid config payload"})

        async with self._lock:
            self.config[PROACTIVE_EMOJI_CONFIG_KEY] = (
                self._normalize_proactive_emoji_config(payload)
            )
            self._save_plugin_config()
            self._refresh_proactive_emoji_schema()

        return jsonify({"status": "ok", "data": self._proactive_emoji_snapshot()})

    async def auto_collection_config_api(self):
        if request.method == "GET":
            return jsonify({"status": "ok", "data": self._auto_collection_snapshot()})

        payload = await request.get_json(silent=True) or {}
        if not isinstance(payload, dict):
            return jsonify({"status": "error", "message": "Invalid config payload"})

        async with self._lock:
            self.config[AUTO_COLLECTION_CONFIG_KEY] = (
                self._normalize_auto_collection_config(payload)
            )
            self._save_plugin_config()
            self._cleanup_collection_pool()

        return jsonify({"status": "ok", "data": self._auto_collection_snapshot()})

    async def meme_combat_config_api(self):
        if request.method == "GET":
            self._refresh_meme_combat_schema()
            return jsonify({"status": "ok", "data": self._meme_combat_snapshot()})

        payload = await request.get_json(silent=True) or {}
        if not isinstance(payload, dict):
            return jsonify({"status": "error", "message": "Invalid config payload"})

        provider_id = str(
            (
                payload.get("battle", {})
                if isinstance(payload.get("battle"), dict)
                else {}
            ).get("analysis_provider_id")
            or ""
        ).strip()
        provider_ids = {option["id"] for option in self._chat_provider_options()}
        if provider_id and provider_id not in provider_ids:
            battle_payload = (
                payload.get("battle", {})
                if isinstance(payload.get("battle"), dict)
                else {}
            )
            payload["battle"] = {**battle_payload, "analysis_provider_id": ""}

        async with self._lock:
            self.config[MEME_COMBAT_CONFIG_KEY] = (
                self._normalize_meme_combat_config(payload)
            )
            self._save_plugin_config()
            self._refresh_meme_combat_schema()

        return jsonify({"status": "ok", "data": self._meme_combat_snapshot()})

    async def auto_collection_pool_api(self):
        async with self._lock:
            self._cleanup_collection_pool()
        return jsonify({"status": "ok", "data": self._collection_pool_snapshot()})

    async def scheduled_backup_config_api(self):
        if request.method == "GET":
            return jsonify({"status": "ok", "data": self._scheduled_backup_snapshot()})

        payload = await request.get_json(silent=True) or {}
        if not isinstance(payload, dict):
            return jsonify({"status": "error", "message": "Invalid config payload"})

        async with self._lock:
            self.config[SCHEDULED_BACKUP_CONFIG_KEY] = (
                self._normalize_scheduled_backup_config(payload)
            )
            self._save_plugin_config()
            self._enforce_scheduled_backup_limit()
            self._restart_scheduled_backup_task()

        return jsonify({"status": "ok", "data": self._scheduled_backup_snapshot()})

    async def scheduled_backup_list_api(self):
        return jsonify({"status": "ok", "data": self._scheduled_backup_snapshot()})

    async def scheduled_backup_create_api(self):
        await self._sync_library_if_changed(caption_mode="none")
        backup = await self._create_persistent_backup()
        return jsonify(
            {
                "status": "ok",
                "data": {
                    "backup": backup,
                    "backups": self._scheduled_backup_files(),
                    "config": self._scheduled_backup_config(),
                    "storage_dir": str(self._scheduled_backup_dir()),
                },
            }
        )

    async def scheduled_backup_delete_api(self):
        payload = await request.get_json(silent=True) or {}
        backup_id = str(payload.get("backup_id") or payload.get("filename") or "")
        deleted = self._delete_scheduled_backup(backup_id)
        if not deleted:
            return jsonify({"status": "error", "message": "backup not found"})
        self._refresh_scheduled_backup_schema()
        return jsonify(
            {
                "status": "ok",
                "data": {
                    "deleted": deleted,
                    "backups": self._scheduled_backup_files(),
                    "config": self._scheduled_backup_config(),
                    "storage_dir": str(self._scheduled_backup_dir()),
                },
            }
        )

    async def scheduled_backup_download_api(self, backup_id: str):
        item = self._scheduled_backup_item_by_id(backup_id)
        if not item:
            return jsonify({"status": "error", "message": "backup not found"})
        path = self._scheduled_backup_path(item["filename"])
        if not path.is_file():
            return jsonify({"status": "error", "message": "backup file missing"})
        headers = {
            "Content-Disposition": (
                f'attachment; filename="{item["filename"]}"; '
                f'filename*=UTF-8\'\'{item["filename"]}'
            )
        }
        try:
            headers["Content-Length"] = str(path.stat().st_size)
        except OSError:
            pass
        return Response(
            self._stream_file_no_delete(path),
            mimetype="application/zip",
            headers=headers,
        )

    async def auto_collection_accept_api(self):
        payload = await request.get_json(silent=True) or {}
        image_ids = self._normalize_ids(payload.get("image_ids", []))
        if not image_ids:
            return jsonify({"status": "error", "message": "image_ids is required"})
        capacity_action = str(payload.get("capacity_action") or "").strip()
        async with self._lock:
            result = self._accept_pending_collection_images(
                image_ids,
                capacity_action=capacity_action,
            )
        if result.get("capacity_error"):
            return jsonify(
                {
                    "status": "ok",
                    "data": {
                        "result": result,
                        "pool": self._collection_pool_snapshot(),
                        "progress": self._caption_progress_snapshot(),
                        "library": self._caption_library_snapshot(),
                    },
                }
            )
        if result["accepted"]:
            self._start_caption_background_task()
        return jsonify(
            {
                "status": "ok",
                "data": {
                    "result": result,
                    "pool": self._collection_pool_snapshot(),
                    "progress": self._caption_progress_snapshot(),
                    "library": self._caption_library_snapshot(),
                },
            }
        )

    async def auto_collection_discard_api(self):
        payload = await request.get_json(silent=True) or {}
        image_ids = self._normalize_ids(payload.get("image_ids", []))
        if not image_ids:
            return jsonify({"status": "error", "message": "image_ids is required"})
        async with self._lock:
            result = self._discard_pending_collection_images(image_ids)
        return jsonify(
            {
                "status": "ok",
                "data": {
                    "result": result,
                    "pool": self._collection_pool_snapshot(),
                },
            }
        )

    async def external_import_tree_api(self):
        return jsonify(
            {"status": "ok", "data": self._external_import_visible_tree()}
        )

    async def external_import_stat_api(self):
        payload = await request.get_json(silent=True) or {}
        directory = str(payload.get("directory") or "").strip()
        try:
            stat = await self._external_import_stat_directory_async(directory)
        except ValueError as exc:
            return jsonify({"status": "error", "message": str(exc)})
        return jsonify({"status": "ok", "data": stat})

    async def external_import_start_api(self):
        payload = await request.get_json(silent=True) or {}
        directory = str(payload.get("directory") or "").strip()
        include_parent_dir_tag = self._to_bool(
            payload.get("include_parent_dir_tag"),
            False,
        )
        try:
            await self._sync_library_if_changed(caption_mode="none")
            status = await self._start_external_import(
                directory,
                include_parent_dir_tag=include_parent_dir_tag,
            )
        except ValueError as exc:
            return jsonify({"status": "error", "message": str(exc)})
        return jsonify({"status": "ok", "data": status})

    async def external_import_status_api(self):
        return jsonify(
            {"status": "ok", "data": self._external_import_status_snapshot()}
        )

    async def external_import_pending_api(self):
        return jsonify(
            {"status": "ok", "data": self._external_import_pending_snapshot()}
        )

    async def external_import_thumb_api(self, image_id: str):
        try:
            image_path = await self._external_import_image_response_path(image_id)
        except ValueError as exc:
            message = str(exc)
            status_code = 404 if "not found" in message or "missing" in message else 400
            return jsonify({"status": "error", "message": message}), status_code
        return await send_file(image_path)

    async def external_import_delete_pending_api(self):
        payload = await request.get_json(silent=True) or {}
        image_ids = self._normalize_ids(payload.get("image_ids", []))
        if not image_ids:
            return jsonify({"status": "error", "message": "image_ids is required"})
        async with self._lock:
            result = self._delete_external_pending_images(image_ids)
        return jsonify(
            {
                "status": "ok",
                "data": {
                    "result": result,
                    "pending": self._external_import_pending_snapshot(),
                    "library": self._caption_library_snapshot(),
                    "progress": self._caption_progress_snapshot(),
                },
            }
        )

    async def external_import_warning_preference_api(self):
        payload = await request.get_json(silent=True) or {}
        action = str(payload.get("action") or "").strip()
        skip = self._to_bool(payload.get("skip"), False)
        try:
            async with self._lock:
                preferences = self._set_external_import_warning_preference(
                    action,
                    skip,
                )
        except ValueError as exc:
            return jsonify({"status": "error", "message": str(exc)})
        return jsonify({"status": "ok", "data": {"warning_preferences": preferences}})

    async def external_import_pause_caption_api(self):
        await self._pause_external_captioning()
        return jsonify(
            {
                "status": "ok",
                "data": {
                    "pending": self._external_import_pending_snapshot(),
                    "progress": self._caption_progress_snapshot(),
                },
            }
        )

    async def external_import_resume_caption_api(self):
        await self._resume_external_captioning()
        return jsonify(
            {
                "status": "ok",
                "data": {
                    "pending": self._external_import_pending_snapshot(),
                    "progress": self._caption_progress_snapshot(),
                },
            }
        )

    async def external_import_start_caption_api(self):
        try:
            await self._start_external_captioning()
        except ValueError as exc:
            return jsonify({"status": "error", "message": str(exc)}), 400
        return jsonify(
            {
                "status": "ok",
                "data": {
                    "pending": self._external_import_pending_snapshot(),
                    "progress": self._caption_progress_snapshot(),
                },
            }
        )

    async def external_import_cancel_caption_api(self):
        result = await self._cancel_external_captioning()
        return jsonify(
            {
                "status": "ok",
                "data": {
                    "result": result,
                    "pending": self._external_import_pending_snapshot(),
                    "library": self._caption_library_snapshot(),
                    "progress": self._caption_progress_snapshot(),
                },
            }
        )

    async def imagebed_import_config_api(self):
        if request.method == "GET":
            return jsonify({"status": "ok", "data": self._imagebed_config_snapshot()})

        payload = await request.get_json(silent=True) or {}
        if not isinstance(payload, dict):
            return jsonify({"status": "error", "message": "Invalid config payload"})
        async with self._lock:
            self._set_imagebed_import_config(payload)
            self._restart_imagebed_sync_task()
        return jsonify({"status": "ok", "data": self._imagebed_config_snapshot()})

    async def imagebed_import_test_api(self):
        payload = await request.get_json(silent=True) or {}
        if not isinstance(payload, dict):
            payload = {}
        return jsonify({"status": "ok", "data": await self._test_imagebed_connection(payload)})

    async def imagebed_import_status_api(self):
        return jsonify(
            {"status": "ok", "data": self._imagebed_import_status_snapshot()}
        )

    async def imagebed_import_start_api(self):
        try:
            await self._sync_library_if_changed(caption_mode="none")
            status = await self._start_imagebed_import(trigger="manual")
        except ValueError as exc:
            return jsonify({"status": "error", "message": str(exc)}), 400
        return jsonify({"status": "ok", "data": status})

    async def imagebed_import_pending_api(self):
        return jsonify(
            {"status": "ok", "data": self._imagebed_import_pending_snapshot()}
        )

    async def imagebed_import_thumb_api(self, image_id: str):
        try:
            image_path = await self._imagebed_import_image_response_path(image_id)
        except ValueError as exc:
            message = str(exc)
            status_code = 404 if "not found" in message or "missing" in message else 400
            return jsonify({"status": "error", "message": message}), status_code
        return await send_file(image_path)

    async def imagebed_import_delete_pending_api(self):
        payload = await request.get_json(silent=True) or {}
        image_ids = self._normalize_ids(payload.get("image_ids", []))
        if not image_ids:
            return jsonify({"status": "error", "message": "image_ids is required"})
        async with self._lock:
            result = self._delete_imagebed_pending_images(image_ids)
        return jsonify(
            {
                "status": "ok",
                "data": {
                    "result": result,
                    "pending": self._imagebed_import_pending_snapshot(),
                    "library": self._caption_library_snapshot(),
                    "progress": self._caption_progress_snapshot(),
                },
            }
        )

    async def imagebed_import_start_caption_api(self):
        try:
            await self._start_imagebed_captioning()
        except ValueError as exc:
            return jsonify({"status": "error", "message": str(exc)}), 400
        return jsonify(
            {
                "status": "ok",
                "data": {
                    "pending": self._imagebed_import_pending_snapshot(),
                    "progress": self._caption_progress_snapshot(),
                },
            }
        )

    async def imagebed_import_cancel_caption_api(self):
        result = await self._cancel_imagebed_captioning()
        return jsonify(
            {
                "status": "ok",
                "data": {
                    "result": result,
                    "pending": self._imagebed_import_pending_snapshot(),
                    "library": self._caption_library_snapshot(),
                    "progress": self._caption_progress_snapshot(),
                },
            }
        )

    async def imagebed_import_ack_error_api(self):
        payload = await request.get_json(silent=True) or {}
        error_id = str(payload.get("error_id") or "").strip()
        return jsonify(
            {
                "status": "ok",
                "data": self._ack_imagebed_import_error(error_id),
            }
        )

    async def caption_update_tags_api(self):
        payload = await request.get_json(silent=True) or {}
        image_id = str(payload.get("image_id") or "").strip()
        tags = self._normalize_tags(payload.get("tags", []))
        selected_global_tags = self._normalize_tags(
            payload.get("selected_global_tags", [])
        )
        source = str(payload.get("library_source") or "").strip()
        async with self._lock:
            item = self._update_image_tags(
                image_id,
                tags,
                selected_global_tags,
                source=source,
            )
        if not item:
            return jsonify({"status": "error", "message": "image not found"})
        return jsonify(
            {
                "status": "ok",
                "data": {
                    "image": item,
                    "library": self._caption_library_snapshot(),
                },
            }
        )

    async def caption_update_global_tags_api(self):
        payload = await request.get_json(silent=True) or {}
        global_tags = self._normalize_tags(payload.get("global_tags", []))
        async with self._lock:
            self._update_global_tags(global_tags)
        return jsonify(
            {
                "status": "ok",
                "data": {
                    "library": self._caption_library_snapshot(),
                },
            }
        )

    async def caption_upload_image_api(self):
        payload = await request.get_json(silent=True)
        if isinstance(payload, dict) and payload.get("content_base64"):
            return await self._caption_upload_image_json(payload)

        files = await request.files
        if not files:
            return jsonify({"status": "error", "message": "No files uploaded"})

        uploaded = []
        errors = []
        for file in files.values():
            filename = self._safe_upload_filename(file.filename or "")
            if not filename:
                errors.append("Invalid filename")
                continue
            if Path(filename).suffix.lower() not in SUPPORTED_IMAGE_EXTS:
                errors.append(f"Unsupported file type: {filename}")
                continue

            folder = self._config_file_folder(IMAGE_FILES_CONFIG_KEY)
            rel_path = self._unique_upload_rel_path(folder, filename)
            try:
                save_path = self._abs_plugin_data_path(rel_path)
            except ValueError:
                errors.append(f"Invalid path: {filename}")
                continue
            save_path.parent.mkdir(parents=True, exist_ok=True)
            await file.save(str(save_path))
            if not self._is_allowed_image(save_path):
                try:
                    save_path.unlink()
                except OSError:
                    pass
                errors.append(f"Unsupported file type: {filename}")
                continue
            uploaded.append(rel_path)

        if uploaded:
            await self._sync_library(caption_mode="background")

        if not uploaded:
            return jsonify(
                {
                    "status": "error",
                    "message": "Upload failed: " + ", ".join(errors),
                }
            )

        return jsonify(
            {
                "status": "ok",
                "data": {
                    "uploaded": uploaded,
                    "errors": errors,
                    "progress": self._caption_progress_snapshot(),
                    "library": self._caption_library_snapshot(),
                },
            }
        )

    async def caption_provider_config_api(self):
        if request.method == "GET":
            return jsonify(
                {"status": "ok", "data": self._caption_provider_config_snapshot()}
            )

        payload = await request.get_json(silent=True) or {}
        if not isinstance(payload, dict):
            return jsonify({"status": "error", "message": "Invalid config payload"})
        provider_id = str(payload.get("provider_id") or "").strip()
        provider_ids = {option["id"] for option in self._chat_provider_options()}
        if provider_id and provider_id not in provider_ids:
            return jsonify({"status": "error", "message": "provider not found"})

        cfg = self.context.get_config()
        if cfg:
            self._set_system_default_image_caption_provider_id(provider_id)
        async with self._lock:
            self._set_plugin_default_image_caption_provider_id(provider_id)
            self._save_plugin_config()
            self._refresh_caption_tag_category_schema()

        logger.info(
            "astrbot_plugin_smart_imagechat_hub: default image caption provider updated to %s.",
            provider_id or "<empty>",
        )
        return jsonify(
            {"status": "ok", "data": self._caption_provider_config_snapshot()}
        )

    async def caption_delete_image_api(self):
        payload = await request.get_json(silent=True) or {}
        image_id = str(payload.get("image_id") or "").strip()
        source = str(payload.get("library_source") or "").strip()
        async with self._lock:
            deleted = self._delete_image(image_id, source=source)
        if not deleted:
            return jsonify({"status": "error", "message": "image not found"})
        return jsonify(
            {
                "status": "ok",
                "data": {
                    "deleted": deleted,
                    "progress": self._caption_progress_snapshot(),
                    "library": self._caption_library_snapshot(),
                },
            }
        )

    async def caption_export_config_api(self):
        await self._sync_library_if_changed(caption_mode="none")
        backup = await self._create_persistent_backup()
        filename = backup["filename"]
        zip_path = self._scheduled_backup_path(filename)

        headers = {
            "Content-Disposition": (
                f'attachment; filename="{filename}"; filename*=UTF-8\'\'{filename}'
            )
        }
        try:
            headers["Content-Length"] = str(zip_path.stat().st_size)
        except OSError:
            pass
        return Response(
            self._stream_file_no_delete(zip_path),
            mimetype="application/zip",
            headers=headers,
        )

    async def caption_import_config_api(self):
        temp_path: Path | None = None
        try:
            temp_path, filename, library_mode, overwrite_plugin_config = (
                await self._receive_backup_import_file()
            )
            return await self._handle_backup_import(
                temp_path,
                filename=filename,
                library_mode=library_mode,
                overwrite_plugin_config=overwrite_plugin_config,
            )
        except ValueError as exc:
            return jsonify({"status": "error", "message": str(exc)})
        finally:
            if temp_path is not None:
                self._unlink_temp_path(temp_path)

    async def _handle_backup_import(
        self,
        temp_path: Path,
        filename: str,
        library_mode: str,
        overwrite_plugin_config: bool,
    ):
        if library_mode not in {"overwrite", "merge"}:
            return jsonify(
                {
                    "status": "error",
                    "message": "library_mode must be overwrite or merge",
                }
            )
        if not filename.lower().endswith(".zip"):
            return jsonify({"status": "error", "message": "Only zip backup is supported"})

        try:
            backup = await asyncio.to_thread(self._read_backup_zip, temp_path)
        except ValueError as exc:
            return jsonify({"status": "error", "message": str(exc)})

        await self._sync_library_if_changed(caption_mode="none")
        await self._cancel_caption_task()
        async with self._lock:
            result = self._restore_backup(
                backup,
                library_mode=library_mode,
                overwrite_plugin_config=overwrite_plugin_config,
            )
        self._start_caption_background_task()

        return jsonify(
            {
                "status": "ok",
                "data": {
                    "result": result,
                    "progress": self._caption_progress_snapshot(),
                    "library": self._caption_library_snapshot(),
                },
            }
        )

    async def caption_import_config_file_api(self):
        try:
            temp_path, filename, library_mode, overwrite_plugin_config = (
                await self._receive_backup_import_file()
            )
        except ValueError as exc:
            return jsonify({"status": "error", "message": str(exc)})

        try:
            return await self._handle_backup_import(
                temp_path,
                filename=filename,
                library_mode=library_mode,
                overwrite_plugin_config=overwrite_plugin_config,
            )
        finally:
            self._unlink_temp_path(temp_path)

    async def _caption_upload_image_json(self, payload: dict[str, Any]):
        filename = self._safe_upload_filename(str(payload.get("filename") or ""))
        if not filename:
            return jsonify({"status": "error", "message": "Invalid filename"})
        if Path(filename).suffix.lower() not in SUPPORTED_IMAGE_EXTS:
            return jsonify(
                {"status": "error", "message": f"Unsupported file type: {filename}"}
            )

        raw_content = str(payload.get("content_base64") or "")
        if "," in raw_content and raw_content.split(",", 1)[0].startswith("data:"):
            raw_content = raw_content.split(",", 1)[1]
        try:
            content = base64.b64decode(raw_content, validate=True)
        except Exception:
            return jsonify({"status": "error", "message": "Invalid image payload"})
        if not content:
            return jsonify({"status": "error", "message": "Empty file"})

        selected_global_tags = self._valid_global_tags(
            payload.get("selected_global_tags", [])
        )
        folder = self._config_file_folder(IMAGE_FILES_CONFIG_KEY)
        rel_path = self._unique_upload_rel_path(folder, filename)
        try:
            save_path = self._abs_plugin_data_path(rel_path)
        except ValueError:
            return jsonify({"status": "error", "message": f"Invalid path: {filename}"})
        save_path.parent.mkdir(parents=True, exist_ok=True)
        with open(save_path, "wb") as f:
            f.write(content)
        if not self._is_allowed_image(save_path):
            try:
                save_path.unlink()
            except OSError:
                pass
            return jsonify(
                {"status": "error", "message": f"Unsupported file type: {filename}"}
            )

        await self._sync_library(
            caption_mode="background",
            initial_global_tags_by_rel_path={rel_path: selected_global_tags}
            if selected_global_tags
            else None,
        )
        return jsonify(
            {
                "status": "ok",
                "data": {
                    "uploaded": [rel_path],
                    "errors": [],
                    "progress": self._caption_progress_snapshot(),
                    "library": self._caption_library_snapshot(),
                },
            }
        )

    async def caption_image_api(self, image_id: str):
        item = self._index_image_by_id(image_id)
        if not item:
            return jsonify({"status": "error", "message": "image not found"})
        rel_path = self._norm_rel_path(item.get("rel_path"))
        try:
            image_path = self._abs_plugin_data_path(rel_path)
        except ValueError:
            return jsonify({"status": "error", "message": "invalid image path"})
        if not image_path.is_file():
            return jsonify({"status": "error", "message": "image file missing"})
        return await send_file(image_path)

    async def caption_image_data_api(self, image_id: str):
        item = self._index_image_by_id(image_id)
        if not item:
            return jsonify({"status": "error", "message": "image not found"})
        rel_path = self._norm_rel_path(item.get("rel_path"))
        try:
            image_path = self._abs_plugin_data_path(rel_path)
        except ValueError:
            return jsonify({"status": "error", "message": "invalid image path"})
        if not image_path.is_file():
            return jsonify({"status": "error", "message": "image file missing"})

        mime_type = mimetypes.guess_type(image_path.name)[0] or "image/png"
        with open(image_path, "rb") as f:
            encoded = base64.b64encode(f.read()).decode("ascii")
        return jsonify(
            {
                "status": "ok",
                "data": {
                    "image_id": str(item.get("id") or image_id),
                    "mime_type": mime_type,
                    "data_url": f"data:{mime_type};base64,{encoded}",
                    "updated_at": self._to_int(item.get("updated_at"), 0),
                },
            }
        )

    async def collection_pending_image_api(self, image_id: str):
        item = self._collection_pool_item_by_id(image_id)
        if not item:
            return jsonify({"status": "error", "message": "image not found"})
        rel_path = self._norm_rel_path(item.get("rel_path"))
        try:
            image_path = self._abs_plugin_data_path(rel_path)
        except ValueError:
            return jsonify({"status": "error", "message": "invalid image path"})
        if not image_path.is_file():
            return jsonify({"status": "error", "message": "image file missing"})
        return await send_file(image_path)

    async def collection_pending_image_data_api(self, image_id: str):
        item = self._collection_pool_item_by_id(image_id)
        if not item:
            return jsonify({"status": "error", "message": "image not found"})
        rel_path = self._norm_rel_path(item.get("rel_path"))
        try:
            image_path = self._abs_plugin_data_path(rel_path)
        except ValueError:
            return jsonify({"status": "error", "message": "invalid image path"})
        if not image_path.is_file():
            return jsonify({"status": "error", "message": "image file missing"})

        mime_type = mimetypes.guess_type(image_path.name)[0] or "image/png"
        with open(image_path, "rb") as f:
            encoded = base64.b64encode(f.read()).decode("ascii")
        return jsonify(
            {
                "status": "ok",
                "data": {
                    "image_id": str(item.get("id") or image_id),
                    "mime_type": mime_type,
                    "data_url": f"data:{mime_type};base64,{encoded}",
                    "updated_at": self._to_int(item.get("collected_at"), 0),
                },
            }
        )

