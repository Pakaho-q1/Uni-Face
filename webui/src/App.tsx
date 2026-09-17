import { useState, useEffect, useRef, useCallback } from 'react';
import { toast, Toaster } from 'sonner';
import { TopNav } from '@/components/layout/TopNav';
import { HistorySidebar } from '@/components/layout/HistorySidebar';
import { SettingsPanel } from '@/components/layout/SettingsPanel';
import { BottomControlBar } from '@/components/layout/BottomControlBar';
import { PreviewStage } from '@/components/stage/PreviewStage';
import { ModelBuilderDialog } from '@/components/stage/ModelBuilderDialog';
import { TargetSetManager } from '@/components/stage/TargetSetManager';
import { ImmichTargetManager } from '@/components/stage/ImmichTargetManager';
import { ReferenceFaceSelector } from '@/components/stage/ReferenceFaceSelector';
import { JobManagerDialog } from '@/components/stage/JobManagerDialog';
import { FaceCleanDialog } from '@/components/stage/FaceCleanDialog';
import { useSettings } from '@/hooks/useSettings';
import { useHistory } from '@/hooks/useHistory';
import { useJobManager } from '@/hooks/useJobManager';
import { api } from '@/services/api';
import type { HistoryItem, ExtractedFace, TargetFile } from '@/types';

