const els = {
  statusBadge: document.getElementById("statusBadge"),
  progressBar: document.getElementById("progressBar"),
  percentText: document.getElementById("percentText"),
  totalCount: document.getElementById("totalCount"),
  completedCount: document.getElementById("completedCount"),
  failedCount: document.getElementById("failedCount"),
  remainingCount: document.getElementById("remainingCount"),
  currentImage: document.getElementById("currentImage"),
  libraryCount: document.getElementById("libraryCount"),
  updatedAt: document.getElementById("updatedAt"),
  messageText: document.getElementById("messageText"),
  completeHint: document.getElementById("completeHint"),
  refreshButton: document.getElementById("refreshButton"),
  openUploadButton: document.getElementById("openUploadButton"),
  libraryManageButton: document.getElementById("libraryManageButton"),
  tagCategoryButton: document.getElementById("tagCategoryButton"),
  moreConfigButton: document.getElementById("moreConfigButton"),
  userSearchButton: document.getElementById("userSearchButton"),
  proactiveEmojiButton: document.getElementById("proactiveEmojiButton"),
  autoCollectionButton: document.getElementById("autoCollectionButton"),
  memeCombatButton: document.getElementById("memeCombatButton"),
  externalImportButton: document.getElementById("externalImportButton"),
  imagebedImportButton: document.getElementById("imagebedImportButton"),
  importButton: document.getElementById("importButton"),
  exportButton: document.getElementById("exportButton"),
  uploadInput: document.getElementById("uploadInput"),
  uploadButton: document.getElementById("uploadButton"),
  uploadMessage: document.getElementById("uploadMessage"),
  uploadOverlay: document.getElementById("uploadOverlay"),
  uploadCloseButton: document.getElementById("uploadCloseButton"),
  captionProviderInput: document.getElementById("captionProviderInput"),
  captionProviderWarning: document.getElementById("captionProviderWarning"),
  providerWarningOverlay: document.getElementById("providerWarningOverlay"),
  providerWarningCloseButton: document.getElementById(
    "providerWarningCloseButton",
  ),
  warningCaptionProviderInput: document.getElementById(
    "warningCaptionProviderInput",
  ),
  warningCaptionProviderHint: document.getElementById(
    "warningCaptionProviderHint",
  ),
  providerWarningMessage: document.getElementById("providerWarningMessage"),
  providerWarningContinueButton: document.getElementById(
    "providerWarningContinueButton",
  ),
  providerWarningCancelButton: document.getElementById(
    "providerWarningCancelButton",
  ),
  globalTagsMeta: document.getElementById("globalTagsMeta"),
  globalTagsInput: document.getElementById("globalTagsInput"),
  globalTagsPreview: document.getElementById("globalTagsPreview"),
  globalTagsMessage: document.getElementById("globalTagsMessage"),
  globalTagsSaveButton: document.getElementById("globalTagsSaveButton"),
  manualLibraryScopeButton: document.getElementById(
    "manualLibraryScopeButton",
  ),
  autoCollectionScopeButton: document.getElementById(
    "autoCollectionScopeButton",
  ),
  externalImportScopeButton: document.getElementById(
    "externalImportScopeButton",
  ),
  imagebedImportScopeButton: document.getElementById(
    "imagebedImportScopeButton",
  ),
  manualLibraryScope: document.getElementById("manualLibraryScope"),
  autoCollectionScope: document.getElementById("autoCollectionScope"),
  externalImportScope: document.getElementById("externalImportScope"),
  imagebedImportScope: document.getElementById("imagebedImportScope"),
  libraryScopeSwitchRow: document.getElementById("libraryScopeSwitchRow"),
  libraryMeta: document.getElementById("libraryMeta"),
  libraryListModeButton: document.getElementById("libraryListModeButton"),
  libraryGalleryModeButton: document.getElementById("libraryGalleryModeButton"),
  libraryUploadButton: document.getElementById("libraryUploadButton"),
  libraryTagSearchInput: document.getElementById("libraryTagSearchInput"),
  libraryTagSearchClearButton: document.getElementById(
    "libraryTagSearchClearButton",
  ),
  libraryList: document.getElementById("libraryList"),
  emptyLibraryText: document.getElementById("emptyLibraryText"),
  pendingPoolMeta: document.getElementById("pendingPoolMeta"),
  pendingSkipButton: document.getElementById("pendingSkipButton"),
  pendingSelectAllButton: document.getElementById("pendingSelectAllButton"),
  pendingAcceptButton: document.getElementById("pendingAcceptButton"),
  pendingDiscardButton: document.getElementById("pendingDiscardButton"),
  pendingPoolList: document.getElementById("pendingPoolList"),
  emptyPendingPoolText: document.getElementById("emptyPendingPoolText"),
  pendingPoolMessage: document.getElementById("pendingPoolMessage"),
  solidifiedLibraryMeta: document.getElementById("solidifiedLibraryMeta"),
  solidifiedListModeButton: document.getElementById("solidifiedListModeButton"),
  solidifiedGalleryModeButton: document.getElementById("solidifiedGalleryModeButton"),
  solidifiedBackToScopeButton: document.getElementById(
    "solidifiedBackToScopeButton",
  ),
  solidifiedLibraryTagSearchInput: document.getElementById(
    "solidifiedLibraryTagSearchInput",
  ),
  solidifiedLibraryTagSearchClearButton: document.getElementById(
    "solidifiedLibraryTagSearchClearButton",
  ),
  solidifiedLibraryList: document.getElementById("solidifiedLibraryList"),
  emptySolidifiedLibraryText: document.getElementById(
    "emptySolidifiedLibraryText",
  ),
  externalImportPendingMeta: document.getElementById(
    "externalImportPendingMeta",
  ),
  externalImportSelectAllButton: document.getElementById(
    "externalImportSelectAllButton",
  ),
  externalImportDeletePendingButton: document.getElementById(
    "externalImportDeletePendingButton",
  ),
  externalImportPauseButton: document.getElementById("externalImportPauseButton"),
  externalImportCancelCaptionButton: document.getElementById(
    "externalImportCancelCaptionButton",
  ),
  externalImportPendingList: document.getElementById(
    "externalImportPendingList",
  ),
  emptyExternalImportPendingText: document.getElementById(
    "emptyExternalImportPendingText",
  ),
  externalImportMessage: document.getElementById("externalImportMessage"),
  externalLibraryMeta: document.getElementById("externalLibraryMeta"),
  externalLibraryImportButton: document.getElementById(
    "externalLibraryImportButton",
  ),
  externalListModeButton: document.getElementById("externalListModeButton"),
  externalGalleryModeButton: document.getElementById(
    "externalGalleryModeButton",
  ),
  externalLibraryTagSearchInput: document.getElementById(
    "externalLibraryTagSearchInput",
  ),
  externalLibraryTagSearchClearButton: document.getElementById(
    "externalLibraryTagSearchClearButton",
  ),
  externalLibraryList: document.getElementById("externalLibraryList"),
  emptyExternalLibraryText: document.getElementById("emptyExternalLibraryText"),
  imagebedImportPendingMeta: document.getElementById(
    "imagebedImportPendingMeta",
  ),
  imagebedImportSelectAllButton: document.getElementById(
    "imagebedImportSelectAllButton",
  ),
  imagebedImportDeletePendingButton: document.getElementById(
    "imagebedImportDeletePendingButton",
  ),
  imagebedImportPauseButton: document.getElementById(
    "imagebedImportPauseButton",
  ),
  imagebedImportCancelCaptionButton: document.getElementById(
    "imagebedImportCancelCaptionButton",
  ),
  imagebedImportPendingList: document.getElementById(
    "imagebedImportPendingList",
  ),
  emptyImagebedImportPendingText: document.getElementById(
    "emptyImagebedImportPendingText",
  ),
  imagebedImportDialogMessage: document.getElementById(
    "imagebedImportDialogMessage",
  ),
  imagebedLibraryMeta: document.getElementById("imagebedLibraryMeta"),
  imagebedLibraryImportButton: document.getElementById(
    "imagebedLibraryImportButton",
  ),
  imagebedListModeButton: document.getElementById("imagebedListModeButton"),
  imagebedGalleryModeButton: document.getElementById(
    "imagebedGalleryModeButton",
  ),
  imagebedLibraryTagSearchInput: document.getElementById(
    "imagebedLibraryTagSearchInput",
  ),
  imagebedLibraryTagSearchClearButton: document.getElementById(
    "imagebedLibraryTagSearchClearButton",
  ),
  imagebedLibraryList: document.getElementById("imagebedLibraryList"),
  emptyImagebedLibraryText: document.getElementById("emptyImagebedLibraryText"),
  imagebedImportOverlay: document.getElementById("imagebedImportOverlay"),
  imagebedImportTestButton: document.getElementById("imagebedImportTestButton"),
  imagebedImportSaveButton: document.getElementById("imagebedImportSaveButton"),
  imagebedImportCancelButton: document.getElementById(
    "imagebedImportCancelButton",
  ),
  imagebedConnectionStatus: document.getElementById("imagebedConnectionStatus"),
  imagebedLastSyncAt: document.getElementById("imagebedLastSyncAt"),
  imagebedUnsyncedCount: document.getElementById("imagebedUnsyncedCount"),
  imagebedAccountIdInput: document.getElementById("imagebedAccountIdInput"),
  imagebedAccessKeyIdInput: document.getElementById("imagebedAccessKeyIdInput"),
  imagebedSecretAccessKeyInput: document.getElementById(
    "imagebedSecretAccessKeyInput",
  ),
  imagebedBucketNameInput: document.getElementById("imagebedBucketNameInput"),
  imagebedEndpointUrlInput: document.getElementById("imagebedEndpointUrlInput"),
  imagebedPrefixInput: document.getElementById("imagebedPrefixInput"),
  imagebedMaxFileSizeKbInput: document.getElementById(
    "imagebedMaxFileSizeKbInput",
  ),
  imagebedScheduledEnabledInput: document.getElementById(
    "imagebedScheduledEnabledInput",
  ),
  imagebedScheduledTimeInput: document.getElementById(
    "imagebedScheduledTimeInput",
  ),
  imagebedImportMessage: document.getElementById("imagebedImportMessage"),
  imagebedImportStartButton: document.getElementById(
    "imagebedImportStartButton",
  ),
  editorOverlay: document.getElementById("editorOverlay"),
  editorTitle: document.getElementById("editorTitle"),
  editorImage: document.getElementById("editorImage"),
  tagInput: document.getElementById("tagInput"),
  globalTagChoices: document.getElementById("globalTagChoices"),
  editorMessage: document.getElementById("editorMessage"),
  editorSaveButton: document.getElementById("editorSaveButton"),
  editorCancelButton: document.getElementById("editorCancelButton"),
  editorCloseButton: document.getElementById("editorCloseButton"),
  tagCategoryOverlay: document.getElementById("tagCategoryOverlay"),
  tagCategoryPresetChoices: document.getElementById("tagCategoryPresetChoices"),
  tagCategoryCustomInput: document.getElementById("tagCategoryCustomInput"),
  tagCategoryRecaptionInput: document.getElementById("tagCategoryRecaptionInput"),
  tagCategoryMessage: document.getElementById("tagCategoryMessage"),
  tagCategorySaveButton: document.getElementById("tagCategorySaveButton"),
  tagCategoryCancelButton: document.getElementById("tagCategoryCancelButton"),
  proactiveEmojiOverlay: document.getElementById("proactiveEmojiOverlay"),
  proactiveEmojiEnabledInput: document.getElementById(
    "proactiveEmojiEnabledInput",
  ),
  proactiveEmojiProviderInput: document.getElementById(
    "proactiveEmojiProviderInput",
  ),
  proactiveEmojiMemeOnlyInput: document.getElementById(
    "proactiveEmojiMemeOnlyInput",
  ),
  proactiveEmojiEmbedInput: document.getElementById(
    "proactiveEmojiEmbedInput",
  ),
  proactiveEmojiProbabilityInput: document.getElementById(
    "proactiveEmojiProbabilityInput",
  ),
  proactiveEmojiMessage: document.getElementById("proactiveEmojiMessage"),
  proactiveEmojiSaveButton: document.getElementById("proactiveEmojiSaveButton"),
  proactiveEmojiCancelButton: document.getElementById(
    "proactiveEmojiCancelButton",
  ),
  autoCollectionOverlay: document.getElementById("autoCollectionOverlay"),
  autoCollectionEnabledInput: document.getElementById(
    "autoCollectionEnabledInput",
  ),
  autoCollectionIncludeInput: document.getElementById(
    "autoCollectionIncludeInput",
  ),
  autoCollectionGroupsInput: document.getElementById(
    "autoCollectionGroupsInput",
  ),
  autoCollectionMaxSizeInput: document.getElementById(
    "autoCollectionMaxSizeInput",
  ),
  autoCollectionPendingLimitInput: document.getElementById(
    "autoCollectionPendingLimitInput",
  ),
  autoCollectionTtlInput: document.getElementById("autoCollectionTtlInput"),
  autoCollectionAutoAcceptInput: document.getElementById(
    "autoCollectionAutoAcceptInput",
  ),
  autoCollectionRejectDiscardedInput: document.getElementById(
    "autoCollectionRejectDiscardedInput",
  ),
  autoCollectionSolidifiedLimitInput: document.getElementById(
    "autoCollectionSolidifiedLimitInput",
  ),
  autoCollectionMessage: document.getElementById("autoCollectionMessage"),
  autoCollectionSaveButton: document.getElementById("autoCollectionSaveButton"),
  autoCollectionCancelButton: document.getElementById(
    "autoCollectionCancelButton",
  ),
  memeCombatOverlay: document.getElementById("memeCombatOverlay"),
  memeCombatEnabledInput: document.getElementById("memeCombatEnabledInput"),
  memeCombatFollowEnabledInput: document.getElementById(
    "memeCombatFollowEnabledInput",
  ),
  memeCombatFollowWindowInput: document.getElementById(
    "memeCombatFollowWindowInput",
  ),
  memeCombatFollowCountInput: document.getElementById(
    "memeCombatFollowCountInput",
  ),
  memeCombatFollowDistinctUsersInput: document.getElementById(
    "memeCombatFollowDistinctUsersInput",
  ),
  memeCombatBurstEnabledInput: document.getElementById(
    "memeCombatBurstEnabledInput",
  ),
  memeCombatBurstProbabilityInput: document.getElementById(
    "memeCombatBurstProbabilityInput",
  ),
  memeCombatBurstCountInput: document.getElementById(
    "memeCombatBurstCountInput",
  ),
  memeCombatBattleEnabledInput: document.getElementById(
    "memeCombatBattleEnabledInput",
  ),
  memeCombatBattleWindowInput: document.getElementById(
    "memeCombatBattleWindowInput",
  ),
  memeCombatBattleCountInput: document.getElementById(
    "memeCombatBattleCountInput",
  ),
  memeCombatBattleProviderInput: document.getElementById(
    "memeCombatBattleProviderInput",
  ),
  memeCombatMessage: document.getElementById("memeCombatMessage"),
  memeCombatSaveButton: document.getElementById("memeCombatSaveButton"),
  memeCombatCancelButton: document.getElementById("memeCombatCancelButton"),
  userSearchOverlay: document.getElementById("userSearchOverlay"),
  userSearchEnabledInput: document.getElementById("userSearchEnabledInput"),
  userSearchMessage: document.getElementById("userSearchMessage"),
  userSearchSaveButton: document.getElementById("userSearchSaveButton"),
  userSearchCancelButton: document.getElementById("userSearchCancelButton"),
  configOverlay: document.getElementById("configOverlay"),
  configKeywordsInput: document.getElementById("configKeywordsInput"),
  configHiddenImagesInput: document.getElementById("configHiddenImagesInput"),
  configSyncOnStartupInput: document.getElementById("configSyncOnStartupInput"),
  configConfidenceInput: document.getElementById("configConfidenceInput"),
  configLibraryDefaultViewModeInput: document.getElementById(
    "configLibraryDefaultViewModeInput",
  ),
  scheduledBackupEnabledInput: document.getElementById(
    "scheduledBackupEnabledInput",
  ),
  scheduledBackupTimeInput: document.getElementById("scheduledBackupTimeInput"),
  scheduledBackupLimitInput: document.getElementById("scheduledBackupLimitInput"),
  scheduledBackupConfigList: document.getElementById("scheduledBackupConfigList"),
  modelFallbackModeInheritInput: document.getElementById(
    "modelFallbackModeInheritInput",
  ),
  modelFallbackModeManualInput: document.getElementById(
    "modelFallbackModeManualInput",
  ),
  modelFallbackManualPanel: document.getElementById("modelFallbackManualPanel"),
  modelFallbackProviderSelect: document.getElementById(
    "modelFallbackProviderSelect",
  ),
  modelFallbackAddButton: document.getElementById("modelFallbackAddButton"),
  modelFallbackProviderList: document.getElementById("modelFallbackProviderList"),
  modelFallbackEmptyText: document.getElementById("modelFallbackEmptyText"),
  configUseCustomReplyInput: document.getElementById("configUseCustomReplyInput"),
  configCustomReplyInput: document.getElementById("configCustomReplyInput"),
  configLlmReplyWhenNotFoundInput: document.getElementById(
    "configLlmReplyWhenNotFoundInput",
  ),
  configNotFoundReplyInput: document.getElementById("configNotFoundReplyInput"),
  configEmptyLibraryReplyInput: document.getElementById(
    "configEmptyLibraryReplyInput",
  ),
  configMessage: document.getElementById("configMessage"),
  configSaveButton: document.getElementById("configSaveButton"),
  configCancelButton: document.getElementById("configCancelButton"),
  importOverlay: document.getElementById("importOverlay"),
  importFileInput: document.getElementById("importFileInput"),
  importModeOverwrite: document.getElementById("importModeOverwrite"),
  importModeMerge: document.getElementById("importModeMerge"),
  importOverwriteConfig: document.getElementById("importOverwriteConfig"),
  importMessage: document.getElementById("importMessage"),
  importConfirmButton: document.getElementById("importConfirmButton"),
  importCancelButton: document.getElementById("importCancelButton"),
  importCloseButton: document.getElementById("importCloseButton"),
  externalImportOverlay: document.getElementById("externalImportOverlay"),
  externalImportCloseButton: document.getElementById(
    "externalImportCloseButton",
  ),
  externalImportStatProgress: document.getElementById(
    "externalImportStatProgress",
  ),
  externalImportTree: document.getElementById("externalImportTree"),
  externalImportSelectedPath: document.getElementById(
    "externalImportSelectedPath",
  ),
  externalImportStatHint: document.getElementById("externalImportStatHint"),
  externalImportDialogMessage: document.getElementById(
    "externalImportDialogMessage",
  ),
  externalImportStatButton: document.getElementById("externalImportStatButton"),
  externalImportStatText: document.getElementById("externalImportStatText"),
  externalImportStartButton: document.getElementById("externalImportStartButton"),
  externalImportCancelButton: document.getElementById("externalImportCancelButton"),
  externalImportParentTagInput: document.getElementById(
    "externalImportParentTagInput",
  ),
  exportOverlay: document.getElementById("exportOverlay"),
  exportCloseButton: document.getElementById("exportCloseButton"),
  exportProgressBar: document.getElementById("exportProgressBar"),
  exportBackupList: document.getElementById("exportBackupList"),
  emptyExportBackupText: document.getElementById("emptyExportBackupText"),
  exportDialogMessage: document.getElementById("exportDialogMessage"),
  exportManualButton: document.getElementById("exportManualButton"),
  exportCancelButton: document.getElementById("exportCancelButton"),
  solidifiedCapacityOverlay: document.getElementById("solidifiedCapacityOverlay"),
  capacityWarningText: document.getElementById("capacityWarningText"),
  capacityDeleteOldestButton: document.getElementById("capacityDeleteOldestButton"),
  capacityExpandButton: document.getElementById("capacityExpandButton"),
  capacityCancelButton: document.getElementById("capacityCancelButton"),
  capacityCancelTopButton: document.getElementById("capacityCancelTopButton"),
  externalImportWarningOverlay: document.getElementById(
    "externalImportWarningOverlay",
  ),
  externalImportWarningTitle: document.getElementById(
    "externalImportWarningTitle",
  ),
  externalImportWarningText: document.getElementById("externalImportWarningText"),
  externalImportWarningDontShowInput: document.getElementById(
    "externalImportWarningDontShowInput",
  ),
  externalImportWarningConfirmButton: document.getElementById(
    "externalImportWarningConfirmButton",
  ),
  externalImportWarningCancelButton: document.getElementById(
    "externalImportWarningCancelButton",
  ),
  externalImportWarningCloseButton: document.getElementById(
    "externalImportWarningCloseButton",
  ),
  imagebedImportWarningOverlay: document.getElementById(
    "imagebedImportWarningOverlay",
  ),
  imagebedImportWarningTitle: document.getElementById(
    "imagebedImportWarningTitle",
  ),
  imagebedImportWarningText: document.getElementById(
    "imagebedImportWarningText",
  ),
  imagebedImportWarningDontShowInput: document.getElementById(
    "imagebedImportWarningDontShowInput",
  ),
  imagebedImportWarningConfirmButton: document.getElementById(
    "imagebedImportWarningConfirmButton",
  ),
  imagebedImportWarningCancelButton: document.getElementById(
    "imagebedImportWarningCancelButton",
  ),
  imagebedImportWarningCloseButton: document.getElementById(
    "imagebedImportWarningCloseButton",
  ),
  captionErrorOverlay: document.getElementById("captionErrorOverlay"),
  captionErrorCloseButton: document.getElementById("captionErrorCloseButton"),
  captionErrorOkButton: document.getElementById("captionErrorOkButton"),
  captionErrorMessage: document.getElementById("captionErrorMessage"),
  captionErrorDetailText: document.getElementById("captionErrorDetailText"),
  captionErrorEyebrow: document.getElementById("captionErrorEyebrow"),
  captionErrorTitle: document.getElementById("captionErrorTitle"),
};

const pluginApiBase = "/api/plug/astrbot_plugin_smart_imagechat_hub";
const PLUGIN_VERSION = "v2.8.2";
let bridge = window.AstrBotPluginPage || null;
let bridgeReady = false;
let bridgeUnavailable = false;
let libraryImages = [];
let solidifiedLibraryImages = [];
let externalLibraryImages = [];
let imagebedLibraryImages = [];
let pendingPoolImages = [];
let externalImportPendingImages = [];
let imagebedImportPendingImages = [];
let selectedPendingImageIds = new Set();
let selectedExternalPendingImageIds = new Set();
let selectedImagebedPendingImageIds = new Set();
let globalTags = [];
let editingImage = null;
let globalTagsDirty = false;
let tagCategorySettings = null;
let editorScrollLock = null;
let uploadedInThisPageSession = false;
let uploadProviderCheckInProgress = false;
let warningProviderConfig = null;
let providerWarningContinueAction = null;
let libraryViewMode = "list";
let solidifiedLibraryViewMode = "list";
let externalLibraryViewMode = "list";
let imagebedLibraryViewMode = "list";
let pageDefaultLibraryViewModeApplied = false;
let libraryScopeMode = "manual";
let libraryTagSearchText = "";
let solidifiedLibraryTagSearchText = "";
let externalLibraryTagSearchText = "";
let imagebedLibraryTagSearchText = "";
let selectedGalleryImageId = "";
let selectedSolidifiedGalleryImageId = "";
let selectedExternalGalleryImageId = "";
let selectedImagebedGalleryImageId = "";
let libraryRenderResizeTimer = 0;
let solidifiedLibraryRenderResizeTimer = 0;
let externalLibraryRenderResizeTimer = 0;
let imagebedLibraryRenderResizeTimer = 0;
let lastLibraryListWidth = 0;
let lastSolidifiedLibraryListWidth = 0;
let lastExternalLibraryListWidth = 0;
let lastImagebedLibraryListWidth = 0;
let pageScrollIdleTimer = 0;
let isPageScrolling = false;
let pendingLibraryRender = new Set();
let renderedLibrarySignature = "";
let renderedPendingPoolSignature = "";
let renderedExternalPendingSignature = "";
let renderedImagebedPendingSignature = "";
let lastExternalImportRunning = false;
let lastExternalImportDialogBlocked = false;
let lastImagebedImportRunning = false;
let lastImagebedImportDialogBlocked = false;
let externalCaptionPaused = false;
let imagebedCaptionPaused = false;
const skippedExternalImportWarnings = new Set();
const skippedImagebedImportWarnings = new Set();
let pendingCapacityActionImageIds = [];
let selectedExternalImportDirectory = "";
let externalImportDirectoryStat = null;
let imagebedImportStatusCache = null;
let imagebedImportConnectionVerified = false;
let expandedExternalImportDirectories = new Set();
let currentExternalImportTree = null;
let pendingExternalImportWarningAction = null;
let pendingImagebedImportWarningAction = null;
let lastCaptionErrorSignature = "";
let dismissedCaptionErrorSignature = "";
let lastImagebedErrorSignature = "";
let dismissedImagebedErrorSignature = "";
let activeFailureDialog = null;
let scheduledBackupState = {
  enabled: true,
  backup_time: "06:00",
  backup_limit: 3,
  backup_files: [],
  storage_dir: "",
};
let modelFallbackConfigCache = {
  mode: "inherit",
  provider_ids: [],
  provider_options: [],
  astrbot_fallback_provider_ids: [],
};
let autoCollectionConfigCache = {
  pending_pool_limit: 100,
  solidified_library_limit: 300,
};
const imageUrlCache = new Map();
const thumbnailLoadQueue = [];
let activeThumbnailLoads = 0;
let directThumbnailTransportFailed = false;
const MAX_ACTIVE_THUMBNAIL_LOADS = 6;
const TRANSPARENT_IMAGE_SRC =
  "data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///ywAAAAAAQABAAACAUwAOw==";
const EXTERNAL_IMPORT_DEFAULT_STAT_HINT =
  "请选择目录后点击“统计图库规模”，统计完成后才能开始导入。";
