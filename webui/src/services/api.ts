/**
 * Centralized API Service for Uni-Face Backend Communication.
 */

import axios from 'axios';
import { API_BASE, PLATFORM, ENDPOINTS } from '@/config';
import type { 
  HistoryItem, 
  TargetSet, 
  FaceModelItem, 
  ExtractedFace,
  JobStartSettings,
  ImmichAlbum,
  ImmichTag,
  ImmichPerson,
  ImmichAsset,
  ImmichCategoryType,
  TargetFile,
  JobListResponse
} from '@/types';

const defaultHeaders = {
  'X-Client-Platform': PLATFORM,
};

export const api = {
  // --- Jobs ---
  async getActiveJob(): Promise<{ job_id: string | null }> {
    const res = await fetch(`${API_BASE}${ENDPOINTS.ACTIVE_JOB}`, { headers: defaultHeaders });
    if (!res.ok) return { job_id: null };
    return res.json();
  },

  async getActiveJobsCount(): Promise<number> {
    try {
      const res = await fetch(`${API_BASE}${ENDPOINTS.ACTIVE_JOB_COUNT}`, { headers: defaultHeaders });
      if (!res.ok) return 0;
      const data = await res.json();
      return data.active_count ?? 0;
    } catch {
      return 0;
    }
  },

  async getJobs(status?: string, limit = 50, offset = 0): Promise<JobListResponse> {
    const params = new URLSearchParams();
    if (status && status !== 'all') params.append('status', status);
    params.append('limit', limit.toString());
    params.append('offset', offset.toString());

    const res = await fetch(`${API_BASE}${ENDPOINTS.JOBS}?${params.toString()}`, { headers: defaultHeaders });
    if (!res.ok) {
      throw new Error('Failed to fetch jobs');
    }
    return res.json();
  },

  async deleteJob(jobId: string): Promise<void> {
    const res = await fetch(`${API_BASE}${ENDPOINTS.JOB_DELETE(jobId)}`, {
      method: 'DELETE',
      headers: defaultHeaders,
    });
    if (!res.ok) {
      throw new Error('Failed to delete job');
    }
  },

  async clearCompletedJobs(): Promise<number> {
    const res = await fetch(`${API_BASE}${ENDPOINTS.JOBS_CLEAR}`, {
      method: 'DELETE',
      headers: defaultHeaders,
    });
    if (!res.ok) {
      throw new Error('Failed to clear completed jobs');
    }
    const data = await res.json();
    return data.count ?? 0;
  },

  async rerunJob(jobId: string): Promise<{ new_job_id: string }> {
    const res = await fetch(`${API_BASE}${ENDPOINTS.JOB_RERUN(jobId)}`, {
      method: 'POST',
      headers: defaultHeaders,
    });
    if (!res.ok) {
      const err = await res.json().catch(() => ({ detail: 'Failed to rerun job' }));
      throw new Error(err.detail || 'Failed to rerun job');
    }
    return res.json();
  },

  async retryJob(jobId: string): Promise<{ status: string; job_id: string }> {
    const res = await fetch(`${API_BASE}${ENDPOINTS.JOB_RETRY(jobId)}`, {
      method: 'POST',
      headers: defaultHeaders,
    });
    if (!res.ok) {
      const err = await res.json().catch(() => ({ detail: 'Failed to retry job' }));
      throw new Error(err.detail || 'Failed to retry job');
    }
    return res.json();
  },

  async startJob(payload: {
    source_type: 'image' | 'model';
    source_file_id: string;
    target_file_ids: string[];
  } & JobStartSettings): Promise<{ job_id: string; message: string }> {
    const res = await fetch(`${API_BASE}${ENDPOINTS.JOBS}`, {
      method: 'POST',
      headers: { ...defaultHeaders, 'Content-Type': 'application/json' },
      body: JSON.stringify(payload),
    });
    if (!res.ok) {
      const err = await res.json().catch(() => ({ detail: 'Failed to start job' }));
      throw new Error(err.detail || 'Failed to start job');
    }
    return res.json();
  },

  async cancelJob(jobId: string): Promise<void> {
    await fetch(`${API_BASE}${ENDPOINTS.JOB_CANCEL(jobId)}`, {
      method: 'POST',
      headers: defaultHeaders,
    });
  },

  async updatePreviewSettings(jobId: string, enabled: boolean, resolution: number): Promise<void> {
    await fetch(`${API_BASE}${ENDPOINTS.JOB_PREVIEW(jobId)}`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ enabled, resolution }),
    });
  },

  // --- Uploads ---
  async uploadFile(
    file: File, 
    type: 'source' | 'target', 
    onProgress?: (pct: number) => void
  ): Promise<string> {
    const formData = new FormData();
    formData.append('files', file);
    formData.append('type', type);

    const res = await axios.post(`${API_BASE}${ENDPOINTS.UPLOAD}`, formData, {
      headers: defaultHeaders,
      onUploadProgress: (progressEvent) => {
        if (progressEvent.total) {
          const pct = Math.round((progressEvent.loaded * 100) / progressEvent.total);
          if (onProgress) onProgress(pct);
        }
      },
    });
    return res.data.uploaded[0].file_id;
  },

  async uploadFilesConcurrently(
    files: File[], 
    type: 'source' | 'target', 
    concurrency = 3,
    onProgress?: (completedCount: number, totalCount: number, overallPct: number) => void
  ): Promise<string[]> {
    if (files.length === 0) return [];

    const results: string[] = new Array(files.length);
    const progressMap = new Map<number, number>();
    let completedCount = 0;

    const reportProgress = () => {
      if (!onProgress) return;
      let totalPctSum = 0;
      for (let i = 0; i < files.length; i++) {
        totalPctSum += progressMap.get(i) || 0;
      }
      const overallPct = Math.round(totalPctSum / files.length);
      onProgress(completedCount, files.length, overallPct);
    };

    let nextIndex = 0;
    const worker = async () => {
      while (nextIndex < files.length) {
        const index = nextIndex++;
        const file = files[index];
        const fileId = await api.uploadFile(file, type, (pct) => {
          progressMap.set(index, pct);
          reportProgress();
        });
        results[index] = fileId;
        completedCount++;
        progressMap.set(index, 100);
        reportProgress();
      }
    };

    const workerCount = Math.min(concurrency, files.length);
    const workers = Array.from({ length: workerCount }, () => worker());
    await Promise.all(workers);
    return results;
  },

  async extractFaces(formData: FormData): Promise<{ faces: ExtractedFace[] }> {
    const res = await fetch(`${API_BASE}${ENDPOINTS.EXTRACT_FACES}`, {
      method: 'POST',
      headers: defaultHeaders,
      body: formData,
    });
    if (!res.ok) {
      const text = await res.text();
      throw new Error(text || 'Failed to scan faces');
    }
    return res.json();
  },

  async cleanFacePreview(fileOrId: File | string): Promise<{
    success: boolean;
    has_face?: boolean;
    has_forehead_hair?: boolean;
    original_crop?: string;
    hair_mask?: string | null;
    cleaned_crop?: string;
    error?: string;
  }> {
    const formData = new FormData();
    if (typeof fileOrId === 'string') {
      formData.append('file_id', fileOrId);
    } else {
      formData.append('file', fileOrId);
    }
    const res = await axios.post(`${API_BASE}/api/v1/face/clean-preview`, formData, {
      headers: defaultHeaders,
    });
    return res.data;
  },

  async clearTempWorkspace(): Promise<{ success: boolean; deleted_count: number; reclaimed_bytes: number }> {
    const res = await fetch(`${API_BASE}${ENDPOINTS.CLEAR_TEMP_WORKSPACE}`, {
      method: 'POST',
      headers: defaultHeaders,
    });
    if (!res.ok) {
      throw new Error('Failed to clear temporary workspace');
    }
    return res.json();
  },

  async unloadModels(): Promise<{ status: string; message: string }> {
    const res = await fetch(`${API_BASE}/api/v1/system/unload-models`, {
      method: 'POST',
      headers: defaultHeaders,
    });
    if (!res.ok) {
      throw new Error('Failed to unload models');
    }
    return res.json();
  },

  // --- Face Models ---
  async getFaceModels(): Promise<{ models: FaceModelItem[] }> {
    const res = await fetch(`${API_BASE}${ENDPOINTS.FACE_MODELS}`, { headers: defaultHeaders });
    if (!res.ok) return { models: [] };
    return res.json();
  },

  async deleteFaceModel(name: string): Promise<void> {
    const res = await fetch(`${API_BASE}${ENDPOINTS.FACE_MODELS}/${encodeURIComponent(name)}`, {
      method: 'DELETE',
      headers: defaultHeaders,
    });
    if (!res.ok) throw new Error('Failed to delete face model');
  },

  async buildFaceModel(formData: FormData): Promise<{ model_name: string; faces_extracted: number }> {
    const res = await fetch(`${API_BASE}${ENDPOINTS.FACE_MODELS_BUILD}`, {
      method: 'POST',
      headers: defaultHeaders,
      body: formData,
    });
    const data = await res.json();
    if (!res.ok) {
      throw new Error(data.detail || 'Failed to build face model');
    }
    return data;
  },

  // --- Target Sets ---
  async getTargetSets(): Promise<{ target_sets: TargetSet[] }> {
    const res = await fetch(`${API_BASE}${ENDPOINTS.TARGET_SETS}`, { headers: defaultHeaders });
    if (!res.ok) return { target_sets: [] };
    return res.json();
  },

  async createTargetSet(name: string): Promise<{ name: string; files: any[] }> {
    const fd = new FormData();
    fd.append('name', name);
    const res = await fetch(`${API_BASE}${ENDPOINTS.TARGET_SETS}`, {
      method: 'POST',
      headers: defaultHeaders,
      body: fd,
    });
    if (!res.ok) throw new Error('Failed to create target set');
    return res.json();
  },

  async deleteTargetSet(name: string): Promise<void> {
    const res = await fetch(`${API_BASE}${ENDPOINTS.TARGET_SET_BY_NAME(name)}`, {
      method: 'DELETE',
      headers: defaultHeaders,
    });
    if (!res.ok) throw new Error('Failed to delete target set');
  },

  async deleteTargetSetFiles(name: string, filenames: string[]): Promise<void> {
    const res = await fetch(`${API_BASE}${ENDPOINTS.TARGET_SET_DELETE_FILES(name)}`, {
      method: 'POST',
      headers: { ...defaultHeaders, 'Content-Type': 'application/json' },
      body: JSON.stringify({ filenames }),
    });
    if (!res.ok) throw new Error('Failed to delete target set files');
  },

  async preflightTargetSet(files: { filename: string; hash: string }[]): Promise<{ results: { filename: string; status: 'exists' | 'new'; file_id?: string; url?: string }[] }> {
    const res = await fetch(`${API_BASE}${ENDPOINTS.TARGET_SETS_PREFLIGHT}`, {
      method: 'POST',
      headers: { ...defaultHeaders, 'Content-Type': 'application/json' },
      body: JSON.stringify({ files }),
    });
    if (!res.ok) throw new Error('Target set preflight failed');
    return res.json();
  },

  async linkTargetSetFiles(name: string, files: any[]): Promise<void> {
    const res = await fetch(`${API_BASE}${ENDPOINTS.TARGET_SET_LINK(name)}`, {
      method: 'POST',
      headers: { ...defaultHeaders, 'Content-Type': 'application/json' },
      body: JSON.stringify({ files }),
    });
    if (!res.ok) throw new Error('Failed to link existing files to target set');
  },

  async uploadTargetSetFiles(name: string, formData: FormData): Promise<void> {
    const res = await fetch(`${API_BASE}${ENDPOINTS.TARGET_SET_UPLOAD(name)}`, {
      method: 'POST',
      headers: defaultHeaders,
      body: formData,
    });
    if (!res.ok) throw new Error('Failed to upload target set files');
  },

  // --- History ---
  async getHistory(skip: number = 0, limit: number = 30): Promise<{ history: HistoryItem[]; total: number }> {
    const res = await fetch(`${API_BASE}${ENDPOINTS.HISTORY}?skip=${skip}&limit=${limit}`, {
      headers: defaultHeaders,
    });
    if (!res.ok) return { history: [], total: 0 };
    return res.json();
  },

  async deleteHistory(filenames: string[], deleteAll: boolean = false): Promise<void> {
    const res = await fetch(`${API_BASE}${ENDPOINTS.HISTORY}`, {
      method: 'DELETE',
      headers: { ...defaultHeaders, 'Content-Type': 'application/json' },
      body: JSON.stringify({ filenames, delete_all: deleteAll }),
    });
    if (!res.ok) throw new Error('Failed to delete history items');
  },

  async downloadHistoryZip(filenames: string[]): Promise<Blob> {
    const res = await fetch(`${API_BASE}${ENDPOINTS.HISTORY_DOWNLOAD}`, {
      method: 'POST',
      headers: { ...defaultHeaders, 'Content-Type': 'application/json' },
      body: JSON.stringify({ filenames }),
    });
    if (!res.ok) throw new Error('Failed to download files');
    return res.blob();
  },

  // --- Immich ---
  async testImmich(url: string, apiKey: string): Promise<{ success: boolean; message: string }> {
    const res = await fetch(`${API_BASE}${ENDPOINTS.IMMICH_TEST}`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ url, api_key: apiKey }),
    });
    return res.json();
  },

  async getImmichAlbums(url: string, apiKey: string): Promise<{ success: boolean; albums: ImmichAlbum[] }> {
    const u = encodeURIComponent(url);
    const k = encodeURIComponent(apiKey);
    const res = await fetch(`${API_BASE}${ENDPOINTS.IMMICH_ALBUMS}?url=${u}&api_key=${k}`);
    return res.json();
  },

  async getImmichTags(url: string, apiKey: string): Promise<{ success: boolean; tags: ImmichTag[] }> {
    const u = encodeURIComponent(url);
    const k = encodeURIComponent(apiKey);
    const res = await fetch(`${API_BASE}${ENDPOINTS.IMMICH_TAGS}?url=${u}&api_key=${k}`);
    return res.json();
  },

  async getImmichPeople(url: string, apiKey: string): Promise<{ success: boolean; people: ImmichPerson[] }> {
    const u = encodeURIComponent(url);
    const k = encodeURIComponent(apiKey);
    const res = await fetch(`${API_BASE}${ENDPOINTS.IMMICH_PEOPLE}?url=${u}&api_key=${k}`);
    return res.json();
  },

  async getImmichCategoryAssets(
    url: string, 
    apiKey: string, 
    categoryType: ImmichCategoryType, 
    categoryId: string
  ): Promise<{ success: boolean; assets: ImmichAsset[] }> {
    const u = encodeURIComponent(url);
    const k = encodeURIComponent(apiKey);
    const ct = encodeURIComponent(categoryType);
    const cid = encodeURIComponent(categoryId);
    const res = await fetch(`${API_BASE}${ENDPOINTS.IMMICH_ASSETS}?url=${u}&api_key=${k}&category_type=${ct}&category_id=${cid}`);
    return res.json();
  },

  async importImmichTargets(
    url: string, 
    apiKey: string, 
    assetIds: string[],
    localPath?: string
  ): Promise<{ 
    success: boolean; 
    imported: TargetFile[]; 
    failed: any[]; 
    message: string;
    import_method?: 'hardlink' | 'download' | 'mixed';
    hardlink_count?: number;
    download_count?: number;
    skipped_count?: number;
  }> {
    const res = await fetch(`${API_BASE}${ENDPOINTS.IMMICH_IMPORT}`, {
      method: 'POST',
      headers: { ...defaultHeaders, 'Content-Type': 'application/json' },
      body: JSON.stringify({ url, api_key: apiKey, asset_ids: assetIds, local_path: localPath }),
    });
    if (!res.ok) throw new Error('Failed to import Immich targets');
    return res.json();
  },

  async exportToImmich(payload: {
    url: string;
    api_key: string;
    new_album: boolean;
    album: string;
    tags: string[];
    filenames: string[];
  }): Promise<{ success: boolean; message?: string }> {
    const res = await fetch(`${API_BASE}${ENDPOINTS.IMMICH_EXPORT}`, {
      method: 'POST',
      headers: { ...defaultHeaders, 'Content-Type': 'application/json' },
      body: JSON.stringify(payload),
    });
    return res.json();
  },
};