export default function App() {
  const [leftOpen, setLeftOpen] = useState(false);
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

  const [targetType, setTargetType] = useState<"upload" | "set">("upload");
  const [targetSetFiles, setTargetSetFiles] = useState<TargetFile[]>([]);
  const [targetManagerOpen, setTargetManagerOpen] = useState(false);
  const [immichManagerOpen, setImmichManagerOpen] = useState(false);

  const [referenceSelectorOpen, setReferenceSelectorOpen] = useState(false);
  const [referenceFaces, setReferenceFaces] = useState<ExtractedFace[]>([]);
  const [referenceThreshold, setReferenceThreshold] = useState<number>(0.6);

  const [faceCleanOpen, setFaceCleanOpen] = useState(false);
  const [faceCleanFile, setFaceCleanFile] = useState<File | null>(null);

  const [jobManagerOpen, setJobManagerOpen] = useState(false);
  const [activeJobCount, setActiveJobCount] = useState(0);

  const sourcePreviewUrlRef = useRef<string>('');
  const targetPreviewUrlRef = useRef<string>('');

  const settings = useSettings();
  const historyManager = useHistory();
  
  const updateActiveCount = useCallback(async () => {
    if (typeof document !== 'undefined' && document.hidden) return;
    try {
      const count = await api.getActiveJobsCount();
      setActiveJobCount(count);
    } catch {
      // ignore
    }
  }, []);

  const jobManager = useJobManager(() => {
    historyManager.fetchHistory(0, false);
    updateActiveCount();
  });

  const fetchModels = async () => {
    try {
      const data = await api.getFaceModels();
      setAvailableModels(data.models.map(m => m.name));
    } catch (e) {
      console.error("Failed to fetch models", e);
    }
  };

  // Initial load
  useEffect(() => {
    historyManager.fetchHistory(0, false);
    jobManager.checkActiveJob();
    fetchModels();
    updateActiveCount();
    const countInterval = setInterval(updateActiveCount, 3000);
    const handleVisibilityChange = () => {
      if (!document.hidden) {
        updateActiveCount();
      }
    };
    document.addEventListener('visibilitychange', handleVisibilityChange);
    return () => {
      clearInterval(countInterval);
      document.removeEventListener('visibilitychange', handleVisibilityChange);
    };
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [updateActiveCount]);

  const { currentJobId, running } = jobManager.jobState;
  const { updatePreviewSettings } = jobManager;

  // Sync dynamic preview settings with backend
  useEffect(() => {
    if (currentJobId && running) {
      updatePreviewSettings(previewVisible, parseInt(settings.previewRes, 10));
    }
  }, [previewVisible, settings.previewRes, currentJobId, running, updatePreviewSettings]);

  const handleSourceChange = (file: File) => {
    if (sourcePreviewUrlRef.current) {
      URL.revokeObjectURL(sourcePreviewUrlRef.current);
    }
    const newUrl = URL.createObjectURL(file);
    sourcePreviewUrlRef.current = newUrl;
    setSourceFile(file);
    setSourcePreview(newUrl);
  };

  const handleTargetChange = (files: File[]) => {
    setTargetFiles(files);
    const file = files[0];
    if (file && (file.type.startsWith('video/') || file.type.startsWith('image/'))) {
      if (targetPreviewUrlRef.current) {
        URL.revokeObjectURL(targetPreviewUrlRef.current);
      }
      const newUrl = URL.createObjectURL(file);
      targetPreviewUrlRef.current = newUrl;
      jobManager.setJobState(prev => ({
        ...prev,
        targetType: file.type.startsWith('video/') ? 'video' : 'image',
        targetPreview: newUrl
      }));
    }
  };

  const toggleRun = () => {
    if (jobManager.jobState.running) {
      jobManager.cancelJob();
    } else {
      const hasSource = (sourceType === "image" && sourceFile) || (sourceType === "model" && sourceModel);
      const hasTarget = (targetType === "upload" && targetFiles.length > 0) || (targetType === "set" && targetSetFiles.length > 0);
      
      if (!hasSource || !hasTarget) {
        toast.error("Missing Input", { description: "Please select both Source and Target media before starting." });
        return;
      }
      
      const processors = ["swap"];
      if (settings.stage1Restore || settings.stage2Restore || settings.faceRestore) processors.push("restore");
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
        occlusion_model: settings.occlusionModel,
        target_gender: settings.genderFilter ? settings.targetGender : 'all',
        face_order: settings.faceOrder,
        similarity: settings.similarity,
        providers: [settings.executionProvider],
        execution_thread_count: settings.executionThreadCount[0],
        skip_existing: settings.skipExisting,
        reference_face_ids: referenceFaces.map(f => f.id),
        reference_threshold: referenceThreshold,
        face_detector_score: settings.faceDetectorScore[0] / 100,
        face_landmark_score: settings.faceLandmarkScore[0] / 100,
        stage1_restore: settings.stage1Restore,
        dual_swap: settings.dualSwap,
        swap_model_2: settings.swapModel2,
        swap_weight_2: settings.swapWeight2[0] / 100,
        stage2_restore: settings.stage2Restore,
        restore_model_2: settings.restoreModel2,
        restore_weight_2: settings.restoreWeight2[0] / 100,
        restore_blend_2: settings.restoreBlend2[0],
        clean_source_face: false,
        mask_padding: settings.enableFaceCleanTools ? settings.maskPadding : [0, 0, 0, 0],
        mask_blur: (settings.enableFaceCleanTools ? settings.maskBlur[0] : 30) / 100,
        face_boost: settings.faceBoost,
        restore_source_face: settings.restoreSourceFace,
        restore_source_face_model: settings.restoreSourceFaceModel,
        restore_source_face_weight: settings.restoreSourceFaceWeight[0] / 100,
        target_hair_protect: settings.targetHairProtect,
        
        immich_url: settings.immichUrl,
        immich_api_key: settings.immichApiKey,
        immich_auto_save: settings.immichAutoSave,
        immich_new_album: settings.immichNewAlbum,
        immich_album: settings.immichAlbum,
        immich_tags: settings.immichTags,
        immich_delete_local: settings.immichDeleteLocal
      };

      const src = sourceType === "image" ? sourceFile! : sourceModel;
      const tgts = targetType === "upload" ? targetFiles : targetSetFiles.map(f => f.file_id);
      
      jobManager.startJob(sourceType, src, targetType, tgts, jobSettings);
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
        openJobManager={() => setJobManagerOpen(true)}
        activeJobCount={Math.max(activeJobCount, jobManager.jobState.running ? 1 : 0)}
      />

      <div className="flex-1 flex overflow-hidden relative">
        
        <HistorySidebar 
          open={leftOpen}
          onClose={() => setLeftOpen(false)}
          history={historyManager.history}
          totalHistory={historyManager.totalHistory}
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
          settings={settings}
        />

        <PreviewStage 
          previewVisible={previewVisible}
          jobState={jobManager.jobState}
          sourceType={sourceType}
          sourceFile={sourceFile}
          sourcePreview={sourcePreview}
          sourceModel={sourceModel}
          targetFiles={targetFiles}
          targetType={targetType}
          targetSetFiles={targetSetFiles}
          referenceFaces={referenceFaces}
          referenceThreshold={referenceThreshold}
          onSourceTypeChange={setSourceType}
          onSourceChange={handleSourceChange}
          onSourceModelChange={setSourceModel}
          onTargetTypeChange={setTargetType}
          onTargetChange={handleTargetChange}
          availableModels={availableModels}
          enableFaceCleanTools={settings.enableFaceCleanTools}
          onOpenFaceClean={() => {
            setFaceCleanFile(sourceFile);
            setFaceCleanOpen(true);
          }}
          onOpenModelBuilder={() => setBuilderOpen(true)}
          onOpenTargetManager={() => setTargetManagerOpen(true)}
          onOpenImmichManager={() => {
            if (!settings.immichUrl || !settings.immichApiKey) {
              toast.error("Immich Not Connected", { description: "Please enter your Immich URL and API Key in Settings first." });
              setRightOpen(true);
              return;
            }
            setImmichManagerOpen(true);
          }}
          onOpenReferenceSelector={() => setReferenceSelectorOpen(true)}
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
          onModelBuilt={fetchModels}
          enableFaceCleanTools={settings.enableFaceCleanTools}
          onOpenFaceClean={(file) => {
            setFaceCleanFile(file);
            setFaceCleanOpen(true);
          }}
        />
        
        <TargetSetManager
          open={targetManagerOpen}
          chunkSizeMB={settings.hashChunkSize[0]}
          onOpenChange={setTargetManagerOpen}
          onSelectSet={(files) => {
            setTargetSetFiles(files);
            setTargetType("set");
          }}
        />

        <ImmichTargetManager
          open={immichManagerOpen}
          onOpenChange={setImmichManagerOpen}
          immichUrl={settings.immichUrl}
          immichApiKey={settings.immichApiKey}
          immichLocalPath={settings.immichLocalPath}
          onSelectTargets={(files) => {
            setTargetSetFiles(files);
            setTargetType("set");
          }}
        />

        <ReferenceFaceSelector
          open={referenceSelectorOpen}
          onOpenChange={setReferenceSelectorOpen}
          targetType={targetType}
          sampleCount={settings.scanSampleCount[0]}
          targetFiles={targetFiles}
          targetSetFiles={targetSetFiles.map(f => f.file_id)}
          initialFaces={referenceFaces}
          initialThreshold={referenceThreshold}
          onConfirm={(faces, threshold) => {
            setReferenceFaces(faces);
            setReferenceThreshold(threshold);
          }}
        />

        <JobManagerDialog
          open={jobManagerOpen}
          onOpenChange={setJobManagerOpen}
          onJobStarted={() => {
            jobManager.checkActiveJob();
            updateActiveCount();
          }}
        />

        <FaceCleanDialog 
          open={faceCleanOpen}
          onOpenChange={setFaceCleanOpen}
          file={faceCleanFile || sourceFile}
          sourcePreviewUrl={faceCleanFile === sourceFile ? sourcePreview : undefined}
          maskPadding={settings.maskPadding}
          maskBlur={settings.maskBlur}
          onSave={(padding, blur) => {
            settings.setMaskPadding(padding);
            settings.setMaskBlur([blur]);
          }}
        />
      </div>
      <Toaster theme="dark" position="bottom-center" />
    </div>
  );
}