const EXTERNAL_IMPORT_BUSY_STAT_HINT =
  "当前已经有导入进程正在运行，请等待图像全部处理完毕后再继续导入，也可以直接点击“取消导入”按钮取消正在进行的自动标签任务后再执行导入。";
const imageLoadObserver =
  "IntersectionObserver" in window
    ? new IntersectionObserver(
        (entries) => {
          for (const entry of entries) {
            if (!entry.isIntersecting) {
              continue;
            }
            imageLoadObserver.unobserve(entry.target);
            const loader = entry.target.__smartImageLoader;
            if (typeof loader === "function") {
              loader();
            }
          }
        },
        { rootMargin: "240px 0px" },
      )
    : null;
const MANUAL_LIBRARY_SOURCE = "manual_upload";
const SOLIDIFIED_LIBRARY_SOURCE = "auto_collected";
const EXTERNAL_LIBRARY_SOURCE = "external_imported";
const IMAGEBED_LIBRARY_SOURCE = "imagebed_imported";

const LIBRARY_MODE_ICONS = {
  list:
    '<svg viewBox="0 0 16 16" aria-hidden="true" focusable="false"><rect x="2" y="2.5" width="3" height="3" rx="0.8"/><rect x="7" y="3.3" width="7" height="1.4" rx="0.7"/><rect x="2" y="6.5" width="3" height="3" rx="0.8"/><rect x="7" y="7.3" width="7" height="1.4" rx="0.7"/><rect x="2" y="11" width="3" height="3" rx="0.8"/><rect x="7" y="11.8" width="7" height="1.4" rx="0.7"/></svg>',
  gallery:
    '<svg viewBox="0 0 16 16" aria-hidden="true" focusable="false"><rect x="1.8" y="1.8" width="5.1" height="5.1" rx="1"/><rect x="9.1" y="1.8" width="5.1" height="5.1" rx="1"/><rect x="1.8" y="9.1" width="5.1" height="5.1" rx="1"/><rect x="9.1" y="9.1" width="5.1" height="5.1" rx="1"/></svg>',
  trash:
    '<svg viewBox="0 0 16 16" aria-hidden="true" focusable="false"><path d="M6.2 1.6h3.6a1.2 1.2 0 0 1 1.2 1.2V4h2.7a.8.8 0 0 1 0 1.6h-.8V12.3A2.1 2.1 0 0 1 10.8 14.4H5.2a2.1 2.1 0 0 1-2.1-2.1V5.6h-.8a.8.8 0 0 1 0-1.6H5V2.8a1.2 1.2 0 0 1 1.2-1.2Zm.2 2.4h3.2V3.1H6.4V4Zm-1.8 1.6v6.6c0 .3.3.6.6.6h5.2c.3 0 .6-.3.6-.6V5.6H4.8Zm1.1 1.1h1.1v4.3H5.9V6.7Zm2.5 0h1.1v4.3H8.4V6.7Z"/></svg>',
};

const SEARCH_ICON =
  '<svg viewBox="0 0 16 16" aria-hidden="true" focusable="false"><path d="M7.1 2a5.1 5.1 0 1 1 0 10.2A5.1 5.1 0 0 1 7.1 2Zm0 1.6a3.5 3.5 0 1 0 0 7 3.5 3.5 0 0 0 0-7Zm3.9 7.9 2.4 2.4-1.1 1.1-2.4-2.4 1.1-1.1Z"/></svg>';

const CLEAR_ICON =
  '<svg viewBox="0 0 16 16" aria-hidden="true" focusable="false"><path d="m8 6.9 2.1-2.1 1.1 1.1L9.1 8l2.1 2.1-1.1 1.1L8 9.1l-2.1 2.1-1.1-1.1L6.9 8 4.8 5.9l1.1-1.1L8 6.9Z"/></svg>';

const SCOPE_MODE_ICONS = {
  manual:
    '<svg viewBox="0 0 16 16" aria-hidden="true" focusable="false"><path d="M3.2 2.4c0-.6.6-.9 1.1-.6l8.7 5.3c.6.4.4 1.3-.3 1.4l-3.1.5 1.8 3.1c.2.4.1.9-.3 1.1l-1.1.6c-.4.2-.9.1-1.1-.3L7.1 10.4l-2.4 2.4c-.5.5-1.5.2-1.5-.6V2.4z"/></svg>',
  auto:
    '<svg viewBox="0 0 16 16" aria-hidden="true" focusable="false"><rect x="2.2" y="11.2" width="9.6" height="2" rx="1" transform="rotate(-45 2.2 11.2)"/><path d="M10.7 1.8l.7 1.7 1.8.7-1.8.7-.7 1.8-.7-1.8-1.8-.7 1.8-.7.7-1.7z"/><path d="M13.1 8.1l.4 1 .9.4-.9.4-.4 1-.4-1-.9-.4.9-.4.4-1z"/><path d="M4.2 3.2l.4 1 .9.4-.9.4-.4 1-.4-1-.9-.4.9-.4.4-1z"/></svg>',
  external:
    '<svg viewBox="0 0 16 16" aria-hidden="true" focusable="false"><path d="M2.2 3.4c0-.8.6-1.4 1.4-1.4h3l1.2 1.4h4.6c.8 0 1.4.6 1.4 1.4v.8H2.2V3.4z"/><path d="M2.2 6.2h11.6v5.7c0 .8-.6 1.4-1.4 1.4H3.6c-.8 0-1.4-.6-1.4-1.4V6.2zm6.2 1.1H6.8v1.8H5l3 3 3-3H9.4V7.3z"/></svg>',
  imagebed:
    '<svg viewBox="0 0 16 16" aria-hidden="true" focusable="false"><path d="M4 2.3a1 1 0 0 0-1 1v9.4a1 1 0 0 0 1 1h8a1 1 0 0 0 1-1V6.7L9.5 2.3H4zm4.7 1.2 2.6 2.6H8.7V3.5z"/><path d="M5 11.2 6.9 8.8l1.7 2.1 1.3-1.6 1.8 1.9H5z"/></svg>',
};

const UP_ARROW_ICON =
  '<svg viewBox="0 0 16 16" aria-hidden="true" focusable="false"><path d="M8 3.1 3.2 7.9a.9.9 0 0 0 1.3 1.3l2.6-2.6v5.6a.9.9 0 1 0 1.8 0V6.6l2.6 2.6a.9.9 0 1 0 1.3-1.3L8 3.1Z"/></svg>';

const PENDING_SELECTION_ICON =
  '<svg viewBox="0 0 24 24" aria-hidden="true" focusable="false"><path d="M20.3 6.8a1 1 0 0 1 0 1.4l-9.2 9.2a1 1 0 0 1-1.4 0L3.7 11.4a1 1 0 0 1 1.4-1.4l5 5 8.5-8.5a1 1 0 0 1 1.4 0Z"/></svg>';

els.manualLibraryScopeButton.innerHTML = `${SCOPE_MODE_ICONS.manual}<span>手动上传的图库</span>`;
els.autoCollectionScopeButton.innerHTML = `${SCOPE_MODE_ICONS.auto}<span>自动收集的图库</span>`;
els.externalImportScopeButton.innerHTML = `${SCOPE_MODE_ICONS.external}<span>其他插件的图库</span>`;
els.imagebedImportScopeButton.innerHTML = `${SCOPE_MODE_ICONS.imagebed}<span>图床同步的图库</span>`;
els.libraryListModeButton.innerHTML = LIBRARY_MODE_ICONS.list;
els.libraryGalleryModeButton.innerHTML = LIBRARY_MODE_ICONS.gallery;
els.solidifiedListModeButton.innerHTML = LIBRARY_MODE_ICONS.list;
els.solidifiedGalleryModeButton.innerHTML = LIBRARY_MODE_ICONS.gallery;
els.externalListModeButton.innerHTML = LIBRARY_MODE_ICONS.list;
els.externalGalleryModeButton.innerHTML = LIBRARY_MODE_ICONS.gallery;
els.imagebedListModeButton.innerHTML = LIBRARY_MODE_ICONS.list;
els.imagebedGalleryModeButton.innerHTML = LIBRARY_MODE_ICONS.gallery;
els.solidifiedBackToScopeButton.innerHTML = UP_ARROW_ICON;
for (const icon of document.querySelectorAll(".library-search-icon")) {
  icon.innerHTML = SEARCH_ICON;
}
els.libraryTagSearchClearButton.innerHTML = CLEAR_ICON;
els.solidifiedLibraryTagSearchClearButton.innerHTML = CLEAR_ICON;
els.externalLibraryTagSearchClearButton.innerHTML = CLEAR_ICON;

const standbyHintHtml =
  "请点击 [上传新图片] 按钮更新图库，本插件会自动为新图片分配标签。<br>" +
  "本 Page 页面中提供了丰富的功能配置和图库管理方法，请向下划动本页面，进一步进行详细配置。";
const doneHintHtml =
  "图片标签生成已经完成。请向下划动本页面，进一步进行详细配置。";

const statusText = {
  standby: "待命中",
  idle: "空闲",
  pending: "等待中",
  running: "生成中",
  done: "已完成",
  failed: "有失败",
  cancelled: "已取消",
};

function asInt(value) {
  const parsed = Number.parseInt(value, 10);
  return Number.isFinite(parsed) ? parsed : 0;
}

function collectionLimitText(limit) {
  const normalized = asInt(limit);
  return normalized < 0 ? "不限" : String(normalized);
}

function renderLimitedCount(metaElement, count, limit) {
  if (!metaElement) {
    return;
  }
  const current = Math.max(0, asInt(count));
  const normalizedLimit = asInt(limit);
  const currentSpan = document.createElement("span");
  currentSpan.className = "count-current";
  currentSpan.textContent = String(current);
  currentSpan.classList.toggle(
    "is-near-limit",
    normalizedLimit > 0 && current >= normalizedLimit * 0.8 && current < normalizedLimit,
  );
  currentSpan.classList.toggle(
    "is-over-limit",
    normalizedLimit >= 0 && current >= normalizedLimit,
  );

  metaElement.replaceChildren(
    currentSpan,
    document.createTextNode(`/${collectionLimitText(normalizedLimit)} 张`),
  );
}

function renderSolidifiedLibraryCount() {
  renderLimitedCount(
    els.solidifiedLibraryMeta,
    solidifiedLibraryImages.length,
    autoCollectionConfigCache.solidified_library_limit,
  );
}

function formatTime(timestamp) {
  const seconds = asInt(timestamp);
  if (!seconds) {
    return "-";
  }
  return new Date(seconds * 1000).toLocaleString();
}

function formatPendingCollectionTime(timestamp) {
  const seconds = asInt(timestamp);
  if (!seconds) {
    return "-";
  }
  const date = new Date(seconds * 1000);
  if (Number.isNaN(date.getTime())) {
    return "-";
  }
  const month = String(date.getMonth() + 1).padStart(2, "0");
  const day = String(date.getDate()).padStart(2, "0");
  const hour = String(date.getHours()).padStart(2, "0");
  const minute = String(date.getMinutes()).padStart(2, "0");
  return `${month}-${day} ${hour}:${minute}`;
}

function normalizeTags(value) {
  const items = Array.isArray(value)
    ? value
    : String(value || "").split(/[\n,，、;； ]+/);
  const tags = [];
  for (const item of items) {
    const tag = String(item || "").trim();
    if (tag && !tags.includes(tag)) {
      tags.push(tag);
    }
  }
  return tags;
}

function normalizePathList(value) {
  const items = Array.isArray(value)
    ? value
    : String(value || "").split(/[\n,，、;；]+/);
  const paths = [];
  for (const item of items) {
    const relPath = String(item || "")
      .replaceAll("\\", "/")
      .replace(/^\/+/, "")
      .trim();
    if (relPath && !paths.includes(relPath)) {
      paths.push(relPath);
    }
  }
  return paths;
}

function clampConfidence(value) {
  const parsed = Number.parseFloat(value);
  if (!Number.isFinite(parsed)) {
    return 0.45;
  }
  return Math.max(0, Math.min(parsed, 1));
}

function clampProbability(value) {
  const parsed = Number.parseFloat(value);
  if (!Number.isFinite(parsed)) {
    return 0.25;
  }
  return Math.max(0, Math.min(parsed, 1));
}

function clampInt(value, defaultValue, minValue = 0) {
  const parsed = Number.parseInt(value, 10);
  if (!Number.isFinite(parsed)) {
    return defaultValue;
  }
  return Math.max(parsed, minValue);
}

function clampIntRange(value, defaultValue, minValue, maxValue) {
  const parsed = clampInt(value, defaultValue, minValue);
  return Math.min(parsed, maxValue);
}

function normalizeBackupTime(value) {
  const text = String(value || "").trim();
  const match = text.match(/^(\d{1,2}):(\d{1,2})$/);
  if (!match) {
    return "06:00";
  }
  const hour = Math.max(0, Math.min(asInt(match[1]), 23));
  const minute = Math.max(0, Math.min(asInt(match[2]), 59));
  return `${String(hour).padStart(2, "0")}:${String(minute).padStart(2, "0")}`;
}

function formatBytes(bytes) {
  const size = Math.max(0, asInt(bytes));
  if (size >= 1024 * 1024) {
    return `${(size / 1024 / 1024).toFixed(1)} MB`;
  }
  if (size >= 1024) {
    return `${Math.ceil(size / 1024)} KB`;
  }
  return `${size} B`;
}

function extractBackupVersion(filename) {
  const match = String(filename || "").match(/_(v\d+(?:\.\d+){1,3})(?:_\d+)?\.zip$/i);
  return match ? match[1] : "";
}

function setStatus(status) {
  const normalized = status || "idle";
  els.statusBadge.textContent = statusText[normalized] || normalized;
  els.statusBadge.dataset.status = normalized;
}

function setMessage(message) {
  els.messageText.textContent = message;
}

function lockEditorBackgroundScroll() {
  if (editorScrollLock) {
    return;
  }
  const scrollY = window.scrollY || document.documentElement.scrollTop || 0;
  editorScrollLock = {
    scrollY,
    position: document.body.style.position,
    top: document.body.style.top,
    left: document.body.style.left,
    right: document.body.style.right,
    width: document.body.style.width,
    overflowY: document.body.style.overflowY,
  };
  document.body.style.position = "fixed";
  document.body.style.top = `-${scrollY}px`;
  document.body.style.left = "0";
  document.body.style.right = "0";
  document.body.style.width = "100%";
  document.body.style.overflowY = "hidden";
}

function unlockEditorBackgroundScroll() {
  if (!editorScrollLock) {
    return;
  }
  const { scrollY, position, top, left, right, width, overflowY } = editorScrollLock;
  editorScrollLock = null;
  document.body.style.position = position;
  document.body.style.top = top;
  document.body.style.left = left;
  document.body.style.right = right;
  document.body.style.width = width;
  document.body.style.overflowY = overflowY;
  window.scrollTo(0, scrollY);
}

function captureScrollPosition() {
  const scrollingElement = document.scrollingElement || document.documentElement;
  return {
    x:
      window.scrollX ||
      scrollingElement.scrollLeft ||
      document.documentElement.scrollLeft ||
      0,
    y:
      window.scrollY ||
      scrollingElement.scrollTop ||
      document.documentElement.scrollTop ||
      0,
  };
}

function restoreScrollPosition(position) {
  if (!position) {
    return;
  }
  const restore = () => window.scrollTo(position.x, position.y);
  restore();
  window.requestAnimationFrame(restore);
}

function renderLibraryPreservingScroll(source = MANUAL_LIBRARY_SOURCE) {
  const position = captureScrollPosition();
  renderLibrary(source);
  restoreScrollPosition(position);
}

function flushPendingLibraryRenders() {
  if (isPageScrolling || !pendingLibraryRender.size) {
    return;
  }
  const sources = Array.from(pendingLibraryRender);
  pendingLibraryRender.clear();
  for (const source of sources) {
    renderLibraryPreservingScroll(source);
  }
}

function deferLibraryRenderUntilScrollIdle(source = MANUAL_LIBRARY_SOURCE) {
  pendingLibraryRender.add(source);
  if (!isPageScrolling) {
    flushPendingLibraryRenders();
  }
}

function withTimeout(promise, timeoutMs) {
  return new Promise((resolve, reject) => {
    const timer = window.setTimeout(() => {
      reject(new Error("等待 AstrBot Plugin Page Bridge 超时"));
    }, timeoutMs);
    promise.then(
      (value) => {
        window.clearTimeout(timer);
        resolve(value);
      },
      (error) => {
        window.clearTimeout(timer);
        reject(error);
      },
    );
  });
}

async function ensureBridgeReady() {
  if (bridgeUnavailable) {
    throw new Error("AstrBot Plugin Page Bridge 不可用");
  }
  bridge = window.AstrBotPluginPage || bridge;
  if (!bridge) {
    bridgeUnavailable = true;
    throw new Error("AstrBot Plugin Page Bridge 未加载");
  }
  if (bridgeReady) {
    return bridge;
  }
  try {
    await withTimeout(bridge.ready(), 5000);
  } catch (error) {
    bridgeUnavailable = true;
    throw error;
  }
  bridgeReady = true;
  return bridge;
}

function unwrapApiResponse(payload) {
  if (payload && typeof payload === "object" && "data" in payload) {
    return payload.data;
  }
  return payload;
}

async function directPluginApi(method, endpoint, body) {
  const options = {
    method,
    credentials: "same-origin",
    headers: {},
  };
  if (body !== undefined) {
    options.headers["Content-Type"] = "application/json";
    options.body = JSON.stringify(body);
  }
  const response = await fetch(`${pluginApiBase}/${endpoint}`, options);
  if (!response.ok) {
    throw new Error(`HTTP ${response.status}`);
  }
  const payload = await response.json();
  if (payload?.status === "error") {
    throw new Error(payload.message || "插件 API 请求失败");
  }
  return unwrapApiResponse(payload);
}

async function pluginApiGet(endpoint) {
  try {
    const api = await ensureBridgeReady();
    return unwrapApiResponse(await api.apiGet(endpoint));
  } catch (bridgeError) {
    return directPluginApi("GET", endpoint);
  }
}

async function pluginApiPost(endpoint, body) {
  try {
    const api = await ensureBridgeReady();
    return unwrapApiResponse(await api.apiPost(endpoint, body));
  } catch (bridgeError) {
    return directPluginApi("POST", endpoint, body);
  }
}

async function pluginApiDownload(endpoint, filename) {
  const api = await ensureBridgeReady();
  await api.download(endpoint, undefined, filename || "");
}

async function uploadBackupConfig(file, libraryMode, overwritePluginConfig) {
  const api = await ensureBridgeReady();
  const encodedFilename = [
    "__asmimgimport__",
    libraryMode === "overwrite" ? "overwrite" : "merge",
    overwritePluginConfig ? "1" : "0",
    encodeURIComponent(file.name || "backup.zip"),
  ].join("::");
  const uploadFile = new File([file], encodedFilename, {
    type: file.type || "application/zip",
    lastModified: file.lastModified || Date.now(),
  });
  return unwrapApiResponse(
    await api.upload("caption_import_config_file", uploadFile),
  );
}

function readFileAsBase64(file) {
  return new Promise((resolve, reject) => {
    const reader = new FileReader();
    reader.onload = () => {
      const result = String(reader.result || "");
      resolve(result.includes(",") ? result.split(",", 2)[1] : result);
    };
    reader.onerror = () => {
      reject(reader.error || new Error("读取文件失败"));
    };
    reader.readAsDataURL(file);
  });
}

async function uploadImageFile(file) {
  const contentBase64 = await readFileAsBase64(file);
  return pluginApiPost("caption_upload_image", {
    filename: file.name || "image",
    mime_type: file.type || "",
    size: file.size || 0,
    content_base64: contentBase64,
  });
}

function directImageUrl(imageId) {
  return `${pluginApiBase}/caption_image/${encodeURIComponent(imageId)}`;
}

function pendingImageUrl(imageId) {
  return `${pluginApiBase}/collection_pending_image/${encodeURIComponent(imageId)}`;
}

function imageCacheKey(image) {
  return [
    String(image?.id || "").trim(),
    String(image?.mtime || 0),
    String(image?.size || 0),
  ].join(":");
}

async function resolveImageUrl(image) {
  const imageId = String(image?.id || "").trim();
  if (!imageId) {
    return "";
  }
  const preferDirect =
    image?.prefer_direct_thumbnail === true && !directThumbnailTransportFailed;
  const cacheKey = `${preferDirect ? "direct" : "data"}:${imageCacheKey(image)}`;
  if (imageUrlCache.has(cacheKey)) {
    return imageUrlCache.get(cacheKey);
  }

  if (!preferDirect) {
    const dataUrl = await resolveImageDataUrl(image);
    if (dataUrl) {
      return dataUrl;
    }
  }

  const url = image.thumbnail_url || directImageUrl(imageId);
  imageUrlCache.set(cacheKey, url);
  return url;
}

async function resolveImageDataUrl(image) {
  const imageId = String(image?.id || "").trim();
  if (!imageId) {
    return "";
  }
  const cacheKey = `data:${imageCacheKey(image)}`;
  if (imageUrlCache.has(cacheKey)) {
    return imageUrlCache.get(cacheKey);
  }
  const result = await pluginApiGet(`caption_image_data/${imageId}`);
  if (result?.data_url) {
    imageUrlCache.set(cacheKey, result.data_url);
    return result.data_url;
  }
  return "";
}

async function resolvePendingImageUrl(image) {
  const imageId = String(image?.id || "").trim();
  if (!imageId) {
    return "";
  }
  const cacheKey = `pending:${image?.prefer_direct_thumbnail === true ? "direct" : "data"}:${imageCacheKey(image)}`;
  if (imageUrlCache.has(cacheKey)) {
    return imageUrlCache.get(cacheKey);
  }

  if (image?.prefer_direct_thumbnail !== true) {
    const dataUrl = await resolvePendingImageDataUrl(image);
    if (dataUrl) {
      return dataUrl;
    }
  }

  const url = image.thumbnail_url || pendingImageUrl(imageId);
  imageUrlCache.set(cacheKey, url);
  return url;
}

async function resolvePendingImageDataUrl(image) {
  const imageId = String(image?.id || "").trim();
  if (!imageId) {
    return "";
  }
  const cacheKey = `pending:data:${imageCacheKey(image)}`;
  if (imageUrlCache.has(cacheKey)) {
    return imageUrlCache.get(cacheKey);
  }
  const result = await pluginApiGet(`collection_pending_image_data/${imageId}`);
  if (result?.data_url) {
    imageUrlCache.set(cacheKey, result.data_url);
    return result.data_url;
  }
  return "";
}

function setThumbnailLoading(img) {
  if (typeof img.__smartThumbnailCancel === "function") {
    img.__smartThumbnailCancel();
  }
  img.onload = null;
  img.onerror = null;
  img.src = TRANSPARENT_IMAGE_SRC;
  img.classList.add("is-loading");
}

function isDataImageUrl(url) {
  return String(url || "").startsWith("data:");
}

function setThumbnailSource(img, url, fallbackResolver) {
  if (!url) {
    return Promise.resolve(false);
  }
  return new Promise((resolve) => {
    let finished = false;
    let fallbackUsed = false;
    const cleanup = () => {
      img.onload = null;
      img.onerror = null;
      if (img.__smartThumbnailCancel === cancel) {
        img.__smartThumbnailCancel = null;
      }
    };
    const finish = (loaded) => {
      if (finished) {
        return;
      }
      finished = true;
      cleanup();
      img.classList.toggle("is-loading", !loaded);
      if (!loaded) {
        img.src = TRANSPARENT_IMAGE_SRC;
      }
      resolve(loaded);
    };
    const cancel = () => finish(false);
    img.__smartThumbnailCancel = cancel;
    img.onload = () => finish(true);
    img.onerror = () => {
      if (fallbackUsed || typeof fallbackResolver !== "function") {
        finish(false);
        return;
      }
      fallbackUsed = true;
      Promise.resolve()
        .then(fallbackResolver)
        .then((fallbackUrl) => {
          if (fallbackUrl && fallbackUrl !== url) {
            img.src = fallbackUrl;
            return;
          }
          finish(false);
        })
        .catch(() => finish(false));
    };
    img.src = url;
  });
}

function enqueueThumbnailLoad(load) {
  if (typeof load !== "function") {
    return;
  }
  thumbnailLoadQueue.push(load);
  drainThumbnailLoadQueue();
}

function drainThumbnailLoadQueue() {
  while (
    activeThumbnailLoads < MAX_ACTIVE_THUMBNAIL_LOADS &&
    thumbnailLoadQueue.length
  ) {
    const load = thumbnailLoadQueue.shift();
    activeThumbnailLoads += 1;
    Promise.resolve()
      .then(load)
      .finally(() => {
        activeThumbnailLoads = Math.max(0, activeThumbnailLoads - 1);
        drainThumbnailLoadQueue();
      });
  }
}

function applyResolvedImageUrl(img, image) {
  setThumbnailLoading(img);
  const load = () => {
    return resolveImageUrl(image).then(
      (url) => {
        return setThumbnailSource(img, url, () => {
          if (!isDataImageUrl(url)) {
            if (image?.prefer_direct_thumbnail === true) {
              directThumbnailTransportFailed = true;
            }
            return resolveImageDataUrl(image);
          }
          return image.thumbnail_url || directImageUrl(image.id);
        });
      },
      () => {
        return setThumbnailSource(
          img,
          image.thumbnail_url || directImageUrl(image.id),
          () => resolveImageDataUrl(image),
        );
      },
    );
  };
  if (imageLoadObserver) {
    img.__smartImageLoader = () => enqueueThumbnailLoad(load);
    imageLoadObserver.observe(img);
  } else {
    enqueueThumbnailLoad(load);
  }
}

