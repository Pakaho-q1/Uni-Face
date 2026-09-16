import React, { useState, useEffect, useMemo } from 'react';
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogDescription, DialogFooter } from '@/components/ui/dialog';
import { Button } from '@/components/ui/button';
import { Upload, X, Loader2, Trash2, Box } from 'lucide-react';
import { toast } from 'sonner';
import { api } from '@/services/api';
import type { FaceModelItem } from '@/types';

interface ModelBuilderDialogProps {
  open: boolean;
  onClose: () => void;
  onModelBuilt: () => void;
  enableFaceCleanTools?: boolean;
  onOpenFaceClean?: (file: File) => void;
}

export function ModelBuilderDialog({ open, onClose, onModelBuilt, enableFaceCleanTools, onOpenFaceClean }: ModelBuilderDialogProps) {
  const [activeTab, setActiveTab] = useState<'build' | 'manage'>('build');
  const [modelName, setModelName] = useState('');
  const [files, setFiles] = useState<File[]>([]);
  const [selectedImageIndex, setSelectedImageIndex] = useState<number | null>(null);
  const [isBuilding, setIsBuilding] = useState(false);
  const [error, setError] = useState<string | null>(null);

  // Existing models state
  const [savedModels, setSavedModels] = useState<FaceModelItem[]>([]);
  const [isLoadingModels, setIsLoadingModels] = useState(false);
  const [deletingModel, setDeletingModel] = useState<string | null>(null);

  // Load saved models when dialog opens or after build
  const loadSavedModels = async () => {
    setIsLoadingModels(true);
    try {
      const data = await api.getFaceModels();
      setSavedModels(data.models || []);
    } catch (e) {
      console.error("Failed to load face models:", e);
    } finally {
      setIsLoadingModels(false);
    }
  };

  useEffect(() => {
    if (open) {
      loadSavedModels();
    }
  }, [open]);

  // Object URLs for image previews
  const filePreviews = useMemo(() => {
    return files.map(file => ({
      file,
      url: URL.createObjectURL(file)
    }));
  }, [files]);

  // Clean up object URLs on change
  useEffect(() => {
    return () => {
      filePreviews.forEach(item => URL.revokeObjectURL(item.url));
    };
  }, [filePreviews]);

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files.length > 0) {
      const newFiles = Array.from(e.target.files);
      setFiles(prev => [...prev, ...newFiles]);
    }
    // reset input
    e.target.value = '';
  };

  const removeFile = (index: number) => {
    setFiles(prev => prev.filter((_, i) => i !== index));
    setSelectedImageIndex(prev => {
      if (prev === null) return null;
      if (prev === index) return null;
      if (prev > index) return prev - 1;
      return prev;
    });
  };

  const clearAllFiles = () => {
    setFiles([]);
    setSelectedImageIndex(null);
  };

  const handleDeleteModel = async (name: string) => {
    setDeletingModel(name);
    try {
      await api.deleteFaceModel(name);
      toast.success(`Deleted model '${name}'`);
      setSavedModels(prev => prev.filter(m => m.name !== name));
      onModelBuilt(); // Refresh global model list
    } catch (err: any) {
      toast.error(`Failed to delete model`, { description: err.message });
    } finally {
      setDeletingModel(null);
    }
  };

  const handleBuild = async () => {
    if (!modelName.trim()) {
      setError("Please provide a model name.");
      return;
    }
    if (files.length === 0) {
      setError("Please upload at least one image.");
      return;
    }

    setIsBuilding(true);
    setError(null);

    try {
      const formData = new FormData();
      formData.append('name', modelName.trim());
      files.forEach(f => formData.append('files', f));

      const data = await api.buildFaceModel(formData);

      toast.success(`Successfully built model '${data.model_name}' with ${data.faces_extracted} faces extracted!`);
      onModelBuilt();
      await loadSavedModels();
      setModelName('');
      setFiles([]);
      setSelectedImageIndex(null);
      setActiveTab('manage');
    } catch (err: any) {
      setError(err.message || "Failed to build model.");
      toast.error("Failed to build model", { description: err.message });
    } finally {
      setIsBuilding(false);
    }
  };

  return (
    <Dialog open={open} onOpenChange={(val) => !val && onClose()}>
      <DialogContent className="sm:max-w-[560px] max-h-[90vh] flex flex-col p-6 overflow-hidden">
        <DialogHeader className="shrink-0 pb-2">
          <div className="flex items-center justify-between">
            <DialogTitle className="text-base font-mono tracking-wider flex items-center gap-2">
              <Box size={18} className="text-primary" />
              FACE MODEL MANAGER
            </DialogTitle>
          </div>
          <DialogDescription className="text-xs">
            Build multi-angle .safetensors embedding models or manage saved models.
          </DialogDescription>

          {/* Navigation Tabs */}
          <div className="flex bg-secondary p-0.5 rounded-lg text-xs font-mono mt-3">
            <button
              className={`flex-1 py-1.5 rounded-md transition-all ${
                activeTab === 'build' ? 'bg-primary text-primary-foreground font-bold shadow' : 'text-muted-foreground hover:text-foreground'
              }`}
              onClick={() => setActiveTab('build')}
            >
              🔨 BUILD MODEL
            </button>
            <button
              className={`flex-1 py-1.5 rounded-md transition-all flex items-center justify-center gap-1.5 ${
                activeTab === 'manage' ? 'bg-primary text-primary-foreground font-bold shadow' : 'text-muted-foreground hover:text-foreground'
              }`}
              onClick={() => setActiveTab('manage')}
            >
              <span>📁 SAVED MODELS</span>
              <span className="text-[10px] bg-background/40 px-1.5 py-0.2 rounded-full font-mono">
                {savedModels.length}
              </span>
            </button>
          </div>
        </DialogHeader>

        {/* Tab 1: Build Model */}
        {activeTab === 'build' && (
          <div className="flex-1 flex flex-col min-h-0 space-y-4 py-2 overflow-y-auto pr-1">
            <div className="space-y-1.5">
              <label className="text-xs font-mono font-medium text-foreground">Model Name</label>
              <input 
                type="text"
                className="flex h-9 w-full rounded-md border border-input bg-background px-3 py-1 text-xs ring-offset-background placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-primary font-mono"
                placeholder="e.g. avatar_character" 
                value={modelName} 
                onChange={(e: React.ChangeEvent<HTMLInputElement>) => setModelName(e.target.value)} 
                disabled={isBuilding}
              />
            </div>

            <div className="space-y-2 flex-1 flex flex-col min-h-0">
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-2">
                  <label className="text-xs font-mono font-medium text-foreground">
                    Training Images ({files.length})
                  </label>
                  {enableFaceCleanTools && (
                    <button
                      type="button"
                      disabled={isBuilding}
                      onClick={() => {
                        if (files.length === 0 || selectedImageIndex === null || !files[selectedImageIndex]) {
                          toast.info("Please upload and select an image first");
                          return;
                        }
                        onOpenFaceClean?.(files[selectedImageIndex]);
                      }}
                      className="text-[10px] font-mono px-2 py-0.5 rounded border border-border hover:bg-primary/20 hover:text-primary transition-colors text-muted-foreground disabled:opacity-50"
                      title="Visual Face Boundary Tuner for selected image"
                    >
                      BOUNDARY
                    </button>
                  )}
                </div>
                {files.length > 0 && (
                  <button
                    onClick={clearAllFiles}
                    disabled={isBuilding}
                    className="text-xs text-destructive hover:underline flex items-center gap-1 font-mono"
                  >
                    <Trash2 size={12} />
                    <span>Clear All</span>
                  </button>
                )}
              </div>

              {/* Upload Drop Area */}
              <div className="border-2 border-dashed border-border rounded-xl p-4 text-center hover:bg-secondary/40 transition-colors shrink-0">
                <label className="cursor-pointer flex flex-col items-center gap-1.5">
                  <Upload className="h-6 w-6 text-primary/70" />
                  <span className="text-xs font-medium text-foreground">Click to upload training images</span>
                  <span className="text-[11px] text-muted-foreground">Select multiple angles/expressions (JPG, PNG)</span>
                  <input 
                    type="file" 
                    multiple 
                    accept="image/*" 
                    className="hidden" 
                    onChange={handleFileChange}
                    disabled={isBuilding}
                  />
                </label>
              </div>
              
              {/* Visual Thumbnail Grid with Delete Buttons */}
              {filePreviews.length > 0 && (
                <div className="border border-border rounded-xl p-2.5 bg-background/50 flex-1 overflow-y-auto min-h-[140px] max-h-[220px]">
                  <div className="grid grid-cols-4 sm:grid-cols-5 gap-2">
                    {filePreviews.map((item, i) => {
                      const isSelected = selectedImageIndex === i;
                      return (
                        <div 
                          key={i} 
                          onClick={() => setSelectedImageIndex(isSelected ? null : i)}
                          className={`group relative aspect-square rounded-lg border bg-secondary overflow-hidden shadow-sm transition-all cursor-pointer ${
                            isSelected 
                              ? 'border-primary ring-2 ring-primary/80 scale-[0.98]' 
                              : 'border-border hover:border-primary/60'
                          }`}
                        >
                          <img 
                            src={item.url} 
                            alt={item.file.name} 
                            className="w-full h-full object-cover" 
                          />

                          {isSelected && (
                            <div className="absolute top-1 left-1 bg-primary text-primary-foreground text-[8px] font-mono font-bold px-1.5 py-0.2 rounded shadow">
                              ACTIVE
                            </div>
                          )}
                          
                          {/* Delete Button on Hover / Mobile */}
                          <button
                            type="button"
                            onClick={(e) => {
                              e.stopPropagation();
                              removeFile(i);
                            }}
                            disabled={isBuilding}
                            className="absolute top-1 right-1 w-6 h-6 rounded-full bg-black/80 hover:bg-destructive text-white flex items-center justify-center transition-colors shadow"
                            title="Remove image"
                          >
                            <X size={13} />
                          </button>
                          
                          <div className="absolute bottom-0 inset-x-0 bg-black/70 px-1 py-0.5 text-[9px] text-muted-foreground truncate font-mono text-center">
                            {item.file.name}
                          </div>
                        </div>
                      );
                    })}
                  </div>
                </div>
              )}
            </div>
            
            {error && (
              <div className="text-xs text-destructive bg-destructive/10 border border-destructive/20 p-2 rounded-md font-mono">
                {error}
              </div>
            )}
          </div>
        )}

        {/* Tab 2: Manage Saved Models */}
        {activeTab === 'manage' && (
          <div className="flex-1 flex flex-col min-h-0 space-y-3 py-2 overflow-y-auto pr-1">
            {isLoadingModels ? (
              <div className="flex flex-col items-center justify-center py-12 text-muted-foreground gap-2">
                <Loader2 className="h-6 w-6 animate-spin text-primary" />
                <span className="text-xs font-mono">Loading models...</span>
              </div>
            ) : savedModels.length === 0 ? (
              <div className="flex flex-col items-center justify-center py-12 text-muted-foreground text-center gap-2 border border-dashed border-border rounded-xl">
                <Box size={32} strokeWidth={1} className="opacity-40" />
                <span className="text-xs font-mono font-medium">No saved face models found</span>
                <p className="text-[11px] text-muted-foreground max-w-xs">
                  Switch to "BUILD MODEL" tab to create your first .safetensors face model.
                </p>
              </div>
            ) : (
              <div className="space-y-2">
                {savedModels.map(m => (
                  <div 
                    key={m.name}
                    className="flex items-center justify-between p-3 rounded-lg bg-secondary/60 border border-border hover:border-primary/50 transition-colors"
                  >
                    <div className="flex items-center gap-3 min-w-0">
                      <div className="w-8 h-8 rounded-md bg-primary/10 text-primary flex items-center justify-center shrink-0 border border-primary/20">
                        <Box size={16} />
                      </div>
                      <div className="flex flex-col min-w-0">
                        <span className="text-xs font-mono font-semibold truncate text-foreground">
                          {m.name}
                        </span>
                        <span className="text-[10px] text-muted-foreground font-mono">
                          .safetensors face model
                        </span>
                      </div>
                    </div>

                    <button
                      onClick={() => handleDeleteModel(m.name)}
                      disabled={deletingModel === m.name}
                      className="shrink-0 h-8 px-2.5 rounded-md bg-destructive/10 text-destructive hover:bg-destructive hover:text-destructive-foreground border border-destructive/20 text-xs font-mono flex items-center gap-1.5 transition-all disabled:opacity-50"
                      title="Delete model file"
                    >
                      {deletingModel === m.name ? (
                        <Loader2 size={13} className="animate-spin" />
                      ) : (
                        <Trash2 size={13} />
                      )}
                      <span>Delete</span>
                    </button>
                  </div>
                ))}
              </div>
            )}
          </div>
        )}

        <DialogFooter className="shrink-0 pt-3 border-t border-border mt-2">
          <Button variant="outline" size="sm" onClick={onClose} disabled={isBuilding}>
            Close
          </Button>
          {activeTab === 'build' && (
            <Button size="sm" onClick={handleBuild} disabled={isBuilding || files.length === 0}>
              {isBuilding ? (
                <><Loader2 className="mr-1.5 h-3.5 w-3.5 animate-spin" /> Building...</>
              ) : (
                'Build Model'
              )}
            </Button>
          )}
        </DialogFooter>
      </DialogContent>
    </Dialog>
  );
}
