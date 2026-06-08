# DEVELOP

# v2.8.1

- Added the `meme_combat.follow_pattern.distinct_users_required` option to both
  native WebUI config and the Page meme-combat dialog. When enabled, join-pattern
  matching counts unique senders for the same image digest inside the configured
  time window, so repeated sends by one user only count once.
- Hardened proactive emoji replies with an event-level decision marker. The
  configured `trigger_probability` was read from the correct config field, but
  repeated `on_decorating_result` invocations for the same message could sample
  more than once and raise the effective trigger rate.
- Bumped plugin metadata, runtime version, and Page backup-version constant to
  `v2.8.1`.

# v2.8.0

- Added a Page-only Cloudflare R2 imagebed import flow. Users can configure
  account, bucket, auth, prefix, size cap, and scheduled sync settings in the
  Page modal, test the connection, and import remote objects into a separate
  imagebed pending pool before captioning.
- Split the imagebed pipeline from the existing external-plugin import path.
  Imagebed pending images, imported library images, discarded-object history,
  and import state are stored in their own files and folders so the two import
  sources do not share queues or cleanup state.
- Extended the Page with a new imagebed scope tab, imagebed import progress
  panel, imagebed library manager, and a failure dialog that exposes the full
  backend error log in a collapsible block while staying hidden during the
  imagebed config modal.
- Persisted imagebed import settings in the imagebed state file as a mirrored
  recovery copy, so the Cloudflare R2 modal can repopulate after plugin reloads
  even when the plugin config object is recreated.
- Versioned the external destructive-warning preference storage so stale
  "do not show again" state from earlier builds no longer suppresses the
  confirmation overlay for external-plugin import actions.
- Bumped plugin metadata, runtime version, and Page backup-version constant to
  `v2.8.0`.

# v2.6.1

- Adjusted the Page model-fallback provider priority controls: the delete
  action now uses the existing trash icon with white fill, the up/down/delete
  controls are square icon buttons, and the provider list has spacing below the
  provider selector.
- Added the Page-only `page_library_default_view_mode` setting in the More
  Config dialog after `match_confidence_threshold`. The setting is intentionally
  not added to native `_conf_schema.json`, and controls the initial list/gallery
  display mode for manual, solidified, and external image libraries when the
  Page is opened.
- Bumped plugin metadata, runtime version, and Page backup-version constant to
  `v2.6.1`.

# v2.6.0

- Added `model_fallback_options`, a plugin-level model failure fallback config
  group. Page users can choose between inheriting AstrBot's fallback chat model
  list or maintaining a manually ordered provider list; native WebUI users can
  use the `priority_1` / `priority_2` / `priority_3` fallback provider fields.
- Added a shared `_llm_generate_with_provider_fallback` path for plugin-owned LLM
  calls. Default image captioning, proactive emoji analysis, group meme-combat
  quick image analysis, meme-combat matching, and user image-search matching now
  try the configured primary provider first, then manual plugin fallback
  providers, then AstrBot's `provider_settings.fallback_chat_models`.
- Added provider-call timeouts and short failure cooldowns so an unavailable
  provider is skipped for later calls instead of being repeatedly awaited under
  group image bursts.
- Hardened group meme-combat battle detection. Each group now allows only one
  running battle task, clears the image streak when a battle is triggered,
  caps total battle tasks, and enters a failure cooldown if battle analysis
  fails. This prevents repeated-image bursts from stacking slow LLM calls when a
  selected provider is unavailable.
- Added Page controls for "模型失效时的回退选项" below "定时备份" in the More
  Config dialog, including add/remove and up/down priority controls for manual
  fallback providers.
- Included fallback-provider settings in plugin config snapshots, backup export,
  and backup import.
- Bumped plugin metadata, runtime version, and Page backup-version constant to
  `v2.6.0`.

# v2.5.8

- Added an external-import dialog option to import each image's source parent
  directory name as an additional peer feature tag. The choice is passed through
  `external_import_start`, stored as `import_extra_tags`, merged into generated
  tags during captioning, and preserved by backup restore.
