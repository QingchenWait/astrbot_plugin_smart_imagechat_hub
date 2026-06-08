from astrbot.api import logger
from astrbot.api.event import filter
from astrbot.api.star import Context, Star, StarTools, register

from .backend import (
    AutoCollectionMixin,
    BackupRestoreMixin,
    CaptionLibraryMixin,
    ConfigSchemaMixin,
    ExternalImportMixin,
    ImageBedImportMixin,
    ImageManagementMixin,
    LLMContextMixin,
    MemeCombatMixin,
    RetrievalMixin,
    TaggingMixin,
    UtilityMixin,
    WebApiMixin,
)
from .backend.common import (
    AUTO_COLLECTION_DISCARDED_FILENAME,
    AUTO_COLLECTION_POOL_FILENAME,
    Any,
    AstrBotConfig,
    AstrMessageEvent,
    AutoImageCollectionMessageFilter,
    Image,
    MemeCombatMessageFilter,
    EXTERNAL_IMPORT_STATE_FILENAME,
    IMAGEBED_IMPORT_DISCARDED_FILENAME,
    IMAGEBED_IMPORT_STATE_FILENAME,
    PLUGIN_NAME,
    PLUGIN_VERSION,
    Plain,
    SKIP_PROACTIVE_EMOJI_EXTRA_KEY,
    TextPart,
    WakeImageRequestFilter,
    _is_explicit_user_search_wake,
    asyncio,
    clear_auto_collection_plugin,
    set_auto_collection_plugin,
)

