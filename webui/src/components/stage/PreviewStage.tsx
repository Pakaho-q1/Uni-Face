import { useRef, useState } from 'react';
import { Video, Image as ImageIcon } from 'lucide-react';
import type { JobState } from '@/hooks/useJobManager';

import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';

interface PreviewStageProps {
  previewVisible: boolean;
  jobState: JobState;
  sourceType: "image" | "model";
  sourceFile: File | null;
  sourcePreview: string;
  sourceModel: string;
  targetFiles: File[];
  onSourceTypeChange: (type: "image" | "model") => void;
  onSourceChange: (file: File) => void;
  onSourceModelChange: (model: string) => void;
  onTargetChange: (files: File[]) => void;
  availableModels: string[];
  onOpenModelBuilder: () => void;
}

export function PreviewStage({
  previewVisible, jobState, 
  sourceType, sourceFile, sourcePreview, sourceModel, 
  targetFiles, onSourceTypeChange, onSourceChange, onSourceModelChange, onTargetChange,
  availableModels, onOpenModelBuilder
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
    <main className="flex-1 flex flex-col min-w-0 min-h-0 p-4 gap-4 overflow-hidden relative">
      
      {/* The Main Screen */}
      <div className="flex-1 relative bg-black border border-border rounded-2xl overflow-hidden flex items-center justify-center shadow-2xl">
        
        {/* HUD Elements */}
        <div className="absolute top-4 left-4 w-4 h-4 border-t-2 border-l-2 border-primary/50 pointer-events-none" />
        <div className="absolute top-4 right-4 w-4 h-4 border-t-2 border-r-2 border-primary/50 pointer-events-none" />
        <div className="absolute bottom-4 left-4 w-4 h-4 border-b-2 border-l-2 border-primary/50 pointer-events-none" />
        <div className="absolute bottom-4 right-4 w-4 h-4 border-b-2 border-r-2 border-primary/50 pointer-events-none" />

        <div className="absolute top-6 left-8 z-10 flex items-center gap-2 font-mono text-[10px] tracking-widest text-muted-foreground bg-black/40 px-2 py-1 rounded">
          <div className={`w-1.5 h-1.5 rounded-full ${jobState.running ? 'bg-destructive animate-pulse' : 'bg-muted-foreground'}`} />
          <span className={jobState.running ? 'text-destructive' : ''}>{jobState.running ? 'REC' : 'STBY'}</span>
        </div>
        
        <div className="absolute bottom-6 right-8 z-10 font-mono text-[10px] tracking-widest text-muted-foreground bg-black/40 px-2 py-1 rounded">
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
          <div className="flex flex-col items-center gap-3 text-muted-foreground opacity-50 p-6 text-center max-w-xs">
            <Video size={48} strokeWidth={1} />
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

      {/* Uploaders */}
      <div className="shrink-0 grid grid-cols-1 md:grid-cols-2 gap-3 mb-16">
        
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
            <span className="font-mono text-[10px] tracking-widest text-foreground">SOURCE FACE</span>
            <div className="flex bg-background border border-border rounded-md overflow-hidden text-[10px] font-mono">
              <button 
                className={`px-2 py-1 ${sourceType === "image" ? "bg-primary text-primary-foreground" : "text-muted-foreground hover:bg-secondary"}`}
                onClick={() => onSourceTypeChange("image")}
              >
                IMAGE
              </button>
              <button 
                className={`px-2 py-1 border-l border-border ${sourceType === "model" ? "bg-primary text-primary-foreground" : "text-muted-foreground hover:bg-secondary"}`}
                onClick={() => onSourceTypeChange("model")}
              >
                MODEL
              </button>
            </div>
          </div>
          
          {sourceType === "image" ? (
            <div className="flex items-center gap-3 cursor-pointer mt-1" onClick={() => sourceInputRef.current?.click()}>
              <input type="file" accept="image/*" hidden ref={sourceInputRef} onChange={handleSourceChange} />
              <div className="w-12 h-12 shrink-0 rounded-lg bg-background flex items-center justify-center text-muted-foreground overflow-hidden">
                {sourcePreview ? <img src={sourcePreview} className="w-full h-full object-cover" alt="source" /> : <ImageIcon size={20} />}
              </div>
              <div className="flex flex-col min-w-0">
                <span className="text-xs text-muted-foreground truncate">{sourceFile ? sourceFile.name : 'Click or drag image here'}</span>
              </div>
            </div>
          ) : (
            <div className="flex items-center gap-2 mt-1">
              <Select value={sourceModel} onValueChange={onSourceModelChange}>
                <SelectTrigger className="h-9 text-xs bg-background border-border flex-1">
                  <SelectValue placeholder="Select .safetensors model" />
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
                className="shrink-0 h-9 px-3 bg-secondary hover:bg-primary hover:text-primary-foreground text-xs font-medium rounded-md border border-border transition-colors"
                onClick={onOpenModelBuilder}
              >
                BUILD
              </button>
            </div>
          )}
        </div>

        {/* Target Card */}
        <div 
          className={`flex items-center gap-3 p-3 bg-secondary/50 border rounded-xl cursor-pointer transition-all hover:bg-secondary hover:border-primary/50 ${targetFiles.length > 0 || targetDrag ? 'border-primary/50 shadow-[0_0_15px_rgba(var(--primary),0.1)]' : 'border-border'} ${targetDrag ? 'bg-secondary ring-2 ring-primary/50' : ''}`}
          onClick={() => targetInputRef.current?.click()}
          onDragOver={handleTargetDragOver}
          onDragLeave={handleTargetDragLeave}
          onDrop={handleTargetDrop}
        >
          <input type="file" accept="image/*,video/*" multiple hidden ref={targetInputRef} onChange={handleTargetChange} />
          <div className="w-12 h-12 shrink-0 rounded-lg bg-background flex items-center justify-center text-muted-foreground">
            <Video size={20} />
          </div>
          <div className="flex flex-col min-w-0 flex-1">
            <span className="font-mono text-[10px] tracking-widest text-foreground">TARGET</span>
            <span className="text-xs text-muted-foreground truncate">{targetFiles.length > 0 ? targetFiles.map(f => f.name).join(', ') : 'Click to upload · Multiple allowed'}</span>
          </div>
          {targetFiles.length > 0 && (
            <span className="shrink-0 font-mono text-[10px] bg-primary/20 text-primary px-2 py-0.5 rounded-full">
              {targetFiles.length}
            </span>
          )}
        </div>
      </div>
      
    </main>
  );
}