- Changed automatic image caption failures caused by provider errors such as
  AstrBot `[ERRO]` / `500 Internal Server Error` into a fatal caption stop with
  source-specific rollback: manual-upload failures are removed, solidified
  failures are returned to the pending pool, and external-import failures remain
  in the import-process panel for another explicit "开始" retry.
- Added a Page error dialog for automatic tag-generation failures. The dialog
  shows the user-facing recovery message and a collapsible "报错信息" block with
  the full backend error detail.
- Bumped plugin metadata, runtime version, and Page backup-version constant to
  `v2.5.8`.

# v2.5.7

- Optimized the Page external-import pending queue for large imports. External
  pending cards are now updated incrementally by image id instead of rebuilding
  the entire grid on every poll, and Page thumbnail loading is concurrency
  limited so hundreds of pending images do not flood the AstrBot web process.
- Changed external-import pending thumbnails to prefer a direct lightweight
  route (`external_import_thumb`) instead of JSON data URLs, avoiding large
  base64 payloads during bulk import. The route falls back to the stored image
  file when no generated thumbnail exists.
- Follow-up bugfix without a version bump: external-import pending thumbnails
  now fall back to the existing Page bridge data-URL API when direct image
  transport is unavailable in the AstrBot Page container, and the thumbnail
  request queue waits for the actual image `load/error` event instead of only
  URL resolution.
- Follow-up bugfix without a version bump: backup restore now preserves
  external-import images whose stored caption status is still `pending` or
  `failed`, even when they already carry filename fallback tags, so untagged
  images return to the Page "导入进程" panel instead of the external library
  manager after export/import.
- Follow-up bugfix without a version bump: the external import directory dialog
  now treats an active external-import auto-caption run as a busy import process
  while pending external images remain, keeps count/start disabled, and shows
  the warning in the yellow stat-hint box until the run finishes or is
  cancelled.
- Reduced external-import worker lock contention by moving file copying out of
  the plugin-wide lock, using metadata-backed digest dedupe at import start, and
  saving lightweight index/state batches during import while deferring full
  config/schema refresh to the end of the import.
- Skipped normal background library sync while an external import task is
  actively copying files, preventing Page polling and the upload watcher from
  repeatedly rescanning the growing external library.
- Added Page dialog protection while an external import is running. Opening the
  external import chooser during an active import now shows a running-import
  message and disables both image counting and import start until the active
  import completes.
- Bumped plugin metadata, runtime version, and Page backup-version constant to
  `v2.5.7`.

# v2.5.6

- Follow-up bugfix without a version bump: external-import destructive warning
  "不再提示" choices now take effect immediately in memory and persist through
  `external_import_state.json`, with localStorage kept as a browser-side cache.
- Added the same default image caption provider warning flow to the external
  import "开始" action before starting automatic tag generation.
- Treated a configured default image caption provider as missing when its
  provider id no longer exists in the current AstrBot service, covering backups
  restored from servers with different provider configurations.
- Added a backend guard so `external_import_start_caption` cannot start without
  a valid current default image caption provider.
- Bumped plugin metadata, runtime version, and Page backup-version constant to
  `v2.5.6`.

# v2.5.5

- Changed the external import flow so copying images into the Page "导入进程"
  queue no longer starts automatic tag generation immediately. External pending
  images stay behind the persisted external pause gate during and after import;
  the Page button now shows "请稍候" while copying, then enables "开始" after the
  import finishes.
- Added the `external_import_start_caption` Page API for the new explicit start
  action while keeping the older pause/resume endpoints for compatibility.
- Replaced unloaded Page thumbnail rendering with a transparent placeholder and
  animated macOS/iOS-style spinner on `img.is-loading`, preserving lazy
  `IntersectionObserver` loading and existing image URL caches.
- Bumped plugin metadata, runtime version, and Page backup-version constant to
  `v2.5.5`.

# v2.5.4

- Fixed external-import pending deletion progress totals by allowing the
  background caption worker to shrink `total` when pending images are deleted
  while a caption job is active.
- Added a yellow hint in the external directory chooser after selecting a
  folder, reminding users to run the explicit image-count step before import.