function applyResolvedPendingImageUrl(img, image) {
  setThumbnailLoading(img);
  const load = () => {
    return resolvePendingImageUrl(image).then(
      (url) => {
        return setThumbnailSource(img, url, () => {
          if (!isDataImageUrl(url)) {
            return resolvePendingImageDataUrl(image);
          }
          return image.thumbnail_url || pendingImageUrl(image.id);
        });
      },
      () => {
        return setThumbnailSource(
          img,
          image.thumbnail_url || pendingImageUrl(image.id),
          () => resolvePendingImageDataUrl(image),
        );
      },
    );
  };
  if (imageLoadObserver) {
    img.__smartImageLoader = () => enqueueThumbnailLoad(load);
    imageLoadObserver.observe(img);
  } else {
    enqueueThumbnailLoad(load);
  }
}

function captionErrorSignature(progress) {
  return [
    String(progress?.error_image || ""),
    String(progress?.error_source || ""),
    String(progress?.error_detail || progress?.message || ""),
    String(progress?.updated_at || ""),
  ].join("|");
}

function imagebedImportErrorSignature(error) {
  return [
    String(error?.id || ""),
    String(error?.trigger || ""),
    String(error?.detail || error?.message || ""),
    String(error?.occurred_at || ""),
  ].join("|");
}

function isImagebedImportConfigDialogOpen() {
  return Boolean(
    els.imagebedImportOverlay &&
      !els.imagebedImportOverlay.classList.contains("is-hidden"),
  );
}

function openFailureErrorDialog(kind, options = {}) {
  if (!els.captionErrorOverlay) {
    return;
  }
  activeFailureDialog = {
    kind,
    signature: String(options.signature || ""),
    errorId: String(options.errorId || ""),
  };
  if (els.captionErrorEyebrow) {
    els.captionErrorEyebrow.textContent =
      kind === "imagebed" ? "图床同步错误" : "自动标签错误";
  }
  if (els.captionErrorTitle) {
    els.captionErrorTitle.textContent =
      kind === "imagebed" ? "图床同步失败" : "自动标签进程失败";
  }
  els.captionErrorMessage.textContent = String(
    options.message || "任务执行失败。",
  );
  if (els.captionErrorDetailText) {
    els.captionErrorDetailText.textContent = String(options.detail || "");
  }
  els.captionErrorOverlay.classList.remove("is-hidden");
}

function maybeOpenCaptionErrorDialog(progress) {
  if (
    isImagebedImportConfigDialogOpen() ||
    !els.captionErrorOverlay ||
    progress?.status !== "failed" ||
    (!progress?.error_detail && !progress?.error_message)
  ) {
    return false;
  }
  if (activeFailureDialog && !els.captionErrorOverlay.classList.contains("is-hidden")) {
    return false;
  }
  const signature = captionErrorSignature(progress);
  if (
    !signature ||
    signature === lastCaptionErrorSignature ||
    signature === dismissedCaptionErrorSignature
  ) {
    return false;
  }
  lastCaptionErrorSignature = signature;
  openFailureErrorDialog("caption", {
    signature,
    message: progress.error_message || progress.message || "自动标签进程失败。",
    detail:
      progress.error_detail || progress.error_message || progress.message || "",
  });
  return true;
}

function maybeOpenImagebedImportErrorDialog(status) {
  if (isImagebedImportConfigDialogOpen() || !els.captionErrorOverlay) {
    return false;
  }
  if (activeFailureDialog && !els.captionErrorOverlay.classList.contains("is-hidden")) {
    return false;
  }
  const lastError = status?.last_error || {};
  if (
    !lastError ||
    !lastError.id ||
    lastError.acknowledged ||
    (!lastError.detail && !lastError.message)
  ) {
    return false;
  }
  const signature = imagebedImportErrorSignature(lastError);
  if (
    !signature ||
    signature === lastImagebedErrorSignature ||
    signature === dismissedImagebedErrorSignature
  ) {
    return false;
  }
  lastImagebedErrorSignature = signature;
  openFailureErrorDialog("imagebed", {
    signature,
    errorId: String(lastError.id || ""),
    message: lastError.message || "图床同步失败。",
    detail: lastError.detail || lastError.message || "图床同步失败。",
  });
  return true;
}

async function closeCaptionErrorDialog() {
  const dialog = activeFailureDialog;
  activeFailureDialog = null;
  if (dialog?.kind === "imagebed") {
    dismissedImagebedErrorSignature = dialog.signature;
    if (dialog.errorId) {
      try {
        await pluginApiPost("imagebed_import_ack_error", {
          error_id: dialog.errorId,
        });
      } catch (error) {
        // Best effort: the dialog is already dismissed for this session.
      }
    }
  } else {
    dismissedCaptionErrorSignature = lastCaptionErrorSignature;
  }
  if (!els.captionErrorOverlay) {
    return;
  }
  els.captionErrorOverlay.classList.add("is-hidden");
}

function renderProgress(progress) {
  const percent = Math.max(0, Math.min(asInt(progress.percent), 100));
  const running = progress.running || progress.status === "running";
  const complete = !running && progress.status === "done";
  const standby = !uploadedInThisPageSession;

  setStatus(standby ? "standby" : progress.status);
  els.progressBar.style.width = `${percent}%`;
  els.progressBar.classList.toggle("is-running", running);
  els.percentText.textContent = `${percent}%`;
  els.totalCount.textContent = asInt(progress.total);
  els.completedCount.textContent = asInt(progress.completed);
  els.failedCount.textContent = asInt(progress.failed);
  els.remainingCount.textContent = asInt(progress.remaining);
  els.currentImage.textContent = progress.current_image || "-";
  els.libraryCount.textContent = asInt(progress.library_images);
  els.updatedAt.textContent = formatTime(progress.updated_at);
  els.messageText.textContent = progress.message || "暂无后台任务。";
  if (standby) {
    els.completeHint.innerHTML = standbyHintHtml;
    els.completeHint.classList.remove("is-hidden");
  } else {
    els.completeHint.innerHTML = doneHintHtml;
    els.completeHint.classList.toggle("is-hidden", !complete);
  }
  if (progress?.external_import) {
    renderExternalImportStatus(progress.external_import);
  }
  if (progress?.imagebed_import) {
    renderImagebedImportStatus(progress.imagebed_import);
  }
  const imagebedErrorOpened = maybeOpenImagebedImportErrorDialog(
    progress?.imagebed_import || {},
  );
  if (!imagebedErrorOpened) {
    maybeOpenCaptionErrorDialog(progress);
  }
}

function updateLibraryScopeVisibility() {
  const autoMode = libraryScopeMode === "auto";
  const externalMode = libraryScopeMode === "external";
  const imagebedMode = libraryScopeMode === "imagebed";
  els.manualLibraryScope.classList.toggle(
    "is-hidden",
    autoMode || externalMode || imagebedMode,
  );
  els.autoCollectionScope.classList.toggle("is-hidden", !autoMode);
  els.externalImportScope.classList.toggle("is-hidden", !externalMode);
  els.imagebedImportScope.classList.toggle("is-hidden", !imagebedMode);
  els.manualLibraryScopeButton.setAttribute(
    "aria-pressed",
    String(!autoMode && !externalMode && !imagebedMode),
  );
  els.autoCollectionScopeButton.setAttribute("aria-pressed", String(autoMode));
  els.externalImportScopeButton.setAttribute(
    "aria-pressed",
    String(externalMode),
  );
  els.imagebedImportScopeButton.setAttribute(
    "aria-pressed",
    String(imagebedMode),
  );
}

function setLibraryScopeMode(mode) {
  const normalizedMode =
    mode === "imagebed"
      ? "imagebed"
      : mode === "auto"
        ? "auto"
        : mode === "external"
          ? "external"
          : "manual";
  if (libraryScopeMode === normalizedMode) {
    updateLibraryScopeVisibility();
    return;
  }
  const position = captureScrollPosition();
  libraryScopeMode = normalizedMode;
  updateLibraryScopeVisibility();
  restoreScrollPosition(position);
}

function scrollToLibraryScopeSwitch() {
  const target = els.libraryScopeSwitchRow;
  if (!target) {
    return;
  }
  target.scrollIntoView({
    behavior: "smooth",
    block: "start",
  });
}

function imageDisplayName(image) {
  const rawName = String(image?.filename || image?.rel_path || "").trim();
  if (!rawName) {
    return "编辑图像标签";
  }
  return rawName.replaceAll("\\", "/").split("/").filter(Boolean).pop() || rawName;
}

function tagChip(tag) {
  const chip = document.createElement("span");
  chip.className = "tag-chip";
  chip.textContent = tag;
  return chip;
}

function getLibraryState(source = MANUAL_LIBRARY_SOURCE) {
  if (source === IMAGEBED_LIBRARY_SOURCE) {
    return {
      source: IMAGEBED_LIBRARY_SOURCE,
      images: imagebedLibraryImages,
      list: els.imagebedLibraryList,
      meta: els.imagebedLibraryMeta,
      empty: els.emptyImagebedLibraryText,
      listModeButton: els.imagebedListModeButton,
      galleryModeButton: els.imagebedGalleryModeButton,
      getViewMode: () => imagebedLibraryViewMode,
      setViewModeValue: (mode) => {
        imagebedLibraryViewMode = mode;
      },
      getSearchText: () => imagebedLibraryTagSearchText,
      setSearchText: (text) => {
        imagebedLibraryTagSearchText = text;
      },
      searchInput: els.imagebedLibraryTagSearchInput,
      searchClearButton: els.imagebedLibraryTagSearchClearButton,
      searchRow: els.imagebedLibraryTagSearchInput.closest(".library-search-row"),
      getSelectedId: () => selectedImagebedGalleryImageId,
      setSelectedId: (imageId) => {
        selectedImagebedGalleryImageId = imageId;
      },
      getLastWidth: () => lastImagebedLibraryListWidth,
      setLastWidth: (width) => {
        lastImagebedLibraryListWidth = width;
      },
      getResizeTimer: () => imagebedLibraryRenderResizeTimer,
      setResizeTimer: (timer) => {
        imagebedLibraryRenderResizeTimer = timer;
      },
    };
  }
  if (source === EXTERNAL_LIBRARY_SOURCE) {
    return {
      source: EXTERNAL_LIBRARY_SOURCE,
      images: externalLibraryImages,
      list: els.externalLibraryList,
      meta: els.externalLibraryMeta,
      empty: els.emptyExternalLibraryText,
      listModeButton: els.externalListModeButton,
      galleryModeButton: els.externalGalleryModeButton,
      getViewMode: () => externalLibraryViewMode,
      setViewModeValue: (mode) => {
        externalLibraryViewMode = mode;
      },
      getSearchText: () => externalLibraryTagSearchText,
      setSearchText: (text) => {
        externalLibraryTagSearchText = text;
      },
      searchInput: els.externalLibraryTagSearchInput,
      searchClearButton: els.externalLibraryTagSearchClearButton,
      searchRow: els.externalLibraryTagSearchInput.closest(".library-search-row"),
      getSelectedId: () => selectedExternalGalleryImageId,
      setSelectedId: (imageId) => {
        selectedExternalGalleryImageId = imageId;
      },
      getLastWidth: () => lastExternalLibraryListWidth,
      setLastWidth: (width) => {
        lastExternalLibraryListWidth = width;
      },
      getResizeTimer: () => externalLibraryRenderResizeTimer,
      setResizeTimer: (timer) => {
        externalLibraryRenderResizeTimer = timer;
      },
    };
  }
  if (source === SOLIDIFIED_LIBRARY_SOURCE) {
    return {
      source: SOLIDIFIED_LIBRARY_SOURCE,
      images: solidifiedLibraryImages,
      list: els.solidifiedLibraryList,
      meta: els.solidifiedLibraryMeta,
      empty: els.emptySolidifiedLibraryText,
      listModeButton: els.solidifiedListModeButton,
      galleryModeButton: els.solidifiedGalleryModeButton,
      getViewMode: () => solidifiedLibraryViewMode,
      setViewModeValue: (mode) => {
        solidifiedLibraryViewMode = mode;
      },
      getSearchText: () => solidifiedLibraryTagSearchText,
      setSearchText: (text) => {
        solidifiedLibraryTagSearchText = text;
      },
      searchInput: els.solidifiedLibraryTagSearchInput,
      searchClearButton: els.solidifiedLibraryTagSearchClearButton,
      searchRow: els.solidifiedLibraryTagSearchInput.closest(
        ".library-search-row",
      ),
      getSelectedId: () => selectedSolidifiedGalleryImageId,
      setSelectedId: (imageId) => {
        selectedSolidifiedGalleryImageId = imageId;
      },
      getLastWidth: () => lastSolidifiedLibraryListWidth,
      setLastWidth: (width) => {
        lastSolidifiedLibraryListWidth = width;
      },
      getResizeTimer: () => solidifiedLibraryRenderResizeTimer,
      setResizeTimer: (timer) => {
        solidifiedLibraryRenderResizeTimer = timer;
      },
    };
  }
  return {
    source: MANUAL_LIBRARY_SOURCE,
    images: libraryImages,
    list: els.libraryList,
    meta: els.libraryMeta,
    empty: els.emptyLibraryText,
    listModeButton: els.libraryListModeButton,
    galleryModeButton: els.libraryGalleryModeButton,
    getViewMode: () => libraryViewMode,
    setViewModeValue: (mode) => {
      libraryViewMode = mode;
    },
    getSearchText: () => libraryTagSearchText,
    setSearchText: (text) => {
      libraryTagSearchText = text;
    },
    searchInput: els.libraryTagSearchInput,
    searchClearButton: els.libraryTagSearchClearButton,
    searchRow: els.libraryTagSearchInput.closest(".library-search-row"),
    getSelectedId: () => selectedGalleryImageId,
    setSelectedId: (imageId) => {
      selectedGalleryImageId = imageId;
    },
    getLastWidth: () => lastLibraryListWidth,
    setLastWidth: (width) => {
      lastLibraryListWidth = width;
    },
    getResizeTimer: () => libraryRenderResizeTimer,
    setResizeTimer: (timer) => {
      libraryRenderResizeTimer = timer;
    },
  };
}

function syncSelectedGalleryImage(source = MANUAL_LIBRARY_SOURCE) {
  const state = getLibraryState(source);
  const selectedId = String(state.getSelectedId() || "").trim();
  if (!selectedId) {
    state.setSelectedId("");
    return;
  }
  if (
    !filteredLibraryImages(state).some(
      (image) => String(image?.id || "").trim() === selectedId,
    )
  ) {
    state.setSelectedId("");
  }
}

function libraryImageTags(image) {
  return [
    ...(Array.isArray(image?.merged_tags) ? image.merged_tags : []),
    ...(Array.isArray(image?.tags) ? image.tags : []),
    ...(Array.isArray(image?.auto_tags) ? image.auto_tags : []),
    ...(Array.isArray(image?.manual_tags) ? image.manual_tags : []),
    ...(Array.isArray(image?.selected_global_tags)
      ? image.selected_global_tags
      : []),
  ];
}

function filteredLibraryImages(state) {
  const keyword = String(state.getSearchText() || "").trim().toLocaleLowerCase();
  if (!keyword) {
    return state.images;
  }
  return state.images.filter((image) =>
    libraryImageTags(image).some((tag) =>
      String(tag || "").toLocaleLowerCase().includes(keyword),
    ),
  );
}

function updateLibrarySearchControls(source = MANUAL_LIBRARY_SOURCE) {
  const state = getLibraryState(source);
  const value = String(state.getSearchText() || "");
  if (state.searchInput && state.searchInput.value !== value) {
    state.searchInput.value = value;
  }
  if (state.searchClearButton) {
    state.searchClearButton.classList.toggle("is-hidden", !value);
  }
  updateLibrarySearchWidth(state);
}

function updateLibrarySearchWidth(state) {
  if (!state.searchRow) {
    return;
  }
  const width = state.list.getBoundingClientRect().width || state.list.clientWidth || 0;
  if (!width) {
    state.searchRow.style.removeProperty("--library-search-width");
    return;
  }
  const columns = getGalleryColumns(state.list);
  const fraction = Math.min(1, 3 / Math.max(columns, 3));
  state.searchRow.style.setProperty(
    "--library-search-width",
    `${Math.round(width * fraction)}px`,
  );
}

function setLibraryTagSearch(source, value) {
  const state = getLibraryState(source);
  const nextValue = String(value || "");
  if (state.getSearchText() === nextValue) {
    updateLibrarySearchControls(source);
    return;
  }
  state.setSearchText(nextValue);
  renderLibraryPreservingScroll(source);
}

function updateLibraryModeButtons(source = MANUAL_LIBRARY_SOURCE) {
  const state = getLibraryState(source);
  const galleryMode = state.getViewMode() === "gallery";
  state.listModeButton.setAttribute("aria-pressed", String(!galleryMode));
  state.galleryModeButton.setAttribute("aria-pressed", String(galleryMode));
}

function setLibraryViewMode(mode, source = MANUAL_LIBRARY_SOURCE) {
  const state = getLibraryState(source);
  const nextMode = mode === "gallery" ? "gallery" : "list";
  if (state.getViewMode() === nextMode) {
    updateLibraryModeButtons(source);
    return;
  }
  state.setViewModeValue(nextMode);
  renderLibraryPreservingScroll(source);
}

function applyDefaultLibraryViewMode(mode, force = false) {
  if (pageDefaultLibraryViewModeApplied && !force) {
    return;
  }
  const nextMode = mode === "gallery" ? "gallery" : "list";
  libraryViewMode = nextMode;
  solidifiedLibraryViewMode = nextMode;
  externalLibraryViewMode = nextMode;
  imagebedLibraryViewMode = nextMode;
  pageDefaultLibraryViewModeApplied = true;
}

function scheduleLibraryRender(source = MANUAL_LIBRARY_SOURCE) {
  const state = getLibraryState(source);
  if (state.getViewMode() !== "gallery") {
    return;
  }
  const nextWidth = Math.round(
    state.list.getBoundingClientRect().width || state.list.clientWidth || 0,
  );
  if (nextWidth && nextWidth === state.getLastWidth()) {
    return;
  }
  if (state.getResizeTimer()) {
    window.clearTimeout(state.getResizeTimer());
  }
  const timer = window.setTimeout(() => {
    state.setResizeTimer(0);
    const measuredWidth = Math.round(
      state.list.getBoundingClientRect().width || state.list.clientWidth || 0,
    );
    if (measuredWidth && measuredWidth === state.getLastWidth()) {
      return;
    }
    const currentColumns = Number.parseInt(
      state.list.dataset.galleryColumns || "0",
      10,
    );
    const nextColumns = getGalleryColumns(state.list);
    if (nextColumns === currentColumns) {
      state.setLastWidth(measuredWidth);
      return;
    }
    deferLibraryRenderUntilScrollIdle(source);
  }, 120);
  state.setResizeTimer(timer);
}

function fallbackVisibleLibraryWidth(listEl) {
  for (const candidate of [
    els.libraryList,
    els.solidifiedLibraryList,
    els.externalLibraryList,
    els.imagebedLibraryList,
  ]) {
    if (!candidate || candidate === listEl) {
      continue;
    }
    const width =
      candidate.getBoundingClientRect().width || candidate.clientWidth || 0;
    if (width > 0) {
      return width;
    }
  }
  return 0;
}

function getGalleryColumns(listEl = els.libraryList) {
  const width =
    listEl.getBoundingClientRect().width ||
    listEl.clientWidth ||
    fallbackVisibleLibraryWidth(listEl);
  if (!width) {
    const cachedColumns = Number.parseInt(
      listEl.dataset.galleryColumns || "0",
      10,
    );
    return cachedColumns > 0 ? cachedColumns : 3;
  }
  const cardMinWidth = 90;
  const gap = 12;
  return Math.min(6, Math.max(3, Math.floor((width + gap) / (cardMinWidth + gap))));
}

function createGalleryIconButton(className, icon, label) {
  const button = document.createElement("button");
  button.type = "button";
  button.className = className;
  button.innerHTML = icon;
  button.setAttribute("aria-label", label);
  button.title = label;
  return button;
}

function createGalleryCard(image, isSelected, source = MANUAL_LIBRARY_SOURCE) {
  const card = document.createElement("div");
  card.className = isSelected ? "gallery-card is-selected" : "gallery-card";
  card.setAttribute("role", "button");
  card.setAttribute("tabindex", "0");
  card.setAttribute("aria-pressed", String(!!isSelected));
  card.setAttribute("aria-label", image.filename || image.rel_path || "图片");
  card.dataset.galleryImageId = String(image?.id || "").trim();

  const thumb = document.createElement("img");
  thumb.className = "gallery-thumb";
  thumb.alt = image.filename || image.rel_path;
  thumb.loading = "lazy";
  thumb.decoding = "async";
  applyResolvedImageUrl(thumb, image);

  const deleteButton = createGalleryIconButton(
    "gallery-delete-button",
    LIBRARY_MODE_ICONS.trash,
    "删除",
  );
  deleteButton.addEventListener("click", (event) => {
    event.stopPropagation();
    deleteImage(image, deleteButton, source);
  });

  card.addEventListener("click", () => {
    toggleGallerySelection(image, source);
  });
  card.addEventListener("keydown", (event) => {
    if (event.key === "Enter" || event.key === " ") {
      event.preventDefault();
      toggleGallerySelection(image, source);
    }
  });

  card.append(thumb, deleteButton);
  return card;
}

function setDeleteButtonBusyState(button, busy) {
  button.disabled = busy;
  if (button.classList.contains("gallery-delete-button")) {
    button.setAttribute("aria-label", busy ? "删除中" : "删除");
    button.title = busy ? "删除中" : "删除";
    button.innerHTML = LIBRARY_MODE_ICONS.trash;
    return;
  }
  button.textContent = busy ? "删除中" : "删除";
}

function createGalleryDetailRow(image, source = MANUAL_LIBRARY_SOURCE) {
  const row = document.createElement("div");
  row.className = "gallery-detail-row";

  const main = document.createElement("button");
  main.type = "button";
  main.className = "gallery-detail-main";

  const path = document.createElement("div");
  path.className = "gallery-detail-path";
  path.textContent = image.filename || image.rel_path;

  const relPath = document.createElement("div");
  relPath.className = "gallery-detail-rel-path";
  relPath.textContent = image.rel_path;

  const tags = document.createElement("div");
  tags.className = "tag-list gallery-detail-tags";
  for (const tag of image.merged_tags || image.tags || []) {
    tags.appendChild(tagChip(tag));
  }

  main.append(path, relPath, tags);
  main.addEventListener("click", () => openEditor(image));
  main.addEventListener("keydown", (event) => {
    if (event.key === "Enter" || event.key === " ") {
      event.preventDefault();
      openEditor(image);
    }
  });

  const editButton = document.createElement("button");
  editButton.type = "button";
  editButton.className = "gallery-detail-edit";
  editButton.textContent = "编辑标签";
  editButton.addEventListener("click", (event) => {
    event.stopPropagation();
    openEditor(image);
  });

  const deleteButton = document.createElement("button");
  deleteButton.type = "button";
  deleteButton.className = "danger-button gallery-detail-delete";
  deleteButton.textContent = "删除";
  deleteButton.addEventListener("click", (event) => {
    event.stopPropagation();
    deleteImage(image, deleteButton, source);
  });

  row.addEventListener("click", (event) => {
    if (event.target === row) {
      openEditor(image);
    }
  });

  row.append(main, editButton, deleteButton);
  return row;
}

function renderLibraryListMode(source = MANUAL_LIBRARY_SOURCE) {
  const state = getLibraryState(source);
  const images = filteredLibraryImages(state);
  for (const image of images) {
    const row = document.createElement("button");
    row.type = "button";
    row.className = "library-row";
    row.addEventListener("click", () => openEditor(image));

    const thumb = document.createElement("img");
    thumb.className = "thumb";
    thumb.alt = image.filename || image.rel_path;
    thumb.loading = "lazy";
    thumb.decoding = "async";
    applyResolvedImageUrl(thumb, image);

    const content = document.createElement("div");
    content.className = "library-row-content";

    const path = document.createElement("div");
    path.className = "image-path";
    path.textContent = image.rel_path;

    const tags = document.createElement("div");
    tags.className = "tag-list";
    for (const tag of image.merged_tags || image.tags || []) {
      tags.appendChild(tagChip(tag));
    }

    const deleteButton = document.createElement("button");
    deleteButton.type = "button";
    deleteButton.className = "danger-button";
    deleteButton.textContent = "删除";
    deleteButton.addEventListener("click", (event) => {
      event.stopPropagation();
      deleteImage(image, deleteButton, source);
    });

    content.append(path, tags);
    row.append(thumb, content, deleteButton);
    state.list.appendChild(row);
  }
}

function toggleGallerySelection(image, source = MANUAL_LIBRARY_SOURCE) {
  const state = getLibraryState(source);
  const imageId = String(image?.id || "").trim();
  if (!imageId) {
    return;
  }
  state.setSelectedId(state.getSelectedId() === imageId ? "" : imageId);
  syncGallerySelectionView(source);
}

function renderLibraryGalleryMode(source = MANUAL_LIBRARY_SOURCE) {
  const state = getLibraryState(source);
  const images = filteredLibraryImages(state);
  const columns = getGalleryColumns(state.list);
  state.list.dataset.galleryColumns = String(columns);
  state.setLastWidth(
    Math.round(
      state.list.getBoundingClientRect().width || state.list.clientWidth || 0,
    ),
  );
  const selectedId = String(state.getSelectedId() || "").trim();
  const groups = [];
  for (let index = 0; index < images.length; index += columns) {
    groups.push(images.slice(index, index + columns));
  }

  for (const group of groups) {
    const rowGroup = document.createElement("div");
    rowGroup.className = "gallery-row-group";
    rowGroup.style.setProperty("--gallery-columns", String(columns));

    const row = document.createElement("div");
    row.className = "gallery-row";

    let selectedImage = null;
    for (const image of group) {
      const imageId = String(image?.id || "").trim();
      const card = createGalleryCard(
        image,
        imageId && imageId === selectedId,
        source,
      );
      if (imageId && imageId === selectedId) {
        selectedImage = image;
      }
      row.appendChild(card);
    }

    rowGroup.appendChild(row);
    if (selectedImage) {
      rowGroup.appendChild(createGalleryDetailRow(selectedImage, source));
    }
    state.list.appendChild(rowGroup);
  }
}

