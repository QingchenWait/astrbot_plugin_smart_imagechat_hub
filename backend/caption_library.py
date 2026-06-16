from .common import (
    AUTO_COLLECTION_CONFIG_KEY,
    Any,
    CAPTION_PROMPT_VERSION,
    CaptionGenerationError,
    COLLECTED_LIBRARY_SOURCE,
    CONFIG_PAGE_PATH,
    DEFAULT_CAPTION_PROVIDER_CONFIG_KEY,
    IMAGEBED_IMPORT_CONFIG_KEY,
    EXTERNAL_LIBRARY_SOURCE,
    GLOBAL_TAGS_CONFIG_KEY,
    IMAGEBED_LIBRARY_SOURCE,
    IMAGE_TAGS_CONFIG_KEY,
    LIBRARY_WATCH_INTERVAL_SECONDS,
    MANUAL_LIBRARY_SOURCE,
    MEME_COMBAT_CONFIG_KEY,
    MODEL_FALLBACK_CONFIG_KEY,
    PAGE_LIBRARY_DEFAULT_VIEW_MODE_CONFIG_KEY,
    Path,
    PROACTIVE_EMOJI_CONFIG_KEY,
    PROGRESS_PAGE_PATH,
    SCHEDULED_BACKUP_CONFIG_KEY,
    SEND_IMAGE_STYLE_CONFIG_KEY,
    TAG_CATEGORY_CONFIG_KEY,
    TAG_CATEGORY_LABEL_TO_KEY,
    TAG_CATEGORY_PRESETS,
    USER_SEARCH_CONFIG_KEY,
    normalize_auto_collection_non_meme_filter_strategy,
    _normalize_qq_id_list,
    asyncio,
    json,
    logger,
    re,
    shutil,
    time,
)


