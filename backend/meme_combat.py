from .common import (
    Any,
    AstrMessageEvent,
    Image,
    MEME_COMBAT_CONFIG_KEY,
    MessageEventResult,
    PENDING_MEME_COMBAT_IMAGE_EXTRA_KEY,
    Path,
    Plain,
    SUPPORTED_IMAGE_EXTS,
    asyncio,
    json,
    logger,
    random,
    time,
    urlparse,
)


MEME_COMBAT_CHAIN_COOLDOWN_SECONDS = 45
MEME_COMBAT_BATTLE_COOLDOWN_SECONDS = 60
MEME_COMBAT_BATTLE_FAILURE_COOLDOWN_SECONDS = 90
MEME_COMBAT_BURST_INTERVAL_SECONDS = 0.9
MEME_COMBAT_MAX_GROUPS = 128
MEME_COMBAT_MAX_EVENTS_PER_GROUP = 32
MEME_COMBAT_MAX_BATTLE_TASKS = 8
MEME_COMBAT_HASH_PREFIX_BYTES = 128 * 1024
MEME_COMBAT_QUEUE_MAXSIZE = 96
MEME_COMBAT_LLM_TIMEOUT_SECONDS = 8


class MemeCombatMixin:
    def _init_meme_combat_state(self) -> None:
        self._meme_combat_groups: dict[str, dict[str, Any]] = {}
        self._last_plugin_image_by_group: dict[str, dict[str, Any]] = {}
        self._meme_combat_last_chain_at: dict[str, float] = {}
        self._meme_combat_last_battle_at: dict[str, float] = {}
        self._meme_combat_battle_running_groups: set[str] = set()
        self._meme_combat_battle_failure_until: dict[str, float] = {}
        self._meme_combat_tasks: set[asyncio.Task] = set()
        self._meme_combat_queue: asyncio.Queue[dict[str, Any]] | None = None
        self._meme_combat_worker_task: asyncio.Task | None = None

    async def _wait_meme_combat_tasks(self) -> None:
        if self._meme_combat_worker_task and not self._meme_combat_worker_task.done():
            self._meme_combat_worker_task.cancel()
            try:
                await self._meme_combat_worker_task
            except asyncio.CancelledError:
                pass
        tasks = [task for task in self._meme_combat_tasks if not task.done()]
        if not tasks:
            return
        for task in tasks:
            task.cancel()
        await asyncio.gather(*tasks, return_exceptions=True)
        self._meme_combat_tasks.clear()

    def _start_meme_combat_worker(self) -> None:
        if self._meme_combat_worker_task and not self._meme_combat_worker_task.done():
            return
        self._meme_combat_queue = asyncio.Queue(maxsize=MEME_COMBAT_QUEUE_MAXSIZE)
        self._meme_combat_worker_task = asyncio.create_task(
            self._meme_combat_worker_loop(),
        )

    def _enqueue_meme_combat_event(self, event: AstrMessageEvent) -> bool:
        queue = self._meme_combat_queue
        if queue is None:
            try:
                self._start_meme_combat_worker()
                queue = self._meme_combat_queue
            except RuntimeError:
                return False
        if queue is None:
            return False
        try:
            images = tuple(comp for comp in event.get_messages() if isinstance(comp, Image))
            plain_parts = tuple(
                str(comp.text or "")
                for comp in event.get_messages()
                if isinstance(comp, Plain) and str(comp.text or "").strip()
            )
            queue.put_nowait(
                {
                    "event": event,
                    "group_id": str(event.get_group_id() or "").strip(),
                    "sender_id": str(event.get_sender_id() or "").strip(),
                    "self_id": str(event.get_self_id() or "").strip(),
                    "message_str": str(event.get_message_str() or ""),
                    "images": images,
                    "plain_parts": plain_parts,
                }
            )
            return True
        except asyncio.QueueFull:
            logger.debug(
                "astrbot_plugin_smart_imagechat_hub: meme combat queue is full; skipped group message.",
            )
            return False

    async def _meme_combat_worker_loop(self) -> None:
        queue = self._meme_combat_queue
        if queue is None:
            return
        while True:
            job = await queue.get()
            try:
                await self._track_group_meme_combat(job)
            except asyncio.CancelledError:
                raise
            except Exception as exc:
                logger.debug(
                    "astrbot_plugin_smart_imagechat_hub: meme combat event skipped: %s",
                    exc,
                )
            finally:
                queue.task_done()

    def _meme_combat_config(self) -> dict[str, Any]:
        return self._normalize_meme_combat_config(
            self.config.get(MEME_COMBAT_CONFIG_KEY, {})
        )

    def _normalize_meme_combat_config(self, raw: Any) -> dict[str, Any]:
        raw = raw if isinstance(raw, dict) else {}
        follow_raw = raw.get("follow_pattern", {})
        burst_raw = raw.get("image_burst", {})
        battle_raw = raw.get("battle", {})
        follow = follow_raw if isinstance(follow_raw, dict) else {}
        burst = burst_raw if isinstance(burst_raw, dict) else {}
        battle = battle_raw if isinstance(battle_raw, dict) else {}
        follow_window = self._to_int(follow.get("time_window_seconds"), 30)
        follow_count = self._to_int(follow.get("same_image_count"), 3)
        burst_probability = self._to_float(burst.get("trigger_probability"), 0.2)
        burst_count = self._to_int(burst.get("burst_count"), 2)
        battle_window = self._to_int(battle.get("time_window_seconds"), 30)
        battle_count = self._to_int(battle.get("continuous_image_count"), 6)
        provider_id = str(battle.get("analysis_provider_id") or "").strip()
        return {
            "enabled": self._to_bool(raw.get("enabled"), False),
            "follow_pattern": {
                "enabled": self._to_bool(follow.get("enabled"), True),
                "time_window_seconds": max(1, min(follow_window, 600)),
                "same_image_count": max(2, min(follow_count, 20)),
                "distinct_users_required": self._to_bool(
                    follow.get("distinct_users_required"),
                    False,
                ),
            },
            "image_burst": {
                "enabled": self._to_bool(burst.get("enabled"), True),
                "trigger_probability": str(
                    max(0.0, min(burst_probability, 1.0))
                ),
                "burst_count": max(1, min(burst_count, 6)),
            },
            "battle": {
                "enabled": self._to_bool(battle.get("enabled"), True),
                "time_window_seconds": max(1, min(battle_window, 600)),
                "continuous_image_count": max(2, min(battle_count, 30)),
                "analysis_provider_id": provider_id,
            },
        }

    def _meme_combat_snapshot(self) -> dict[str, Any]:
        cfg = self._meme_combat_config()
        return {
            **cfg,
            "provider_options": self._chat_provider_options(),
            "updated_at": int(time.time()),
        }

    def _migrate_meme_combat_config(self) -> None:
        current = self.config.get(MEME_COMBAT_CONFIG_KEY, {})
        normalized = self._normalize_meme_combat_config(current)
        if current != normalized:
            self.config[MEME_COMBAT_CONFIG_KEY] = normalized
            self._save_plugin_config()

    def _refresh_meme_combat_schema(self) -> None:
        schema = getattr(self.config, "schema", None)
        if not isinstance(schema, dict):
            return
        group_schema = schema.get(MEME_COMBAT_CONFIG_KEY)
        if not isinstance(group_schema, dict):
            return
        battle_schema = (
            group_schema.get("items", {})
            if isinstance(group_schema.get("items"), dict)
            else {}
        ).get("battle")
        if not isinstance(battle_schema, dict):
            return
        battle_items = battle_schema.get("items")
        if not isinstance(battle_items, dict):
            return
        provider_schema = battle_items.get("analysis_provider_id")
        if not isinstance(provider_schema, dict):
            return
        provider_schema["options"] = [
            option["id"] for option in self._chat_provider_options()
        ]

    async def _track_group_meme_combat(
        self,
        job: AstrMessageEvent | dict[str, Any],
    ) -> None:
        cfg = self._meme_combat_config()
        if not cfg.get("enabled"):
            return
        event = job.get("event") if isinstance(job, dict) else job
        if not isinstance(event, AstrMessageEvent):
            return
        group_id = str(
            job.get("group_id") if isinstance(job, dict) else event.get_group_id()
            or ""
        ).strip()
        if not group_id:
            return
        images = list(job.get("images") or []) if isinstance(job, dict) else [
            comp for comp in event.get_messages() if isinstance(comp, Image)
        ]
        sender_id = str(
            job.get("sender_id") if isinstance(job, dict) else event.get_sender_id()
            or ""
        ).strip()
        self_id = str(
            job.get("self_id") if isinstance(job, dict) else event.get_self_id() or ""
        ).strip()
        is_self = bool(sender_id and self_id and sender_id == self_id)
        has_plain_text = self._meme_combat_has_plain_text(job)

        if is_self and images:
            self._reset_meme_combat_group_after_bot_image(group_id)
            return
        if is_self:
            if has_plain_text:
                self._break_meme_combat_image_streak(group_id)
            return
        if not images:
            self._break_meme_combat_image_streak(group_id)
            return

        now = time.time()
        state = self._meme_combat_group_state(group_id)
        if has_plain_text:
            state["streak"] = []

        image_items = self._meme_combat_image_infos(images)
        if not image_items:
            self._break_meme_combat_image_streak(group_id)
            return

        follow_candidates: list[dict[str, Any]] = []
        for image_item in image_items:
            event_item = {
                **image_item,
                "ts": now,
                "sender_id": sender_id,
            }
            state["events"].append(event_item)
            if not has_plain_text:
                state["streak"].append(event_item)
            follow_candidates.append(event_item)

        self._trim_meme_combat_state(state, cfg, now)
        await self._maybe_follow_meme_pattern(event, group_id, follow_candidates, cfg)
        self._maybe_start_meme_battle_task(event, group_id, state, cfg)

    def _meme_combat_group_state(self, group_id: str) -> dict[str, Any]:
        if group_id not in self._meme_combat_groups:
            if len(self._meme_combat_groups) >= MEME_COMBAT_MAX_GROUPS:
                oldest_group = min(
                    self._meme_combat_groups,
                    key=lambda key: self._to_float(
                        self._meme_combat_groups[key].get("updated_at"),
                        0.0,
                    ),
                )
                self._meme_combat_groups.pop(oldest_group, None)
            self._meme_combat_groups[group_id] = {
                "events": [],
                "streak": [],
                "followed_digests": set(),
                "updated_at": time.time(),
            }
        state = self._meme_combat_groups[group_id]
        state["updated_at"] = time.time()
        if not isinstance(state.get("events"), list):
            state["events"] = []
        if not isinstance(state.get("streak"), list):
            state["streak"] = []
        if not isinstance(state.get("followed_digests"), set):
            state["followed_digests"] = set()
        return state

    def _trim_meme_combat_state(
        self,
        state: dict[str, Any],
        cfg: dict[str, Any],
        now: float,
    ) -> None:
        follow_window = self._to_int(
            cfg.get("follow_pattern", {}).get("time_window_seconds"),
            30,
        )
        battle_window = self._to_int(
            cfg.get("battle", {}).get("time_window_seconds"),
            30,
        )
        window = max(follow_window, battle_window, 1)
        min_ts = now - window
        state["events"] = [
            item
            for item in state.get("events", [])[-MEME_COMBAT_MAX_EVENTS_PER_GROUP:]
            if self._to_float(item.get("ts"), 0.0) >= min_ts
        ]
        state["streak"] = [
            item
            for item in state.get("streak", [])[-MEME_COMBAT_MAX_EVENTS_PER_GROUP:]
            if self._to_float(item.get("ts"), 0.0) >= min_ts
        ]
        active_digests = {
            str(item.get("digest") or "")
            for item in state["events"]
            if str(item.get("digest") or "")
        }
        followed = state.get("followed_digests")
        if isinstance(followed, set):
            state["followed_digests"] = {
                digest for digest in followed if digest in active_digests
            }

    def _break_meme_combat_image_streak(self, group_id: str) -> None:
        state = self._meme_combat_groups.get(group_id)
        if isinstance(state, dict):
            state["streak"] = []

    def _reset_meme_combat_group_after_bot_image(self, group_id: str) -> None:
        state = self._meme_combat_group_state(group_id)
        state["events"] = []
        state["streak"] = []
        state["followed_digests"] = set()
        state["updated_at"] = time.time()

    def _meme_combat_image_infos(
        self,
        images: list[Image],
    ) -> list[dict[str, Any]]:
        infos: list[dict[str, Any]] = []
        for image in images:
            info = self._meme_combat_image_info(image)
            if info:
                infos.append(info)
        return infos

    def _meme_combat_has_plain_text(
        self,
        job: AstrMessageEvent | dict[str, Any],
    ) -> bool:
        if isinstance(job, dict):
            if any(str(text or "").strip() for text in job.get("plain_parts", ())):
                return True
            outline = str(job.get("message_str") or "")
        else:
            for comp in job.get_messages():
                if isinstance(comp, Plain) and str(comp.text or "").strip():
                    return True
            outline = job.get_message_str() or ""
        for token in ("[图片]", "[image]", "[Image]", "[图片消息]"):
            outline = outline.replace(token, "")
        return bool(outline.strip())

    def _meme_combat_image_info(self, image: Image) -> dict[str, Any] | None:
        local_path = self._meme_combat_fast_image_path(image)
        if local_path:
            path = Path(local_path)
            if not path.is_file() or path.suffix.lower() not in SUPPORTED_IMAGE_EXTS:
                return None
            try:
                digest = self._meme_combat_light_digest(path)
            except OSError:
                return None
            return {
                "digest": digest,
                "path": str(path),
                "image": image,
                "send_source": {"kind": "path", "value": str(path)},
            }

        raw_values = self._meme_combat_image_raw_values(image)
        digest_source = self._meme_combat_digest_source(raw_values)
        if not digest_source:
            return None
        send_source = self._meme_combat_send_source(raw_values)

        if digest_source.startswith(("http://", "https://")):
            digest = self._sha256_bytes(
                self._meme_combat_normalized_url_key(digest_source).encode("utf-8")
            )
            return {
                "digest": f"url:{digest}",
                "path": "",
                "image": image,
                "send_source": send_source,
            }

        if digest_source.startswith("base64://"):
            digest = self._sha256_bytes(digest_source.encode("utf-8"))
            return {
                "digest": f"base64:{digest}",
                "path": "",
                "image": image,
                "send_source": send_source,
            }

        digest = self._sha256_bytes(digest_source.encode("utf-8"))
        return {
            "digest": f"raw:{digest}",
            "path": "",
            "image": image,
            "send_source": send_source,
        }

    def _meme_combat_image_raw_values(self, image: Image) -> dict[str, str]:
        return {
            "path": str(getattr(image, "path", None) or "").strip(),
            "file": str(getattr(image, "file", None) or "").strip(),
            "url": str(getattr(image, "url", None) or "").strip(),
        }

    def _meme_combat_send_source(self, values: dict[str, str]) -> dict[str, str]:
        for key in ("url", "file", "path"):
            value = str(values.get(key) or "").strip()
            if value.startswith(("http://", "https://")):
                return {"kind": "url", "value": value}
            if value.startswith("base64://"):
                return {"kind": "base64", "value": value.removeprefix("base64://")}
        raw = str(values.get("file") or values.get("url") or values.get("path") or "")
        return {"kind": "raw", "value": raw.strip()}

    def _meme_combat_digest_source(self, values: dict[str, str]) -> str:
        for key in ("file", "path", "url"):
            value = str(values.get(key) or "").strip()
            if (
                value
                and not value.startswith(("http://", "https://", "base64://", "file://"))
                and not Path(value).is_file()
            ):
                return f"{key}:{value}"
        for key in ("url", "file", "path"):
            value = str(values.get(key) or "").strip()
            if value:
                return value
        return ""

    def _meme_combat_normalized_url_key(self, url: str) -> str:
        parsed = urlparse(url)
        if not parsed.scheme or not parsed.netloc:
            return url
        return f"{parsed.scheme}://{parsed.netloc}{parsed.path}"

    async def _meme_combat_resolve_item_path(self, item: dict[str, Any]) -> str:
        path = str(item.get("path") or "")
        if path and Path(path).is_file():
            return path
        send_source = item.get("send_source", {})
        if not isinstance(send_source, dict):
            send_source = {}
        kind = str(send_source.get("kind") or "")
        value = str(send_source.get("value") or "")
        image = item.get("image")
        if kind == "url" and value:
            try:
                resolved = await self._download_collected_image_url(value, 1024)
                item["path"] = str(resolved)
                return str(resolved)
            except Exception as exc:
                logger.debug(
                    "astrbot_plugin_smart_imagechat_hub: meme combat failed to download image URL: %s",
                    exc,
                )
                return ""
        if isinstance(image, Image):
            try:
                resolved = await asyncio.wait_for(
                    image.convert_to_file_path(),
                    timeout=4,
                )
                item["path"] = resolved
                return resolved
            except Exception as exc:
                logger.debug(
                    "astrbot_plugin_smart_imagechat_hub: meme combat skipped unreadable image: %s",
                    exc,
                )
                return ""
        return ""

    def _meme_combat_image_component(self, item: dict[str, Any]) -> Image | None:
        send_source = item.get("send_source", {})
        if not isinstance(send_source, dict):
            send_source = {}
        kind = str(send_source.get("kind") or "")
        value = str(send_source.get("value") or "")
        try:
            if kind == "path" and value and Path(value).is_file():
                return Image.fromFileSystem(value)
            if kind == "url" and value.startswith(("http://", "https://")):
                return Image.fromURL(value)
            if kind == "base64" and value:
                return Image.fromBase64(value)
            image = item.get("image")
            if isinstance(image, Image):
                raw = str(
                    getattr(image, "url", None) or getattr(image, "file", None) or ""
                )
                if raw.startswith(("http://", "https://")):
                    return Image.fromURL(raw)
                if raw.startswith("base64://"):
                    return Image.fromBase64(raw.removeprefix("base64://"))
                path = self._meme_combat_fast_image_path(image)
                if path:
                    return Image.fromFileSystem(path)
        except Exception:
            return None
        return None

    async def _meme_combat_follow_send_path(
        self,
        item: dict[str, Any],
    ) -> tuple[Path | None, list[Path]]:
        cleanup_paths: list[Path] = []
        existing_path = str(item.get("path") or "")
        resolved_path = await self._meme_combat_resolve_item_path(item)
        if not resolved_path:
            return None, cleanup_paths
        path = Path(resolved_path)
        if not path.is_file():
            return None, cleanup_paths
        cleanup_resolved_path = True
        if existing_path:
            try:
                cleanup_resolved_path = Path(existing_path).resolve() != path.resolve()
            except OSError:
                cleanup_resolved_path = True
        if cleanup_resolved_path:
            cleanup_paths.append(path)
        prepared_path, style_cleanup_paths = await self._prepare_send_image_path(
            path,
            None,
            ignore_tag_gate=True,
        )
        cleanup_paths.extend(style_cleanup_paths)
        return prepared_path, cleanup_paths

    async def _send_meme_combat_item(
        self,
        event: AstrMessageEvent,
        group_id: str,
        item: dict[str, Any],
        source: str,
        reset_window: bool = True,
    ) -> bool:
        component = self._meme_combat_image_component(item)
        original_path = str(item.get("path") or "")
        cleanup_paths: list[Path] = []
        if source == "follow_pattern":
            prepared_path, cleanup_paths = await self._meme_combat_follow_send_path(
                item,
            )
            if prepared_path is not None:
                component = Image.fromFileSystem(str(prepared_path))
                if not original_path:
                    original_path = str(Path(str(item.get("path") or "")))
            cleanup_paths = self._defer_send_image_style_cleanup(event, cleanup_paths)
        if component is None:
            self._cleanup_temp_paths(cleanup_paths)
            return False
        try:
            result = MessageEventResult()
            result.chain = [component]
            await event.send(result)
            self._record_plugin_sent_image(
                group_id,
                original_path,
                source,
            )
            if reset_window:
                self._reset_meme_combat_group_after_bot_image(group_id)
            if source != "image_burst":
                await self._maybe_send_meme_burst(event, group_id)
            return True
        except Exception as exc:
            logger.warning(
                "astrbot_plugin_smart_imagechat_hub: failed to send meme combat image: %s",
                exc,
                exc_info=True,
            )
            return False
        finally:
            self._cleanup_temp_paths(cleanup_paths)

    def _meme_combat_fast_image_path(self, image: Image) -> str:
        path = self._local_image_component_path(image)
        return str(path) if path else ""

    def _meme_combat_light_digest(self, path: Path) -> str:
        stat = path.stat()
        with open(path, "rb") as f:
            prefix = f.read(MEME_COMBAT_HASH_PREFIX_BYTES)
        raw = (
            f"{stat.st_size}:".encode("utf-8")
            + str(path.suffix.lower()).encode("utf-8")
            + b":"
            + prefix
        )
        return self._sha256_bytes(raw)

    async def _maybe_follow_meme_pattern(
        self,
        event: AstrMessageEvent,
        group_id: str,
        new_items: list[dict[str, Any]],
        cfg: dict[str, Any],
    ) -> None:
        follow_cfg = cfg.get("follow_pattern", {})
        if not follow_cfg.get("enabled"):
            return
        state = self._meme_combat_group_state(group_id)
        threshold = self._to_int(follow_cfg.get("same_image_count"), 3)
        window = self._to_int(follow_cfg.get("time_window_seconds"), 30)
        now = time.time()
        followed = state.get("followed_digests")
        if not isinstance(followed, set):
            followed = set()
            state["followed_digests"] = followed

        for item in new_items:
            digest = str(item.get("digest") or "")
            if not digest or digest in followed:
                continue
            matches = [
                candidate
                for candidate in state.get("events", [])
                if str(candidate.get("digest") or "") == digest
                and now - self._to_float(candidate.get("ts"), 0.0) <= window
            ]
            send_item = matches[-1] if matches else item
            if (
                self._meme_combat_follow_match_count(
                    matches,
                    bool(follow_cfg.get("distinct_users_required")),
                )
                < threshold
            ):
                continue
            if await self._send_meme_combat_item(
                event,
                group_id,
                send_item,
                source="follow_pattern",
            ):
                followed.add(digest)
            return

    def _meme_combat_follow_match_count(
        self,
        matches: list[dict[str, Any]],
        distinct_users_required: bool,
    ) -> int:
        if not distinct_users_required:
            return len(matches)
        senders = set()
        unknown_seen = False
        for item in matches:
            sender_id = str(item.get("sender_id") or "").strip()
            if sender_id:
                senders.add(sender_id)
            elif not unknown_seen:
                senders.add("")
                unknown_seen = True
        return len(senders)

    def _maybe_start_meme_battle_task(
        self,
        event: AstrMessageEvent,
        group_id: str,
        state: dict[str, Any],
        cfg: dict[str, Any],
    ) -> None:
        battle_cfg = cfg.get("battle", {})
        if not battle_cfg.get("enabled"):
            return
        if group_id in self._meme_combat_battle_running_groups:
            return
        threshold = self._to_int(battle_cfg.get("continuous_image_count"), 6)
        window = self._to_int(battle_cfg.get("time_window_seconds"), 30)
        now = time.time()
        failure_until = self._to_float(
            self._meme_combat_battle_failure_until.get(group_id),
            0.0,
        )
        if failure_until > now:
            return
        last_at = self._meme_combat_last_battle_at.get(group_id, 0.0)
        if now - last_at < MEME_COMBAT_BATTLE_COOLDOWN_SECONDS:
            return
        streak = [
            item
            for item in state.get("streak", [])
            if now - self._to_float(item.get("ts"), 0.0) <= window
        ]
        if len(streak) < threshold:
            return
        if len(self._meme_combat_tasks) >= MEME_COMBAT_MAX_BATTLE_TASKS:
            return
        sample = random.sample(streak, 2) if len(streak) >= 2 else streak[:]
        if len(sample) < 2:
            return
        state["streak"] = []
        self._meme_combat_last_battle_at[group_id] = now
        self._meme_combat_battle_running_groups.add(group_id)
        task = asyncio.create_task(
            self._handle_meme_battle(event, group_id, sample, battle_cfg)
        )
        self._meme_combat_tasks.add(task)
        task.add_done_callback(self._meme_combat_tasks.discard)

    async def _handle_meme_battle(
        self,
        event: AstrMessageEvent,
        group_id: str,
        image_items: list[dict[str, Any]],
        battle_cfg: dict[str, Any],
    ) -> None:
        try:
            await self._sync_library(caption_mode="none")
            candidates = self._library_candidates()
            if not candidates:
                return
            image_paths = []
            for item in image_items:
                resolved_path = await self._meme_combat_resolve_item_path(item)
                if resolved_path:
                    image_paths.append(resolved_path)
                if len(image_paths) >= 2:
                    break
            if len(image_paths) < 2:
                return
            profile_text = await self._analyze_meme_battle_images(
                event,
                image_paths,
                str(battle_cfg.get("analysis_provider_id") or ""),
            )
            if not profile_text:
                return
            profile, ranked = self._rank_search_candidates(profile_text, candidates)
            if not ranked:
                return
            try:
                provider_id = str(battle_cfg.get("analysis_provider_id") or "").strip()
                decision = await self._analyze_meme_battle_match(
                    event,
                    provider_id,
                    profile_text,
                    profile,
                    ranked,
                )
            except Exception as exc:
                logger.debug(
                    "astrbot_plugin_smart_imagechat_hub: meme battle matching fell back locally: %s",
                    exc,
                )
                fallback = self._fallback_match(ranked)
                decision = {
                    "matched": bool(fallback),
                    "image_ids": [fallback.get("id")] if fallback else [],
                    "image_id": fallback.get("id") if fallback else "",
                    "confidence": 0.5 if fallback else 0.0,
                }
            image_item = self._select_meme_battle_image(decision, ranked)
            if not image_item:
                image_item = self._fallback_match(ranked)
            if not image_item:
                return
            image_path = self._abs_plugin_data_path(image_item["rel_path"])
            await self._send_meme_combat_image(
                event,
                group_id,
                str(image_path),
                source="battle",
                reset_window=True,
            )
        except asyncio.CancelledError:
            raise
        except Exception as exc:
            self._meme_combat_battle_failure_until[group_id] = (
                time.time() + MEME_COMBAT_BATTLE_FAILURE_COOLDOWN_SECONDS
            )
            logger.warning(
                "astrbot_plugin_smart_imagechat_hub: meme battle failed: %s",
                exc,
                exc_info=True,
            )
        finally:
            self._meme_combat_battle_running_groups.discard(group_id)

    async def _analyze_meme_battle_images(
        self,
        event: AstrMessageEvent,
        image_paths: list[str],
        provider_id: str,
    ) -> str:
        paths = [path for path in image_paths[:2] if Path(path).is_file()]
        if len(paths) < 2:
            return ""
        resp = await self._llm_generate_with_provider_fallback(
            primary_provider_id=provider_id,
            umo=event.unified_msg_origin,
            use_current_when_primary_empty=True,
            operation_name="meme battle image analysis",
            timeout_seconds=MEME_COMBAT_LLM_TIMEOUT_SECONDS,
            prompt=(
                "请快速分析这两张连续图片对话的共同语义、情绪、场景和适合接上的表情包方向。"
                "只输出 6 到 12 个短中文关键词，用空格分隔，不要解释。"
            ),
            image_urls=paths,
            contexts=[],
            system_prompt="你是群聊斗图语义压缩器，只输出关键词。",
        )
        return " ".join(self._normalize_tags(resp.completion_text))[:160]

    async def _analyze_meme_battle_match(
        self,
        event: AstrMessageEvent,
        provider_id: str,
        profile_text: str,
        profile: dict[str, Any],
        candidates: list[dict[str, Any]],
    ) -> dict[str, Any]:
        resp = await self._llm_generate_with_provider_fallback(
            primary_provider_id=provider_id,
            umo=event.unified_msg_origin,
            use_current_when_primary_empty=True,
            operation_name="meme battle match analysis",
            timeout_seconds=MEME_COMBAT_LLM_TIMEOUT_SECONDS,
            prompt=self._match_prompt(profile_text, profile, candidates),
            contexts=[],
            system_prompt=(
                "你是 AstrBot 的本地表情包斗图匹配器。"
                "只能输出严格 JSON，不要输出 Markdown、解释或多余文本。"
            ),
        )
        return self._parse_decision(resp.completion_text)

    def _select_meme_battle_image(
        self,
        decision: dict[str, Any],
        candidates: list[dict[str, Any]],
    ) -> dict[str, Any] | None:
        if not decision.get("matched"):
            return None
        candidate_by_id = {str(item["id"]): item for item in candidates}
        image_ids = self._normalize_ids(decision.get("image_ids", []))
        fallback_id = str(decision.get("image_id") or "").strip()
        if fallback_id and fallback_id not in image_ids:
            image_ids.append(fallback_id)
        matched_items = [
            candidate_by_id[image_id]
            for image_id in image_ids
            if image_id in candidate_by_id
        ]
        return random.choice(matched_items) if matched_items else None

    async def _meme_combat_provider_id(
        self,
        event: AstrMessageEvent,
        provider_id: str,
    ) -> str:
        provider_ids = {option["id"] for option in self._chat_provider_options()}
        normalized = str(provider_id or "").strip()
        if normalized and normalized in provider_ids:
            return normalized
        return await self.context.get_current_chat_provider_id(event.unified_msg_origin)

    async def _send_meme_combat_image(
        self,
        event: AstrMessageEvent,
        group_id: str,
        image_path: str,
        source: str,
        reset_window: bool = True,
    ) -> bool:
        path = Path(image_path)
        if not path.is_file():
            return False
        send_path, cleanup_paths = await self._prepare_send_image_path(
            path,
            self._tags_for_library_path(path),
        )
        cleanup_paths = self._defer_send_image_style_cleanup(event, cleanup_paths)
        try:
            await event.send(MessageEventResult().file_image(str(send_path)))
            self._record_plugin_sent_image(group_id, str(path), source)
            if reset_window:
                self._reset_meme_combat_group_after_bot_image(group_id)
            if source != "image_burst":
                await self._maybe_send_meme_burst(event, group_id)
            return True
        except Exception as exc:
            logger.warning(
                "astrbot_plugin_smart_imagechat_hub: failed to send meme combat image: %s",
                exc,
                exc_info=True,
            )
            return False
        finally:
            self._cleanup_temp_paths(cleanup_paths)

    def _record_plugin_sent_image(
        self,
        group_id: str,
        image_path: str,
        source: str,
    ) -> None:
        image_path = str(image_path or "").strip()
        if not image_path:
            self._last_plugin_image_by_group[group_id] = {
                "path": "",
                "rel_path": "",
                "image_id": "",
                "tags": [],
                "source": source,
                "sent_at": time.time(),
            }
            return
        path = Path(image_path)
        tags: list[str] = []
        image_id = ""
        rel_path = ""
        try:
            rel_path = path.resolve().relative_to(self.data_dir.resolve()).as_posix()
            image_id = self._image_id(rel_path)
            item = self._index_image_by_id(image_id)
            if item:
                tags = self._tags_from_item(item)
        except ValueError:
            rel_path = ""
        self._last_plugin_image_by_group[group_id] = {
            "path": str(path),
            "rel_path": rel_path,
            "image_id": image_id,
            "tags": tags,
            "source": source,
            "sent_at": time.time(),
        }

    async def _after_plugin_sent_image_for_meme_combat(
        self,
        event: AstrMessageEvent,
        image_path: str,
        source: str,
        allow_burst: bool = True,
        defer_burst: bool = False,
    ) -> None:
        cfg = self._meme_combat_config()
        if not cfg.get("enabled"):
            return
        group_id = str(event.get_group_id() or "").strip()
        if not group_id:
            return
        self._record_plugin_sent_image(group_id, image_path, source)
        if allow_burst:
            if defer_burst:
                event.set_extra(
                    PENDING_MEME_COMBAT_IMAGE_EXTRA_KEY,
                    {"group_id": group_id},
                )
            else:
                await self._maybe_send_meme_burst(event, group_id, cfg)

    async def _send_pending_meme_combat_burst(self, event: AstrMessageEvent) -> None:
        pending = event.get_extra(PENDING_MEME_COMBAT_IMAGE_EXTRA_KEY)
        if not isinstance(pending, dict):
            return
        event.set_extra(PENDING_MEME_COMBAT_IMAGE_EXTRA_KEY, None)
        group_id = str(pending.get("group_id") or event.get_group_id() or "").strip()
        if not group_id:
            return
        await self._maybe_send_meme_burst(event, group_id)

    async def _maybe_send_meme_burst(
        self,
        event: AstrMessageEvent,
        group_id: str,
        cfg: dict[str, Any] | None = None,
    ) -> None:
        cfg = cfg or self._meme_combat_config()
        burst_cfg = cfg.get("image_burst", {})
        if not cfg.get("enabled") or not burst_cfg.get("enabled"):
            return
        probability = self._to_float(burst_cfg.get("trigger_probability"), 0.2)
        if probability <= 0 or random.random() > probability:
            return
        now = time.time()
        last_at = self._meme_combat_last_chain_at.get(group_id, 0.0)
        if now - last_at < MEME_COMBAT_CHAIN_COOLDOWN_SECONDS:
            return
        last_image = self._last_plugin_image_by_group.get(group_id)
        if not isinstance(last_image, dict):
            return
        search_text = " ".join(self._normalize_tags(last_image.get("tags", [])))
        if not search_text:
            rel_path = str(last_image.get("rel_path") or "")
            if rel_path:
                item = self._index_image_by_id(self._image_id(rel_path))
                if item:
                    search_text = " ".join(self._tags_from_item(item))
                    last_image["tags"] = self._tags_from_item(item)
        if not search_text:
            return
        await self._sync_library(caption_mode="none")
        profile, candidates = self._rank_search_candidates(
            search_text,
            self._library_candidates(),
        )
        original_id = str(last_image.get("image_id") or "")
        candidates = [
            item for item in candidates if str(item.get("id") or "") != original_id
        ]
        if not candidates:
            return
        count = self._to_int(burst_cfg.get("burst_count"), 2)
        selected = self._select_meme_burst_images(candidates, count)
        if not selected:
            return
        self._meme_combat_last_chain_at[group_id] = now
        for item in selected:
            image_path = self._abs_plugin_data_path(item["rel_path"])
            if not image_path.is_file():
                continue
            sent = await self._send_meme_combat_image(
                event,
                group_id,
                str(image_path),
                source="image_burst",
                reset_window=True,
            )
            if not sent:
                continue
            await asyncio.sleep(MEME_COMBAT_BURST_INTERVAL_SECONDS)

    def _select_meme_burst_images(
        self,
        candidates: list[dict[str, Any]],
        count: int,
    ) -> list[dict[str, Any]]:
        if count <= 0:
            return []
        scored = [
            item
            for item in candidates
            if self._to_float(item.get("search_score"), 0.0) > 0
        ]
        pool = scored or candidates
        pool = pool[: max(count * 3, count)]
        count = min(count, len(pool))
        return random.sample(pool, count) if len(pool) > count else pool[:count]

    def _meme_combat_prompt_item(self, item: dict[str, Any]) -> dict[str, Any]:
        return {
            "id": item.get("id"),
            "filename": item.get("filename"),
            "tags": self._normalize_tags(item.get("tags", [])),
            "score": item.get("search_score", 0.0),
        }

    def _meme_combat_debug_state(self) -> str:
        return json.dumps(
            {
                "groups": len(self._meme_combat_groups),
                "tasks": len(self._meme_combat_tasks),
            },
            ensure_ascii=False,
        )