function syncGallerySelectionView(source = MANUAL_LIBRARY_SOURCE) {
  const state = getLibraryState(source);
  if (state.getViewMode() !== "gallery") {
    return;
  }

  const selectedId = String(state.getSelectedId() || "").trim();
  const rowGroups = Array.from(state.list.querySelectorAll(".gallery-row-group"));
  let selectedGroup = null;

  for (const group of rowGroups) {
    const existingDetail = group.querySelector(".gallery-detail-row");
    if (existingDetail) {
      existingDetail.remove();
    }

    const cards = Array.from(group.querySelectorAll(".gallery-card"));
    for (const card of cards) {
      const cardId = String(card.dataset.galleryImageId || "").trim();
      const isSelected = Boolean(selectedId) && cardId === selectedId;
      card.classList.toggle("is-selected", isSelected);
      card.setAttribute("aria-pressed", String(isSelected));
      if (isSelected) {
        selectedGroup = group;
      }
    }
  }

  if (!selectedId || !selectedGroup) {
    return;
  }

  const selectedImage = filteredLibraryImages(state).find(
    (image) => String(image?.id || "").trim() === selectedId,
  );
  if (!selectedImage) {
    return;
  }

  selectedGroup.appendChild(createGalleryDetailRow(selectedImage, source));
}

function renderLibrary(source = MANUAL_LIBRARY_SOURCE) {
  const state = getLibraryState(source);
  const visibleImages = filteredLibraryImages(state);
  state.list.replaceChildren();
  updateLibrarySearchControls(source);
  if (source === SOLIDIFIED_LIBRARY_SOURCE) {
    renderSolidifiedLibraryCount();
  } else if (source === IMAGEBED_LIBRARY_SOURCE) {
    state.meta.textContent = `${state.images.length} 张`;
  } else if (source === EXTERNAL_LIBRARY_SOURCE) {
    state.meta.textContent = `${state.images.length} 张`;
  } else {
    state.meta.textContent = `${state.images.length} 张`;
  }
  syncSelectedGalleryImage(source);
  state.empty.textContent =
    state.images.length > 0 && state.getSearchText().trim()
      ? "没有找到含有该标签的图片。"
      : source === SOLIDIFIED_LIBRARY_SOURCE
        ? "暂无已完成标签生成的固化图像。"
        : source === IMAGEBED_LIBRARY_SOURCE
          ? "暂无从图床同步并完成打标签的图像。"
        : source === EXTERNAL_LIBRARY_SOURCE
          ? "暂无已完成标签生成的外部插件图像。"
          : "暂无已经生成特征标签的图像。";
  state.empty.classList.toggle("is-hidden", visibleImages.length > 0);
  updateLibraryModeButtons(source);
  state.list.classList.toggle("is-gallery-mode", state.getViewMode() === "gallery");
  if (state.getViewMode() !== "gallery") {
    delete state.list.dataset.galleryColumns;
    state.setLastWidth(0);
  }

  if (!visibleImages.length) {
    return;
  }

  if (state.getViewMode() === "gallery") {
    renderLibraryGalleryMode(source);
    return;
  }

  renderLibraryListMode(source);
}

function renderGlobalTagsEditor() {
  els.globalTagsMeta.textContent = `${globalTags.length} 个`;
  if (!globalTagsDirty) {
    els.globalTagsInput.value = globalTags.join("\n");
  }
  renderGlobalTagsPreview();
}

function renderGlobalTagsPreview() {
  els.globalTagsPreview.replaceChildren();
  const previewTags = normalizeTags(els.globalTagsInput.value);
  if (!previewTags.length) {
    const empty = document.createElement("span");
    empty.className = "empty-text inline";
    empty.textContent = "暂无公用特征标签。";
    els.globalTagsPreview.appendChild(empty);
    return;
  }
  for (const tag of previewTags) {
    els.globalTagsPreview.appendChild(tagChip(tag));
  }
}

function librarySignature(images, tags) {
  const imagePart = (Array.isArray(images) ? images : [])
    .map((image) =>
      [
        String(image?.id || ""),
        String(image?.rel_path || ""),
        String(image?.mtime || ""),
        String(image?.size || ""),
        JSON.stringify(image?.tags || []),
        JSON.stringify(image?.selected_global_tags || []),
        JSON.stringify(image?.merged_tags || []),
      ].join("|"),
    )
    .join("\n");
  return `${imagePart}\n::global::${JSON.stringify(Array.isArray(tags) ? tags : [])}`;
}

function pendingPoolSignature(images) {
  return (Array.isArray(images) ? images : [])
    .map((image) =>
      [
        String(image?.id || ""),
        String(image?.rel_path || ""),
        String(image?.mtime || ""),
        String(image?.size || ""),
        String(image?.collected_at || image?.external_imported_at || ""),
        String(image?.imagebed_imported_at || ""),
        String(image?.caption_status || ""),
      ].join("|"),
    )
    .join("\n");
}

function externalPendingImageSignature(image) {
  return [
    String(image?.id || ""),
    String(image?.rel_path || ""),
    String(image?.mtime || ""),
    String(image?.size || ""),
    String(image?.external_imported_at || ""),
    String(image?.caption_status || ""),
  ].join("|");
}

function applyLibraryState(library, options = {}) {
  applyDefaultLibraryViewMode(library?.page_library_default_view_mode);
  const nextImages = Array.isArray(library?.manual_images)
    ? library.manual_images
    : Array.isArray(library?.images)
      ? library.images
      : [];
  const nextSolidifiedImages = Array.isArray(library?.solidified_images)
    ? library.solidified_images
    : [];
  const nextExternalImages = Array.isArray(library?.external_images)
    ? library.external_images
    : [];
  const nextImagebedImages = Array.isArray(library?.imagebed_images)
    ? library.imagebed_images
    : [];
  const nextGlobalTags = Array.isArray(library?.global_tags)
    ? library.global_tags
    : [];
  const nextSignature = [
    librarySignature(nextImages, nextGlobalTags),
    "::solidified::",
    librarySignature(nextSolidifiedImages, nextGlobalTags),
    "::external::",
    librarySignature(nextExternalImages, nextGlobalTags),
    "::imagebed::",
    librarySignature(nextImagebedImages, nextGlobalTags),
  ].join("\n");
  const force = options.force === true;
  const changed = force || nextSignature !== renderedLibrarySignature;

  libraryImages = nextImages;
  solidifiedLibraryImages = nextSolidifiedImages;
  externalLibraryImages = nextExternalImages;
  imagebedLibraryImages = nextImagebedImages;
  globalTags = nextGlobalTags;
  syncSelectedGalleryImage(MANUAL_LIBRARY_SOURCE);
  syncSelectedGalleryImage(SOLIDIFIED_LIBRARY_SOURCE);
  syncSelectedGalleryImage(EXTERNAL_LIBRARY_SOURCE);
  syncSelectedGalleryImage(IMAGEBED_LIBRARY_SOURCE);

  if (!changed) {
    return false;
  }

  renderedLibrarySignature = nextSignature;
  renderGlobalTagsEditor();
  if (isPageScrolling) {
    deferLibraryRenderUntilScrollIdle(MANUAL_LIBRARY_SOURCE);
    deferLibraryRenderUntilScrollIdle(SOLIDIFIED_LIBRARY_SOURCE);
    deferLibraryRenderUntilScrollIdle(EXTERNAL_LIBRARY_SOURCE);
    deferLibraryRenderUntilScrollIdle(IMAGEBED_LIBRARY_SOURCE);
  } else {
    renderLibraryPreservingScroll(MANUAL_LIBRARY_SOURCE);
    renderLibraryPreservingScroll(SOLIDIFIED_LIBRARY_SOURCE);
    renderLibraryPreservingScroll(EXTERNAL_LIBRARY_SOURCE);
    renderLibraryPreservingScroll(IMAGEBED_LIBRARY_SOURCE);
  }
  return true;
}

function applyPendingPoolState(pool, options = {}) {
  const nextImages = Array.isArray(pool?.images) ? pool.images : [];
  if (pool?.config && typeof pool.config === "object") {
    autoCollectionConfigCache = {
      ...autoCollectionConfigCache,
      ...pool.config,
    };
    renderSolidifiedLibraryCount();
  }
  const nextSignature = pendingPoolSignature(nextImages);
  const force = options.force === true;
  const changed = force || nextSignature !== renderedPendingPoolSignature;

  pendingPoolImages = nextImages;
  const existingIds = new Set(nextImages.map((image) => String(image?.id || "")));
  selectedPendingImageIds = new Set(
    Array.from(selectedPendingImageIds).filter((imageId) => existingIds.has(imageId)),
  );

  if (!changed) {
    syncPendingSelectionView();
    return false;
  }

  renderedPendingPoolSignature = nextSignature;
  const position = captureScrollPosition();
  renderPendingPool();
  restoreScrollPosition(position);
  return true;
}

function applyExternalPendingState(pending, options = {}) {
  const nextImages = Array.isArray(pending?.images) ? pending.images : [];
  applyExternalImportWarningPreferences(pending?.warning_preferences);
  const nextSignature = pendingPoolSignature(nextImages);
  const force = options.force === true;
  const changed = force || nextSignature !== renderedExternalPendingSignature;

  externalImportPendingImages = nextImages;
  const existingIds = new Set(nextImages.map((image) => String(image?.id || "")));
  selectedExternalPendingImageIds = new Set(
    Array.from(selectedExternalPendingImageIds).filter((imageId) =>
      existingIds.has(imageId),
    ),
  );

  if (!changed) {
    syncExternalPendingSelectionView();
    return false;
  }

  renderedExternalPendingSignature = nextSignature;
  const position = captureScrollPosition();
  renderExternalPendingPool({ force });
  restoreScrollPosition(position);
  return true;
}

function syncPendingSelectionView() {
  const cards = Array.from(els.pendingPoolList.querySelectorAll(".pending-card"));
  for (const card of cards) {
    const imageId = String(card.dataset.pendingImageId || "").trim();
    const selected = selectedPendingImageIds.has(imageId);
    card.classList.toggle("is-selected", selected);
    const checkbox = card.querySelector("input[type='checkbox']");
    if (checkbox) {
      checkbox.checked = selected;
    }
  }
  const selectedCount = selectedPendingImageIds.size;
  els.pendingAcceptButton.disabled = selectedCount === 0;
  els.pendingDiscardButton.disabled = selectedCount === 0;
  els.pendingSelectAllButton.textContent =
    pendingPoolImages.length && selectedCount === pendingPoolImages.length
      ? "取消全选"
      : "全选";
}

function togglePendingSelection(imageId) {
  const normalizedId = String(imageId || "").trim();
  if (!normalizedId) {
    return;
  }
  if (selectedPendingImageIds.has(normalizedId)) {
    selectedPendingImageIds.delete(normalizedId);
  } else {
    selectedPendingImageIds.add(normalizedId);
  }
  syncPendingSelectionView();
}

function syncExternalPendingSelectionView() {
  const cards = Array.from(
    els.externalImportPendingList.querySelectorAll(".pending-card"),
  );
  for (const card of cards) {
    const imageId = String(card.dataset.pendingImageId || "").trim();
    const selected = selectedExternalPendingImageIds.has(imageId);
    card.classList.toggle("is-selected", selected);
    const checkbox = card.querySelector("input[type='checkbox']");
    if (checkbox) {
      checkbox.checked = selected;
    }
  }
  const selectedCount = selectedExternalPendingImageIds.size;
  els.externalImportDeletePendingButton.disabled = selectedCount === 0;
  els.externalImportCancelCaptionButton.disabled =
    externalImportPendingImages.length === 0;
  if (!externalImportPendingImages.length || lastExternalImportRunning) {
    els.externalImportPauseButton.disabled = true;
  }
  els.externalImportSelectAllButton.textContent =
    externalImportPendingImages.length &&
    selectedCount === externalImportPendingImages.length
      ? "取消全选"
      : "全选";
}

function toggleExternalPendingSelection(imageId) {
  const normalizedId = String(imageId || "").trim();
  if (!normalizedId) {
    return;
  }
  if (selectedExternalPendingImageIds.has(normalizedId)) {
    selectedExternalPendingImageIds.delete(normalizedId);
  } else {
    selectedExternalPendingImageIds.add(normalizedId);
  }
  syncExternalPendingSelectionView();
}

function toggleAllExternalPendingSelection() {
  if (!externalImportPendingImages.length) {
    return;
  }
  if (selectedExternalPendingImageIds.size === externalImportPendingImages.length) {
    selectedExternalPendingImageIds.clear();
  } else {
    selectedExternalPendingImageIds = new Set(
      externalImportPendingImages
        .map((image) => String(image?.id || ""))
        .filter(Boolean),
    );
  }
  syncExternalPendingSelectionView();
}

function imagebedPendingImageSignature(image) {
  return [
    String(image?.id || ""),
    String(image?.rel_path || ""),
    String(image?.mtime || ""),
    String(image?.size || ""),
    String(image?.imagebed_imported_at || ""),
    String(image?.caption_status || ""),
  ].join("|");
}

function applyImagebedPendingState(pending, options = {}) {
  const nextImages = Array.isArray(pending?.images) ? pending.images : [];
  const nextSignature = pendingPoolSignature(nextImages);
  const force = options.force === true;
  const changed = force || nextSignature !== renderedImagebedPendingSignature;

  imagebedImportPendingImages = nextImages;
  const existingIds = new Set(nextImages.map((image) => String(image?.id || "")));
  selectedImagebedPendingImageIds = new Set(
    Array.from(selectedImagebedPendingImageIds).filter((imageId) =>
      existingIds.has(imageId),
    ),
  );

  if (!changed) {
    syncImagebedPendingSelectionView();
    return false;
  }

  renderedImagebedPendingSignature = nextSignature;
  const position = captureScrollPosition();
  renderImagebedPendingPool({ force });
  restoreScrollPosition(position);
  return true;
}

function syncImagebedPendingSelectionView() {
  const cards = Array.from(
    els.imagebedImportPendingList.querySelectorAll(".pending-card"),
  );
  for (const card of cards) {
    const imageId = String(card.dataset.pendingImageId || "").trim();
    const selected = selectedImagebedPendingImageIds.has(imageId);
    card.classList.toggle("is-selected", selected);
    const checkbox = card.querySelector("input[type='checkbox']");
    if (checkbox) {
      checkbox.checked = selected;
    }
  }
  const selectedCount = selectedImagebedPendingImageIds.size;
  els.imagebedImportDeletePendingButton.disabled = selectedCount === 0;
  els.imagebedImportCancelCaptionButton.disabled =
    imagebedImportPendingImages.length === 0;
  if (!imagebedImportPendingImages.length || lastImagebedImportRunning) {
    els.imagebedImportPauseButton.disabled = true;
  }
  els.imagebedImportSelectAllButton.textContent =
    imagebedImportPendingImages.length &&
    selectedCount === imagebedImportPendingImages.length
      ? "取消全选"
      : "全选";
}

function toggleImagebedPendingSelection(imageId) {
  const normalizedId = String(imageId || "").trim();
  if (!normalizedId) {
    return;
  }
  if (selectedImagebedPendingImageIds.has(normalizedId)) {
    selectedImagebedPendingImageIds.delete(normalizedId);
  } else {
    selectedImagebedPendingImageIds.add(normalizedId);
  }
  syncImagebedPendingSelectionView();
}

function toggleAllImagebedPendingSelection() {
  if (!imagebedImportPendingImages.length) {
    return;
  }
  if (
    selectedImagebedPendingImageIds.size === imagebedImportPendingImages.length
  ) {
    selectedImagebedPendingImageIds.clear();
  } else {
    selectedImagebedPendingImageIds = new Set(
      imagebedImportPendingImages
        .map((image) => String(image?.id || ""))
        .filter(Boolean),
    );
  }
  syncImagebedPendingSelectionView();
}

function renderImagebedPendingPool(options = {}) {
  if (options.force === true) {
    els.imagebedImportPendingList.replaceChildren();
  } else {
    els.imagebedImportPendingList.replaceChildren();
  }
  els.imagebedImportPendingMeta.textContent = `${imagebedImportPendingImages.length} 张`;
  els.emptyImagebedImportPendingText.classList.toggle(
    "is-hidden",
    imagebedImportPendingImages.length > 0,
  );

  for (const image of imagebedImportPendingImages) {
    const imageId = String(image?.id || "").trim();
    if (!imageId) {
      continue;
    }
    const card = document.createElement("label");
    card.className = "pending-card";
    card.dataset.pendingImageId = imageId;
    card.dataset.pendingSignature = imagebedPendingImageSignature(image);

    const checkbox = document.createElement("input");
    checkbox.type = "checkbox";
    checkbox.checked = selectedImagebedPendingImageIds.has(imageId);
    checkbox.addEventListener("change", (event) => {
      event.stopPropagation();
      toggleImagebedPendingSelection(imageId);
    });

    const thumb = document.createElement("img");
    thumb.className = "pending-thumb";
    thumb.alt = image.filename || image.rel_path || "图床待打标签图像";
    thumb.loading = "lazy";
    thumb.decoding = "async";
    applyResolvedImageUrl(thumb, image);

    const selectedOverlay = document.createElement("span");
    selectedOverlay.className = "pending-selected-overlay";
    selectedOverlay.innerHTML = PENDING_SELECTION_ICON;
    selectedOverlay.setAttribute("aria-hidden", "true");

    const thumbWrap = document.createElement("div");
    thumbWrap.className = "pending-thumb-wrap";
    thumbWrap.append(thumb, selectedOverlay);

    const meta = document.createElement("div");
    meta.className = "pending-card-meta";
    const time = document.createElement("div");
    time.className = "pending-card-title pending-card-time";
    time.textContent = formatPendingCollectionTime(
      image.imagebed_imported_at || image.updated_at,
    );
    const details = document.createElement("div");
    details.className = "pending-card-details";
    details.textContent = image.caption_status || "pending";
    meta.append(time, details);

    card.append(checkbox, thumbWrap, meta);
    card.addEventListener("click", (event) => {
      if (event.target !== checkbox) {
        event.preventDefault();
        toggleImagebedPendingSelection(imageId);
      }
    });
    els.imagebedImportPendingList.appendChild(card);
  }

  syncImagebedPendingSelectionView();
}

function imagebedImportDialogBlockState(status) {
  const active = status?.active_import || {};
  const importRunning = String(active?.status || "") === "running";
  const pendingCount = asInt(status?.pending_count ?? active?.pending_count);
  const captionActive =
    Boolean(status?.caption_active) ||
    (!Boolean(status?.caption_paused) && pendingCount > 0);
  return {
    blocked: importRunning || captionActive,
    importRunning,
    captionActive,
    pendingCount,
  };
}

function renderImagebedImportDialogStatus(status) {
  const snapshot = status || imagebedImportStatusCache || {};
  imagebedImportStatusCache = snapshot;
  const connection = snapshot?.last_connection || {};
  const stat = snapshot?.last_stat || {};
  if (els.imagebedConnectionStatus) {
    if (connection.connected) {
      els.imagebedConnectionStatus.textContent = "已连接";
    } else {
      els.imagebedConnectionStatus.textContent = connection.message || "未连接";
    }
  }
  if (els.imagebedLastSyncAt) {
    els.imagebedLastSyncAt.textContent = formatTime(
      snapshot?.last_successful_sync_at,
    );
  }
  if (els.imagebedUnsyncedCount) {
    const hasUnsynced =
      stat && Object.prototype.hasOwnProperty.call(stat, "unsynced_count");
    els.imagebedUnsyncedCount.textContent = hasUnsynced
      ? String(asInt(stat.unsynced_count))
      : "-";
  }

  const blockState = imagebedImportDialogBlockState(snapshot);
  lastImagebedImportRunning = blockState.importRunning;
  lastImagebedImportDialogBlocked = blockState.blocked;
  const connectionReady =
    Boolean(connection.connected) && imagebedImportConnectionVerified;
  const canStartCaptioning =
    imagebedCaptionPaused && !blockState.importRunning && blockState.pendingCount > 0;
  if (els.imagebedImportPauseButton) {
    els.imagebedImportPauseButton.textContent = blockState.blocked
      ? "请稍候"
      : "开始";
    els.imagebedImportPauseButton.disabled = !canStartCaptioning;
    els.imagebedImportPauseButton.classList.toggle(
      "primary-action",
      canStartCaptioning,
    );
    els.imagebedImportPauseButton.classList.toggle(
      "secondary",
      !canStartCaptioning,
    );
  }
  if (els.imagebedImportStartButton) {
    els.imagebedImportStartButton.disabled =
      blockState.blocked || !connectionReady;
  }
}

function renderImagebedImportStatus(status) {
  const active = status?.active_import || {};
  const stat = status?.last_stat || {};
  imagebedCaptionPaused = Boolean(status?.caption_paused);
  renderImagebedImportDialogStatus(status);

  const isImportRunning = String(active?.status || "") === "running";
  const pendingCount = asInt(status?.pending_count);
  if (isImportRunning) {
    els.imagebedImportMessage.textContent =
      `正在导入：已扫描 ${asInt(active.scanned)} 张，复制 ${asInt(active.copied)} 张，` +
      `跳过重复 ${asInt(active.skipped_duplicates)} 张。`;
    return;
  }
  if (active?.status === "done") {
    els.imagebedImportMessage.textContent =
      `最近一次导入完成：复制 ${asInt(active.copied)} 张，跳过重复 ${asInt(
        active.skipped_duplicates,
      )} 张。`;
    return;
  }
  if (active?.status === "failed") {
    els.imagebedImportMessage.textContent = `最近一次导入失败：${active.message || "-"}`;
    return;
  }
  if (active?.status === "stopped") {
    els.imagebedImportMessage.textContent =
      `最近一次导入已停止：已扫描 ${asInt(active.scanned)} 张，复制 ${asInt(active.copied)} 张。`;
    return;
  }
  if (status?.caption_active || (!imagebedCaptionPaused && pendingCount > 0)) {
    els.imagebedImportMessage.textContent = "自动标签进程正在运行。";
    return;
  }
  if (imagebedCaptionPaused && pendingCount > 0) {
    els.imagebedImportMessage.textContent =
      "导入完成后，可点击“开始”生成标签。";
    return;
  }
  if (stat?.count) {
    els.imagebedImportMessage.textContent = `最近统计目录包含 ${asInt(stat.count)} 张图片。`;
    return;
  }
  els.imagebedImportMessage.textContent = "";
}

function selectedImagebedPendingIds() {
  return Array.from(selectedImagebedPendingImageIds).filter(Boolean);
}

function scrollToSolidifiedLibrary() {
  const target = els.solidifiedLibraryList?.closest(".solidified-library-panel");
  if (!target) {
    return;
  }
  target.scrollIntoView({
    behavior: "smooth",
    block: "start",
  });
}

function renderPendingPool() {
  els.pendingPoolList.replaceChildren();
  renderLimitedCount(
    els.pendingPoolMeta,
    pendingPoolImages.length,
    autoCollectionConfigCache.pending_pool_limit,
  );
  els.emptyPendingPoolText.classList.toggle(
    "is-hidden",
    pendingPoolImages.length > 0,
  );

  for (const image of pendingPoolImages) {
    const imageId = String(image?.id || "").trim();
    const card = document.createElement("label");
    card.className = "pending-card";
    card.dataset.pendingImageId = imageId;

    const checkbox = document.createElement("input");
    checkbox.type = "checkbox";
    checkbox.checked = selectedPendingImageIds.has(imageId);
    checkbox.addEventListener("change", (event) => {
      event.stopPropagation();
      togglePendingSelection(imageId);
    });

    const thumb = document.createElement("img");
    thumb.className = "pending-thumb";
    thumb.alt = image.filename || image.rel_path || "待筛选图片";
    thumb.loading = "lazy";
    thumb.decoding = "async";
    applyResolvedPendingImageUrl(thumb, image);

    const selectedOverlay = document.createElement("span");
    selectedOverlay.className = "pending-selected-overlay";
    selectedOverlay.innerHTML = PENDING_SELECTION_ICON;
    selectedOverlay.setAttribute("aria-hidden", "true");

    const thumbWrap = document.createElement("div");
    thumbWrap.className = "pending-thumb-wrap";
    thumbWrap.append(thumb, selectedOverlay);

    const meta = document.createElement("div");
    meta.className = "pending-card-meta";

    const filename = document.createElement("div");
    filename.className = "pending-card-title";
    filename.classList.add("pending-card-time");
    filename.textContent = formatPendingCollectionTime(image.collected_at);

    meta.append(filename);
    card.append(checkbox, thumbWrap, meta);
    card.addEventListener("click", (event) => {
      if (event.target !== checkbox) {
        event.preventDefault();
        togglePendingSelection(imageId);
      }
    });
    els.pendingPoolList.appendChild(card);
  }

  syncPendingSelectionView();
}

