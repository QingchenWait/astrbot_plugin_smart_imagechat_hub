# STRUCTURE

This document is the live development map for `astrbot_plugin_smart_imagechat_hub`.
Update it whenever plugin structure, runtime flow, Web APIs, Page elements, or
configuration semantics change.

## Version

- Current plugin version: `v2.8.4`
- AstrBot requirement: `>=4.24.2`
- Main entry: `main.py`
- Backend package: `backend/`
- Page entry: `pages/image-center-page/index.html`

## File Tree

```text
astrbot_plugin_smart_imagechat_hub/
|-- main.py
|-- metadata.yaml
|-- _conf_schema.json
|-- README.md
|-- DEVELOP.md
|-- STRUCTURE.md
|-- logo.png
|-- backend/
|   |-- __init__.py
|   |-- common.py
|   |-- web_api.py
|   |-- llm_context.py
|   |-- config_schema.py
|   |-- external_import.py
|   |-- imagebed_import.py
|   |-- caption_library.py
|   |-- backup_restore.py
|   |-- auto_collection.py
|   |-- image_management.py
|   |-- meme_combat.py
|   |-- retrieval.py
|   |-- tagging.py
|   `-- utils.py
|-- imgs/
|   |-- how_to_enter_page_ui.png
|   |-- upload_imgs_and_global_tags_in_page_ui.png
|   |-- import_imgs_then_check_tag_generation_step.png
|   |-- config_and_edit_tags_in_page_ui.png
|   `-- import_backup_data_in_page_ui.png
`-- pages/
    `-- image-center-page/
        |-- index.html
        |-- app.js
        `-- style.css
