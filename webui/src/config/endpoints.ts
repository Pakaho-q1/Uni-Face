/**
 * Single Source of Truth (SSOT) for all Uni-Face API & WebSocket Endpoints.
 */

export const ENDPOINTS = {
  // Jobs
  JOBS: '/api/v1/jobs',
  ACTIVE_JOB: '/api/v1/jobs/active',
  ACTIVE_JOB_COUNT: '/api/v1/jobs/active-count',
  JOB_WS: (jobId: string) => `/api/v1/ws/jobs/${jobId}`,
  JOB_CANCEL: (jobId: string) => `/api/v1/jobs/${jobId}/cancel`,
  JOB_DELETE: (jobId: string) => `/api/v1/jobs/${jobId}`,
  JOB_RERUN: (jobId: string) => `/api/v1/jobs/${jobId}/rerun`,
  JOB_RETRY: (jobId: string) => `/api/v1/jobs/${jobId}/retry`,
  JOBS_CLEAR: '/api/v1/jobs',
  JOB_PREVIEW: (jobId: string) => `/api/v1/jobs/${jobId}/preview`,

  // Upload & Workspace
  UPLOAD: '/api/v1/upload',
  UPLOAD_FILE: (filePath: string) => `/api/v1/uploads/${filePath}`,
  EXTRACT_FACES: '/api/v1/extract-faces',
  CLEAR_TEMP_WORKSPACE: '/api/v1/workspace/clear-temp',

  // Face Models (.safetensors)
  FACE_MODELS: '/api/v1/face-models',
  FACE_MODELS_BUILD: '/api/v1/face-models/build',

  // Target Sets (Galleries)
  TARGET_SETS: '/api/v1/target-sets',
  TARGET_SETS_PREFLIGHT: '/api/v1/target-sets/preflight',
  TARGET_SET_BY_NAME: (name: string) => `/api/v1/target-sets/${encodeURIComponent(name)}`,
  TARGET_SET_LINK: (name: string) => `/api/v1/target-sets/${encodeURIComponent(name)}/link`,
  TARGET_SET_UPLOAD: (name: string) => `/api/v1/target-sets/${encodeURIComponent(name)}/upload`,
  TARGET_SET_DELETE_FILES: (name: string) => `/api/v1/target-sets/${encodeURIComponent(name)}/delete-files`,

  // Output History
  HISTORY: '/api/v1/history',
  HISTORY_DOWNLOAD: '/api/v1/history/download',
  HISTORY_FILE: (filename: string, platform: string) => `/api/v1/history/${encodeURIComponent(filename)}?platform=${encodeURIComponent(platform)}`,

  // Immich Integration
  IMMICH_TEST: '/api/v1/immich/test',
  IMMICH_ALBUMS: '/api/v1/immich/albums',
  IMMICH_TAGS: '/api/v1/immich/tags',
  IMMICH_PEOPLE: '/api/v1/immich/people',
  IMMICH_ASSETS: '/api/v1/immich/assets',
  IMMICH_IMPORT: '/api/v1/immich/import',
  IMMICH_EXPORT: '/api/v1/immich/export',
  IMMICH_PERSON_THUMB: (id: string, url: string, key: string) => `/api/v1/immich/thumbnail/person/${encodeURIComponent(id)}?url=${encodeURIComponent(url)}&api_key=${encodeURIComponent(key)}`,
  IMMICH_ASSET_THUMB: (id: string, url: string, key: string) => `/api/v1/immich/thumbnail/asset/${encodeURIComponent(id)}?url=${encodeURIComponent(url)}&api_key=${encodeURIComponent(key)}`,
} as const;