function renderExternalPendingPool(options = {}) {
  if (options.force === true) {
    els.externalImportPendingList.replaceChildren();
  }
  const currentCards = new Map();
  for (const card of els.externalImportPendingList.querySelectorAll(".pending-card")) {
    const imageId = String(card.dataset.pendingImageId || "").trim();
    if (imageId) {
      currentCards.set(imageId, card);
    }
  }
  const nextIds = new Set();
  const renderedCards = new Set();
  const fragment = document.createDocumentFragment();
  els.externalImportPendingMeta.textContent = `${externalImportPendingImages.length} 张`;
  els.emptyExternalImportPendingText.classList.toggle(
    "is-hidden",
    externalImportPendingImages.length > 0,
  );

  for (const image of externalImportPendingImages) {
    const imageId = String(image?.id || "").trim();
    if (!imageId) {
      continue;
    }
    nextIds.add(imageId);
    const nextSignature = externalPendingImageSignature(image);
    const existingCard = currentCards.get(imageId);
    if (existingCard?.dataset.pendingSignature === nextSignature) {
      renderedCards.add(existingCard);
      fragment.appendChild(existingCard);
      continue;
    }
    const oldThumb = existingCard?.querySelector("img");
    if (oldThumb && imageLoadObserver) {
      imageLoadObserver.unobserve(oldThumb);
    }
    const card = document.createElement("label");
    card.className = "pending-card";
    card.dataset.pendingImageId = imageId;
    card.dataset.pendingSignature = nextSignature;

    const checkbox = document.createElement("input");
    checkbox.type = "checkbox";
    checkbox.checked = selectedExternalPendingImageIds.has(imageId);
    checkbox.addEventListener("change", (event) => {
      event.stopPropagation();
      toggleExternalPendingSelection(imageId);
    });

    const thumb = document.createElement("img");
    thumb.className = "pending-thumb";
    thumb.alt = image.filename || image.rel_path || "待打标签图像";
    thumb.loading = "lazy";
    thumb.decoding = "async";
    applyResolvedImageUrl(thumb, image);

    const selectedOverlay = document.createElement("span");
    selectedOverlay.className = "pending-selected-overlay";
    selectedOverlay.innerHTML = PENDING_SELECTION_ICON;
    selectedOverlay.setAttribute("aria-hidden", "true");

    const thumbWrap = document.createElement("div");
    thumbWrap.className = "pending-thumb-wrap";
    thumbWrap.append(thumb, selectedOverlay);

    const meta = document.createElement("div");
    meta.className = "pending-card-meta";
    const status = document.createElement("div");
    status.className = "pending-card-details";
    status.textContent = image.caption_status || "pending";
    meta.append(status);

    card.append(checkbox, thumbWrap, meta);
    card.addEventListener("click", (event) => {
      if (event.target !== checkbox) {
        event.preventDefault();
        toggleExternalPendingSelection(imageId);
      }
    });
    renderedCards.add(card);
    fragment.appendChild(card);
  }
  for (const [imageId, card] of currentCards.entries()) {
    if (nextIds.has(imageId) || renderedCards.has(card)) {
      continue;
    }
    const thumb = card.querySelector("img");
    if (thumb && imageLoadObserver) {
      imageLoadObserver.unobserve(thumb);
    }
  }
  els.externalImportPendingList.replaceChildren(fragment);

  syncExternalPendingSelectionView();
}

function externalImportDialogBlockState(status) {
  const active = status?.active_import || {};
  const importRunning = String(active?.status || "") === "running";
  const pendingCount = asInt(status?.pending_count ?? active?.pending_count);
  const captionActive =
    Boolean(status?.caption_active) ||
    (!Boolean(status?.caption_paused) && pendingCount > 0);
  return {
    blocked: importRunning || captionActive,
    importRunning,
    captionActive,
    pendingCount,
  };
}

function setExternalImportStatHint(text, visible) {
  els.externalImportStatHint.textContent =
    text || EXTERNAL_IMPORT_DEFAULT_STAT_HINT;
  els.externalImportStatHint.classList.toggle("is-hidden", !visible);
}

function renderExternalImportStatus(status) {
  const active = status?.active_import || {};
  const stat = status?.last_stat || externalImportDirectoryStat;
  externalCaptionPaused = Boolean(status?.caption_paused);
  const isImportRunning = String(active?.status || "") === "running";
  const pendingCount = asInt(status?.pending_count);
  const dialogBlockState = externalImportDialogBlockState(status);
  lastExternalImportRunning = isImportRunning;
  lastExternalImportDialogBlocked = dialogBlockState.blocked;
  const canStartCaptioning =
    externalCaptionPaused && !isImportRunning && pendingCount > 0;
  els.externalImportPauseButton.textContent = isImportRunning ? "请稍候" : "开始";
  els.externalImportPauseButton.disabled = !canStartCaptioning;
  els.externalImportPauseButton.classList.toggle(
    "primary-action",
    canStartCaptioning,
  );
  els.externalImportPauseButton.classList.toggle(
    "secondary",
    !canStartCaptioning,
  );
  if (active?.status === "running") {
    els.externalImportMessage.textContent =
      `正在导入：已扫描 ${asInt(active.scanned)} 张，复制 ${asInt(active.copied)} 张，` +
      `跳过重复 ${asInt(active.skipped_duplicates)} 张。`;
    return;
  }
  if (active?.status === "done") {
    els.externalImportMessage.textContent =
      `最近一次导入完成：复制 ${asInt(active.copied)} 张，跳过重复 ${asInt(active.skipped_duplicates)} 张。`;
    return;
  }
  if (active?.status === "failed") {
    els.externalImportMessage.textContent = `最近一次导入失败：${active.message || "-"}`;
    return;
  }
  if (active?.status === "stopped") {
    els.externalImportMessage.textContent =
      `最近一次导入已停止：已扫描 ${asInt(active.scanned)} 张，复制 ${asInt(active.copied)} 张。`;
    return;
  }
  if (externalCaptionPaused && pendingCount > 0) {
    els.externalImportMessage.textContent =
      "导入完成后，可点击“开始”生成标签。";
    return;
  }
  if (stat?.count) {
    els.externalImportMessage.textContent = `最近统计目录包含 ${asInt(stat.count)} 张图片。`;
  }
}

function selectedExternalPendingIds() {
  return Array.from(selectedExternalPendingImageIds).filter(Boolean);
}

const EXTERNAL_IMPORT_WARNING_STORAGE_VERSION = "v2";
const EXTERNAL_IMPORT_WARNING_STORAGE_KEYS = {
  delete_pending: `smart_image_external_import_skip_delete_warning_${EXTERNAL_IMPORT_WARNING_STORAGE_VERSION}`,
  cancel_caption: `smart_image_external_import_skip_cancel_warning_${EXTERNAL_IMPORT_WARNING_STORAGE_VERSION}`,
};

function shouldSkipExternalImportWarning(action) {
  const normalizedAction = String(action || "").trim();
  if (skippedExternalImportWarnings.has(normalizedAction)) {
    return true;
  }
  try {
    return localStorage.getItem(EXTERNAL_IMPORT_WARNING_STORAGE_KEYS[normalizedAction]) === "1";
  } catch (error) {
    return false;
  }
}

function rememberExternalImportWarning(action) {
  const normalizedAction = String(action || "").trim();
  if (!EXTERNAL_IMPORT_WARNING_STORAGE_KEYS[normalizedAction]) {
    return;
  }
  skippedExternalImportWarnings.add(normalizedAction);
  try {
    localStorage.setItem(EXTERNAL_IMPORT_WARNING_STORAGE_KEYS[normalizedAction], "1");
  } catch (error) {
    // Ignore private-mode or quota failures; the warning will simply show again.
  }
  pluginApiPost("external_import_warning_preference", {
    action: normalizedAction,
    skip: true,
  }).catch(() => {});
}

function applyExternalImportWarningPreferences(preferences) {
  if (!preferences || typeof preferences !== "object") {
    return;
  }
  for (const action of Object.keys(EXTERNAL_IMPORT_WARNING_STORAGE_KEYS)) {
    if (!preferences[action]) {
      continue;
    }
    skippedExternalImportWarnings.add(action);
    try {
      localStorage.setItem(EXTERNAL_IMPORT_WARNING_STORAGE_KEYS[action], "1");
    } catch (error) {
      // Persisted server-side preference is still enough for this page session.
    }
  }
}

function externalImportWarningContent(action) {
  if (action === "delete_pending") {
    return {
      title: "确认删除待打标签图像",
      text: "手动删除的图片会被记录，未来再次同步外部图库时不会再次进入本插件。",
      confirmText: "确认删除",
    };
  }
  return {
    title: "确认取消自动标签进程",
    text: "取消后会释放所有未打标签图像；以后需要重新走导入流程，但插件会自动去重。",
    confirmText: "确认取消",
  };
}

function openExternalImportWarning(action) {
  const content = externalImportWarningContent(action);
  pendingExternalImportWarningAction = action;
  els.externalImportWarningTitle.textContent = content.title;
  els.externalImportWarningText.textContent = content.text;
  els.externalImportWarningConfirmButton.textContent = content.confirmText;
  els.externalImportWarningDontShowInput.checked = false;
  els.externalImportWarningOverlay.classList.remove("is-hidden");
}

function closeExternalImportWarning() {
  pendingExternalImportWarningAction = null;
  els.externalImportWarningOverlay.classList.add("is-hidden");
}

async function confirmExternalImportWarning() {
  const action = pendingExternalImportWarningAction;
  if (!action) {
    closeExternalImportWarning();
    return;
  }
  if (els.externalImportWarningDontShowInput.checked) {
    rememberExternalImportWarning(action);
  }
  closeExternalImportWarning();
  if (action === "delete_pending") {
    await deleteSelectedExternalPendingImages({ confirmed: true });
  } else if (action === "cancel_caption") {
    await cancelExternalCaptioning({ confirmed: true });
  }
}

const IMAGEBED_IMPORT_WARNING_STORAGE_KEYS = {
  delete_pending: "smart_image_imagebed_import_skip_delete_warning",
  cancel_caption: "smart_image_imagebed_import_skip_cancel_warning",
};

function shouldSkipImagebedImportWarning(action) {
  const normalizedAction = String(action || "").trim();
  if (skippedImagebedImportWarnings.has(normalizedAction)) {
    return true;
  }
  try {
    return localStorage.getItem(IMAGEBED_IMPORT_WARNING_STORAGE_KEYS[normalizedAction]) === "1";
  } catch (error) {
    return false;
  }
}

function rememberImagebedImportWarning(action) {
  const normalizedAction = String(action || "").trim();
  if (!IMAGEBED_IMPORT_WARNING_STORAGE_KEYS[normalizedAction]) {
    return;
  }
  skippedImagebedImportWarnings.add(normalizedAction);
  try {
    localStorage.setItem(IMAGEBED_IMPORT_WARNING_STORAGE_KEYS[normalizedAction], "1");
  } catch (error) {
    // Ignore private-mode or quota failures; the warning will simply show again.
  }
}

function imagebedImportWarningContent(action) {
  if (action === "delete_pending") {
    return {
      title: "确认删除待打标签图像",
      text: "手动删除的图床同步图片会被记录，未来再次同步同一个图床对象时不会再次进入本插件。",
      confirmText: "确认删除",
    };
  }
  return {
    title: "确认取消自动标签进程",
    text: "取消后会释放所有未打标签图像；以后需要重新走图床同步导入流程，但插件会自动去重。",
    confirmText: "确认取消",
  };
}

function openImagebedImportWarning(action) {
  const content = imagebedImportWarningContent(action);
  pendingImagebedImportWarningAction = action;
  els.imagebedImportWarningTitle.textContent = content.title;
  els.imagebedImportWarningText.textContent = content.text;
  els.imagebedImportWarningConfirmButton.textContent = content.confirmText;
  els.imagebedImportWarningDontShowInput.checked = false;
  els.imagebedImportWarningOverlay.classList.remove("is-hidden");
}

function closeImagebedImportWarning() {
  pendingImagebedImportWarningAction = null;
  els.imagebedImportWarningOverlay.classList.add("is-hidden");
}

async function confirmImagebedImportWarning() {
  const action = pendingImagebedImportWarningAction;
  if (!action) {
    closeImagebedImportWarning();
    return;
  }
  if (els.imagebedImportWarningDontShowInput.checked) {
    rememberImagebedImportWarning(action);
  }
  closeImagebedImportWarning();
  if (action === "delete_pending") {
    await deleteSelectedImagebedPendingImages({ confirmed: true });
  } else if (action === "cancel_caption") {
    await cancelImagebedCaptioning({ confirmed: true });
  }
}

async function deleteSelectedExternalPendingImages(options = {}) {
  const imageIds = selectedExternalPendingIds();
  if (!imageIds.length) {
    return;
  }
  if (options.confirmed !== true && !shouldSkipExternalImportWarning("delete_pending")) {
    openExternalImportWarning("delete_pending");
    return;
  }
  els.externalImportDeletePendingButton.disabled = true;
  els.externalImportMessage.textContent = "正在删除选中的待打标签图像...";
  try {
    const result = await pluginApiPost("external_import_delete_pending", {
      image_ids: imageIds,
    });
    selectedExternalPendingImageIds.clear();
    if (result?.pending) {
      applyExternalPendingState(result.pending, { force: true });
    } else {
      await refreshExternalImportPending();
    }
    if (result?.library) {
      applyLibraryState(result.library, { force: true });
    }
    if (result?.progress) {
      renderProgress(result.progress);
    }
    const deleted = asInt(result?.result?.deleted?.length);
    const skipped = asInt(result?.result?.skipped?.length);
    els.externalImportMessage.textContent = `已删除 ${deleted} 张，跳过 ${skipped} 张。`;
  } catch (error) {
    els.externalImportMessage.textContent = `删除失败：${error.message || error}`;
  } finally {
    syncExternalPendingSelectionView();
  }
}

async function startExternalCaptioning() {
  if (
    !externalCaptionPaused ||
    !externalImportPendingImages.length ||
    lastExternalImportRunning
  ) {
    syncExternalPendingSelectionView();
    return;
  }
  const providerReady = await ensureCaptionProviderConfigured(
    startExternalCaptioningAfterProviderCheck,
  );
  if (!providerReady) {
    return;
  }
  await startExternalCaptioningAfterProviderCheck();
}

async function startExternalCaptioningAfterProviderCheck() {
  if (
    !externalCaptionPaused ||
    !externalImportPendingImages.length ||
    lastExternalImportRunning
  ) {
    syncExternalPendingSelectionView();
    return;
  }
  els.externalImportPauseButton.disabled = true;
  els.externalImportMessage.textContent = "正在开始自动标签进程...";
  try {
    const result = await pluginApiPost("external_import_start_caption", {});
    if (result?.pending) {
      applyExternalPendingState(result.pending, { force: true });
      renderExternalImportStatus(result.pending.status || {});
    }
    if (result?.progress) {
      renderProgress(result.progress);
    }
    els.externalImportMessage.textContent = "自动标签进程已开始。";
  } catch (error) {
    els.externalImportMessage.textContent = `开始失败：${error.message || error}`;
  } finally {
    syncExternalPendingSelectionView();
    try {
      await refreshExternalImportPending();
    } catch (refreshError) {
      // Keep the original start error visible if the status refresh also fails.
    }
  }
}

async function cancelExternalCaptioning(options = {}) {
  if (!externalImportPendingImages.length) {
    syncExternalPendingSelectionView();
    return;
  }
  if (options.confirmed !== true && !shouldSkipExternalImportWarning("cancel_caption")) {
    openExternalImportWarning("cancel_caption");
    return;
  }
  els.externalImportCancelCaptionButton.disabled = true;
  els.externalImportMessage.textContent = "正在取消自动标签进程...";
  try {
    const result = await pluginApiPost("external_import_cancel_caption", {});
    selectedExternalPendingImageIds.clear();
    if (result?.pending) {
      applyExternalPendingState(result.pending, { force: true });
    }
    if (result?.library) {
      applyLibraryState(result.library, { force: true });
    }
    if (result?.progress) {
      renderProgress(result.progress);
    }
    const removed = asInt(result?.result?.deleted?.length);
    els.externalImportMessage.textContent = `已取消，释放 ${removed} 张未打标签图像。`;
  } catch (error) {
    els.externalImportMessage.textContent = `取消失败：${error.message || error}`;
  } finally {
    syncExternalPendingSelectionView();
  }
}

async function refreshImagebedImportPending() {
  const pending = await pluginApiGet("imagebed_import_pending");
  applyImagebedPendingState(pending);
  renderImagebedImportStatus(pending?.status || {});
  return pending;
}

async function deleteSelectedImagebedPendingImages(options = {}) {
  const imageIds = selectedImagebedPendingIds();
  if (!imageIds.length) {
    return;
  }
  if (options.confirmed !== true && !shouldSkipImagebedImportWarning("delete_pending")) {
    openImagebedImportWarning("delete_pending");
    return;
  }
  els.imagebedImportDeletePendingButton.disabled = true;
  els.imagebedImportMessage.textContent = "正在删除选中的待打标签图像...";
  try {
    const result = await pluginApiPost("imagebed_import_delete_pending", {
      image_ids: imageIds,
    });
    selectedImagebedPendingImageIds.clear();
    if (result?.pending) {
      applyImagebedPendingState(result.pending, { force: true });
    } else {
      await refreshImagebedImportPending();
    }
    if (result?.library) {
      applyLibraryState(result.library, { force: true });
    }
    if (result?.progress) {
      renderProgress(result.progress);
    }
    const deleted = asInt(result?.result?.deleted?.length);
    const skipped = asInt(result?.result?.skipped?.length);
    els.imagebedImportMessage.textContent = `已删除 ${deleted} 张，跳过 ${skipped} 张。`;
  } catch (error) {
    els.imagebedImportMessage.textContent = `删除失败：${error.message || error}`;
  } finally {
    syncImagebedPendingSelectionView();
  }
}

async function startImagebedCaptioning() {
  if (
    !imagebedCaptionPaused ||
    !imagebedImportPendingImages.length ||
    lastImagebedImportRunning
  ) {
    syncImagebedPendingSelectionView();
    return;
  }
  const providerReady = await ensureCaptionProviderConfigured(
    startImagebedCaptioningAfterProviderCheck,
  );
  if (!providerReady) {
    return;
  }
  await startImagebedCaptioningAfterProviderCheck();
}

async function startImagebedCaptioningAfterProviderCheck() {
  if (
    !imagebedCaptionPaused ||
    !imagebedImportPendingImages.length ||
    lastImagebedImportRunning
  ) {
    syncImagebedPendingSelectionView();
    return;
  }
  els.imagebedImportPauseButton.disabled = true;
  els.imagebedImportMessage.textContent = "正在开始自动标签进程...";
  try {
    const result = await pluginApiPost("imagebed_import_start_caption", {});
    if (result?.pending) {
      applyImagebedPendingState(result.pending, { force: true });
      renderImagebedImportStatus(result.pending.status || {});
    }
    if (result?.progress) {
      renderProgress(result.progress);
    }
    els.imagebedImportMessage.textContent = "自动标签进程已开始。";
  } catch (error) {
    els.imagebedImportMessage.textContent = `开始失败：${error.message || error}`;
  } finally {
    syncImagebedPendingSelectionView();
    try {
      await refreshImagebedImportPending();
    } catch (refreshError) {
      // Keep the original start error visible if the status refresh also fails.
    }
  }
}

async function cancelImagebedCaptioning(options = {}) {
  if (!imagebedImportPendingImages.length) {
    syncImagebedPendingSelectionView();
    return;
  }
  if (options.confirmed !== true && !shouldSkipImagebedImportWarning("cancel_caption")) {
    openImagebedImportWarning("cancel_caption");
    return;
  }
  els.imagebedImportCancelCaptionButton.disabled = true;
  els.imagebedImportMessage.textContent = "正在取消自动标签进程...";
  try {
    const result = await pluginApiPost("imagebed_import_cancel_caption", {});
    selectedImagebedPendingImageIds.clear();
    if (result?.pending) {
      applyImagebedPendingState(result.pending, { force: true });
    }
    if (result?.library) {
      applyLibraryState(result.library, { force: true });
    }
    if (result?.progress) {
      renderProgress(result.progress);
    }
    const removed = asInt(result?.result?.deleted?.length);
    els.imagebedImportMessage.textContent = `已取消，释放 ${removed} 张未打标签图像。`;
  } catch (error) {
    els.imagebedImportMessage.textContent = `取消失败：${error.message || error}`;
  } finally {
    syncImagebedPendingSelectionView();
  }
}

async function refreshLibrary() {
  const library = await pluginApiGet("caption_library");
  applyLibraryState(library);
}

async function refreshPendingPool() {
  const pool = await pluginApiGet("auto_collection_pool");
  applyPendingPoolState(pool);
}

async function refreshExternalImportPending() {
  const pending = await pluginApiGet("external_import_pending");
  applyExternalPendingState(pending);
  renderExternalImportStatus(pending?.status || {});
  return pending;
}

async function refreshAll() {
  try {
    const progress = await pluginApiGet("caption_progress");
    renderProgress(progress || {});
    await refreshLibrary();
    await refreshPendingPool();
    const externalStatus = progress?.external_import || {};
    const externalBlockState = externalImportDialogBlockState(externalStatus);
    let latestExternalStatus = externalStatus;
    if (libraryScopeMode === "external" || externalBlockState.blocked) {
      const pending = await refreshExternalImportPending();
      latestExternalStatus = pending?.status || latestExternalStatus;
    }
    if (
      els.externalImportOverlay &&
      !els.externalImportOverlay.classList.contains("is-hidden")
    ) {
      applyExternalImportDialogRunningState(latestExternalStatus);
    }
    const imagebedStatus = progress?.imagebed_import || {};
    const imagebedBlockState = imagebedImportDialogBlockState(imagebedStatus);
    let latestImagebedStatus = imagebedStatus;
    if (libraryScopeMode === "imagebed" || imagebedBlockState.blocked) {
      const pending = await refreshImagebedImportPending();
      latestImagebedStatus = pending?.status || latestImagebedStatus;
    }
    if (
      els.imagebedImportOverlay &&
      !els.imagebedImportOverlay.classList.contains("is-hidden")
    ) {
      renderImagebedImportDialogStatus(latestImagebedStatus);
    }
  } catch (error) {
    setStatus("failed");
    setMessage(`读取进度失败：${error.message || error}`);
  }
}

function openEditor(image) {
  lockEditorBackgroundScroll();
  editingImage = image;
  els.editorTitle.textContent = imageDisplayName(image);
  els.editorImage.alt = image.filename || image.rel_path;
  applyResolvedImageUrl(els.editorImage, image);
  els.tagInput.value = (image.tags || []).join("\n");
  els.editorMessage.textContent = "";
  renderGlobalTagChoices(image.selected_global_tags || []);
  els.editorOverlay.classList.remove("is-hidden");
}

function closeEditor() {
  editingImage = null;
  els.editorOverlay.classList.add("is-hidden");
  unlockEditorBackgroundScroll();
}

function openImportDialog() {
  els.importFileInput.value = "";
  els.importModeMerge.checked = true;
  els.importOverwriteConfig.checked = false;
  els.importMessage.textContent = "";
  els.importOverlay.classList.remove("is-hidden");
}

function closeImportDialog() {
  els.importOverlay.classList.add("is-hidden");
  els.importMessage.textContent = "";
}

function renderExternalImportTreeNode(node) {
  const item = document.createElement("div");
  item.className = "external-tree-item";
  const relPath = String(node?.rel_path || "").trim();
  const children = Array.isArray(node?.children) ? node.children : [];
  const expanded = expandedExternalImportDirectories.has(relPath);

  const row = document.createElement("div");
  row.className = "external-tree-row";

  const toggleButton = document.createElement("button");
  toggleButton.type = "button";
  toggleButton.className = "external-tree-toggle";
  toggleButton.textContent = children.length ? (expanded ? "▾" : "▸") : "";
  toggleButton.disabled = !children.length;
  toggleButton.setAttribute("aria-label", expanded ? "折叠目录" : "展开目录");
  toggleButton.addEventListener("click", (event) => {
    event.stopPropagation();
    if (!children.length) {
      return;
    }
    if (expandedExternalImportDirectories.has(relPath)) {
      expandedExternalImportDirectories.delete(relPath);
    } else {
      expandedExternalImportDirectories.add(relPath);
    }
    renderExternalImportTree(currentExternalImportTree);
  });

  const button = document.createElement("button");
  button.type = "button";
  button.className = "external-tree-button";
  button.dataset.path = relPath;
  button.disabled = !relPath;
  button.addEventListener("click", () => selectExternalImportDirectory(node));

  const icon = document.createElement("span");
  icon.className = "external-tree-folder";
  icon.setAttribute("aria-hidden", "true");

  const label = document.createElement("span");
  label.className = "external-tree-label";
  label.textContent = node?.name || relPath || "/";
  button.append(icon, label);
  row.append(toggleButton, button);
  item.appendChild(row);

  if (children.length && expanded) {
    const childWrap = document.createElement("div");
    childWrap.className = "external-tree-children";
    for (const child of children) {
      childWrap.appendChild(renderExternalImportTreeNode(child));
    }
    item.appendChild(childWrap);
  }
  return item;
}

function renderExternalImportTree(tree) {
  currentExternalImportTree = tree || null;
  if (tree?.rel_path !== undefined && !expandedExternalImportDirectories.has("")) {
    expandedExternalImportDirectories.add("");
  }
  els.externalImportTree.replaceChildren();
  const children = Array.isArray(tree?.children) ? tree.children : [];
  if (!children.length) {
    const empty = document.createElement("p");
    empty.className = "empty-text inline";
    empty.textContent = "未找到可导入的其他插件数据目录。";
    els.externalImportTree.appendChild(empty);
    return;
  }
  for (const child of children) {
    els.externalImportTree.appendChild(renderExternalImportTreeNode(child));
  }
}

function selectExternalImportDirectory(node) {
  if (lastExternalImportDialogBlocked) {
    setExternalImportStatHint(EXTERNAL_IMPORT_BUSY_STAT_HINT, true);
    els.externalImportDialogMessage.textContent = "";
    els.externalImportStatButton.disabled = true;
    els.externalImportStartButton.disabled = true;
    return;
  }
  selectedExternalImportDirectory = String(node?.rel_path || "").trim();
  externalImportDirectoryStat = null;
  els.externalImportSelectedPath.textContent = selectedExternalImportDirectory
    ? `已选择：${selectedExternalImportDirectory}`
    : "请选择一个目录。";
  els.externalImportStatButton.classList.toggle(
    "is-hidden",
    !selectedExternalImportDirectory,
  );
  els.externalImportStatText.textContent = "";
  els.externalImportStartButton.disabled = true;
  setExternalImportStatHint(
    EXTERNAL_IMPORT_DEFAULT_STAT_HINT,
    Boolean(selectedExternalImportDirectory),
  );

  for (const button of els.externalImportTree.querySelectorAll(
    ".external-tree-button",
  )) {
    button.classList.toggle(
      "is-selected",
      String(button.dataset.path || "") === selectedExternalImportDirectory,
    );
  }
}

