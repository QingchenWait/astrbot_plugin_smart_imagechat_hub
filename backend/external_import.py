from .common import (
    Any,
    EXTERNAL_IMPORT_FOLDER,
    EXTERNAL_IMPORT_THUMBNAIL_FOLDER,
    EXTERNAL_LIBRARY_SOURCE,
    PLUGIN_NAME,
    SUPPORTED_IMAGE_EXTS,
    Path,
    asyncio,
    logger,
    json,
    re,
    time,
)

EXTERNAL_IMPORT_WARNING_PREFERENCES_VERSION = 2


class ExternalImportMixin:
    def _external_import_root(self) -> Path:
        return self.data_dir.parent.resolve()

    def _load_external_import_state(self) -> dict[str, Any]:
        if not self.external_import_state_path.is_file():
            return self._empty_external_import_state()
        try:
            with open(self.external_import_state_path, encoding="utf-8-sig") as f:
                data = self._loads_json_object(f.read())
            if not isinstance(data, dict):
                raise ValueError("external import state root is not object")
            data.setdefault("version", 1)
            data.setdefault("imports", {})
            data.setdefault("manually_deleted_digests", {})
            data.setdefault("active_import", {})
            data.setdefault("last_stat", {})
            data.setdefault("caption_paused", True)
            data.setdefault("warning_preferences", {})
            stored_warning_preferences_version = data.get(
                "warning_preferences_version"
            )
            if not isinstance(data["imports"], dict):
                data["imports"] = {}
            if not isinstance(data["manually_deleted_digests"], dict):
                data["manually_deleted_digests"] = {}
            if not isinstance(data["active_import"], dict):
                data["active_import"] = {}
            if not isinstance(data["last_stat"], dict):
                data["last_stat"] = {}
            if not isinstance(data["warning_preferences"], dict):
                data["warning_preferences"] = {}
            if self._to_int(
                stored_warning_preferences_version,
                0,
            ) != EXTERNAL_IMPORT_WARNING_PREFERENCES_VERSION:
                data["warning_preferences"] = {}
            data["warning_preferences_version"] = (
                EXTERNAL_IMPORT_WARNING_PREFERENCES_VERSION
            )
            return data
        except Exception as exc:
            logger.warning(
                "astrbot_plugin_smart_imagechat_hub: failed to load external import state: %s",
                exc,
            )
            return self._empty_external_import_state()

    def _empty_external_import_state(self) -> dict[str, Any]:
        return {
            "version": 1,
            "imports": {},
            "manually_deleted_digests": {},
            "active_import": {},
            "last_stat": {},
            "caption_paused": True,
            "warning_preferences": {},
            "warning_preferences_version": EXTERNAL_IMPORT_WARNING_PREFERENCES_VERSION,
        }

    def _save_external_import_state(self) -> None:
        self.data_dir.mkdir(parents=True, exist_ok=True)
        with open(self.external_import_state_path, "w", encoding="utf-8") as f:
            json.dump(self._external_import_state, f, ensure_ascii=False, indent=2)

    def _external_import_discover_rel_paths(self) -> set[str]:
        rel_paths: set[str] = set()
        root = self.data_dir / "files" / EXTERNAL_IMPORT_FOLDER
        if not root.is_dir():
            return rel_paths
        for path in self._iter_external_images(root):
            try:
                rel_paths.add(path.relative_to(self.data_dir).as_posix())
            except ValueError:
                continue
        return rel_paths

    def _external_import_visible_tree(self) -> dict[str, Any]:
        root = self._external_import_root()
        root.mkdir(parents=True, exist_ok=True)
        return {
            "name": root.name or str(root),
            "rel_path": "",
            "children": self._external_import_dir_children(root, ""),
            "updated_at": int(time.time()),
        }

    def _external_import_dir_children(
        self,
        directory: Path,
        rel_path: str,
        visited: set[Path] | None = None,
    ) -> list[dict[str, Any]]:
        if rel_path and len(rel_path.split("/")) > 8:
            return []
        visited = visited or set()
        try:
            resolved = directory.resolve()
        except OSError:
            return []
        if resolved in visited:
            return []
        next_visited = set(visited)
        next_visited.add(resolved)
        children = []
        try:
            entries = sorted(
                (entry for entry in directory.iterdir() if entry.is_dir()),
                key=lambda entry: entry.name.lower(),
            )
        except OSError:
            return children

        for entry in entries:
            if entry.name == PLUGIN_NAME:
                continue
            child_rel = f"{rel_path}/{entry.name}".strip("/")
            children.append(
                {
                    "name": entry.name,
                    "rel_path": child_rel,
                    "children": self._external_import_dir_children(
                        entry,
                        child_rel,
                        next_visited,
                    ),
                }
            )
        return children

    def _external_import_dir_from_rel(self, rel_path: Any) -> Path:
        text = str(rel_path if rel_path is not None else "").replace("\\", "/").strip()
        root = self._external_import_root()
        if not text:
            raise ValueError("directory is required")
        parts = [part for part in text.split("/") if part]
        if any(part in {".", ".."} for part in parts):
            raise ValueError("invalid external directory")
        path = (root / Path(*parts)).resolve()
        try:
            path.relative_to(root)
        except ValueError as exc:
            raise ValueError("external directory is outside plugin data root") from exc
        if path == self.data_dir.resolve():
            raise ValueError("cannot import this plugin's own data directory")
        plugin_root = self.data_dir.resolve()
        try:
            path.relative_to(plugin_root)
        except ValueError:
            pass
        else:
            raise ValueError("cannot import this plugin's own data directory")
        if not path.is_dir():
            raise ValueError("external directory not found")
        return path

    def _iter_external_images(self, directory: Path):
        stack = [directory]
        visited: set[Path] = set()
        while stack:
            current = stack.pop()
            try:
                resolved = current.resolve()
            except OSError:
                continue
            if resolved in visited:
                continue
            visited.add(resolved)
            try:
                entries = sorted(
                    current.iterdir(),
                    key=lambda entry: entry.name.lower(),
                    reverse=True,
                )
            except OSError:
                continue
            for path in entries:
                try:
                    if path.is_dir():
                        stack.append(path)
                    elif (
                        path.is_file()
                        and path.suffix.lower() in SUPPORTED_IMAGE_EXTS
                    ):
                        yield path
                except OSError:
                    continue

    def _external_import_stat_directory(self, rel_path: str) -> dict[str, Any]:
        rel_path = str(rel_path or "").strip().replace("\\", "/").strip("/")
        directory = self._external_import_dir_from_rel(rel_path)
        count = 0
        total_bytes = 0
        for path in self._iter_external_images(directory):
            count += 1
            try:
                total_bytes += path.stat().st_size
            except OSError:
                continue
        stat = {
            "directory": rel_path,
            "count": count,
            "total_size": total_bytes,
            "updated_at": int(time.time()),
        }
        self._external_import_state["last_stat"] = stat
        self._save_external_import_state()
        return stat

    async def _external_import_stat_directory_async(
        self,
        rel_path: str,
    ) -> dict[str, Any]:
        return await asyncio.to_thread(self._external_import_stat_directory, rel_path)

    def _external_import_status_snapshot(self) -> dict[str, Any]:
        active = self._external_import_state.get("active_import", {})
        if not isinstance(active, dict):
            active = {}
        else:
            active = dict(active)
            if (
                active.get("status") == "running"
                and (
                    not self._external_import_task
                    or self._external_import_task.done()
                )
            ):
                active["status"] = "stopped"
        last_stat = self._external_import_state.get("last_stat", {})
        if not isinstance(last_stat, dict):
            last_stat = {}
        library_count = self._source_image_count(EXTERNAL_LIBRARY_SOURCE)
        active["pending_count"] = self._external_pending_count()
        active["library_count"] = library_count
        caption_paused = self._external_caption_paused()
        return {
            "active_import": active,
            "last_stat": last_stat,
            "pending_count": active["pending_count"],
            "library_count": library_count,
            "caption_paused": caption_paused,
            "caption_active": not caption_paused and active["pending_count"] > 0,
            "updated_at": int(time.time()),
        }

    async def _start_external_import(
        self,
        rel_path: str,
        include_parent_dir_tag: bool = False,
    ) -> dict[str, Any]:
        rel_path = str(rel_path or "").strip().replace("\\", "/").strip("/")
        directory = self._external_import_dir_from_rel(rel_path)
        if self._external_import_task and not self._external_import_task.done():
            raise ValueError("external import is already running")
        import_id = f"external-{int(time.time())}"
        active = {
            "id": import_id,
            "directory": rel_path,
            "status": "running",
            "scanned": 0,
            "copied": 0,
            "skipped_duplicates": 0,
            "skipped_deleted": 0,
            "skipped_errors": 0,
            "include_parent_dir_tag": bool(include_parent_dir_tag),
            "message": "External image import started.",
            "started_at": int(time.time()),
            "updated_at": int(time.time()),
        }
        async with self._lock:
            self._external_import_state["caption_paused"] = True
            self._external_import_state["active_import"] = active
            self._save_external_import_state()
        self._external_import_task = asyncio.create_task(
            self._external_import_worker(
                import_id,
                directory,
                rel_path,
                bool(include_parent_dir_tag),
            )
        )
        return self._external_import_status_snapshot()

    async def _external_import_worker(
        self,
        import_id: str,
        directory: Path,
        rel_path: str,
        include_parent_dir_tag: bool = False,
    ) -> None:
        try:
            async with self._lock:
                known_digests = self._external_import_known_digests()
                manually_deleted = self._external_import_deleted_digests()
                self._last_library_signature = self._library_signature()
            copied_any = False
            copied_since_save = 0
            for source_path in self._iter_external_images(directory):
                await asyncio.sleep(0)
                if not await self._external_import_increment_counter(
                    import_id,
                    "scanned",
                ):
                    return

                try:
                    digest = await self._cached_sha256_async(source_path)
                except OSError:
                    await self._external_import_increment_counter(
                        import_id,
                        "skipped_errors",
                    )
                    continue

                try:
                    async with self._lock:
                        active = self._external_active_import(import_id)
                        if not active or active.get("status") == "cancelled":
                            return
                        if digest in known_digests:
                            active["skipped_duplicates"] = (
                                self._to_int(active.get("skipped_duplicates"), 0) + 1
                            )
                            active["updated_at"] = int(time.time())
                            continue
                        if digest in manually_deleted:
                            active["skipped_deleted"] = (
                                self._to_int(active.get("skipped_deleted"), 0) + 1
                            )
                            active["updated_at"] = int(time.time())
                            continue

                    item = await self._copy_external_import_image(
                        source_path,
                        digest,
                        rel_path,
                        include_parent_dir_tag=include_parent_dir_tag,
                    )
                    async with self._lock:
                        active = self._external_active_import(import_id)
                        if not active or active.get("status") == "cancelled":
                            if item:
                                self._discard_copied_external_import_item(item)
                            return
                        if digest in known_digests or digest in manually_deleted:
                            if item:
                                self._discard_copied_external_import_item(item)
                            skip_key = (
                                "skipped_deleted"
                                if digest in manually_deleted
                                else "skipped_duplicates"
                            )
                            active[skip_key] = self._to_int(active.get(skip_key), 0) + 1
                            active["updated_at"] = int(time.time())
                            continue
                        if item:
                            copied_any = True
                            copied_since_save += 1
                            known_digests.add(digest)
                            images = self._index.setdefault("images", {})
                            if not isinstance(images, dict):
                                images = {}
                                self._index["images"] = images
                            images[str(item.get("id") or "")] = item
                            self._remember_external_import_source(rel_path, digest)
                            active["copied"] = self._to_int(active.get("copied"), 0) + 1
                        else:
                            active["skipped_errors"] = (
                                self._to_int(active.get("skipped_errors"), 0) + 1
                            )
                        active["updated_at"] = int(time.time())
                except Exception as exc:
                    logger.warning(
                        "astrbot_plugin_smart_imagechat_hub: failed to import external image %s: %s",
                        source_path,
                        exc,
                    )
                    async with self._lock:
                        active = self._external_active_import(import_id)
                        if active:
                            active["skipped_errors"] = (
                                self._to_int(active.get("skipped_errors"), 0) + 1
                            )
                            active["updated_at"] = int(time.time())
                if copied_since_save >= 25:
                    async with self._lock:
                        self._save_index()
                        self._save_external_import_state()
                    copied_since_save = 0

            async with self._lock:
                active = self._external_active_import(import_id)
                if active:
                    active["status"] = "done"
                    active["message"] = "External image import finished."
                    active["finished_at"] = int(time.time())
                    active["updated_at"] = int(time.time())
                self._save_index()
                existing_rel_paths = self._all_existing_index_rel_paths()
                self._sync_config_image_files(existing_rel_paths)
                self._sync_config_tags(existing_rel_paths)
                self._refresh_image_tag_schema(existing_rel_paths)
                self._last_library_signature = self._library_signature_for_rel_paths(
                    existing_rel_paths
                )
                if copied_any:
                    self._refresh_caption_progress_after_external_pending_change()
                self._save_external_import_state()
        except asyncio.CancelledError:
            async with self._lock:
                active = self._external_active_import(import_id)
                if active:
                    if active.get("status") != "done":
                        active["status"] = "cancelled"
                        active["message"] = "External image import was cancelled."
                    active["updated_at"] = int(time.time())
                self._save_index()
                existing_rel_paths = self._all_existing_index_rel_paths()
                self._sync_config_image_files(existing_rel_paths)
                self._sync_config_tags(existing_rel_paths)
                self._refresh_image_tag_schema(existing_rel_paths)
                self._last_library_signature = self._library_signature_for_rel_paths(
                    existing_rel_paths
                )
                self._save_external_import_state()
            raise
        except Exception as exc:
            logger.warning(
                "astrbot_plugin_smart_imagechat_hub: external import worker failed: %s",
                exc,
                exc_info=True,
            )
            async with self._lock:
                active = self._external_active_import(import_id)
                if active:
                    if active.get("status") != "done":
                        active["status"] = "failed"
                        active["message"] = str(exc)
                    active["updated_at"] = int(time.time())
                self._save_index()
                existing_rel_paths = self._all_existing_index_rel_paths()
                self._sync_config_image_files(existing_rel_paths)
                self._sync_config_tags(existing_rel_paths)
                self._refresh_image_tag_schema(existing_rel_paths)
                self._last_library_signature = self._library_signature_for_rel_paths(
                    existing_rel_paths
                )
                self._save_external_import_state()

    async def _external_import_increment_counter(
        self,
        import_id: str,
        key: str,
        amount: int = 1,
    ) -> bool:
        async with self._lock:
            active = self._external_active_import(import_id)
            if not active or active.get("status") == "cancelled":
                return False
            active[key] = self._to_int(active.get(key), 0) + amount
            active["updated_at"] = int(time.time())
            return True

    def _external_active_import(self, import_id: str) -> dict[str, Any] | None:
        active = self._external_import_state.get("active_import", {})
        if not isinstance(active, dict):
            return None
        if str(active.get("id") or "") != str(import_id or ""):
            return None
        return active

    def _external_import_known_digests(self) -> set[str]:
        return self._stored_image_digests_from_metadata(include_pending_pool=True)

    def _external_import_deleted_digests(self) -> set[str]:
        digests = self._external_import_state.get("manually_deleted_digests", {})
        if not isinstance(digests, dict):
            return set()
        return {str(digest).strip() for digest in digests.keys() if str(digest).strip()}

    def _external_caption_paused(self) -> bool:
        return bool(self._external_import_state.get("caption_paused", False))

    def _is_paused_external_caption_item(self, item: dict[str, Any]) -> bool:
        if not self._external_caption_paused():
            return False
        rel_path = self._norm_rel_path(item.get("rel_path"))
        return (
            self._library_source_for_rel_path(rel_path, item)
            == EXTERNAL_LIBRARY_SOURCE
            and item.get("caption_status") in {"pending", "running", "failed"}
        )

    async def _copy_external_import_image(
        self,
        source_path: Path,
        digest: str,
        source_rel_path: str,
        include_parent_dir_tag: bool = False,
    ) -> dict[str, Any] | None:
        try:
            valid_source = (
                source_path.is_file()
                and source_path.suffix.lower() in SUPPORTED_IMAGE_EXTS
            )
        except OSError:
            return None
        if not valid_source:
            return None
        safe_source = re.sub(
            r"[^A-Za-z0-9_-]+",
            "_",
            str(source_rel_path or "external").strip("/\\") or "external",
        ).strip("_") or "external"
        target_rel_path = self._unique_upload_rel_path(
            EXTERNAL_IMPORT_FOLDER,
            f"{safe_source}-{source_path.name}",
        )
        target_path = self._abs_plugin_data_path(target_rel_path)
        target_path.parent.mkdir(parents=True, exist_ok=True)
        await self._copy_file_streaming_async(
            source_path,
            target_path,
            chunk_size=4 * 1024 * 1024,
        )
        if not self._is_allowed_image(target_path):
            self._unlink_temp_path(target_path)
            return None

        stat = target_path.stat()
        now = int(time.time())
        image_id = self._image_id(target_rel_path)
        import_extra_tags = (
            self._external_import_parent_dir_tags(source_path)
            if include_parent_dir_tag
            else []
        )
        item = {
            "id": image_id,
            "rel_path": target_rel_path,
            "filename": target_path.name,
            "library_source": EXTERNAL_LIBRARY_SOURCE,
            "sha256": digest,
            "size": stat.st_size,
            "mtime": int(stat.st_mtime),
            "auto_tags": self._normalize_caption_tags([], target_path.name),
            "manual_tags": [],
            "manual_tags_override": False,
            "selected_global_tags": [],
            "tags": self._normalize_caption_tags([], target_path.name),
            "import_extra_tags": import_extra_tags,
            "caption_status": "pending",
            "caption_prompt_version": 0,
            "captioned_at": 0,
            "external_source_dir": source_rel_path,
            "external_source_path": str(source_path),
            "external_imported_at": now,
            "updated_at": now,
        }
        return item

    def _external_import_parent_dir_tags(self, source_path: Path) -> list[str]:
        try:
            parent_name = source_path.parent.name
        except OSError:
            parent_name = ""
        return self._normalize_tags([parent_name])[:1]

    def _discard_copied_external_import_item(self, item: dict[str, Any]) -> None:
        rel_path = self._norm_rel_path(item.get("rel_path"))
        if not rel_path:
            return
        try:
            target_path = self._abs_plugin_data_path(rel_path)
        except ValueError:
            return
        self._unlink_temp_path(target_path)

    async def _external_import_image_response_path(self, image_id: str) -> Path:
        item = self._index_image_by_id(image_id)
        if not item:
            raise ValueError("image not found")
        rel_path = self._norm_rel_path(item.get("rel_path"))
        if (
            not rel_path
            or self._library_source_for_rel_path(rel_path, item)
            != EXTERNAL_LIBRARY_SOURCE
        ):
            raise ValueError("image not found")
        try:
            image_path = self._abs_plugin_data_path(rel_path)
        except ValueError as exc:
            raise ValueError("invalid image path") from exc
        if not image_path.is_file():
            raise ValueError("image file missing")
        return self._external_import_thumbnail_path(item) or image_path

    def _remember_external_import_source(self, source_rel_path: str, digest: str) -> None:
        source_rel_path = str(source_rel_path or "").strip()
        imports = self._external_import_state.setdefault("imports", {})
        if not isinstance(imports, dict):
            imports = {}
            self._external_import_state["imports"] = imports
        record = imports.setdefault(source_rel_path, {})
        if not isinstance(record, dict):
            record = {}
            imports[source_rel_path] = record
        digests = record.setdefault("digests", {})
        if not isinstance(digests, dict):
            digests = {}
            record["digests"] = digests
        digests[digest] = {"imported_at": int(time.time())}
        record["updated_at"] = int(time.time())

    def _external_pending_count(self) -> int:
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
            == EXTERNAL_LIBRARY_SOURCE
            and item.get("caption_status") in {"pending", "running", "failed"}
        )

    def _external_pending_items(self) -> list[dict[str, Any]]:
        images = self._index.get("images", {})
        if not isinstance(images, dict):
            return []
        items = []
        for item in images.values():
            if not isinstance(item, dict):
                continue
            rel_path = self._norm_rel_path(item.get("rel_path"))
            if not rel_path:
                continue
            if (
                self._library_source_for_rel_path(rel_path, item)
                != EXTERNAL_LIBRARY_SOURCE
            ):
                continue
            if item.get("caption_status") not in {"pending", "running", "failed"}:
                continue
            try:
                image_path = self._abs_plugin_data_path(rel_path)
            except ValueError:
                continue
            if not image_path.is_file():
                continue
            items.append(self._external_pending_item_snapshot(item, image_path))
        items.sort(
            key=lambda entry: (
                self._to_int(entry.get("external_imported_at"), 0),
                self._to_int(entry.get("updated_at"), 0),
            ),
            reverse=True,
        )
        return items

    def _external_pending_item_snapshot(
        self,
        item: dict[str, Any],
        image_path: Path,
    ) -> dict[str, Any]:
        image_id = str(item.get("id") or self._image_id(item.get("rel_path", "")))
        return {
            "id": image_id,
            "rel_path": self._norm_rel_path(item.get("rel_path")),
            "filename": item.get("filename") or image_path.name,
            "caption_status": str(item.get("caption_status") or ""),
            "size": self._to_int(item.get("size"), 0),
            "mtime": self._to_int(item.get("mtime"), 0),
            "updated_at": self._to_int(item.get("updated_at"), 0),
            "external_imported_at": self._to_int(item.get("external_imported_at"), 0),
            "thumbnail_url": f"/api/plug/{PLUGIN_NAME}/external_import_thumb/{image_id}",
            "prefer_direct_thumbnail": True,
        }

    def _external_import_pending_snapshot(self) -> dict[str, Any]:
        return {
            "images": self._external_pending_items(),
            "status": self._external_import_status_snapshot(),
            "warning_preferences": self._external_import_warning_preferences(),
            "updated_at": int(time.time()),
        }

    def _external_import_thumbnail_path(self, item: dict[str, Any]) -> Path | None:
        rel_path = self._norm_rel_path(item.get("rel_path"))
        if not rel_path:
            return None
        image_id = str(item.get("id") or self._image_id(rel_path)).strip()
        if not image_id:
            return None
        try:
            source_path = self._abs_plugin_data_path(rel_path)
            thumb_path = self._abs_plugin_data_path(
                f"files/{EXTERNAL_IMPORT_THUMBNAIL_FOLDER}/{image_id}{source_path.suffix.lower() or '.jpg'}"
            )
        except ValueError:
            return None
        if thumb_path.is_file():
            try:
                source_stat = source_path.stat()
                thumb_stat = thumb_path.stat()
                if thumb_stat.st_mtime >= source_stat.st_mtime:
                    return thumb_path
            except OSError:
                return thumb_path
        return None

    def _external_import_warning_preferences(self) -> dict[str, bool]:
        raw = self._external_import_state.get("warning_preferences", {})
        if not isinstance(raw, dict):
            return {}
        return {
            "delete_pending": bool(raw.get("delete_pending")),
            "cancel_caption": bool(raw.get("cancel_caption")),
        }

    def _set_external_import_warning_preference(
        self,
        action: str,
        skip: bool,
    ) -> dict[str, bool]:
        action = str(action or "").strip()
        if action not in {"delete_pending", "cancel_caption"}:
            raise ValueError("invalid warning action")
        raw = self._external_import_state.setdefault("warning_preferences", {})
        if not isinstance(raw, dict):
            raw = {}
            self._external_import_state["warning_preferences"] = raw
        raw[action] = bool(skip)
        self._external_import_state["warning_preferences_version"] = (
            EXTERNAL_IMPORT_WARNING_PREFERENCES_VERSION
        )
        self._save_external_import_state()
        return self._external_import_warning_preferences()

    def _delete_external_pending_images(self, image_ids: list[str]) -> dict[str, Any]:
        deleted = []
        skipped = []
        digests = self._external_import_state.setdefault("manually_deleted_digests", {})
        if not isinstance(digests, dict):
            digests = {}
            self._external_import_state["manually_deleted_digests"] = digests
        now = int(time.time())
        for image_id in image_ids:
            item = self._index_image_by_id(image_id)
            if not isinstance(item, dict):
                skipped.append(image_id)
                continue
            rel_path = self._norm_rel_path(item.get("rel_path"))
            if (
                not rel_path
                or item.get("caption_status") == "done"
                or self._library_source_for_rel_path(rel_path, item)
                != EXTERNAL_LIBRARY_SOURCE
            ):
                skipped.append(image_id)
                continue
            digest = str(item.get("sha256") or "").strip()
            removed = self._delete_image(
                image_id,
                source=EXTERNAL_LIBRARY_SOURCE,
                sync_after=False,
            )
            if not removed:
                skipped.append(image_id)
                continue
            if digest:
                digests[digest] = {"deleted_at": now}
            deleted.append(image_id)

        self._save_index()
        self._save_external_import_state()
        existing_rel_paths = self._all_existing_index_rel_paths()
        self._sync_config_image_files(existing_rel_paths)
        self._sync_config_tags(existing_rel_paths)
        self._refresh_image_tag_schema(existing_rel_paths)
        self._last_library_signature = self._library_signature_for_rel_paths(
            existing_rel_paths
        )
        self._refresh_caption_progress_after_external_pending_change()
        return {"deleted": deleted, "skipped": skipped}

    async def _pause_external_captioning(self) -> None:
        await self._cancel_caption_task()
        async with self._lock:
            self._external_import_state["caption_paused"] = True
            self._save_external_import_state()
            self._refresh_caption_progress_after_external_pending_change()

    async def _resume_external_captioning(self) -> None:
        async with self._lock:
            self._external_import_state["caption_paused"] = False
            self._save_external_import_state()
        self._start_caption_background_task()

    async def _start_external_captioning(self) -> None:
        if self._external_import_task and not self._external_import_task.done():
            raise ValueError("external import is still running")
        if not self._default_image_caption_provider_id():
            raise ValueError("default image caption provider is not configured")
        await self._resume_external_captioning()

    async def _toggle_external_captioning(self) -> dict[str, Any]:
        if self._external_caption_paused():
            await self._resume_external_captioning()
        else:
            await self._pause_external_captioning()
        return self._external_import_pending_snapshot()

    async def _cancel_external_captioning(self) -> dict[str, Any]:
        await self._cancel_caption_task()
        async with self._lock:
            pending_ids = [
                str(item.get("id") or "")
                for item in self._index.get("images", {}).values()
                if isinstance(item, dict)
                and self._library_source_for_rel_path(
                    self._norm_rel_path(item.get("rel_path")),
                    item,
                )
                == EXTERNAL_LIBRARY_SOURCE
                and item.get("caption_status") in {"pending", "running", "failed"}
            ]
            result = {"deleted": [], "skipped": []}
            if pending_ids:
                for image_id in pending_ids:
                    removed = self._delete_image(
                        image_id,
                        source=EXTERNAL_LIBRARY_SOURCE,
                        sync_after=False,
                    )
                    if removed:
                        result["deleted"].append(image_id)
                    else:
                        result["skipped"].append(image_id)
                self._save_index()
                existing_rel_paths = self._all_existing_index_rel_paths()
                self._sync_config_image_files(existing_rel_paths)
                self._sync_config_tags(existing_rel_paths)
                self._refresh_image_tag_schema(existing_rel_paths)
                self._last_library_signature = self._library_signature_for_rel_paths(
                    existing_rel_paths
                )
            self._external_import_state["caption_paused"] = False
            self._save_external_import_state()
            self._set_caption_progress(
                status="cancelled",
                remaining=len(self._pending_caption_rel_paths()),
                current_image="",
                message="External import tag generation was cancelled.",
                error_detail="",
                error_image="",
                error_message="",
                error_source="",
            )
            return result

    def _refresh_caption_progress_after_external_pending_change(self) -> None:
        pending_count = len(self._pending_caption_rel_paths())
        running_count = self._running_caption_count()
        paused_external_count = (
            self._external_pending_count() if self._external_caption_paused() else 0
        )
        current_total = self._to_int(self._caption_progress.get("total"), 0)
        completed = self._to_int(self._caption_progress.get("completed"), 0)
        failed = self._to_int(self._caption_progress.get("failed"), 0)
        if self._caption_task and not self._caption_task.done():
            total = completed + failed + pending_count + running_count
            self._set_caption_progress(
                total=total,
                remaining=pending_count + running_count,
            )
            return
        if pending_count:
            total = max(completed + failed + pending_count, pending_count)
            self._set_caption_progress(
                status="pending",
                total=total,
                remaining=pending_count,
                current_image="",
            )
            return
        if paused_external_count:
            self._set_caption_progress(
                status="pending",
                total=completed + failed + paused_external_count,
                remaining=paused_external_count,
                current_image="",
                message="External import tag generation paused.",
                error_detail="",
                error_image="",
                error_message="",
                error_source="",
            )
            return
        self._set_caption_progress(
            status="done",
            total=min(current_total, completed + failed),
            remaining=0,
            current_image="",
            error_detail="",
            error_image="",
            error_message="",
            error_source="",
        )
