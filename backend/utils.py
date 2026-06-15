from .common import (
    Any,
    logger,
    PENDING_SEND_IMAGE_STYLE_CLEANUP_EXTRA_KEY,
    PILImage,
    compress_image,
    Path,
    SUPPORTED_IMAGE_EXTS,
    USER_SEARCH_CONFIG_KEY,
    asyncio,
    hashlib,
    json,
    re,
    tempfile,
    uuid,
)


class UtilityMixin:
    async def _prepare_caption_image_input(
        self,
        image_path: Path,
    ) -> tuple[str, list[Path]]:
        prepared = str(image_path)
        cleanup_paths: list[Path] = []
        if not image_path.is_file():
            return prepared, cleanup_paths

        suffix = image_path.suffix.lower()
        if suffix not in {".jpg", ".jpeg", ".png"}:
            if PILImage is None:
                return prepared, cleanup_paths
            try:
                with PILImage.open(image_path) as img:
                    frame = img.convert("RGB")
                    temp_dir = Path(tempfile.gettempdir())
                    temp_dir.mkdir(parents=True, exist_ok=True)
                    temp_path = (
                        temp_dir
                        / f"smart_imagechat_caption_{uuid.uuid4().hex}.jpg"
                    )
                    frame.save(temp_path, "JPEG", quality=92, optimize=True)
                    frame.close()
                    cleanup_paths.append(temp_path)
                    prepared = str(temp_path)
            except Exception:
                return prepared, cleanup_paths

        if compress_image is None:
            return prepared, cleanup_paths
        try:
            compressed = await compress_image(
                prepared,
                max_size=1280,
                quality=95,
            )
            if compressed and compressed != prepared:
                compressed_path = Path(compressed)
                if compressed_path.is_file():
                    cleanup_paths.append(compressed_path)
                    prepared = compressed
        except Exception:
            return prepared, cleanup_paths
        return prepared, cleanup_paths

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

    def _is_gif_file_content(self, image_path: Path) -> bool:
        try:
            with image_path.open("rb") as f:
                return f.read(6) in {b"GIF87a", b"GIF89a"}
        except Exception:
            return False

    def _should_convert_send_image_to_gif(
        self,
        image_path: Path,
        tags: list[str] | None,
        *,
        ignore_tag_gate: bool = False,
    ) -> bool:
        cfg = self._send_image_style_config()
        if not cfg.get("enabled"):
            return False
        if not image_path.is_file():
            return False
        suffix = image_path.suffix.lower()
        if (
            suffix == ".gif"
            or suffix not in SUPPORTED_IMAGE_EXTS
            or self._is_gif_file_content(image_path)
        ):
            return False
        if cfg.get("meme_tag_only") and not ignore_tag_gate:
            return "表情包" in {str(tag or "").strip() for tag in tags or []}
        return True

    async def _prepare_send_image_path(
        self,
        image_path: Path,
        tags: list[str] | None = None,
        *,
        ignore_tag_gate: bool = False,
    ) -> tuple[Path, list[Path]]:
        cleanup_paths: list[Path] = []
        if not self._should_convert_send_image_to_gif(
            image_path,
            tags,
            ignore_tag_gate=ignore_tag_gate,
        ):
            return image_path, cleanup_paths
        if PILImage is None:
            logger.warning(
                "astrbot_plugin_smart_imagechat_hub: Pillow is unavailable; skipped send image GIF conversion."
            )
            return image_path, cleanup_paths
        try:
            converted = await asyncio.to_thread(
                self._convert_static_image_to_one_frame_gif,
                image_path,
            )
        except Exception as exc:
            logger.warning(
                "astrbot_plugin_smart_imagechat_hub: failed to convert send image to GIF, using original: %s",
                exc,
                exc_info=True,
            )
            return image_path, cleanup_paths
        if converted != image_path:
            cleanup_paths.append(converted)
        return converted, cleanup_paths

    def _convert_static_image_to_one_frame_gif(self, source: Path) -> Path:
        if PILImage is None:
            return source
        temp_dir = self.data_dir / "send_image_style_cache"
        temp_dir.mkdir(parents=True, exist_ok=True)
        target = temp_dir / f"send_image_style_{uuid.uuid4().hex}.gif"
        try:
            with PILImage.open(source) as img:
                img.seek(0)
                frame = img.copy()
            try:
                if frame.mode in {"RGBA", "LA"} or (
                    frame.mode == "P" and "transparency" in frame.info
                ):
                    rgba = frame.convert("RGBA")
                    background = PILImage.new("RGBA", rgba.size, (255, 255, 255, 255))
                    background.alpha_composite(rgba)
                    frame.close()
                    rgba.close()
                    frame = background.convert("RGB")
                    background.close()
                elif frame.mode != "RGB":
                    converted = frame.convert("RGB")
                    frame.close()
                    frame = converted
                frame.save(target, format="GIF", save_all=False)
            finally:
                frame.close()
        except Exception:
            target.unlink(missing_ok=True)
            raise
        return target

    def _cleanup_temp_paths(self, paths: list[Path]) -> None:
        for path in paths:
            try:
                path.unlink(missing_ok=True)
            except Exception as exc:
                logger.debug(
                    "astrbot_plugin_smart_imagechat_hub: failed to cleanup temp file %s: %s",
                    path,
                    exc,
                )

    def _defer_send_image_style_cleanup(
        self,
        event: Any,
        cleanup_paths: list[Path],
    ) -> list[Path]:
        if not cleanup_paths:
            return []
        cleanup_paths = self._untracked_send_image_style_paths(event, cleanup_paths)
        if not cleanup_paths:
            return []
        get_extra = getattr(event, "get_extra", None)
        set_extra = getattr(event, "set_extra", None)
        if not callable(get_extra) or not callable(set_extra):
            return cleanup_paths
        pending = get_extra(PENDING_SEND_IMAGE_STYLE_CLEANUP_EXTRA_KEY)
        if not isinstance(pending, list):
            pending = []
        existing = {str(item) for item in pending}
        for path in cleanup_paths:
            path_text = str(path)
            if path_text not in existing:
                pending.append(path_text)
                existing.add(path_text)
        set_extra(PENDING_SEND_IMAGE_STYLE_CLEANUP_EXTRA_KEY, pending)
        return []

    def _cleanup_deferred_send_image_style_paths(self, event: Any) -> None:
        get_extra = getattr(event, "get_extra", None)
        set_extra = getattr(event, "set_extra", None)
        if not callable(get_extra) or not callable(set_extra):
            return
        pending = get_extra(PENDING_SEND_IMAGE_STYLE_CLEANUP_EXTRA_KEY)
        if not isinstance(pending, list):
            return
        set_extra(PENDING_SEND_IMAGE_STYLE_CLEANUP_EXTRA_KEY, None)
        self._cleanup_temp_paths([Path(str(path)) for path in pending if str(path)])

    def _cleanup_or_track_send_image_style_paths(
        self,
        event: Any,
        cleanup_paths: list[Path],
    ) -> None:
        self._cleanup_temp_paths(
            self._defer_send_image_style_cleanup(event, cleanup_paths)
        )

    def _untracked_send_image_style_paths(
        self,
        event: Any,
        cleanup_paths: list[Path],
    ) -> list[Path]:
        if not cleanup_paths:
            return []
        track_temp_file = getattr(event, "track_temporary_local_file", None)
        if not callable(track_temp_file):
            return cleanup_paths
        untracked: list[Path] = []
        for path in cleanup_paths:
            try:
                track_temp_file(str(path))
            except Exception as exc:
                logger.debug(
                    "astrbot_plugin_smart_imagechat_hub: failed to track temp send image %s: %s",
                    path,
                    exc,
                )
                untracked.append(path)
        return untracked

    def _tags_for_library_path(self, image_path: Path) -> list[str]:
        try:
            rel_path = image_path.resolve().relative_to(self.data_dir.resolve()).as_posix()
        except ValueError:
            return []
        item = self._index_image_by_id(self._image_id(rel_path))
        return self._tags_from_item(item) if item else []

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