function applyExternalImportDialogRunningState(status) {
  const blockState =
    typeof status === "boolean"
      ? {
          blocked: Boolean(status),
          importRunning: Boolean(status),
          captionActive: false,
        }
      : externalImportDialogBlockState(status || {});
  lastExternalImportRunning = blockState.importRunning;
  lastExternalImportDialogBlocked = blockState.blocked;
  if (!lastExternalImportDialogBlocked) {
    els.externalImportStatButton.classList.toggle(
      "is-hidden",
      !selectedExternalImportDirectory,
    );
    els.externalImportStatButton.disabled = !selectedExternalImportDirectory;
    els.externalImportStartButton.disabled =
      !selectedExternalImportDirectory ||
      asInt(externalImportDirectoryStat?.count) <= 0;
    setExternalImportStatHint(
      EXTERNAL_IMPORT_DEFAULT_STAT_HINT,
      Boolean(selectedExternalImportDirectory),
    );
    return;
  }
  els.externalImportStatButton.classList.remove("is-hidden");
  els.externalImportStatButton.disabled = true;
  els.externalImportStartButton.disabled = true;
  setExternalImportStatHint(EXTERNAL_IMPORT_BUSY_STAT_HINT, true);
  els.externalImportDialogMessage.textContent = "";
}

function readImagebedImportDraftConfig() {
  return {
    account_id: String(els.imagebedAccountIdInput?.value || "").trim(),
    access_key_id: String(els.imagebedAccessKeyIdInput?.value || "").trim(),
    secret_access_key: String(els.imagebedSecretAccessKeyInput?.value || "").trim(),
    bucket_name: String(els.imagebedBucketNameInput?.value || "").trim(),
    endpoint_url: String(els.imagebedEndpointUrlInput?.value || "").trim(),
    prefix: String(els.imagebedPrefixInput?.value || "").trim(),
    max_file_size_kb: clampInt(els.imagebedMaxFileSizeKbInput?.value, 5120, 1),
    scheduled_enabled: Boolean(els.imagebedScheduledEnabledInput?.checked),
    scheduled_time: normalizeBackupTime(els.imagebedScheduledTimeInput?.value),
  };
}

function applyImagebedImportDraftConfig(config) {
  const next = config || {};
  if (els.imagebedAccountIdInput) {
    els.imagebedAccountIdInput.value = String(next.account_id || "");
  }
  if (els.imagebedAccessKeyIdInput) {
    els.imagebedAccessKeyIdInput.value = String(next.access_key_id || "");
  }
  if (els.imagebedSecretAccessKeyInput) {
    els.imagebedSecretAccessKeyInput.value = String(
      next.secret_access_key || "",
    );
  }
  if (els.imagebedBucketNameInput) {
    els.imagebedBucketNameInput.value = String(next.bucket_name || "");
  }
  if (els.imagebedEndpointUrlInput) {
    els.imagebedEndpointUrlInput.value = String(next.endpoint_url || "");
  }
  if (els.imagebedPrefixInput) {
    els.imagebedPrefixInput.value = String(next.prefix || "");
  }
  if (els.imagebedMaxFileSizeKbInput) {
    els.imagebedMaxFileSizeKbInput.value = String(
      asInt(next.max_file_size_kb) || 5120,
    );
  }
  if (els.imagebedScheduledEnabledInput) {
    els.imagebedScheduledEnabledInput.checked = Boolean(next.scheduled_enabled);
  }
  if (els.imagebedScheduledTimeInput) {
    els.imagebedScheduledTimeInput.value = normalizeBackupTime(
      next.scheduled_time || "03:30",
    );
  }
}

function markImagebedImportConnectionDirty() {
  imagebedImportConnectionVerified = false;
  renderImagebedImportDialogStatus(imagebedImportStatusCache || {});
}

async function testImagebedImportConnection(options = {}) {
  const payload = readImagebedImportDraftConfig();
  const silent = Boolean(options?.silent);
  if (!silent) {
    els.imagebedImportDialogMessage.textContent = "正在测试图床连接...";
  }
  try {
    const data = await pluginApiPost("imagebed_import_test", payload);
    imagebedImportConnectionVerified = Boolean(data?.connection?.connected);
    imagebedImportStatusCache = data.status || imagebedImportStatusCache;
    renderImagebedImportDialogStatus(imagebedImportStatusCache);
    if (!silent) {
      const connection = data.connection || {};
      els.imagebedImportDialogMessage.textContent = connection.connected
        ? "连接测试成功。"
        : `连接测试失败：${connection.message || "-"}`;
    }
    return data;
  } catch (error) {
    imagebedImportConnectionVerified = false;
    if (!silent) {
      els.imagebedImportDialogMessage.textContent = `测试失败：${error.message || error}`;
    }
    throw error;
  }
}

async function openImagebedImportDialog() {
  els.imagebedImportDialogMessage.textContent = "正在读取图床配置...";
  els.imagebedImportStartButton.disabled = true;
  els.imagebedImportOverlay.classList.remove("is-hidden");
  try {
    const config = await pluginApiGet("imagebed_import_config");
    imagebedImportConnectionVerified = false;
    applyImagebedImportDraftConfig(config);
    imagebedImportStatusCache = config.status || imagebedImportStatusCache;
    renderImagebedImportDialogStatus(imagebedImportStatusCache);
    await testImagebedImportConnection({ silent: true });
    els.imagebedImportDialogMessage.textContent = "";
  } catch (error) {
    els.imagebedImportDialogMessage.textContent =
      `读取图床配置失败：${error.message || error}`;
  }
}

function closeImagebedImportDialog() {
  els.imagebedImportOverlay.classList.add("is-hidden");
  els.imagebedImportDialogMessage.textContent = "";
}

async function saveImagebedImportDialog(options = {}) {
  const payload = readImagebedImportDraftConfig();
  const silent = Boolean(options?.silent);
  const keepOpen = Boolean(options?.keepOpen);
  if (!silent) {
    els.imagebedImportDialogMessage.textContent = "正在保存图床配置...";
  }
  try {
    const data = await pluginApiPost("imagebed_import_config", payload);
    imagebedImportConnectionVerified = false;
    applyImagebedImportDraftConfig(data);
    imagebedImportStatusCache = data.status || imagebedImportStatusCache;
    renderImagebedImportDialogStatus(imagebedImportStatusCache);
    if (!silent) {
      els.imagebedImportDialogMessage.textContent = "图床配置已保存。";
    }
    if (!keepOpen) {
      closeImagebedImportDialog();
    }
    return data;
  } catch (error) {
    if (!silent) {
      els.imagebedImportDialogMessage.textContent = `保存失败：${error.message || error}`;
    }
    throw error;
  }
}

async function startImagebedImportAfterSave() {
  els.imagebedImportDialogMessage.textContent = "正在启动导入...";
  await pluginApiPost("imagebed_import_start", {});
  closeImagebedImportDialog();
  setLibraryScopeMode("imagebed");
  els.imagebedImportMessage.textContent = "导入已开始，页面会自动刷新进度。";
  await refreshAll().catch(() => {});
}

async function startImagebedImport() {
  const connectionReady = Boolean(
    imagebedImportStatusCache?.last_connection?.connected &&
      imagebedImportConnectionVerified,
  );
  if (lastImagebedImportDialogBlocked || !connectionReady) {
    return;
  }
  els.imagebedImportStartButton.disabled = true;
  try {
    await saveImagebedImportDialog({ silent: true, keepOpen: true });
    await testImagebedImportConnection({ silent: true });
    await startImagebedImportAfterSave();
  } catch (error) {
    els.imagebedImportDialogMessage.textContent =
      `启动导入失败：${error.message || error}`;
  } finally {
    els.imagebedImportStartButton.disabled = lastImagebedImportDialogBlocked;
  }
}

async function openExternalImportDialog() {
  selectedExternalImportDirectory = "";
  externalImportDirectoryStat = null;
  els.externalImportStatHint.classList.add("is-hidden");
  els.externalImportDialogMessage.textContent = "正在读取目录树...";
  els.externalImportSelectedPath.textContent = "请选择一个目录。";
  els.externalImportStatText.textContent = "";
  if (els.externalImportParentTagInput) {
    els.externalImportParentTagInput.checked = false;
  }
  els.externalImportStartButton.disabled = true;
  els.externalImportStatButton.classList.add("is-hidden");
  els.externalImportStatProgress.classList.add("is-hidden");
  els.externalImportOverlay.classList.remove("is-hidden");
  try {
    const status = await pluginApiGet("external_import_status");
    applyExternalImportDialogRunningState(status);
    renderExternalImportTree(await pluginApiGet("external_import_tree"));
    if (!lastExternalImportDialogBlocked) {
      els.externalImportDialogMessage.textContent = "";
    }
  } catch (error) {
    els.externalImportDialogMessage.textContent =
      `读取外部目录失败：${error.message || error}`;
  }
}

function closeExternalImportDialog() {
  els.externalImportOverlay.classList.add("is-hidden");
  els.externalImportDialogMessage.textContent = "";
}

async function statExternalImportDirectory() {
  if (!selectedExternalImportDirectory || lastExternalImportDialogBlocked) {
    return;
  }
  els.externalImportStatButton.disabled = true;
  els.externalImportStartButton.disabled = true;
  els.externalImportStatProgress.classList.remove("is-hidden");
  els.externalImportDialogMessage.textContent = "正在统计目录中的图片...";
  try {
    externalImportDirectoryStat = await pluginApiPost("external_import_stat", {
      directory: selectedExternalImportDirectory,
    });
    const count = asInt(externalImportDirectoryStat?.count);
    els.externalImportStatHint.classList.add("is-hidden");
    els.externalImportStatText.textContent = `共计 ${count} 张图片`;
    els.externalImportStartButton.disabled = count <= 0;
    els.externalImportDialogMessage.textContent =
      count > 0 ? "统计完成，可以开始导入。" : "该目录中没有可导入的图片。";
  } catch (error) {
    els.externalImportDialogMessage.textContent =
      `统计失败：${error.message || error}`;
  } finally {
    els.externalImportStatButton.disabled = lastExternalImportDialogBlocked;
    els.externalImportStatProgress.classList.add("is-hidden");
  }
}

async function startExternalImport() {
  if (!selectedExternalImportDirectory || lastExternalImportDialogBlocked) {
    return;
  }
  els.externalImportStartButton.disabled = true;
  els.externalImportCancelButton.disabled = true;
  els.externalImportDialogMessage.textContent = "正在启动导入...";
  try {
    await pluginApiPost("external_import_start", {
      directory: selectedExternalImportDirectory,
      include_parent_dir_tag: Boolean(els.externalImportParentTagInput?.checked),
    });
    closeExternalImportDialog();
    setLibraryScopeMode("external");
    els.externalImportMessage.textContent = "导入已开始，页面会自动刷新进度。";
    await refreshAll();
  } catch (error) {
    els.externalImportDialogMessage.textContent =
      `启动导入失败：${error.message || error}`;
  } finally {
    els.externalImportStartButton.disabled = lastExternalImportDialogBlocked;
    els.externalImportCancelButton.disabled = false;
  }
}

async function openExternalImportDialogAndSwitch() {
  setLibraryScopeMode("external");
  await openExternalImportDialog();
}

async function openExportDialog() {
  els.exportDialogMessage.textContent = "正在读取备份列表...";
  els.exportOverlay.classList.remove("is-hidden");
  setExportBusy(false);
  try {
    await refreshScheduledBackups();
    els.exportDialogMessage.textContent = "";
  } catch (error) {
    els.exportDialogMessage.textContent = `读取备份列表失败：${error.message || error}`;
  }
}

function closeExportDialog() {
  els.exportOverlay.classList.add("is-hidden");
  els.exportDialogMessage.textContent = "";
  setExportBusy(false);
}

function setExportBusy(busy) {
  els.exportProgressBar.classList.toggle("is-hidden", !busy);
  els.exportManualButton.disabled = busy;
  els.exportCancelButton.disabled = busy;
  els.exportCloseButton.disabled = busy;
}

function applyScheduledBackupState(state) {
  scheduledBackupState = {
    ...scheduledBackupState,
    ...(state || {}),
    backup_files: Array.isArray(state?.backup_files) ? state.backup_files : [],
  };
  renderScheduledBackupConfigList();
  renderExportBackupList();
}

async function refreshScheduledBackups() {
  const state = await pluginApiGet("scheduled_backup_list");
  applyScheduledBackupState(state || {});
}

function createScheduledBackupRow(item) {
  const row = document.createElement("div");
  row.className = "backup-file-item";

  const info = document.createElement("div");
  info.className = "backup-file-info";
  const name = document.createElement("strong");
  name.textContent = item.filename || "-";
  const meta = document.createElement("span");
  const version = item.version || extractBackupVersion(item.filename);
  const versionLabel = document.createElement("span");
  versionLabel.className = "backup-file-version";
  if (!version || version.toLowerCase() !== PLUGIN_VERSION.toLowerCase()) {
    versionLabel.classList.add("is-outdated");
  }
  versionLabel.textContent = version || "未知版本";
  meta.append(
    document.createTextNode(`${item.created_at_text || "-"} | `),
    versionLabel,
    document.createTextNode(` | ${formatBytes(item.size)}`),
  );
  info.append(name, meta);

  const actions = document.createElement("div");
  actions.className = "backup-file-actions";
  const download = document.createElement("button");
  download.type = "button";
  download.textContent = "下载";
  download.addEventListener("click", () => downloadScheduledBackup(item));
  const remove = document.createElement("button");
  remove.type = "button";
  remove.className = "danger-button";
  remove.textContent = "删除";
  remove.addEventListener("click", () => deleteScheduledBackup(item));
  actions.append(download, remove);

  row.append(info, actions);
  return row;
}

function renderScheduledBackupConfigList() {
  els.scheduledBackupConfigList.replaceChildren();
  const files = scheduledBackupState.backup_files || [];
  if (!files.length) {
    const empty = document.createElement("p");
    empty.className = "empty-text inline";
    empty.textContent = "暂无备份。";
    els.scheduledBackupConfigList.appendChild(empty);
    return;
  }
  for (const item of files) {
    els.scheduledBackupConfigList.appendChild(createScheduledBackupRow(item));
  }
}

function renderExportBackupList() {
  els.exportBackupList.replaceChildren();
  const files = (scheduledBackupState.backup_files || []).slice(0, 3);
  els.emptyExportBackupText.classList.toggle("is-hidden", files.length > 0);
  for (const item of files) {
    els.exportBackupList.appendChild(createScheduledBackupRow(item));
  }
}

function openCapacityWarningDialog(capacity, imageIds) {
  pendingCapacityActionImageIds = Array.isArray(imageIds) ? imageIds : [];
  const limit = asInt(capacity?.limit);
  const current = asInt(capacity?.current);
  const selected = asInt(capacity?.selected);
  const overflow = asInt(capacity?.overflow);
  els.capacityWarningText.textContent =
    `当前固化图像库上限为 ${limit} 张，已有 ${current} 张，本次预计入库 ${selected} 张，超出 ${overflow} 张。请选择处理方式。`;
  els.solidifiedCapacityOverlay.classList.remove("is-hidden");
}

function closeCapacityWarningDialog(clearSelection = true) {
  pendingCapacityActionImageIds = [];
  els.solidifiedCapacityOverlay.classList.add("is-hidden");
  if (clearSelection) {
    selectedPendingImageIds.clear();
    syncPendingSelectionView();
  }
}

async function openUploadDialog() {
  els.uploadMessage.textContent = "";
  els.uploadOverlay.classList.remove("is-hidden");
}

async function openUploadDialogWithProviderCheck() {
  if (uploadProviderCheckInProgress) {
    return;
  }
  uploadProviderCheckInProgress = true;
  try {
    const config = await pluginApiGet("caption_provider_config");
    if (String(config?.provider_id || "").trim()) {
      await openUploadDialog();
      return;
    }
    openProviderWarningDialog(config || {}, openUploadDialog);
  } catch (error) {
    openProviderWarningDialog({
      provider_id: "",
      provider_options: [],
      load_error: error.message || String(error),
    }, openUploadDialog);
  } finally {
    uploadProviderCheckInProgress = false;
  }
}

async function ensureCaptionProviderConfigured(continueAction) {
  try {
    const config = await pluginApiGet("caption_provider_config");
    if (String(config?.provider_id || "").trim()) {
      return true;
    }
    openProviderWarningDialog(config || {}, continueAction);
  } catch (error) {
    openProviderWarningDialog(
      {
        provider_id: "",
        provider_options: [],
        load_error: error.message || String(error),
      },
      continueAction,
    );
  }
  return false;
}

function closeUploadDialog() {
  els.uploadOverlay.classList.add("is-hidden");
  els.uploadMessage.textContent = "";
}

function fillProviderSelect(selectEl, config) {
  const options = Array.isArray(config.provider_options)
    ? config.provider_options
    : [];
  const selectedId = String(
    config.default_image_caption_provider_id || config.provider_id || "",
  );
  selectEl.replaceChildren();

  const warningOption = document.createElement("option");
  warningOption.value = "";
  warningOption.textContent = "需要选择一个可用的图片转述模型";
  warningOption.selected = selectedId === "";
  warningOption.className = "provider-warning-option";
  selectEl.appendChild(warningOption);

  for (const item of options) {
    const providerId = String(item.id || "");
    if (!providerId) {
      continue;
    }
    const option = document.createElement("option");
    option.value = providerId;
    option.textContent = item.label || providerId;
    option.selected = providerId === selectedId;
    selectEl.appendChild(option);
  }
  return selectedId;
}

function fillCaptionProviderSelect(config) {
  const selectedId = fillProviderSelect(els.captionProviderInput, config);
  renderCaptionProviderWarning(selectedId);
}

function renderCaptionProviderWarning(providerId) {
  const missing = !String(providerId || "").trim();
  els.captionProviderInput.classList.toggle("warning-select", missing);
  els.captionProviderWarning.classList.toggle("is-hidden", !missing);
}

function renderWarningCaptionProviderWarning(providerId) {
  const missing = !String(providerId || "").trim();
  els.warningCaptionProviderInput.classList.toggle("warning-select", missing);
  els.warningCaptionProviderHint.classList.toggle("is-hidden", !missing);
}

function fillProviderWarningDialog(config) {
  warningProviderConfig = config || {};
  const selectedId = fillProviderSelect(
    els.warningCaptionProviderInput,
    warningProviderConfig,
  );
  renderWarningCaptionProviderWarning(selectedId);
  if (warningProviderConfig.load_error) {
    els.providerWarningMessage.textContent = `读取模型配置失败：${warningProviderConfig.load_error}`;
  } else if (selectedId) {
    els.providerWarningMessage.textContent = "图片转述模型已配置，可以继续。";
  } else {
    els.providerWarningMessage.textContent = "";
  }
}

function openProviderWarningDialog(config, continueAction = null) {
  providerWarningContinueAction =
    typeof continueAction === "function" ? continueAction : null;
  fillProviderWarningDialog(config || {});
  els.providerWarningOverlay.classList.remove("is-hidden");
}

function closeProviderWarningDialog() {
  providerWarningContinueAction = null;
  els.providerWarningOverlay.classList.add("is-hidden");
  els.providerWarningMessage.textContent = "";
}

async function saveProviderWarningSelection() {
  const providerId = els.warningCaptionProviderInput.value;
  renderWarningCaptionProviderWarning(providerId);
  els.warningCaptionProviderInput.disabled = true;
  els.providerWarningContinueButton.disabled = true;
  els.providerWarningMessage.textContent = "正在保存图片转述模型设置...";
  let saved = false;
  try {
    const config = await pluginApiPost("caption_provider_config", {
      provider_id: providerId,
    });
    warningProviderConfig = config || {};
    if (tagCategorySettings) {
      tagCategorySettings.default_image_caption_provider_id =
        warningProviderConfig.provider_id || "";
      tagCategorySettings.provider_id = warningProviderConfig.provider_id || "";
    }
    fillProviderWarningDialog(warningProviderConfig);
    els.providerWarningMessage.textContent = providerId
      ? "图片转述模型设置已保存。"
      : "已清空图片转述模型设置。";
    saved = true;
  } catch (error) {
    els.providerWarningMessage.textContent = `保存失败：${error.message || error}`;
  } finally {
    els.warningCaptionProviderInput.disabled = false;
    els.providerWarningContinueButton.disabled = false;
  }
  return saved;
}

async function continueFromProviderWarning() {
  const providerId = String(els.warningCaptionProviderInput.value || "").trim();
  if (!providerId) {
    renderWarningCaptionProviderWarning("");
    els.providerWarningMessage.textContent =
      "请先选择一个可用的默认图片转述模型。";
    return;
  }
  const savedProviderId = String(warningProviderConfig?.provider_id || "").trim();
  if (savedProviderId !== providerId) {
    const saved = await saveProviderWarningSelection();
    if (!saved) {
      return;
    }
  }
  const action = providerWarningContinueAction;
  closeProviderWarningDialog();
  if (action) {
    await action();
  } else {
    await openUploadDialog();
  }
}

async function openTagCategoryDialog() {
  els.tagCategoryMessage.textContent = "正在读取配置...";
  els.tagCategorySaveButton.disabled = true;
  els.tagCategoryRecaptionInput.checked = false;
  els.tagCategoryOverlay.classList.remove("is-hidden");
  try {
    const settings = await pluginApiGet("caption_tag_category_settings");
    fillTagCategoryDialog(settings || {});
    els.tagCategoryMessage.textContent = "";
  } catch (error) {
    els.tagCategoryMessage.textContent = `读取配置失败：${error.message || error}`;
  } finally {
    els.tagCategorySaveButton.disabled = false;
  }
}

function closeTagCategoryDialog() {
  els.tagCategoryOverlay.classList.add("is-hidden");
  els.tagCategoryMessage.textContent = "";
  els.tagCategoryRecaptionInput.checked = false;
}

function fillTagCategoryDialog(settings) {
  tagCategorySettings = settings;
  const presetCategories = settings.preset_categories || {};
  const enabledPresets = Array.isArray(settings.enabled_presets)
    ? settings.enabled_presets
    : [];
  fillCaptionProviderSelect(settings || {});
  els.tagCategoryPresetChoices.replaceChildren();
  for (const [key, labelText] of Object.entries(presetCategories)) {
    const label = document.createElement("label");
    label.className = "preset-category-option";

    const input = document.createElement("input");
    input.type = "checkbox";
    input.value = key;
    input.checked = enabledPresets.includes(key);

    const text = document.createElement("span");
    text.textContent = labelText;

    label.append(input, text);
    els.tagCategoryPresetChoices.appendChild(label);
  }
  els.tagCategoryCustomInput.value = Array.isArray(settings.custom_categories)
    ? settings.custom_categories.join(" ")
    : "";
  els.tagCategoryRecaptionInput.checked = false;
}

function readTagCategoryDialog() {
  return {
    default_image_caption_provider_id: els.captionProviderInput.value,
    enabled_presets: Array.from(
      els.tagCategoryPresetChoices.querySelectorAll(
        "input[type='checkbox']:checked",
      ),
    ).map((input) => input.value),
    custom_categories: normalizeTags(els.tagCategoryCustomInput.value),
    recaption_all: els.tagCategoryRecaptionInput.checked,
  };
}

function tagCategoryConfigChanged(nextSettings) {
  const current = tagCategorySettings || {};
  const currentEnabled = Array.isArray(current.enabled_presets)
    ? current.enabled_presets
    : [];
  const nextEnabled = Array.isArray(nextSettings.enabled_presets)
    ? nextSettings.enabled_presets
    : [];
  const currentCustom = Array.isArray(current.custom_categories)
    ? current.custom_categories
    : [];
  const nextCustom = Array.isArray(nextSettings.custom_categories)
    ? nextSettings.custom_categories
    : [];
  return (
    JSON.stringify(currentEnabled) !== JSON.stringify(nextEnabled) ||
    JSON.stringify(currentCustom) !== JSON.stringify(nextCustom)
  );
}

function captionProviderConfigChanged(nextSettings) {
  const current = tagCategorySettings || {};
  return (
    String(current.default_image_caption_provider_id || "") !==
    String(nextSettings.default_image_caption_provider_id || "")
  );
}

async function openProactiveEmojiDialog() {
  els.proactiveEmojiMessage.textContent = "正在读取配置...";
  els.proactiveEmojiSaveButton.disabled = true;
  els.proactiveEmojiOverlay.classList.remove("is-hidden");
  try {
    const config = await pluginApiGet("proactive_emoji_config");
    fillProactiveEmojiDialog(config || {});
    els.proactiveEmojiMessage.textContent = "";
  } catch (error) {
    els.proactiveEmojiMessage.textContent = `读取配置失败：${error.message || error}`;
  } finally {
    els.proactiveEmojiSaveButton.disabled = false;
  }
}

function closeProactiveEmojiDialog() {
  els.proactiveEmojiOverlay.classList.add("is-hidden");
  els.proactiveEmojiMessage.textContent = "";
}

function fillProactiveEmojiDialog(config) {
  els.proactiveEmojiEnabledInput.checked = config.enabled === true;
  els.proactiveEmojiMemeOnlyInput.checked = config.meme_only !== false;
  els.proactiveEmojiEmbedInput.checked = config.embed_in_conversation !== false;
  els.proactiveEmojiProbabilityInput.value = String(
    config.trigger_probability ?? "0.25",
  );
  renderProactiveEmojiProviderOptions(
    Array.isArray(config.provider_options) ? config.provider_options : [],
    config.analysis_provider_id || "",
  );
}

function renderProactiveEmojiProviderOptions(options, selectedId) {
  renderProviderOptions(
    els.proactiveEmojiProviderInput,
    options,
    selectedId,
  );
}

