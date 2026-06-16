# CHANGELOG

## v2.8.6

### 更新日志
- **新增**：`对话中主动发送表情包` 功能中，新增 `表情包检索模式` 配置项。

  我们发现，非 GPT 模型可能因 API 请求频率限制，导致带图回复的速度非常缓慢。因此，我们为表情包检索流程，添加了两种**更加快速的并发检索策略**，以优化 LLM API 响应速度。

  可在以下三种模式中，根据响应速度需求，任选其一：
  1. `依据 bot 生成的回复内容，进行串行检索（更加准确）`：插件原始策略，首先通过 LLM 生成 bot 回复用户的内容，再依据回复内容串行检索表情包，语境识别更准确。
  2. `依据用户发言内容，进行并发检索（速度更快）`：依据用户向 bot 输入的发言内容，以并发形式同步调用 LLM 进行回复生成+表情包检索，速度更快；
  3. `依据发言内容本地精排，进行小规模并发检索（速度最快）`：先按标签库和强语义命中，进行本地轻量化图像库精排，获取一组小规模候选图像，随后以并发形式进行小规模检索。响应速度是三种策略中最快的。

  ( 提示：如果使用 Qwen / MiMO / 通义等非 GPT 模型，且**串行模式下响应较慢**，建议改用并发检索模式。)

- **新增**：`对话中主动发送表情包` 功能中，新增 `表情包检索模式` 配置项，控制自动收集时如何处理照片、截图等非表情包图像。

  1. `不过滤`：去重后的全部图像，都会进入待筛选图片池；
  2. `宽松过滤 (保留照片等普通图像)`：跳过明显的屏幕截图等，正常图片或无法区分的图像仍会保留。
  3. `严格过滤 (只保留表情包)` ：只收 OneBot/NapCat 明确标记为表情包的图片，过滤其他全部图像。

- **修复**：`群聊智能斗图` 功能中，修复 `参与团战` 功能可能无法触发的问题。

### 插件源

- 我们整合了 [芙提雅 ONLINE](https://www.bilibili.com/video/BV1qR7r6tEs1) 聊天机器人的所有功能增强插件，建立了**第三方专属插件源**。
- 可访问 [https://qingchenwait.github.io/fritia_online_guide/plugin-source.html](https://qingchenwait.github.io/fritia_online_guide/plugin-source.html) 查看插件列表、获取订阅链接和导入方法。



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
