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
    skipExisting, setSkipExisting,
    hashChunkSize, setHashChunkSize,
    scanSampleCount, setScanSampleCount,
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