- Added Page warning overlays for external pending batch delete and external
  caption cancellation. Each warning supports a local "不再提示" checkbox, and
  cancel-caption is disabled when there are no external pending images.
- Bumped plugin metadata, runtime version, and Page backup-version constant to
  `v2.5.4`.

# v2.5.3

- Refined the external import pending-image cards. The card container is now
  borderless, the import date under each image is hidden, and only the thumbnail
  itself keeps a light border while preserving the selected check overlay and
  caption status text.
- Bumped plugin metadata, runtime version, and Page backup-version constant to
  `v2.5.3`.

# v2.5.2

- Improved the external import pending-image grid. Pending cards now use a fixed
  compact width so one or two remaining images no longer stretch across the
  panel, while the external-import panel can show up to 12 compact cards per row
  without changing other library grids.
- Improved the external import directory chooser. The tree now renders as a
  compact folder picker with folder icons, explicit expand/collapse controls,
  default top-level plugin directories only, and a scrollable dialog-local tree
  area for servers with many installed plugins.
- Bumped plugin metadata, runtime version, and Page backup-version constant to
  `v2.5.2`.

# v2.5.1

- Fixed external-import images not rendering in the Page by letting pending
  external images use the same JSON image-data resolution path as the normal
  library, while keeping direct image routes as a fallback. Thumbnail requests
  are now gated by `IntersectionObserver` so large external queues do not fetch
  every image at once.
- Fixed external-import caption pause semantics. The pause flag is now persisted
  in `external_import_state.json`, survives Page navigation and plugin/service
  restarts, excludes only external-import pending images from caption queues, and
  toggles the Page button between pause and resume states.
- Fixed external pending-image deletion progress refresh. Deleting pending
  external images now immediately recomputes and returns caption progress so the
  top progress total/remaining counts update in the Page.
- Added a prominent "从外部导入" action to the external library manager header,
  reusing the same dialog flow as the capabilities-panel import button.
- Bumped plugin metadata, runtime version, and Page backup-version constant to
  `v2.5.1`.

# v2.5.0

- Added Page-only external plugin library import. The Page capabilities panel now
  exposes "从其他插件导入图库", opens a persistent-data directory tree rooted at
  AstrBot `data/plugin_data/`, excludes this plugin's own data directory, and
  requires an explicit image-count step before enabling import.
- Added `backend/external_import.py` with isolated import state, external
  directory validation, incremental streaming file copies, cross-library digest
  dedupe, manual pending-delete digest history, and Page APIs for tree, stat,
  start, status, pending list, pending delete, pause, and cancel.
- Added the external imported library source `external_imported` stored under
  `files/external_import/imported_library/`. Imported images enter the normal
  caption/index flow as pending items and move into the external library manager
  once tagged, while remaining separate from manual uploads and auto-collected
  solidified images.
- Extended the Page library scope switch with "其他插件的图库". This view contains
  a lightweight pending import process panel using lazy direct thumbnail URLs for
  large batches, plus an external library tag-management section that reuses the
  existing list/gallery editor and delete flow.
- Extended backup/export restore snapshots to include external-import image
  files and `external_import_state.json` so imported external libraries and
  manually deleted pending digests survive migration.
- Bumped plugin metadata, runtime version, and Page backup-version constant to
  `v2.5.0`.

# v2.4.8

- Follow-up bugfix without a version bump: accepting images from the pending
  auto-collection pool no longer lets Page polling reset an active caption item
  from `running` back to `pending`. Library sync now preserves `running` while a
  caption task is alive, and recovers stale `running` items when no caption task
  exists.
- Follow-up change without a version bump: capability buttons in the Page now
  share the same column width. The layout keeps at most two buttons per row when
  labels can stay on one line, falls back to one column when needed, and keeps
  the "更多插件配置 ..." button on the final row.
- Added a Page "图库管理" primary action between upload and automatic tag-flow
  settings. It scrolls the Page to the manual/auto library scope switch so the
  library manager starts at the top of the viewport.
