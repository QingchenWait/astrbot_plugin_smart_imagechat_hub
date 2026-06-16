import asyncio
import base64
import hashlib
import json
import mimetypes
import random
import re
import shutil
import tempfile
import traceback
import uuid
import weakref
import time
import zipfile
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any
from urllib.parse import unquote, urlparse

import aiohttp
from astrbot.api import logger, star
from astrbot.api.event import AstrMessageEvent
from astrbot.api.event import filter
from astrbot.api.event import MessageEventResult
from astrbot.api.message_components import Image, Plain
from astrbot.core.agent.message import TextPart
from astrbot.core.config.astrbot_config import AstrBotConfig
from quart import Response, jsonify, request, send_file

try:
    from astrbot.core.utils.media_utils import compress_image
except Exception:  # pragma: no cover - depends on AstrBot runtime version
    compress_image = None

try:
    from PIL import Image as PILImage
except Exception:  # pragma: no cover - Pillow is provided by AstrBot
    PILImage = None


PLUGIN_NAME = "astrbot_plugin_smart_imagechat_hub"
PLUGIN_VERSION = "v2.8.6"
SKIP_PROACTIVE_EMOJI_EXTRA_KEY = "smart_imagesender_skip_proactive_emoji"
PENDING_PROACTIVE_EMOJI_EXTRA_KEY = "smart_imagesender_pending_proactive_emoji"
PROACTIVE_EMOJI_DECISION_EXTRA_KEY = "smart_imagesender_proactive_emoji_decision"
PROACTIVE_EMOJI_INTERNAL_LLM_EXTRA_KEY = (
    "smart_imagesender_proactive_emoji_internal_llm"
)
PROACTIVE_EMOJI_TASK_EXTRA_KEY = "smart_imagesender_proactive_emoji_task"
PROACTIVE_EMOJI_FAST_FALLBACK_EXTRA_KEY = (
    "smart_imagesender_proactive_emoji_fast_fallback"
)
PENDING_MEME_COMBAT_IMAGE_EXTRA_KEY = "smart_imagesender_pending_meme_combat_image"
PENDING_SEND_IMAGE_STYLE_CLEANUP_EXTRA_KEY = (
    "smart_imagesender_pending_send_image_style_cleanup"
)
USER_SEARCH_EXPLICIT_WAKE_EXTRA_KEY = "smart_imagesender_explicit_user_search_wake"
USER_SEARCH_CONFIG_KEY = "user_search_flow"
AUTO_COLLECTION_CONFIG_KEY = "auto_image_collection"
SCHEDULED_BACKUP_CONFIG_KEY = "scheduled_backup"
SEND_IMAGE_STYLE_CONFIG_KEY = "send_image_style"
MODEL_FALLBACK_CONFIG_KEY = "model_fallback_options"
PAGE_LIBRARY_DEFAULT_VIEW_MODE_CONFIG_KEY = "page_library_default_view_mode"
LIBRARY_BUILDER_CONFIG_KEY = "library_builder"
IMAGE_FILES_CONFIG_KEY = "library_builder.image_files"
IMAGE_TAGS_CONFIG_KEY = "image_tags"
GLOBAL_TAGS_CONFIG_KEY = "library_builder.global_tags"
PROGRESS_LINK_CONFIG_KEY = "library_builder.empty_config_for_hint_only"
TAG_CATEGORY_CONFIG_KEY = "caption_tag_category_settings"
DEFAULT_CAPTION_PROVIDER_CONFIG_KEY = "default_image_caption_provider_id"
PROACTIVE_EMOJI_CONFIG_KEY = "proactive_emoji_reply"
MEME_COMBAT_CONFIG_KEY = "meme_combat"
LEGACY_IMAGE_TAGS_CONFIG_KEY = "manual_tags"
CAPTION_PROMPT_VERSION = 2
BACKUP_FORMAT_VERSION = 1
SCHEDULED_BACKUP_FOLDER = "scheduled_backups"
SUPPORTED_IMAGE_EXTS = {".jpg", ".jpeg", ".png", ".gif", ".webp", ".bmp"}
IMAGE_CENTER_PAGE_NAME = "image-center-page"
PROGRESS_PAGE_PATH = f"/main/plugin-page/{PLUGIN_NAME}/{IMAGE_CENTER_PAGE_NAME}"
CONFIG_PAGE_PATH = f"/main/extension?open_config={PLUGIN_NAME}"
LIBRARY_WATCH_INTERVAL_SECONDS = 2.0
MANUAL_LIBRARY_SOURCE = "manual_upload"
COLLECTED_LIBRARY_SOURCE = "auto_collected"
EXTERNAL_LIBRARY_SOURCE = "external_imported"
IMAGEBED_LIBRARY_SOURCE = "imagebed_imported"
PENDING_COLLECTION_FOLDER = "auto_collection/pending_pool"
COLLECTED_COLLECTION_FOLDER = "auto_collection/solidified_library"
EXTERNAL_IMPORT_FOLDER = "external_import/imported_library"
IMAGEBED_IMPORT_CONFIG_KEY = "imagebed_import"
IMAGEBED_IMPORT_PENDING_FOLDER = "imagebed_import/pending_pool"
IMAGEBED_IMPORT_LIBRARY_FOLDER = "imagebed_import/imported_library"
IMAGEBED_IMPORT_THUMBNAIL_FOLDER = "imagebed_import/thumbnails"
AUTO_COLLECTION_POOL_FILENAME = "auto_collection_pool.json"
AUTO_COLLECTION_DISCARDED_FILENAME = "auto_collection_discarded.json"
EXTERNAL_IMPORT_STATE_FILENAME = "external_import_state.json"
EXTERNAL_IMPORT_THUMBNAIL_FOLDER = "external_import/thumbnails"
IMAGEBED_IMPORT_STATE_FILENAME = "imagebed_import_state.json"
IMAGEBED_IMPORT_DISCARDED_FILENAME = "imagebed_import_discarded.json"
_AUTO_COLLECTION_PLUGIN_REF: Any | None = None