```

## Runtime Data

- Plugin data root: `data/plugin_data/astrbot_plugin_smart_imagechat_hub/`
- Image index cache: `image_index.json`
- Uploaded image files: `files/library_builder/image_files/`
- Auto-collection pending pool: `files/auto_collection/pending_pool/`
- Auto-collection solidified library: `files/auto_collection/solidified_library/`
- Auto-collection pool metadata: `auto_collection_pool.json`
- Auto-collection discarded-image digest history:
  `auto_collection_discarded.json`
- External plugin imported library: `files/external_import/imported_library/`
- External import thumbnail cache: `files/external_import/thumbnails/`
- External plugin import state and manually deleted pending-image digests:
  `external_import_state.json`
  The same state file stores the persistent external-import caption pause flag
  and versioned Page destructive-warning "do not show again" preferences.
- Cloudflare R2 imagebed pending pool: `files/imagebed_import/pending_pool/`
- Cloudflare R2 imagebed imported library: `files/imagebed_import/imported_library/`
- Cloudflare R2 imagebed thumbnail cache: `files/imagebed_import/thumbnails/`
- Cloudflare R2 imagebed import state, last connection/stat snapshot,
  mirrored config recovery copy, last successful sync time, persistent caption
  pause flag, and last error:
  `imagebed_import_state.json`
- Cloudflare R2 imagebed discarded remote-object and digest history:
  `imagebed_import_discarded.json`
- Scheduled backup storage: `scheduled_backups/`
- Plugin config image list: `library_builder.image_files`
- Global tags: `library_builder.global_tags`
- Per-image tags: `image_tags`
- Hidden images excluded from retrieval: `hidden_images`

## Configuration Groups

- `default_image_caption_provider_id`: Mirrors AstrBot system default image
  caption provider setting.
- `library_builder`: Upload source list, global tags, and Page progress link.
- `caption_tag_category_settings`: Controls categories used when generating
  automatic image tags.
- `user_search_flow`: Enables user-requested image search and stores request
  keywords.
- `reply_after_search`: Custom/fallback replies for user image search.
- `proactive_emoji_reply`: Controls probabilistic proactive emoji/image replies
  after normal LLM responses.
- `meme_combat`: Controls group meme-combat behavior. The top-level `enabled`
  switch gates all runtime tracking. `follow_pattern` sends the same image after
  repeated equal images in a short window and can require those matches to come
  from distinct senders. `image_burst` probabilistically sends extra related
  images after this plugin sends an image. `battle` detects continuous
  image-only group dialogue, quickly analyzes two sampled images with the
  configured provider, then retrieves a semantically close library image.
- `auto_image_collection`: Controls the Page and runtime auto-collection flow.
  Images are first stored in the pending pool, then moved into the solidified
  library for captioning and retrieval. `ignored_sender_ids` lists QQ numbers
  whose images are not auto-collected in any group while their messages are
  still processed normally. `filter_obvious_non_meme_images` uses local image
  header width/height/animation checks to skip obvious screenshots or
  high-resolution photos before hashing/copying, without calling an LLM or
  decoding full images. `auto_reject_discarded` optionally records only
  pending-pool manual discards as SHA-256 digests and skips those images during
  future collection. Runtime collection uses a bounded background queue
  (`AUTO_COLLECTION_QUEUE_MAXSIZE`) so image bursts are skipped instead of
  accumulating work on AstrBot's message-processing path.
- `scheduled_backup`: Controls daily automatic ZIP export, retention count, and
  the read-only list of stored backups.
- `model_fallback_options`: Controls model-failure fallback for plugin-owned LLM
  calls. `mode=inherit` directly uses AstrBot's
  `provider_settings.fallback_chat_models` after the primary provider fails.
  `mode=manual` first tries `provider_ids` in priority order, then still falls
  through to AstrBot's fallback chat model list. Native WebUI also exposes
  `priority_1`, `priority_2`, and `priority_3` as a compact ordering fallback
  when drag/reorder controls are unavailable.
- `match_confidence_threshold`: Minimum LLM confidence accepted by retrieval.
- `page_library_default_view_mode`: Hidden native config field used by the Page
  More Config dialog. It stores the initial list/gallery display mode for the
  manual, solidified, external, and imagebed image libraries when the Page is
  opened. Keeping the hidden schema entry prevents AstrBot config-integrity
  cleanup from dropping the Page preference during plugin reloads.
- `imagebed_import`: Page-only Cloudflare R2 imagebed import settings. Stores
  account, bucket, auth, prefix, size cap, and scheduled sync controls without
  adding a native WebUI config group. The same values are mirrored into
  `imagebed_import_state.json` so the Page modal can recover after reloads even
  when AstrBot recreates the plugin config object.

## Backend Modules

`main.py` intentionally remains the only AstrBot plugin entry module. AstrBot
binds decorated handlers by the handler function `__module__`, so the decorated
message hooks stay in `main.py` and call methods supplied by backend mixins.

- `backend/common.py`: shared imports, constants, wake/collection filters, and
  the weak plugin reference used by the auto-collection filter.
- `backend/web_api.py`: Page and Web API route registration plus route handlers.
- `backend/llm_context.py`: LLM persona request, conversation lookup helpers,
  model fallback config normalization, AstrBot fallback-provider discovery, and
  timeout/cooldown wrapped LLM generation. Image captioning can opt out of the
  plugin-level short timeout and short provider-failure cooldown, use direct
  provider calls, and pass through a caption-only request lock so automatic tag
  generation follows AstrBot's native image-caption request path without
  bursty compatible-provider calls.
- `backend/config_schema.py`: JSON state load/save, config migration, and dynamic
  WebUI schema refresh.
- `backend/caption_library.py`: library sync, caption background jobs, progress
  snapshots, plugin config snapshots, and category/provider normalization.
- `backend/backup_restore.py`: ZIP backup creation, scheduled-backup retention,
  import validation, restore logic, and backup serialization helpers.
- `backend/auto_collection.py`: group-image collection queue, URL/local image
  resolution, pending pool, solidified library lifecycle, and collection limits.
- `backend/external_import.py`: Page-only import from sibling AstrBot plugin
  persistent-data directories, directory-tree/stat APIs, incremental copy with
  cross-library digest dedupe, pending external-image lifecycle, direct
  thumbnail serving for pending imports, manual pending delete digest history,
  versioned destructive-warning preferences, and pause/cancel controls for
  imported images waiting for tags.
- `backend/imagebed_import.py`: Page-only Cloudflare R2 import, SigV4 listing
  and connection test helpers, incremental pending-pool import, discarded
  object/digest history, state-backed config recovery for reloads, scheduled
  sync state, and imagebed caption pause/resume/cancel controls.
- `backend/meme_combat.py`: bounded group-image observer queue, in-memory image
  window tracking, join-pattern replies, image-burst sends, continuous-image
  battle detection, quick visual semantic analysis, and cooldown/state reset
  rules to prevent image loops.
- `backend/image_management.py`: per-image tag updates, global tags, deletion,
  and Page image item formatting.
- `backend/retrieval.py`: local candidate ranking, LLM match/proactive emoji
  prompts, automatic image-caption requests, result parsing, and reply
  rendering. `_caption_image` is the shared automatic tag-generation entry for
  manual uploads, auto-collected solidified images, external imports, imagebed
  imports, and recaptioning.
- `backend/tagging.py`: tag extraction, merge/normalization, image type handling,
  and filename-derived fallback tags.
- `backend/utils.py`: JSON extraction, path safety, upload filename creation,
  stable image IDs/digests, caption-only temporary image input preparation,
  config primitive readers, and scalar conversions.

## Web APIs

All routes are registered below `/api/plug/astrbot_plugin_smart_imagechat_hub/`.

- `GET caption_progress`: Current background tag-generation progress plus
  external and imagebed import status snapshots.
- `POST caption_start`: Sync library and start/continue background captioning.
- `GET caption_library`: Image library snapshot, global tags, and per-image tags.
- `GET/POST caption_plugin_config`: Read/write main plugin settings.
  The snapshot includes `model_fallback_options` with provider options for the
  Page fallback-priority editor.
- `GET/POST caption_tag_category_settings`: Read/write caption provider and
  tag-category settings. Optional `recaption_all` queues full regeneration.
- `GET/POST proactive_emoji_config`: Read/write proactive reply settings.
- `GET/POST meme_combat_config`: Read/write group meme-combat settings and
  provider options for the battle quick-analysis model.
- `GET/POST auto_collection_config`: Read/write auto-collection settings.
- `GET auto_collection_pool`: Inspect pending auto-collected images.
- `POST auto_collection_accept`: Batch accept pending images into the
  solidified library.
- `POST auto_collection_discard`: Batch discard pending images.
- `GET external_import_tree`: Return a directory tree rooted at AstrBot
  `data/plugin_data/`, excluding this plugin's own data directory.
- `POST external_import_stat`: Count supported image files under one selected
  external directory and its subdirectories.
- `POST external_import_start`: Start an incremental import from the selected
  external directory into this plugin's external imported library. Optional
  `include_parent_dir_tag=true` stores each source image's parent-directory name
  in `import_extra_tags` so captioning can merge it as a normal feature tag.
- `GET external_import_status`: Return active/last external import counters,
  pending count, external library count, and persistent caption pause state.
- `GET external_import_pending`: Return imported external images that are still
  waiting for automatic tag generation.
- `GET external_import_thumb/<image_id>`: Serve a direct thumbnail for external
  pending images, falling back to the imported image file when no generated
  thumbnail cache exists.
- `POST external_import_delete_pending`: Delete selected pending external images
  and remember their digests so future syncs skip them.
- `POST external_import_pause_caption`: Persistently pause automatic captioning
  of external-import pending images. Paused external images are kept out of the
  shared caption queue until resumed.
- `POST external_import_start_caption`: Explicitly start automatic captioning
  for external-import pending images after the copy/import phase has completed.
- `POST external_import_resume_caption`: Explicitly resume automatic captioning
  for external-import pending images.
- `POST external_import_cancel_caption`: Cancel captioning and remove untagged
  external imported images without recording deleted digests, so future syncs
  may import them again.
- `GET/POST imagebed_import_config`: Read/write Cloudflare R2 imagebed import
  settings. The snapshot includes the current status row shown in the Page
  modal, and the normalized config is mirrored into the imagebed state file so
  reloads can repopulate the modal when the plugin config object is rebuilt.
- `POST imagebed_import_test`: Test the configured Cloudflare R2 endpoint and
  update the last connection/stat snapshot.
- `GET imagebed_import_status`: Return active/last imagebed import counters,
  pending count, imagebed library count, pause state, and last error.
- `POST imagebed_import_start`: Start an incremental import from the configured
  Cloudflare R2 bucket into the separate imagebed pending pool.
- `GET imagebed_import_pending`: Return imported imagebed images that are still
  waiting for automatic tag generation.
- `GET imagebed_import_thumb/<image_id>`: Serve a direct thumbnail for imagebed
  pending images, falling back to the imported image file when no generated
  thumbnail cache exists.
- `POST imagebed_import_delete_pending`: Delete selected pending imagebed
  images and remember their remote-object markers so future syncs skip them.
- `POST imagebed_import_start_caption`: Explicitly start automatic captioning
  for imagebed pending images after the copy/import phase has completed.
- `POST imagebed_import_cancel_caption`: Cancel captioning and remove untagged
  imagebed imported images without recording deleted digests, so future syncs
  may import them again.
- `POST imagebed_import_ack_error`: Acknowledge an imagebed import or caption
  failure after the Page error dialog has been shown.
- `GET/POST scheduled_backup_config`: Read/write scheduled-backup settings and
  refresh the visible backup list schema.
- `GET scheduled_backup_list`: Return the current stored scheduled backups,
  including filename, creation time, size, and filename-derived plugin version.
- `POST scheduled_backup_create`: Create and store one ZIP backup, pruning old
  files to the configured limit.
- `POST scheduled_backup_delete`: Delete one stored scheduled backup.
- `GET scheduled_backup_download/<backup_id>`: Stream one stored scheduled
  backup without deleting it.
- `POST caption_update_tags`: Save one image's manual tags and selected global tags.
- `POST caption_update_global_tags`: Save global reusable tags.
- `POST caption_upload_image`: Upload one image through Page JSON payload.
  Manual uploads may include `selected_global_tags`; valid entries are stored
  on the new indexed image as global tags before background auto-captioning
  starts, so they remain separate from generated `auto_tags`.
- `GET/POST caption_provider_config`: Read/write default image caption provider.
- `POST caption_delete_image`: Delete one indexed image and its file.
- `GET caption_export_config`: Download ZIP backup. The response streams a
  temporary ZIP file and deletes that temporary file after the response ends.
  The ZIP contains `manifest.json`, `config.json`, `image_index.json`,
  `library.json`, indexed image files, `auto_collection_pool.json`,
  `auto_collection_discarded.json`, and pending-pool image files.
- `POST caption_import_config`: Import ZIP backup from multipart uploads or
  legacy JSON/base64 payloads. Multipart fields are `file`, `library_mode`, and
  `overwrite_plugin_config`.
- `POST caption_import_config_file`: Import ZIP backup from a Page file-upload
  bridge route. The upload filename encodes the import mode and overwrite flag,
  and the handler restores them before loading the temporary ZIP file. This is
  retained as a compatibility path; the Page now uses multipart
  `caption_import_config`.
- `GET caption_image/<image_id>`: Serve image file.
- `GET caption_image_data/<image_id>`: Serve image as JSON data URL.

## Page Element Map

Main sections in `pages/image-center-page/index.html`:

- Progress panel: `statusBadge`, `progressBar`, `percentText`, count fields,
  `refreshButton`, `openUploadButton`, `libraryManageButton`,
  `tagCategoryButton`, `importButton`, `exportButton`. `libraryManageButton`
  scrolls the Page to `libraryScopeSwitchRow`.
- Capabilities/global-tags responsive row: `capability-tags-layout` wraps the
  capabilities panel and global tags panel. It renders as two equal-height
  columns on wide viewports and falls back to the previous stacked layout on
  narrow screens.
- Capabilities panel: `userSearchButton`, `proactiveEmojiButton`,
  `autoCollectionButton`, `memeCombatButton`, `externalImportButton`,
  `imagebedImportButton`, `moreConfigButton`. Buttons render
  as one or two equal-width columns depending on available width, keep labels on
  one line, and keep the yellow more-config button on the final row.
- Global tags panel: `globalTagsInput`, `globalTagsPreview`,
  `globalTagsSaveButton`.
- Upload dialog: `uploadInput`, `uploadButton`, and `uploadGlobalTagChoices`.
  The global-tag choices are manual-upload-only batch checkboxes; selected
  entries are sent with each uploaded image as `selected_global_tags`.
- Library panel: `libraryTagSearchInput`, `libraryTagSearchClearButton`,
  `libraryList`, `libraryListModeButton`, `libraryGalleryModeButton`,
  `libraryUploadButton`, `emptyLibraryText`. The search row sits above the image
  list, outside the sticky header, and filters displayed manual images by tag.
- Library scope switch: `manualLibraryScopeButton`,
  `autoCollectionScopeButton`, `externalImportScopeButton`, and
  `imagebedImportScopeButton` choose whether the Page shows the manual upload
  library, the auto-collection pending/solidified sections, the external-import
  process/library sections, or the imagebed process/library sections.
- Pending collection panel: `pendingPoolList`, `pendingPoolMeta`,
  `pendingSkipButton`, `pendingSelectAllButton`, `pendingAcceptButton`,
  `pendingDiscardButton`,
  `emptyPendingPoolText`, `pendingPoolMessage`. Pending cards show only
  month/day hour:minute collection time and use a full-card selected check
  overlay. The section header is sticky while the pending pool is being scrolled,
  and the skip button jumps directly to the solidified library section. When a
  batch accept would exceed the solidified library limit, the Page opens
  `solidifiedCapacityOverlay`; its actions are `capacityDeleteOldestButton`,
  `capacityExpandButton`, and `capacityCancelButton`. `pendingPoolMeta` displays
  `current/limit 张` from `pending_pool_limit` and colors only the current count
  yellow at 80% capacity and red at or above the limit.
- Solidified library panel: `solidifiedLibraryList`,
  `solidifiedListModeButton`, `solidifiedGalleryModeButton`,
  `solidifiedLibraryTagSearchInput`, `solidifiedLibraryTagSearchClearButton`,
  `solidifiedBackToScopeButton`, `solidifiedLibraryMeta`,
  `emptySolidifiedLibraryText`. `solidifiedLibraryMeta` displays `current/limit 张`
  from `solidified_library_limit`, uses the same yellow/red capacity colors, and
  `solidifiedBackToScopeButton` scrolls back to the manual/auto library scope
  switch. The solidified search row uses the same tag-only local filtering as
  the manual library.
- External import process panel: `externalImportPendingList`,
  `externalImportPendingMeta`, `externalImportSelectAllButton`,
  `externalImportDeletePendingButton`, `externalImportPauseButton`,
  `externalImportCancelCaptionButton`, `emptyExternalImportPendingText`, and
  `externalImportMessage`. `externalImportDeletePendingButton` and
  `externalImportCancelCaptionButton` use a Page warning overlay with local
  "do not show again" preferences before destructive actions. These preferences
  are cached in the browser and persisted in `external_import_state.json`.
  `externalImportPauseButton` is the explicit start button: it shows "请稍候"
  and stays disabled while external files are still copying, then enables
  "开始" once pending images are ready; after start it is disabled again and
  cancellation remains on `externalImportCancelCaptionButton`. Pending external
  cards use a fixed compact borderless grid
  (`#externalImportPendingList`) plus `IntersectionObserver` gated lazy image
  loading, a small browser-side thumbnail request queue, incremental DOM updates
  by image id, and direct external thumbnail URLs to avoid JSON/base64 payloads
  during large imports when direct Page image transport is available. If the
  direct image load fails inside the AstrBot Page container, the same thumbnail
  queue falls back to the existing bridge-backed `caption_image_data` data URL
  path and remembers the direct failure for the current Page session. External
  pending cards show only the thumbnail with a light image border and the
  caption status text below it. Starting external caption generation reuses the
  shared provider warning overlay when the current default image caption
  provider is missing or no longer exists in this AstrBot service.