- Changed the Page capabilities and global-tags sections to share a responsive
  two-column layout on wide viewports while preserving the existing single-column
  layout on narrow screens. Capability buttons now keep text on one line, flow
  as one or two columns, and keep "更多插件配置 ..." on the final row.
- Updated the Edit Tags dialog title to show only the image filename with suffix
  instead of the full relative path.
- Bumped plugin metadata, runtime version, and Page backup-version constant to
  `v2.4.8`.

# v2.4.6

- Fixed group smart meme-combat join-pattern and battle observation paths.
  Incoming group image jobs now snapshot only the required event fields before
  entering the bounded queue, avoiding later pipeline state changes.
- Fixed repeated-image detection for OneBot/QQ-style image messages by using
  stable image file identifiers for fingerprints while keeping URL/base64 data
  available for sendback.
- Fixed image-only streak detection by checking actual `Plain` components first
  and treating common image placeholders in `message_str` as non-text.
- Fixed battle image selection so valid LLM-selected candidate IDs are accepted
  even when the model omits a confidence value; local fallback still applies.
- Added Page-only tag search bars above the manual-upload library and the
  solidified library image lists. Searches filter the currently loaded images
  locally by tag text and expose an inline clear button without touching backend
  configuration or storage.
- Bumped plugin metadata, runtime version, and Page backup-version constant to
  `v2.4.6`.

# v2.4.5

- Added group smart meme-combat (`meme_combat`) with three subfeatures:
  join-pattern replies for repeated identical group images, probability-based
  related image bursts after this plugin sends an image, and continuous-image
  battle participation using quick two-image semantic analysis plus local
  library retrieval.
- Implemented `backend/meme_combat.py` as a focused mixin with bounded
  per-group in-memory windows, lightweight image fingerprints, a lazily-created
  bounded background observer queue, cooldowns for burst/battle sends, and state
  resets after bot image sends to avoid feedback loops.
- Added native WebUI schema support and Page API support through
  `meme_combat_config`, including provider-option refresh for the battle
  quick-analysis model.
- Added a Page "群聊智能斗图" capability button and configuration overlay with
  total switch, "加入队形", "图片连发", and "参与团战" sections.
- Included `meme_combat` in config snapshots and backup import/export
  normalization.
- Bumped plugin metadata, runtime version, and Page backup-version constant to
  `v2.4.5`.

# v2.4.2

- Updated `main.py` to import AstrBot framework symbols directly from
  `astrbot.api`, `astrbot.api.event`, and `astrbot.api.star` for framework
  reflection checks.
- `SmartImageSenderPlugin` now inherits `Star` directly and uses `Context`,
  `StarTools`, and `register` from `astrbot.api.star` without routing those
  symbols through `backend.common`.
- Bumped plugin metadata, runtime version, and Page backup-version constant to
  `v2.4.2`.

# v2.4.1

- Replaced package-level wildcard imports from `common.py` with explicit imports
  in `main.py` and backend mixin modules to avoid namespace pollution.
- Replaced the `_sync_library` index-shape assertion with an explicit dict
  fallback so optimized Python runs keep the same defensive behavior.
- Bumped plugin metadata, runtime version, and Page backup-version constant to
  `v2.4.1`.

# v2.4.0

- Refactored the former monolithic `SmartImageSenderPlugin` God Object into a `backend/` package of focused mixins while keeping `main.py` as the AstrBot plugin entry point.
- `main.py` now keeps only plugin initialization/termination and AstrBot-decorated message hooks so handler discovery continues to bind against the plugin module.
- Moved Web APIs, LLM conversation helpers, config/schema migration, caption/index maintenance, ZIP backup/restore, auto-collection, image management, retrieval, tag helpers, and path/serialization utilities into separate backend modules without changing route names or runtime function names.
- Bumped plugin metadata, runtime version, and Page backup-version constant to `v2.4.0`.

# v2.3.3

- Updated local AstrBot source at `D:\Models\vibe_coding\astrbot_env\AstrBot`
  to official `origin/master` commit `0711172fa7fb1ceabcc0bc8034d4740c385a76de`.