class CaptionLibraryMixin:
    async def _sync_library(
        self,
        force: bool = False,
        caption_mode: str = "background",
        initial_global_tags_by_rel_path: dict[str, list[str]] | None = None,
    ) -> None:
        async with self._lock:
            initial_global_tags_by_rel_path = initial_global_tags_by_rel_path or {}
            configured_rel_paths = self._configured_image_rel_paths()
            discovered_rel_paths = self._discover_uploaded_images()
            configured_tag_items = self._configured_tag_items()
            candidate_rel_paths = (
                configured_rel_paths
                | discovered_rel_paths
                | set(configured_tag_items.keys())
            )
            existing_rel_paths = self._existing_image_rel_paths(candidate_rel_paths)

            images = self._index.setdefault("images", {})
            if not isinstance(images, dict):
                images = {}
                self._index["images"] = images
            caption_task_running = bool(
                self._caption_task and not self._caption_task.done()
            )

            stale_by_digest: dict[str, dict[str, Any]] = {}
            for image_id in list(images.keys()):
                item = images.get(image_id)
                if not isinstance(item, dict):
                    images.pop(image_id, None)
                    continue
                rel_path = self._norm_rel_path(item.get("rel_path"))
                if not rel_path or rel_path not in existing_rel_paths:
                    digest = str(item.get("sha256") or "")
                    if digest:
                        stale_by_digest.setdefault(digest, dict(item))
                    images.pop(image_id, None)

            for rel_path in sorted(existing_rel_paths):
                abs_path = self._abs_plugin_data_path(rel_path)
                stat = abs_path.stat()
                image_id = self._image_id(rel_path)
                item = images.get(image_id)
                digest = await self._cached_sha256_async(abs_path)
                if not isinstance(item, dict) and digest in stale_by_digest:
                    item = dict(stale_by_digest[digest])
                    images[image_id] = item

                configured_tag_item = configured_tag_items.get(rel_path, {})
                configured_auto_tags = configured_tag_item.get("auto_tags", [])
                configured_tags = configured_tag_item.get("tags", [])
                configured_global_tags = configured_tag_item.get(
                    "selected_global_tags",
                    [],
                )
                configured_manual_override = bool(
                    configured_tag_item.get("manual_tags_override", False)
                )
                item_tags = self._tags_from_item(item) if isinstance(item, dict) else []
                old_digest = (
                    str(item.get("sha256") or "") if isinstance(item, dict) else ""
                )
                content_changed = old_digest != digest
                old_caption_prompt_version = (
                    self._to_int(item.get("caption_prompt_version"), 0)
                    if isinstance(item, dict)
                    else 0
                )
                prompt_changed = old_caption_prompt_version < CAPTION_PROMPT_VERSION

                caption_status = (
                    str(item.get("caption_status") or "")
                    if isinstance(item, dict)
                    else ""
                )
                auto_tags = (
                    self._normalize_tags(item.get("auto_tags", []))
                    if isinstance(item, dict)
                    else []
                )
                if configured_auto_tags:
                    auto_tags = configured_auto_tags
                    if caption_status not in {"pending", "running", "failed"}:
                        caption_status = "done"
                elif (
                    not auto_tags
                    and item_tags
                    and not content_changed
                    and caption_status not in {"pending", "running", "failed"}
                    and not (
                        configured_manual_override
                        or (
                            isinstance(item, dict)
                            and item.get("manual_tags_override")
                        )
                    )
                ):
                    auto_tags = item_tags

                if configured_tag_item:
                    manual_override = configured_manual_override or bool(
                        configured_auto_tags
                        and configured_tags != configured_auto_tags
                    )
                    if manual_override:
                        manual_tags = configured_tags
                    elif configured_auto_tags and configured_tags == configured_auto_tags:
                        manual_tags = []
                    else:
                        manual_tags = configured_tags
                    selected_global_tags = configured_global_tags
                elif isinstance(item, dict):
                    manual_tags = self._normalize_tags(item.get("manual_tags", []))
                    manual_override = bool(item.get("manual_tags_override", False))
                    selected_global_tags = self._valid_global_tags(
                        item.get("selected_global_tags", [])
                    )
                else:
                    manual_tags = []
                    manual_override = False
                    selected_global_tags = self._valid_global_tags(
                        initial_global_tags_by_rel_path.get(rel_path, [])
                    )

                needs_caption = (
                    not isinstance(item, dict)
                    or content_changed
                    or force
                    or prompt_changed
                    or caption_status in {"pending", "running", "failed"}
                    or not auto_tags
                )

                if not isinstance(item, dict):
                    item = {}
                    images[image_id] = item

                item.update(
                    {
                        "id": image_id,
                        "rel_path": rel_path,
                        "filename": abs_path.name,
                        "library_source": self._library_source_for_rel_path(
                            rel_path,
                            item if isinstance(item, dict) else None,
                        ),
                        "sha256": digest,
                        "size": stat.st_size,
                        "mtime": int(stat.st_mtime),
                        "updated_at": int(time.time()),
                    }
                )

                if needs_caption and caption_mode == "blocking":
                    auto_tags = await self._caption_image(abs_path)
                    if not auto_tags:
                        auto_tags = self._normalize_caption_tags([], abs_path.name)
                    item["captioned_at"] = int(time.time())
                    item["caption_status"] = "done"
                elif needs_caption:
                    if content_changed or force or prompt_changed or not auto_tags:
                        auto_tags = self._normalize_caption_tags([], abs_path.name)
                    item["caption_status"] = (
                        "running"
                        if caption_status == "running" and caption_task_running
                        else "pending"
                    )
                else:
                    item["caption_status"] = "done"

                item["auto_tags"] = auto_tags
                item["manual_tags"] = manual_tags
                item["manual_tags_override"] = manual_override
                item["selected_global_tags"] = selected_global_tags
                if manual_override:
                    item["tags"] = self._merge_tags(
                        manual_tags,
                        selected_global_tags,
                    )
                else:
                    item["tags"] = self._merge_tags(
                        auto_tags,
                        manual_tags,
                        selected_global_tags,
                    )
                item["tag_source"] = "caption+config"
                item["caption_prompt_version"] = CAPTION_PROMPT_VERSION

            self._save_index()
            self._sync_config_image_files(existing_rel_paths)
            self._sync_config_tags(existing_rel_paths)
            self._refresh_image_tag_schema(existing_rel_paths)
            self._last_library_signature = self._library_signature_for_rel_paths(
                existing_rel_paths
            )
            if caption_mode == "background":
                self._start_caption_background_task()

    def _start_upload_watch_task(self) -> None:
        if self._watch_task and not self._watch_task.done():
            return
        try:
            self._watch_task = asyncio.create_task(self._watch_uploaded_images())
        except RuntimeError:
            logger.warning(
                "astrbot_plugin_smart_imagechat_hub: failed to start upload watcher; no running event loop."
            )

    async def _watch_uploaded_images(self) -> None:
        while True:
            await asyncio.sleep(LIBRARY_WATCH_INTERVAL_SECONDS)
            try:
                await self._sync_library_if_changed(caption_mode="background")
            except asyncio.CancelledError:
                raise
            except Exception as exc:
                logger.warning(
                    "astrbot_plugin_smart_imagechat_hub: upload watcher sync failed: %s",
                    exc,
                    exc_info=True,
                )

    async def _sync_library_if_changed(self, caption_mode: str = "background") -> None:
        if self._external_import_task and not self._external_import_task.done():
            return
        if self._imagebed_import_task and not self._imagebed_import_task.done():
            return
        signature = self._library_signature()
        task_running = bool(self._caption_task and not self._caption_task.done())
        waiting_without_task = (
            bool(self._pending_caption_rel_paths(include_failed=False))
            or self._running_caption_count() > 0
        ) and not task_running
        if self._caption_task and self._caption_task.done():
            self._caption_task = None
        if signature == self._last_library_signature and not waiting_without_task:
            return
        await self._sync_library(caption_mode=caption_mode)

    def _library_signature(self) -> str:
        rel_paths = (
            self._configured_image_rel_paths()
            | self._discover_uploaded_images()
            | set(self._configured_tag_items().keys())
        )
        return self._library_signature_for_rel_paths(rel_paths)

    def _library_signature_for_rel_paths(self, rel_paths: set[str]) -> str:
        chunks = []
        for rel_path in sorted(rel_paths):
            try:
                abs_path = self._abs_plugin_data_path(rel_path)
                stat = abs_path.stat()
            except (OSError, ValueError):
                continue
            mtime_ns = getattr(stat, "st_mtime_ns", int(stat.st_mtime * 1_000_000_000))
            chunks.append(
                f"{rel_path}:{stat.st_size}:{int(stat.st_mtime)}:{mtime_ns}"
            )
        config_part = {
            IMAGE_TAGS_CONFIG_KEY: self.config.get(IMAGE_TAGS_CONFIG_KEY, []),
            GLOBAL_TAGS_CONFIG_KEY: self._config_get(GLOBAL_TAGS_CONFIG_KEY, []),
            TAG_CATEGORY_CONFIG_KEY: self._tag_category_settings(),
        }
        chunks.append(
            "config:"
            + json.dumps(config_part, ensure_ascii=False, sort_keys=True, default=str)
        )
        return "\n".join(chunks)

    def _start_caption_background_task(self) -> None:
        pending_rel_paths = self._pending_caption_rel_paths()
        if not pending_rel_paths:
            if self._caption_progress.get("status") in {"idle", "pending", "running"}:
                self._set_caption_progress(
                    status="done",
                    total=0,
                    completed=0,
                    failed=0,
                    remaining=0,
                    current_image="",
                    message="No images are waiting for tag generation.",
                    error_detail="",
                    error_image="",
                    error_message="",
                    error_source="",
                )
            return
        if self._caption_task and not self._caption_task.done():
            logger.info(
                "astrbot_plugin_smart_imagechat_hub: image tag generation already running, %s image(s) pending.",
                len(pending_rel_paths),
            )
            self._set_caption_progress(
                status="running",
                remaining=len(pending_rel_paths),
                message="Image tag generation is already running.",
            )
            return
        self._set_caption_progress(
            status="pending",
            total=len(pending_rel_paths),
            completed=0,
            failed=0,
            remaining=len(pending_rel_paths),
            current_image="",
            started_at=None,
            message=f"Image tag generation queued for {len(pending_rel_paths)} image(s).",
            error_detail="",
            error_image="",
            error_message="",
            error_source="",
        )
        try:
            self._caption_task = asyncio.create_task(self._caption_pending_images())
        except RuntimeError:
            self._set_caption_progress(
                status="failed",
                remaining=len(pending_rel_paths),
                current_image="",
                message="Failed to start image tag generation; no running event loop.",
            )
            logger.warning(
                "astrbot_plugin_smart_imagechat_hub: failed to start background image tag generation; no running event loop."
            )

    async def _cancel_caption_task(self) -> None:
        if not self._caption_task or self._caption_task.done():
            await self._wait_caption_cleanup_tasks()
            return
        self._caption_task.cancel()
        try:
            await self._caption_task
        except asyncio.CancelledError:
            pass
        self._caption_task = None
        await self._wait_caption_cleanup_tasks()

    def _track_caption_cleanup_task(self, task: asyncio.Task) -> None:
        self._caption_cleanup_tasks.add(task)
        task.add_done_callback(self._caption_cleanup_tasks.discard)
        task.add_done_callback(self._log_caption_cleanup_error)

    def _log_caption_cleanup_error(self, task: asyncio.Task) -> None:
        try:
            task.result()
        except asyncio.CancelledError:
            logger.warning(
                "astrbot_plugin_smart_imagechat_hub: caption cleanup task was cancelled."
            )
        except Exception as exc:
            logger.warning(
                "astrbot_plugin_smart_imagechat_hub: caption cleanup task failed: %s",
                exc,
                exc_info=True,
            )

    async def _wait_caption_cleanup_tasks(self) -> None:
        tasks = [task for task in self._caption_cleanup_tasks if not task.done()]
        if not tasks:
            return
        await asyncio.gather(*(asyncio.shield(task) for task in tasks), return_exceptions=True)

    def _make_caption_progress(self, **updates: Any) -> dict[str, Any]:
        now = int(time.time())
        progress = {
            "status": "idle",
            "total": 0,
            "completed": 0,
            "failed": 0,
            "remaining": 0,
            "current_image": "",
            "message": "",
            "started_at": None,
            "updated_at": now,
            "percent": 0,
            "running": False,
            "error_detail": "",
            "error_image": "",
            "error_message": "",
            "error_source": "",
        }
        progress.update(updates)
        return self._normalize_caption_progress(progress)

    def _set_caption_progress(self, **updates: Any) -> None:
        progress = dict(self._caption_progress)
        progress.update(updates)
        progress["updated_at"] = int(time.time())
        self._caption_progress = self._normalize_caption_progress(progress)

    def _normalize_caption_progress(self, progress: dict[str, Any]) -> dict[str, Any]:
        status = str(progress.get("status") or "idle")
        total = max(self._to_int(progress.get("total"), 0), 0)
        completed = max(self._to_int(progress.get("completed"), 0), 0)
        failed = max(self._to_int(progress.get("failed"), 0), 0)
        remaining = max(self._to_int(progress.get("remaining"), 0), 0)
        processed = min(completed + failed, total) if total else completed + failed
        if total <= 0:
            percent = 100 if status == "done" else 0
        else:
            percent = min(int((processed / total) * 100), 100)
        progress.update(
            {
                "status": status,
                "total": total,
                "completed": completed,
                "failed": failed,
                "remaining": remaining,
                "current_image": str(progress.get("current_image") or ""),
                "message": str(progress.get("message") or ""),
                "error_detail": str(progress.get("error_detail") or ""),
                "error_image": str(progress.get("error_image") or ""),
                "error_message": str(progress.get("error_message") or ""),
                "error_source": str(progress.get("error_source") or ""),
                "percent": percent,
                "running": status == "running",
            }
        )
        return progress

    def _caption_progress_snapshot(self) -> dict[str, Any]:
        snapshot = dict(self._caption_progress)
        pending_count = len(self._pending_caption_rel_paths())
        running_count = self._running_caption_count()
        task_running = bool(self._caption_task and not self._caption_task.done())
        if task_running:
            snapshot["status"] = "running"
            snapshot["running"] = True
        elif pending_count and snapshot.get("status") in {"idle", "running"}:
            snapshot["status"] = "pending"
            snapshot["running"] = False
            snapshot["remaining"] = pending_count
            if not self._to_int(snapshot.get("total"), 0):
                snapshot["total"] = pending_count
            if not snapshot.get("message"):
                snapshot["message"] = "Images are waiting for tag generation."
        elif (
            self._external_caption_paused()
            and self._external_pending_count() > 0
            and snapshot.get("status") in {"idle", "pending", "running", "done"}
        ):
            external_pending_count = self._external_pending_count()
            snapshot["status"] = "pending"
            snapshot["running"] = False
            snapshot["remaining"] = external_pending_count
            snapshot["total"] = external_pending_count
            snapshot["message"] = "External import tag generation paused."
        elif (
            self._imagebed_caption_paused()
            and self._imagebed_pending_count() > 0
            and snapshot.get("status") in {"idle", "pending", "running", "done"}
        ):
            imagebed_pending_count = self._imagebed_pending_count()
            snapshot["status"] = "pending"
            snapshot["running"] = False
            snapshot["remaining"] = imagebed_pending_count
            snapshot["total"] = imagebed_pending_count
            snapshot["message"] = "Imagebed import tag generation paused."
        else:
            snapshot["running"] = False
        snapshot["pending_images"] = pending_count
        snapshot["running_images"] = running_count
        snapshot["library_images"] = self._index_image_count()
        snapshot["updated_at"] = snapshot.get("updated_at") or int(time.time())
        snapshot = self._normalize_caption_progress(snapshot)
        snapshot["progress_page_url"] = PROGRESS_PAGE_PATH
        snapshot["config_page_url"] = CONFIG_PAGE_PATH
        snapshot["config_ready"] = (
            snapshot.get("status") in {"done", "failed", "cancelled"}
            and not snapshot.get("running")
        )
        snapshot["imagebed_import"] = self._imagebed_import_status_snapshot()
        return snapshot

    def _caption_library_snapshot(self) -> dict[str, Any]:
        images = self._index.get("images", {})
        manual_items = []
        solidified_items = []
        external_items = []
        imagebed_items = []
        if isinstance(images, dict):
            for item in images.values():
                if not isinstance(item, dict):
                    continue
                rel_path = self._norm_rel_path(item.get("rel_path"))
                if not rel_path:
                    continue
                if item.get("caption_status") != "done":
                    continue
                try:
                    abs_path = self._abs_plugin_data_path(rel_path)
                except ValueError:
                    continue
                if not abs_path.is_file():
                    continue
                library_item = self._caption_library_image_item(item)
                source = library_item.get("library_source", MANUAL_LIBRARY_SOURCE)
                if source == COLLECTED_LIBRARY_SOURCE:
                    solidified_items.append(library_item)
                elif source == EXTERNAL_LIBRARY_SOURCE:
                    external_items.append(library_item)
                elif source == IMAGEBED_LIBRARY_SOURCE:
                    imagebed_items.append(library_item)
                else:
                    manual_items.append(library_item)

        sort_key = (
            lambda item: (
                self._to_int(item.get("captioned_at"), 0),
                self._to_int(item.get("updated_at"), 0),
            )
        )
        manual_items.sort(
            key=sort_key,
            reverse=True,
        )
        solidified_items.sort(
            key=sort_key,
            reverse=True,
        )
        external_items.sort(
            key=sort_key,
            reverse=True,
        )
        imagebed_items.sort(
            key=sort_key,
            reverse=True,
        )
        all_items = manual_items + solidified_items + external_items + imagebed_items
        return {
            "images": manual_items,
            "manual_images": manual_items,
            "solidified_images": solidified_items,
            "external_images": external_items,
            "imagebed_images": imagebed_items,
            "all_images": all_items,
            "global_tags": self._global_tags(),
            PAGE_LIBRARY_DEFAULT_VIEW_MODE_CONFIG_KEY: (
                self._page_library_default_view_mode()
            ),
            "updated_at": int(time.time()),
        }

    def _library_items_for_source(self, source: str = "") -> list[dict[str, Any]]:
        snapshot = self._caption_library_snapshot()
        if source == COLLECTED_LIBRARY_SOURCE:
            return snapshot.get("solidified_images", [])
        if source == EXTERNAL_LIBRARY_SOURCE:
            return snapshot.get("external_images", [])
        if source == IMAGEBED_LIBRARY_SOURCE:
            return snapshot.get("imagebed_images", [])
        if source == MANUAL_LIBRARY_SOURCE:
            return snapshot.get("manual_images", [])
        return snapshot.get("all_images", [])

    def _sort_library_items(self, items: list[dict[str, Any]]) -> list[dict[str, Any]]:
        return sorted(
            items,
            key=lambda item: (
                self._to_int(item.get("captioned_at"), 0),
                self._to_int(item.get("updated_at"), 0),
            ),
            reverse=True,
        )

    def _plugin_config_snapshot(self) -> dict[str, Any]:
        return {
            "user_search_enabled": self._cfg_bool("user_search_enabled"),
            "user_search_flow": {
                "enabled": self._cfg_bool("user_search_enabled"),
                "request_keywords": self._request_keywords(),
            },
            AUTO_COLLECTION_CONFIG_KEY: self._auto_collection_config(),
            IMAGEBED_IMPORT_CONFIG_KEY: self._imagebed_config_snapshot(),
            MEME_COMBAT_CONFIG_KEY: self._meme_combat_config(),
            SEND_IMAGE_STYLE_CONFIG_KEY: self._send_image_style_config(),
            SCHEDULED_BACKUP_CONFIG_KEY: self._scheduled_backup_config(),
            MODEL_FALLBACK_CONFIG_KEY: self._model_fallback_snapshot(),
            "request_keywords": self._request_keywords(),
            "hidden_images": sorted(self._hidden_rel_paths()),
            "sync_on_startup": self._cfg_bool("sync_on_startup"),
            "match_confidence_threshold": self._cfg_float(
                "match_confidence_threshold"
            ),
            PAGE_LIBRARY_DEFAULT_VIEW_MODE_CONFIG_KEY: (
                self._page_library_default_view_mode()
            ),
            "reply_after_search": {
                "use_custom_reply": self._cfg_bool("use_custom_reply"),
                "custom_reply": self._cfg_str("custom_reply"),
                "llm_reply_when_not_found": self._cfg_bool(
                    "llm_reply_when_not_found"
                ),
                "not_found_reply": self._cfg_str("not_found_reply"),
                "empty_library_reply": self._cfg_str("empty_library_reply"),
            },
            "updated_at": int(time.time()),
        }

    def _update_plugin_config_from_payload(self, payload: dict[str, Any]) -> None:
        raw_auto_collection_cfg = payload.get(AUTO_COLLECTION_CONFIG_KEY)
        if isinstance(raw_auto_collection_cfg, dict):
            self.config[AUTO_COLLECTION_CONFIG_KEY] = (
                self._normalize_auto_collection_config(raw_auto_collection_cfg)
            )
        raw_scheduled_backup_cfg = payload.get(SCHEDULED_BACKUP_CONFIG_KEY)
        if isinstance(raw_scheduled_backup_cfg, dict):
            self.config[SCHEDULED_BACKUP_CONFIG_KEY] = (
                self._normalize_scheduled_backup_config(raw_scheduled_backup_cfg)
            )
            self._restart_scheduled_backup_task()
        raw_imagebed_cfg = payload.get(IMAGEBED_IMPORT_CONFIG_KEY)
        if isinstance(raw_imagebed_cfg, dict):
            self._set_imagebed_import_config(
                raw_imagebed_cfg,
                save_plugin_config=False,
                save_state=True,
            )
            self._restart_imagebed_sync_task()
        raw_model_fallback_cfg = payload.get(MODEL_FALLBACK_CONFIG_KEY)
        if isinstance(raw_model_fallback_cfg, dict):
            self.config[MODEL_FALLBACK_CONFIG_KEY] = (
                self._normalize_model_fallback_config(raw_model_fallback_cfg)
            )
        raw_meme_combat_cfg = payload.get(MEME_COMBAT_CONFIG_KEY)
        if isinstance(raw_meme_combat_cfg, dict):
            self.config[MEME_COMBAT_CONFIG_KEY] = (
                self._normalize_meme_combat_config(raw_meme_combat_cfg)
            )
        raw_send_image_style_cfg = payload.get(SEND_IMAGE_STYLE_CONFIG_KEY)
        if isinstance(raw_send_image_style_cfg, dict):
            self.config[SEND_IMAGE_STYLE_CONFIG_KEY] = (
                self._normalize_send_image_style_config(raw_send_image_style_cfg)
            )
        raw_user_search_cfg = payload.get(USER_SEARCH_CONFIG_KEY)
        if isinstance(raw_user_search_cfg, dict):
            self._set_user_search_config(
                enabled=raw_user_search_cfg.get(
                    "enabled",
                    self._cfg_bool("user_search_enabled"),
                ),
                keywords=raw_user_search_cfg.get(
                    "request_keywords",
                    self._request_keywords(),
                ),
            )
        if "user_search_enabled" in payload:
            self._set_user_search_config(enabled=payload.get("user_search_enabled"))
        if "request_keywords" in payload:
            self._set_user_search_config(keywords=payload.get("request_keywords"))
        if "hidden_images" in payload:
            self.config["hidden_images"] = sorted(
                {
                    rel_path
                    for rel_path in (
                        self._norm_rel_path(raw)
                        for raw in self._list_from_payload(payload.get("hidden_images"))
                    )
                    if rel_path
                }
            )
        if "sync_on_startup" in payload:
            self.config["sync_on_startup"] = self._to_bool(
                payload.get("sync_on_startup"),
                True,
            )
        if "match_confidence_threshold" in payload:
            confidence = self._to_float(
                payload.get("match_confidence_threshold"),
                0.45,
            )
            self.config["match_confidence_threshold"] = max(
                0.0,
                min(confidence, 1.0),
            )
        if PAGE_LIBRARY_DEFAULT_VIEW_MODE_CONFIG_KEY in payload:
            self.config[PAGE_LIBRARY_DEFAULT_VIEW_MODE_CONFIG_KEY] = (
                self._normalize_page_library_default_view_mode(
                    payload.get(PAGE_LIBRARY_DEFAULT_VIEW_MODE_CONFIG_KEY)
                )
            )

        raw_reply_cfg = payload.get("reply_after_search")
        if isinstance(raw_reply_cfg, dict):
            current_reply_cfg = dict(self._reply_cfg())
            if "use_custom_reply" in raw_reply_cfg:
                current_reply_cfg["use_custom_reply"] = self._to_bool(
                    raw_reply_cfg.get("use_custom_reply"),
                    True,
                )
            if "custom_reply" in raw_reply_cfg:
                current_reply_cfg["custom_reply"] = self._clean_text(
                    raw_reply_cfg.get("custom_reply"),
                    "找到一张比较合适的图。",
                )
            if "llm_reply_when_not_found" in raw_reply_cfg:
                current_reply_cfg["llm_reply_when_not_found"] = self._to_bool(
                    raw_reply_cfg.get("llm_reply_when_not_found"),
                    False,
                )
            if "not_found_reply" in raw_reply_cfg:
                current_reply_cfg["not_found_reply"] = self._clean_text(
                    raw_reply_cfg.get("not_found_reply"),
                    "图库里暂时没有找到特别合适的图片。",
                )
            if "empty_library_reply" in raw_reply_cfg:
                current_reply_cfg["empty_library_reply"] = self._clean_text(
                    raw_reply_cfg.get("empty_library_reply"),
                    "图库里还没有可用图片，请先在插件配置里上传图片。",
                )
            self.config["reply_after_search"] = current_reply_cfg
            self.config["reply_config_migrated"] = True

    def _tag_category_settings_snapshot(self) -> dict[str, Any]:
        settings = self._tag_category_settings()
        return {
            "preset_categories": dict(TAG_CATEGORY_PRESETS),
            "enabled_presets": settings["enabled_presets"],
            "custom_categories": settings["custom_categories"],
            DEFAULT_CAPTION_PROVIDER_CONFIG_KEY: settings[
                DEFAULT_CAPTION_PROVIDER_CONFIG_KEY
            ],
            "provider_id": settings[DEFAULT_CAPTION_PROVIDER_CONFIG_KEY],
            "provider_options": self._chat_provider_options(),
            "provider_warning": not bool(
                settings[DEFAULT_CAPTION_PROVIDER_CONFIG_KEY]
            ),
            "updated_at": int(time.time()),
        }

    def _proactive_emoji_snapshot(self) -> dict[str, Any]:
        cfg = self._proactive_emoji_config()
        return {
            **cfg,
            "provider_options": self._chat_provider_options(),
            "inherited_provider_label": self._current_chat_provider_label(),
            "updated_at": int(time.time()),
        }

    def _auto_collection_snapshot(self) -> dict[str, Any]:
        return {
            **self._auto_collection_config(),
            "pending_count": len(self._collection_pool_items()),
            "solidified_count": self._source_image_count(COLLECTED_LIBRARY_SOURCE),
            "solidified_remaining_capacity": (
                self._solidified_remaining_capacity()
            ),
            "updated_at": int(time.time()),
        }

    def _scheduled_backup_snapshot(self) -> dict[str, Any]:
        cfg = self._scheduled_backup_config()
        return {
            **cfg,
            "backup_files": self._scheduled_backup_files(),
            "storage_dir": str(self._scheduled_backup_dir()),
            "updated_at": int(time.time()),
        }

    def _caption_provider_config_snapshot(self) -> dict[str, Any]:
        return {
            "provider_id": self._default_image_caption_provider_id(),
            "provider_options": self._chat_provider_options(),
            "updated_at": int(time.time()),
        }

    def _page_library_default_view_mode(self) -> str:
        return self._normalize_page_library_default_view_mode(
            self.config.get(PAGE_LIBRARY_DEFAULT_VIEW_MODE_CONFIG_KEY)
        )

    def _normalize_page_library_default_view_mode(self, raw: Any) -> str:
        return "gallery" if str(raw or "").strip() == "gallery" else "list"

    def _proactive_emoji_config(self) -> dict[str, Any]:
        return self._normalize_proactive_emoji_config(
            self.config.get(PROACTIVE_EMOJI_CONFIG_KEY, {})
        )

    def _auto_collection_config(self) -> dict[str, Any]:
        return self._normalize_auto_collection_config(
            self.config.get(AUTO_COLLECTION_CONFIG_KEY, {})
        )

    def _scheduled_backup_config(self) -> dict[str, Any]:
        return self._normalize_scheduled_backup_config(
            self.config.get(SCHEDULED_BACKUP_CONFIG_KEY, {})
        )

    def _send_image_style_config(self) -> dict[str, Any]:
        return self._normalize_send_image_style_config(
            self.config.get(SEND_IMAGE_STYLE_CONFIG_KEY, {})
        )

    def _normalize_send_image_style_config(self, raw: Any) -> dict[str, Any]:
        raw = raw if isinstance(raw, dict) else {}
        return {
            "enabled": self._to_bool(raw.get("enabled"), True),
            "meme_tag_only": self._to_bool(raw.get("meme_tag_only"), False),
        }

    def _normalize_auto_collection_config(self, raw: Any) -> dict[str, Any]:
        raw = raw if isinstance(raw, dict) else {}
        source_groups = self._normalize_group_ids(raw.get("source_groups", []))
        if not source_groups:
            source_groups = self._normalize_group_ids(raw.get("group_ids", []))
        ignored_sender_ids = _normalize_qq_id_list(raw.get("ignored_sender_ids", []))
        max_file_size_kb = self._to_int(raw.get("max_file_size_kb"), 1024)
        pending_pool_limit = self._to_int(raw.get("pending_pool_limit"), 100)
        pending_ttl_days = self._to_int(raw.get("pending_ttl_days"), 3)
        solidified_library_limit = self._to_int(
            raw.get("solidified_library_limit"),
            300,
        )
        non_meme_filter_strategy = normalize_auto_collection_non_meme_filter_strategy(
            raw
        )
        return {
            "enabled": self._to_bool(raw.get("enabled"), False),
            "include_in_features": self._to_bool(
                raw.get("include_in_features"),
                False,
            ),
            "auto_reject_discarded": self._to_bool(
                raw.get("auto_reject_discarded"),
                False,
            ),
            "source_groups": source_groups,
            "ignored_sender_ids": ignored_sender_ids,
            "non_meme_filter_strategy": non_meme_filter_strategy,
            "filter_obvious_non_meme_images": non_meme_filter_strategy == "loose",
            "max_file_size_kb": max(1, max_file_size_kb),
            "pending_pool_limit": max(0, pending_pool_limit),
            "pending_ttl_days": max(0, pending_ttl_days),
            "auto_accept": self._to_bool(raw.get("auto_accept"), False),
            "solidified_library_limit": solidified_library_limit,
        }

    def _normalize_scheduled_backup_config(self, raw: Any) -> dict[str, Any]:
        raw = raw if isinstance(raw, dict) else {}
        backup_time = self._normalize_backup_time(raw.get("backup_time"), "06:00")
        backup_limit = self._to_int(raw.get("backup_limit"), 3)
        return {
            "enabled": self._to_bool(raw.get("enabled"), True),
            "backup_time": backup_time,
            "backup_limit": max(1, backup_limit),
        }

    def _normalize_backup_time(self, value: Any, default: str = "06:00") -> str:
        text = str(value or "").strip()
        match = re.match(r"^(\d{1,2}):(\d{1,2})$", text)
        if not match:
            return default
        hour = self._to_int(match.group(1), -1)
        minute = self._to_int(match.group(2), -1)
        if hour < 0 or hour > 23 or minute < 0 or minute > 59:
            return default
        return f"{hour:02d}:{minute:02d}"

    def _normalize_group_ids(self, raw: Any) -> list[str]:
        items = self._list_from_payload(raw)
        group_ids = []
        for item in items:
            group_id = str(item or "").strip()
            if group_id and group_id not in group_ids:
                group_ids.append(group_id)
        return group_ids

    def _normalize_proactive_emoji_config(self, raw: Any) -> dict[str, Any]:
        raw = raw if isinstance(raw, dict) else {}
        provider_id = str(raw.get("analysis_provider_id") or "").strip()
        retrieval_mode = str(raw.get("retrieval_mode") or "").strip()
        if retrieval_mode not in {
            "bot_reply_serial",
            "user_message_parallel",
            "user_message_fast_prefilter",
        }:
            retrieval_mode = "bot_reply_serial"
        probability = self._to_float(raw.get("trigger_probability"), 0.25)
        return {
            "enabled": self._to_bool(raw.get("enabled"), False),
            "analysis_provider_id": provider_id,
            "retrieval_mode": retrieval_mode,
            "meme_only": self._to_bool(raw.get("meme_only"), True),
            "embed_in_conversation": self._to_bool(
                raw.get("embed_in_conversation"),
                True,
            ),
            "trigger_probability": str(max(0.0, min(probability, 1.0))),
            "debug_mode": self._to_bool(raw.get("debug_mode"), False),
        }

    def _chat_provider_options(self) -> list[dict[str, str]]:
        options = [{"id": "", "label": "继承 AstrBot 当前会话模型"}]
        for provider in self.context.get_all_providers():
            meta = provider.meta()
            provider_id = str(getattr(meta, "id", "") or "")
            if not provider_id:
                continue
            provider_type = str(getattr(meta, "type", "") or "").strip()
            model_name = str(
                getattr(meta, "model", "") or getattr(provider, "model_name", "") or ""
            ).strip()
            label = provider_id
            if provider_type:
                label = f"{provider_type} ({provider_id})"
            if model_name and model_name not in label:
                label = f"{label} - {model_name}"
            options.append({"id": provider_id, "label": label})
        return options

    def _current_chat_provider_label(self) -> str:
        try:
            provider = self.context.get_using_provider()
        except Exception:
            return ""
        if provider is None:
            return ""
        try:
            meta = provider.meta()
        except Exception:
            return ""
        provider_id = str(getattr(meta, "id", "") or "").strip()
        provider_type = str(getattr(meta, "type", "") or "").strip()
        model_name = str(
            getattr(meta, "model", "") or getattr(provider, "model_name", "") or ""
        ).strip()
        label = provider_id
        if provider_type:
            label = f"{provider_type} ({provider_id})"
        if model_name and model_name not in label:
            label = f"{label} - {model_name}"
        return label

    def _tag_category_settings(self) -> dict[str, Any]:
        raw = self.config.get(TAG_CATEGORY_CONFIG_KEY, {})
        settings = self._normalize_tag_category_settings(raw)
        provider_id = str(self.config.get(DEFAULT_CAPTION_PROVIDER_CONFIG_KEY) or "").strip()
        provider_ids = self._available_chat_provider_ids()
        if provider_id and provider_id not in provider_ids:
            provider_id = ""
        if not provider_id:
            provider_id = str(settings.get(DEFAULT_CAPTION_PROVIDER_CONFIG_KEY) or "").strip()
            if provider_id and provider_id not in provider_ids:
                provider_id = ""
        if not provider_id:
            provider_id = self._system_default_image_caption_provider_id()
            if provider_id and provider_id not in provider_ids:
                provider_id = ""
        settings[DEFAULT_CAPTION_PROVIDER_CONFIG_KEY] = provider_id
        return settings

    def _normalize_tag_category_settings(self, raw: Any) -> dict[str, Any]:
        raw = raw if isinstance(raw, dict) else {}
        enabled_raw = raw.get("enabled_presets")
        if isinstance(enabled_raw, str):
            enabled_raw = re.split(r"[\n,，、;； ]+", enabled_raw)
        if isinstance(enabled_raw, list):
            enabled = []
            for item in enabled_raw:
                text = str(item).strip()
                preset_key = text if text in TAG_CATEGORY_PRESETS else ""
                if not preset_key:
                    preset_key = TAG_CATEGORY_LABEL_TO_KEY.get(text, "")
                if preset_key:
                    enabled.append(preset_key)
        else:
            enabled = list(TAG_CATEGORY_PRESETS.keys())

        deduped_enabled = []
        for preset_key in TAG_CATEGORY_PRESETS:
            if preset_key in enabled and preset_key not in deduped_enabled:
                deduped_enabled.append(preset_key)

        custom_categories = self._normalize_tags(raw.get("custom_categories", []))
        provider_id = str(
            raw.get(DEFAULT_CAPTION_PROVIDER_CONFIG_KEY) or ""
        ).strip()
        return {
            "enabled_presets": deduped_enabled,
            "custom_categories": custom_categories,
            DEFAULT_CAPTION_PROVIDER_CONFIG_KEY: provider_id,
        }

    def _tag_category_settings_for_storage(
        self,
        settings: dict[str, Any],
    ) -> dict[str, Any]:
        normalized = self._normalize_tag_category_settings(settings)
        return {
            "enabled_presets": [
                TAG_CATEGORY_PRESETS[key]
                for key in normalized["enabled_presets"]
                if key in TAG_CATEGORY_PRESETS
            ],
            "custom_categories": " ".join(normalized["custom_categories"]),
            DEFAULT_CAPTION_PROVIDER_CONFIG_KEY: normalized[
                DEFAULT_CAPTION_PROVIDER_CONFIG_KEY
            ],
        }

    def _tag_category_generation_settings_changed(
        self,
        old_settings: dict[str, Any],
        new_settings: dict[str, Any],
    ) -> bool:
        return (
            old_settings.get("enabled_presets", [])
            != new_settings.get("enabled_presets", [])
            or old_settings.get("custom_categories", [])
            != new_settings.get("custom_categories", [])
        )

    def _caption_category_labels(self) -> list[str]:
        settings = self._tag_category_settings()
        labels = [
            TAG_CATEGORY_PRESETS[key]
            for key in settings["enabled_presets"]
            if key in TAG_CATEGORY_PRESETS
        ]
        labels.extend(settings["custom_categories"])
        return self._normalize_tags(labels)

    def _caption_category_enabled(self, preset_key: str) -> bool:
        return preset_key in self._tag_category_settings()["enabled_presets"]

    def _caption_category_prompt_rules(self) -> str:
        settings = self._tag_category_settings()
        enabled = set(settings["enabled_presets"])
        rules = []
        if "image_type" in enabled:
            rules.append(
                "1. 必须包含且只能包含一个基础图片类型标签，这个标签只能从“照片”和“表情包”中二选一。"
            )
            rules.append(
                "2. 除基础图片类型标签外，最多再生成 1 个图片类型/风格相关标签，例如“二次元”“自拍”“截图”“动图”；不要生成超过 2 个图片类型相关标签。"
            )
        else:
            rules.append("1. 不要专门生成“照片”或“表情包”等基础图片类型标签，除非自定义类别明确要求。")
        if "person_features" in enabled:
            rules.append("3. 如果图片中有人物，可以描述人物特征、发色、服饰、表情或整体印象。")
        if "body_shape" in enabled:
            rules.append(
                "4. 如果图片中存在女性人物，必须在不违反安全规则、不过度性化、不中伤人物的前提下，生成 1 个描述角色身材是否丰满的中性标签，例如“身材丰满”“身材匀称”“身材纤细”或“身材不明显”。"
            )
        if "emotion" in enabled:
            rules.append("5. 可以描述图片里的主要情绪或氛围。")
        if "action" in enabled:
            rules.append("6. 可以描述主体的动作、姿态或互动。")
        if "image_text" in enabled:
            rules.append(
                "7. 如果图片中包含文字，请额外生成 1 个纯文字内容标签：这个标签只能包含图片中的原文文字，不要加“文字”“台词”“内容”等前缀，不要概括或解释；如果没有可辨认文字，就不要生成这个标签。"
            )
        if settings["custom_categories"]:
            rules.append(
                "8. 自定义类别需要优先覆盖："
                + "、".join(settings["custom_categories"])
                + "。"
            )
        if not rules:
            rules.append("1. 请基于图片主体、场景和用途生成简短中文标签。")
        return "\n".join(rules)

    def _reset_all_caption_tags_for_new_categories(self) -> None:
        images = self._index.get("images", {})
        if not isinstance(images, dict):
            return
        now = int(time.time())
        for item in images.values():
            if not isinstance(item, dict):
                continue
            selected_global_tags = self._valid_global_tags(
                item.get("selected_global_tags", [])
            )
            item["auto_tags"] = []
            item["manual_tags"] = []
            item["manual_tags_override"] = False
            item["selected_global_tags"] = selected_global_tags
            item["tags"] = selected_global_tags
            item["caption_status"] = "pending"
            item["caption_prompt_version"] = 0
            item["captioned_at"] = 0
            item["updated_at"] = now

    def _list_from_payload(self, value: Any) -> list[Any]:
        if isinstance(value, list):
            return value
        if isinstance(value, str):
            return re.split(r"[\n,，、;；]+", value)
        return []

    def _running_caption_count(self) -> int:
        images = self._index.get("images", {})
        if not isinstance(images, dict):
            return 0
        return sum(
            1
            for item in images.values()
            if isinstance(item, dict) and item.get("caption_status") == "running"
        )

    def _index_image_count(self) -> int:
        images = self._index.get("images", {})
        return len(images) if isinstance(images, dict) else 0

    def _pending_caption_rel_paths(self, include_failed: bool = True) -> list[str]:
        images = self._index.get("images", {})
        if not isinstance(images, dict):
            return []
        waiting_statuses = {"pending", "failed"} if include_failed else {"pending"}
        rel_paths = []
        for item in images.values():
            if not isinstance(item, dict):
                continue
            if item.get("caption_status") not in waiting_statuses:
                continue
            if self._is_paused_external_caption_item(item):
                continue
            if self._is_paused_imagebed_caption_item(item):
                continue
            rel_path = self._norm_rel_path(item.get("rel_path"))
            if rel_path:
                rel_paths.append(rel_path)
        return sorted(set(rel_paths))

    async def _cleanup_running_caption_state(
        self,
        attempted_rel_paths: set[str],
    ) -> int:
        async with self._lock:
            images = self._index.get("images", {})
            if isinstance(images, dict):
                for item in images.values():
                    if (
                        isinstance(item, dict)
                        and item.get("caption_status") == "running"
                    ):
                        item["caption_status"] = "pending"
                self._save_index()
                existing_rel_paths = self._all_existing_index_rel_paths()
                self._sync_config_image_files(existing_rel_paths)
                self._sync_config_tags(existing_rel_paths)
                self._refresh_image_tag_schema(existing_rel_paths)
                self._last_library_signature = (
                    self._library_signature_for_rel_paths(existing_rel_paths)
                )
            return len(
                [
                    path
                    for path in self._pending_caption_rel_paths()
                    if path not in attempted_rel_paths
                ]
            )

    def _caption_source_failure_hint(self, source: str) -> str:
        if source == COLLECTED_LIBRARY_SOURCE:
            return (
                "自动标签进程失败。失败的固化图像已退回待筛选图片池，"
                "需要再次选择图片并点击“批量入库”按钮进行标签生成。"
            )
        if source == EXTERNAL_LIBRARY_SOURCE:
            return (
                "自动标签进程失败。失败的外部导入图像仍保留在“导入进程”栏目中，"
                "需要重新点击“开始”按钮进行标签生成。"
            )
        if source == IMAGEBED_LIBRARY_SOURCE:
            return (
                "自动标签进程失败。失败的图床同步图像仍保留在“导入进程”栏目中，"
                "需要重新点击“开始”按钮进行标签生成。"
            )
        return (
            "自动标签进程失败。失败的手动上传图像已移除，"
            "需要重新上传图片。"
        )

    def _rollback_caption_failed_item(
        self,
        item: dict[str, Any],
        rel_path: str,
    ) -> str:
        source = self._library_source_for_rel_path(rel_path, item)
        if source == EXTERNAL_LIBRARY_SOURCE:
            item["caption_status"] = "pending"
            item["caption_prompt_version"] = 0
            item["captioned_at"] = 0
            item["updated_at"] = int(time.time())
            self._external_import_state["caption_paused"] = True
            self._save_external_import_state()
            return source
        if source == IMAGEBED_LIBRARY_SOURCE:
            self._rollback_caption_failed_imagebed_item(item)
            return source
        if source == COLLECTED_LIBRARY_SOURCE:
            self._restore_caption_failed_solidified_item_to_pool(item, rel_path)
            return source
        self._delete_image(
            str(item.get("id") or self._image_id(rel_path)),
            source=MANUAL_LIBRARY_SOURCE,
            sync_after=False,
        )
        return MANUAL_LIBRARY_SOURCE

    def _restore_caption_failed_solidified_item_to_pool(
        self,
        item: dict[str, Any],
        rel_path: str,
    ) -> None:
        try:
            source_path = self._abs_plugin_data_path(rel_path)
        except ValueError:
            source_path = None
        if not source_path or not source_path.is_file():
            images = self._index.get("images", {})
            if isinstance(images, dict):
                images.pop(str(item.get("id") or self._image_id(rel_path)), None)
                images.pop(self._image_id(rel_path), None)
            return

        group_id = str(item.get("collected_from_group_id") or "restore")
        sender_id = str(item.get("collected_sender_id") or "")
        collected_at = self._to_int(item.get("collected_at"), int(time.time()))
        suffix = source_path.suffix.lower() or Path(rel_path).suffix.lower() or ".jpg"
        pending_rel_path = self._unique_collected_pending_rel_path(
            group_id,
            collected_at or int(time.time()),
            suffix,
        )
        pending_path = self._abs_plugin_data_path(pending_rel_path)
        pending_path.parent.mkdir(parents=True, exist_ok=True)
        try:
            source_path.replace(pending_path)
        except OSError:
            shutil.copyfile(source_path, pending_path)
            source_path.unlink()

        stat = pending_path.stat()
        image_id = self._image_id(pending_rel_path)
        images = self._index.get("images", {})
        if isinstance(images, dict):
            images.pop(str(item.get("id") or self._image_id(rel_path)), None)
            images.pop(self._image_id(rel_path), None)
        pool_images = self._collection_pool.setdefault("images", {})
        if not isinstance(pool_images, dict):
            pool_images = {}
            self._collection_pool["images"] = pool_images
        pool_images[image_id] = {
            "id": image_id,
            "rel_path": pending_rel_path,
            "filename": pending_path.name,
            "sha256": str(item.get("sha256") or ""),
            "size": stat.st_size,
            "mtime": int(stat.st_mtime),
            "group_id": group_id,
            "sender_id": sender_id,
            "collected_at": collected_at or int(time.time()),
        }
        self._save_collection_pool()

    async def _caption_pending_images(self) -> None:
        started_at = int(time.time())
        total = len(self._pending_caption_rel_paths())
        self._set_caption_progress(
            status="running",
            total=total,
            completed=0,
            failed=0,
            remaining=total,
            current_image="",
            started_at=started_at,
            message=f"Starting image tag generation for {total} image(s).",
            error_detail="",
            error_image="",
            error_message="",
            error_source="",
        )
        logger.info(
            "astrbot_plugin_smart_imagechat_hub: background image tag generation started, total=%s.",
            total,
        )
        completed = 0
        failed = 0
        cancelled = False
        fatal_error_stopped = False
        attempted_rel_paths: set[str] = set()

        try:
            while True:
                async with self._lock:
                    rel_paths = [
                        rel_path
                        for rel_path in self._pending_caption_rel_paths()
                        if rel_path not in attempted_rel_paths
                    ]
                    if not rel_paths:
                        break
                    total = completed + failed + len(rel_paths)
                    rel_path = rel_paths[0]
                    attempted_rel_paths.add(rel_path)
                    images = self._index.get("images", {})
                    item = (
                        images.get(self._image_id(rel_path))
                        if isinstance(images, dict)
                        else None
                    )
                    if not isinstance(item, dict):
                        continue
                    item["caption_status"] = "running"
                    self._save_index()
                    self._set_caption_progress(
                        status="running",
                        total=total,
                        completed=completed,
                        failed=failed,
                        remaining=len(rel_paths),
                        current_image=rel_path,
                        message=f"Generating tags for {rel_path}.",
                        error_detail="",
                        error_image="",
                        error_message="",
                        error_source="",
                    )

                try:
                    abs_path = self._abs_plugin_data_path(rel_path)
                    auto_tags = await self._caption_image(abs_path)
                    if not auto_tags:
                        auto_tags = self._normalize_caption_tags([], abs_path.name)
                    images = self._index.get("images", {})
                    item = (
                        images.get(self._image_id(rel_path))
                        if isinstance(images, dict)
                        else None
                    )
                    if isinstance(item, dict):
                        auto_tags = self._merge_tags(
                            auto_tags,
                            item.get("import_extra_tags", []),
                        )
                    generation_failed = False
                    fatal_error: CaptionGenerationError | None = None
                except asyncio.CancelledError:
                    raise
                except CaptionGenerationError as exc:
                    logger.error(
                        "astrbot_plugin_smart_imagechat_hub: image tag generation stopped for %s: %s",
                        rel_path,
                        exc,
                        exc_info=True,
                    )
                    auto_tags = []
                    generation_failed = True
                    fatal_error = exc
                except Exception as exc:
                    logger.error(
                        "astrbot_plugin_smart_imagechat_hub: image tag generation failed for %s: %s",
                        rel_path,
                        exc,
                        exc_info=True,
                    )
                    auto_tags = []
                    generation_failed = True
                    fatal_error = CaptionGenerationError(str(exc), detail=str(exc))

                async with self._lock:
                    images = self._index.get("images", {})
                    item = (
                        images.get(self._image_id(rel_path))
                        if isinstance(images, dict)
                        else None
                    )
                    if not isinstance(item, dict):
                        continue
                    if fatal_error:
                        failed += 1
                        source = self._rollback_caption_failed_item(item, rel_path)
                        self._save_index()
                        existing_rel_paths = self._all_existing_index_rel_paths()
                        self._sync_config_image_files(existing_rel_paths)
                        self._sync_config_tags(existing_rel_paths)
                        self._refresh_image_tag_schema(existing_rel_paths)
                        self._last_library_signature = (
                            self._library_signature_for_rel_paths(existing_rel_paths)
                        )
                        remaining = len(
                            [
                                path
                                for path in self._pending_caption_rel_paths()
                                if path not in attempted_rel_paths
                            ]
                        )
                        total = completed + failed + remaining
                        message = self._caption_source_failure_hint(source)
                        self._set_caption_progress(
                            status="failed",
                            total=total,
                            completed=completed,
                            failed=failed,
                            remaining=remaining,
                            current_image="",
                            message=message,
                            error_detail=fatal_error.detail,
                            error_message=message,
                            error_image=rel_path,
                            error_source=source,
                        )
                        fatal_error_stopped = True
                        break
                    manual_tags = self._normalize_tags(item.get("manual_tags", []))
                    selected_global_tags = self._valid_global_tags(
                        item.get("selected_global_tags", [])
                    )
                    if auto_tags and not generation_failed:
                        item["auto_tags"] = auto_tags
                        item["caption_status"] = "done"
                        item["captioned_at"] = int(time.time())
                        item["caption_prompt_version"] = CAPTION_PROMPT_VERSION
                        item, rel_path = self._finalize_captioned_imagebed_item(
                            item,
                            rel_path,
                        )
                        completed += 1
                        logger.info(
                            "astrbot_plugin_smart_imagechat_hub: generated image tags %s/%s for %s: %s",
                            completed,
                            total,
                            rel_path,
                            "、".join(auto_tags),
                        )
                    else:
                        failed += 1
                        item["caption_status"] = "failed"

                    if item.get("manual_tags_override"):
                        item["tags"] = self._merge_tags(
                            manual_tags,
                            selected_global_tags,
                        )
                    else:
                        item["tags"] = self._merge_tags(
                            item.get("auto_tags", []),
                            manual_tags,
                            selected_global_tags,
                        )
                    self._save_index()
                    existing_rel_paths = self._all_existing_index_rel_paths()
                    self._sync_config_image_files(existing_rel_paths)
                    self._sync_config_tags(existing_rel_paths)
                    self._refresh_image_tag_schema(existing_rel_paths)
                    self._last_library_signature = (
                        self._library_signature_for_rel_paths(existing_rel_paths)
                    )
                    remaining = len(
                        [
                            path
                            for path in self._pending_caption_rel_paths()
                            if path not in attempted_rel_paths
                        ]
                    )
                    total = completed + failed + remaining
                    status = "running" if remaining else "done"
                    if auto_tags and not generation_failed:
                        message = f"Generated tags for {rel_path}."
                    else:
                        message = f"Failed to generate tags for {rel_path}."
                    self._set_caption_progress(
                        status=status,
                        total=total,
                        completed=completed,
                        failed=failed,
                        remaining=remaining,
                        current_image="" if status == "done" else rel_path,
                        message=message,
                        error_detail="",
                        error_image="",
                        error_message="",
                        error_source="",
                    )

        except asyncio.CancelledError:
            cancelled = True
            self._set_caption_progress(
                status="cancelled",
                remaining=len(self._pending_caption_rel_paths()),
                current_image="",
                message="Image tag generation was cancelled.",
                error_detail="",
                error_image="",
                error_message="",
                error_source="",
            )
            logger.info(
                "astrbot_plugin_smart_imagechat_hub: background image tag generation cancelled."
            )
            raise
        finally:
            cleanup_task = asyncio.create_task(
                self._cleanup_running_caption_state(set(attempted_rel_paths))
            )
            self._track_caption_cleanup_task(cleanup_task)
            remaining = 0
            cleanup_done = False
            try:
                remaining = await asyncio.shield(cleanup_task)
                cleanup_done = True
            except asyncio.CancelledError:
                raise
            except Exception as exc:
                logger.warning(
                    "astrbot_plugin_smart_imagechat_hub: failed to clean caption task state: %s",
                    exc,
                    exc_info=True,
                )
                remaining = len(
                    [
                        path
                        for path in self._pending_caption_rel_paths()
                        if path not in attempted_rel_paths
                    ]
                )
            elapsed = int(time.time()) - started_at
            if not cancelled and not fatal_error_stopped:
                final_status = (
                    "failed" if failed else ("done" if remaining == 0 else "pending")
                )
                self._set_caption_progress(
                    status=final_status,
                    total=total,
                    completed=completed,
                    failed=failed,
                    remaining=remaining,
                    current_image="",
                    message=(
                        "Image tag generation finished."
                        if remaining == 0 and not failed
                        else "Image tag generation finished with failed image(s)."
                        if remaining == 0
                        else "Image tag generation stopped with pending images."
                    ),
                    error_detail="",
                    error_image="",
                    error_message="",
                    error_source="",
                )
            logger.info(
                "astrbot_plugin_smart_imagechat_hub: background image tag generation finished, completed=%s, failed=%s, remaining=%s, elapsed=%ss.",
                completed,
                failed,
                remaining,
                elapsed,
            )

