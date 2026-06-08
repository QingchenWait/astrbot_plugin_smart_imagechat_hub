from .common import (
    Any,
    Path,
    SUPPORTED_IMAGE_EXTS,
    USER_SEARCH_CONFIG_KEY,
    asyncio,
    hashlib,
    json,
    re,
)


class UtilityMixin:
    def _loads_json_object(self, text: str) -> Any:
        text = (text or "").strip()
        if not text:
            return None
        try:
            return json.loads(text)
        except json.JSONDecodeError:
            pass

        fenced = re.search(r"```(?:json)?\s*(.*?)\s*```", text, re.S | re.I)
        if fenced:
            try:
                return json.loads(fenced.group(1))
            except json.JSONDecodeError:
                pass

        start_candidates = [pos for pos in (text.find("{"), text.find("[")) if pos >= 0]
        if not start_candidates:
            return None
        start = min(start_candidates)
        end = max(text.rfind("}"), text.rfind("]"))
        if end <= start:
            return None
        try:
            return json.loads(text[start : end + 1])
        except json.JSONDecodeError:
            return None

    def _is_allowed_image(self, path: Path) -> bool:
        return path.is_file() and path.suffix.lower() in SUPPORTED_IMAGE_EXTS

    def _abs_plugin_data_path(self, rel_path: str) -> Path:
        root = self.data_dir.resolve()
        path = (root / rel_path).resolve()
        try:
            path.relative_to(root)
        except ValueError:
            raise ValueError(f"invalid plugin data path: {rel_path}")
        return path

    def _norm_rel_path(self, rel_path: Any) -> str:
        if not isinstance(rel_path, str):
            return ""
        rel = rel_path.replace("\\", "/").lstrip("/")
        parts = [part for part in rel.split("/") if part]
        if not parts or any(part in {".", ".."} for part in parts):
            return ""
        return "/".join(parts)

    def _safe_upload_filename(self, filename: str) -> str:
        name = Path(filename.replace("\\", "/")).name.strip()
        if not name or name in {".", ".."}:
            return ""
        safe_chars = []
        for ch in name:
            if ch.isalnum() or ch in {" ", ".", "-", "_", "(", ")", "[", "]"}:
                safe_chars.append(ch)
            else:
                safe_chars.append("_")
        safe_name = "".join(safe_chars).strip(" ._")
        return safe_name or ""

    def _unique_upload_rel_path(self, folder: str, filename: str) -> str:
        base = Path(filename).stem or "image"
        suffix = Path(filename).suffix.lower()
        candidate = f"files/{folder}/{base}{suffix}"
        counter = 1
        while True:
            try:
                path = self._abs_plugin_data_path(candidate)
            except ValueError:
                candidate = f"files/{folder}/image{suffix}"
                path = self._abs_plugin_data_path(candidate)
            if not path.exists():
                return candidate
            counter += 1
            candidate = f"files/{folder}/{base}_{counter}{suffix}"

    def _image_id(self, rel_path: str) -> str:
        return hashlib.sha1(rel_path.encode("utf-8")).hexdigest()[:16]

    def _sha256(self, path: Path) -> str:
        digest = hashlib.sha256()
        with open(path, "rb") as f:
            for chunk in iter(lambda: f.read(1024 * 1024), b""):
                digest.update(chunk)
        return digest.hexdigest()

    def _copy_file_streaming(
        self,
        source: Path,
        target: Path,
        chunk_size: int = 1024 * 1024,
    ) -> None:
        chunk_size = max(int(chunk_size or 0), 64 * 1024)
        with open(source, "rb") as src, open(target, "wb") as dst:
            for chunk in iter(lambda: src.read(chunk_size), b""):
                dst.write(chunk)

    async def _copy_file_streaming_async(
        self,
        source: Path,
        target: Path,
        chunk_size: int = 1024 * 1024,
    ) -> None:
        await asyncio.to_thread(
            self._copy_file_streaming,
            source,
            target,
            chunk_size,
        )

    async def _cached_sha256_async(self, path: Path) -> str:
        stat = path.stat()
        cache_key = str(path.resolve())
        fingerprint = (
            int(stat.st_size),
            int(getattr(stat, "st_mtime_ns", int(stat.st_mtime * 1_000_000_000))),
        )
        cached = self._image_digest_cache.get(cache_key)
        if cached and cached[:2] == fingerprint:
            return cached[2]
        digest = await asyncio.to_thread(self._sha256, path)
        self._image_digest_cache[cache_key] = (*fingerprint, digest)
        return digest

    def _cached_sha256(self, path: Path) -> str:
        stat = path.stat()
        cache_key = str(path.resolve())
        fingerprint = (
            int(stat.st_size),
            int(getattr(stat, "st_mtime_ns", int(stat.st_mtime * 1_000_000_000))),
        )
        cached = self._image_digest_cache.get(cache_key)
        if cached and cached[:2] == fingerprint:
            return cached[2]
        digest = self._sha256(path)
        self._image_digest_cache[cache_key] = (*fingerprint, digest)
        return digest

    def _config_file_folder(self, key_path: str) -> str:
        parts = []
        for part in key_path.split("."):
            cleaned = []
            for ch in part:
                if ("a" <= ch <= "z") or ("A" <= ch <= "Z") or ch.isdigit() or ch in {"-", "_"}:
                    cleaned.append(ch)
                else:
                    cleaned.append("_")
            parts.append("".join(cleaned).strip("_") or "_")
        return "/".join(parts)

    def _cfg_str(self, key: str) -> str:
        value = self._reply_cfg().get(key, self.config.get(key, ""))
        value = str(value if value is not None else "")
        if value:
            return value
        defaults = {
            "empty_library_reply": "图库里还没有可用图片，请先在插件配置里上传图片。",
            "not_found_reply": "图库里暂时没有找到特别合适的图片。",
            "custom_reply": "找到一张比较合适的图。",
        }
        return defaults.get(key, "")

    def _cfg_bool(self, key: str) -> bool:
        defaults = {
            "sync_on_startup": True,
            "user_search_enabled": True,
            "use_custom_reply": True,
            "llm_reply_when_not_found": False,
            "reply_config_migrated": False,
        }
        if key == "user_search_enabled":
            raw_group = self.config.get(USER_SEARCH_CONFIG_KEY, {})
            if isinstance(raw_group, dict) and "enabled" in raw_group:
                value = raw_group.get("enabled")
            else:
                value = self.config.get(key, defaults.get(key, False))
        elif key in {"use_custom_reply", "llm_reply_when_not_found"}:
            value = self._reply_cfg().get(
                key,
                self.config.get(key, defaults.get(key, False)),
            )
        else:
            value = self.config.get(key, defaults.get(key, False))
        if isinstance(value, str):
            return value.strip().lower() in {"1", "true", "yes", "on", "y"}
        return bool(value)

    def _reply_cfg(self) -> dict[str, Any]:
        reply_cfg = self.config.get("reply_after_search", {})
        return reply_cfg if isinstance(reply_cfg, dict) else {}

    def _cfg_float(self, key: str) -> float:
        defaults = {"match_confidence_threshold": 0.45}
        return self._to_float(self.config.get(key), defaults.get(key, 0.0))

    def _clean_text(self, value: Any, default: str = "") -> str:
        text = str(value if value is not None else "").strip()
        return text if text else default

    def _to_bool(self, value: Any, default: bool = False) -> bool:
        if value is None:
            return default
        if isinstance(value, bool):
            return value
        if isinstance(value, str):
            normalized = value.strip().lower()
            if normalized in {"1", "true", "yes", "on", "y"}:
                return True
            if normalized in {"0", "false", "no", "off", "n"}:
                return False
            return default
        return bool(value)

    def _to_float(self, value: Any, default: float) -> float:
        try:
            return float(value)
        except (TypeError, ValueError):
            return default

    def _to_int(self, value: Any, default: int) -> int:
        try:
            return int(value)
        except (TypeError, ValueError):
            return default