class CaptionGenerationError(RuntimeError):
    def __init__(self, message: str, detail: str = "") -> None:
        super().__init__(message)
        self.detail = detail or message


class AutoCollectionImageCandidate:
    __slots__ = ("image", "strict_confirmed")

    def __init__(self, image: Any, strict_confirmed: bool = False) -> None:
        self.image = image
        self.strict_confirmed = bool(strict_confirmed)


class AutoCollectionRawImage:
    __slots__ = ("file", "path", "url")

    def __init__(self, *, url: str = "", file: str = "", path: str = "") -> None:
        self.url = str(url or "").strip()
        self.file = str(file or "").strip()
        self.path = str(path or "").strip()

    async def convert_to_file_path(self) -> str:
        return ""


def set_auto_collection_plugin(plugin: Any) -> None:
    global _AUTO_COLLECTION_PLUGIN_REF  # noqa: PLW0603
    _AUTO_COLLECTION_PLUGIN_REF = weakref.ref(plugin)


def clear_auto_collection_plugin(plugin: Any) -> None:
    global _AUTO_COLLECTION_PLUGIN_REF  # noqa: PLW0603
    plugin_ref = _AUTO_COLLECTION_PLUGIN_REF
    current = plugin_ref() if callable(plugin_ref) else None
    if current is plugin:
        _AUTO_COLLECTION_PLUGIN_REF = None


def get_auto_collection_plugin() -> Any | None:
    plugin_ref = _AUTO_COLLECTION_PLUGIN_REF
    return plugin_ref() if callable(plugin_ref) else None


def _qq_id_candidates(value: Any, *, split_composite: bool = True) -> set[str]:
    text = str(value or "").strip()
    if not text:
        return set()
    candidates = {text}
    digit_parts = re.findall(r"\d+", text)
    if text.isdigit() or split_composite or len(digit_parts) == 1:
        candidates.update(part for part in digit_parts if len(part) >= 5)
    return candidates


