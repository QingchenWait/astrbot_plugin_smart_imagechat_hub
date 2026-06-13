from .common import (
    AUTO_COLLECTION_CONFIG_KEY,
    AUTO_COLLECTION_DOWNLOAD_CHUNK_BYTES,
    AUTO_COLLECTION_IMAGE_CONVERT_TIMEOUT_SECONDS,
    AUTO_COLLECTION_QUEUE_MAXSIZE,
    Any,
    AstrMessageEvent,
    COLLECTED_COLLECTION_FOLDER,
    COLLECTED_LIBRARY_SOURCE,
    EXTERNAL_IMPORT_FOLDER,
    IMAGEBED_IMPORT_LIBRARY_FOLDER,
    IMAGEBED_IMPORT_PENDING_FOLDER,
    IMAGE_FILES_CONFIG_KEY,
    IMAGE_TAGS_CONFIG_KEY,
    Image,
    MANUAL_LIBRARY_SOURCE,
    PENDING_COLLECTION_FOLDER,
    PLUGIN_NAME,
    Path,
    SUPPORTED_IMAGE_EXTS,
    _qq_id_candidates,
    aiohttp,
    asyncio,
    logger,
    re,
    shutil,
    tempfile,
    time,
    urlparse,
)


class AutoCollectionMixin:
    def _collection_pool_rel_paths(self) -> list[str]:
        rel_paths = []
        seen = set()
        for item in self._collection_pool_items():
            rel_path = self._norm_rel_path(item.get("rel_path"))
            if (
                not rel_path
                or rel_path in seen
                or not rel_path.startswith(f"files/{PENDING_COLLECTION_FOLDER}/")
                or Path(rel_path).suffix.lower() not in SUPPORTED_IMAGE_EXTS
            ):
                continue
            try:
                image_path = self._abs_plugin_data_path(rel_path)
            except ValueError:
                continue
            if not image_path.is_file():
                continue
            seen.add(rel_path)
            rel_paths.append(rel_path)
        return sorted(rel_paths)

    def _all_existing_index_rel_paths(self) -> set[str]:
        images = self._index.get("images", {})
        if not isinstance(images, dict):
            return set()
        rel_paths = {
            rel_path
            for item in images.values()
            if isinstance(item, dict)
            for rel_path in [self._norm_rel_path(item.get("rel_path"))]
            if rel_path
        }
        return self._existing_image_rel_paths(rel_paths)

    def _configured_image_rel_paths(self) -> set[str]:
        rel_paths = set()
        for raw in self._config_get(IMAGE_FILES_CONFIG_KEY, []) or []:
            rel_path = self._norm_rel_path(raw)
            if rel_path:
                rel_paths.add(rel_path)
        return rel_paths

    def _discover_uploaded_images(self) -> set[str]:
        rel_paths: set[str] = set()
        for folder in (
            self._config_file_folder(IMAGE_FILES_CONFIG_KEY),
            COLLECTED_COLLECTION_FOLDER,
            EXTERNAL_IMPORT_FOLDER,
            IMAGEBED_IMPORT_PENDING_FOLDER,
            IMAGEBED_IMPORT_LIBRARY_FOLDER,
        ):
            root = self.data_dir / "files" / folder
            if not root.is_dir():
                continue
            for path in root.rglob("*"):
                if path.is_file() and path.suffix.lower() in SUPPORTED_IMAGE_EXTS:
                    try:
                        rel_paths.add(path.relative_to(self.data_dir).as_posix())
                    except ValueError:
                        continue
        return rel_paths

    def _configured_tag_items(self) -> dict[str, dict[str, Any]]:
        items: dict[str, dict[str, Any]] = {}
        for key in (IMAGE_TAGS_CONFIG_KEY, "manual_tags"):
            raw_items = self.config.get(key, [])
            if not isinstance(raw_items, list):
                continue
            for raw_item in raw_items:
                if not isinstance(raw_item, dict):
                    continue
                rel_path = self._norm_rel_path(raw_item.get("image_path"))
                if not rel_path:
                    rel_path = self._rel_path_from_template_key(raw_item.get("__template_key"))
                if not rel_path:
                    continue
                tags = self._normalize_tags(raw_item.get("tags", []))
                auto_tags = self._normalize_tags(raw_item.get("auto_tags", []))
                selected_global_tags = self._valid_global_tags(
                    raw_item.get("selected_global_tags", [])
                )
                manual_tags_override = bool(raw_item.get("manual_tags_override", False))
                items[rel_path] = {
                    "auto_tags": auto_tags,
                    "tags": tags,
                    "selected_global_tags": selected_global_tags,
                    "manual_tags_override": manual_tags_override,
                }
        return items

    def _existing_image_rel_paths(self, rel_paths: set[str]) -> set[str]:
        existing = set()
        for rel_path in rel_paths:
            try:
                abs_path = self._abs_plugin_data_path(rel_path)
            except ValueError:
                continue
            if self._is_allowed_image(abs_path):
                existing.add(rel_path)
        return existing

    def _sync_config_image_files(self, rel_paths: set[str]) -> None:
        next_paths = sorted(
            rel_path
            for rel_path in rel_paths
            if self._library_source_for_rel_path(
                rel_path,
                self._index_image_by_id(self._image_id(rel_path)),
            )
            == MANUAL_LIBRARY_SOURCE
        )
        current_paths = sorted(self._configured_image_rel_paths())
        if current_paths == next_paths:
            return
        self._config_set(IMAGE_FILES_CONFIG_KEY, next_paths)
        self._save_plugin_config()

    def _sync_config_tags(self, rel_paths: set[str]) -> None:
        tag_items = []
        images = self._index.get("images", {})
        if not isinstance(images, dict):
            return

        for rel_path in sorted(rel_paths):
            item = images.get(self._image_id(rel_path))
            if not isinstance(item, dict):
                continue
            if self._library_source_for_rel_path(rel_path, item) != MANUAL_LIBRARY_SOURCE:
                continue
            auto_tags = self._normalize_tags(item.get("auto_tags", []))
            manual_tags = self._normalize_tags(item.get("manual_tags", []))
            manual_override = bool(item.get("manual_tags_override", False))
            selected_global_tags = self._valid_global_tags(
                item.get("selected_global_tags", [])
            )
            display_tags = manual_tags if manual_override else (manual_tags or auto_tags)
            if manual_override:
                merged_tags = self._merge_tags(display_tags, selected_global_tags)
            else:
                merged_tags = self._merge_tags(
                    auto_tags,
                    display_tags,
                    selected_global_tags,
                )
            if not merged_tags and not (auto_tags or manual_override):
                continue
            tag_items.append(
                {
                    "__template_key": self._template_key_for_image(rel_path),
                    "image_path": rel_path,
                    "auto_tags": auto_tags,
                    "tags": display_tags,
                    "selected_global_tags": selected_global_tags,
                    "manual_tags_override": manual_override,
                }
            )

        if self.config.get(IMAGE_TAGS_CONFIG_KEY) == tag_items:
            return
        self.config[IMAGE_TAGS_CONFIG_KEY] = tag_items
        self._save_plugin_config()

    async def _collect_images_from_event(self, event: AstrMessageEvent) -> None:
        cfg = self._auto_collection_config()
        group_id = str(event.get_group_id() or "").strip()
        sender_id = str(event.get_sender_id() or "").strip()
        images = [comp for comp in event.get_messages() if isinstance(comp, Image)]
        self._enqueue_auto_collection(
            group_id,
            sender_id,
            tuple(images),
            self._to_int(cfg.get("max_file_size_kb"), 1024),
            bool(cfg.get("auto_accept", False)),
        )

    def _start_auto_collection_worker(self) -> None:
        if (
            self._auto_collection_worker_task
            and not self._auto_collection_worker_task.done()
        ):
            return
        self._auto_collection_queue = asyncio.Queue(
            maxsize=AUTO_COLLECTION_QUEUE_MAXSIZE,
        )
        self._auto_collection_worker_task = asyncio.create_task(
            self._auto_collection_worker_loop(),
        )

    def _enqueue_auto_collection(
        self,
        group_id: str,
        sender_id: str,
        images: tuple[Image, ...],
        max_size_kb: int,
        auto_accept: bool,
    ) -> bool:
        if not images:
            return False
        queue = self._auto_collection_queue
        if queue is None:
            try:
                self._start_auto_collection_worker()
                queue = self._auto_collection_queue
            except RuntimeError:
                return False
        if queue is None:
            return False
        try:
            queue.put_nowait(
                {
                    "group_id": str(group_id or "").strip(),
                    "sender_id": str(sender_id or "").strip(),
                    "images": images,
                    "max_size_kb": max_size_kb,
                    "auto_accept": bool(auto_accept),
                }
            )
            return True
        except asyncio.QueueFull:
            logger.debug(
                "astrbot_plugin_smart_imagechat_hub: auto collection queue is full; skipped %s image(s) from group %s.",
                len(images),
                group_id,
            )
            return False

    async def _auto_collection_worker_loop(self) -> None:
        queue = self._auto_collection_queue
        if queue is None:
            return
        while True:
            job = await queue.get()
            try:
                await self._collect_images_from_components(
                    str(job.get("group_id") or ""),
                    str(job.get("sender_id") or ""),
                    tuple(job.get("images") or ()),
                    self._to_int(job.get("max_size_kb"), 1024),
                    bool(job.get("auto_accept", False)),
                )
            except asyncio.CancelledError:
                raise
            except Exception as exc:
                logger.warning(
                    "astrbot_plugin_smart_imagechat_hub: auto collection worker failed: %s",
                    exc,
                    exc_info=True,
                )
            finally:
                queue.task_done()

    async def _collect_images_from_components(
        self,
        group_id: str,
        sender_id: str,
        images: tuple[Image, ...],
        max_size_kb: int,
        auto_accept: bool,
    ) -> None:
        cfg = self._auto_collection_config()
        if not cfg.get("enabled"):
            return
        group_id = str(group_id or "").strip()
        if not group_id or group_id not in set(cfg.get("source_groups", [])):
            return
        sender_id = str(sender_id or "").strip()
        ignored_sender_ids = set(cfg.get("ignored_sender_ids", []))
        if ignored_sender_ids and (
            _qq_id_candidates(sender_id) & ignored_sender_ids
        ):
            return
        if not images:
            return
        if not self._auto_collection_can_accept_new_item(auto_accept):
            return

        accepted_any = False
        for image in images:
            if not self._auto_collection_can_accept_new_item(auto_accept):
                break
            image_path = ""
            try:
                image_path = await self._resolve_collected_image_path(
                    image,
                    max_size_kb,
                )
            except Exception as exc:
                logger.debug(
                    "astrbot_plugin_smart_imagechat_hub: failed to read collected image: %s",
                    exc,
                )
                continue
            if not image_path:
                continue
            if not self._is_allowed_image(Path(image_path)):
                continue
            try:
                async with self._lock:
                    if not self._auto_collection_can_accept_new_item(auto_accept):
                        break
                    known_digests = self._stored_image_digests_from_metadata()
                    pending_item = self._store_collected_image(
                        Path(image_path),
                        group_id=group_id,
                        sender_id=sender_id,
                        max_size_kb=max_size_kb,
                        known_digests=known_digests,
                        cleanup_pool=True,
                        save_pool=True,
                    )
                    if pending_item and auto_accept:
                        result = self._accept_pending_collection_images(
                            [str(pending_item.get("id") or "")],
                            capacity_action="",
                            auto_accept=True,
                        )
                        if result.get("accepted"):
                            accepted_any = True
            except Exception as exc:
                logger.warning(
                    "astrbot_plugin_smart_imagechat_hub: failed to store collected image: %s",
                    exc,
                    exc_info=True,
                )
            finally:
                self._cleanup_auto_collection_temp_path(image_path)

        if accepted_any:
            self._start_caption_background_task()

    def _auto_collection_can_accept_new_item(self, auto_accept: bool) -> bool:
        cfg = self._auto_collection_config()
        self._cleanup_collection_pool()
        if self._pending_pool_remaining_capacity(cfg) <= 0:
            return False
        if auto_accept:
            return self._solidified_remaining_capacity(cfg) > 0
        return True

    def _auto_collection_has_fast_capacity(self, auto_accept: bool) -> bool:
        cfg = self._auto_collection_config()
        if self._pending_pool_remaining_capacity(cfg) <= 0:
            return False
        if auto_accept:
            return self._solidified_remaining_capacity(cfg) > 0
        return True

    async def _resolve_collected_image_path(
        self,
        image: Image,
        max_size_kb: int,
    ) -> str:
        direct_path = self._local_image_component_path(image)
        if direct_path:
            return str(direct_path)

        url = str(getattr(image, "url", None) or getattr(image, "file", None) or "")
        if url.startswith("http://") or url.startswith("https://"):
            return str(await self._download_collected_image_url(url, max_size_kb))

        try:
            return await asyncio.wait_for(
                image.convert_to_file_path(),
                timeout=AUTO_COLLECTION_IMAGE_CONVERT_TIMEOUT_SECONDS,
            )
        except asyncio.TimeoutError:
            logger.debug(
                "astrbot_plugin_smart_imagechat_hub: timed out while converting collected image."
            )
            return ""

    def _local_image_component_path(self, image: Image) -> Path | None:
        candidates = [
            getattr(image, "path", None),
            getattr(image, "file", None),
            getattr(image, "url", None),
        ]
        for raw in candidates:
            text = str(raw or "").strip()
            if not text:
                continue
            if text.startswith("file:///"):
                text = text[8:]
            if text.startswith("file://"):
                text = text[7:]
            if text.startswith(("http://", "https://", "base64://")):
                continue
            path = Path(text)
            if path.is_file():
                return path
        return None

    async def _download_collected_image_url(self, url: str, max_size_kb: int) -> Path:
        suffix = Path(urlparse(url).path).suffix.lower()
        if suffix not in SUPPORTED_IMAGE_EXTS:
            suffix = ".jpg"
        temp_path = self._new_temp_file_path("autocollect", suffix)
        max_bytes = max(max_size_kb, 1) * 1024
        timeout = aiohttp.ClientTimeout(
            total=AUTO_COLLECTION_IMAGE_CONVERT_TIMEOUT_SECONDS,
            sock_connect=4,
            sock_read=4,
        )
        downloaded = 0
        try:
            async with aiohttp.ClientSession(
                trust_env=True,
                timeout=timeout,
            ) as session:
                async with session.get(url) as response:
                    if response.status >= 400:
                        raise ValueError(f"HTTP {response.status}")
                    content_length = self._to_int(
                        response.headers.get("content-length"),
                        0,
                    )
                    if content_length and content_length > max_bytes:
                        raise ValueError("image exceeds auto collection size limit")
                    with open(temp_path, "wb") as f:
                        async for chunk in response.content.iter_chunked(
                            AUTO_COLLECTION_DOWNLOAD_CHUNK_BYTES,
                        ):
                            if not chunk:
                                continue
                            downloaded += len(chunk)
                            if downloaded > max_bytes:
                                raise ValueError(
                                    "image exceeds auto collection size limit"
                                )
                            f.write(chunk)
        except Exception:
            self._unlink_temp_path(temp_path)
            raise
        if downloaded <= 0:
            self._unlink_temp_path(temp_path)
            raise ValueError("empty image response")
        return temp_path

    def _new_temp_file_path(self, purpose: str, suffix: str) -> Path:
        safe_suffix = suffix if suffix.startswith(".") else f".{suffix}"
        temp_file = tempfile.NamedTemporaryFile(
            prefix=f"{PLUGIN_NAME}_{purpose}_",
            suffix=safe_suffix,
            delete=False,
        )
        temp_path = Path(temp_file.name)
        temp_file.close()
        return temp_path

    def _cleanup_auto_collection_temp_path(self, image_path: str) -> None:
        path = Path(str(image_path or ""))
        if path.name.startswith(f"{PLUGIN_NAME}_autocollect_"):
            self._unlink_temp_path(path)

    def _pending_pool_remaining_capacity(
        self,
        cfg: dict[str, Any] | None = None,
    ) -> int:
        cfg = cfg or self._auto_collection_config()
        limit = self._to_int(cfg.get("pending_pool_limit"), 100)
        if limit < 0:
            return 1_000_000_000
        images = self._collection_pool.get("images", {})
        current = len(images) if isinstance(images, dict) else 0
        return max(0, limit - current)

    def _solidified_remaining_capacity(
        self,
        cfg: dict[str, Any] | None = None,
    ) -> int:
        cfg = cfg or self._auto_collection_config()
        limit = self._to_int(cfg.get("solidified_library_limit"), 300)
        if limit < 0:
            return 1_000_000_000
        return max(0, limit - self._source_image_count(COLLECTED_LIBRARY_SOURCE))

    def _store_collected_image(
        self,
        source_path: Path,
        group_id: str,
        sender_id: str,
        max_size_kb: int,
        known_digests: set[str] | None = None,
        cleanup_pool: bool = True,
        save_pool: bool = True,
    ) -> dict[str, Any] | None:
        if not source_path.is_file():
            return None
        if source_path.suffix.lower() not in SUPPORTED_IMAGE_EXTS:
            return None
        size = source_path.stat().st_size
        if size > max(max_size_kb, 1) * 1024:
            return None
        cfg = self._auto_collection_config()
        if self._pending_pool_remaining_capacity(cfg) <= 0:
            return None
        digest = self._cached_sha256(source_path)
        if cfg.get("auto_reject_discarded") and self._is_previously_discarded_digest(
            digest
        ):
            return None
        if known_digests is None:
            known_digests = self._stored_image_digests_from_metadata()
        if digest in known_digests:
            return None

        now = int(time.time())
        suffix = source_path.suffix.lower() or ".jpg"
        rel_path = self._unique_collected_pending_rel_path(group_id, now, suffix)
        target_path = self._abs_plugin_data_path(rel_path)
        target_path.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source_path, target_path)
        if not self._is_allowed_image(target_path):
            try:
                target_path.unlink()
            except OSError:
                pass
            return None

        stat = target_path.stat()
        image_id = self._image_id(rel_path)
        item = {
            "id": image_id,
            "rel_path": rel_path,
            "filename": target_path.name,
            "sha256": digest,
            "size": stat.st_size,
            "mtime": int(stat.st_mtime),
            "group_id": str(group_id),
            "sender_id": str(sender_id),
            "collected_at": now,
        }
        images = self._collection_pool.setdefault("images", {})
        if not isinstance(images, dict):
            images = {}
            self._collection_pool["images"] = images
        images[image_id] = item
        known_digests.add(digest)
        if cleanup_pool:
            self._cleanup_collection_pool()
        if save_pool:
            self._save_collection_pool()
        logger.info(
            "astrbot_plugin_smart_imagechat_hub: collected image from group %s as %s.",
            group_id,
            rel_path,
        )
        return item

    def _discarded_collection_digests(self) -> set[str]:
        digests = self._discarded_collection.get("digests", {})
        if not isinstance(digests, dict):
            return set()
        normalized = set()
        for digest in digests.keys():
            text = str(digest or "").strip()
            if text:
                normalized.add(text)
        return normalized

    def _is_previously_discarded_digest(self, digest: str) -> bool:
        normalized = str(digest or "").strip()
        if not normalized:
            return False
        digests = self._discarded_collection.get("digests", {})
        return isinstance(digests, dict) and normalized in digests

    def _remember_discarded_digest(self, digest: str) -> None:
        normalized = str(digest or "").strip()
        if not normalized:
            return
        digests = self._discarded_collection.setdefault("digests", {})
        if not isinstance(digests, dict):
            digests = {}
            self._discarded_collection["digests"] = digests
        digests[normalized] = {"discarded_at": int(time.time())}
        self._save_discarded_collection()

    def _remember_discarded_digests(self, digests_to_remember: list[str]) -> None:
        normalized_digests = [
            str(digest or "").strip()
            for digest in digests_to_remember
            if str(digest or "").strip()
        ]
        if not normalized_digests:
            return
        digests = self._discarded_collection.setdefault("digests", {})
        if not isinstance(digests, dict):
            digests = {}
            self._discarded_collection["digests"] = digests
        now = int(time.time())
        for digest in normalized_digests:
            digests[digest] = {"discarded_at": now}
        self._save_discarded_collection()

    def _unique_collected_pending_rel_path(
        self,
        group_id: str,
        timestamp: int,
        suffix: str,
    ) -> str:
        safe_group = re.sub(r"[^A-Za-z0-9_-]+", "_", str(group_id or "group")).strip(
            "_"
        ) or "group"
        suffix = suffix if suffix in SUPPORTED_IMAGE_EXTS else ".jpg"
        index = 1
        while True:
            rel_path = (
                f"files/{PENDING_COLLECTION_FOLDER}/"
                f"{safe_group}-{timestamp}-{index}{suffix}"
            )
            try:
                path = self._abs_plugin_data_path(rel_path)
            except ValueError:
                safe_group = "group"
                index += 1
                continue
            if not path.exists():
                return rel_path
            index += 1

    def _collection_pool_items(self) -> list[dict[str, Any]]:
        images = self._collection_pool.get("images", {})
        if not isinstance(images, dict):
            return []
        items = [item for item in images.values() if isinstance(item, dict)]
        return sorted(
            items,
            key=lambda item: self._to_int(item.get("collected_at"), 0),
            reverse=True,
        )

    def _collection_pool_item_by_id(self, image_id: str) -> dict[str, Any] | None:
        images = self._collection_pool.get("images", {})
        if not isinstance(images, dict):
            return None
        item = images.get(str(image_id or "").strip())
        return item if isinstance(item, dict) else None

    def _collection_pool_snapshot(self) -> dict[str, Any]:
        items = []
        for item in self._collection_pool_items():
            rel_path = self._norm_rel_path(item.get("rel_path"))
            if not rel_path:
                continue
            try:
                image_path = self._abs_plugin_data_path(rel_path)
            except ValueError:
                continue
            if not image_path.is_file():
                continue
            image_id = str(item.get("id") or self._image_id(rel_path))
            items.append(
                {
                    "id": image_id,
                    "rel_path": rel_path,
                    "filename": item.get("filename") or image_path.name,
                    "group_id": str(item.get("group_id") or ""),
                    "sender_id": str(item.get("sender_id") or ""),
                    "collected_at": self._to_int(item.get("collected_at"), 0),
                    "mtime": self._to_int(item.get("mtime"), 0),
                    "size": self._to_int(item.get("size"), 0),
                    "thumbnail_url": (
                        f"/api/plug/{PLUGIN_NAME}/collection_pending_image/{image_id}"
                    ),
                }
            )
        return {
            "images": items,
            "config": self._auto_collection_config(),
            "updated_at": int(time.time()),
        }

    def _cleanup_collection_pool(self) -> None:
        images = self._collection_pool.setdefault("images", {})
        if not isinstance(images, dict):
            images = {}
            self._collection_pool["images"] = images
        cfg = self._auto_collection_config()
        now = int(time.time())
        ttl_days = self._to_int(cfg.get("pending_ttl_days"), 3)
        ttl_seconds = ttl_days * 86400 if ttl_days > 0 else 0
        removed_ids = []
        for image_id, item in list(images.items()):
            if not isinstance(item, dict):
                removed_ids.append(image_id)
                continue
            rel_path = self._norm_rel_path(item.get("rel_path"))
            collected_at = self._to_int(item.get("collected_at"), 0)
            expired = bool(ttl_seconds and collected_at and now - collected_at > ttl_seconds)
            missing = True
            if rel_path:
                try:
                    missing = not self._abs_plugin_data_path(rel_path).is_file()
                except ValueError:
                    missing = True
            if expired or missing:
                removed_ids.append(image_id)

        for image_id in removed_ids:
            self._remove_collection_pool_item(image_id, delete_file=True)

    def _remove_collection_pool_item(
        self,
        image_id: str,
        delete_file: bool,
    ) -> dict[str, Any] | None:
        images = self._collection_pool.get("images", {})
        if not isinstance(images, dict):
            return None
        item = images.pop(str(image_id or "").strip(), None)
        if not isinstance(item, dict):
            return None
        rel_path = self._norm_rel_path(item.get("rel_path"))
        if delete_file and rel_path:
            try:
                image_path = self._abs_plugin_data_path(rel_path)
                pending_root = (
                    self.data_dir / "files" / PENDING_COLLECTION_FOLDER
                ).resolve()
                if image_path.is_file() and image_path.resolve().is_relative_to(
                    pending_root
                ):
                    image_path.unlink()
            except (OSError, ValueError) as exc:
                logger.warning(
                    "astrbot_plugin_smart_imagechat_hub: failed to remove pending collected image %s: %s",
                    rel_path,
                    exc,
                )
        return item

    def _discard_pending_collection_images(
        self,
        image_ids: list[str],
    ) -> dict[str, Any]:
        discarded = []
        skipped = []
        remember_discarded = self._auto_collection_config().get(
            "auto_reject_discarded"
        )
        discarded_digests = []
        for image_id in image_ids:
            item = self._remove_collection_pool_item(image_id, delete_file=True)
            if item:
                if remember_discarded:
                    digest = str(item.get("sha256") or "").strip()
                    if digest:
                        discarded_digests.append(digest)
                discarded.append(image_id)
            else:
                skipped.append(image_id)
        if remember_discarded:
            self._remember_discarded_digests(discarded_digests)
        self._save_collection_pool()
        return {"discarded": discarded, "skipped": skipped}

    def _accept_pending_collection_images(
        self,
        image_ids: list[str],
        capacity_action: str = "",
        auto_accept: bool = False,
    ) -> dict[str, Any]:
        accepted = []
        skipped = []
        capacity_action = str(capacity_action or "").strip()
        cfg = self._auto_collection_config()
        limit = self._to_int(cfg.get("solidified_library_limit"), 300)
        valid_items = self._valid_pending_collection_items(image_ids)
        accepted_slots_needed = len(valid_items)

        current_solidified_count = self._source_image_count(COLLECTED_LIBRARY_SOURCE)
        overflow = (
            max(0, current_solidified_count + accepted_slots_needed - limit)
            if limit >= 0
            else 0
        )
        if overflow > 0:
            if auto_accept:
                return {
                    "accepted": accepted,
                    "skipped": image_ids,
                    "capacity_error": True,
                    "capacity": {
                        "limit": limit,
                        "current": current_solidified_count,
                        "selected": accepted_slots_needed,
                        "overflow": overflow,
                    },
                }
            if capacity_action == "delete_oldest":
                self._delete_oldest_solidified_images(overflow)
                current_solidified_count = self._source_image_count(
                    COLLECTED_LIBRARY_SOURCE
                )
            elif capacity_action == "expand":
                self._expand_solidified_library_limit(cfg)
                cfg = self._auto_collection_config()
                limit = self._to_int(cfg.get("solidified_library_limit"), 300)
            overflow = (
                max(0, current_solidified_count + accepted_slots_needed - limit)
                if limit >= 0
                else 0
            )
            if overflow > 0:
                return {
                    "accepted": accepted,
                    "skipped": [],
                    "capacity_error": True,
                    "capacity": {
                        "limit": limit,
                        "current": current_solidified_count,
                        "selected": accepted_slots_needed,
                        "overflow": overflow,
                    },
                }
            if capacity_action not in {"delete_oldest", "expand"}:
                return {
                    "accepted": accepted,
                    "skipped": [],
                    "capacity_error": True,
                    "capacity": {
                        "limit": limit,
                        "current": current_solidified_count,
                        "selected": accepted_slots_needed,
                        "overflow": overflow,
                    },
                }

        images = self._index.setdefault("images", {})
        if not isinstance(images, dict):
            images = {}
            self._index["images"] = images
        known_digests = self._stored_image_digests_from_metadata(
            include_pending_pool=False
        )

        for image_id in image_ids:
            item = self._collection_pool_item_by_id(image_id)
            if not item:
                skipped.append(image_id)
                continue
            digest = str(item.get("sha256") or "").strip()
            if digest and digest in known_digests:
                self._remove_collection_pool_item(image_id, delete_file=True)
                skipped.append(image_id)
                continue
            rel_path = self._norm_rel_path(item.get("rel_path"))
            if not rel_path:
                skipped.append(image_id)
                continue
            try:
                source_path = self._abs_plugin_data_path(rel_path)
            except ValueError:
                skipped.append(image_id)
                continue
            if not self._is_allowed_image(source_path):
                self._remove_collection_pool_item(image_id, delete_file=True)
                skipped.append(image_id)
                continue

            target_rel_path = self._unique_solidified_rel_path(source_path.name)
            try:
                target_path = self._abs_plugin_data_path(target_rel_path)
            except ValueError:
                skipped.append(image_id)
                continue
            target_path.parent.mkdir(parents=True, exist_ok=True)
            try:
                source_path.replace(target_path)
            except OSError:
                shutil.copyfile(source_path, target_path)
                source_path.unlink()
            stat = target_path.stat()
            target_digest = digest or self._sha256(target_path)
            target_id = self._image_id(target_rel_path)
            now = int(time.time())
            images[target_id] = {
                "id": target_id,
                "rel_path": target_rel_path,
                "filename": target_path.name,
                "library_source": COLLECTED_LIBRARY_SOURCE,
                "sha256": target_digest,
                "size": stat.st_size,
                "mtime": int(stat.st_mtime),
                "auto_tags": self._normalize_caption_tags([], target_path.name),
                "manual_tags": [],
                "manual_tags_override": False,
                "selected_global_tags": [],
                "tags": self._normalize_caption_tags([], target_path.name),
                "caption_status": "pending",
                "caption_prompt_version": 0,
                "captioned_at": 0,
                "collected_from_group_id": str(item.get("group_id") or ""),
                "collected_sender_id": str(item.get("sender_id") or ""),
                "collected_at": self._to_int(item.get("collected_at"), now),
                "solidified_at": now,
                "updated_at": now,
            }
            self._remove_collection_pool_item(image_id, delete_file=False)
            known_digests.add(target_digest)
            accepted.append(target_id)

        if auto_accept:
            self._enforce_solidified_library_limit()
        self._save_index()
        self._save_collection_pool()
        existing_rel_paths = self._all_existing_index_rel_paths()
        self._sync_config_image_files(existing_rel_paths)
        self._sync_config_tags(existing_rel_paths)
        self._refresh_image_tag_schema(existing_rel_paths)
        self._last_library_signature = self._library_signature_for_rel_paths(
            existing_rel_paths
        )
        return {
            "accepted": accepted,
            "skipped": skipped,
            "capacity_error": False,
            "capacity": {
                "limit": limit,
                "current": self._source_image_count(COLLECTED_LIBRARY_SOURCE),
                "selected": len(accepted),
                "overflow": 0,
            },
        }

    def _valid_pending_collection_items(
        self,
        image_ids: list[str],
    ) -> list[tuple[str, dict[str, Any]]]:
        items = []
        for image_id in image_ids:
            item = self._collection_pool_item_by_id(image_id)
            if not item:
                continue
            rel_path = self._norm_rel_path(item.get("rel_path"))
            if not rel_path:
                continue
            try:
                source_path = self._abs_plugin_data_path(rel_path)
            except ValueError:
                continue
            if not self._is_allowed_image(source_path):
                continue
            items.append((image_id, item))
        return items

    def _delete_oldest_solidified_images(self, count: int) -> int:
        if count <= 0:
            return 0
        images = self._index.get("images", {})
        if not isinstance(images, dict):
            return 0
        solidified = [
            item
            for item in images.values()
            if isinstance(item, dict)
            and self._library_source_for_rel_path(
                self._norm_rel_path(item.get("rel_path")),
                item,
            )
            == COLLECTED_LIBRARY_SOURCE
        ]
        solidified.sort(
            key=self._solidified_library_order_key,
        )
        deleted = 0
        for item in solidified[:count]:
            result = self._delete_image(
                str(item.get("id") or ""),
                source=COLLECTED_LIBRARY_SOURCE,
                sync_after=False,
            )
            if result:
                deleted += 1
        return deleted

    def _solidified_library_order_key(self, item: dict[str, Any]) -> tuple[int, int, str]:
        rel_path = self._norm_rel_path(item.get("rel_path"))
        created_at = self._solidified_library_created_at(item, rel_path)
        return (
            1 if created_at <= 0 else 0,
            created_at,
            rel_path or str(item.get("id") or ""),
        )

    def _solidified_library_created_at(
        self,
        item: dict[str, Any],
        rel_path: str = "",
    ) -> int:
        for key in ("solidified_at", "collected_at"):
            value = self._to_int(item.get(key), 0)
            if value > 0:
                return value
        path_time = self._solidified_time_from_path(rel_path or item.get("rel_path"))
        if path_time > 0:
            return path_time
        for key in ("updated_at", "captioned_at"):
            value = self._to_int(item.get(key), 0)
            if value > 0:
                return value
        return 0

    def _solidified_time_from_path(self, rel_path: Any) -> int:
        filename = Path(self._norm_rel_path(rel_path)).stem
        match = re.match(r"^(\d+)-(\d{10})-\d+(?:_\d+)?$", filename)
        if not match:
            return 0
        return self._to_int(match.group(2), 0)

    def _expand_solidified_library_limit(self, cfg: dict[str, Any]) -> int:
        current_limit = self._to_int(cfg.get("solidified_library_limit"), 300)
        pending_limit = self._to_int(cfg.get("pending_pool_limit"), 100)
        if current_limit < 0:
            return current_limit
        next_limit = current_limit + max(0, pending_limit)
        next_cfg = dict(cfg)
        next_cfg["solidified_library_limit"] = next_limit
        self.config[AUTO_COLLECTION_CONFIG_KEY] = (
            self._normalize_auto_collection_config(next_cfg)
        )
        self._save_plugin_config()
        return next_limit

    def _unique_solidified_rel_path(self, filename: str) -> str:
        safe_name = self._safe_upload_filename(filename) or "image.jpg"
        return self._unique_upload_rel_path(COLLECTED_COLLECTION_FOLDER, safe_name)

    def _enforce_solidified_library_limit(self) -> None:
        limit = self._to_int(
            self._auto_collection_config().get("solidified_library_limit"),
            300,
        )
        if limit < 0:
            return
        images = self._index.get("images", {})
        if not isinstance(images, dict):
            return
        solidified = [
            item
            for item in images.values()
            if isinstance(item, dict)
            and self._library_source_for_rel_path(
                self._norm_rel_path(item.get("rel_path")),
                item,
            )
            == COLLECTED_LIBRARY_SOURCE
        ]
        solidified.sort(
            key=lambda item: self._to_int(
                item.get("solidified_at") or item.get("updated_at"),
                0,
            )
            )
        overflow = max(0, len(solidified) - limit)
        for item in solidified[:overflow]:
            self._delete_image(
                str(item.get("id") or ""),
                source=COLLECTED_LIBRARY_SOURCE,
                sync_after=False,
            )

    def _index_image_by_id(self, image_id: str) -> dict[str, Any] | None:
        images = self._index.get("images", {})
        if not isinstance(images, dict):
            return None
        item = images.get(str(image_id or "").strip())
        return item if isinstance(item, dict) else None