@register(
    PLUGIN_NAME,
    "青尘工作室",
    "LLM 驱动的图片回复插件：支持为图片自动添加特征标签，支持通过识别用户意图，智能回复相关的图片。",
    PLUGIN_VERSION,
)
class SmartImageSenderPlugin(
    WebApiMixin,
    LLMContextMixin,
    ConfigSchemaMixin,
    CaptionLibraryMixin,
    BackupRestoreMixin,
    AutoCollectionMixin,
    ExternalImportMixin,
    ImageBedImportMixin,
    ImageManagementMixin,
    MemeCombatMixin,
    RetrievalMixin,
    TaggingMixin,
    UtilityMixin,
    Star,
):
    def __init__(self, context: Context, config: AstrBotConfig | None = None):
        super().__init__(context)
        self.config = config or {}
        set_auto_collection_plugin(self)
        self.data_dir = StarTools.get_data_dir(PLUGIN_NAME)
        self.index_path = self.data_dir / "image_index.json"
        self.collection_pool_path = self.data_dir / AUTO_COLLECTION_POOL_FILENAME
        self.discarded_collection_path = (
            self.data_dir / AUTO_COLLECTION_DISCARDED_FILENAME
        )
        self.external_import_state_path = self.data_dir / EXTERNAL_IMPORT_STATE_FILENAME
        self.imagebed_import_state_path = self.data_dir / IMAGEBED_IMPORT_STATE_FILENAME
        self.imagebed_discarded_path = self.data_dir / IMAGEBED_IMPORT_DISCARDED_FILENAME
        self._lock = asyncio.Lock()
        self._caption_task: asyncio.Task | None = None
        self._caption_cleanup_tasks: set[asyncio.Task] = set()
        self._watch_task: asyncio.Task | None = None
        self._scheduled_backup_task: asyncio.Task | None = None
        self._imagebed_sync_task: asyncio.Task | None = None
        self._model_provider_failure_until: dict[str, float] = {}
        self._auto_collection_queue: asyncio.Queue[dict[str, Any]] | None = None
        self._auto_collection_worker_task: asyncio.Task | None = None
        self._external_import_task: asyncio.Task | None = None
        self._imagebed_import_task: asyncio.Task | None = None
        self._last_library_signature = ""
        self._image_digest_cache: dict[str, tuple[int, int, str]] = {}
        self._index: dict[str, Any] = self._load_index()
        self._collection_pool: dict[str, Any] = self._load_collection_pool()
        self._discarded_collection: dict[str, Any] = self._load_discarded_collection()
        self._external_import_state: dict[str, Any] = self._load_external_import_state()
        self._imagebed_import_state: dict[str, Any] = self._load_imagebed_import_state()
        self._imagebed_discarded: dict[str, Any] = self._load_imagebed_discarded()
        self._init_meme_combat_state()
        self._caption_progress: dict[str, Any] = self._make_caption_progress(
            status="idle",
            message="No image tag generation task has started.",
        )
        self._register_web_apis()

    async def initialize(self) -> None:
        self._migrate_reply_config()
        self._migrate_progress_link_config()
        self._migrate_auto_collection_config()
        self._migrate_meme_combat_config()
        self._migrate_scheduled_backup_config()
        self._migrate_model_fallback_config()
        self._migrate_imagebed_import_config()
        self._ensure_caption_provider_setting_initialized()
        self._refresh_caption_tag_category_schema()
        self._refresh_proactive_emoji_schema()
        self._refresh_meme_combat_schema()
        self._refresh_scheduled_backup_schema()
        self._refresh_model_fallback_schema()
        self._refresh_image_tag_schema()
        self._cleanup_collection_pool()
        self._enforce_scheduled_backup_limit()
        await self._sync_library(caption_mode="background")
        self._start_upload_watch_task()
        self._start_scheduled_backup_task()
        self._start_imagebed_sync_task()
        self._start_auto_collection_worker()

    async def terminate(self) -> None:
        if self._auto_collection_worker_task and not self._auto_collection_worker_task.done():
            self._auto_collection_worker_task.cancel()
            try:
                await self._auto_collection_worker_task
            except asyncio.CancelledError:
                pass
        if self._external_import_task and not self._external_import_task.done():
            self._external_import_task.cancel()
            try:
                await self._external_import_task
            except asyncio.CancelledError:
                pass
        if self._imagebed_import_task and not self._imagebed_import_task.done():
            self._imagebed_import_task.cancel()
            try:
                await self._imagebed_import_task
            except asyncio.CancelledError:
                pass
        if self._imagebed_sync_task and not self._imagebed_sync_task.done():
            self._imagebed_sync_task.cancel()
            try:
                await self._imagebed_sync_task
            except asyncio.CancelledError:
                pass
        await self._wait_meme_combat_tasks()
        if self._scheduled_backup_task and not self._scheduled_backup_task.done():
            self._scheduled_backup_task.cancel()
            try:
                await self._scheduled_backup_task
            except asyncio.CancelledError:
                pass
        if self._watch_task and not self._watch_task.done():
            self._watch_task.cancel()
            try:
                await self._watch_task
            except asyncio.CancelledError:
                pass
        if self._caption_task and not self._caption_task.done():
            self._caption_task.cancel()
            try:
                await self._caption_task
            except asyncio.CancelledError:
                pass
        await self._wait_caption_cleanup_tasks()
        self._save_index()
        self._save_collection_pool()
        self._save_discarded_collection()
        self._save_external_import_state()
        self._save_imagebed_import_state()
        self._save_imagebed_discarded()
        clear_auto_collection_plugin(self)

    @filter.custom_filter(WakeImageRequestFilter, priority=100)
    @filter.event_message_type(filter.EventMessageType.ALL, priority=100)
    async def on_wake_message(self, event: AstrMessageEvent):
        message = (event.get_message_str() or "").strip()
        if not message:
            return
        if not self._cfg_bool("user_search_enabled"):
            return
        if not _is_explicit_user_search_wake(event):
            return
        if not self._has_request_keyword(message):
            return

        event.set_extra(SKIP_PROACTIVE_EMOJI_EXTRA_KEY, True)
        event.should_call_llm(True)

        await self._sync_library(caption_mode="none")
        profile, candidates = self._rank_search_candidates(
            message,
            self._library_candidates(),
        )
        if not candidates:
            yield event.plain_result(self._cfg_str("empty_library_reply"))
            event.stop_event()
            return

        try:
            decision = await self._analyze_request(
                event,
                message,
                profile,
                candidates,
            )
        except Exception as exc:
            logger.error(
                "astrbot_plugin_smart_imagechat_hub: LLM image matching failed: %s",
                exc,
                exc_info=True,
            )
            fallback = self._fallback_match(candidates)
            decision = {
                "matched": bool(fallback),
                "image_id": fallback.get("id") if fallback else "",
                "image_ids": [fallback.get("id")] if fallback else [],
                "reason": "LLM matching failed, used local keyword fallback.",
                "need": message,
            }

        image_item = self._select_image(decision, candidates)
        if not image_item:
            if self._cfg_bool("llm_reply_when_not_found"):
                yield await self._request_llm_with_persona(
                    event,
                    self._not_found_prompt(message, candidates),
                )
            else:
                yield event.plain_result(self._cfg_str("not_found_reply"))
            event.stop_event()
            return

        image_path = self._abs_plugin_data_path(image_item["rel_path"])
        if not image_path.is_file():
            await self._sync_library(force=True, caption_mode="background")
            yield event.plain_result(self._cfg_str("not_found_reply"))
            event.stop_event()
            return

        if self._cfg_bool("use_custom_reply"):
            reply_text = self._render_custom_reply(image_item, decision)
            chain = []
            if reply_text:
                chain.append(Plain(reply_text))
            chain.append(Image.fromFileSystem(str(image_path)))
            yield event.chain_result(chain)
            await self._after_plugin_sent_image_for_meme_combat(
                event,
                str(image_path),
                source="user_search",
                defer_burst=True,
            )
        else:
            request = await self._request_llm_with_persona(
                event,
                self._found_prompt(message, image_item, decision),
            )
            request.extra_user_content_parts.append(
                TextPart(
                    text=(
                        "<astrbot_plugin_smart_imagechat_hub>"
                        "已匹配到本地图片，系统会在回复后发送图片。"
                        "</astrbot_plugin_smart_imagechat_hub>"
                    )
                )
            )
            yield request
            yield event.chain_result([Image.fromFileSystem(str(image_path))])
            await self._after_plugin_sent_image_for_meme_combat(
                event,
                str(image_path),
                source="user_search",
                defer_burst=True,
            )

        event.stop_event()

    @filter.on_decorating_result(priority=20)
    async def on_decorating_result(self, event: AstrMessageEvent):
        await self._maybe_append_proactive_emoji(event)

    @filter.after_message_sent(priority=20)
    async def after_message_sent(self, event: AstrMessageEvent):
        await self._send_pending_proactive_emoji(event)
        await self._send_pending_meme_combat_burst(event)

    # This handler intentionally never activates; the custom filter performs
    # the collection side effect without waking the bot.
    @filter.custom_filter(AutoImageCollectionMessageFilter, priority=5)
    @filter.event_message_type(filter.EventMessageType.ALL, priority=5)
    async def on_any_message_collect_images(self, event: AstrMessageEvent):
        return

    @filter.custom_filter(MemeCombatMessageFilter, priority=4)
    @filter.event_message_type(filter.EventMessageType.GROUP_MESSAGE, priority=4)
    async def on_group_meme_combat(self, event: AstrMessageEvent):
        return

    @filter.command("smart_image_sync", priority=50)
    async def sync_images_command(self, event: AstrMessageEvent):
        if not event.is_admin():
            yield event.plain_result("只有管理员可以同步智能图库。")
            event.stop_event()
            return

        before = len(self._index.get("images", {}))
        await self._sync_library(force=True, caption_mode="background")
        after = len(self._index.get("images", {}))
        yield event.plain_result(
            f"智能图库同步完成：{before} -> {after} 张。图片特征标签会在后台生成。"
        )
        event.stop_event()