def _normalize_qq_id_list(raw: Any) -> list[str]:
    if isinstance(raw, list):
        items = raw
    elif isinstance(raw, str):
        items = re.split(r"[\n,，、;；\s]+", raw)
    else:
        items = [raw]

    qq_ids: list[str] = []
    seen: set[str] = set()
    for item in items:
        text = str(item or "").strip()
        if not text:
            continue
        candidates = re.findall(r"\d+", text) or [text]
        for candidate in candidates:
            qq_id = str(candidate or "").strip()
            if qq_id and qq_id not in seen:
                seen.add(qq_id)
                qq_ids.append(qq_id)
    return qq_ids


def _to_bool_compat(value: Any, default: bool = False) -> bool:
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


def normalize_auto_collection_non_meme_filter_strategy(raw: Any) -> str:
    raw = raw if isinstance(raw, dict) else {}
    strategy = str(raw.get("non_meme_filter_strategy") or "").strip().lower()
    if strategy in {"none", "loose", "strict"}:
        return strategy
    return (
        "loose"
        if _to_bool_compat(raw.get("filter_obvious_non_meme_images"), True)
        else "none"
    )


def _raw_sender_user_id(raw_message: Any) -> Any:
    if isinstance(raw_message, dict):
        if raw_message.get("user_id") is not None:
            return raw_message.get("user_id")
        if raw_message.get("sender_id") is not None:
            return raw_message.get("sender_id")
        sender = raw_message.get("sender")
        if isinstance(sender, dict):
            return sender.get("user_id") or sender.get("id")
    sender = getattr(raw_message, "sender", None)
    return getattr(sender, "user_id", None) or getattr(sender, "id", None)


def _event_sender_qq_candidates(event: AstrMessageEvent) -> set[str]:
    message_obj = getattr(event, "message_obj", None)
    sender = getattr(message_obj, "sender", None)
    raw_message = getattr(message_obj, "raw_message", None)

    authoritative: set[str] = set()
    for value in (
        getattr(sender, "user_id", None),
        getattr(sender, "id", None),
        _raw_sender_user_id(raw_message),
    ):
        authoritative.update(_qq_id_candidates(value))

    candidates = set(authoritative)
    sender_id = event.get_sender_id()
    candidates.update(
        _qq_id_candidates(sender_id, split_composite=not bool(authoritative))
    )
    return candidates


def _raw_message_segments(event: AstrMessageEvent) -> list[Any]:
    message_obj = getattr(event, "message_obj", None)
    raw_message = getattr(message_obj, "raw_message", None)
    candidates = [
        getattr(raw_message, "message", None),
        raw_message.get("message") if isinstance(raw_message, dict) else None,
        raw_message,
    ]
    for candidate in candidates:
        if isinstance(candidate, (list, tuple)):
            return list(candidate)
    return []


def _raw_segment_type(segment: Any) -> str:
    if isinstance(segment, dict):
        return str(segment.get("type") or "").strip().lower()
    return str(getattr(segment, "type", "") or "").strip().lower()


def _raw_segment_data(segment: Any) -> Any:
    if isinstance(segment, dict):
        data = segment.get("data")
        return data if data is not None else {}
    return getattr(segment, "data", None) or {}


def _raw_data_value(data: Any, key: str) -> Any:
    if isinstance(data, dict):
        return data.get(key)
    return getattr(data, key, None)


def _raw_text_value(data: Any, keys: tuple[str, ...]) -> str:
    for key in keys:
        value = _raw_data_value(data, key)
        if value is None:
            continue
        text = str(value or "").strip()
        if text:
            return text
    return ""


def _raw_data_has_any(data: Any, keys: tuple[str, ...]) -> bool:
    for key in keys:
        value = _raw_data_value(data, key)
        if value is not None and str(value or "").strip():
            return True
    return False


def _strict_meme_url(data: Any) -> str:
    urls = _strict_meme_urls(data)
    return urls[0] if urls else ""