- External imported library panel: `externalLibraryList`,
  `externalListModeButton`, `externalGalleryModeButton`,
  `externalLibraryTagSearchInput`, `externalLibraryTagSearchClearButton`,
  `externalLibraryImportButton`, `externalLibraryMeta`, and
  `emptyExternalLibraryText`. It reuses the same list/gallery image editor, tag
  save, and delete APIs as the manual and solidified libraries while passing
  `library_source=external_imported`. `externalLibraryImportButton` opens the
  same external import dialog as the capabilities-panel import button.
- Imagebed import process panel: `imagebedImportPendingList`,
  `imagebedImportPendingMeta`, `imagebedImportSelectAllButton`,
  `imagebedImportDeletePendingButton`, `imagebedImportPauseButton`,
  `imagebedImportCancelCaptionButton`, `emptyImagebedImportPendingText`, and
  `imagebedImportMessage`. It mirrors the external-import pending flow but uses
  a separate pending pool, a separate caption-start/pause/resume control, and a separate
  `imagebed_imported` library source.
- Imagebed imported library panel: `imagebedLibraryList`,
  `imagebedListModeButton`, `imagebedGalleryModeButton`,
  `imagebedLibraryTagSearchInput`, `imagebedLibraryTagSearchClearButton`,
  `imagebedLibraryImportButton`, `imagebedLibraryMeta`, and
  `emptyImagebedLibraryText`. It reuses the same list/gallery image editor, tag
  save, and delete APIs as the other libraries while passing
  `library_source=imagebed_imported`. `imagebedLibraryImportButton` opens the
  same imagebed import dialog as the capabilities-panel button.