- Optimized auto image collection so message filters only do lightweight checks
  and enqueue work into a bounded background queue. Queue overflow now skips new
  collection jobs instead of piling up tasks on the AstrBot event path.
- Added short timeout and size-bounded streaming for collected HTTP image URLs,
  avoiding repeated direct use of AstrBot `Image.convert_to_file_path()` when a
  URL can be handled safely by the plugin. Local files and base64 images remain
  supported through the existing fallback path.
- Bumped plugin metadata and runtime version to `v2.3.3`.

# v2.3.2

- Fixed scheduled-backup list action labels in the Page export dialog and the scheduled-backup config section so download/delete render as readable Chinese text.
- Backup list rows now show the backup package version parsed from the ZIP filename between creation time and file size; versions different from the current plugin version are highlighted in yellow.
- Scheduled-backup list APIs now include a `version` field while preserving filename-based fallback compatibility.
- Bumped plugin metadata and runtime version to `v2.3.2`.

# v2.3.1

- Page scheduled-backup list now uses the same download/delete row layout as the export dialog and no longer shows the storage path hint in the Page UI.
- Native WebUI scheduled-backup group hint now includes the concrete backup storage path under `scheduled_backups/`.
- Bumped plugin metadata and runtime version to `v2.3.1`.

# v2.3.0

- Added scheduled backups with a daily time switch, a backup time input, and a retention count.
- Manual export now creates the same ZIP archive as before, stores it in the plugin data directory, and also downloads it for the user.
- Page and native WebUI both expose scheduled-backup settings and the stored backup list.
- The Page export dialog now lists stored backups, supports direct download and deletion, and shows an indeterminate progress bar while a backup is being created or downloaded.
- Bumped plugin metadata and runtime version to `v2.3.0`.

# v2.2.8

- Page pending-pool and solidified-library header counts now display `current/limit 张` using the auto-collection limits from plugin config. Only the current count turns red when it exceeds the configured limit.
- Added a round up-arrow button on the solidified-library header. It uses the same visual style as the list/gallery toggle icons and scrolls back to the manual/auto library scope switch.
- Follow-up change without a version bump: the count turns yellow at 80% capacity and red at or above the limit, and the standalone up-arrow button now matches the full outer height of the list/gallery toggle.
- Follow-up fix without a version bump: deleting the oldest solidified images now preserves imported solidified timestamps and falls back to the original collection timestamp embedded in legacy solidified filenames, so imported/old-version images participate correctly in oldest-first deletion.
- Bumped plugin metadata and runtime version to `v2.2.8`.

# v2.2.7

- Fixed Page backup import so the "overwrite plugin config" checkbox is sent as a real multipart form field instead of being encoded into the uploaded filename. The checkbox remains unchecked by default.
- Updated the main `/caption_import_config` route to accept multipart ZIP uploads directly while keeping the legacy JSON/base64 payload path.
- Backup export now includes auto-collection pending-pool metadata, pending-pool image files, and discarded-image digest history, in addition to plugin config, image index, library metadata, and indexed image files.
- Backup import restores the auto-collection pending pool and discarded digest history using the existing plugin data directory structure.
- Follow-up fix without a version bump: Page backup import now uses AstrBot bridge upload again to avoid protected Page iframe `fetch` failures, and the backend filename decoder correctly strips the `__asmimgimport__::` separator so the overwrite-config checkbox is honored.
- Follow-up change without a version bump: auto collection now stops before image conversion/hash/copy when the pending pool is full, and auto-accept mode also stops when the solidified library has no remaining capacity.
- Follow-up change without a version bump: pending-pool batch accept now returns a capacity warning instead of silently deleting old solidified images. The Page warning lets the user delete the oldest solidified images, expand the solidified limit by the pending-pool limit, or cancel and clear the selection.
- Bumped plugin metadata and runtime version to `v2.2.7`.

# v2.2.6

