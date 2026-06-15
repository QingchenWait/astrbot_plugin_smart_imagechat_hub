# CHANGELOG

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