- Auto-collection dialog: `autoCollectionButton`, `autoCollectionOverlay`,
  save/cancel buttons, and the auto-collection config inputs, including
  `autoCollectionMaxSizeInput`, `autoCollectionFilterNonMemeInput`,
  `autoCollectionTtlInput`, `autoCollectionIgnoredSendersInput`, and
  `autoCollectionRejectDiscardedInput`.
- Tag category dialog: `captionProviderInput` selects the default image
  caption provider, and `captionProviderWarning` shows either the missing-model
  warning or the Qwen speed reminder when a Qwen-series provider is selected.
- Meme combat dialog: `memeCombatBattleProviderInput` selects the battle quick
  image semantic analysis provider, and `memeCombatBattleProviderWarning` shows
  the Qwen speed reminder for Qwen-series selections.
- External import dialog: `externalImportOverlay`, `externalImportTree`,
  `externalImportSelectedPath`, `externalImportStatHint`,
  `externalImportParentTagInput`, `externalImportStatButton`,
  `externalImportStatProgress`, `externalImportStatText`,
  `externalImportStartButton`, `externalImportCancelButton`, and close button.
  The tree is a compact scrollable folder picker. Top-level plugin directories
  render first and child directories are shown only after the user expands a
  folder. `externalImportParentTagInput` optionally imports each image's source
  parent-directory name as an additional feature tag. A yellow stat hint is
  shown after directory selection. The start button stays disabled until a
  directory is selected and the explicit stat API returns a positive image
  count. If an external import is copying files, or if the external-import
  auto-caption flow is active while pending external images remain, the dialog
  shows a running-import notice in the yellow stat-hint box and disables both
  the stat and start buttons until polling observes that the process has
  completed or the user cancels the active caption run.
- Imagebed import dialog: `imagebedImportOverlay`, `imagebedAccountIdInput`,
  `imagebedAccessKeyIdInput`, `imagebedSecretAccessKeyInput`,
  `imagebedBucketNameInput`, `imagebedEndpointUrlInput`, `imagebedPrefixInput`,
  `imagebedMaxFileSizeKbInput`, `imagebedScheduledEnabledInput`,
  `imagebedScheduledTimeInput`, `imagebedConnectionStatus`,
  `imagebedLastSyncAt`, `imagebedUnsyncedCount`, `imagebedImportTestButton`,
  `imagebedImportSaveButton`, `imagebedImportCancelButton`,
  `imagebedImportDialogMessage`, and `imagebedImportStartButton`. The modal lets
  the user test the configured R2 endpoint before saving, shows the current
  connection state and unsynced count in the header row, and is the only place
  where imagebed sync settings are edited. If a failure happens while this
  modal is open, the Page keeps the error dialog suppressed because the modal
  already exposes connection test feedback.
- Meme-combat dialog: `memeCombatOverlay`, save/cancel buttons, the total
  enable switch, `memeCombatFollow*` inputs for join-pattern settings including
  `memeCombatFollowDistinctUsersInput`, `memeCombatBurst*` inputs for image
  burst settings, and `memeCombatBattle*` inputs including
  `memeCombatBattleProviderInput`.
- Image editor overlay: `editorOverlay`, `editorImage`, `tagInput`,
  `globalTagChoices`, save/cancel/close buttons. `editorTitle` displays only
  the image filename and suffix, not the full relative library path.
- Caption settings overlay: `tagCategoryOverlay`, `captionProviderInput`,
  preset/custom category inputs, `tagCategoryRecaptionInput`.
- Proactive emoji overlay: enable/provider/meme-only/embed/probability inputs.
- User search overlay: enable switch and request keyword textarea.
- More config overlay: hidden image paths, startup sync, confidence threshold.
  It also includes `configLibraryDefaultViewModeInput`, a Page-only selector
  for the default list/gallery mode used by the three image-library managers on
  later Page opens.
- More config overlay: also includes the scheduled-backup section with enable,
  time, retention, and visible backup list fields. Backup rows show download and
  delete actions plus the package version, highlighting non-current versions.
- More config overlay: also includes the model-failure fallback section below
  scheduled backup. Its Page element ids are
  `modelFallbackModeInheritInput`, `modelFallbackModeManualInput`,
  `modelFallbackManualPanel`, `modelFallbackProviderSelect`,
  `modelFallbackAddButton`, `modelFallbackProviderList`, and
  `modelFallbackEmptyText`. Manual mode stores provider priority in
  `model_fallback_options.provider_ids`, with square up/down icon buttons
  changing order and a trash icon button removing a provider.
