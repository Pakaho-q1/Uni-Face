/**
 * Centralized Configuration (SSOT) for Uni-Face WebUI
 */

export * from './endpoints';
export * from './models';

export const PLATFORM = 'webui_react';

export const API_BASE = import.meta.env.DEV 
  ? `http://${window.location.hostname}:8000` 
  : window.location.origin;

export const WS_BASE = API_BASE.replace(/^http/, 'ws');

export const DEFAULT_SETTINGS = {
  executionProvider: 'cpu',
  executionThreadCount: 4,
  swapModel: 'inswapper_128',
  swapWeight: 65,
  restoreModel: 'gfpgan_1.4',
  restoreWeight: 100,
  restoreBlend: 100,
  faceRestore: true,
  colorMatch: false,
  similarity: false,
  previewFreq: 15,
  previewRes: '320',
  galleryRes: '384',
  maskTypes: ['box'],
  maskRegions: ['skin', 'l_brow', 'r_brow', 'l_eye', 'r_eye', 'nose', 'mouth', 'u_lip', 'l_lip'],
  occlusionModel: 'xseg_1',
  genderFilter: false,
  targetGender: 'all',
  faceOrder: 'largest',
  skipExisting: true,
  hashChunkSize: 100,
  scanSampleCount: 5,
  referenceThreshold: 0.6,
  
  // Immich
  immichUrl: '',
  immichApiKey: '',
  immichLocalPath: '',
  immichAutoSave: false,
  immichNewAlbum: false,
  immichAlbum: '',
  immichTags: [] as string[],
  immichDeleteLocal: false,
};
