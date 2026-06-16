# CHANGELOG

## v2.8.6

### Added

- 新增“对话中主动发送表情包”的“表情包检索模式”配置：
  `bot_reply_serial` 保持原串行逻辑，依据 bot 生成的回复内容检索；
  `user_message_parallel` 依据用户发言内容并发检索，减少主动表情包等待时间。
- 新增第三种主动表情包检索模式 `user_message_fast_prefilter`，展示为“依据发言内容本地精排，进行小规模并发检索（速度最快）”，只服务主动表情包流程。
- 该模式沿用配置值 `user_message_fast_prefilter`；v2.8.6 仅调整 WebUI 展示名称和主动表情包流程内的行为。
- 新增“对话中主动发送表情包”的“调试模式”开关，默认关闭；开启后仅输出该功能的逐步排查日志。
- Plugin Page 和原生 `_conf_schema.json` 均提供检索模式下拉选择。
- Plugin Page 在串行模式且 provider 文本包含 mimo / qwen / 通义时显示黄色速度提示，建议切换并发检索模式。

### Changed

- 并发检索模式会在主 LLM 请求前，用同一 provider 启动后台检索分析任务；目标并发边界为主 LLM 回复 + 表情包检索分析共 2 路。
- 本地精排+并发模式会先按标签库和强语义命中精排候选，再给 LLM 与普通搜图一致规模的候选集合；主回复装饰阶段若后台任务未完成，会直接取消任务，并仅在高置信命中时使用本地兜底候选或跳过发图。
- 图像检索、候选排序和选图核心逻辑保持不变，仅调整主动表情包分析的调用时机和输入文本来源；普通搜图、群聊智能斗图、图库格式和打标流程不受影响。
- 主动表情包调试日志限定在该功能流程内；关闭调试模式时不新增 info 日志，也不改变其他功能日志输出。
- Plugin Page 中 mimo / qwen / 通义 + 串行模式提示移动到“表情包检索模式”下拉菜单正下方，并复用黄色小字 `.provider-warning` 样式。

### Fixed

- 新增内部 marker，避免插件自身的主动表情包 LLM 分析请求递归触发并发检索入口。

### Documentation

- 补充主动表情包检索模式、默认值、使用建议、调用时机和调试注意事项。
- 补充主动表情包调试模式、日志边界和 Plugin Page 提示位置说明。

## v2.8.5

### Added

- Added `send_image_style`, a native WebUI and Page config group for sending selected local images as temporary single-frame GIF copies.
- Added `send_image_style.enabled`, enabled by default.
- Added `send_image_style.meme_tag_only`, disabled by default, to limit conversion to images whose merged tags include `表情包`.

### Changed

- User-search image replies, proactive emoji sends, and meme-combat library image sends now prepare a temporary GIF copy for non-GIF local files before entering the AstrBot send flow.
- Follow-pattern meme-combat replies prepare a temporary GIF copy when the repeated image is a local non-GIF file; URL/base64 follow-pattern images keep the previous send path.
- Original library files keep their source format for storage, indexing, tagging, and backups.

### Fixed

- No fixes in this release.

### Removed

- No removals.

### Performance

- Temporary GIF files are created only for the selected image immediately before send and are stored under the plugin data directory `send_image_style_cache/`.
- Send-path temporary GIF files are cleaned after send completion; proactive emoji images embedded into the LLM result chain defer cleanup until `after_message_sent`.

### Documentation

- Documented the GIF send-style switches, affected send paths, fallback behavior, and `send_image_style_cache/` cleanup behavior.