- Upload/provider warning/import/error overlays: handle upload, missing
  provider, automatic tag-generation failures, imagebed import failures, and
  backup import workflows. `captionErrorOverlay` displays the source-specific
  recovery message, `captionErrorEyebrow` and `captionErrorTitle` identify the
  failing flow, and `captionErrorDetailText` exposes the full backend error
  detail in a collapsible block. The dialog stays hidden while the imagebed
  config modal is open, then appears on the next Page refresh if a background
  imagebed sync or caption failure was recorded.
  Page backup import uses the AstrBot bridge upload path
  `caption_import_config_file` so it works inside the protected Page iframe.
  Because the bridge upload API only carries a single `file` field, import mode
  and the "overwrite plugin config" checkbox are encoded into the temporary
  uploaded filename and decoded by the backend. The checkbox remains unchecked
  by default.
- Export overlay: `exportOverlay`, `exportCloseButton`, `exportProgressBar`,
  `exportBackupList`, `emptyExportBackupText`, `exportDialogMessage`,
  `exportManualButton`, and `exportCancelButton`. It shows the newest three
  stored backups, supports delete/download actions, shows each package version,
  and shows an indeterminate progress bar during backup creation or download.

`pages/image-center-page/app.js` owns all Page behavior and keeps the local
backup package version constant in sync with `PLUGIN_VERSION`:

- Bridge/API helpers: `ensureBridgeReady`, `pluginApiGet`, `pluginApiPost`,
  `pluginApiDownload`, `uploadBackupConfig`.
- Rendering: `renderProgress`, `renderLibrary`, `renderGlobalTagsEditor`,
  `renderGlobalTagChoices`. `renderLibrary` branches on the local
  `libraryViewMode`: list mode keeps the original row layout, while gallery mode
  renders a responsive grid, top-right trash buttons, and a second-line detail
  row for the selected image. Gallery layout now clamps its per-row card count
  between 3 and 6 columns using `getGalleryColumns()`, which is width-driven
  rather than CSS auto-flow based. When a hidden library panel temporarily
  reports zero width, `getGalleryColumns()` reuses that list's cached
  `data-gallery-columns` value to avoid a transient three-column render while
  switching scopes.
- The manual library and the solidified library now have separate local view
  modes, tag-search state, and selection state. `filteredLibraryImages()` checks
  `merged_tags`, `tags`, `auto_tags`, `manual_tags`, and selected global tags
  before list/gallery rendering; filtering is local to the loaded Page snapshot.
  The Page also keeps a pending-pool selection model for batch accept/discard
  actions.
- Library state and gallery stability: `applyLibraryState` fingerprints the
  library snapshot and skips DOM rebuilds when polling returns unchanged image
  data. `ResizeObserver` is used for gallery layout changes, and
  `scheduleLibraryRender` only rebuilds when the library width changes enough to
  alter the gallery column count. This avoids mobile browser sticky-header
  scroll jumps caused by address-bar resize events or unchanged polling refreshes.
- `applyDefaultLibraryViewMode` applies `page_library_default_view_mode` once
  when the Page first receives a library snapshot, so later polling does not
  overwrite a user-initiated list/gallery switch during the same Page session.
- The Page now preserves the current scroll position around library re-renders
  and defers gallery refreshes while the page is actively scrolling, which
  prevents the sticky header from snapping back on iOS browsers.
- All Page thumbnail renderers use a transparent placeholder plus animated
  `img.is-loading` spinner until the real thumbnail has fired `load`; failed
  image loads fall back to the placeholder instead of showing the browser's
  broken-image icon.
- Dialogs: open/fill/read/save functions for upload, provider warning, tag
  categories, proactive reply, meme combat, auto collection, external import,
  imagebed import, user search, more config, import, error, and editor.
- Provider warning dialog: `providerWarningOverlay` is shared by upload and
  external-import caption start. It can save the default image caption provider
  and then continue the blocked action.
- Data actions: `refreshAll`, `refreshLibrary`, `saveEditor`,
  `saveGlobalTags`, `deleteImage`, `acceptSelectedPendingImages`,
  `discardSelectedPendingImages`, `exportConfig`, `manualExportConfig`,
  `deleteSelectedExternalPendingImages`, `startExternalCaptioning`,
  `cancelExternalCaptioning`, `statExternalImportDirectory`,
  `startExternalImport`, `deleteSelectedImagebedPendingImages`,
  `startImagebedCaptioning`, `cancelImagebedCaptioning`,
  `testImagebedImportConnection`, `openImagebedImportDialog`,
  `saveImagebedImportDialog`, `startImagebedImport`,
  `downloadScheduledBackup`, `deleteScheduledBackup`, `importConfig`,
  `uploadImages`.
  `scrollToLibraryScopeSwitch`, `setLibraryViewMode`, `toggleGallerySelection`,
  `togglePendingSelection`, and `scheduleLibraryRender` keep navigation and
  gallery/list switch state local to the Page session. Imagebed-specific list
  and pending selection logic is isolated from the external-import flow even
  though the UI structure mirrors it closely.

## main.py Flow Map

`SmartImageSenderPlugin` now composes the focused backend mixins and keeps only
core plugin responsibilities in the entry module: constructor state setup,
`initialize`, `terminate`, AstrBot-decorated message hooks, and the admin sync
command. All route handlers and domain logic keep their original method names but
live in `backend/` mixin modules.

### Entry And Hooks

- `SmartImageSenderPlugin.__init__`: Initializes shared runtime state, loads
  index/pool/discarded-history JSON, registers Web APIs via `WebApiMixin`, and
  publishes the weak plugin reference used by auto-collection, meme-combat,
  and imagebed sync/import helpers.
- `initialize`: Runs config migrations, including imagebed config normalization,
  refreshes schemas, syncs the library, starts the upload watcher,
  scheduled-backup loop, auto-collection worker, and imagebed sync loop. The
  meme-combat observer worker is created lazily on the first observed group
  image event after its total switch is enabled.
- `terminate`: Cancels background tasks, waits for caption cleanup, persists
  index/pool/discarded-history data plus imagebed state/discarded data, and
  clears the auto-collection plugin reference.
- `WakeImageRequestFilter.filter`: Allows the user-search handler only for
  explicit wake contexts: private chat, `event.is_at_or_wake_command`, or an
  explicit configured AstrBot `wake_prefix` appearing in the current message.
  It intentionally does not trust `event.is_wake_up()` because other handlers
  can mark an event as awake.
- `_message_has_config_wake_prefix`: Reads AstrBot `wake_prefix` from the active
  config. It allows sentence-internal matching for text-like wake words such as
  names, but avoids treating one-character symbol prefixes such as `/` as
  anywhere-in-message matches.
- `_message_has_image_request_hint`: Keeps the wake filter from activating this
  plugin on non-image wake-prefix messages such as "XXX 晚上好". Sentence-internal
  wake-prefix matching is only used when the same message also looks like an
  image request.