function renderProviderOptions(selectEl, options, selectedId) {
  selectEl.replaceChildren();
  const normalizedOptions = options.length
    ? options
    : [{ id: "", label: "继承 AstrBot 当前会话模型" }];
  for (const item of normalizedOptions) {
    const option = document.createElement("option");
    option.value = String(item.id || "");
    option.textContent = item.label || item.id || "继承 AstrBot 当前会话模型";
    option.selected = option.value === String(selectedId || "");
    selectEl.appendChild(option);
  }
  if (!Array.from(selectEl.options).some((option) => option.selected)) {
    selectEl.value = "";
  }
}

function normalizeModelFallbackProviderIds(rawIds) {
  const ids = [];
  const seen = new Set();
  const providerIds = new Set(
    (modelFallbackConfigCache.provider_options || [])
      .map((item) => String(item.id || "").trim())
      .filter(Boolean),
  );
  for (const rawId of Array.isArray(rawIds) ? rawIds : []) {
    const providerId = String(rawId || "").trim();
    if (
      !providerId ||
      seen.has(providerId) ||
      (providerIds.size > 0 && !providerIds.has(providerId))
    ) {
      continue;
    }
    seen.add(providerId);
    ids.push(providerId);
  }
  return ids;
}

function setModelFallbackMode(mode) {
  modelFallbackConfigCache.mode = mode === "manual" ? "manual" : "inherit";
  if (els.modelFallbackModeInheritInput) {
    els.modelFallbackModeInheritInput.checked =
      modelFallbackConfigCache.mode !== "manual";
  }
  if (els.modelFallbackModeManualInput) {
    els.modelFallbackModeManualInput.checked =
      modelFallbackConfigCache.mode === "manual";
  }
  if (els.modelFallbackManualPanel) {
    els.modelFallbackManualPanel.classList.toggle(
      "is-hidden",
      modelFallbackConfigCache.mode !== "manual",
    );
  }
}

function modelFallbackProviderLabel(providerId) {
  const option = (modelFallbackConfigCache.provider_options || []).find(
    (item) => String(item.id || "") === String(providerId || ""),
  );
  return option?.label || providerId;
}

function renderModelFallbackProviderSelect() {
  if (!els.modelFallbackProviderSelect) {
    return;
  }
  const selectedIds = new Set(modelFallbackConfigCache.provider_ids || []);
  const options = (modelFallbackConfigCache.provider_options || []).filter(
    (item) => item.id && !selectedIds.has(String(item.id)),
  );
  els.modelFallbackProviderSelect.replaceChildren();
  for (const item of options) {
    const option = document.createElement("option");
    option.value = String(item.id || "");
    option.textContent = item.label || item.id;
    els.modelFallbackProviderSelect.appendChild(option);
  }
  const hasOptions = options.length > 0;
  els.modelFallbackProviderSelect.disabled = !hasOptions;
  if (els.modelFallbackAddButton) {
    els.modelFallbackAddButton.disabled = !hasOptions;
  }
}

function renderModelFallbackProviderList() {
  if (!els.modelFallbackProviderList) {
    return;
  }
  els.modelFallbackProviderList.replaceChildren();
  const providerIds = modelFallbackConfigCache.provider_ids || [];
  els.modelFallbackEmptyText?.classList.toggle("is-hidden", providerIds.length > 0);
  providerIds.forEach((providerId, index) => {
    const row = document.createElement("div");
    row.className = "fallback-provider-row";

    const info = document.createElement("div");
    info.className = "fallback-provider-info";
    const title = document.createElement("strong");
    title.textContent = modelFallbackProviderLabel(providerId);
    const idText = document.createElement("span");
    idText.textContent = providerId;
    info.append(title, idText);

    const actions = document.createElement("div");
    actions.className = "fallback-provider-actions";
    const upButton = document.createElement("button");
    upButton.type = "button";
    upButton.className = "secondary compact-button";
    upButton.textContent = "↑";
    upButton.disabled = index === 0;
    upButton.addEventListener("click", () =>
      moveModelFallbackProvider(index, -1),
    );
    const downButton = document.createElement("button");
    downButton.type = "button";
    downButton.className = "secondary compact-button";
    downButton.textContent = "↓";
    downButton.disabled = index === providerIds.length - 1;
    downButton.addEventListener("click", () =>
      moveModelFallbackProvider(index, 1),
    );
    const removeButton = document.createElement("button");
    removeButton.type = "button";
    removeButton.className = "danger-button compact-button";
    removeButton.innerHTML = LIBRARY_MODE_ICONS.trash;
    removeButton.setAttribute("aria-label", "删除");
    removeButton.title = "删除";
    removeButton.addEventListener("click", () =>
      removeModelFallbackProvider(index),
    );
    actions.append(upButton, downButton, removeButton);

    row.append(info, actions);
    els.modelFallbackProviderList.appendChild(row);
  });
  renderModelFallbackProviderSelect();
}

function addModelFallbackProvider() {
  const providerId = String(els.modelFallbackProviderSelect?.value || "").trim();
  if (!providerId || modelFallbackConfigCache.provider_ids.includes(providerId)) {
    return;
  }
  modelFallbackConfigCache.provider_ids.push(providerId);
  renderModelFallbackProviderList();
}

function moveModelFallbackProvider(index, direction) {
  const providerIds = modelFallbackConfigCache.provider_ids || [];
  const nextIndex = index + direction;
  if (nextIndex < 0 || nextIndex >= providerIds.length) {
    return;
  }
  [providerIds[index], providerIds[nextIndex]] = [
    providerIds[nextIndex],
    providerIds[index],
  ];
  renderModelFallbackProviderList();
}

function removeModelFallbackProvider(index) {
  modelFallbackConfigCache.provider_ids.splice(index, 1);
  renderModelFallbackProviderList();
}

function fillModelFallbackConfig(config) {
  const providerOptions = Array.isArray(config.provider_options)
    ? config.provider_options.filter((item) => item?.id)
    : [];
  modelFallbackConfigCache = {
    mode: config.mode === "manual" ? "manual" : "inherit",
    provider_ids: [],
    provider_options: providerOptions,
    astrbot_fallback_provider_ids: Array.isArray(config.astrbot_fallback_provider_ids)
      ? config.astrbot_fallback_provider_ids
      : [],
  };
  modelFallbackConfigCache.provider_ids = normalizeModelFallbackProviderIds(
    Array.isArray(config.provider_ids)
      ? config.provider_ids
      : [config.priority_1, config.priority_2, config.priority_3],
  );
  setModelFallbackMode(modelFallbackConfigCache.mode);
  renderModelFallbackProviderList();
}

function readModelFallbackConfig() {
  const providerIds = normalizeModelFallbackProviderIds(
    modelFallbackConfigCache.provider_ids || [],
  );
  return {
    mode: modelFallbackConfigCache.mode === "manual" ? "manual" : "inherit",
    provider_ids: providerIds,
    priority_1: providerIds[0] || "",
    priority_2: providerIds[1] || "",
    priority_3: providerIds[2] || "",
  };
}

function readProactiveEmojiDialog() {
  return {
    enabled: els.proactiveEmojiEnabledInput.checked,
    analysis_provider_id: els.proactiveEmojiProviderInput.value,
    meme_only: els.proactiveEmojiMemeOnlyInput.checked,
    embed_in_conversation: els.proactiveEmojiEmbedInput.checked,
    trigger_probability: String(
      clampProbability(els.proactiveEmojiProbabilityInput.value),
    ),
  };
}

async function openAutoCollectionDialog() {
  els.autoCollectionMessage.textContent = "正在读取配置...";
  els.autoCollectionSaveButton.disabled = true;
  els.autoCollectionOverlay.classList.remove("is-hidden");
  try {
    const config = await pluginApiGet("auto_collection_config");
    fillAutoCollectionDialog(config || {});
    els.autoCollectionMessage.textContent = "";
  } catch (error) {
    els.autoCollectionMessage.textContent = `读取配置失败：${error.message || error}`;
  } finally {
    els.autoCollectionSaveButton.disabled = false;
  }
}

function closeAutoCollectionDialog() {
  els.autoCollectionOverlay.classList.add("is-hidden");
  els.autoCollectionMessage.textContent = "";
}

function fillAutoCollectionDialog(config) {
  els.autoCollectionEnabledInput.checked = config.enabled === true;
  els.autoCollectionIncludeInput.checked = config.include_in_features === true;
  els.autoCollectionGroupsInput.value = Array.isArray(config.source_groups)
    ? config.source_groups.join("\n")
    : "";
  els.autoCollectionMaxSizeInput.value = String(config.max_file_size_kb ?? 1024);
  els.autoCollectionPendingLimitInput.value = String(
    config.pending_pool_limit ?? 100,
  );
  els.autoCollectionTtlInput.value = String(config.pending_ttl_days ?? 3);
  els.autoCollectionAutoAcceptInput.checked = config.auto_accept === true;
  els.autoCollectionRejectDiscardedInput.checked =
    config.auto_reject_discarded === true;
  els.autoCollectionSolidifiedLimitInput.value = String(
    config.solidified_library_limit ?? 300,
  );
}

function readAutoCollectionDialog() {
  return {
    enabled: els.autoCollectionEnabledInput.checked,
    include_in_features: els.autoCollectionIncludeInput.checked,
    source_groups: normalizeTags(els.autoCollectionGroupsInput.value),
    max_file_size_kb: clampInt(els.autoCollectionMaxSizeInput.value, 1024, 1),
    pending_pool_limit: clampInt(
      els.autoCollectionPendingLimitInput.value,
      100,
      0,
    ),
    pending_ttl_days: clampInt(els.autoCollectionTtlInput.value, 3, 0),
    auto_accept: els.autoCollectionAutoAcceptInput.checked,
    auto_reject_discarded: els.autoCollectionRejectDiscardedInput.checked,
    solidified_library_limit: clampInt(
      els.autoCollectionSolidifiedLimitInput.value,
      300,
      -1,
    ),
  };
}

async function openMemeCombatDialog() {
  els.memeCombatMessage.textContent = "正在读取配置...";
  els.memeCombatSaveButton.disabled = true;
  els.memeCombatOverlay.classList.remove("is-hidden");
  try {
    const config = await pluginApiGet("meme_combat_config");
    fillMemeCombatDialog(config || {});
    els.memeCombatMessage.textContent = "";
  } catch (error) {
    els.memeCombatMessage.textContent = `读取配置失败：${error.message || error}`;
  } finally {
    els.memeCombatSaveButton.disabled = false;
  }
}

function closeMemeCombatDialog() {
  els.memeCombatOverlay.classList.add("is-hidden");
  els.memeCombatMessage.textContent = "";
}

function fillMemeCombatDialog(config) {
  const follow = config.follow_pattern || {};
  const burst = config.image_burst || {};
  const battle = config.battle || {};
  els.memeCombatEnabledInput.checked = config.enabled === true;
  els.memeCombatFollowEnabledInput.checked = follow.enabled !== false;
  els.memeCombatFollowWindowInput.value = String(
    follow.time_window_seconds ?? 30,
  );
  els.memeCombatFollowCountInput.value = String(follow.same_image_count ?? 3);
  els.memeCombatFollowDistinctUsersInput.checked =
    follow.distinct_users_required === true;
  els.memeCombatBurstEnabledInput.checked = burst.enabled !== false;
  els.memeCombatBurstProbabilityInput.value = String(
    burst.trigger_probability ?? "0.2",
  );
  els.memeCombatBurstCountInput.value = String(burst.burst_count ?? 2);
  els.memeCombatBattleEnabledInput.checked = battle.enabled !== false;
  els.memeCombatBattleWindowInput.value = String(
    battle.time_window_seconds ?? 30,
  );
  els.memeCombatBattleCountInput.value = String(
    battle.continuous_image_count ?? 6,
  );
  renderProviderOptions(
    els.memeCombatBattleProviderInput,
    Array.isArray(config.provider_options) ? config.provider_options : [],
    battle.analysis_provider_id || "",
  );
}

function readMemeCombatDialog() {
  return {
    enabled: els.memeCombatEnabledInput.checked,
    follow_pattern: {
      enabled: els.memeCombatFollowEnabledInput.checked,
      time_window_seconds: clampIntRange(
        els.memeCombatFollowWindowInput.value,
        30,
        1,
        600,
      ),
      same_image_count: clampIntRange(
        els.memeCombatFollowCountInput.value,
        3,
        2,
        20,
      ),
      distinct_users_required: els.memeCombatFollowDistinctUsersInput.checked,
    },
    image_burst: {
      enabled: els.memeCombatBurstEnabledInput.checked,
      trigger_probability: String(
        clampProbability(els.memeCombatBurstProbabilityInput.value),
      ),
      burst_count: clampIntRange(
        els.memeCombatBurstCountInput.value,
        2,
        1,
        6,
      ),
    },
    battle: {
      enabled: els.memeCombatBattleEnabledInput.checked,
      time_window_seconds: clampIntRange(
        els.memeCombatBattleWindowInput.value,
        30,
        1,
        600,
      ),
      continuous_image_count: clampIntRange(
        els.memeCombatBattleCountInput.value,
        6,
        2,
        30,
      ),
      analysis_provider_id: els.memeCombatBattleProviderInput.value,
    },
  };
}

async function openUserSearchDialog() {
  els.userSearchMessage.textContent = "正在读取配置...";
  els.userSearchSaveButton.disabled = true;
  els.userSearchOverlay.classList.remove("is-hidden");
  try {
    const config = await pluginApiGet("caption_plugin_config");
    fillUserSearchDialog(config || {});
    els.userSearchMessage.textContent = "";
  } catch (error) {
    els.userSearchMessage.textContent = `读取配置失败：${error.message || error}`;
  } finally {
    els.userSearchSaveButton.disabled = false;
  }
}

function closeUserSearchDialog() {
  els.userSearchOverlay.classList.add("is-hidden");
  els.userSearchMessage.textContent = "";
}

function fillUserSearchDialog(config) {
  const reply = config.reply_after_search || {};
  const flow = config.user_search_flow || {};
  const keywords = Array.isArray(flow.request_keywords)
    ? flow.request_keywords
    : config.request_keywords;
  els.userSearchEnabledInput.checked = flow.enabled !== undefined
    ? flow.enabled !== false
    : config.user_search_enabled !== false;
  els.configKeywordsInput.value = Array.isArray(keywords)
    ? keywords.join("\n")
    : "";
  els.configUseCustomReplyInput.checked = reply.use_custom_reply !== false;
  els.configCustomReplyInput.value =
    reply.custom_reply || "找到一张比较合适的图。";
  els.configLlmReplyWhenNotFoundInput.checked =
    reply.llm_reply_when_not_found === true;
  els.configNotFoundReplyInput.value =
    reply.not_found_reply || "图库里暂时没有找到特别合适的图片。";
  els.configEmptyLibraryReplyInput.value =
    reply.empty_library_reply ||
    "图库里还没有可用图片，请先在插件配置里上传图片。";
}

function readUserSearchDialog() {
  return {
    user_search_flow: {
      enabled: els.userSearchEnabledInput.checked,
      request_keywords: normalizeTags(els.configKeywordsInput.value),
    },
    reply_after_search: {
      use_custom_reply: els.configUseCustomReplyInput.checked,
      custom_reply: els.configCustomReplyInput.value.trim(),
      llm_reply_when_not_found: els.configLlmReplyWhenNotFoundInput.checked,
      not_found_reply: els.configNotFoundReplyInput.value.trim(),
      empty_library_reply: els.configEmptyLibraryReplyInput.value.trim(),
    },
  };
}

async function openConfigDialog() {
  els.configMessage.textContent = "正在读取配置...";
  els.configSaveButton.disabled = true;
  els.configOverlay.classList.remove("is-hidden");
  try {
    const [config, backupState] = await Promise.all([
      pluginApiGet("caption_plugin_config"),
      pluginApiGet("scheduled_backup_list"),
    ]);
    applyScheduledBackupState(backupState || {});
    fillConfigDialog(config || {});
    els.configMessage.textContent = "";
  } catch (error) {
    els.configMessage.textContent = `读取配置失败：${error.message || error}`;
  } finally {
    els.configSaveButton.disabled = false;
  }
}

function closeConfigDialog() {
  els.configOverlay.classList.add("is-hidden");
  els.configMessage.textContent = "";
}

function fillConfigDialog(config) {
  els.configHiddenImagesInput.value = Array.isArray(config.hidden_images)
    ? config.hidden_images.join("\n")
    : "";
  els.configSyncOnStartupInput.checked = config.sync_on_startup !== false;
  els.configConfidenceInput.value = clampConfidence(
    config.match_confidence_threshold,
  ).toFixed(2);
  els.configLibraryDefaultViewModeInput.value =
    config.page_library_default_view_mode === "gallery" ? "gallery" : "list";
  const backupConfig = config.scheduled_backup || scheduledBackupState;
  scheduledBackupState = {
    ...scheduledBackupState,
    ...(backupConfig || {}),
    backup_files: scheduledBackupState.backup_files || [],
  };
  els.scheduledBackupEnabledInput.checked = backupConfig?.enabled !== false;
  els.scheduledBackupTimeInput.value = normalizeBackupTime(
    backupConfig?.backup_time || "06:00",
  );
  els.scheduledBackupLimitInput.value = String(
    clampInt(backupConfig?.backup_limit, 3, 1),
  );
  renderScheduledBackupConfigList();
  fillModelFallbackConfig(config.model_fallback_options || {});
}

function readConfigDialog() {
  return {
    hidden_images: normalizePathList(els.configHiddenImagesInput.value),
    sync_on_startup: els.configSyncOnStartupInput.checked,
    match_confidence_threshold: clampConfidence(els.configConfidenceInput.value),
    page_library_default_view_mode:
      els.configLibraryDefaultViewModeInput.value === "gallery"
        ? "gallery"
        : "list",
    scheduled_backup: {
      enabled: els.scheduledBackupEnabledInput.checked,
      backup_time: normalizeBackupTime(els.scheduledBackupTimeInput.value),
      backup_limit: clampInt(els.scheduledBackupLimitInput.value, 3, 1),
    },
    model_fallback_options: readModelFallbackConfig(),
  };
}

function renderGlobalTagChoices(selectedTags) {
  els.globalTagChoices.replaceChildren();
  if (!globalTags.length) {
    const empty = document.createElement("p");
    empty.className = "empty-text inline";
    empty.textContent = "暂无公共特征标签。";
    els.globalTagChoices.appendChild(empty);
    return;
  }

  for (const tag of globalTags) {
    const label = document.createElement("label");
    label.className = "global-tag-option";

    const input = document.createElement("input");
    input.type = "checkbox";
    input.value = tag;
    input.checked = selectedTags.includes(tag);

    const text = document.createElement("span");
    text.textContent = tag;

    label.append(input, text);
    els.globalTagChoices.appendChild(label);
  }
}

function selectedGlobalTags() {
  return Array.from(
    els.globalTagChoices.querySelectorAll("input[type='checkbox']:checked"),
  ).map((input) => input.value);
}

async function saveEditor() {
  if (!editingImage) {
    return;
  }
  els.editorSaveButton.disabled = true;
  els.editorMessage.textContent = "正在保存...";
  try {
    const result = await pluginApiPost("caption_update_tags", {
      image_id: editingImage.id,
      library_source: editingImage.library_source || MANUAL_LIBRARY_SOURCE,
      tags: normalizeTags(els.tagInput.value),
      selected_global_tags: selectedGlobalTags(),
    });
    if (result?.library) {
      applyLibraryState(result.library, { force: true });
    } else {
      await refreshLibrary();
    }
    els.editorMessage.textContent = "已保存。";
    window.setTimeout(closeEditor, 350);
  } catch (error) {
    els.editorMessage.textContent = `保存失败：${error.message || error}`;
  } finally {
    els.editorSaveButton.disabled = false;
  }
}

async function saveGlobalTags() {
  els.globalTagsSaveButton.disabled = true;
  els.globalTagsMessage.textContent = "正在保存...";
  try {
    const result = await pluginApiPost("caption_update_global_tags", {
      global_tags: normalizeTags(els.globalTagsInput.value),
    });
    if (result?.library) {
      globalTagsDirty = false;
      applyLibraryState(result.library, { force: true });
    } else {
      await refreshLibrary();
    }
    els.globalTagsMessage.textContent = "已保存。";
    window.setTimeout(() => {
      els.globalTagsMessage.textContent = "";
    }, 1200);
  } catch (error) {
    els.globalTagsMessage.textContent = `保存失败：${error.message || error}`;
  } finally {
    els.globalTagsSaveButton.disabled = false;
  }
}

async function saveTagCategoryDialog() {
  const payload = readTagCategoryDialog();
  const changed = tagCategoryConfigChanged(payload);
  const providerChanged = captionProviderConfigChanged(payload);
  els.tagCategorySaveButton.disabled = true;
  els.tagCategoryCancelButton.disabled = true;
  els.tagCategoryMessage.textContent = "正在保存配置...";
  try {
    const result = await pluginApiPost("caption_tag_category_settings", payload);
    if (result?.settings) {
      fillTagCategoryDialog(result.settings);
    }
    if (result?.progress) {
      renderProgress(result.progress);
    }
    if (result?.library) {
      applyLibraryState(result.library, { force: true });
    }
    if (changed && payload.recaption_all) {
      els.tagCategoryMessage.textContent =
        "已保存，正在使用新的标签类别重新加载图库。";
      await refreshAll();
    } else if (changed) {
      els.tagCategoryMessage.textContent =
        "已保存。新的标签类别会应用于之后上传的新图片。";
    } else if (providerChanged) {
      els.tagCategoryMessage.textContent = "图片转述模型设置已保存。";
    } else {
      els.tagCategoryMessage.textContent = "配置没有变化。";
    }
    window.setTimeout(closeTagCategoryDialog, 650);
  } catch (error) {
    els.tagCategoryMessage.textContent = `保存配置失败：${error.message || error}`;
  } finally {
    els.tagCategorySaveButton.disabled = false;
    els.tagCategoryCancelButton.disabled = false;
  }
}

async function saveProactiveEmojiDialog() {
  els.proactiveEmojiSaveButton.disabled = true;
  els.proactiveEmojiCancelButton.disabled = true;
  els.proactiveEmojiMessage.textContent = "正在保存配置...";
  try {
    const config = await pluginApiPost(
      "proactive_emoji_config",
      readProactiveEmojiDialog(),
    );
    fillProactiveEmojiDialog(config || {});
    els.proactiveEmojiMessage.textContent = "已保存。";
    window.setTimeout(closeProactiveEmojiDialog, 350);
  } catch (error) {
    els.proactiveEmojiMessage.textContent = `保存配置失败：${error.message || error}`;
  } finally {
    els.proactiveEmojiSaveButton.disabled = false;
    els.proactiveEmojiCancelButton.disabled = false;
  }
}

async function saveAutoCollectionDialog() {
  els.autoCollectionSaveButton.disabled = true;
  els.autoCollectionCancelButton.disabled = true;
  els.autoCollectionMessage.textContent = "正在保存配置...";
  try {
    const config = await pluginApiPost(
      "auto_collection_config",
      readAutoCollectionDialog(),
    );
    autoCollectionConfigCache = {
      ...autoCollectionConfigCache,
      ...(config || {}),
    };
    fillAutoCollectionDialog(config || {});
    els.autoCollectionMessage.textContent = "已保存。";
    await refreshPendingPool();
    window.setTimeout(closeAutoCollectionDialog, 350);
  } catch (error) {
    els.autoCollectionMessage.textContent = `保存配置失败：${error.message || error}`;
  } finally {
    els.autoCollectionSaveButton.disabled = false;
    els.autoCollectionCancelButton.disabled = false;
  }
}

async function saveMemeCombatDialog() {
  els.memeCombatSaveButton.disabled = true;
  els.memeCombatCancelButton.disabled = true;
  els.memeCombatMessage.textContent = "正在保存配置...";
  try {
    const config = await pluginApiPost(
      "meme_combat_config",
      readMemeCombatDialog(),
    );
    fillMemeCombatDialog(config || {});
    els.memeCombatMessage.textContent = "已保存。";
    window.setTimeout(closeMemeCombatDialog, 350);
  } catch (error) {
    els.memeCombatMessage.textContent = `保存配置失败：${error.message || error}`;
  } finally {
    els.memeCombatSaveButton.disabled = false;
    els.memeCombatCancelButton.disabled = false;
  }
}

async function saveUserSearchDialog() {
  els.userSearchSaveButton.disabled = true;
  els.userSearchCancelButton.disabled = true;
  els.userSearchMessage.textContent = "正在保存配置...";
  try {
    const savedConfig = await pluginApiPost(
      "caption_plugin_config",
      readUserSearchDialog(),
    );
    fillUserSearchDialog(savedConfig || {});
    els.userSearchMessage.textContent = "已保存。";
    await refreshLibrary();
    window.setTimeout(closeUserSearchDialog, 350);
  } catch (error) {
    els.userSearchMessage.textContent = `保存配置失败：${error.message || error}`;
  } finally {
    els.userSearchSaveButton.disabled = false;
    els.userSearchCancelButton.disabled = false;
  }
}

async function saveConfigDialog() {
  els.configSaveButton.disabled = true;
  els.configCancelButton.disabled = true;
  els.configMessage.textContent = "正在保存配置...";
  try {
    const savedConfig = await pluginApiPost(
      "caption_plugin_config",
      readConfigDialog(),
    );
    fillConfigDialog(savedConfig || {});
    applyDefaultLibraryViewMode(savedConfig?.page_library_default_view_mode, true);
    await refreshScheduledBackups();
    els.configMessage.textContent = "已保存。";
    await refreshLibrary();
    window.setTimeout(closeConfigDialog, 350);
  } catch (error) {
    els.configMessage.textContent = `保存配置失败：${error.message || error}`;
  } finally {
    els.configSaveButton.disabled = false;
    els.configCancelButton.disabled = false;
  }
}

