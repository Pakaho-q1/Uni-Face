import { useState, useEffect } from 'react';
import { TopNav } from '@/components/layout/TopNav';
import { HistorySidebar } from '@/components/layout/HistorySidebar';
import { SettingsPanel, useSettings } from '@/components/layout/SettingsPanel';
import { BottomControlBar } from '@/components/layout/BottomControlBar';
import { PreviewStage } from '@/components/stage/PreviewStage';
import { ModelBuilderDialog } from '@/components/stage/ModelBuilderDialog';
import { Toaster } from 'sonner';
import { useHistory, type HistoryItem } from '@/hooks/useHistory';
import { useJobManager } from '@/hooks/useJobManager';

const API_BASE = `http://${window.location.hostname}:8000`;
const PLATFORM = "webui_react";

export default function App() {
  const [leftOpen, setLeftOpen] = useState(true);
  const [rightOpen, setRightOpen] = useState(false);
  const [previewVisible, setPreviewVisible] = useState(true);

  const [sourceType, setSourceType] = useState<"image" | "model">("image");
  const [sourceFile, setSourceFile] = useState<File | null>(null);
  const [sourcePreview, setSourcePreview] = useState<string>('');
  const [sourceModel, setSourceModel] = useState<string>('');
  const [availableModels, setAvailableModels] = useState<string[]>([]);
  const [builderOpen, setBuilderOpen] = useState(false);
  
  const [targetFiles, setTargetFiles] = useState<File[]>([]);
  
  const [lightboxItem, setLightboxItem] = useState<HistoryItem | null>(null);

  const settings = useSettings();
  
  const historyManager = useHistory(API_BASE, PLATFORM);
  
  const jobManager = useJobManager(API_BASE, PLATFORM, () => {
    historyManager.fetchHistory(0, false);
  });

  const fetchModels = async () => {
    try {
      const res = await fetch(`${API_BASE}/api/v1/face-models`, { headers: { 'X-Client-Platform': PLATFORM } });
      const data = await res.json();
      setAvailableModels(data.models.map((m: any) => m.name));
    } catch (e) {
      console.error("Failed to fetch models", e);
    }
  };

  // Initial load
  useEffect(() => {
    historyManager.fetchHistory(0, false);
    jobManager.checkActiveJob();
    fetchModels();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  // Sync dynamic preview settings with backend
  useEffect(() => {
    if (jobManager.jobState.currentJobId && jobManager.jobState.running) {
      jobManager.updatePreviewSettings(previewVisible, parseInt(settings.previewRes, 10));
    }
  }, [previewVisible, settings.previewRes, jobManager.jobState.currentJobId, jobManager.jobState.running]);

  const handleSourceChange = (file: File) => {
    setSourceFile(file);
    setSourcePreview(URL.createObjectURL(file));
  };

  const handleTargetChange = (files: File[]) => {
    setTargetFiles(files);
    const file = files[0];
    if (file.type.startsWith('video/') || file.type.startsWith('image/')) {
      jobManager.setJobState(prev => ({
        ...prev,
        targetType: file.type.startsWith('video/') ? 'video' : 'image',
        targetPreview: URL.createObjectURL(file)
      }));
    }
  };

  const toggleRun = () => {
    if (jobManager.jobState.running) {
      jobManager.cancelJob();
    } else {
      if ((sourceType === "image" && !sourceFile) || (sourceType === "model" && !sourceModel) || targetFiles.length === 0) {
        alert("Please select a Source and Target files.");
        return;
      }
      
      let processors = ["swap"];
      if (settings.faceRestore) processors.push("restore");
      if (settings.colorMatch) processors.push("color");

      const jobSettings = {
        preview_frequency: settings.previewFreq[0],
        preview_enabled: previewVisible,
        preview_resolution: parseInt(settings.previewRes, 10),
        processors: processors,
        swap_model: settings.swapModel,
        swap_weight: settings.swapWeight[0] / 100,
        restore_model: settings.restoreModel,
        restore_weight: settings.restoreWeight[0] / 100,
        restore_blend: settings.restoreBlend[0],
        mask_types: settings.maskTypes,
        mask_regions: settings.maskRegions,
        similarity: settings.similarity,
        providers: [settings.executionProvider],
        execution_thread_count: settings.executionThreadCount[0],
        skip_existing: settings.skipExisting
      };

      const src = sourceType === "image" ? sourceFile! : sourceModel;
      jobManager.startJob(sourceType, src, targetFiles, jobSettings);
    }
  };

  const toggleLeft = () => { 
    setLeftOpen(!leftOpen); 
    if (window.innerWidth < 768 && !leftOpen) setRightOpen(false);
  };
  const toggleRight = () => { 
    setRightOpen(!rightOpen); 
    if (window.innerWidth < 768 && !rightOpen) setLeftOpen(false);
  };

  return (
    <div className="flex flex-col h-[100dvh] w-full overflow-hidden bg-background">
      
      <TopNav 
        leftOpen={leftOpen} 
        rightOpen={rightOpen} 
        toggleLeft={toggleLeft} 
        toggleRight={toggleRight} 
      />

      <div className="flex-1 flex overflow-hidden relative">
        
        <HistorySidebar 
          open={leftOpen}
          onClose={() => setLeftOpen(false)}
          history={historyManager.history}
          hasMore={historyManager.hasMoreHistory}
          onLoadMore={() => historyManager.fetchHistory(historyManager.historyPage + 1, true)}
          onRefresh={() => historyManager.fetchHistory(0, false)}
          selectedItems={historyManager.selectedItems}
          onToggleSelect={historyManager.toggleSelection}
          onToggleSelectAll={historyManager.toggleSelectAll}
          onBulkDelete={historyManager.bulkDelete}
          onBulkDownload={historyManager.bulkDownload}
          lightboxItem={lightboxItem}
          setLightboxItem={setLightboxItem}
        />

        <PreviewStage 
          previewVisible={previewVisible}
          jobState={jobManager.jobState}
          sourceType={sourceType}
          sourceFile={sourceFile}
          sourcePreview={sourcePreview}
          sourceModel={sourceModel}
          targetFiles={targetFiles}
          onSourceTypeChange={setSourceType}
          onSourceChange={handleSourceChange}
          onSourceModelChange={setSourceModel}
          onTargetChange={handleTargetChange}
          availableModels={availableModels}
          onOpenModelBuilder={() => setBuilderOpen(true)}
        />

        <SettingsPanel 
          open={rightOpen}
          onClose={() => setRightOpen(false)}
          settings={settings}
        />
        
        <BottomControlBar 
          running={jobManager.jobState.running}
          uploading={jobManager.jobState.uploading}
          uploadProgress={jobManager.jobState.uploadProgress}
          progress={jobManager.jobState.progress}
          previewVisible={previewVisible}
          visible={!builderOpen}
          onToggleRun={toggleRun}
          onTogglePreview={() => setPreviewVisible(!previewVisible)}
        />
        
        <ModelBuilderDialog
          open={builderOpen}
          onClose={() => setBuilderOpen(false)}
          apiBase={API_BASE}
          platform={PLATFORM}
          onModelBuilt={fetchModels}
        />
        
        
      </div>
      <Toaster theme="dark" position="bottom-center" />
    </div>
  );
}
