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
