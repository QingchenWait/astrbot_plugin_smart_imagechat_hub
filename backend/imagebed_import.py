import hashlib
import hmac
import traceback
import xml.etree.ElementTree as ET
from urllib.parse import quote, unquote, urlparse

from .common import (
    Any,
    DEFAULT_CAPTION_PROVIDER_CONFIG_KEY,
    IMAGEBED_IMPORT_CONFIG_KEY,
    IMAGEBED_IMPORT_LIBRARY_FOLDER,
    IMAGEBED_IMPORT_PENDING_FOLDER,
    IMAGEBED_LIBRARY_SOURCE,
    PLUGIN_NAME,
    SUPPORTED_IMAGE_EXTS,
    Path,
    aiohttp,
    asyncio,
    json,
    logger,
    re,
    shutil,
    time,
)


class ImageBedImportMixin:
    def _empty_imagebed_import_state(self) -> dict[str, Any]:
        return {
            "version": 1,
            "config": {},
            "active_import": {},
            "known_remote_objects": {},
            "last_connection": {},
            "last_stat": {},
            "last_successful_sync_at": 0,
            "caption_paused": True,
            "last_error": {},
        }

    def _empty_imagebed_discarded(self) -> dict[str, Any]:
        return {"version": 1, "digests": {}, "objects": {}}

    def _load_imagebed_import_state(self) -> dict[str, Any]:
        if not self.imagebed_import_state_path.is_file():
            return self._empty_imagebed_import_state()
        try:
            with open(self.imagebed_import_state_path, encoding="utf-8-sig") as f:
                data = self._loads_json_object(f.read())
            if not isinstance(data, dict):
                raise ValueError("imagebed import state root is not object")
            default = self._empty_imagebed_import_state()
            for key, value in default.items():
                data.setdefault(key, value)
            for key in (
                "config",
                "active_import",
                "known_remote_objects",
                "last_connection",
                "last_stat",
                "last_error",
            ):
                if not isinstance(data.get(key), dict):
                    data[key] = {}
            data["caption_paused"] = self._to_bool(data.get("caption_paused"), True)
            data["last_successful_sync_at"] = self._to_int(
                data.get("last_successful_sync_at"),
                0,
            )
            return data
        except Exception as exc:
            logger.warning(
                "astrbot_plugin_smart_imagechat_hub: failed to load imagebed import state: %s",
                exc,
            )
            return self._empty_imagebed_import_state()

    def _save_imagebed_import_state(self) -> None:
        self.data_dir.mkdir(parents=True, exist_ok=True)
        with open(self.imagebed_import_state_path, "w", encoding="utf-8") as f:
            json.dump(self._imagebed_import_state, f, ensure_ascii=False, indent=2)

    def _load_imagebed_discarded(self) -> dict[str, Any]:
        if not self.imagebed_discarded_path.is_file():
            return self._empty_imagebed_discarded()
        try:
            with open(self.imagebed_discarded_path, encoding="utf-8-sig") as f:
                data = self._loads_json_object(f.read())
            if not isinstance(data, dict):
                raise ValueError("imagebed discarded root is not object")
            data.setdefault("version", 1)
            for key in ("digests", "objects"):
                if not isinstance(data.get(key), dict):
                    data[key] = {}
            return data
        except Exception as exc:
            logger.warning(
                "astrbot_plugin_smart_imagechat_hub: failed to load imagebed discarded state: %s",
                exc,
            )
            return self._empty_imagebed_discarded()

    def _save_imagebed_discarded(self) -> None:
        digests = self._imagebed_discarded.get("digests", {})
        objects = self._imagebed_discarded.get("objects", {})
        has_records = (
            isinstance(digests, dict)
            and bool(digests)
            or isinstance(objects, dict)
            and bool(objects)
        )
        if not has_records and not self.imagebed_discarded_path.is_file():
            return
        self.data_dir.mkdir(parents=True, exist_ok=True)
        with open(self.imagebed_discarded_path, "w", encoding="utf-8") as f:
            json.dump(self._imagebed_discarded, f, ensure_ascii=False, indent=2)

    def _migrate_imagebed_import_config(self) -> None:
        current = self.config.get(IMAGEBED_IMPORT_CONFIG_KEY, {})
        stored = self._imagebed_import_state.get("config", {})
        normalized = self._normalize_imagebed_import_config(current, stored)
        if current != normalized or stored != normalized:
            self.config[IMAGEBED_IMPORT_CONFIG_KEY] = normalized
            self._imagebed_import_state["config"] = self._json_safe_copy(normalized)
            self._save_plugin_config()
            self._save_imagebed_import_state()

    def _imagebed_import_config(self) -> dict[str, Any]:
        current = self.config.get(IMAGEBED_IMPORT_CONFIG_KEY, {})
        stored = self._imagebed_import_state.get("config", {})
        return self._normalize_imagebed_import_config(current, stored)

    def _normalize_imagebed_import_config(
        self,
        raw: Any,
        current: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        raw = raw if isinstance(raw, dict) else {}
        current = current if isinstance(current, dict) else {}
        account_id = self._clean_imagebed_text(
            raw.get("account_id") if "account_id" in raw else current.get("account_id")
        )
        access_key_id = self._clean_imagebed_text(
            raw.get("access_key_id")
            if "access_key_id" in raw
            else current.get("access_key_id")
        )
        secret_access_key = self._clean_imagebed_text(
            raw.get("secret_access_key")
            if "secret_access_key" in raw
            else current.get("secret_access_key")
        )
        if not secret_access_key and "secret_access_key" not in raw:
            secret_access_key = self._clean_imagebed_text(
                current.get("secret_access_key")
            )
        bucket_name = self._clean_imagebed_text(
            raw.get("bucket_name") if "bucket_name" in raw else current.get("bucket_name")
        )
        endpoint_url = self._clean_imagebed_text(
            raw.get("endpoint_url")
            if "endpoint_url" in raw
            else current.get("endpoint_url")
        ).rstrip("/")
        prefix = self._normalize_imagebed_prefix(
            raw.get("prefix") if "prefix" in raw else current.get("prefix")
        )
        max_file_size_kb = self._to_int(
            raw.get("max_file_size_kb")
            if "max_file_size_kb" in raw
            else current.get("max_file_size_kb"),
            5120,
        )
        scheduled_time = self._normalize_backup_time(
            raw.get("scheduled_time")
            if "scheduled_time" in raw
            else current.get("scheduled_time"),
            "03:30",
        )
        return {
            "account_id": account_id,
            "access_key_id": access_key_id,
            "secret_access_key": secret_access_key,
            "bucket_name": bucket_name,
            "endpoint_url": endpoint_url,
            "prefix": prefix,
            "max_file_size_kb": max(1, max_file_size_kb),
            "scheduled_enabled": self._to_bool(
                raw.get("scheduled_enabled")
                if "scheduled_enabled" in raw
                else current.get("scheduled_enabled"),
                False,
            ),
            "scheduled_time": scheduled_time,
        }

    def _set_imagebed_import_config(
        self,
        cfg: dict[str, Any],
        *,
        save_plugin_config: bool = True,
        save_state: bool = True,
    ) -> dict[str, Any]:
        normalized = self._normalize_imagebed_import_config(
            cfg,
            self._imagebed_import_state.get("config", {}),
        )
        self.config[IMAGEBED_IMPORT_CONFIG_KEY] = normalized
        self._imagebed_import_state["config"] = self._json_safe_copy(normalized)
        if save_plugin_config:
            self._save_plugin_config()
        if save_state:
            self._save_imagebed_import_state()
        return normalized

    def _clean_imagebed_text(self, value: Any) -> str:
        return str(value if value is not None else "").strip()

    def _normalize_imagebed_prefix(self, value: Any) -> str:
        text = str(value if value is not None else "").replace("\\", "/").strip()
        text = text.lstrip("/")
        while "//" in text:
            text = text.replace("//", "/")
        return text

    def _imagebed_config_snapshot(self) -> dict[str, Any]:
        cfg = self._imagebed_import_config()
        return {
            "account_id": cfg["account_id"],
            "access_key_id": cfg["access_key_id"],
            "secret_access_key": cfg["secret_access_key"],
            "secret_configured": bool(cfg["secret_access_key"]),
            "bucket_name": cfg["bucket_name"],
            "endpoint_url": cfg["endpoint_url"],
            "effective_endpoint_url": self._imagebed_endpoint_url(cfg, allow_empty=True),
            "prefix": cfg["prefix"],
            "max_file_size_kb": cfg["max_file_size_kb"],
            "scheduled_enabled": cfg["scheduled_enabled"],
            "scheduled_time": cfg["scheduled_time"],
            "status": self._imagebed_import_status_snapshot(),
            "updated_at": int(time.time()),
        }

    def _imagebed_endpoint_url(
        self,
        cfg: dict[str, Any],
        allow_empty: bool = False,
    ) -> str:
        endpoint_url = str(cfg.get("endpoint_url") or "").strip().rstrip("/")
        if not endpoint_url:
            account_id = str(cfg.get("account_id") or "").strip()
            if account_id:
                endpoint_url = f"https://{account_id}.r2.cloudflarestorage.com"
        if not endpoint_url and allow_empty:
            return ""
        parsed = urlparse(endpoint_url)
        if parsed.scheme not in {"http", "https"} or not parsed.netloc:
            raise ValueError("Cloudflare R2 endpoint is invalid")
        return endpoint_url

    def _validate_imagebed_config(self, cfg: dict[str, Any]) -> None:
        missing = []
        if not str(cfg.get("account_id") or "").strip() and not str(
            cfg.get("endpoint_url") or ""
        ).strip():
            missing.append("account_id")
        for key in ("access_key_id", "secret_access_key", "bucket_name"):
            if not str(cfg.get(key) or "").strip():
                missing.append(key)
        if missing:
            raise ValueError("Cloudflare R2 config missing: " + ", ".join(missing))
        self._imagebed_endpoint_url(cfg)

    def _imagebed_import_status_snapshot(self) -> dict[str, Any]:
        active = self._imagebed_import_state.get("active_import", {})
        if not isinstance(active, dict):
            active = {}
        else:
            active = dict(active)
            if (
                active.get("status") == "running"
                and (
                    not self._imagebed_import_task
                    or self._imagebed_import_task.done()
                )
            ):
                active["status"] = "stopped"
        pending_count = self._imagebed_pending_count()
        library_count = self._source_image_count(IMAGEBED_LIBRARY_SOURCE)
        last_error = self._imagebed_import_state.get("last_error", {})
        if not isinstance(last_error, dict):
            last_error = {}
        return {
            "active_import": active,
            "last_connection": self._json_safe_copy(
                self._imagebed_import_state.get("last_connection", {})
            ),
            "last_stat": self._json_safe_copy(
                self._imagebed_import_state.get("last_stat", {})
            ),
            "last_successful_sync_at": self._to_int(
                self._imagebed_import_state.get("last_successful_sync_at"),
                0,
            ),
            "pending_count": pending_count,
            "library_count": library_count,
            "caption_paused": self._imagebed_caption_paused(),
            "caption_active": (
                not self._imagebed_caption_paused() and pending_count > 0
            ),
            "last_error": last_error,
            "updated_at": int(time.time()),
        }

    def _imagebed_remote_object_marker(
        self,
        cfg: dict[str, Any],
        obj: dict[str, Any],
    ) -> str:
        bucket = str(cfg.get("bucket_name") or "").strip()
        key = str(obj.get("key") or "")
        etag = str(obj.get("etag") or "")
        size = self._to_int(obj.get("size"), 0)
        raw = f"{bucket}\n{key}\n{etag}\n{size}"
        return hashlib.sha1(raw.encode("utf-8")).hexdigest()

    def _imagebed_known_remote_markers(self) -> set[str]:
        markers = set()
        raw = self._imagebed_import_state.get("known_remote_objects", {})
        if isinstance(raw, dict):
            markers.update(str(marker) for marker in raw.keys() if str(marker).strip())
        images = self._index.get("images", {})
        if isinstance(images, dict):
            for item in images.values():
                if not isinstance(item, dict):
                    continue
                marker = str(item.get("imagebed_object_marker") or "").strip()
                if marker:
                    markers.add(marker)
        return markers

    def _imagebed_discarded_markers(self) -> set[str]:
        raw = self._imagebed_discarded.get("objects", {})
        if not isinstance(raw, dict):
            return set()
        return {str(marker) for marker in raw.keys() if str(marker).strip()}

    def _imagebed_discarded_digests(self) -> set[str]:
        raw = self._imagebed_discarded.get("digests", {})
        if not isinstance(raw, dict):
            return set()
        return {str(digest) for digest in raw.keys() if str(digest).strip()}

    def _imagebed_record_known_remote_object(
        self,
        marker: str,
        obj: dict[str, Any],
        status: str,
    ) -> None:
        marker = str(marker or "").strip()
        if not marker:
            return
        known = self._imagebed_import_state.setdefault("known_remote_objects", {})
        if not isinstance(known, dict):
            known = {}
            self._imagebed_import_state["known_remote_objects"] = known
        known[marker] = {
            "status": status,
            "key": str(obj.get("key") or ""),
            "etag": str(obj.get("etag") or ""),
            "size": self._to_int(obj.get("size"), 0),
            "updated_at": int(time.time()),
        }

    def _imagebed_forget_known_remote_object(self, item: dict[str, Any]) -> None:
        marker = str(item.get("imagebed_object_marker") or "").strip()
        if not marker:
            return
        known = self._imagebed_import_state.get("known_remote_objects", {})
        if isinstance(known, dict):
            known.pop(marker, None)

    def _imagebed_record_discarded_item(self, item: dict[str, Any]) -> None:
        now = int(time.time())
        digest = str(item.get("sha256") or "").strip()
        if digest:
            digests = self._imagebed_discarded.setdefault("digests", {})
            if not isinstance(digests, dict):
                digests = {}
                self._imagebed_discarded["digests"] = digests
            digests[digest] = {"discarded_at": now}
        marker = str(item.get("imagebed_object_marker") or "").strip()
        if marker:
            objects = self._imagebed_discarded.setdefault("objects", {})
            if not isinstance(objects, dict):
                objects = {}
                self._imagebed_discarded["objects"] = objects
            objects[marker] = {
                "discarded_at": now,
                "key": str(item.get("imagebed_object_key") or ""),
                "etag": str(item.get("imagebed_object_etag") or ""),
                "size": self._to_int(item.get("imagebed_object_size"), 0),
            }
        self._imagebed_forget_known_remote_object(item)

    def _imagebed_caption_paused(self) -> bool:
        return bool(self._imagebed_import_state.get("caption_paused", True))

    def _is_paused_imagebed_caption_item(self, item: dict[str, Any]) -> bool:
        if not self._imagebed_caption_paused():
            return False
        rel_path = self._norm_rel_path(item.get("rel_path"))
        return (
            self._library_source_for_rel_path(rel_path, item)
            == IMAGEBED_LIBRARY_SOURCE
            and item.get("caption_status") in {"pending", "running", "failed"}
        )

    def _imagebed_pending_count(self) -> int:
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
            == IMAGEBED_LIBRARY_SOURCE
            and item.get("caption_status") in {"pending", "running", "failed"}
        )

    def _imagebed_pending_items(self) -> list[dict[str, Any]]:
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
                != IMAGEBED_LIBRARY_SOURCE
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
            image_id = str(item.get("id") or self._image_id(rel_path))
            items.append(
                {
                    "id": image_id,
                    "rel_path": rel_path,
                    "filename": item.get("filename") or image_path.name,
                    "caption_status": str(item.get("caption_status") or ""),
                    "size": self._to_int(item.get("size"), 0),
                    "mtime": self._to_int(item.get("mtime"), 0),
                    "updated_at": self._to_int(item.get("updated_at"), 0),
                    "imagebed_imported_at": self._to_int(
                        item.get("imagebed_imported_at"),
                        0,
                    ),
                    "thumbnail_url": f"/api/plug/{PLUGIN_NAME}/imagebed_import_thumb/{image_id}",
                    "prefer_direct_thumbnail": True,
                }
            )
        items.sort(
            key=lambda entry: (
                self._to_int(entry.get("imagebed_imported_at"), 0),
                self._to_int(entry.get("updated_at"), 0),
            ),
            reverse=True,
        )
        return items

    def _imagebed_import_pending_snapshot(self) -> dict[str, Any]:
        return {
            "images": self._imagebed_pending_items(),
            "status": self._imagebed_import_status_snapshot(),
            "updated_at": int(time.time()),
        }

    async def _imagebed_import_image_response_path(self, image_id: str) -> Path:
        item = self._index_image_by_id(image_id)
        if not item:
            raise ValueError("image not found")
        rel_path = self._norm_rel_path(item.get("rel_path"))
        if (
            not rel_path
            or self._library_source_for_rel_path(rel_path, item)
            != IMAGEBED_LIBRARY_SOURCE
        ):
            raise ValueError("image not found")
        try:
            image_path = self._abs_plugin_data_path(rel_path)
        except ValueError as exc:
            raise ValueError("invalid image path") from exc
        if not image_path.is_file():
            raise ValueError("image file missing")
        return image_path

    async def _imagebed_s3_get(
        self,
        cfg: dict[str, Any],
        canonical_uri: str,
        query_params: list[tuple[str, str]],
        session: aiohttp.ClientSession,
        timeout_seconds: int,
    ) -> aiohttp.ClientResponse:
        endpoint = self._imagebed_endpoint_url(cfg)
        parsed_endpoint = urlparse(endpoint)
        host = parsed_endpoint.netloc
        request_path = canonical_uri
        canonical_query = self._imagebed_canonical_query(query_params)
        url = endpoint + request_path
        if canonical_query:
            url = f"{url}?{canonical_query}"
        now = time.gmtime()
        amz_date = time.strftime("%Y%m%dT%H%M%SZ", now)
        date_stamp = time.strftime("%Y%m%d", now)
        headers = {
            "host": host,
            "x-amz-content-sha256": "UNSIGNED-PAYLOAD",
            "x-amz-date": amz_date,
        }
        signed_headers = "host;x-amz-content-sha256;x-amz-date"
        canonical_headers = "".join(f"{key}:{headers[key]}\n" for key in sorted(headers))
        canonical_request = "\n".join(
            [
                "GET",
                canonical_uri,
                canonical_query,
                canonical_headers,
                signed_headers,
                "UNSIGNED-PAYLOAD",
            ]
        )
        credential_scope = f"{date_stamp}/auto/s3/aws4_request"
        string_to_sign = "\n".join(
            [
                "AWS4-HMAC-SHA256",
                amz_date,
                credential_scope,
                hashlib.sha256(canonical_request.encode("utf-8")).hexdigest(),
            ]
        )
        signing_key = self._imagebed_signature_key(
            str(cfg.get("secret_access_key") or ""),
            date_stamp,
        )
        signature = hmac.new(
            signing_key,
            string_to_sign.encode("utf-8"),
            hashlib.sha256,
        ).hexdigest()
        headers["authorization"] = (
            "AWS4-HMAC-SHA256 "
            f"Credential={cfg['access_key_id']}/{credential_scope}, "
            f"SignedHeaders={signed_headers}, Signature={signature}"
        )
        response = await session.get(
            url,
            headers=headers,
            timeout=aiohttp.ClientTimeout(total=timeout_seconds),
        )
        if response.status >= 400:
            text = await response.text()
            response.release()
            raise ValueError(
                f"R2 request failed: HTTP {response.status}: {self._short_error_text(text)}"
            )
        return response

    def _imagebed_signature_key(self, secret: str, date_stamp: str) -> bytes:
        key = ("AWS4" + secret).encode("utf-8")
        date_key = hmac.new(key, date_stamp.encode("utf-8"), hashlib.sha256).digest()
        region_key = hmac.new(date_key, b"auto", hashlib.sha256).digest()
        service_key = hmac.new(region_key, b"s3", hashlib.sha256).digest()
        return hmac.new(service_key, b"aws4_request", hashlib.sha256).digest()

    def _imagebed_canonical_query(self, params: list[tuple[str, str]]) -> str:
        encoded = []
        for key, value in params:
            encoded.append(
                (
                    quote(str(key), safe="-_.~"),
                    quote(str(value), safe="-_.~"),
                )
            )
        encoded.sort()
        return "&".join(f"{key}={value}" for key, value in encoded)

    def _imagebed_object_uri(self, bucket: str, key: str = "") -> str:
        bucket_part = quote(bucket, safe="-_.~")
        if not key:
            return f"/{bucket_part}"
        key_part = quote(key, safe="/-_.~")
        return f"/{bucket_part}/{key_part}"

    def _short_error_text(self, text: str, limit: int = 800) -> str:
        normalized = re.sub(r"\s+", " ", str(text or "")).strip()
        if len(normalized) <= limit:
            return normalized
        return normalized[:limit] + "..."

    async def _imagebed_list_remote_objects(
        self,
        cfg: dict[str, Any],
        session: aiohttp.ClientSession | None = None,
    ) -> list[dict[str, Any]]:
        self._validate_imagebed_config(cfg)
        owns_session = session is None
        if owns_session:
            session = aiohttp.ClientSession()
        assert session is not None
        objects: list[dict[str, Any]] = []
        token = ""
        try:
            while True:
                params = [
                    ("encoding-type", "url"),
                    ("list-type", "2"),
                    ("max-keys", "1000"),
                ]
                prefix = str(cfg.get("prefix") or "")
                if prefix:
                    params.append(("prefix", prefix))
                if token:
                    params.append(("continuation-token", token))
                async with await self._imagebed_s3_get(
                    cfg,
                    self._imagebed_object_uri(str(cfg["bucket_name"])),
                    params,
                    session,
                    30,
                ) as response:
                    text = await response.text()
                parsed = self._parse_imagebed_list_objects(text)
                for obj in parsed["objects"]:
                    key = str(obj.get("key") or "")
                    if (
                        key
                        and Path(key).suffix.lower() in SUPPORTED_IMAGE_EXTS
                        and self._to_int(obj.get("size"), 0) > 0
                    ):
                        objects.append(obj)
                if not parsed["is_truncated"]:
                    break
                token = str(parsed.get("next_token") or "")
                if not token:
                    break
                await asyncio.sleep(0)
        finally:
            if owns_session:
                await session.close()
        return objects

    def _parse_imagebed_list_objects(self, text: str) -> dict[str, Any]:
        try:
            root = ET.fromstring(text)
        except ET.ParseError as exc:
            raise ValueError("R2 list response is not valid XML") from exc

        objects = []
        for node in root.findall(".//{*}Contents"):
            key = self._xml_child_text(node, "Key")
            if key:
                key = unquote(key)
            objects.append(
                {
                    "key": key,
                    "etag": self._xml_child_text(node, "ETag").strip('"'),
                    "size": self._to_int(self._xml_child_text(node, "Size"), 0),
                    "last_modified": self._xml_child_text(node, "LastModified"),
                }
            )
        return {
            "objects": objects,
            "is_truncated": self._xml_child_text(root, "IsTruncated").lower()
            == "true",
            "next_token": self._xml_child_text(root, "NextContinuationToken"),
        }

    def _xml_child_text(self, node: ET.Element, name: str) -> str:
        child = node.find(f"{{*}}{name}")
        if child is None or child.text is None:
            return ""
        return str(child.text)

    async def _test_imagebed_connection(
        self,
        payload: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        current = self._imagebed_import_config()
        cfg = (
            self._normalize_imagebed_import_config(payload, current)
            if isinstance(payload, dict)
            else current
        )
        checked_at = int(time.time())
        try:
            self._validate_imagebed_config(cfg)
            async with aiohttp.ClientSession() as session:
                objects = await self._imagebed_list_remote_objects(cfg, session)
            unsynced_count = self._imagebed_unsynced_count(cfg, objects)
            stat = {
                "count": len(objects),
                "unsynced_count": unsynced_count,
                "total_size": sum(self._to_int(obj.get("size"), 0) for obj in objects),
                "checked_at": checked_at,
            }
            connection = {
                "connected": True,
                "message": "连接成功。",
                "checked_at": checked_at,
            }
        except Exception as exc:
            stat = {
                "count": 0,
                "unsynced_count": 0,
                "total_size": 0,
                "checked_at": checked_at,
            }
            connection = {
                "connected": False,
                "message": str(exc),
                "checked_at": checked_at,
            }
        async with self._lock:
            self._imagebed_import_state["last_connection"] = connection
            self._imagebed_import_state["last_stat"] = stat
            self._save_imagebed_import_state()
        return {
            "config": self._imagebed_config_snapshot(),
            "connection": connection,
            "stat": stat,
            "status": self._imagebed_import_status_snapshot(),
        }

    def _imagebed_unsynced_count(
        self,
        cfg: dict[str, Any],
        objects: list[dict[str, Any]],
    ) -> int:
        known_markers = self._imagebed_known_remote_markers()
        discarded_markers = self._imagebed_discarded_markers()
        count = 0
        for obj in objects:
            marker = self._imagebed_remote_object_marker(cfg, obj)
            if marker in known_markers or marker in discarded_markers:
                continue
            count += 1
        return count

    async def _start_imagebed_import(self, trigger: str = "manual") -> dict[str, Any]:
        cfg = self._imagebed_import_config()
        self._validate_imagebed_config(cfg)
        if self._imagebed_import_task and not self._imagebed_import_task.done():
            raise ValueError("imagebed import is already running")
        import_id = f"imagebed-{int(time.time())}"
        active = {
            "id": import_id,
            "status": "running",
            "trigger": trigger,
            "listed": 0,
            "scanned": 0,
            "copied": 0,
            "skipped_known": 0,
            "skipped_duplicates": 0,
            "skipped_discarded": 0,
            "skipped_too_large": 0,
            "skipped_errors": 0,
            "message": "Imagebed import started.",
            "started_at": int(time.time()),
            "updated_at": int(time.time()),
        }
        async with self._lock:
            self._imagebed_import_state["caption_paused"] = True
            self._imagebed_import_state["active_import"] = active
            self._save_imagebed_import_state()
        self._imagebed_import_task = asyncio.create_task(
            self._imagebed_import_worker(import_id, cfg, trigger)
        )
        return self._imagebed_import_status_snapshot()

    async def _imagebed_import_worker(
        self,
        import_id: str,
        cfg: dict[str, Any],
        trigger: str,
    ) -> None:
        copied_any = False
        copied_since_save = 0
        try:
            async with self._lock:
                known_markers = self._imagebed_known_remote_markers()
                discarded_markers = self._imagebed_discarded_markers()
                known_digests = self._stored_image_digests_from_metadata(
                    include_pending_pool=True
                )
                discarded_digests = self._imagebed_discarded_digests()
                self._last_library_signature = self._library_signature()
            async with aiohttp.ClientSession() as session:
                objects = await self._imagebed_list_remote_objects(cfg, session)
                async with self._lock:
                    active = self._imagebed_active_import(import_id)
                    if not active:
                        return
                    active["listed"] = len(objects)
                    active["updated_at"] = int(time.time())
                max_bytes = max(1, self._to_int(cfg.get("max_file_size_kb"), 5120)) * 1024
                for obj in objects:
                    await asyncio.sleep(0)
                    if not await self._imagebed_increment_counter(
                        import_id,
                        "scanned",
                    ):
                        return
                    marker = self._imagebed_remote_object_marker(cfg, obj)
                    if marker in known_markers:
                        await self._imagebed_increment_counter(
                            import_id,
                            "skipped_known",
                        )
                        continue
                    if marker in discarded_markers:
                        await self._imagebed_increment_counter(
                            import_id,
                            "skipped_discarded",
                        )
                        continue
                    size = self._to_int(obj.get("size"), 0)
                    if size > max_bytes:
                        await self._imagebed_increment_counter(
                            import_id,
                            "skipped_too_large",
                        )
                        continue

                    item = None
                    try:
                        item = await self._download_imagebed_object(
                            cfg,
                            obj,
                            marker,
                            session,
                            max_bytes,
                        )
                        digest = str(item.get("sha256") or "")
                        if digest in known_digests:
                            self._discard_copied_imagebed_item(item)
                            self._imagebed_record_known_remote_object(
                                marker,
                                obj,
                                "duplicate",
                            )
                            known_markers.add(marker)
                            await self._imagebed_increment_counter(
                                import_id,
                                "skipped_duplicates",
                            )
                            continue
                        if digest in discarded_digests:
                            self._discard_copied_imagebed_item(item)
                            self._imagebed_record_known_remote_object(
                                marker,
                                obj,
                                "discarded_digest",
                            )
                            known_markers.add(marker)
                            await self._imagebed_increment_counter(
                                import_id,
                                "skipped_discarded",
                            )
                            continue
                        async with self._lock:
                            active = self._imagebed_active_import(import_id)
                            if not active or active.get("status") == "cancelled":
                                self._discard_copied_imagebed_item(item)
                                return
                            images = self._index.setdefault("images", {})
                            if not isinstance(images, dict):
                                images = {}
                                self._index["images"] = images
                            images[str(item.get("id") or "")] = item
                            self._imagebed_record_known_remote_object(
                                marker,
                                obj,
                                "imported",
                            )
                            active["copied"] = (
                                self._to_int(active.get("copied"), 0) + 1
                            )
                            active["updated_at"] = int(time.time())
                            copied_any = True
                            copied_since_save += 1
                            known_markers.add(marker)
                            known_digests.add(digest)
                    except Exception as exc:
                        if item:
                            self._discard_copied_imagebed_item(item)
                        logger.warning(
                            "astrbot_plugin_smart_imagechat_hub: failed to import R2 object %s: %s",
                            obj.get("key"),
                            exc,
                            exc_info=True,
                        )
                        await self._imagebed_increment_counter(
                            import_id,
                            "skipped_errors",
                        )
                    if copied_since_save >= 20:
                        async with self._lock:
                            self._save_index()
                            self._save_imagebed_import_state()
                        copied_since_save = 0

            async with self._lock:
                active = self._imagebed_active_import(import_id)
                if active:
                    active["status"] = "done"
                    active["message"] = "Imagebed import finished."
                    active["finished_at"] = int(time.time())
                    active["updated_at"] = int(time.time())
                self._imagebed_import_state["last_successful_sync_at"] = int(time.time())
                self._save_index()
                self._save_imagebed_import_state()
                existing_rel_paths = self._all_existing_index_rel_paths()
                self._sync_config_image_files(existing_rel_paths)
                self._sync_config_tags(existing_rel_paths)
                self._refresh_image_tag_schema(existing_rel_paths)
                self._last_library_signature = self._library_signature_for_rel_paths(
                    existing_rel_paths
                )
                if copied_any:
                    self._refresh_caption_progress_after_imagebed_pending_change()
        except asyncio.CancelledError:
            async with self._lock:
                active = self._imagebed_active_import(import_id)
                if active and active.get("status") != "done":
                    active["status"] = "cancelled"
                    active["message"] = "Imagebed import was cancelled."
                    active["updated_at"] = int(time.time())
                self._save_index()
                self._save_imagebed_import_state()
            raise
        except Exception as exc:
            detail = traceback.format_exc()
            logger.warning(
                "astrbot_plugin_smart_imagechat_hub: imagebed import worker failed: %s",
                exc,
                exc_info=True,
            )
            async with self._lock:
                active = self._imagebed_active_import(import_id)
                if active and active.get("status") != "done":
                    active["status"] = "failed"
                    active["message"] = str(exc)
                    active["updated_at"] = int(time.time())
                self._record_imagebed_import_error(
                    "图床同步失败。",
                    detail,
                    trigger,
                )
                self._save_index()
                self._save_imagebed_import_state()

    async def _download_imagebed_object(
        self,
        cfg: dict[str, Any],
        obj: dict[str, Any],
        marker: str,
        session: aiohttp.ClientSession,
        max_bytes: int,
    ) -> dict[str, Any]:
        key = str(obj.get("key") or "")
        filename = self._safe_upload_filename(Path(key).name or "image")
        if not filename or Path(filename).suffix.lower() not in SUPPORTED_IMAGE_EXTS:
            raise ValueError("unsupported image filename")
        target_rel_path = self._unique_upload_rel_path(
            IMAGEBED_IMPORT_PENDING_FOLDER,
            filename,
        )
        target_path = self._abs_plugin_data_path(target_rel_path)
        target_path.parent.mkdir(parents=True, exist_ok=True)
        temp_path = target_path.with_name(f".{target_path.name}.download")
        digest = hashlib.sha256()
        total = 0
        try:
            async with await self._imagebed_s3_get(
                cfg,
                self._imagebed_object_uri(str(cfg["bucket_name"]), key),
                [],
                session,
                60,
            ) as response:
                content_length = self._to_int(response.headers.get("Content-Length"), 0)
                if content_length > max_bytes:
                    raise ValueError("remote image exceeds max_file_size_kb")
                with open(temp_path, "wb") as f:
                    async for chunk in response.content.iter_chunked(128 * 1024):
                        if not chunk:
                            continue
                        total += len(chunk)
                        if total > max_bytes:
                            raise ValueError("remote image exceeds max_file_size_kb")
                        digest.update(chunk)
                        f.write(chunk)
            temp_path.replace(target_path)
        except Exception:
            self._unlink_temp_path(temp_path)
            self._unlink_temp_path(target_path)
            raise

        if not self._is_allowed_image(target_path):
            self._unlink_temp_path(target_path)
            raise ValueError("downloaded object is not a supported image")
        stat = target_path.stat()
        now = int(time.time())
        image_id = self._image_id(target_rel_path)
        return {
            "id": image_id,
            "rel_path": target_rel_path,
            "filename": target_path.name,
            "library_source": IMAGEBED_LIBRARY_SOURCE,
            "sha256": digest.hexdigest(),
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
            "imagebed_object_key": key,
            "imagebed_object_etag": str(obj.get("etag") or ""),
            "imagebed_object_size": self._to_int(obj.get("size"), stat.st_size),
            "imagebed_object_last_modified": str(obj.get("last_modified") or ""),
            "imagebed_object_marker": marker,
            "imagebed_imported_at": now,
            "updated_at": now,
        }

    def _discard_copied_imagebed_item(self, item: dict[str, Any]) -> None:
        rel_path = self._norm_rel_path(item.get("rel_path"))
        if not rel_path:
            return
        try:
            target_path = self._abs_plugin_data_path(rel_path)
        except ValueError:
            return
        self._unlink_temp_path(target_path)

    async def _imagebed_increment_counter(
        self,
        import_id: str,
        key: str,
        amount: int = 1,
    ) -> bool:
        async with self._lock:
            active = self._imagebed_active_import(import_id)
            if not active or active.get("status") == "cancelled":
                return False
            active[key] = self._to_int(active.get(key), 0) + amount
            active["updated_at"] = int(time.time())
            return True

    def _imagebed_active_import(self, import_id: str) -> dict[str, Any] | None:
        active = self._imagebed_import_state.get("active_import", {})
        if not isinstance(active, dict):
            return None
        if str(active.get("id") or "") != str(import_id or ""):
            return None
        return active

    async def _start_imagebed_captioning(self) -> None:
        if self._imagebed_import_task and not self._imagebed_import_task.done():
            raise ValueError("imagebed import is still running")
        if not self._default_image_caption_provider_id():
            raise ValueError("default image caption provider is not configured")
        async with self._lock:
            self._imagebed_import_state["caption_paused"] = False
            self._save_imagebed_import_state()
        self._start_caption_background_task()

    async def _cancel_imagebed_captioning(self) -> dict[str, Any]:
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
                == IMAGEBED_LIBRARY_SOURCE
                and item.get("caption_status") in {"pending", "running", "failed"}
            ]
            result = {"deleted": [], "skipped": []}
            for image_id in pending_ids:
                item = self._index_image_by_id(image_id)
                if isinstance(item, dict):
                    self._imagebed_forget_known_remote_object(item)
                removed = self._delete_image(
                    image_id,
                    source=IMAGEBED_LIBRARY_SOURCE,
                    sync_after=False,
                )
                if removed:
                    result["deleted"].append(image_id)
                else:
                    result["skipped"].append(image_id)
            self._imagebed_import_state["caption_paused"] = True
            self._save_index()
            self._save_imagebed_import_state()
            existing_rel_paths = self._all_existing_index_rel_paths()
            self._sync_config_image_files(existing_rel_paths)
            self._sync_config_tags(existing_rel_paths)
            self._refresh_image_tag_schema(existing_rel_paths)
            self._last_library_signature = self._library_signature_for_rel_paths(
                existing_rel_paths
            )
            self._set_caption_progress(
                status="cancelled",
                remaining=len(self._pending_caption_rel_paths()),
                current_image="",
                message="Imagebed import tag generation was cancelled.",
                error_detail="",
                error_image="",
                error_message="",
                error_source="",
            )
            return result

    def _delete_imagebed_pending_images(self, image_ids: list[str]) -> dict[str, Any]:
        deleted = []
        skipped = []
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
                != IMAGEBED_LIBRARY_SOURCE
            ):
                skipped.append(image_id)
                continue
            self._imagebed_record_discarded_item(item)
            removed = self._delete_image(
                image_id,
                source=IMAGEBED_LIBRARY_SOURCE,
                sync_after=False,
            )
            if removed:
                deleted.append(image_id)
            else:
                skipped.append(image_id)
        self._save_index()
        self._save_imagebed_import_state()
        self._save_imagebed_discarded()
        existing_rel_paths = self._all_existing_index_rel_paths()
        self._sync_config_image_files(existing_rel_paths)
        self._sync_config_tags(existing_rel_paths)
        self._refresh_image_tag_schema(existing_rel_paths)
        self._last_library_signature = self._library_signature_for_rel_paths(
            existing_rel_paths
        )
        self._refresh_caption_progress_after_imagebed_pending_change()
        return {"deleted": deleted, "skipped": skipped}

    def _rollback_caption_failed_imagebed_item(
        self,
        item: dict[str, Any],
    ) -> None:
        item["caption_status"] = "pending"
        item["caption_prompt_version"] = 0
        item["captioned_at"] = 0
        item["updated_at"] = int(time.time())
        self._imagebed_import_state["caption_paused"] = True
        self._save_imagebed_import_state()

    def _finalize_captioned_imagebed_item(
        self,
        item: dict[str, Any],
        rel_path: str,
    ) -> tuple[dict[str, Any], str]:
        if (
            self._library_source_for_rel_path(rel_path, item)
            != IMAGEBED_LIBRARY_SOURCE
            or not rel_path.startswith(f"files/{IMAGEBED_IMPORT_PENDING_FOLDER}/")
        ):
            return item, rel_path
        source_path = self._abs_plugin_data_path(rel_path)
        target_rel_path = self._unique_upload_rel_path(
            IMAGEBED_IMPORT_LIBRARY_FOLDER,
            source_path.name,
        )
        target_path = self._abs_plugin_data_path(target_rel_path)
        target_path.parent.mkdir(parents=True, exist_ok=True)
        try:
            source_path.replace(target_path)
        except OSError:
            shutil.copyfile(source_path, target_path)
            source_path.unlink()
        stat = target_path.stat()
        old_id = str(item.get("id") or self._image_id(rel_path))
        new_id = self._image_id(target_rel_path)
        images = self._index.setdefault("images", {})
        if isinstance(images, dict):
            images.pop(old_id, None)
            images.pop(self._image_id(rel_path), None)
        item["id"] = new_id
        item["rel_path"] = target_rel_path
        item["filename"] = target_path.name
        item["library_source"] = IMAGEBED_LIBRARY_SOURCE
        item["size"] = stat.st_size
        item["mtime"] = int(stat.st_mtime)
        item["imagebed_finalized_at"] = int(time.time())
        if isinstance(images, dict):
            images[new_id] = item
        marker = str(item.get("imagebed_object_marker") or "")
        known = self._imagebed_import_state.get("known_remote_objects", {})
        if marker and isinstance(known, dict) and marker in known:
            record = known.get(marker)
            if isinstance(record, dict):
                record["status"] = "captioned"
                record["updated_at"] = int(time.time())
        self._save_imagebed_import_state()
        return item, target_rel_path

    def _refresh_caption_progress_after_imagebed_pending_change(self) -> None:
        pending_count = len(self._pending_caption_rel_paths())
        running_count = self._running_caption_count()
        paused_count = self._imagebed_pending_count() if self._imagebed_caption_paused() else 0
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
            self._set_caption_progress(
                status="pending",
                total=max(completed + failed + pending_count, pending_count),
                remaining=pending_count,
                current_image="",
            )
            return
        if paused_count:
            self._set_caption_progress(
                status="pending",
                total=completed + failed + paused_count,
                remaining=paused_count,
                current_image="",
                message="Imagebed import tag generation paused.",
                error_detail="",
                error_image="",
                error_message="",
                error_source="",
            )

    def _record_imagebed_import_error(
        self,
        message: str,
        detail: str,
        trigger: str,
    ) -> None:
        now = int(time.time())
        raw = f"{trigger}\n{message}\n{detail}\n{now}"
        self._imagebed_import_state["last_error"] = {
            "id": hashlib.sha1(raw.encode("utf-8")).hexdigest()[:16],
            "message": message,
            "detail": detail or message,
            "trigger": trigger,
            "occurred_at": now,
            "acknowledged": False,
        }

    def _ack_imagebed_import_error(self, error_id: str = "") -> dict[str, Any]:
        last_error = self._imagebed_import_state.get("last_error", {})
        if isinstance(last_error, dict):
            if not error_id or str(last_error.get("id") or "") == str(error_id):
                last_error["acknowledged"] = True
                self._save_imagebed_import_state()
        return self._imagebed_import_status_snapshot()

    def _start_imagebed_sync_task(self) -> None:
        if self._imagebed_sync_task and not self._imagebed_sync_task.done():
            return
        try:
            self._imagebed_sync_task = asyncio.create_task(
                self._imagebed_sync_loop()
            )
        except RuntimeError:
            logger.warning(
                "astrbot_plugin_smart_imagechat_hub: failed to start imagebed sync scheduler; no running event loop."
            )

    def _restart_imagebed_sync_task(self) -> None:
        if self._imagebed_sync_task and not self._imagebed_sync_task.done():
            self._imagebed_sync_task.cancel()
        try:
            asyncio.get_running_loop()
        except RuntimeError:
            return
        self._imagebed_sync_task = asyncio.create_task(self._imagebed_sync_loop())

    async def _imagebed_sync_loop(self) -> None:
        while True:
            cfg = self._imagebed_import_config()
            if not cfg.get("scheduled_enabled"):
                await asyncio.sleep(3600)
                continue
            delay = self._seconds_until_backup_time(str(cfg.get("scheduled_time") or "03:30"))
            await asyncio.sleep(delay)
            try:
                await self._sync_library_if_changed(caption_mode="none")
                if self._imagebed_import_task and not self._imagebed_import_task.done():
                    continue
                await self._start_imagebed_import(trigger="scheduled")
                task = self._imagebed_import_task
                if task:
                    await task
            except asyncio.CancelledError:
                raise
            except Exception as exc:
                detail = traceback.format_exc()
                logger.warning(
                    "astrbot_plugin_smart_imagechat_hub: scheduled imagebed sync failed: %s",
                    exc,
                    exc_info=True,
                )
                async with self._lock:
                    self._record_imagebed_import_error(
                        "图床定时同步失败。",
                        detail,
                        "scheduled",
                    )
                    self._save_imagebed_import_state()
                await asyncio.sleep(300)