- Fixed backup export config snapshots so normalized runtime settings are included, including the full `auto_image_collection` group (`enabled`, `include_in_features`, `source_groups`, and related fields).
- Added a sticky header to the Page pending-pool section so batch actions remain reachable while scrolling through long pending pools.
- Added a pending-pool skip action that scrolls directly to the solidified library section.
- Tightened pending-pool card density and changed its grid to clamp between 3 and 6 columns.
- Bumped plugin metadata and runtime version to `v2.2.6`.

# v2.2.5

- Optimized auto-collection hot paths for lightweight servers. New pending images now dedupe against index/pool metadata instead of rescanning and hashing the full data directory for every collected image.
- Batch pending-pool discard now records discarded SHA-256 digests in memory and saves the discarded-history file once per batch instead of once per image.
- Batch pending-pool accept now uses metadata-backed dedupe for manual/solidified libraries and defers solidified-limit cleanup saves/schema refreshes to the existing batch finalization step.
- Bumped plugin metadata and runtime version to `v2.2.5`.

# v2.2.4

- Hardened background caption cancellation cleanup. Running image states are now restored through a shielded cleanup task so cancellation cannot leave images stuck as `running`.
- Moved image SHA-256 calculation in `_sync_library` to a thread-backed async helper, reducing event-loop stalls during large library syncs.
- Reworked backup export/import to use temporary ZIP files and chunked file handling instead of keeping full backup archives and all restored images in memory.
- Page backup import now uses a dedicated file-upload route via AstrBot bridge upload; the legacy JSON/base64 import payload remains supported for compatibility.
- Bumped plugin metadata and runtime version to `v2.2.4`.

# v2.2.3

- Added `auto_reject_discarded` for auto collection. When enabled, manual pending-pool discards are recorded as lightweight SHA-256 digests in plugin data and future matching images are skipped before entering the pending pool.
- The discarded-image history only tracks images discarded from the pending pool; deleting manual uploads or solidified images does not add records.
- Page image management now has a prominent switch between the manual-upload library and the auto-collected library view.
- Pending-pool cards now hide filenames and source group IDs, show only minute-level 24-hour collection time, and use a large translucent selected check overlay.
- Bumped plugin metadata and runtime version to `v2.2.3`.

# v2.2.2

- Fixed pending-pool batch acceptance so accepted images are no longer treated as duplicates against the pending pool itself.
- Batch accept now uses a dedupe scope that covers the manual library and solidified library, then moves accepted images into the solidified library and starts captioning as intended.
- Bumped plugin metadata and runtime version to `v2.2.2`.

# v2.2.1

- Fixed auto-collection reading the wrong config source. The collector filter now reads the plugin's own `auto_image_collection` config instead of AstrBot's global config, so the enable switch and group list take effect.
- Bumped plugin metadata and runtime version to `v2.2.1`.

# v2.2.0

- Added automatic group-image collection for selected QQ groups, with a separate pending pool and solidified library stored in isolated data subfolders.
- Pending images are deduplicated against manual uploads, the pending pool, and the solidified library, and they can be batch accepted or discarded from the Page UI.
- Accepted collected images now enter the same captioning and retrieval flow as manual uploads, while the solidified library stays separate from the manual library in both storage and Page management.
- Added a Page dialog for configuring auto collection and a Page-only selection view for pending images.
- Hardened the Page gallery against sticky-header scroll jumps by preserving scroll position around library re-renders and deferring updates while the page is actively scrolling.
- Bumped plugin metadata and runtime version to `v2.2.0`.

## v2.1.1

- Added a gallery mode to the Page image library. The header now includes a minimal icon toggle for list/gallery views, while list mode keeps the original layout unchanged.
- Gallery mode shows medium-sized image cards in a grid, adds a top-right trash icon delete button on each card, and reveals the familiar file/tags/delete detail row under the selected row without showing the thumbnail again.
- Hardened gallery mode against mobile sticky-header scroll jumps by avoiding unchanged polling re-renders and by observing library width instead of relying on window resize events.
- Gallery cards now keep a square frame and use at least three columns on narrow screens.
- The gallery/list switch stays local to the Page session and does not add any new config options.
- Bumped plugin metadata and runtime version to `v2.1.1`.
- Synced `STRUCTURE.md` with the new Page library layout and control mapping.