def _strict_meme_urls(data: Any) -> list[str]:
    urls: list[str] = []
    for key in (
        "url",
        "cdnurl",
        "cdn_url",
        "raw_url",
        "origin_url",
        "original_url",
        "thumb",
        "thumb_url",
    ):
        text = _raw_text_value(data, (key,))
        if text.startswith(("http://", "https://")):
            urls.append(text)
    return urls


def _raw_image_segment_is_explicit_meme(data: Any) -> bool:
    sub_type = _raw_text_value(data, ("sub_type", "subType"))
    if sub_type == "1":
        return True
    summary = _raw_text_value(data, ("summary",))
    lowered_summary = summary.lower()
    if any(token in lowered_summary for token in ("表情", "emoji", "sticker")):
        return True
    if _raw_data_has_any(
        data,
        ("emoji_id", "emojiId", "emoji_package_id", "emojiPackageId"),
    ):
        return True
    return any(
        "vip.qq.com/club/item/parcel" in url.lower()
        or "gxh.vip.qq.com" in url.lower()
        for url in _strict_meme_urls(data)
    )


def _auto_collection_signature_values(value: Any) -> set[str]:
    text = str(value or "").strip()
    if not text or text.startswith("base64://"):
        return set()
    values = {text, unquote(text)}
    parsed = urlparse(text)
    path = unquote(parsed.path or text)
    name = Path(path).name
    if len(name) >= 12:
        values.add(name)
    return {item for item in values if item}


def _image_component_signature_values(image: Any) -> set[str]:
    values: set[str] = set()
    for attr in ("file", "url", "path"):
        values.update(_auto_collection_signature_values(getattr(image, attr, None)))
    return values


def _raw_image_signature_values(data: Any) -> set[str]:
    values: set[str] = set()
    for key in (
        "file",
        "url",
        "path",
        "file_id",
        "fileId",
        "file_unique",
        "fileUnique",
    ):
        values.update(_auto_collection_signature_values(_raw_data_value(data, key)))
    return values


def _match_strict_raw_image_component(
    data: Any,
    images: tuple[Image, ...],
    used_indexes: set[int],
) -> int:
    raw_values = _raw_image_signature_values(data)
    if not raw_values:
        return -1
    for index, image in enumerate(images):
        if index in used_indexes:
            continue
        if raw_values & _image_component_signature_values(image):
            return index
    return -1


def auto_collection_strict_image_candidates(
    event: AstrMessageEvent,
    images: tuple[Image, ...],
) -> tuple[AutoCollectionImageCandidate, ...]:
    segments = _raw_message_segments(event)
    if not segments:
        return ()

    candidates: list[AutoCollectionImageCandidate] = []
    used_image_indexes: set[int] = set()
    raw_image_index = 0
    raw_mface_count = 0
    for segment in segments:
        segment_type = _raw_segment_type(segment)
        data = _raw_segment_data(segment)
        if segment_type == "image":
            if _raw_image_segment_is_explicit_meme(data):
                image_index = _match_strict_raw_image_component(
                    data,
                    images,
                    used_image_indexes,
                )
                if image_index < 0 and raw_image_index < len(images):
                    image_index = raw_image_index
                if image_index >= 0 and image_index not in used_image_indexes:
                    candidates.append(
                        AutoCollectionImageCandidate(
                            images[image_index],
                            strict_confirmed=True,
                        )
                    )
                    used_image_indexes.add(image_index)
            raw_image_index += 1
            continue
        if segment_type not in {"mface", "marketface"}:
            continue
        if raw_mface_count >= AUTO_COLLECTION_STRICT_MFACE_MAX_IMAGES:
            continue
        for url in _strict_meme_urls(data):
            if raw_mface_count >= AUTO_COLLECTION_STRICT_MFACE_MAX_IMAGES:
                break
            candidates.append(
                AutoCollectionImageCandidate(
                    AutoCollectionRawImage(url=url, file=url),
                    strict_confirmed=True,
                )
            )
            raw_mface_count += 1
    return tuple(candidates)


