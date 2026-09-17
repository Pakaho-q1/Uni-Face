/**
 * Centralized TypeScript Interfaces and Type Definitions (SSOT)
 */

export interface JobState {
  currentJobId: string | null;
  running: boolean;
  progress: number;
  uploading: boolean;
  uploadProgress: number;
  framesDone: number;
  totalFrames: number;
  targetPreview: string;
  targetType?: 'video' | 'image';
}

export interface JobStartSettings {
  preview_frequency: number;
  preview_enabled: boolean;
  preview_resolution: number;
  processors: string[];
  swap_model: string;
  swap_weight: number;
  restore_model: string;
  restore_weight: number;
  restore_blend: number;
  mask_types: string[];
  mask_regions: string[];
  occlusion_model?: string;
  target_gender?: string;
  face_order?: string;
  similarity: boolean;
  providers: string[];
  execution_thread_count: number;
  skip_existing: boolean;
  reference_face_ids: string[];
  reference_threshold: number;
  face_detector_score?: number;
  face_landmark_score?: number;
  stage1_restore?: boolean;
  dual_swap?: boolean;
  swap_model_2?: string;
  swap_weight_2?: number;
  stage2_restore?: boolean;
  restore_model_2?: string;
  restore_weight_2?: number;
  restore_blend_2?: number;
  
  // Clean Source & Mask Boundary Settings
  clean_source_face?: boolean;
  mask_padding?: number[];
  mask_blur?: number;
  
  // Immich settings
  immich_url?: string;
  immich_api_key?: string;
  immich_auto_save?: boolean;
  immich_new_album?: boolean;
  immich_album?: string;
  immich_tags?: string[];
  immich_delete_local?: boolean;
}

export interface HistoryItem {
  filename: string;
  url: string;
  type: 'image' | 'video' | string;
  created_at: number;
  size?: number;
}

export interface ExtractedFace {
  id: string;
  url: string;
}

export interface TargetFile {
  filename: string;
  file_id: string;
  url: string;
  duration?: number;
}

export interface TargetSet {
  name: string;
  files: TargetFile[];
}

export interface FaceModelItem {
  name: string;
  path?: string;
  faces_count?: number;
}

export interface ImmichAlbum {
  id: string;
  name?: string;
  albumName?: string;
  assetCount?: number;
}

export interface ImmichTag {
  id: string;
  name: string;
}

export interface ImmichPerson {
  id: string;
  name: string;
  thumbnailPath?: string;
}

export interface ImmichAsset {
  id: string;
  filename: string;
  type: 'image' | 'video';
  duration?: number;
  originalPath?: string;
  thumbnailUrl: string;
}

export type ImmichCategoryType = 'people' | 'albums' | 'tags';

export interface SettingsState {
  executionProvider: string;
  setExecutionProvider: (v: string) => void;
  executionThreadCount: number[];
  setExecutionThreadCount: (v: number[]) => void;
  swapModel: string;
  setSwapModel: (v: string) => void;
  swapWeight: number[];
  setSwapWeight: (v: number[]) => void;
  restoreModel: string;
  setRestoreModel: (v: string) => void;
  restoreWeight: number[];
  setRestoreWeight: (v: number[]) => void;
  restoreBlend: number[];
  setRestoreBlend: (v: number[]) => void;
  faceRestore: boolean;
  setFaceRestore: (v: boolean) => void;
  colorMatch: boolean;
  setColorMatch: (v: boolean) => void;
  similarity: boolean;
  setSimilarity: (v: boolean) => void;
  previewFreq: number[];
  setPreviewFreq: (v: number[]) => void;
  previewRes: string;
  setPreviewRes: (v: string) => void;
  galleryRes: string;
  setGalleryRes: (v: string) => void;
  maskTypes: string[];
  setMaskTypes: (v: string[]) => void;
  maskRegions: string[];
  setMaskRegions: (v: string[]) => void;
  occlusionModel: string;
  setOcclusionModel: (v: string) => void;
  genderFilter: boolean;
  setGenderFilter: (v: boolean) => void;
  targetGender: string;
  setTargetGender: (v: string) => void;
  faceOrder: string;
  setFaceOrder: (v: string) => void;
  skipExisting: boolean;
  setSkipExisting: (v: boolean) => void;
  hashChunkSize: number[];
  setHashChunkSize: (v: number[]) => void;
  scanSampleCount: number[];
  setScanSampleCount: (v: number[]) => void;
  faceDetectorScore: number[];
  setFaceDetectorScore: (v: number[]) => void;
  faceLandmarkScore: number[];
  setFaceLandmarkScore: (v: number[]) => void;
  
  // Dual-Stage Swap & Staged Restore Settings
  stage1Restore: boolean;
  setStage1Restore: (v: boolean) => void;
  dualSwap: boolean;
  setDualSwap: (v: boolean) => void;
  swapModel2: string;
  setSwapModel2: (v: string) => void;
  swapWeight2: number[];
  setSwapWeight2: (v: number[]) => void;
  stage2Restore: boolean;
  setStage2Restore: (v: boolean) => void;
  restoreModel2: string;
  setRestoreModel2: (v: string) => void;
  restoreWeight2: number[];
  setRestoreWeight2: (v: number[]) => void;
  restoreBlend2: number[];
  setRestoreBlend2: (v: number[]) => void;
  
  // Clean Source & Mask Boundary Settings
  enableFaceCleanTools: boolean;
  setEnableFaceCleanTools: (v: boolean) => void;
  cleanSourceFace: boolean;
  setCleanSourceFace: (v: boolean) => void;
  maskPadding: number[];
  setMaskPadding: (v: number[]) => void;
  maskBlur: number[];
  setMaskBlur: (v: number[]) => void;
  
  // ReActor Logics
  faceBoost: string;
  setFaceBoost: (v: string) => void;
  restoreSourceFace: boolean;
  setRestoreSourceFace: (v: boolean) => void;
  restoreSourceFaceModel: string;
  setRestoreSourceFaceModel: (v: string) => void;
  restoreSourceFaceWeight: number[];
  setRestoreSourceFaceWeight: (v: number[]) => void;
  targetHairProtect: boolean;
  setTargetHairProtect: (v: boolean) => void;
  
  // Immich Settings
  immichUrl: string;
  setImmichUrl: (v: string) => void;
  immichApiKey: string;
  setImmichApiKey: (v: string) => void;
  immichLocalPath: string;
  setImmichLocalPath: (v: string) => void;
  immichAutoSave: boolean;
  setImmichAutoSave: (v: boolean) => void;
  immichNewAlbum: boolean;
  setImmichNewAlbum: (v: boolean) => void;
  immichAlbum: string;
  setImmichAlbum: (v: string) => void;
  immichTags: string[];
  setImmichTags: (v: string[]) => void;
  immichDeleteLocal: boolean;
  setImmichDeleteLocal: (v: boolean) => void;
}

export interface JobRecord {
  id: string;
  platform: string;
  status: 'pending' | 'processing' | 'completed' | 'failed' | 'cancelled';
  source_type: 'image' | 'model';
  source_file_id?: string;
  source_name?: string;
  target_type?: string;
  target_count: number;
  target_summary?: string;
  progress: number;
  frames_done: number;
  total_frames: number;
  output_path?: string;
  error?: string;
  config_json?: string;
  created_at: string;
  updated_at: string;
}

export interface JobListResponse {
  jobs: JobRecord[];
  total: number;
  active_count: number;
}