- `on_wake_message`: User-requested image search. Checks message text, feature
  switch, explicit wake state, and request keyword before syncing the library,
  reranking candidates, asking the LLM for a shortlist, and sending one image.
- `on_decorating_result`: Proactive emoji/image append hook for LLM replies.
- `after_message_sent`: Sends queued independent proactive image replies and
  deferred meme-combat burst sends.
- `on_group_meme_combat`: Non-activating placeholder for
  `MemeCombatMessageFilter`. The filter returns `False` after enqueueing the
  group event, so ordinary group messages are observed without waking this
  plugin handler. The background worker keeps bounded in-memory image-window
  state, ignores the bot's own images for new windows, and resets the active
  image statistics whenever this plugin sends an image.
- `sync_images_command`: Admin command to resync the library.

### User Image Search Flow

The user search flow is deliberately lightweight:

1. `_library_candidates` builds candidates from existing index/config data.
   Each candidate carries `tags`, `auto_tags`, `manual_tags`, and
   `selected_global_tags`.
2. `_search_query_profile` extracts query terms, name-like terms, and image type
   terms from the message.
3. `_search_candidate_score` scores candidates locally using filename, merged
   tags, name-like query terms, and type hints.
4. `_rank_search_candidates` keeps only `SEARCH_CANDIDATE_LIMIT` candidates for
   the LLM call.
5. `_match_prompt` asks the LLM to choose the top `1-SEARCH_SELECTION_POOL_SIZE`
   candidate IDs in a single call.
6. `_parse_decision` normalizes the LLM JSON output.
7. `_select_image` enforces `match_confidence_threshold` and randomly selects
   from the shortlisted IDs.
8. `_fallback_match` picks from the locally highest-scored pool if the LLM call
   fails.

### Group Meme Combat Flow

- `MemeCombatMessageFilter` and `_enqueue_meme_combat_event`: observe group
  image traffic as a filter side effect and enqueue it without activating the
  handler. Enqueued jobs snapshot only the required group/sender/message/image
  fields. The queue is bounded by `MEME_COMBAT_QUEUE_MAXSIZE`, so pressure is
  handled by skipping new observations instead of growing memory.
- `_meme_combat_worker_loop` and `_track_group_meme_combat`: process queued
  group messages when `meme_combat.enabled` is true. They store at most
  `MEME_COMBAT_MAX_EVENTS_PER_GROUP` recent image records per group and evict
  old group states beyond `MEME_COMBAT_MAX_GROUPS`.
- Join-pattern mode uses a cheap digest path first: local files are hashed from
  size, suffix, and a small prefix; OneBot/QQ-style stable image file IDs are
  keyed before URL fields; URL/base64 images are keyed by normalized source
  string. When the same digest reaches `same_image_count` inside
  `follow_pattern.time_window_seconds`, the bot sends the same component and
  resets the current group window. If
  `follow_pattern.distinct_users_required` is true, `_maybe_follow_meme_pattern`
  uses `_meme_combat_follow_match_count` to count unique `sender_id` values for
  that digest instead of raw message events.
- Image-burst mode is only counted from image sends performed by this plugin:
  user-search image replies, proactive emoji replies, join-pattern replies,
  battle replies, and burst replies. If probability and cooldown pass, it ranks
  library candidates against the previous image tags and sends up to
  `image_burst.burst_count` related images.
- Battle mode detects a streak of image-only messages inside
  `battle.time_window_seconds`. At `battle.continuous_image_count`, it samples
  two images, resolves them only at trigger time, calls the configured quick
  analysis provider or the current AstrBot session provider, and searches the
  local library from the compact semantic keywords. After sending, the window is
  cleared to avoid self-trigger loops. Since v2.6.0 it also allows only one
  running battle task per group, clears the streak as soon as a battle is
  launched, caps global battle tasks with `MEME_COMBAT_MAX_BATTLE_TASKS`, and
  applies a short per-group failure cooldown when analysis fails.

### Captioning And Indexing

- `_sync_library`: Syncs configured/uploaded images into `image_index.json`,
  preserves manual/global tags, queues missing/stale captions, refreshes config
  schemas, and computes uncached image digests through `_cached_sha256_async` so
  large files do not monopolize the event loop. During Page polling it preserves
  `caption_status == "running"` while the caption task is alive, and
  `_sync_library_if_changed` treats stale `running` items without a live task as
  recoverable work. Background sync skips while external or imagebed import
  tasks are actively copying files, so the import workers can finish and then
  trigger their own final refresh.
- `_create_persistent_backup`: Builds the canonical ZIP backup snapshot, writes
  it to a temporary file, stores it in `scheduled_backups/`, and returns the
  stored backup metadata. `caption_export_config_api` uses the same code path so
  manual export and scheduled backups stay aligned in content and filename
  format.
- `_scheduled_backup_loop`: Sleeps until the configured daily backup time,
  creates one persistent backup, and enforces the retention limit.
- `_scheduled_backup_config_api`, `_scheduled_backup_list_api`,
  `_scheduled_backup_create_api`, `_scheduled_backup_delete_api`, and
  `_scheduled_backup_download_api` expose the scheduled-backup surface. Backup
  metadata includes a `version` field parsed from the ZIP filename.
- `_collect_images_from_event`: Enqueues image collection jobs for selected
  groups. The worker resolves each image to a local path, optionally applies the
  local obvious-non-meme header filter, then stores accepted images in the
  pending pool and leaves them outside retrieval until the user accepts them.
- `AutoImageCollectionMessageFilter`: Lives in `backend/common.py` and reads the
  plugin-owned `auto_image_collection` config through the weak plugin reference,
  so the enable switch and source groups work even when AstrBot global config
  changes elsewhere. The filter skips auto collection for QQ numbers listed in
  `ignored_sender_ids` by matching sender candidates from `get_sender_id()`,
  `message_obj.sender`, and platform `raw_message` fields. The filter only
  performs lightweight sender/capacity checks and queue insertion.
- `_auto_collection_worker_loop`, `_enqueue_auto_collection`, and
  `_resolve_collected_image_path`: Process auto-collected images off the event
  path. HTTP URLs are downloaded with short timeouts and size-bounded streaming;
  local files are used directly; other component forms fall back to
  `Image.convert_to_file_path()` behind a timeout.
- `_is_obvious_non_meme_image`, `_auto_collection_image_header_info`,
  `_jpeg_header_info`, `_webp_header_info`, and `_bmp_header_info`: Lightweight
  auto-collection helpers that read a bounded file header to identify dimensions
  and animation hints for PNG/JPEG/GIF/WebP/BMP. Unknown or animated images are
  allowed through; only clear screenshot/photo-sized images are rejected. Static
  images with `long_side / short_side > 2.5` are rejected as screenshot-like
  long images.
