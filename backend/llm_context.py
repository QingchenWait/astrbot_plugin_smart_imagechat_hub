from .common import AstrMessageEvent, MODEL_FALLBACK_CONFIG_KEY, asyncio, logger, time


MODEL_FALLBACK_MODE_INHERIT = "inherit"
MODEL_FALLBACK_MODE_MANUAL = "manual"
MODEL_FALLBACK_MAX_MANUAL_PROVIDERS = 8
MODEL_PROVIDER_FAILURE_COOLDOWN_SECONDS = 90
MODEL_PROVIDER_TIMEOUT_SECONDS = 18
IMAGE_CAPTION_PROVIDER_MIN_INTERVAL_SECONDS = 1.0


class LLMContextMixin:
    async def _request_llm_with_persona(
        self,
        event: AstrMessageEvent,
        prompt: str,
    ):
        conversation = await self._current_conversation(event)
        return event.request_llm(prompt=prompt, conversation=conversation)

    async def _current_conversation(self, event: AstrMessageEvent):
        conv_mgr = getattr(self.context, "conversation_manager", None)
        if conv_mgr is None:
            return None

        umo = event.unified_msg_origin
        platform_id = event.get_platform_id()
        cid = await conv_mgr.get_curr_conversation_id(umo)
        if not cid:
            cid = await conv_mgr.new_conversation(umo, platform_id)

        conversation = await conv_mgr.get_conversation(umo, cid)
        if conversation:
            return conversation

        cid = await conv_mgr.new_conversation(umo, platform_id)
        return await conv_mgr.get_conversation(umo, cid)

    def _normalize_model_fallback_config(self, raw) -> dict:
        raw = raw if isinstance(raw, dict) else {}
        mode = str(raw.get("mode") or "").strip().lower()
        if mode not in {MODEL_FALLBACK_MODE_INHERIT, MODEL_FALLBACK_MODE_MANUAL}:
            mode = MODEL_FALLBACK_MODE_INHERIT

        provider_ids: list[str] = []
        for provider_id in self._list_from_payload(raw.get("provider_ids", [])):
            normalized = str(provider_id or "").strip()
            if normalized:
                provider_ids.append(normalized)
        for key in ("priority_1", "priority_2", "priority_3"):
            normalized = str(raw.get(key) or "").strip()
            if normalized:
                provider_ids.append(normalized)

        available_provider_ids = self._available_chat_provider_ids()
        deduped: list[str] = []
        seen: set[str] = set()
        for provider_id in provider_ids:
            if provider_id in seen:
                continue
            if available_provider_ids and provider_id not in available_provider_ids:
                continue
            seen.add(provider_id)
            deduped.append(provider_id)
            if len(deduped) >= MODEL_FALLBACK_MAX_MANUAL_PROVIDERS:
                break

        return {
            "mode": mode,
            "provider_ids": deduped,
            "priority_1": deduped[0] if len(deduped) >= 1 else "",
            "priority_2": deduped[1] if len(deduped) >= 2 else "",
            "priority_3": deduped[2] if len(deduped) >= 3 else "",
        }

    def _model_fallback_config(self) -> dict:
        return self._normalize_model_fallback_config(
            self.config.get(MODEL_FALLBACK_CONFIG_KEY, {})
        )

    def _model_fallback_snapshot(self) -> dict:
        cfg = self._model_fallback_config()
        return {
            **cfg,
            "provider_options": [
                option
                for option in self._chat_provider_options()
                if str(option.get("id") or "").strip()
            ],
            "astrbot_fallback_provider_ids": self._astrbot_fallback_chat_provider_ids(),
        }

    def _migrate_model_fallback_config(self) -> None:
        current = self.config.get(MODEL_FALLBACK_CONFIG_KEY, {})
        normalized = self._normalize_model_fallback_config(current)
        if current != normalized:
            self.config[MODEL_FALLBACK_CONFIG_KEY] = normalized
            self._save_plugin_config()

    def _refresh_model_fallback_schema(self) -> None:
        schema = getattr(self.config, "schema", None)
        if not isinstance(schema, dict):
            return
        group_schema = schema.get(MODEL_FALLBACK_CONFIG_KEY)
        if not isinstance(group_schema, dict):
            return
        items = group_schema.get("items")
        if not isinstance(items, dict):
            return
        options = [""] + [
            str(option.get("id") or "").strip()
            for option in self._chat_provider_options()
            if str(option.get("id") or "").strip()
        ]
        for key in ("priority_1", "priority_2", "priority_3"):
            provider_schema = items.get(key)
            if isinstance(provider_schema, dict):
                provider_schema["options"] = options

    def _astrbot_fallback_chat_provider_ids(self) -> list[str]:
        cfg = self.context.get_config()
        provider_settings = cfg.get("provider_settings", {}) if cfg else {}
        if not isinstance(provider_settings, dict):
            return []
        available_provider_ids = self._available_chat_provider_ids()
        provider_ids: list[str] = []
        seen: set[str] = set()
        raw_ids = provider_settings.get("fallback_chat_models", [])
        for raw_id in self._list_from_payload(raw_ids):
            provider_id = str(raw_id or "").strip()
            if (
                not provider_id
                or provider_id in seen
                or provider_id not in available_provider_ids
            ):
                continue
            seen.add(provider_id)
            provider_ids.append(provider_id)
        return provider_ids

    def _model_provider_is_temporarily_failed(self, provider_id: str) -> bool:
        if not provider_id:
            return False
        failure_until = getattr(self, "_model_provider_failure_until", {})
        if not isinstance(failure_until, dict):
            return False
        until = self._to_float(failure_until.get(provider_id), 0.0)
        if until <= time.time():
            failure_until.pop(provider_id, None)
            return False
        return True

    def _mark_model_provider_failure(self, provider_id: str) -> None:
        if not provider_id:
            return
        failure_until = getattr(self, "_model_provider_failure_until", None)
        if not isinstance(failure_until, dict):
            self._model_provider_failure_until = {}
            failure_until = self._model_provider_failure_until
        failure_until[provider_id] = time.time() + MODEL_PROVIDER_FAILURE_COOLDOWN_SECONDS

    async def _run_image_caption_provider_request(self, call_factory):
        lock = getattr(self, "_caption_provider_call_lock", None)
        if lock is None:
            lock = asyncio.Lock()
            self._caption_provider_call_lock = lock

        async with lock:
            try:
                last_call_at = float(getattr(self, "_last_caption_provider_call_at", 0.0))
            except (TypeError, ValueError):
                last_call_at = 0.0
            wait_seconds = IMAGE_CAPTION_PROVIDER_MIN_INTERVAL_SECONDS - (
                time.monotonic() - last_call_at
            )
            if wait_seconds > 0:
                await asyncio.sleep(wait_seconds)
            try:
                return await call_factory()
            finally:
                self._last_caption_provider_call_at = time.monotonic()

    async def _model_provider_candidate_ids(
        self,
        primary_provider_id: str = "",
        umo: str = "",
        use_current_when_primary_empty: bool = False,
        use_failure_cooldown: bool = True,
    ) -> list[str]:
        available_provider_ids = self._available_chat_provider_ids()
        candidates: list[str] = []
        seen: set[str] = set()

        def add_provider(provider_id: str) -> None:
            normalized = str(provider_id or "").strip()
            if (
                not normalized
                or normalized in seen
                or normalized not in available_provider_ids
                or (
                    use_failure_cooldown
                    and self._model_provider_is_temporarily_failed(normalized)
                )
            ):
                return
            seen.add(normalized)
            candidates.append(normalized)

        primary_provider_id = str(primary_provider_id or "").strip()
        if primary_provider_id:
            add_provider(primary_provider_id)
        elif use_current_when_primary_empty and umo:
            try:
                add_provider(await self.context.get_current_chat_provider_id(umo))
            except Exception as exc:
                logger.debug(
                    "astrbot_plugin_smart_imagechat_hub: failed to resolve current chat provider: %s",
                    exc,
                )

        fallback_cfg = self._model_fallback_config()
        if fallback_cfg.get("mode") == MODEL_FALLBACK_MODE_MANUAL:
            for provider_id in fallback_cfg.get("provider_ids", []):
                add_provider(provider_id)
        for provider_id in self._astrbot_fallback_chat_provider_ids():
            add_provider(provider_id)
        return candidates

    async def _llm_generate_with_provider_fallback(
        self,
        *,
        primary_provider_id: str = "",
        umo: str = "",
        use_current_when_primary_empty: bool = False,
        prompt: str,
        image_urls: list[str] | None = None,
        contexts: list | None = None,
        system_prompt: str = "",
        operation_name: str = "llm request",
        timeout_seconds: float | None = MODEL_PROVIDER_TIMEOUT_SECONDS,
        allow_no_provider: bool = False,
        use_failure_cooldown: bool = True,
        direct_provider_call: bool = False,
    ):
        provider_ids = await self._model_provider_candidate_ids(
            primary_provider_id=primary_provider_id,
            umo=umo,
            use_current_when_primary_empty=use_current_when_primary_empty,
            use_failure_cooldown=use_failure_cooldown,
        )
        if not provider_ids:
            if allow_no_provider:
                return None
            raise RuntimeError(f"No available provider for {operation_name}.")

        last_exc: Exception | None = None
        for provider_id in provider_ids:
            try:
                if direct_provider_call:
                    provider = self.context.get_provider_by_id(provider_id)
                    if provider is None or not callable(
                        getattr(provider, "text_chat", None)
                    ):
                        raise RuntimeError(f"provider {provider_id} is unavailable")
                    llm_call = provider.text_chat(
                        prompt=prompt,
                        image_urls=image_urls,
                        contexts=contexts if contexts is not None else [],
                        system_prompt=system_prompt,
                    )
                else:
                    llm_call = self.context.llm_generate(
                        chat_provider_id=provider_id,
                        prompt=prompt,
                        image_urls=image_urls,
                        contexts=contexts if contexts is not None else [],
                        system_prompt=system_prompt,
                    )
                if timeout_seconds is None or self._to_float(timeout_seconds, 0.0) <= 0:
                    resp = await llm_call
                else:
                    resp = await asyncio.wait_for(
                        llm_call,
                        timeout=max(1.0, float(timeout_seconds)),
                    )
                completion_text = str(getattr(resp, "completion_text", "") or "")
                error_text = completion_text.lower()
                if "[erro]" in error_text or "internal server error" in error_text:
                    raise RuntimeError(completion_text[:500] or "provider returned error")
                return resp
            except asyncio.CancelledError:
                raise
            except Exception as exc:
                last_exc = exc
                if use_failure_cooldown:
                    self._mark_model_provider_failure(provider_id)
                logger.warning(
                    "astrbot_plugin_smart_imagechat_hub: %s failed on provider %s: %s",
                    operation_name,
                    provider_id,
                    str(exc) or type(exc).__name__,
                )
        last_error = (
            f"{type(last_exc).__name__}: {last_exc}"
            if last_exc and str(last_exc)
            else type(last_exc).__name__ if last_exc else "unknown error"
        )
        raise RuntimeError(f"All providers failed for {operation_name}: {last_error}")