AUTO_COLLECTION_QUEUE_MAXSIZE = 24
AUTO_COLLECTION_STRICT_MFACE_MAX_IMAGES = 3
AUTO_COLLECTION_IMAGE_CONVERT_TIMEOUT_SECONDS = 8
AUTO_COLLECTION_DOWNLOAD_CHUNK_BYTES = 64 * 1024
PROGRESS_PAGE_CONFIG_VALUE = (
    "/#/plugin-page/astrbot_plugin_smart_imagechat_hub/image-center-page"
)
TAG_CATEGORY_PRESETS = {
    "image_type": "图像类别",
    "person_features": "人物特征",
    "body_shape": "身材",
    "emotion": "情绪",
    "action": "动作",
    "image_text": "图片中的文本",
}
TAG_CATEGORY_LABEL_TO_KEY = {
    label: key for key, label in TAG_CATEGORY_PRESETS.items()
}
SEARCH_CANDIDATE_LIMIT = 10
SEARCH_SELECTION_POOL_SIZE = 3
WAKE_FILTER_IMAGE_REQUEST_HINTS = (
    "表情包",
    "表情",
    "照片",
    "图片",
    "美图",
    "梗图",
    "头像",
    "壁纸",
    "图",
)
SEARCH_QUERY_STOPWORDS = {
    "来",
    "来点",
    "来个",
    "来一张",
    "来几张",
    "给我",
    "帮我",
    "看看",
    "看看吧",
    "有",
    "有没有",
    "吗",
    "嘛",
    "呢",
    "啊",
    "呀",
    "吧",
    "呗",
    "请",
    "求",
    "找",
    "找找",
    "发",
    "发个",
    "发一张",
    "一张",
    "一张图",
    "一张照片",
    "一张表情包",
    "一张美图",
    "图片",
    "照片",
    "表情包",
    "美图",
    "图",
    "图像",
    "这个",
    "那个",
    "这种",
    "那种",
    "一些",
    "一点",
    "一点点",
    "一下",
    "都行",
    "可以",
    "想要",
    "我要",
    "我想",
    "请给",
    "整点",
    "安排",
    "搞点",
    "点",
    "张",
    "个",
}


def _is_explicit_user_search_wake(event: AstrMessageEvent) -> bool:
    return bool(
        event.get_extra(USER_SEARCH_EXPLICIT_WAKE_EXTRA_KEY, False)
        or event.is_private_chat()
        or event.is_at_or_wake_command
    )


def _message_has_config_wake_prefix(
    event: AstrMessageEvent,
    cfg: AstrBotConfig,
) -> bool:
    message = (event.get_message_str() or "").strip()
    if not message:
        return False
    cfg_get = getattr(cfg, "get", None)
    raw_prefixes = cfg_get("wake_prefix", []) if callable(cfg_get) else []
    if isinstance(raw_prefixes, str):
        raw_prefixes = [raw_prefixes]
    if not isinstance(raw_prefixes, list):
        return False

    for raw_prefix in raw_prefixes:
        wake_prefix = str(raw_prefix or "").strip()
        if not wake_prefix:
            continue
        if message.startswith(wake_prefix):
            return True
        if len(wake_prefix) < 2:
            continue
        if not re.search(r"[A-Za-z0-9_\u4e00-\u9fff]", wake_prefix):
            continue
        if re.fullmatch(r"[A-Za-z0-9_]+", wake_prefix):
            pattern = rf"(?<![A-Za-z0-9_]){re.escape(wake_prefix)}(?![A-Za-z0-9_])"
            if re.search(pattern, message, re.I):
                return True
        elif wake_prefix in message:
            return True
    return False


def _message_has_image_request_hint(event: AstrMessageEvent) -> bool:
    message = (event.get_message_str() or "").strip()
    return any(hint in message for hint in WAKE_FILTER_IMAGE_REQUEST_HINTS)


