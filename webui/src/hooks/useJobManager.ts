/**
 * Custom hook for Job lifecycle management (WebSocket stream, start, cancel, preview settings).
 */

import { useState, useRef, useCallback } from 'react';
import { toast } from 'sonner';
import { API_BASE, WS_BASE, PLATFORM, ENDPOINTS } from '@/config';
import { api } from '@/services/api';
import type { JobState, JobStartSettings } from '@/types';

export function useJobManager(onJobComplete?: () => void) {
  const [state, setState] = useState<JobState>({
    currentJobId: null,
    running: false,
    progress: 0,
    uploading: false,
    uploadProgress: 0,
    framesDone: 0,
    totalFrames: 0,
    targetPreview: '',
    targetType: 'image',
  });
  const wsRef = useRef<WebSocket | null>(null);
  const lastPreviewTimeRef = useRef<number>(0);

  const connectWebSocket = useCallback((jobId: string) => {
    if (wsRef.current) wsRef.current.close();
    
    const wsUrl = `${WS_BASE}${ENDPOINTS.JOB_WS(jobId)}`;
    const ws = new WebSocket(wsUrl);
    wsRef.current = ws;

    ws.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data);
        if (data.error) {
          toast.error("Job Error", { description: data.error });
          setState(prev => ({ ...prev, running: false }));
          return;
        }

        const isFinished = data.status === "completed" || data.status === "failed" || data.status === "cancelled";
        const now = performance.now();
        const shouldUpdatePreview = !data.preview_image || (now - lastPreviewTimeRef.current >= 66); // ~15 FPS preview throttle

        if (isFinished) {
          let finalPreview = '';
          if (data.status === "completed" && data.output_path) {
            const filename = data.output_path.split(/[/\\]/).pop();
            finalPreview = `${API_BASE}${ENDPOINTS.HISTORY_FILE(filename, PLATFORM)}`;
            toast.success("Job Completed Successfully");
          } else if (data.status === "failed") {
            toast.error("Job Failed", { description: data.error || "Unknown error" });
          } else if (data.status === "cancelled") {
            toast.info("Job Cancelled");
          }
          
          setState(prev => ({ 
            ...prev, 
            running: false, 
            progress: data.progress ?? prev.progress,
            framesDone: data.frames_done ?? prev.framesDone,
            totalFrames: data.total_frames ?? prev.totalFrames,
            targetPreview: finalPreview || prev.targetPreview 
          }));
          if (onJobComplete) onJobComplete();
          ws.close();
        } else {
          if (data.preview_image && shouldUpdatePreview) {
            lastPreviewTimeRef.current = now;
          }
          setState(prev => ({
            ...prev,
            progress: data.progress ?? prev.progress,
            framesDone: data.frames_done ?? prev.framesDone,
            totalFrames: data.total_frames ?? prev.totalFrames,
            ...(data.preview_image && shouldUpdatePreview ? { 
              targetPreview: data.preview_image,
              targetType: 'image'
            } : {})
          }));
        }
      } catch (e) {
        console.error("WS parse error", e);
      }
    };
    
    ws.onerror = (e) => {
      console.error("WebSocket error", e);
    };
  }, [onJobComplete]);

  const checkActiveJob = useCallback(async () => {
    try {
      const data = await api.getActiveJob();
      if (data.job_id) {
        setState(prev => ({ ...prev, currentJobId: data.job_id, running: true }));
        connectWebSocket(data.job_id);
      }
    } catch (e) {
      console.error("Failed to fetch active job", e);
    }
  }, [connectWebSocket]);

  const cancelJob = async () => {
    if (state.running && state.currentJobId) {
      setState(prev => ({ ...prev, running: false, progress: 0, uploading: false }));
      if (wsRef.current) wsRef.current.close();
      await api.cancelJob(state.currentJobId);
      toast.info("Job cancelled");
    } else if (state.running) {
      setState(prev => ({ ...prev, running: false, progress: 0, uploading: false }));
    }
  };

  const startJob = async (
    sourceType: "image" | "model",
    sourceFileOrModelId: File | string,
    targetType: "upload" | "set",
    targetFilesOrIds: (File | string)[],
    settings: JobStartSettings
  ) => {
    setState(prev => ({ ...prev, running: true, uploading: true, uploadProgress: 0, progress: 0 }));
    try {
      let sourceId = typeof sourceFileOrModelId === 'string' ? sourceFileOrModelId : '';
      
      const uploadTargets = targetType === "upload" ? (targetFilesOrIds as File[]) : [];
      const setTargets = targetType === "set" ? (targetFilesOrIds as string[]) : [];
      const hasSourceFile = sourceType === "image" && sourceFileOrModelId instanceof File;
      const totalFiles = uploadTargets.length + (hasSourceFile ? 1 : 0);

      if (hasSourceFile) {
        sourceId = await api.uploadFile(sourceFileOrModelId, "source", (pct) => {
          if (totalFiles <= 1) {
            setState(prev => ({ ...prev, uploadProgress: pct }));
          } else {
            const overall = Math.round(pct / totalFiles);
            setState(prev => ({ ...prev, uploadProgress: overall }));
          }
        });
      }

      let targetIds: string[] = [];
      if (targetType === "upload") {
        const sourceWeight = hasSourceFile ? (1 / totalFiles) : 0;
        const targetWeight = totalFiles > 0 ? (uploadTargets.length / totalFiles) : 1;
        targetIds = await api.uploadFilesConcurrently(
          uploadTargets, 
          "target", 
          3, 
          (_completed, _total, overallPct) => {
            const currentTotal = Math.round((sourceWeight * 100) + (targetWeight * overallPct));
            setState(prev => ({ ...prev, uploadProgress: Math.min(100, currentTotal) }));
          }
        );
      } else {
        targetIds = setTargets;
      }

      setState(prev => ({ ...prev, uploading: false }));

      const jobData = await api.startJob({
        source_type: sourceType,
        source_file_id: sourceId,
        target_file_ids: targetIds,
        ...settings,
      });

      setState(prev => ({ ...prev, currentJobId: jobData.job_id, uploading: false }));
      toast.success("Job started");
      connectWebSocket(jobData.job_id);
    } catch (err: any) {
      toast.error("Error starting job", { description: err.message || String(err) });
      setState(prev => ({ ...prev, running: false, uploading: false, uploadProgress: 0 }));
    }
  };

  const updatePreviewSettings = useCallback(async (enabled: boolean, resolution: number) => {
    if (!state.currentJobId) return;
    try {
      await api.updatePreviewSettings(state.currentJobId, enabled, resolution);
    } catch (err) {
      console.error("Failed to update preview settings:", err);
    }
  }, [state.currentJobId]);

  return {
    jobState: state,
    setJobState: setState,
    checkActiveJob,
    startJob,
    cancelJob,
    updatePreviewSettings
  };
}
