import { useState, useCallback, useRef } from 'react';

export type JobState = {
  running: boolean;
  uploading: boolean;
  progress: number;
  targetPreview: string;
  targetType: 'video' | 'image';
  currentJobId: string | null;
}

export function useJobManager(apiBase: string, platform: string, onJobComplete: () => void) {
  const [state, setState] = useState<JobState>({
    running: false,
    uploading: false,
    progress: 0,
    targetPreview: '',
    targetType: 'video',
    currentJobId: null
  });

  const wsRef = useRef<WebSocket | null>(null);

  const connectWebSocket = useCallback((jobId: string) => {
    const wsUrl = `ws://${window.location.hostname}:8000/api/v1/ws/jobs/${jobId}`;
    const websocket = new WebSocket(wsUrl);
    
    websocket.onmessage = (event) => {
      const data = JSON.parse(event.data);
      
      setState(prev => ({
        ...prev,
        progress: data.progress || 0,
        ...(data.preview_image ? { 
          targetType: 'image', 
          targetPreview: data.preview_image 
        } : {})
      }));
      
      if (data.status === 'completed') {
        let finalPreview = '';
        if (data.output_path) {
          const filename = data.output_path.split(/[\\/]/).pop();
          finalPreview = `${apiBase}/api/v1/history/${filename}?platform=${platform}`;
        }
        setState(prev => ({ ...prev, running: false, targetPreview: finalPreview || prev.targetPreview }));
        onJobComplete();
        websocket.close();
      } else if (data.status === 'failed') {
        setState(prev => ({ ...prev, running: false }));
        console.error("Processing Failed: " + data.error);
        websocket.close();
      }
    };
    
    wsRef.current = websocket;
  }, [apiBase, platform, onJobComplete]);

  const checkActiveJob = useCallback(async () => {
    try {
      const res = await fetch(`${apiBase}/api/v1/jobs/active`, { headers: { 'X-Client-Platform': platform } });
      const data = await res.json();
      if (data.job_id) {
        setState(prev => ({ ...prev, currentJobId: data.job_id, running: true }));
        connectWebSocket(data.job_id);
      }
    } catch (e) {
      console.error("Failed to fetch active job");
    }
  }, [apiBase, platform, connectWebSocket]);

  const uploadFile = async (file: File, type: "source" | "target") => {
    const formData = new FormData();
    formData.append('files', file);
    formData.append('type', type);
    const res = await fetch(`${apiBase}/api/v1/upload`, {
      method: 'POST',
      headers: { 'X-Client-Platform': platform },
      body: formData
    });
    const data = await res.json();
    return data.uploaded[0].file_id;
  };

  const cancelJob = async () => {
    if (state.running && state.currentJobId) {
      setState(prev => ({ ...prev, running: false, progress: 0, uploading: false }));
      if (wsRef.current) wsRef.current.close();
      await fetch(`${apiBase}/api/v1/jobs/${state.currentJobId}/cancel`, { method: 'POST' });
    } else if (state.running) {
      setState(prev => ({ ...prev, running: false, progress: 0, uploading: false }));
    }
  };

  const startJob = async (
    sourceType: "image" | "model",
    sourceFileOrModelId: File | string,
    targetFiles: File[],
    settings: any
  ) => {
    setState(prev => ({ ...prev, running: true, uploading: true, progress: 0 }));
    try {
      let sourceId = typeof sourceFileOrModelId === 'string' ? sourceFileOrModelId : '';
      if (sourceType === "image" && sourceFileOrModelId instanceof File) {
        sourceId = await uploadFile(sourceFileOrModelId, "source");
      }
      
      const targetUploadPromises = targetFiles.map(f => uploadFile(f, "target"));
      const targetIds = await Promise.all(targetUploadPromises);

      const jobRes = await fetch(`${apiBase}/api/v1/jobs`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', 'X-Client-Platform': platform },
        body: JSON.stringify({
          source_type: sourceType,
          source_file_id: sourceId,
          target_file_ids: targetIds,
          ...settings
        })
      });
      const jobData = await jobRes.json();
      setState(prev => ({ ...prev, currentJobId: jobData.job_id, uploading: false }));
      connectWebSocket(jobData.job_id);
    } catch (err) {
      alert("Error starting job: " + err);
      setState(prev => ({ ...prev, running: false, uploading: false }));
    }
  };

  return {
    jobState: state,
    setJobState: setState,
    checkActiveJob,
    startJob,
    cancelJob
  };
}