- `_stored_image_digests(include_pending_pool=True)`: Builds the dedupe set for
  collection and, when needed, excludes the pending pool so batch accept does
  not self-conflict with the source pool.
- `_stored_image_digests_from_metadata(include_pending_pool=True)`: Fast
  metadata-only dedupe helper used by auto collection and batch accept to avoid
  full directory scans on hot paths.
- `_store_collected_image`, `_accept_pending_collection_images`,
  `_discard_pending_collection_images`, `_cleanup_collection_pool`: Manage the
  isolated pending pool and solidified library lifecycle. `_store_collected_image`
  checks pending-pool capacity before SHA-256 calculation and file copy, checks
  the discarded digest history when `auto_reject_discarded` is enabled, and
  reuses a caller-supplied digest set when available. `_accept_pending_collection_images`
  rejects manual batch accepts that would exceed `solidified_library_limit`
  unless the Page explicitly asks to delete the oldest solidified images or
  expand the limit. `_delete_oldest_solidified_images` sorts by preserved
  `solidified_at`/`collected_at`, then by legacy solidified filenames containing
  the original collection timestamp, so imported older images remain ordered
  correctly. `_discard_pending_collection_images` is the only path that records
  new discarded digests, and it saves discarded history once per batch.
- `_start_upload_watch_task` / `_watch_uploaded_images`: Background file sync.
  `_sync_library_if_changed` skips background sync while an external import task
  is actively copying files; the external worker performs the final full
  sync/schema refresh after import completion.
- `_start_external_import`, `_external_import_worker`,
  `_copy_external_import_image`, and `_external_import_pending_snapshot`: Copy
  images from selected sibling plugin-data directories into
  `files/external_import/imported_library/`, dedupe against all known plugin
  libraries and pending pools by SHA-256 metadata, mark new images `pending`,
  optionally store a normalized parent-directory tag in `import_extra_tags`, and
  expose the untagged import queue to the Page. The import worker copies files
  outside the plugin-wide lock, saves lightweight index/state batches during
  long imports, and defers full config/schema synchronization to final
  completion so Page actions and other AstrBot tasks are not blocked by bulk IO.
- `_external_import_image_response_path` and `external_import_thumb`: Resolve
  the direct image response path used by external pending thumbnails. A
  generated thumbnail cache may be served when present; otherwise the imported
  source image is streamed directly without JSON/base64 expansion. The Page
  frontend treats this route as the fast path and falls back through
  `caption_image_data/<image_id>` via the AstrBot Page bridge when direct image
  transport cannot be used.
- `_delete_external_pending_images`: Deletes selected untagged external imports
  and records their digests in `external_import_state.json` so future incremental
  imports from other plugin directories skip them, then refreshes caption
  progress counters. `_pause_external_captioning` and
  `_resume_external_captioning` persist the external caption pause flag and keep
  only paused external imports out of the shared caption queue.
  `_start_external_captioning` guards against starting while the import worker
  is still running or no valid current default image caption provider is
  configured, then opens the pause gate and starts the shared caption worker.
  `_cancel_external_captioning` deletes untagged external imports without adding
  those digest records.
- `_test_imagebed_connection`, `_start_imagebed_import`,
  `_imagebed_import_worker`, `_imagebed_list_remote_objects`,
  `_imagebed_import_pending_snapshot`, and `_imagebed_import_image_response_path`:
  Drive the Cloudflare R2 import pipeline. The worker lists objects with a
  lightweight SigV4 GET, skips known or discarded remote objects, streams
  accepted files into `files/imagebed_import/pending_pool/`, and exposes the
  pending queue to the Page. After captioning succeeds the pending files move
  into `files/imagebed_import/imported_library/`; failed captioning rolls back
  to the pending pool or records a fatal error state so the Page can show the
  error dialog later.
- `_start_imagebed_captioning`, `_cancel_imagebed_captioning`,
  `_finalize_captioned_imagebed_item`, `_rollback_caption_failed_imagebed_item`,
  `_record_imagebed_import_error`, and `_ack_imagebed_import_error`: Control the
  imagebed pending queue after import. Captioning can be started explicitly
  from the Page, paused when the queue is blocked, canceled without recording
  new discard history, and acknowledged after a failure dialog is shown.
- `_caption_pending_images`: Processes pending caption jobs and merges
  `import_extra_tags` into successful LLM-generated tags. Provider exceptions or
  `[ERRO]` provider text stop the queue, publish `error_message`,
  `error_detail`, `error_image`, and `error_source` in caption progress, then
  roll back the failed image according to source: manual uploads are removed,
  solidified images return to the pending pool, and external imports remain in
  the import-process panel with captioning paused for an explicit retry. Its
  cancellation cleanup uses a tracked shielded task so images marked `running`
  are restored to `pending` even if the caption worker is cancelled while
  waiting on the plugin lock.
- `_caption_image`: Calls the configured image caption provider through the
  shared provider fallback chain while using direct `provider.text_chat` calls,
  matching AstrBot's native image-caption path. Before the request,
  `_prepare_caption_image_input` may convert GIF/WebP/BMP or other supported
  non-JPEG/PNG files to a temporary JPEG preview and pass large images through
  AstrBot's built-in image compressor; temporary files are removed after the
  call. Caption requests opt out of the plugin-level hard timeout so they
  inherit the AstrBot provider's own timeout/retry behavior, and
  `_run_image_caption_provider_request` serializes caption provider calls with a
  one-second minimum interval. They also opt out of the short provider-failure
  cooldown so an intermittent compatible-provider failure does not make the
  next queued images skip the selected provider. Provider exceptions, timeouts,
  or AstrBot `[ERRO]`/500 response text still try configured fallback providers
  before a `CaptionGenerationError` is raised; if no provider is available it
  returns filename-derived fallback tags instead of blocking.
- `_reset_all_caption_tags_for_new_categories`: Clears auto/manual tags for full
  recaption after category changes.

### Config And Schema

- `_migrate_reply_config`: Migrates legacy reply fields into `reply_after_search`.
- `_migrate_progress_link_config`: Keeps Page link in config.
- `_refresh_image_tag_schema`: Builds WebUI templates for current images.
- `_refresh_caption_tag_category_schema`: Updates provider/category options.
  A saved default image caption provider id is considered configured only when
  it still exists in the current AstrBot provider list; stale ids from restored
  backups show the same warning state as an empty provider.