class WakeImageRequestFilter(filter.CustomFilter):
    """Only activate the plugin when this is a wake event."""

    def filter(self, event: AstrMessageEvent, cfg: AstrBotConfig) -> bool:
        # `is_wake_up()` can be true because another handler already woke the
        # event. This flow must only run when the current message explicitly
        # wakes the bot, including direct private chats.
        explicit_wake = _is_explicit_user_search_wake(event)
        if not explicit_wake and _message_has_image_request_hint(event):
            explicit_wake = _message_has_config_wake_prefix(event, cfg)
        if explicit_wake:
            event.set_extra(USER_SEARCH_EXPLICIT_WAKE_EXTRA_KEY, True)
        return explicit_wake


class AutoImageCollectionMessageFilter(filter.CustomFilter):
    """Only activate the collector for incoming group messages that carry images."""

    def filter(self, event: AstrMessageEvent, cfg: AstrBotConfig) -> bool:
        plugin = get_auto_collection_plugin()
        if plugin is None:
            return False

        raw_cfg = plugin.config.get(AUTO_COLLECTION_CONFIG_KEY, {})
        if not isinstance(raw_cfg, dict):
            return False
        collection_cfg = {
            "enabled": bool(raw_cfg.get("enabled", False)),
            "source_groups": [
                str(item or "").strip()
                for item in (
                    raw_cfg.get("source_groups", [])
                    if isinstance(raw_cfg.get("source_groups", []), list)
                    else re.split(r"[\n,，、;； ]+", str(raw_cfg.get("source_groups", "")))
                )
                if str(item or "").strip()
            ],
            "non_meme_filter_strategy": (
                normalize_auto_collection_non_meme_filter_strategy(raw_cfg)
            ),
        }
        if not collection_cfg["enabled"]:
            return False

        group_id = str(event.get_group_id() or "").strip()
        if not group_id:
            return False
        if group_id not in set(collection_cfg["source_groups"]):
            return False

        sender_id = str(event.get_sender_id() or "").strip()
        self_id = str(event.get_self_id() or "").strip()
        if sender_id and self_id and sender_id == self_id:
            return False

        images = tuple(comp for comp in event.get_messages() if isinstance(comp, Image))
        strategy = collection_cfg["non_meme_filter_strategy"]
        if strategy == "strict":
            collection_images = auto_collection_strict_image_candidates(event, images)
        else:
            collection_images = tuple(
                AutoCollectionImageCandidate(image, strict_confirmed=False)
                for image in images
            )
        if not collection_images:
            return False

        ignored_sender_ids = set(
            _normalize_qq_id_list(raw_cfg.get("ignored_sender_ids", []))
        )
        if ignored_sender_ids and (
            _event_sender_qq_candidates(event) & ignored_sender_ids
        ):
            return False

        if not plugin._auto_collection_has_fast_capacity(
            bool(raw_cfg.get("auto_accept", False)),
        ):
            return False
        plugin._enqueue_auto_collection(
            group_id,
            sender_id,
            collection_images,
            plugin._to_int(raw_cfg.get("max_file_size_kb"), 1024),
            bool(raw_cfg.get("auto_accept", False)),
            strategy,
        )
        return False


class MemeCombatMessageFilter(filter.CustomFilter):
    """Observe group image traffic without activating the plugin handler."""

    def filter(self, event: AstrMessageEvent, cfg: AstrBotConfig) -> bool:
        plugin = get_auto_collection_plugin()
        if plugin is None:
            return False

        raw_cfg = plugin.config.get(MEME_COMBAT_CONFIG_KEY, {})
        cfg = plugin._normalize_meme_combat_config(raw_cfg)
        if not cfg.get("enabled"):
            return False

        group_id = str(event.get_group_id() or "").strip()
        if not group_id:
            return False

        images = tuple(comp for comp in event.get_messages() if isinstance(comp, Image))
        group_state = getattr(plugin, "_meme_combat_groups", {})
        state = group_state.get(group_id) if isinstance(group_state, dict) else None
        has_active_streak = isinstance(state, dict) and bool(state.get("streak"))
        if not images and not has_active_streak:
            return False

        plugin._enqueue_meme_combat_event(event)
        return False
