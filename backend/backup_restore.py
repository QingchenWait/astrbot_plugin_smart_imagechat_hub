from .common import (
    AUTO_COLLECTION_CONFIG_KEY,
    AUTO_COLLECTION_DISCARDED_FILENAME,
    AUTO_COLLECTION_POOL_FILENAME,
    Any,
    BACKUP_FORMAT_VERSION,
    CAPTION_PROMPT_VERSION,
    COLLECTED_COLLECTION_FOLDER,
    COLLECTED_LIBRARY_SOURCE,
    DEFAULT_CAPTION_PROVIDER_CONFIG_KEY,
    EXTERNAL_IMPORT_FOLDER,
    EXTERNAL_IMPORT_STATE_FILENAME,
    EXTERNAL_LIBRARY_SOURCE,
    GLOBAL_TAGS_CONFIG_KEY,
    IMAGEBED_IMPORT_CONFIG_KEY,
    IMAGEBED_IMPORT_DISCARDED_FILENAME,
    IMAGEBED_IMPORT_LIBRARY_FOLDER,
    IMAGEBED_IMPORT_PENDING_FOLDER,
    IMAGEBED_IMPORT_STATE_FILENAME,
    IMAGEBED_LIBRARY_SOURCE,
    IMAGE_FILES_CONFIG_KEY,
    IMAGE_TAGS_CONFIG_KEY,
    LEGACY_IMAGE_TAGS_CONFIG_KEY,
    LIBRARY_BUILDER_CONFIG_KEY,
    MANUAL_LIBRARY_SOURCE,
    MEME_COMBAT_CONFIG_KEY,
    MODEL_FALLBACK_CONFIG_KEY,
    PAGE_LIBRARY_DEFAULT_VIEW_MODE_CONFIG_KEY,
    PENDING_COLLECTION_FOLDER,
    PLUGIN_NAME,
    PLUGIN_VERSION,
    PROACTIVE_EMOJI_CONFIG_KEY,
    PROGRESS_LINK_CONFIG_KEY,
    PROGRESS_PAGE_CONFIG_VALUE,
    Path,
    SCHEDULED_BACKUP_CONFIG_KEY,
    SCHEDULED_BACKUP_FOLDER,
    SUPPORTED_IMAGE_EXTS,
    TAG_CATEGORY_CONFIG_KEY,
    USER_SEARCH_CONFIG_KEY,
    asyncio,
    base64,
    datetime,
    hashlib,
    json,
    logger,
    re,
    request,
    shutil,
    tempfile,
    time,
    timedelta,
    unquote,
    zipfile,
)


