import { useRef, useState } from 'react';
import { Video, Image as ImageIcon, User } from 'lucide-react';
import { toast } from 'sonner';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import type { ExtractedFace, JobState, TargetFile } from '@/types';

interface PreviewStageProps {
  previewVisible: boolean;
  jobState: JobState;
  sourceType: "image" | "model";
  sourceFile: File | null;
  sourcePreview: string;
  sourceModel: string;
  targetType: "upload" | "set";
  targetFiles: File[];
  targetSetFiles: TargetFile[];
  referenceFaces: ExtractedFace[];
  referenceThreshold: number;
  onSourceTypeChange: (type: "image" | "model") => void;
  onSourceChange: (file: File) => void;
  onSourceModelChange: (model: string) => void;
  onTargetTypeChange: (type: "upload" | "set") => void;
  onTargetChange: (files: File[]) => void;
  availableModels: string[];
  enableFaceCleanTools?: boolean;
  onOpenFaceClean?: () => void;
  onOpenModelBuilder: () => void;
  onOpenTargetManager: () => void;
  onOpenImmichManager: () => void;
  onOpenReferenceSelector: () => void;
}

export function PreviewStage({
  previewVisible, jobState, 
  sourceType, sourceFile, sourcePreview, sourceModel, 
  targetType, targetFiles, targetSetFiles,
  referenceFaces, referenceThreshold,
  onSourceTypeChange, onSourceChange, onSourceModelChange, 
  onTargetTypeChange, onTargetChange,
  availableModels, enableFaceCleanTools, onOpenFaceClean,
  onOpenModelBuilder, onOpenTargetManager, onOpenImmichManager, onOpenReferenceSelector
}: PreviewStageProps) {
  
  const sourceInputRef = useRef<HTMLInputElement>(null);
  const targetInputRef = useRef<HTMLInputElement>(null);
  
  const [sourceDrag, setSourceDrag] = useState(false);
  const [targetDrag, setTargetDrag] = useState(false);

  const handleSourceChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      onSourceChange(e.target.files[0]);
    }
  };

  const handleTargetChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files.length > 0) {
      onTargetChange(Array.from(e.target.files));
    }
  };

  const handleSourceDragOver = (e: React.DragEvent) => { e.preventDefault(); setSourceDrag(true); };
  const handleSourceDragLeave = (e: React.DragEvent) => { e.preventDefault(); setSourceDrag(false); };
  const handleSourceDrop = (e: React.DragEvent) => {
    e.preventDefault();
    setSourceDrag(false);
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      onSourceChange(e.dataTransfer.files[0]);
    }
  };

  const handleTargetDragOver = (e: React.DragEvent) => { e.preventDefault(); setTargetDrag(true); };
  const handleTargetDragLeave = (e: React.DragEvent) => { e.preventDefault(); setTargetDrag(false); };
  const handleTargetDrop = (e: React.DragEvent) => {
    e.preventDefault();
    setTargetDrag(false);
    if (e.dataTransfer.files && e.dataTransfer.files.length > 0) {
      onTargetChange(Array.from(e.dataTransfer.files));
    }
  };

  return (
    <main className="flex-1 flex flex-col min-w-0 min-h-0 p-3 md:p-4 pb-20 md:pb-20 gap-2.5 md:gap-3 overflow-y-auto overflow-x-hidden relative scroll-smooth">
      
      {/* The Main Screen */}
      <div className="relative bg-black md:border border-border rounded-xl md:rounded-2xl overflow-hidden flex items-center justify-center shadow-xl flex-1 min-h-[180px]">
        
        {/* HUD Elements */}
        <div className="absolute top-4 left-4 w-4 h-4 border-t-2 border-l-2 border-primary/50 pointer-events-none" />
        <div className="absolute top-4 right-4 w-4 h-4 border-t-2 border-r-2 border-primary/50 pointer-events-none" />
        <div className="absolute bottom-4 left-4 w-4 h-4 border-b-2 border-l-2 border-primary/50 pointer-events-none" />
        <div className="absolute bottom-4 right-4 w-4 h-4 border-b-2 border-r-2 border-primary/50 pointer-events-none" />

        <div className="absolute top-4 md:top-6 left-6 md:left-8 z-10 flex items-center gap-2 font-mono text-[10px] tracking-widest text-muted-foreground bg-black/40 px-2 py-1 rounded backdrop-blur-sm">
          <div className={`w-1.5 h-1.5 rounded-full ${jobState.running ? 'bg-destructive animate-pulse' : 'bg-muted-foreground'}`} />
          <span className={jobState.running ? 'text-destructive' : ''}>{jobState.running ? 'REC' : 'STBY'}</span>
        </div>
        
        <div className="absolute bottom-4 md:bottom-6 right-6 md:right-8 z-10 font-mono text-[10px] tracking-widest text-muted-foreground bg-black/40 px-2 py-1 rounded backdrop-blur-sm">
          --:--:--
        </div>

        {/* Video / Image Display */}
        {jobState.targetPreview ? (
          jobState.targetType === 'video' ? (
            <video className="w-full h-full object-contain" src={jobState.targetPreview} controls playsInline autoPlay muted loop />
          ) : (
            <img className="w-full h-full object-contain" src={jobState.targetPreview} alt="Preview" />
          )
        ) : (
          <div className="flex flex-col items-center gap-2 md:gap-3 text-muted-foreground opacity-50 p-4 md:p-6 text-center max-w-xs">
            <Video size={40} className="md:w-12 md:h-12" strokeWidth={1} />
            <p className="text-xs">Upload TARGET files and click START to see the preview here</p>
          </div>
        )}

        {/* Preview Off Overlay */}
        {!previewVisible && (
          <div className="absolute inset-0 bg-background/95 backdrop-blur-sm flex flex-col items-center justify-center gap-2 z-20 font-mono tracking-widest text-xs text-muted-foreground">
            <Video size={24} className="opacity-50" />
            <span>PREVIEW HIDDEN</span>
          </div>
        )}
      </div>

      {/* Uploaders & Control Cards (1-column on mobile, 2-column on desktop) */}
      <div className="shrink-0 grid grid-cols-1 md:grid-cols-2 gap-3">
        
        {/* Source Card */}
        <div 
          className={`flex flex-col gap-2 p-3 bg-secondary/50 border rounded-xl transition-all ${
            (sourceType === "image" && (sourceFile || sourceDrag)) || (sourceType === "model" && sourceModel)
              ? 'border-primary/50 shadow-[0_0_15px_rgba(var(--primary),0.1)]' 
              : 'border-border'
          } ${sourceDrag ? 'bg-secondary ring-2 ring-primary/50' : ''}`}
          onDragOver={handleSourceDragOver}
          onDragLeave={handleSourceDragLeave}
          onDrop={handleSourceDrop}
        >
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-2">
              <span className="font-mono text-[10px] tracking-widest text-foreground">SOURCE FACE</span>
              {enableFaceCleanTools && (
                <button 
                  type="button"
                  title="Visual Face Boundary Tuner"
                  onClick={(e) => {
                    e.stopPropagation();
                    if (!sourceFile && !sourcePreview) {
                      toast.info("Please upload a source image first");
                      return;
                    }
                    onOpenFaceClean?.();
                  }}
                  className="text-[10px] font-mono px-2 py-0.5 rounded border border-border hover:bg-primary/20 hover:text-primary transition-colors text-muted-foreground"
                >
                  BOUNDARY
                </button>
              )}
            </div>
            <div className="flex bg-background border border-border rounded-md overflow-hidden text-[10px] font-mono">
              <button 
                className={`px-3 py-1 ${sourceType === "image" ? "bg-primary text-primary-foreground" : "text-muted-foreground hover:bg-secondary"}`}
                onClick={() => onSourceTypeChange("image")}
              >
                IMAGE
              </button>
              <button 
                className={`px-3 py-1 border-l border-border ${sourceType === "model" ? "bg-primary text-primary-foreground" : "text-muted-foreground hover:bg-secondary"}`}
                onClick={() => onSourceTypeChange("model")}
              >
                MODEL
              </button>
            </div>
          </div>
          
          {sourceType === "image" ? (
            <div className="flex items-center gap-3 cursor-pointer mt-1" onClick={() => sourceInputRef.current?.click()}>
              <input type="file" accept="image/*" hidden ref={sourceInputRef} onChange={handleSourceChange} />
              <div className="w-12 h-12 shrink-0 rounded-lg bg-background flex items-center justify-center text-muted-foreground overflow-hidden border border-border">
                {sourcePreview ? <img src={sourcePreview} className="w-full h-full object-cover" alt="source" /> : <ImageIcon size={20} />}
              </div>
              <div className="flex flex-col min-w-0 flex-1">
                <span className="text-xs text-muted-foreground truncate">{sourceFile ? sourceFile.name : 'Click or drag image here'}</span>
              </div>
            </div>
          ) : (
            <div className="flex items-center gap-2 mt-1 min-w-0">
              <Select value={sourceModel} onValueChange={onSourceModelChange}>
                <SelectTrigger className="h-10 text-xs bg-background border-border flex-1 min-w-0 [&>span]:truncate px-3">
                  <SelectValue placeholder="Select model" />
                </SelectTrigger>
                <SelectContent>
                  {availableModels.length === 0 ? (
                    <SelectItem value="none" disabled>No models found</SelectItem>
                  ) : (
                    availableModels.map(m => (
                      <SelectItem key={m} value={m}>{m}</SelectItem>
                    ))
                  )}
                </SelectContent>
              </Select>
              <button 
                className="shrink-0 h-10 px-4 bg-secondary hover:bg-primary hover:text-primary-foreground text-xs font-mono font-medium rounded-md border border-border transition-colors flex items-center justify-center"
                onClick={onOpenModelBuilder}
              >
                BUILD
              </button>
            </div>
          )}
        </div>

        {/* Target Card */}
        <div 
          className={`flex flex-col p-3 bg-secondary/50 border rounded-xl transition-all ${((targetType === "upload" && targetFiles.length > 0) || (targetType === "set" && targetSetFiles.length > 0)) || targetDrag ? 'border-primary/50 shadow-[0_0_15px_rgba(var(--primary),0.1)]' : 'border-border'} ${targetDrag ? 'bg-secondary ring-2 ring-primary/50' : ''}`}
          onDragOver={targetType === "upload" ? handleTargetDragOver : undefined}
          onDragLeave={targetType === "upload" ? handleTargetDragLeave : undefined}
          onDrop={targetType === "upload" ? handleTargetDrop : undefined}
        >
          <div className="flex items-center justify-between mb-2">
            <span className="font-mono text-[10px] tracking-widest text-foreground">TARGET</span>
            <div className="flex bg-background border border-border rounded-md overflow-hidden text-[10px] font-mono">
              <button 
                className={`px-3 py-1 ${targetType === "upload" ? "bg-primary text-primary-foreground" : "text-muted-foreground hover:bg-secondary"}`}
                onClick={() => onTargetTypeChange("upload")}
              >
                UPLOAD
              </button>
              <button 
                className={`px-3 py-1 border-l border-border ${targetType === "set" ? "bg-primary text-primary-foreground" : "text-muted-foreground hover:bg-secondary"}`}
                onClick={() => onTargetTypeChange("set")}
              >
                GALLERY
              </button>
            </div>
          </div>
          
          {targetType === "upload" ? (
            <div className="flex items-center gap-3 cursor-pointer mt-1" onClick={() => targetInputRef.current?.click()}>
              <input type="file" accept="image/*,video/*" multiple hidden ref={targetInputRef} onChange={handleTargetChange} />
              <div className="w-12 h-12 shrink-0 rounded-lg bg-background flex items-center justify-center text-muted-foreground relative border border-border">
                <Video size={20} />
                {referenceFaces.length > 0 && (
                  <img src={referenceFaces[0].url} className="absolute inset-0 w-full h-full object-cover rounded-lg border-2 border-primary" alt="ref" />
                )}
              </div>
              <div className="flex flex-col min-w-0 flex-1">
                <span className="text-xs text-muted-foreground truncate">{targetFiles.length > 0 ? targetFiles.map(f => f.name).join(', ') : 'Click or drag files here'}</span>
              </div>
              {targetFiles.length > 0 && (
                <span className="shrink-0 font-mono text-[10px] bg-primary/20 text-primary px-2 py-0.5 rounded-full">
                  {targetFiles.length}
                </span>
              )}
            </div>
          ) : (
            <div className="flex items-center gap-2 mt-1 min-w-0">
              {/* Dashed Box: Status info only (Item count & Specific Face Filter preview) */}
              <div className="flex-1 flex flex-col items-center justify-center border border-dashed border-border rounded-lg bg-background/50 p-2 text-center relative overflow-hidden min-h-[44px]">
                {referenceFaces.length > 0 && (
                  <div className="absolute inset-0 bg-background/80 backdrop-blur-sm z-0" />
                )}
                {referenceFaces.length > 0 && (
                  <img src={referenceFaces[0].url} className="absolute left-1/2 top-1/2 -translate-x-1/2 -translate-y-1/2 h-full opacity-40 z-0 object-cover" alt="ref" />
                )}
                <div className="z-10 flex items-center gap-2">
                  <span className="text-xs font-medium">
                    {targetSetFiles.length > 0 ? `${targetSetFiles.length} items selected` : 'No media selected'}
                  </span>
                  {referenceFaces.length > 0 && (
                    <span className="text-[10px] font-mono bg-primary/20 text-primary px-1.5 py-0.5 rounded border border-primary/30 flex items-center gap-1">
                      <User size={10} /> {referenceFaces.length} Face Filter
                    </span>
                  )}
                </div>
              </div>

              {/* Action Button: File Set (no icon) */}
              <button 
                className="shrink-0 h-10 px-3.5 bg-secondary hover:bg-primary hover:text-primary-foreground text-xs font-mono font-medium rounded-md border border-border transition-colors flex items-center justify-center"
                onClick={onOpenTargetManager}
                title="Manage File Sets"
              >
                File Set
              </button>

              {/* Action Button: Immich (no icon) */}
              <button 
                className="shrink-0 h-10 px-3.5 bg-secondary hover:bg-primary hover:text-primary-foreground text-xs font-mono font-medium rounded-md border border-border transition-colors flex items-center justify-center"
                onClick={onOpenImmichManager}
                title="Browse Immich Library"
              >
                Immich
              </button>
            </div>
          )}

          {/* Reference Face Selector Button */}
          {((targetType === "upload" && targetFiles.length > 0) || (targetType === "set" && targetSetFiles.length > 0)) && (
            <div className="mt-2.5 flex justify-end">
              <button 
                className={`flex items-center gap-2 px-3 py-1 text-xs font-medium rounded-md border transition-colors ${referenceFaces.length > 0 ? 'bg-primary/20 border-primary/50 text-primary hover:bg-primary/30' : 'bg-background border-border text-muted-foreground hover:bg-secondary'}`}
                onClick={onOpenReferenceSelector}
              >
                <User size={13} />
                {referenceFaces.length > 0 ? `Targeting ${referenceFaces.length} Face(s) [${referenceThreshold}]` : 'Filter Specific Face'}
              </button>
            </div>
          )}
        </div>
      </div>
      
    </main>
  );
}