- `_refresh_proactive_emoji_schema`: Updates proactive provider options.
- `_refresh_meme_combat_schema`: Updates the battle quick-analysis provider
  options for native WebUI.
- `_migrate_model_fallback_config`, `_normalize_model_fallback_config`,
  `_model_fallback_config`, `_model_fallback_snapshot`, and
  `_refresh_model_fallback_schema`: Maintain the plugin fallback-provider
  config, Page snapshot, and native WebUI priority select options. Normalization
  keeps saved provider ids when the current provider list is temporarily empty,
  so service startup does not erase Page manual fallback priority settings
  before providers finish loading.
- `_migrate_imagebed_import_config`, `_imagebed_import_config`,
  `_normalize_imagebed_import_config`, `_set_imagebed_import_config`,
  `_imagebed_config_snapshot`, `_test_imagebed_connection`,
  `_restart_imagebed_sync_task`, `_start_imagebed_sync_task`, and
  `_imagebed_sync_loop`: Maintain the Page-only Cloudflare R2 import config,
  preserve secrets during partial Page updates, mirror the normalized config
  into `imagebed_import_state.json` for reload recovery, keep the
  connection/stat snapshot current, and drive scheduled syncs when enabled.
- `_llm_generate_with_provider_fallback`: Shared LLM call wrapper. Candidate
  order is primary provider, current session provider when the feature inherits
  current chat, manual plugin fallback providers when enabled, then AstrBot
  `fallback_chat_models`. Failed providers are cooled down briefly and every
  normal plugin-owned call is wrapped in a bounded timeout. Passing
  `timeout_seconds=None` or `<= 0` disables the plugin-level `wait_for` wrapper,
  which is used only by automatic image captioning so provider-native timeout
  and retry behavior is preserved.
- `_plugin_config_snapshot`, `_update_plugin_config_from_payload`: Page config
  IO. They include the Page-only `imagebed_import` snapshot and restart the
  imagebed sync task when the payload changes.
- `_tag_category_settings_snapshot`, `_normalize_tag_category_settings`: Caption
  category config IO.
- `_proactive_emoji_snapshot`, `_normalize_proactive_emoji_config`: Proactive
  reply config IO. `_maybe_append_proactive_emoji` also sets
  `PROACTIVE_EMOJI_DECISION_EXTRA_KEY` after the message is eligible so one
  message only samples `trigger_probability` once.
- `_meme_combat_snapshot`, `_normalize_meme_combat_config`: Group meme-combat
  config IO.

### Backup And Restore

- `_backup_snapshot`, `_write_backup_zip_file`, `_stream_temp_file`: Export
  plugin config, index, global tags, image tags, imagebed state/discarded data,
  and image files as a temporary ZIP file without keeping the full archive in
  memory. `_config_snapshot` injects normalized runtime config groups so
  Page/native WebUI settings are not missed by backup export.
- `_receive_backup_import_file`, `_write_legacy_backup_payload_to_temp_file`,
  `_read_backup_zip`: Accept multipart imports or legacy JSON/base64 imports,
  save them to a temporary ZIP path, and validate manifest/config/index data.
- `_restore_backup`, `_restore_backup_images`, `_copy_zip_image_entry_to_temp`,
  `_imported_index_item`: Merge or overwrite image library and index state while
  copying imported images one-by-one from the ZIP through temporary image files.
  Imported index items preserve explicit waiting states (`pending`/`failed`)
  even when the backup item already has filename fallback tags, so untagged
  external-import and imagebed-import images remain in their Page
  import-process panels after backup export/import. External-import
  `import_extra_tags` are preserved so parent-directory tags survive backup
  round-trips, and imagebed metadata fields such as remote object markers,
  import timestamps, and final move timestamps are preserved as well.
- `_restore_backup_external_import_state`,
  `_restore_backup_imagebed_import_state`: Restore source-specific digest and
  persistent Page state, including versioned destructive-warning preferences,
  the imagebed config mirror, the caption pause flag, and last error for
  imagebed, while clearing any active import process from the imported backup.
- `_apply_imported_config`: Restores compatible config fields.
  `model_fallback_options` is normalized on import so stale provider ids from a
  different AstrBot instance are dropped, and `imagebed_import` is normalized so
  stale R2 secrets or invalid endpoints from another instance do not survive the
  restore.
- `_clear_image_library`: Removes current indexed image files for overwrite mode.

### Tag Helpers

- `_tags_from_item`: Runtime merged tag set used for retrieval.
- `_display_tags_from_item`: Page-visible manual-or-auto tags.
- `_normalize_tags`, `_merge_tags`, `_valid_global_tags`: Tag normalization.
- `import_extra_tags`: Optional normalized external-import tags derived from the
  source parent directory. They are merged into generated auto tags rather than
  treated as manual overrides.
- `_filename_tags`: Fallback tags derived from filename.
- `_is_image_type_tag`, `_choose_base_image_type`: Image type tag handling.

### Path And Serialization Helpers

- `_abs_plugin_data_path`: Resolves relative plugin-data paths safely.
- `_norm_rel_path`: Normalizes and validates relative paths.
- `_safe_upload_filename`, `_unique_upload_rel_path`: Upload path creation.
- `_image_id`, `_sha256`, `_cached_sha256_async`, `_cached_sha256`,
  `_sha256_bytes`: Stable IDs and digests.
- `_loads_json_object`: Lenient JSON extraction from LLM output.
- `_cfg_str`, `_cfg_bool`, `_cfg_float`: Runtime config readers.
- `_stored_image_digests`, `_stored_image_digests_from_metadata`,
  `_cached_sha256`, `_all_known_image_digests`: lightweight cross-folder
  deduplication helpers for auto collection and external imports.

## AstrBot Behavior References Used

- `AstrMessageEvent.is_private_chat()` identifies private chats.
- `AstrMessageEvent.is_at_or_wake_command` is set by AstrBot waking checks for
  @bot, reply-to-bot, wake-prefix, and private chat when private wake prefix is
  not required.
- `AstrMessageEvent.is_wake_up()` may also be set by activated plugin handlers,
  so the user-search flow avoids using it as the user-search gate.
- AstrBot `WakingCheckStage` checks wake prefixes, @bot, @all, reply-to-bot, and
  private chat before normal plugin processing.

## Development Notes

- Do not add new config fields for retrieval tuning unless explicitly requested.
- Keep user-search retrieval to one LLM call.
- Keep candidate filtering cheap: simple string/token scoring over existing
  tags and filenames only.
- Preserve random selection from a relevant LLM shortlist to avoid repetitive
  replies.
- Update `DEVELOP.md`, `metadata.yaml`, `PLUGIN_VERSION`, and this file for each
  release-level change.