class BackupRestoreMixin:
    def _backup_snapshot(self) -> dict[str, Any]:
        exported_at = int(time.time())
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{PLUGIN_NAME}_BackupData_{timestamp}_{PLUGIN_VERSION}.zip"
        rel_paths = sorted(self._all_existing_index_rel_paths())
        pending_rel_paths = self._collection_pool_rel_paths()
        config_snapshot = self._config_snapshot()
        index_snapshot = self._json_safe_copy(self._index)
        collection_pool_snapshot = self._json_safe_copy(self._collection_pool)
        discarded_collection_snapshot = self._json_safe_copy(
            self._discarded_collection
        )
        external_import_snapshot = self._json_safe_copy(
            self._external_import_state
        )
        imagebed_import_snapshot = self._json_safe_copy(
            self._imagebed_import_state
        )
        imagebed_discarded_snapshot = self._json_safe_copy(
            self._imagebed_discarded
        )
        manifest = {
            "plugin": PLUGIN_NAME,
            "version": PLUGIN_VERSION,
            "format_version": BACKUP_FORMAT_VERSION,
            "exported_at": exported_at,
            "image_count": len(rel_paths),
            "pending_image_count": len(pending_rel_paths),
        }
        library = {
            "global_tags": self._global_tags(),
            "image_files": rel_paths,
            "image_tags": config_snapshot.get(IMAGE_TAGS_CONFIG_KEY, []),
        }
        return {
            "filename": filename,
            "rel_paths": rel_paths,
            "pending_rel_paths": pending_rel_paths,
            "manifest": manifest,
            "config": config_snapshot,
            "image_index": index_snapshot,
            "library": library,
            "collection_pool": collection_pool_snapshot,
            "discarded_collection": discarded_collection_snapshot,
            "external_import_state": external_import_snapshot,
            "imagebed_import_state": imagebed_import_snapshot,
            "imagebed_discarded": imagebed_discarded_snapshot,
        }

    async def _create_persistent_backup(self) -> dict[str, Any]:
        async with self._lock:
            backup_snapshot = self._backup_snapshot()
        filename, temp_path = await asyncio.to_thread(
            self._write_backup_zip_file,
            backup_snapshot,
        )
        try:
            item = await asyncio.to_thread(
                self._store_scheduled_backup_file,
                filename,
                temp_path,
                self._to_int(
                    backup_snapshot.get("manifest", {}).get("exported_at"),
                    int(time.time()),
                ),
            )
        finally:
            self._unlink_temp_path(temp_path)
        self._refresh_scheduled_backup_schema()
        return item

    def _new_temp_zip_path(self, purpose: str) -> Path:
        temp_file = tempfile.NamedTemporaryFile(
            prefix=f"{PLUGIN_NAME}_{purpose}_",
            suffix=".zip",
            delete=False,
        )
        temp_path = Path(temp_file.name)
        temp_file.close()
        return temp_path

    def _write_backup_zip_file(self, snapshot: dict[str, Any]) -> tuple[str, Path]:
        filename = str(snapshot.get("filename") or "backup.zip")
        rel_paths = [
            rel_path
            for rel_path in snapshot.get("rel_paths", [])
            if isinstance(rel_path, str)
        ]
        pending_rel_paths = [
            rel_path
            for rel_path in snapshot.get("pending_rel_paths", [])
            if isinstance(rel_path, str)
        ]
        zip_path = self._new_temp_zip_path("backup")
        try:
            with zipfile.ZipFile(
                zip_path,
                "w",
                compression=zipfile.ZIP_DEFLATED,
                allowZip64=True,
            ) as zf:
                zf.writestr(
                    "manifest.json",
                    self._json_dump_bytes(snapshot.get("manifest", {})),
                )
                zf.writestr(
                    "config.json",
                    self._json_dump_bytes(snapshot.get("config", {})),
                )
                zf.writestr(
                    "image_index.json",
                    self._json_dump_bytes(snapshot.get("image_index", {})),
                )
                zf.writestr(
                    "library.json",
                    self._json_dump_bytes(snapshot.get("library", {})),
                )
                zf.writestr(
                    AUTO_COLLECTION_POOL_FILENAME,
                    self._json_dump_bytes(snapshot.get("collection_pool", {})),
                )
                zf.writestr(
                    AUTO_COLLECTION_DISCARDED_FILENAME,
                    self._json_dump_bytes(
                        snapshot.get("discarded_collection", {})
                    ),
                )
                zf.writestr(
                    EXTERNAL_IMPORT_STATE_FILENAME,
                    self._json_dump_bytes(
                        snapshot.get("external_import_state", {})
                    ),
                )
                zf.writestr(
                    IMAGEBED_IMPORT_STATE_FILENAME,
                    self._json_dump_bytes(
                        snapshot.get("imagebed_import_state", {})
                    ),
                )
                zf.writestr(
                    IMAGEBED_IMPORT_DISCARDED_FILENAME,
                    self._json_dump_bytes(snapshot.get("imagebed_discarded", {})),
                )
                written_rel_paths: set[str] = set()
                for rel_path in [*rel_paths, *pending_rel_paths]:
                    if rel_path in written_rel_paths:
                        continue
                    written_rel_paths.add(rel_path)
                    try:
                        image_path = self._abs_plugin_data_path(rel_path)
                    except ValueError:
                        continue
                    if image_path.is_file():
                        try:
                            zf.write(image_path, rel_path)
                        except OSError as exc:
                            logger.warning(
                                "astrbot_plugin_smart_imagechat_hub: failed to add image to backup %s: %s",
                                rel_path,
                                exc,
                            )
        except Exception:
            self._unlink_temp_path(zip_path)
            raise

        logger.info(
            "astrbot_plugin_smart_imagechat_hub: exported backup %s with %s indexed image(s), %s pending image(s).",
            filename,
            len(rel_paths),
            len(pending_rel_paths),
        )
        return filename, zip_path

    async def _stream_temp_file(self, path: Path):
        try:
            with open(path, "rb") as f:
                while True:
                    chunk = await asyncio.to_thread(f.read, 1024 * 1024)
                    if not chunk:
                        break
                    yield chunk
        finally:
            self._unlink_temp_path(path)

    async def _stream_file_no_delete(self, path: Path):
        with open(path, "rb") as f:
            while True:
                chunk = await asyncio.to_thread(f.read, 1024 * 1024)
                if not chunk:
                    break
                yield chunk

    def _scheduled_backup_dir(self) -> Path:
        return self.data_dir / SCHEDULED_BACKUP_FOLDER

    def _scheduled_backup_path(self, filename: str) -> Path:
        safe_name = self._safe_backup_filename(filename)
        if not safe_name:
            raise ValueError("invalid backup filename")
        return self._scheduled_backup_dir() / safe_name

    def _safe_backup_filename(self, filename: Any) -> str:
        name = Path(str(filename or "").replace("\\", "/")).name.strip()
        if not name.lower().endswith(".zip"):
            return ""
        if name != self._safe_upload_filename(name):
            return ""
        return name

    def _scheduled_backup_files(self) -> list[dict[str, Any]]:
        backup_dir = self._scheduled_backup_dir()
        if not backup_dir.is_dir():
            return []
        items = []
        for path in backup_dir.glob("*.zip"):
            if not path.is_file():
                continue
            try:
                stat = path.stat()
            except OSError:
                continue
            filename = path.name
            created_at = self._backup_created_at_from_filename(filename)
            if created_at <= 0:
                created_at = int(stat.st_mtime)
            items.append(
                {
                    "id": self._image_id(filename),
                    "filename": filename,
                    "version": self._backup_version_from_filename(filename),
                    "created_at": created_at,
                    "created_at_text": self._format_timestamp(created_at),
                    "size": stat.st_size,
                }
            )
        return sorted(
            items,
            key=lambda item: (self._to_int(item.get("created_at"), 0), item["filename"]),
            reverse=True,
        )

    def _scheduled_backup_item_by_id(self, backup_id: str) -> dict[str, Any] | None:
        normalized = str(backup_id or "").strip()
        for item in self._scheduled_backup_files():
            if normalized in {str(item.get("id") or ""), str(item.get("filename") or "")}:
                return item
        return None

    def _store_scheduled_backup_file(
        self,
        filename: str,
        source_path: Path,
        created_at: int,
    ) -> dict[str, Any]:
        backup_dir = self._scheduled_backup_dir()
        backup_dir.mkdir(parents=True, exist_ok=True)
        safe_name = self._safe_backup_filename(filename) or "backup.zip"
        target = backup_dir / safe_name
        if target.exists():
            stem = target.stem
            suffix = target.suffix
            counter = 1
            while target.exists():
                counter += 1
                target = backup_dir / f"{stem}_{counter}{suffix}"
        shutil.copyfile(source_path, target)
        item = self._scheduled_backup_item_for_path(target, created_at)
        self._enforce_scheduled_backup_limit()
        return item

    def _scheduled_backup_item_for_path(
        self,
        path: Path,
        created_at: int | None = None,
    ) -> dict[str, Any]:
        if created_at is None or created_at <= 0:
            created_at = self._backup_created_at_from_filename(path.name)
        if created_at <= 0:
            try:
                created_at = int(path.stat().st_mtime)
            except OSError:
                created_at = 0
        try:
            stat = path.stat()
            size = stat.st_size
        except OSError:
            size = 0
        return {
            "id": self._image_id(path.name),
            "filename": path.name,
            "version": self._backup_version_from_filename(path.name),
            "created_at": created_at,
            "created_at_text": self._format_timestamp(created_at),
            "size": size,
        }

    def _delete_scheduled_backup(self, backup_id: str) -> dict[str, Any] | None:
        item = self._scheduled_backup_item_by_id(backup_id)
        if not item:
            return None
        try:
            path = self._scheduled_backup_path(item["filename"])
        except ValueError:
            return None
        try:
            if path.is_file():
                path.unlink()
        except OSError as exc:
            logger.warning(
                "astrbot_plugin_smart_imagechat_hub: failed to delete scheduled backup %s: %s",
                item.get("filename"),
                exc,
            )
            return None
        return item

    def _enforce_scheduled_backup_limit(self) -> None:
        limit = max(1, self._to_int(self._scheduled_backup_config().get("backup_limit"), 3))
        backups = self._scheduled_backup_files()
        for item in backups[limit:]:
            try:
                path = self._scheduled_backup_path(item["filename"])
                if path.is_file():
                    path.unlink()
            except (OSError, ValueError) as exc:
                logger.warning(
                    "astrbot_plugin_smart_imagechat_hub: failed to prune scheduled backup %s: %s",
                    item.get("filename"),
                    exc,
                )

    def _backup_created_at_from_filename(self, filename: str) -> int:
        match = re.search(r"BackupData_(\d{8})_(\d{6})", str(filename or ""))
        if not match:
            return 0
        try:
            dt = datetime.strptime(
                f"{match.group(1)}_{match.group(2)}",
                "%Y%m%d_%H%M%S",
            )
            return int(dt.timestamp())
        except ValueError:
            return 0

    def _backup_version_from_filename(self, filename: str) -> str:
        match = re.search(
            r"_(v\d+(?:\.\d+){1,3})(?:_\d+)?\.zip$",
            str(filename or ""),
            re.IGNORECASE,
        )
        return match.group(1) if match else ""

    def _format_timestamp(self, timestamp: int) -> str:
        seconds = self._to_int(timestamp, 0)
        if seconds <= 0:
            return "-"
        return datetime.fromtimestamp(seconds).strftime("%Y-%m-%d %H:%M:%S")

    def _start_scheduled_backup_task(self) -> None:
        if self._scheduled_backup_task and not self._scheduled_backup_task.done():
            return
        self._scheduled_backup_task = asyncio.create_task(
            self._scheduled_backup_loop()
        )

    def _restart_scheduled_backup_task(self) -> None:
        if self._scheduled_backup_task and not self._scheduled_backup_task.done():
            self._scheduled_backup_task.cancel()
        try:
            asyncio.get_running_loop()
        except RuntimeError:
            return
        self._scheduled_backup_task = asyncio.create_task(
            self._scheduled_backup_loop()
        )

    async def _scheduled_backup_loop(self) -> None:
        while True:
            cfg = self._scheduled_backup_config()
            if not cfg.get("enabled"):
                await asyncio.sleep(3600)
                continue
            delay = self._seconds_until_backup_time(str(cfg.get("backup_time") or "06:00"))
            await asyncio.sleep(delay)
            try:
                await self._sync_library_if_changed(caption_mode="none")
                backup = await self._create_persistent_backup()
                logger.info(
                    "astrbot_plugin_smart_imagechat_hub: scheduled backup created: %s.",
                    backup.get("filename"),
                )
            except asyncio.CancelledError:
                raise
            except Exception as exc:
                logger.warning(
                    "astrbot_plugin_smart_imagechat_hub: scheduled backup failed: %s",
                    exc,
                    exc_info=True,
                )
                await asyncio.sleep(300)

    def _seconds_until_backup_time(self, backup_time: str) -> int:
        normalized = self._normalize_backup_time(backup_time, "06:00")
        hour, minute = [self._to_int(part, 0) for part in normalized.split(":", 1)]
        now = datetime.now()
        target = now.replace(hour=hour, minute=minute, second=0, microsecond=0)
        if target <= now:
            target = target + timedelta(days=1)
        return max(1, int((target - now).total_seconds()))

    async def _receive_backup_import_file(self) -> tuple[Path, str, str, bool]:
        content_type = str(request.content_type or "").lower()
        if "multipart/form-data" in content_type:
            form = await request.form
            files = await request.files
            file = files.get("file")
            if file is None:
                file = next(iter(files.values()), None)
            if file is None:
                raise ValueError("No backup file uploaded")
            filename, encoded_mode, encoded_overwrite = self._decode_backup_import_filename(
                str(file.filename or "backup.zip")
            )
            library_mode = str(
                form.get("library_mode") or encoded_mode or "merge"
            ).strip().lower()
            overwrite_plugin_config = self._to_bool(
                form.get("overwrite_plugin_config"),
                encoded_overwrite,
            )
            temp_path = self._new_temp_zip_path("import")
            try:
                await file.save(str(temp_path))
            except Exception as exc:
                self._unlink_temp_path(temp_path)
                raise ValueError("Failed to save backup upload") from exc
            if not temp_path.is_file() or temp_path.stat().st_size <= 0:
                self._unlink_temp_path(temp_path)
                raise ValueError("Empty backup file")
            return temp_path, filename, library_mode, overwrite_plugin_config

        payload = await request.get_json(silent=True) or {}
        if not isinstance(payload, dict):
            raise ValueError("Invalid backup payload")
        return self._write_legacy_backup_payload_to_temp_file(payload)

    def _write_legacy_backup_payload_to_temp_file(
        self,
        payload: dict[str, Any],
    ) -> tuple[Path, str, str, bool]:
        raw_content = str(payload.get("content_base64") or "")
        filename = Path(str(payload.get("filename") or "backup.zip")).name.strip()
        filename = filename or "backup.zip"
        library_mode = str(payload.get("library_mode") or "merge").strip().lower()
        overwrite_plugin_config = self._to_bool(
            payload.get("overwrite_plugin_config"),
            False,
        )

        if "," in raw_content and raw_content.split(",", 1)[0].startswith("data:"):
            raw_content = raw_content.split(",", 1)[1]
        try:
            content = base64.b64decode(raw_content, validate=True)
        except Exception as exc:
            raise ValueError("Invalid backup payload") from exc
        if not content:
            raise ValueError("Empty backup file")

        temp_path = self._new_temp_zip_path("import")
        try:
            with open(temp_path, "wb") as f:
                f.write(content)
        except OSError as exc:
            self._unlink_temp_path(temp_path)
            raise ValueError("Failed to save backup payload") from exc
        return temp_path, filename, library_mode, overwrite_plugin_config

    def _decode_backup_import_filename(self, filename: str) -> tuple[str, str, bool]:
        raw_name = Path(str(filename or "backup.zip").replace("\\", "/")).name.strip()
        raw_name = raw_name or "backup.zip"
        library_mode = "merge"
        overwrite_plugin_config = False
        prefix = "__asmimgimport__"
        if raw_name.startswith(prefix):
            payload = raw_name[len(prefix) :]
            if payload.startswith("::"):
                payload = payload[2:]
            parts = payload.split("::", 2)
            if len(parts) == 3:
                maybe_mode, maybe_overwrite, encoded_name = parts
                if maybe_mode in {"merge", "overwrite"}:
                    library_mode = maybe_mode
                overwrite_plugin_config = maybe_overwrite.strip().lower() in {
                    "1",
                    "true",
                    "yes",
                    "on",
                }
                decoded_name = unquote(encoded_name).strip()
                if decoded_name:
                    raw_name = decoded_name
        return raw_name, library_mode, overwrite_plugin_config

    def _unlink_temp_path(self, path: Path) -> None:
        try:
            path.unlink(missing_ok=True)
        except OSError:
            pass

    def _read_backup_zip(self, zip_path: Path | str) -> dict[str, Any]:
        try:
            with zipfile.ZipFile(Path(zip_path), "r") as zf:
                members = {}
                for info in zf.infolist():
                    if info.is_dir():
                        continue
                    rel_name = self._safe_zip_member_name(info.filename)
                    if not rel_name:
                        raise ValueError(f"Invalid backup file path: {info.filename}")
                    members[rel_name] = info

                if "manifest.json" not in members:
                    raise ValueError("Invalid backup: manifest.json is missing")

                manifest = self._read_json_zip_member(zf, "manifest.json")
                if manifest.get("plugin") != PLUGIN_NAME:
                    raise ValueError("Invalid backup: plugin name does not match")
                if self._to_int(manifest.get("format_version"), 0) != BACKUP_FORMAT_VERSION:
                    raise ValueError("Invalid backup: unsupported backup format version")

                config = (
                    self._read_json_zip_member(zf, "config.json")
                    if "config.json" in members
                    else {}
                )
                image_index = (
                    self._read_json_zip_member(zf, "image_index.json")
                    if "image_index.json" in members
                    else {"version": 1, "images": {}}
                )
                collection_pool = (
                    self._read_json_zip_member(zf, AUTO_COLLECTION_POOL_FILENAME)
                    if AUTO_COLLECTION_POOL_FILENAME in members
                    else {"version": 1, "images": {}}
                )
                discarded_collection = (
                    self._read_json_zip_member(
                        zf,
                        AUTO_COLLECTION_DISCARDED_FILENAME,
                    )
                    if AUTO_COLLECTION_DISCARDED_FILENAME in members
                    else {"version": 1, "digests": {}}
                )
                external_import_state = (
                    self._read_json_zip_member(zf, EXTERNAL_IMPORT_STATE_FILENAME)
                    if EXTERNAL_IMPORT_STATE_FILENAME in members
                    else self._empty_external_import_state()
                )
                imagebed_import_state = (
                    self._read_json_zip_member(zf, IMAGEBED_IMPORT_STATE_FILENAME)
                    if IMAGEBED_IMPORT_STATE_FILENAME in members
                    else self._empty_imagebed_import_state()
                )
                imagebed_discarded = (
                    self._read_json_zip_member(zf, IMAGEBED_IMPORT_DISCARDED_FILENAME)
                    if IMAGEBED_IMPORT_DISCARDED_FILENAME in members
                    else self._empty_imagebed_discarded()
                )
                if not isinstance(config, dict):
                    raise ValueError("Invalid backup: config.json must be an object")
                if not isinstance(image_index, dict):
                    raise ValueError("Invalid backup: image_index.json must be an object")
                if not isinstance(image_index.get("images"), dict):
                    image_index["images"] = {}
                if not isinstance(collection_pool, dict):
                    collection_pool = {"version": 1, "images": {}}
                if not isinstance(collection_pool.get("images"), dict):
                    collection_pool["images"] = {}
                if not isinstance(discarded_collection, dict):
                    discarded_collection = {"version": 1, "digests": {}}
                if not isinstance(discarded_collection.get("digests"), dict):
                    discarded_collection["digests"] = {}
                if not isinstance(external_import_state, dict):
                    external_import_state = self._empty_external_import_state()
                external_import_state.setdefault("version", 1)
                external_import_state.setdefault("imports", {})
                external_import_state.setdefault("manually_deleted_digests", {})
                external_import_state.setdefault("active_import", {})
                external_import_state.setdefault("last_stat", {})
                external_import_state.setdefault("caption_paused", True)
                external_import_state.setdefault("warning_preferences", {})
                if not isinstance(imagebed_import_state, dict):
                    imagebed_import_state = self._empty_imagebed_import_state()
                imagebed_import_state.setdefault("version", 1)
                imagebed_import_state.setdefault("active_import", {})
                imagebed_import_state.setdefault("known_remote_objects", {})
                imagebed_import_state.setdefault("last_connection", {})
                imagebed_import_state.setdefault("last_stat", {})
                imagebed_import_state.setdefault("last_successful_sync_at", 0)
                imagebed_import_state.setdefault("caption_paused", True)
                imagebed_import_state.setdefault("last_error", {})
                if not isinstance(imagebed_discarded, dict):
                    imagebed_discarded = self._empty_imagebed_discarded()
                imagebed_discarded.setdefault("version", 1)
                imagebed_discarded.setdefault("digests", {})
                imagebed_discarded.setdefault("objects", {})

                pending_prefix = f"files/{PENDING_COLLECTION_FOLDER}/"
                file_entries = sorted(
                    rel_name
                    for rel_name in members
                    if rel_name.startswith("files/")
                    and not rel_name.startswith(pending_prefix)
                    and Path(rel_name).suffix.lower() in SUPPORTED_IMAGE_EXTS
                )
                pending_file_entries = sorted(
                    rel_name
                    for rel_name in members
                    if rel_name.startswith(pending_prefix)
                    and Path(rel_name).suffix.lower() in SUPPORTED_IMAGE_EXTS
                )

        except zipfile.BadZipFile as exc:
            raise ValueError("Invalid backup: zip file cannot be read") from exc
        except json.JSONDecodeError as exc:
            raise ValueError("Invalid backup: json file cannot be parsed") from exc

        return {
            "manifest": manifest,
            "config": config,
            "image_index": image_index,
                "collection_pool": collection_pool,
                "discarded_collection": discarded_collection,
                "external_import_state": external_import_state,
                "imagebed_import_state": imagebed_import_state,
                "imagebed_discarded": imagebed_discarded,
                "file_entries": file_entries,
                "pending_file_entries": pending_file_entries,
                "zip_path": str(zip_path),
            }

    def _restore_backup(
        self,
        backup: dict[str, Any],
        library_mode: str,
        overwrite_plugin_config: bool,
    ) -> dict[str, Any]:
        config = backup.get("config") if isinstance(backup.get("config"), dict) else {}
        if overwrite_plugin_config:
            applied_config_keys = self._apply_imported_config(config)
            self._restart_scheduled_backup_task()
        else:
            applied_config_keys = []

        if library_mode == "overwrite":
            deleted = self._clear_image_library()
            self._index = {"version": 1, "images": {}}
            self._config_set(
                GLOBAL_TAGS_CONFIG_KEY,
                self._normalize_tags(
                    self._nested_config_get(config, GLOBAL_TAGS_CONFIG_KEY, [])
                ),
            )
        else:
            deleted = 0
            current_global_tags = self._global_tags()
            self._config_set(
                GLOBAL_TAGS_CONFIG_KEY,
                self._merge_tags(
                    current_global_tags,
                    self._nested_config_get(config, GLOBAL_TAGS_CONFIG_KEY, []),
                ),
            )

        imported, skipped = self._restore_backup_images(backup, library_mode)
        pending_imported, pending_skipped = self._restore_backup_collection_pool(
            backup,
            library_mode,
        )
        self._restore_backup_external_import_state(backup, library_mode)
        self._restore_backup_imagebed_import_state(backup, library_mode)
        self._save_index()
        self._save_collection_pool()
        self._save_discarded_collection()
        self._save_external_import_state()
        self._save_imagebed_import_state()
        self._save_imagebed_discarded()

        existing_rel_paths = self._all_existing_index_rel_paths()
        self._sync_config_image_files(existing_rel_paths)
        self._sync_config_tags(existing_rel_paths)
        self._refresh_image_tag_schema(existing_rel_paths)
        self._refresh_caption_tag_category_schema()
        self._last_library_signature = self._library_signature_for_rel_paths(
            existing_rel_paths
        )
        self._migrate_reply_config()
        self._config_set(PROGRESS_LINK_CONFIG_KEY, PROGRESS_PAGE_CONFIG_VALUE)
        self._save_plugin_config()
        if IMAGEBED_IMPORT_CONFIG_KEY in applied_config_keys:
            self._restart_imagebed_sync_task()

        pending_count = len(self._pending_caption_rel_paths())
        self._set_caption_progress(
            status="pending" if pending_count else "done",
            total=pending_count,
            completed=0,
            failed=0,
            remaining=pending_count,
            current_image="",
            message=(
                f"Backup imported. {pending_count} image(s) are waiting for tag generation."
                if pending_count
                else "Backup imported. No images are waiting for tag generation."
            ),
            error_detail="",
            error_image="",
            error_message="",
            error_source="",
        )

        result = {
            "library_mode": library_mode,
            "overwrite_plugin_config": overwrite_plugin_config,
            "imported_images": imported,
            "skipped_images": skipped,
            "imported_pending_images": pending_imported,
            "skipped_pending_images": pending_skipped,
            "deleted_images": deleted,
            "global_tags": len(self._global_tags()),
            "applied_config_keys": applied_config_keys,
        }
        logger.info(
            "astrbot_plugin_smart_imagechat_hub: imported backup mode=%s overwrite_config=%s config_keys=%s imported=%s skipped=%s pending_imported=%s pending_skipped=%s deleted=%s.",
            library_mode,
            overwrite_plugin_config,
            len(applied_config_keys),
            imported,
            skipped,
            pending_imported,
            pending_skipped,
            deleted,
        )
        return result

    def _restore_backup_images(
        self,
        backup: dict[str, Any],
        library_mode: str,
    ) -> tuple[int, int]:
        zip_path = Path(str(backup.get("zip_path") or ""))
        file_entries = [
            rel_path
            for rel_path in backup.get("file_entries", [])
            if isinstance(rel_path, str)
        ]
        image_index = (
            backup.get("image_index")
            if isinstance(backup.get("image_index"), dict)
            else {}
        )
        backup_items_by_rel, backup_items_by_digest = self._backup_image_item_maps(
            image_index
        )
        config = backup.get("config") if isinstance(backup.get("config"), dict) else {}
        configured_items = self._configured_tag_items_from_config(config)
        backup_items_by_rel.update(
            {
                rel_path: item
                for rel_path, item in configured_items.items()
                if rel_path not in backup_items_by_rel
            }
        )

        images = self._index.setdefault("images", {})
        if not isinstance(images, dict):
            images = {}
            self._index["images"] = images

        imported = 0
        skipped = 0
        current_digests = self._current_image_digests()
        folder = self._config_file_folder(IMAGE_FILES_CONFIG_KEY)

        try:
            with zipfile.ZipFile(zip_path, "r") as zf:
                for zip_rel_path in file_entries:
                    rel_path = self._norm_rel_path(zip_rel_path)
                    if (
                        not rel_path
                        or Path(rel_path).suffix.lower() not in SUPPORTED_IMAGE_EXTS
                    ):
                        skipped += 1
                        continue

                    temp_image_path: Path | None = self._copy_zip_image_entry_to_temp(
                        zf,
                        rel_path,
                    )
                    try:
                        digest = self._sha256(temp_image_path)
                        if library_mode == "merge" and digest in current_digests:
                            skipped += 1
                            continue

                        save_rel_path = rel_path
                        if library_mode == "merge":
                            try:
                                target_path = self._abs_plugin_data_path(save_rel_path)
                            except ValueError:
                                target_path = None
                            if target_path is None or target_path.exists():
                                filename = (
                                    self._safe_upload_filename(Path(rel_path).name)
                                    or "image"
                                )
                                save_rel_path = self._unique_upload_rel_path(
                                    folder,
                                    filename,
                                )

                        try:
                            save_path = self._abs_plugin_data_path(save_rel_path)
                        except ValueError:
                            skipped += 1
                            continue

                        save_path.parent.mkdir(parents=True, exist_ok=True)
                        shutil.move(str(temp_image_path), save_path)
                        temp_image_path = None
                        if not self._is_allowed_image(save_path):
                            try:
                                save_path.unlink()
                            except OSError:
                                pass
                            skipped += 1
                            continue

                        backup_item = backup_items_by_rel.get(
                            rel_path
                        ) or backup_items_by_digest.get(
                            digest,
                            {},
                        )
                        item = self._imported_index_item(
                            save_rel_path,
                            save_path,
                            backup_item,
                            digest,
                        )
                        images[item["id"]] = item
                        current_digests.add(digest)
                        imported += 1
                    finally:
                        if temp_image_path:
                            self._unlink_temp_path(temp_image_path)
        except (OSError, zipfile.BadZipFile) as exc:
            logger.warning(
                "astrbot_plugin_smart_imagechat_hub: failed to restore backup images: %s",
                exc,
                exc_info=True,
            )

        return imported, skipped

    def _restore_backup_collection_pool(
        self,
        backup: dict[str, Any],
        library_mode: str,
    ) -> tuple[int, int]:
        zip_path = Path(str(backup.get("zip_path") or ""))
        pending_entries = {
            rel_path
            for rel_path in backup.get("pending_file_entries", [])
            if isinstance(rel_path, str)
        }
        pool = (
            backup.get("collection_pool")
            if isinstance(backup.get("collection_pool"), dict)
            else {}
        )
        pool_images = pool.get("images", {}) if isinstance(pool, dict) else {}
        if not isinstance(pool_images, dict):
            pool_images = {}

        if library_mode == "overwrite":
            self._clear_collection_pool_files()
            self._collection_pool = {"version": 1, "images": {}}

        imported = 0
        skipped = 0
        images = self._collection_pool.setdefault("images", {})
        if not isinstance(images, dict):
            images = {}
            self._collection_pool["images"] = images

        current_digests = self._stored_image_digests_from_metadata(
            include_pending_pool=True
        )
        current_ids = set(images.keys())

        try:
            with zipfile.ZipFile(zip_path, "r") as zf:
                for raw_item in pool_images.values():
                    if not isinstance(raw_item, dict):
                        skipped += 1
                        continue
                    rel_path = self._norm_rel_path(raw_item.get("rel_path"))
                    if (
                        not rel_path
                        or rel_path not in pending_entries
                        or not rel_path.startswith(
                            f"files/{PENDING_COLLECTION_FOLDER}/"
                        )
                        or Path(rel_path).suffix.lower() not in SUPPORTED_IMAGE_EXTS
                    ):
                        skipped += 1
                        continue

                    digest = str(raw_item.get("sha256") or "").strip()
                    if library_mode == "merge" and digest and digest in current_digests:
                        skipped += 1
                        continue

                    item_id = str(raw_item.get("id") or "").strip()
                    if not item_id:
                        item_id = self._image_id(rel_path)

                    save_rel_path = rel_path
                    if library_mode == "merge":
                        try:
                            target_path = self._abs_plugin_data_path(save_rel_path)
                        except ValueError:
                            target_path = None
                        if (
                            not target_path
                            or target_path.exists()
                            or item_id in current_ids
                        ):
                            suffix = Path(rel_path).suffix.lower() or ".jpg"
                            save_rel_path = self._unique_collected_pending_rel_path(
                                raw_item.get("group_id") or "group",
                                self._to_int(raw_item.get("collected_at"), int(time.time())),
                                suffix,
                            )
                            item_id = self._image_id(save_rel_path)

                    temp_image_path: Path | None = self._copy_zip_image_entry_to_temp(
                        zf,
                        rel_path,
                    )
                    try:
                        if not digest:
                            digest = self._sha256(temp_image_path)
                        if library_mode == "merge" and digest in current_digests:
                            skipped += 1
                            continue

                        try:
                            save_path = self._abs_plugin_data_path(save_rel_path)
                        except ValueError:
                            skipped += 1
                            continue

                        save_path.parent.mkdir(parents=True, exist_ok=True)
                        if save_path.exists():
                            try:
                                save_path.unlink()
                            except OSError:
                                skipped += 1
                                continue
                        shutil.move(str(temp_image_path), save_path)
                        temp_image_path = None
                        if not self._is_allowed_image(save_path):
                            try:
                                save_path.unlink()
                            except OSError:
                                pass
                            skipped += 1
                            continue

                        stat = save_path.stat()
                        item = self._imported_collection_pool_item(
                            raw_item,
                            item_id,
                            save_rel_path,
                            save_path,
                            digest,
                            stat,
                        )
                        images[item_id] = item
                        current_ids.add(item_id)
                        current_digests.add(digest)
                        imported += 1
                    finally:
                        if temp_image_path:
                            self._unlink_temp_path(temp_image_path)
        except (OSError, zipfile.BadZipFile) as exc:
            logger.warning(
                "astrbot_plugin_smart_imagechat_hub: failed to restore backup pending collection pool: %s",
                exc,
                exc_info=True,
            )

        self._restore_discarded_collection_history(
            backup.get("discarded_collection"),
            library_mode,
        )
        return imported, skipped

    def _restore_backup_external_import_state(
        self,
        backup: dict[str, Any],
        library_mode: str,
    ) -> None:
        imported_state = backup.get("external_import_state")
        if not isinstance(imported_state, dict):
            return
        if library_mode == "overwrite":
            self._external_import_state = self._empty_external_import_state()

        state = self._external_import_state
        state.setdefault("version", 1)
        state.setdefault("imports", {})
        state.setdefault("manually_deleted_digests", {})

        imported_deleted = imported_state.get("manually_deleted_digests", {})
        if isinstance(imported_deleted, dict):
            deleted = state.setdefault("manually_deleted_digests", {})
            if not isinstance(deleted, dict):
                deleted = {}
                state["manually_deleted_digests"] = deleted
            for digest, value in imported_deleted.items():
                normalized = str(digest or "").strip()
                if normalized:
                    deleted[normalized] = self._json_safe_copy(value)

        imported_imports = imported_state.get("imports", {})
        if isinstance(imported_imports, dict):
            imports = state.setdefault("imports", {})
            if not isinstance(imports, dict):
                imports = {}
                state["imports"] = imports
            for key, value in imported_imports.items():
                if isinstance(value, dict):
                    imports[str(key)] = self._json_safe_copy(value)

        last_stat = imported_state.get("last_stat", {})
        state["last_stat"] = (
            self._json_safe_copy(last_stat) if isinstance(last_stat, dict) else {}
        )
        state["caption_paused"] = self._to_bool(
            imported_state.get("caption_paused"),
            bool(state.get("caption_paused", True)),
        )
        warning_preferences = imported_state.get("warning_preferences")
        warning_preferences_version = self._to_int(
            imported_state.get("warning_preferences_version"),
            0,
        )
        if (
            warning_preferences_version == 2
            and isinstance(warning_preferences, dict)
        ):
            state["warning_preferences"] = self._json_safe_copy(
                warning_preferences
            )
        else:
            state["warning_preferences"] = {}
        state["warning_preferences_version"] = 2
        state["active_import"] = {}

    def _restore_backup_imagebed_import_state(
        self,
        backup: dict[str, Any],
        library_mode: str,
    ) -> None:
        imported_state = backup.get("imagebed_import_state")
        if not isinstance(imported_state, dict):
            return
        if library_mode == "overwrite":
            self._imagebed_import_state = self._empty_imagebed_import_state()
            self._imagebed_discarded = self._empty_imagebed_discarded()

        state = self._imagebed_import_state
        state.setdefault("version", 1)
        state.setdefault("config", {})
        state.setdefault("known_remote_objects", {})
        state.setdefault("last_connection", {})
        state.setdefault("last_stat", {})
        state.setdefault("last_successful_sync_at", 0)
        state.setdefault("caption_paused", True)
        state.setdefault("last_error", {})

        imported_config = imported_state.get("config", {})
        if isinstance(imported_config, dict):
            state["config"] = self._json_safe_copy(imported_config)

        imported_known = imported_state.get("known_remote_objects", {})
        if isinstance(imported_known, dict):
            known = state.setdefault("known_remote_objects", {})
            if not isinstance(known, dict):
                known = {}
                state["known_remote_objects"] = known
            for marker, value in imported_known.items():
                normalized = str(marker or "").strip()
                if normalized:
                    known[normalized] = self._json_safe_copy(value)

        state["last_connection"] = self._json_safe_copy(
            imported_state.get("last_connection", {})
        )
        state["last_stat"] = self._json_safe_copy(imported_state.get("last_stat", {}))
        state["last_successful_sync_at"] = self._to_int(
            imported_state.get("last_successful_sync_at"),
            0,
        )
        state["caption_paused"] = self._to_bool(
            imported_state.get("caption_paused"),
            bool(state.get("caption_paused", True)),
        )
        last_error = imported_state.get("last_error", {})
        state["last_error"] = (
            self._json_safe_copy(last_error) if isinstance(last_error, dict) else {}
        )
        state["active_import"] = {}

        imported_discarded = backup.get("imagebed_discarded")
        if isinstance(imported_discarded, dict):
            if library_mode == "overwrite":
                self._imagebed_discarded = self._empty_imagebed_discarded()
            digests = imported_discarded.get("digests", {})
            if isinstance(digests, dict):
                current_digests = self._imagebed_discarded.setdefault("digests", {})
                if not isinstance(current_digests, dict):
                    current_digests = {}
                    self._imagebed_discarded["digests"] = current_digests
                for digest, value in digests.items():
                    normalized = str(digest or "").strip()
                    if normalized:
                        current_digests[normalized] = self._json_safe_copy(value)
            objects = imported_discarded.get("objects", {})
            if isinstance(objects, dict):
                current_objects = self._imagebed_discarded.setdefault("objects", {})
                if not isinstance(current_objects, dict):
                    current_objects = {}
                    self._imagebed_discarded["objects"] = current_objects
                for marker, value in objects.items():
                    normalized = str(marker or "").strip()
                    if normalized:
                        current_objects[normalized] = self._json_safe_copy(value)

    def _imported_collection_pool_item(
        self,
        raw_item: dict[str, Any],
        item_id: str,
        rel_path: str,
        image_path: Path,
        digest: str,
        stat: Any,
    ) -> dict[str, Any]:
        now = int(time.time())
        collected_at = self._to_int(raw_item.get("collected_at"), 0) or now
        return {
            "id": item_id,
            "rel_path": rel_path,
            "filename": image_path.name,
            "sha256": digest,
            "size": stat.st_size,
            "mtime": int(stat.st_mtime),
            "group_id": str(raw_item.get("group_id") or ""),
            "sender_id": str(raw_item.get("sender_id") or ""),
            "collected_at": collected_at,
        }

    def _clear_collection_pool_files(self) -> None:
        for item in list(self._collection_pool_items()):
            image_id = str(item.get("id") or "")
            if image_id:
                self._remove_collection_pool_item(image_id, delete_file=True)

    def _restore_discarded_collection_history(
        self,
        imported_history: Any,
        library_mode: str,
    ) -> None:
        if not isinstance(imported_history, dict):
            return
        imported_digests = imported_history.get("digests", {})
        if not isinstance(imported_digests, dict):
            return

        if library_mode == "overwrite":
            self._discarded_collection = {"version": 1, "digests": {}}

        digests = self._discarded_collection.setdefault("digests", {})
        if not isinstance(digests, dict):
            digests = {}
            self._discarded_collection["digests"] = digests

        now = int(time.time())
        for digest, value in imported_digests.items():
            normalized = str(digest or "").strip()
            if not normalized:
                continue
            discarded_at = 0
            if isinstance(value, dict):
                discarded_at = self._to_int(value.get("discarded_at"), 0)
            else:
                discarded_at = self._to_int(value, 0)
            digests[normalized] = {"discarded_at": discarded_at or now}

    def _copy_zip_image_entry_to_temp(
        self,
        zf: zipfile.ZipFile,
        rel_path: str,
    ) -> Path:
        suffix = Path(rel_path).suffix.lower() or ".img"
        temp_file = tempfile.NamedTemporaryFile(
            prefix=f"{PLUGIN_NAME}_restore_image_",
            suffix=suffix,
            delete=False,
        )
        temp_path = Path(temp_file.name)
        try:
            with temp_file:
                with zf.open(rel_path, "r") as source:
                    shutil.copyfileobj(source, temp_file, length=1024 * 1024)
        except Exception:
            self._unlink_temp_path(temp_path)
            raise
        return temp_path

    def _imported_index_item(
        self,
        rel_path: str,
        image_path: Path,
        backup_item: dict[str, Any],
        digest: str,
    ) -> dict[str, Any]:
        stat = image_path.stat()
        now = int(time.time())
        backup_tags = self._normalize_tags(backup_item.get("tags", []))
        auto_tags = self._normalize_tags(backup_item.get("auto_tags", []))
        manual_tags = self._normalize_tags(backup_item.get("manual_tags", []))
        manual_override = bool(backup_item.get("manual_tags_override", False))

        if not auto_tags and not manual_override:
            auto_tags = backup_tags
        if manual_override and not manual_tags:
            manual_tags = backup_tags

        selected_global_tags = self._valid_global_tags(
            backup_item.get("selected_global_tags", [])
        )
        if manual_override:
            merged_tags = self._merge_tags(manual_tags, selected_global_tags)
        else:
            merged_tags = self._merge_tags(auto_tags, manual_tags, selected_global_tags)

        caption_status = str(backup_item.get("caption_status") or "").strip()
        if caption_status == "running":
            caption_status = "pending"
        if caption_status in {"pending", "failed"}:
            pass
        elif merged_tags:
            caption_status = "done"
        elif caption_status not in {"done", "pending", "failed"}:
            caption_status = "pending"

        return {
            "id": self._image_id(rel_path),
            "rel_path": rel_path,
            "filename": image_path.name,
            "sha256": digest,
            "size": stat.st_size,
            "mtime": int(stat.st_mtime),
            "library_source": self._library_source_for_rel_path(rel_path, backup_item),
            "auto_tags": auto_tags,
            "manual_tags": manual_tags,
            "manual_tags_override": manual_override,
            "selected_global_tags": selected_global_tags,
            "tags": merged_tags,
            "import_extra_tags": self._normalize_tags(
                backup_item.get("import_extra_tags", [])
            ),
            "caption_status": caption_status,
            "captioned_at": self._to_int(
                backup_item.get("captioned_at"),
                now if caption_status == "done" else 0,
            ),
            "caption_prompt_version": (
                CAPTION_PROMPT_VERSION if caption_status == "done" else 0
            ),
            "updated_at": self._to_int(backup_item.get("updated_at"), now),
            "collected_from_group_id": str(
                backup_item.get("collected_from_group_id") or ""
            ),
            "collected_sender_id": str(backup_item.get("collected_sender_id") or ""),
            "collected_at": self._to_int(backup_item.get("collected_at"), 0),
            "solidified_at": self._to_int(backup_item.get("solidified_at"), 0),
            "external_source_dir": str(backup_item.get("external_source_dir") or ""),
            "external_source_path": str(backup_item.get("external_source_path") or ""),
            "external_imported_at": self._to_int(
                backup_item.get("external_imported_at"),
                0,
            ),
            "imagebed_object_key": str(backup_item.get("imagebed_object_key") or ""),
            "imagebed_object_etag": str(backup_item.get("imagebed_object_etag") or ""),
            "imagebed_object_size": self._to_int(
                backup_item.get("imagebed_object_size"),
                0,
            ),
            "imagebed_object_last_modified": str(
                backup_item.get("imagebed_object_last_modified") or ""
            ),
            "imagebed_object_marker": str(
                backup_item.get("imagebed_object_marker") or ""
            ),
            "imagebed_imported_at": self._to_int(
                backup_item.get("imagebed_imported_at"),
                0,
            ),
            "imagebed_finalized_at": self._to_int(
                backup_item.get("imagebed_finalized_at"),
                0,
            ),
        }

    def _apply_imported_config(self, config: dict[str, Any]) -> list[str]:
        excluded = {
            GLOBAL_TAGS_CONFIG_KEY,
            IMAGE_FILES_CONFIG_KEY,
            PROGRESS_LINK_CONFIG_KEY,
            IMAGE_TAGS_CONFIG_KEY,
            LEGACY_IMAGE_TAGS_CONFIG_KEY,
        }
        applied_keys: list[str] = []
        for key, value in config.items():
            if key in excluded:
                continue
            if key == LIBRARY_BUILDER_CONFIG_KEY and isinstance(value, dict):
                current_group = self._config_get(LIBRARY_BUILDER_CONFIG_KEY, {})
                if not isinstance(current_group, dict):
                    current_group = {}
                next_group = dict(current_group)
                for group_key, group_value in value.items():
                    nested_key = f"{LIBRARY_BUILDER_CONFIG_KEY}.{group_key}"
                    if nested_key in excluded:
                        continue
                    next_group[group_key] = self._json_safe_copy(group_value)
                    applied_keys.append(nested_key)
                self.config[LIBRARY_BUILDER_CONFIG_KEY] = next_group
                continue
            if key == TAG_CATEGORY_CONFIG_KEY:
                self.config[key] = self._json_safe_copy(value)
                applied_keys.append(key)
                if isinstance(value, dict) and DEFAULT_CAPTION_PROVIDER_CONFIG_KEY in value:
                    self.config[DEFAULT_CAPTION_PROVIDER_CONFIG_KEY] = str(
                        value.get(DEFAULT_CAPTION_PROVIDER_CONFIG_KEY) or ""
                    ).strip()
                    applied_keys.append(DEFAULT_CAPTION_PROVIDER_CONFIG_KEY)
                continue
            if key == DEFAULT_CAPTION_PROVIDER_CONFIG_KEY:
                self._set_plugin_default_image_caption_provider_id(value)
                applied_keys.append(key)
                continue
            if key == IMAGEBED_IMPORT_CONFIG_KEY:
                self._set_imagebed_import_config(
                    value,
                    save_plugin_config=False,
                    save_state=False,
                )
                applied_keys.append(key)
                continue
            if key == PROACTIVE_EMOJI_CONFIG_KEY:
                self.config[key] = self._normalize_proactive_emoji_config(value)
                applied_keys.append(key)
                continue
            if key == AUTO_COLLECTION_CONFIG_KEY:
                self.config[key] = self._normalize_auto_collection_config(value)
                applied_keys.append(key)
                continue
            if key == MEME_COMBAT_CONFIG_KEY:
                self.config[key] = self._normalize_meme_combat_config(value)
                applied_keys.append(key)
                continue
            if key == SCHEDULED_BACKUP_CONFIG_KEY:
                self.config[key] = self._normalize_scheduled_backup_config(value)
                applied_keys.append(key)
                continue
            if key == MODEL_FALLBACK_CONFIG_KEY:
                self.config[key] = self._normalize_model_fallback_config(value)
                applied_keys.append(key)
                continue
            if key == PAGE_LIBRARY_DEFAULT_VIEW_MODE_CONFIG_KEY:
                self.config[key] = self._normalize_page_library_default_view_mode(value)
                applied_keys.append(key)
                continue
            if key == USER_SEARCH_CONFIG_KEY:
                if isinstance(value, dict):
                    self._set_user_search_config(
                        enabled=value.get("enabled"),
                        keywords=value.get("request_keywords", []),
                    )
                    applied_keys.append(key)
                continue
            self.config[key] = self._json_safe_copy(value)
            applied_keys.append(key)
        return applied_keys

    def _configured_tag_items_from_config(
        self,
        config: dict[str, Any],
    ) -> dict[str, dict[str, Any]]:
        raw_items = config.get(IMAGE_TAGS_CONFIG_KEY, [])
        if not isinstance(raw_items, list):
            raw_items = config.get(LEGACY_IMAGE_TAGS_CONFIG_KEY, [])
        if not isinstance(raw_items, list):
            return {}

        by_rel: dict[str, dict[str, Any]] = {}
        for raw_item in raw_items:
            if not isinstance(raw_item, dict):
                continue
            rel_path = self._norm_rel_path(raw_item.get("image_path"))
            if not rel_path:
                rel_path = self._norm_rel_path(raw_item.get("rel_path"))
            if not rel_path:
                continue
            tags = self._normalize_tags(raw_item.get("tags", []))
            auto_tags = self._normalize_tags(raw_item.get("auto_tags", []))
            selected_global_tags = self._valid_global_tags_from_config(
                raw_item.get("selected_global_tags", []),
                config,
            )
            by_rel[rel_path] = {
                "tags": tags,
                "auto_tags": auto_tags,
                "manual_tags": self._normalize_tags(
                    raw_item.get("manual_tags", tags)
                ),
                "manual_tags_override": self._to_bool(
                    raw_item.get("manual_tags_override"),
                    bool(tags and tags != auto_tags),
                ),
                "selected_global_tags": selected_global_tags,
                "caption_status": "done" if (tags or auto_tags) else "pending",
            }
        return by_rel

    def _valid_global_tags_from_config(
        self,
        raw_tags: Any,
        config: dict[str, Any],
    ) -> list[str]:
        allowed = set(
            self._normalize_tags(
                self._nested_config_get(config, GLOBAL_TAGS_CONFIG_KEY, [])
            )
        )
        return [tag for tag in self._normalize_tags(raw_tags) if tag in allowed]

    def _clear_image_library(self) -> int:
        rel_paths = (
            self._configured_image_rel_paths()
            | self._discover_uploaded_images()
            | self._all_existing_index_rel_paths()
            | set(self._configured_tag_items().keys())
        )
        deleted = 0
        for rel_path in sorted(rel_paths):
            try:
                image_path = self._abs_plugin_data_path(rel_path)
            except ValueError:
                continue
            if not image_path.is_file():
                continue
            try:
                image_path.unlink()
                deleted += 1
            except OSError as exc:
                logger.warning(
                    "astrbot_plugin_smart_imagechat_hub: failed to delete image during backup restore %s: %s",
                    rel_path,
                    exc,
                )
        self._config_set(IMAGE_FILES_CONFIG_KEY, [])
        self.config[IMAGE_TAGS_CONFIG_KEY] = []
        if LEGACY_IMAGE_TAGS_CONFIG_KEY in self.config:
            self.config[LEGACY_IMAGE_TAGS_CONFIG_KEY] = []
        return deleted

    def _backup_image_item_maps(
        self,
        image_index: dict[str, Any],
    ) -> tuple[dict[str, dict[str, Any]], dict[str, dict[str, Any]]]:
        by_rel: dict[str, dict[str, Any]] = {}
        by_digest: dict[str, dict[str, Any]] = {}
        images = image_index.get("images", {})
        if not isinstance(images, dict):
            return by_rel, by_digest
        for item in images.values():
            if not isinstance(item, dict):
                continue
            rel_path = self._norm_rel_path(item.get("rel_path"))
            if rel_path:
                by_rel[rel_path] = item
            digest = str(item.get("sha256") or "").strip()
            if digest:
                by_digest[digest] = item
        return by_rel, by_digest

    def _current_image_digests(self) -> set[str]:
        digests: set[str] = set()
        images = self._index.get("images", {})
        if not isinstance(images, dict):
            return digests
        for item in images.values():
            if not isinstance(item, dict):
                continue
            digest = str(item.get("sha256") or "").strip()
            if digest:
                digests.add(digest)
        return digests

    def _stored_image_digests(self, include_pending_pool: bool = True) -> set[str]:
        digests = set(self._current_image_digests())
        folders = [self._config_file_folder(IMAGE_FILES_CONFIG_KEY)]
        if include_pending_pool:
            folders.append(PENDING_COLLECTION_FOLDER)
        folders.append(COLLECTED_COLLECTION_FOLDER)
        folders.append(EXTERNAL_IMPORT_FOLDER)
        folders.append(IMAGEBED_IMPORT_PENDING_FOLDER)
        folders.append(IMAGEBED_IMPORT_LIBRARY_FOLDER)
        for folder in folders:
            root = self.data_dir / "files" / folder
            if not root.is_dir():
                continue
            for path in root.rglob("*"):
                if not self._is_allowed_image(path):
                    continue
                try:
                    digest = self._cached_sha256(path)
                except OSError:
                    continue
                if digest:
                    digests.add(digest)
        return digests

    def _stored_image_digests_from_metadata(
        self,
        include_pending_pool: bool = True,
    ) -> set[str]:
        digests = set(self._current_image_digests())
        if include_pending_pool:
            for item in self._collection_pool_items():
                digest = str(item.get("sha256") or "").strip()
                if digest:
                    digests.add(digest)
        return digests

    def _all_known_image_digests(self) -> set[str]:
        digests = set(self._stored_image_digests())
        for item in self._collection_pool_items():
            digest = str(item.get("sha256") or "").strip()
            if digest:
                digests.add(digest)
        return digests

    def _library_source_for_rel_path(
        self,
        rel_path: str,
        item: dict[str, Any] | None = None,
    ) -> str:
        if item:
            source = str(item.get("library_source") or "").strip()
            if source in {
                MANUAL_LIBRARY_SOURCE,
                COLLECTED_LIBRARY_SOURCE,
                EXTERNAL_LIBRARY_SOURCE,
                IMAGEBED_LIBRARY_SOURCE,
            }:
                return source
        normalized = self._norm_rel_path(rel_path)
        if normalized.startswith(f"files/{COLLECTED_COLLECTION_FOLDER}/"):
            return COLLECTED_LIBRARY_SOURCE
        if normalized.startswith(f"files/{EXTERNAL_IMPORT_FOLDER}/"):
            return EXTERNAL_LIBRARY_SOURCE
        if normalized.startswith(f"files/{IMAGEBED_IMPORT_PENDING_FOLDER}/"):
            return IMAGEBED_LIBRARY_SOURCE
        if normalized.startswith(f"files/{IMAGEBED_IMPORT_LIBRARY_FOLDER}/"):
            return IMAGEBED_LIBRARY_SOURCE
        return MANUAL_LIBRARY_SOURCE

    def _source_image_count(self, source: str) -> int:
        images = self._index.get("images", {})
        if not isinstance(images, dict):
            return 0
        return sum(
            1
            for item in images.values()
            if isinstance(item, dict)
            and self._library_source_for_rel_path(
                self._norm_rel_path(item.get("rel_path")),
                item,
            )
            == source
        )

    def _config_snapshot(self) -> dict[str, Any]:
        if hasattr(self.config, "items"):
            raw = {str(key): value for key, value in self.config.items()}
        elif isinstance(self.config, dict):
            raw = dict(self.config)
        else:
            raw = {}
        snapshot = self._json_safe_copy(raw)
        snapshot[AUTO_COLLECTION_CONFIG_KEY] = self._auto_collection_config()
        snapshot[MEME_COMBAT_CONFIG_KEY] = self._meme_combat_config()
        snapshot[SCHEDULED_BACKUP_CONFIG_KEY] = self._scheduled_backup_config()
        snapshot[MODEL_FALLBACK_CONFIG_KEY] = self._model_fallback_config()
        snapshot[USER_SEARCH_CONFIG_KEY] = {
            "enabled": self._cfg_bool("user_search_enabled"),
            "request_keywords": self._request_keywords(),
        }
        snapshot[PROACTIVE_EMOJI_CONFIG_KEY] = self._proactive_emoji_config()
        snapshot["reply_after_search"] = {
            "use_custom_reply": self._cfg_bool("use_custom_reply"),
            "custom_reply": self._cfg_str("custom_reply"),
            "llm_reply_when_not_found": self._cfg_bool("llm_reply_when_not_found"),
            "not_found_reply": self._cfg_str("not_found_reply"),
            "empty_library_reply": self._cfg_str("empty_library_reply"),
        }
        snapshot["hidden_images"] = sorted(self._hidden_rel_paths())
        snapshot["sync_on_startup"] = self._cfg_bool("sync_on_startup")
        snapshot["match_confidence_threshold"] = self._cfg_float(
            "match_confidence_threshold"
        )
        snapshot[PAGE_LIBRARY_DEFAULT_VIEW_MODE_CONFIG_KEY] = (
            self._page_library_default_view_mode()
        )
        snapshot[TAG_CATEGORY_CONFIG_KEY] = self._tag_category_settings_for_storage(
            self._tag_category_settings()
        )
        snapshot[DEFAULT_CAPTION_PROVIDER_CONFIG_KEY] = (
            self._default_image_caption_provider_id()
        )
        return snapshot

    def _json_safe_copy(self, value: Any) -> Any:
        return json.loads(json.dumps(value, ensure_ascii=False, default=str))

    def _json_dump_bytes(self, value: Any) -> bytes:
        return json.dumps(
            value,
            ensure_ascii=False,
            indent=2,
            sort_keys=True,
            default=str,
        ).encode("utf-8")

    def _read_json_zip_member(self, zf: zipfile.ZipFile, name: str) -> dict[str, Any]:
        with zf.open(name, "r") as f:
            data = json.loads(f.read().decode("utf-8-sig"))
        if not isinstance(data, dict):
            raise ValueError(f"Invalid backup: {name} must be an object")
        return data

    def _safe_zip_member_name(self, name: str) -> str:
        raw = str(name or "").strip()
        if not raw or raw.endswith("/") or "\\" in raw or ":" in raw:
            return ""
        if raw.startswith("/"):
            return ""
        rel = self._norm_rel_path(raw)
        return rel if rel == raw else ""

    def _sha256_bytes(self, content: bytes) -> str:
        return hashlib.sha256(content).hexdigest()

