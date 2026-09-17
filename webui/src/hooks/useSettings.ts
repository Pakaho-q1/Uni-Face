/**
 * Custom hook for global persistent settings with localStorage sticky state.
 */

import { useStickyState } from '@/hooks/useStickyState';
import { DEFAULT_SETTINGS } from '@/config';
import type { SettingsState } from '@/types';

export function useSettings(): SettingsState {
  const [executionProvider, setExecutionProvider] = useStickyState(
    DEFAULT_SETTINGS.executionProvider, 
    'setting_executionProvider'
  );
  const [executionThreadCount, setExecutionThreadCount] = useStickyState(
    [DEFAULT_SETTINGS.executionThreadCount], 
    'setting_executionThreadCount'
  );
  const [swapModel, setSwapModel] = useStickyState(
    DEFAULT_SETTINGS.swapModel, 
    'setting_swapModel'
  );
  const [swapWeight, setSwapWeight] = useStickyState(
    [DEFAULT_SETTINGS.swapWeight], 
    'setting_swapWeight'
  );
  const [restoreModel, setRestoreModel] = useStickyState(
    DEFAULT_SETTINGS.restoreModel, 
    'setting_restoreModel'
  );
  const [restoreWeight, setRestoreWeight] = useStickyState(
    [DEFAULT_SETTINGS.restoreWeight], 
    'setting_restoreWeight'
  );
  const [restoreBlend, setRestoreBlend] = useStickyState(
    [DEFAULT_SETTINGS.restoreBlend], 
    'setting_restoreBlend'
  );
  const [faceRestore, setFaceRestore] = useStickyState(
    DEFAULT_SETTINGS.faceRestore, 
    'setting_faceRestore'
  );
  const [colorMatch, setColorMatch] = useStickyState(
    DEFAULT_SETTINGS.colorMatch, 
    'setting_colorMatch'
  );
  const [similarity, setSimilarity] = useStickyState(
    DEFAULT_SETTINGS.similarity, 
    'setting_similarity'
  );
  const [previewFreq, setPreviewFreq] = useStickyState(
    [DEFAULT_SETTINGS.previewFreq], 
    'setting_previewFreq'
  );
  const [previewRes, setPreviewRes] = useStickyState(
    DEFAULT_SETTINGS.previewRes, 
    'setting_previewRes'
  );
  const [galleryRes, setGalleryRes] = useStickyState(
    DEFAULT_SETTINGS.galleryRes, 
    'setting_galleryRes'
  );
  const [maskTypes, setMaskTypes] = useStickyState<string[]>(
    DEFAULT_SETTINGS.maskTypes, 
    'setting_maskTypes'
  );
  const [maskRegions, setMaskRegions] = useStickyState<string[]>(
    DEFAULT_SETTINGS.maskRegions, 
    'setting_maskRegions'
  );
  const [occlusionModel, setOcclusionModel] = useStickyState(
    DEFAULT_SETTINGS.occlusionModel, 
    'setting_occlusionModel'
  );
  const [genderFilter, setGenderFilter] = useStickyState(
    DEFAULT_SETTINGS.genderFilter,
    'setting_genderFilter'
  );
  const [targetGender, setTargetGender] = useStickyState(
    DEFAULT_SETTINGS.targetGender,
    'setting_targetGender'
  );
  const [faceOrder, setFaceOrder] = useStickyState(
    DEFAULT_SETTINGS.faceOrder,
    'setting_faceOrder'
  );
  const [skipExisting, setSkipExisting] = useStickyState(
    DEFAULT_SETTINGS.skipExisting, 
    'setting_skipExisting'
  );
  const [hashChunkSize, setHashChunkSize] = useStickyState(
    [DEFAULT_SETTINGS.hashChunkSize], 
    'setting_hashChunkSize'
  );
  const [scanSampleCount, setScanSampleCount] = useStickyState(
    [DEFAULT_SETTINGS.scanSampleCount], 
    'setting_scanSampleCount'
  );
  const [faceDetectorScore, setFaceDetectorScore] = useStickyState(
    [DEFAULT_SETTINGS.faceDetectorScore], 
    'setting_faceDetectorScore'
  );
  const [faceLandmarkScore, setFaceLandmarkScore] = useStickyState(
    [DEFAULT_SETTINGS.faceLandmarkScore], 
    'setting_faceLandmarkScore'
  );

  // Dual-Stage Swap & Staged Restore Settings
  const [stage1Restore, setStage1Restore] = useStickyState(
    DEFAULT_SETTINGS.stage1Restore,
    'setting_stage1Restore'
  );
  const [dualSwap, setDualSwap] = useStickyState(
    DEFAULT_SETTINGS.dualSwap,
    'setting_dualSwap'
  );
  const [swapModel2, setSwapModel2] = useStickyState(
    DEFAULT_SETTINGS.swapModel2,
    'setting_swapModel2'
  );
  const [swapWeight2, setSwapWeight2] = useStickyState(
    [DEFAULT_SETTINGS.swapWeight2],
    'setting_swapWeight2'
  );
  const [stage2Restore, setStage2Restore] = useStickyState(
    DEFAULT_SETTINGS.stage2Restore,
    'setting_stage2Restore'
  );
  const [restoreModel2, setRestoreModel2] = useStickyState(
    DEFAULT_SETTINGS.restoreModel2,
    'setting_restoreModel2'
  );
  const [restoreWeight2, setRestoreWeight2] = useStickyState(
    [DEFAULT_SETTINGS.restoreWeight2],
    'setting_restoreWeight2'
  );
  const [restoreBlend2, setRestoreBlend2] = useStickyState(
    [DEFAULT_SETTINGS.restoreBlend2],
    'setting_restoreBlend2'
  );

  // Clean Source & Mask Boundary Settings
  const [enableFaceCleanTools, setEnableFaceCleanTools] = useStickyState<boolean>(
    DEFAULT_SETTINGS.enableFaceCleanTools,
    'setting_enableFaceCleanTools'
  );
  const [cleanSourceFace, setCleanSourceFace] = useStickyState<boolean>(
    DEFAULT_SETTINGS.cleanSourceFace,
    'setting_cleanSourceFace'
  );
  const [maskPadding, setMaskPadding] = useStickyState<number[]>(
    DEFAULT_SETTINGS.maskPadding,
    'setting_maskPadding'
  );
  const [maskBlur, setMaskBlur] = useStickyState<number[]>(
    [DEFAULT_SETTINGS.maskBlur],
    'setting_maskBlur'
  );

  // ReActor Logics
  const [faceBoost, setFaceBoost] = useStickyState<string>(
    DEFAULT_SETTINGS.faceBoost,
    'setting_faceBoost'
  );
  const [restoreSourceFace, setRestoreSourceFace] = useStickyState<boolean>(
    DEFAULT_SETTINGS.restoreSourceFace,
    'setting_restoreSourceFace'
  );
  const [restoreSourceFaceModel, setRestoreSourceFaceModel] = useStickyState<string>(
    DEFAULT_SETTINGS.restoreSourceFaceModel,
    'setting_restoreSourceFaceModel'
  );
  const [restoreSourceFaceWeight, setRestoreSourceFaceWeight] = useStickyState<number[]>(
    [DEFAULT_SETTINGS.restoreSourceFaceWeight],
    'setting_restoreSourceFaceWeight'
  );
  const [targetHairProtect, setTargetHairProtect] = useStickyState<boolean>(
    DEFAULT_SETTINGS.targetHairProtect,
    'setting_targetHairProtect'
  );

  // Immich Settings
  const [immichUrl, setImmichUrl] = useStickyState(
    DEFAULT_SETTINGS.immichUrl, 
    'setting_immichUrl'
  );
  const [immichApiKey, setImmichApiKey] = useStickyState(
    DEFAULT_SETTINGS.immichApiKey, 
    'setting_immichApiKey'
  );
  const [immichLocalPath, setImmichLocalPath] = useStickyState(
    DEFAULT_SETTINGS.immichLocalPath, 
    'setting_immichLocalPath'
  );
  const [immichAutoSave, setImmichAutoSave] = useStickyState(
    DEFAULT_SETTINGS.immichAutoSave, 
    'setting_immichAutoSave'
  );
  const [immichNewAlbum, setImmichNewAlbum] = useStickyState(
    DEFAULT_SETTINGS.immichNewAlbum, 
    'setting_immichNewAlbum'
  );
  const [immichAlbum, setImmichAlbum] = useStickyState(
    DEFAULT_SETTINGS.immichAlbum, 
    'setting_immichAlbum'
  );
  const [immichTags, setImmichTags] = useStickyState<string[]>(
    DEFAULT_SETTINGS.immichTags, 
    'setting_immichTags'
  );
  const [immichDeleteLocal, setImmichDeleteLocal] = useStickyState(
    DEFAULT_SETTINGS.immichDeleteLocal, 
    'setting_immichDeleteLocal'
  );

  return {
    executionProvider, setExecutionProvider,
    executionThreadCount, setExecutionThreadCount,
    swapModel, setSwapModel,
    swapWeight, setSwapWeight,
    restoreModel, setRestoreModel,
    restoreWeight, setRestoreWeight,
    restoreBlend, setRestoreBlend,
    faceRestore, setFaceRestore,
    colorMatch, setColorMatch,
    similarity, setSimilarity,
    previewFreq, setPreviewFreq,
    previewRes, setPreviewRes,
    galleryRes, setGalleryRes,
    maskTypes, setMaskTypes,
    maskRegions, setMaskRegions,
    occlusionModel, setOcclusionModel,
    genderFilter, setGenderFilter,
    targetGender, setTargetGender,
    faceOrder, setFaceOrder,
    skipExisting, setSkipExisting,
    hashChunkSize, setHashChunkSize,
    scanSampleCount, setScanSampleCount,
    faceDetectorScore, setFaceDetectorScore,
    faceLandmarkScore, setFaceLandmarkScore,
    stage1Restore, setStage1Restore,
    dualSwap, setDualSwap,
    swapModel2, setSwapModel2,
    swapWeight2, setSwapWeight2,
    stage2Restore, setStage2Restore,
    restoreModel2, setRestoreModel2,
    restoreWeight2, setRestoreWeight2,
    restoreBlend2, setRestoreBlend2,
    enableFaceCleanTools, setEnableFaceCleanTools,
    cleanSourceFace, setCleanSourceFace,
    maskPadding, setMaskPadding,
    maskBlur, setMaskBlur,
    faceBoost, setFaceBoost,
    restoreSourceFace, setRestoreSourceFace,
    restoreSourceFaceModel, setRestoreSourceFaceModel,
    restoreSourceFaceWeight, setRestoreSourceFaceWeight,
    targetHairProtect, setTargetHairProtect,
    immichUrl, setImmichUrl,
    immichApiKey, setImmichApiKey,
    immichLocalPath, setImmichLocalPath,
    immichAutoSave, setImmichAutoSave,
    immichNewAlbum, setImmichNewAlbum,
    immichAlbum, setImmichAlbum,
    immichTags, setImmichTags,
    immichDeleteLocal, setImmichDeleteLocal,
  };
}