## v2.1.0

- Tightened the user-triggered image search flow so it only runs when the current message explicitly wakes the bot: direct private chat, @bot/reply-to-bot, or AstrBot wake-prefix messages.
- Text-like AstrBot wake words are also recognized when they appear inside the current message, matching common phrases such as "来点 XXX 表情包" without enabling plain keyword-only group triggers.
- Non-image wake-prefix messages such as "XXX 晚上好" do not activate this plugin's handler.
- Plain group messages that only contain request keywords no longer trigger image retrieval.
- Added a lightweight local reranking step before LLM image matching. The reranker builds a short candidate list from merged image tags, filename, and name-like query terms, then lets the LLM choose only from that list.
- Updated the image-search prompt to ask the LLM for the top 1-3 matching image IDs in one call.
- The runtime randomly selects from that shortlisted set to preserve response variety.
- Bumped plugin metadata and runtime version to `v2.1.0`.
- Added `STRUCTURE.md` as the cross-device development map for file structure, runtime APIs, Page element mapping, and `main.py` function responsibilities.

## v2.0.5

- Page upload actions now check whether a default image caption provider is configured before opening the upload dialog.
- Added a Page warning dialog that lets admins configure the default image caption provider in place, saving changes immediately through the existing provider config API.

## v2.0.4

- Moved the Page "更多插件配置 ..." action into the capability configuration panel and aligned it to the right side of the capability action row.
- Updated the image library header upload action to use the same prominent primary style as the main upload action.
- Moved the WebUI default image caption provider field to the top of the plugin config while keeping Page and stored-config compatibility.

## v2.0.3

- Upload dialog now closes automatically after images are accepted and queued for background tag generation.
- Moved default image caption provider selection into the tag category settings dialog, with a warning state when no provider is configured.
- WebUI exposes the same default image caption provider setting inside `caption_tag_category_settings`, and the plugin syncs it with AstrBot's system `provider_settings.default_image_caption_provider_id`.
- Image library header is sticky while scrolling through long libraries.

## v2.0.2

- Page initial progress view now shows a standby state until the current page session uploads new files.
- Moved the refresh action into the progress message row and replaced the old lower-left refresh position with an "上传新图片" action.
- Moved image upload from an inline page panel into a shared upload dialog, also reachable from the image library header.
- Added `caption_provider_config` Page API to view and update AstrBot's `provider_settings.default_image_caption_provider_id` from the upload dialog.

## v2.0.1

- Added `user_search_flow` to let admins disable the user-triggered image search flow without affecting proactive emoji replies.
- Added `embed_in_conversation` to `proactive_emoji_reply`; when disabled, the selected emoji image is sent after the LLM reply through `after_message_sent`.
- Plugin Page now separates "为用户寻找表情包" from "更多插件配置"; the former owns request keywords and reply-after-search settings, while the latter keeps retrieval-process settings.
- Page proactive emoji dialog exposes the same embed/independent-send option as WebUI.

## v2.0.0

- Added `proactive_emoji_reply` configuration for probabilistic proactive meme/image replies after ordinary LLM responses.
- WebUI exposes the proactive reply group between the normal image-search reply settings and image tag list.
- Plugin Page adds a "插件能力配置" section with a "对话中主动发送表情包" dialog that reads and saves the same config through plugin Web APIs.
- Runtime hook uses `on_decorating_result`, only runs for LLM-generated results, skips plugin-owned image-search replies, and appends one locally matched image when the configured probability hits.
- The analysis provider can be selected from AstrBot chat providers; empty or unavailable choices fall back to AstrBot's current session provider strategy.

## v1.9.0

- Added `caption_tag_category_settings` to control which categories the image caption prompt should prioritize.
- WebUI exposes preset category selection and custom category input before the image library builder section.
- Plugin Page adds a separate "生成标签类别设定 ..." dialog.
- Page-only recaption option clears existing auto/manual image tags, preserves selected global tags, marks all images as pending, and reuses the existing background caption progress pipeline.
- README intentionally remains unchanged for this internal development change.