async function deleteImage(image, button, source = MANUAL_LIBRARY_SOURCE) {
  if (!image?.id) {
    return;
  }
  setDeleteButtonBusyState(button, true);
  try {
    const deletedImageId = String(image.id || "").trim();
    const result = await pluginApiPost("caption_delete_image", {
      image_id: image.id,
      library_source: source,
    });
    if (String(selectedGalleryImageId || "").trim() === deletedImageId) {
      selectedGalleryImageId = "";
    }
    if (String(selectedSolidifiedGalleryImageId || "").trim() === deletedImageId) {
      selectedSolidifiedGalleryImageId = "";
    }
    if (String(selectedExternalGalleryImageId || "").trim() === deletedImageId) {
      selectedExternalGalleryImageId = "";
    }
    if (result?.library) {
      applyLibraryState(result.library, { force: true });
    } else {
      await refreshLibrary();
    }
    if (editingImage?.id === image.id) {
      closeEditor();
    }
    await refreshAll();
  } catch (error) {
    setDeleteButtonBusyState(button, false);
    setMessage(`删除失败：${error.message || error}`);
  }
}

async function exportConfig() {
  await openExportDialog();
}

async function downloadScheduledBackup(item) {
  const backupId = item?.id || item?.filename || "";
  if (!backupId) {
    return;
  }
  setExportBusy(true);
  els.exportDialogMessage.textContent = "正在下载备份...";
  try {
    await pluginApiDownload(
      `scheduled_backup_download/${encodeURIComponent(backupId)}`,
      item.filename || "",
    );
    els.exportDialogMessage.textContent = "备份下载已开始，请查看浏览器下载列表。";
  } catch (error) {
    els.exportDialogMessage.textContent = `下载失败：${error.message || error}`;
  } finally {
    setExportBusy(false);
  }
}

async function manualExportConfig() {
  setExportBusy(true);
  els.exportDialogMessage.textContent = "正在创建备份...";
  try {
    const result = await pluginApiPost("scheduled_backup_create", {});
    applyScheduledBackupState({
      ...(result?.config || scheduledBackupState),
      backup_files: result?.backups || [],
      storage_dir: result?.storage_dir || scheduledBackupState.storage_dir,
    });
    const backup = result?.backup;
    if (backup) {
      await pluginApiDownload(
        `scheduled_backup_download/${encodeURIComponent(backup.id || backup.filename)}`,
        backup.filename || "",
      );
    }
    els.exportDialogMessage.textContent = "图库与配置已导出到默认下载目录。";
  } catch (error) {
    els.exportDialogMessage.textContent = `导出配置失败：${error.message || error}`;
  } finally {
    setExportBusy(false);
  }
}

async function deleteScheduledBackup(item) {
  const backupId = item?.id || item?.filename || "";
  if (!backupId) {
    return;
  }
  setExportBusy(true);
  els.exportDialogMessage.textContent = "正在删除备份...";
  try {
    const result = await pluginApiPost("scheduled_backup_delete", {
      backup_id: backupId,
    });
    applyScheduledBackupState({
      ...scheduledBackupState,
      backup_files: result?.backups || [],
    });
    els.exportDialogMessage.textContent = "备份已删除。";
  } catch (error) {
    els.exportDialogMessage.textContent = `删除失败：${error.message || error}`;
  } finally {
    setExportBusy(false);
  }
}

async function importConfig() {
  const file = els.importFileInput.files?.[0];
  if (!file) {
    els.importMessage.textContent = "请先选择通过导出配置获得的 ZIP 文件。";
    return;
  }
  if (!String(file.name || "").toLowerCase().endsWith(".zip")) {
    els.importMessage.textContent = "请选择 ZIP 备份文件。";
    return;
  }

  els.importConfirmButton.disabled = true;
  els.importCancelButton.disabled = true;
  els.importCloseButton.disabled = true;
  els.importMessage.textContent = "正在上传并导入备份...";

  try {
    const result = await uploadBackupConfig(
      file,
      els.importModeOverwrite.checked ? "overwrite" : "merge",
      els.importOverwriteConfig.checked,
    );

    if (result?.progress) {
      renderProgress(result.progress);
    }
    if (result?.library) {
      globalTagsDirty = false;
      imageUrlCache.clear();
      applyLibraryState(result.library, { force: true });
    }

    const stats = result?.result || {};
    els.importMessage.textContent = `导入完成：新增 ${asInt(stats.imported_images)} 张，跳过 ${asInt(stats.skipped_images)} 张。`;
    await refreshAll();
    window.setTimeout(closeImportDialog, 800);
  } catch (error) {
    els.importMessage.textContent = `导入配置失败：${error.message || error}`;
  } finally {
    els.importConfirmButton.disabled = false;
    els.importCancelButton.disabled = false;
    els.importCloseButton.disabled = false;
  }
}

function selectedPendingIds() {
  return Array.from(selectedPendingImageIds).filter(Boolean);
}

async function acceptSelectedPendingImages() {
  const imageIds = selectedPendingIds();
  if (!imageIds.length) {
    return;
  }
  await acceptPendingImagesWithCapacityAction(imageIds, "");
}

async function acceptPendingImagesWithCapacityAction(imageIds, capacityAction) {
  if (!imageIds.length) {
    return;
  }
  els.pendingAcceptButton.disabled = true;
  els.pendingDiscardButton.disabled = true;
  els.pendingPoolMessage.textContent = "正在入库选中的图片...";
  try {
    const payload = { image_ids: imageIds };
    if (capacityAction) {
      payload.capacity_action = capacityAction;
    }
    const result = await pluginApiPost("auto_collection_accept", payload);
    if (result?.result?.capacity_error) {
      openCapacityWarningDialog(result.result.capacity || {}, imageIds);
      els.pendingPoolMessage.textContent = "固化图像库容量不足，请选择处理方式。";
      return;
    }
    closeCapacityWarningDialog(false);
    selectedPendingImageIds.clear();
    if (result?.pool) {
      applyPendingPoolState(result.pool, { force: true });
    } else {
      await refreshPendingPool();
    }
    if (result?.library) {
      applyLibraryState(result.library, { force: true });
    } else {
      await refreshLibrary();
    }
    if (result?.progress) {
      renderProgress(result.progress);
    }
    const accepted = asInt(result?.result?.accepted?.length);
    const skipped = asInt(result?.result?.skipped?.length);
    els.pendingPoolMessage.textContent = `已入库 ${accepted} 张，跳过 ${skipped} 张。`;
    await refreshAll();
  } catch (error) {
    els.pendingPoolMessage.textContent = `入库失败：${error.message || error}`;
  } finally {
    syncPendingSelectionView();
  }
}

async function resolveCapacityWarning(action) {
  const imageIds = pendingCapacityActionImageIds.slice();
  if (!imageIds.length) {
    closeCapacityWarningDialog(true);
    return;
  }
  els.capacityDeleteOldestButton.disabled = true;
  els.capacityExpandButton.disabled = true;
  els.capacityCancelButton.disabled = true;
  els.capacityCancelTopButton.disabled = true;
  try {
    await acceptPendingImagesWithCapacityAction(imageIds, action);
  } finally {
    els.capacityDeleteOldestButton.disabled = false;
    els.capacityExpandButton.disabled = false;
    els.capacityCancelButton.disabled = false;
    els.capacityCancelTopButton.disabled = false;
  }
}

async function discardSelectedPendingImages() {
  const imageIds = selectedPendingIds();
  if (!imageIds.length) {
    return;
  }
  els.pendingAcceptButton.disabled = true;
  els.pendingDiscardButton.disabled = true;
  els.pendingPoolMessage.textContent = "正在丢弃选中的图片...";
  try {
    const result = await pluginApiPost("auto_collection_discard", {
      image_ids: imageIds,
    });
    selectedPendingImageIds.clear();
    if (result?.pool) {
      applyPendingPoolState(result.pool, { force: true });
    } else {
      await refreshPendingPool();
    }
    const discarded = asInt(result?.result?.discarded?.length);
    const skipped = asInt(result?.result?.skipped?.length);
    els.pendingPoolMessage.textContent = `已丢弃 ${discarded} 张，跳过 ${skipped} 张。`;
  } catch (error) {
    els.pendingPoolMessage.textContent = `丢弃失败：${error.message || error}`;
  } finally {
    syncPendingSelectionView();
  }
}

function toggleAllPendingSelection() {
  if (!pendingPoolImages.length) {
    return;
  }
  if (selectedPendingImageIds.size === pendingPoolImages.length) {
    selectedPendingImageIds.clear();
  } else {
    selectedPendingImageIds = new Set(
      pendingPoolImages.map((image) => String(image?.id || "")).filter(Boolean),
    );
  }
  syncPendingSelectionView();
}

async function uploadImages() {
  const files = Array.from(els.uploadInput.files || []);
  if (!files.length) {
    els.uploadMessage.textContent = "请先选择一张或多张图片。";
    return;
  }

  uploadedInThisPageSession = true;
  els.uploadButton.disabled = true;
  els.uploadInput.disabled = true;
  const uploaded = [];
  const errors = [];
  try {
    for (const [index, file] of files.entries()) {
      els.uploadMessage.textContent = `正在上传 ${index + 1}/${files.length}：${file.name}`;
      try {
        const result = await uploadImageFile(file);
        if (Array.isArray(result?.uploaded)) {
          uploaded.push(...result.uploaded);
        }
        if (Array.isArray(result?.errors)) {
          errors.push(...result.errors);
        }
        if (result?.progress) {
          renderProgress(result.progress);
        }
        if (result?.library) {
          applyLibraryState(result.library, { force: true });
        }
      } catch (error) {
        errors.push(`${file.name}: ${error.message || error}`);
      }
    }

    els.uploadInput.value = "";
    els.uploadMessage.textContent = errors.length
      ? `已上传 ${uploaded.length} 张，失败 ${errors.length} 个：${errors.join("；")}`
      : `已上传 ${uploaded.length} 张，正在后台生成特征标签。`;
    await refreshAll();
    if (uploaded.length) {
      closeUploadDialog();
    }
  } finally {
    els.uploadButton.disabled = false;
    els.uploadInput.disabled = false;
  }
}

els.refreshButton.addEventListener("click", refreshAll);
els.openUploadButton.addEventListener("click", openUploadDialogWithProviderCheck);
els.libraryManageButton.addEventListener("click", scrollToLibraryScopeSwitch);
els.manualLibraryScopeButton.addEventListener("click", () =>
  setLibraryScopeMode("manual"),
);
els.autoCollectionScopeButton.addEventListener("click", () =>
  setLibraryScopeMode("auto"),
);
els.externalImportScopeButton.addEventListener("click", () => {
  setLibraryScopeMode("external");
  refreshExternalImportPending();
});
els.imagebedImportScopeButton.addEventListener("click", () => {
  setLibraryScopeMode("imagebed");
  refreshImagebedImportPending().catch(() => {});
});
els.libraryListModeButton.addEventListener("click", () =>
  setLibraryViewMode("list", MANUAL_LIBRARY_SOURCE),
);
els.libraryGalleryModeButton.addEventListener("click", () =>
  setLibraryViewMode("gallery", MANUAL_LIBRARY_SOURCE),
);
els.solidifiedListModeButton.addEventListener("click", () =>
  setLibraryViewMode("list", SOLIDIFIED_LIBRARY_SOURCE),
);
els.solidifiedGalleryModeButton.addEventListener("click", () =>
  setLibraryViewMode("gallery", SOLIDIFIED_LIBRARY_SOURCE),
);
els.externalListModeButton.addEventListener("click", () =>
  setLibraryViewMode("list", EXTERNAL_LIBRARY_SOURCE),
);
els.externalGalleryModeButton.addEventListener("click", () =>
  setLibraryViewMode("gallery", EXTERNAL_LIBRARY_SOURCE),
);
els.imagebedListModeButton.addEventListener("click", () =>
  setLibraryViewMode("list", IMAGEBED_LIBRARY_SOURCE),
);
els.imagebedGalleryModeButton.addEventListener("click", () =>
  setLibraryViewMode("gallery", IMAGEBED_LIBRARY_SOURCE),
);
els.solidifiedBackToScopeButton.addEventListener(
  "click",
  scrollToLibraryScopeSwitch,
);
els.libraryTagSearchInput.addEventListener("input", (event) =>
  setLibraryTagSearch(MANUAL_LIBRARY_SOURCE, event.target.value),
);
els.libraryTagSearchClearButton.addEventListener("click", () =>
  setLibraryTagSearch(MANUAL_LIBRARY_SOURCE, ""),
);
els.solidifiedLibraryTagSearchInput.addEventListener("input", (event) =>
  setLibraryTagSearch(SOLIDIFIED_LIBRARY_SOURCE, event.target.value),
);
els.solidifiedLibraryTagSearchClearButton.addEventListener("click", () =>
  setLibraryTagSearch(SOLIDIFIED_LIBRARY_SOURCE, ""),
);
els.externalLibraryTagSearchInput.addEventListener("input", (event) =>
  setLibraryTagSearch(EXTERNAL_LIBRARY_SOURCE, event.target.value),
);
els.externalLibraryTagSearchClearButton.addEventListener("click", () =>
  setLibraryTagSearch(EXTERNAL_LIBRARY_SOURCE, ""),
);
els.imagebedLibraryTagSearchInput.addEventListener("input", (event) =>
  setLibraryTagSearch(IMAGEBED_LIBRARY_SOURCE, event.target.value),
);
els.imagebedLibraryTagSearchClearButton.addEventListener("click", () =>
  setLibraryTagSearch(IMAGEBED_LIBRARY_SOURCE, ""),
);
els.libraryUploadButton.addEventListener(
  "click",
  openUploadDialogWithProviderCheck,
);
els.tagCategoryButton.addEventListener("click", openTagCategoryDialog);
els.moreConfigButton.addEventListener("click", openConfigDialog);
els.userSearchButton.addEventListener("click", openUserSearchDialog);
els.proactiveEmojiButton.addEventListener("click", openProactiveEmojiDialog);
els.autoCollectionButton.addEventListener("click", openAutoCollectionDialog);
els.memeCombatButton.addEventListener("click", openMemeCombatDialog);
els.externalImportButton.addEventListener(
  "click",
  openExternalImportDialogAndSwitch,
);
els.imagebedImportButton.addEventListener("click", openImagebedImportDialog);
els.externalLibraryImportButton.addEventListener(
  "click",
  openExternalImportDialogAndSwitch,
);
els.imagebedLibraryImportButton.addEventListener(
  "click",
  openImagebedImportDialog,
);
els.pendingSkipButton.addEventListener("click", scrollToSolidifiedLibrary);
els.pendingSelectAllButton.addEventListener("click", toggleAllPendingSelection);
els.pendingAcceptButton.addEventListener("click", acceptSelectedPendingImages);
els.pendingDiscardButton.addEventListener("click", discardSelectedPendingImages);
els.externalImportSelectAllButton.addEventListener(
  "click",
  toggleAllExternalPendingSelection,
);
els.externalImportDeletePendingButton.addEventListener(
  "click",
  deleteSelectedExternalPendingImages,
);
els.externalImportPauseButton.addEventListener("click", startExternalCaptioning);
els.externalImportCancelCaptionButton.addEventListener(
  "click",
  cancelExternalCaptioning,
);
els.imagebedImportSelectAllButton.addEventListener(
  "click",
  toggleAllImagebedPendingSelection,
);
els.imagebedImportDeletePendingButton.addEventListener(
  "click",
  deleteSelectedImagebedPendingImages,
);
els.imagebedImportPauseButton.addEventListener("click", startImagebedCaptioning);
els.imagebedImportCancelCaptionButton.addEventListener(
  "click",
  cancelImagebedCaptioning,
);
els.capacityDeleteOldestButton.addEventListener("click", () =>
  resolveCapacityWarning("delete_oldest"),
);
els.capacityExpandButton.addEventListener("click", () =>
  resolveCapacityWarning("expand"),
);
els.capacityCancelButton.addEventListener("click", () =>
  closeCapacityWarningDialog(true),
);
els.capacityCancelTopButton.addEventListener("click", () =>
  closeCapacityWarningDialog(true),
);
els.externalImportWarningConfirmButton.addEventListener(
  "click",
  confirmExternalImportWarning,
);
els.externalImportWarningCancelButton.addEventListener(
  "click",
  closeExternalImportWarning,
);
els.externalImportWarningCloseButton.addEventListener(
  "click",
  closeExternalImportWarning,
);
els.imagebedImportWarningConfirmButton.addEventListener(
  "click",
  confirmImagebedImportWarning,
);
els.imagebedImportWarningCancelButton.addEventListener(
  "click",
  closeImagebedImportWarning,
);
els.imagebedImportWarningCloseButton.addEventListener(
  "click",
  closeImagebedImportWarning,
);
if (els.captionErrorOkButton) {
  els.captionErrorOkButton.addEventListener("click", closeCaptionErrorDialog);
}
if (els.captionErrorCloseButton) {
  els.captionErrorCloseButton.addEventListener("click", closeCaptionErrorDialog);
}
els.imagebedImportTestButton.addEventListener("click", () =>
  testImagebedImportConnection().catch(() => {}),
);
els.imagebedImportSaveButton.addEventListener("click", () => {
  saveImagebedImportDialog().catch(() => {});
});
els.imagebedImportCancelButton.addEventListener("click", closeImagebedImportDialog);
els.imagebedImportStartButton.addEventListener("click", () => {
  startImagebedImport().catch(() => {});
});
for (const element of [
  els.imagebedAccountIdInput,
  els.imagebedAccessKeyIdInput,
  els.imagebedSecretAccessKeyInput,
  els.imagebedBucketNameInput,
  els.imagebedEndpointUrlInput,
  els.imagebedPrefixInput,
  els.imagebedMaxFileSizeKbInput,
  els.imagebedScheduledEnabledInput,
  els.imagebedScheduledTimeInput,
]) {
  if (!element) {
    continue;
  }
  element.addEventListener("input", markImagebedImportConnectionDirty);
  element.addEventListener("change", markImagebedImportConnectionDirty);
}
els.importButton.addEventListener("click", openImportDialog);
els.exportButton.addEventListener("click", exportConfig);
els.exportManualButton.addEventListener("click", manualExportConfig);
els.exportCancelButton.addEventListener("click", closeExportDialog);
els.exportCloseButton.addEventListener("click", closeExportDialog);
els.exportOverlay.addEventListener("click", (event) => {
  if (event.target === els.exportOverlay) {
    closeExportDialog();
  }
});
els.uploadButton.addEventListener("click", uploadImages);
els.uploadCloseButton.addEventListener("click", closeUploadDialog);
els.captionProviderInput.addEventListener("change", () => {
  renderCaptionProviderWarning(els.captionProviderInput.value);
});
els.warningCaptionProviderInput.addEventListener(
  "change",
  saveProviderWarningSelection,
);
els.providerWarningContinueButton.addEventListener(
  "click",
  continueFromProviderWarning,
);
els.providerWarningCancelButton.addEventListener(
  "click",
  closeProviderWarningDialog,
);
els.providerWarningCloseButton.addEventListener(
  "click",
  closeProviderWarningDialog,
);
els.providerWarningOverlay.addEventListener("click", (event) => {
  if (event.target === els.providerWarningOverlay) {
    closeProviderWarningDialog();
  }
});
els.uploadOverlay.addEventListener("click", (event) => {
  if (event.target === els.uploadOverlay) {
    closeUploadDialog();
  }
});
els.globalTagsInput.addEventListener("input", () => {
  globalTagsDirty = true;
  renderGlobalTagsPreview();
});
els.globalTagsSaveButton.addEventListener("click", saveGlobalTags);
els.editorSaveButton.addEventListener("click", saveEditor);
els.editorCancelButton.addEventListener("click", closeEditor);
els.editorCloseButton.addEventListener("click", closeEditor);
els.editorOverlay.addEventListener("click", (event) => {
  if (event.target === els.editorOverlay) {
    closeEditor();
  }
});
els.tagCategorySaveButton.addEventListener("click", saveTagCategoryDialog);
els.tagCategoryCancelButton.addEventListener("click", closeTagCategoryDialog);
els.tagCategoryOverlay.addEventListener("click", (event) => {
  if (event.target === els.tagCategoryOverlay) {
    closeTagCategoryDialog();
  }
});
els.proactiveEmojiSaveButton.addEventListener("click", saveProactiveEmojiDialog);
els.proactiveEmojiCancelButton.addEventListener("click", closeProactiveEmojiDialog);
els.proactiveEmojiOverlay.addEventListener("click", (event) => {
  if (event.target === els.proactiveEmojiOverlay) {
    closeProactiveEmojiDialog();
  }
});
els.autoCollectionSaveButton.addEventListener("click", saveAutoCollectionDialog);
els.autoCollectionCancelButton.addEventListener(
  "click",
  closeAutoCollectionDialog,
);
els.autoCollectionOverlay.addEventListener("click", (event) => {
  if (event.target === els.autoCollectionOverlay) {
    closeAutoCollectionDialog();
  }
});
els.memeCombatSaveButton.addEventListener("click", saveMemeCombatDialog);
els.memeCombatCancelButton.addEventListener("click", closeMemeCombatDialog);
els.memeCombatOverlay.addEventListener("click", (event) => {
  if (event.target === els.memeCombatOverlay) {
    closeMemeCombatDialog();
  }
});
els.userSearchSaveButton.addEventListener("click", saveUserSearchDialog);
els.userSearchCancelButton.addEventListener("click", closeUserSearchDialog);
els.userSearchOverlay.addEventListener("click", (event) => {
  if (event.target === els.userSearchOverlay) {
    closeUserSearchDialog();
  }
});
els.configSaveButton.addEventListener("click", saveConfigDialog);
els.configCancelButton.addEventListener("click", closeConfigDialog);
els.modelFallbackModeInheritInput?.addEventListener("change", () =>
  setModelFallbackMode("inherit"),
);
els.modelFallbackModeManualInput?.addEventListener("change", () =>
  setModelFallbackMode("manual"),
);
els.modelFallbackAddButton?.addEventListener("click", addModelFallbackProvider);
els.configOverlay.addEventListener("click", (event) => {
  if (event.target === els.configOverlay) {
    closeConfigDialog();
  }
});
els.importConfirmButton.addEventListener("click", importConfig);
els.importCancelButton.addEventListener("click", closeImportDialog);
els.importCloseButton.addEventListener("click", closeImportDialog);
els.importOverlay.addEventListener("click", (event) => {
  if (event.target === els.importOverlay) {
    closeImportDialog();
  }
});
els.externalImportStatButton.addEventListener(
  "click",
  statExternalImportDirectory,
);
els.externalImportStartButton.addEventListener("click", startExternalImport);
els.externalImportCancelButton.addEventListener(
  "click",
  closeExternalImportDialog,
);
els.externalImportCloseButton.addEventListener("click", closeExternalImportDialog);
els.externalImportOverlay.addEventListener("click", (event) => {
  if (event.target === els.externalImportOverlay) {
    closeExternalImportDialog();
  }
});
els.imagebedImportOverlay.addEventListener("click", (event) => {
  if (event.target === els.imagebedImportOverlay) {
    closeImagebedImportDialog();
  }
});
els.solidifiedCapacityOverlay.addEventListener("click", (event) => {
  if (event.target === els.solidifiedCapacityOverlay) {
    closeCapacityWarningDialog(true);
  }
});
els.externalImportWarningOverlay.addEventListener("click", (event) => {
  if (event.target === els.externalImportWarningOverlay) {
    closeExternalImportWarning();
  }
});
els.imagebedImportWarningOverlay.addEventListener("click", (event) => {
  if (event.target === els.imagebedImportWarningOverlay) {
    closeImagebedImportWarning();
  }
});
if (els.captionErrorOverlay) {
  els.captionErrorOverlay.addEventListener("click", (event) => {
    if (event.target === els.captionErrorOverlay) {
      closeCaptionErrorDialog();
    }
  });
}
if (typeof ResizeObserver === "function") {
  const libraryResizeObserver = new ResizeObserver(scheduleLibraryRender);
  libraryResizeObserver.observe(els.libraryList);
  const solidifiedLibraryResizeObserver = new ResizeObserver(() =>
    scheduleLibraryRender(SOLIDIFIED_LIBRARY_SOURCE),
  );
  solidifiedLibraryResizeObserver.observe(els.solidifiedLibraryList);
  const externalLibraryResizeObserver = new ResizeObserver(() =>
    scheduleLibraryRender(EXTERNAL_LIBRARY_SOURCE),
  );
  externalLibraryResizeObserver.observe(els.externalLibraryList);
  const imagebedLibraryResizeObserver = new ResizeObserver(() =>
    scheduleLibraryRender(IMAGEBED_LIBRARY_SOURCE),
  );
  imagebedLibraryResizeObserver.observe(els.imagebedLibraryList);
} else {
  window.addEventListener("resize", () =>
    scheduleLibraryRender(MANUAL_LIBRARY_SOURCE),
  );
  window.addEventListener("resize", () =>
    scheduleLibraryRender(SOLIDIFIED_LIBRARY_SOURCE),
  );
  window.addEventListener("resize", () =>
    scheduleLibraryRender(EXTERNAL_LIBRARY_SOURCE),
  );
  window.addEventListener("resize", () =>
    scheduleLibraryRender(IMAGEBED_LIBRARY_SOURCE),
  );
}

window.addEventListener(
  "scroll",
  () => {
    isPageScrolling = true;
    if (pageScrollIdleTimer) {
      window.clearTimeout(pageScrollIdleTimer);
    }
    pageScrollIdleTimer = window.setTimeout(() => {
      isPageScrolling = false;
      pageScrollIdleTimer = 0;
      flushPendingLibraryRenders();
    }, 220);
  },
  { passive: true },
);

try {
  const api = await ensureBridgeReady();
  document.title = api.t(
    "pages.image-center-page.title",
    "智能图片对话插件 | 图像库处理中心",
  );
} catch (error) {
  setStatus("failed");
  setMessage(`页面初始化失败：${error.message || error}`);
}

updateLibraryScopeVisibility();
await refreshAll();
window.setInterval(refreshAll, 1500);
