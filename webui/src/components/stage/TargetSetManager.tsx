import { useState, useRef, useEffect, useCallback } from 'react';
import { Upload, X, Trash2, Plus, Image as ImageIcon, Video } from 'lucide-react';
import { toast } from 'sonner';

import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogDescription } from '@/components/ui/dialog';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { Button } from '@/components/ui/button';
import { api } from '@/services/api';
import { uploadFilesToTargetSet } from '@/services/hashService';
import type { TargetFile, TargetSet } from '@/types';

interface TargetSetManagerProps {
  open: boolean;
  chunkSizeMB: number;
  galleryRes?: string;
  onOpenChange: (open: boolean) => void;
  onSelectSet: (files: TargetFile[]) => void;
}

function VideoThumbnail({ url, initialDuration }: { url: string; initialDuration?: number }) {
  const [duration, setDuration] = useState<string>("MP4");
  const [needsMetadata, setNeedsMetadata] = useState<boolean>(!initialDuration);

  useEffect(() => {
    if (initialDuration && !isNaN(initialDuration)) {
      const minutes = Math.floor(initialDuration / 60);
      const seconds = Math.floor(initialDuration % 60);
      setDuration(`${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`);
      setNeedsMetadata(false);
    }
  }, [initialDuration]);

  const handleLoadedMetadata = (e: React.SyntheticEvent<HTMLVideoElement, Event>) => {
    if (!needsMetadata) return;
    const video = e.currentTarget;
    if (video.duration && !isNaN(video.duration)) {
      const minutes = Math.floor(video.duration / 60);
      const seconds = Math.floor(video.duration % 60);
      setDuration(`${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`);
    }
  };

  return (
    <>
      <video src={url} className="w-full h-full object-contain bg-black" onLoadedMetadata={handleLoadedMetadata} preload="metadata" />
      <div className="absolute bottom-1 left-1 bg-black/60 rounded px-1.5 py-0.5 text-[10px] font-mono text-white flex items-center">
        <Video size={10} className="mr-1" /> {duration}
      </div>
    </>
  );
}

export function TargetSetManager({ open, chunkSizeMB, galleryRes, onOpenChange, onSelectSet }: TargetSetManagerProps) {
  const [sets, setSets] = useState<TargetSet[]>([]);
  const [selectedSetName, setSelectedSetName] = useState<string>('');
  
  const [isCreating, setIsCreating] = useState(false);
  const [newSetName, setNewSetName] = useState('');
  
  const [selectedFiles, setSelectedFiles] = useState<Set<string>>(new Set());
  const [isUploading, setIsUploading] = useState(false);
  const [uploadProgress, setUploadProgress] = useState(0);

  const fileInputRef = useRef<HTMLInputElement>(null);

  const fetchSets = useCallback(async () => {
    try {
      const data = await api.getTargetSets();
      setSets(data.target_sets || []);
      
      if (!selectedSetName && data.target_sets && data.target_sets.length > 0) {
        setSelectedSetName(data.target_sets[0].name);
      }
    } catch (e) {
      console.error('Failed to fetch target sets:', e);
      toast.error('Failed to load target sets');
    }
  }, [selectedSetName]);

  useEffect(() => {
    if (open) {
      fetchSets();
    }
  }, [open, fetchSets]);

  const currentSet = sets.find(s => s.name === selectedSetName);

  const handleUseSet = () => {
    if (currentSet) {
      onSelectSet(currentSet.files);
      onOpenChange(false);
    }
  };

  const handleCreateSet = async () => {
    if (!newSetName.trim()) return;
    try {
      const data = await api.createTargetSet(newSetName.trim());
      setIsCreating(false);
      setNewSetName('');
      setSelectedSetName(data.name);
      toast.success(`Created target set "${data.name}"`);
      await fetchSets();
    } catch (e: any) {
      toast.error(e.message || 'Failed to create target set');
    }
  };

  const handleDeleteSet = async () => {
    if (!selectedSetName) return;
    if (!window.confirm(`Are you sure you want to delete set "${selectedSetName}"?`)) return;
    
    try {
      await api.deleteTargetSet(selectedSetName);
      const newSets = sets.filter(s => s.name !== selectedSetName);
      setSets(newSets);
      setSelectedSetName(newSets.length > 0 ? newSets[0].name : '');
      toast.success(`Deleted target set "${selectedSetName}"`);
    } catch (e: any) {
      toast.error(e.message || 'Failed to delete target set');
    }
  };

  const handleDeleteSelectedFiles = async () => {
    if (!selectedSetName || selectedFiles.size === 0) return;
    
    try {
      await api.deleteTargetSetFiles(selectedSetName, Array.from(selectedFiles));
      toast.success(`Deleted ${selectedFiles.size} file(s) from set`);
      setSelectedFiles(new Set());
      await fetchSets();
    } catch (e: any) {
      toast.error(e.message || 'Failed to delete files');
    }
  };

  const toggleFileSelection = (filename: string) => {
    const next = new Set(selectedFiles);
    if (next.has(filename)) next.delete(filename);
    else next.add(filename);
    setSelectedFiles(next);
  };

  const handleUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const files = e.target.files;
    if (!files || files.length === 0 || !selectedSetName) return;

    setIsUploading(true);
    setUploadProgress(0);
    
    try {
      await uploadFilesToTargetSet(selectedSetName, files, chunkSizeMB, setUploadProgress);
      toast.success(`Uploaded ${files.length} file(s) to "${selectedSetName}"`);
      await fetchSets();
    } catch (e: any) {
      console.error('Upload failed:', e);
      toast.error('Upload failed', { description: e.message });
    } finally {
      setIsUploading(false);
      setUploadProgress(0);
      if (fileInputRef.current) fileInputRef.current.value = '';
    }
  };

  const handleUseSelectedFiles = () => {
    if (currentSet && selectedFiles.size > 0) {
      const subset = currentSet.files.filter(f => selectedFiles.has(f.filename));
      onSelectSet(subset);
      onOpenChange(false);
    }
  };

  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      <DialogContent className="sm:max-w-[700px] bg-background border-border flex flex-col max-h-[85vh]">
        <DialogHeader>
          <DialogTitle className="font-mono tracking-widest">TARGET SET BUILDER</DialogTitle>
          <DialogDescription className="text-xs">
            Manage your persistent target sets, templates, and galleries here.
          </DialogDescription>
        </DialogHeader>

        <div className="flex flex-col gap-4 mt-2 overflow-hidden">
          
          {/* Top Control Bar: Select / Create / Delete */}
          <div className="flex items-center gap-2 shrink-0">
            {isCreating ? (
              <input
                type="text"
                autoFocus
                placeholder="Enter new set name..."
                className="flex-1 h-9 bg-secondary/50 border border-border rounded-md px-3 text-sm focus:outline-none focus:ring-1 focus:ring-primary"
                value={newSetName}
                onChange={e => setNewSetName(e.target.value)}
                onKeyDown={e => e.key === 'Enter' && handleCreateSet()}
              />
            ) : (
              <Select value={selectedSetName} onValueChange={setSelectedSetName}>
                <SelectTrigger className="flex-1 h-9 bg-secondary/50 border-border">
                  <SelectValue placeholder="Select a target set..." />
                </SelectTrigger>
                <SelectContent>
                  {sets.map(s => (
                    <SelectItem key={s.name} value={s.name}>{s.name} ({s.files.length})</SelectItem>
                  ))}
                </SelectContent>
              </Select>
            )}

            {isCreating ? (
              <>
                <Button variant="default" size="sm" className="h-9" onClick={handleCreateSet}>Create</Button>
                <Button variant="ghost" size="icon" className="h-9 w-9" onClick={() => setIsCreating(false)}><X size={16} /></Button>
              </>
            ) : (
              <>
                <Button variant="outline" size="icon" className="h-9 w-9 shrink-0" onClick={() => setIsCreating(true)} title="Create New Set">
                  <Plus size={16} />
                </Button>
                <Button 
                  variant="destructive" 
                  size="icon" 
                  className="h-9 w-9 shrink-0" 
                  onClick={handleDeleteSet} 
                  disabled={!selectedSetName}
                  title="Delete Entire Set"
                >
                  <Trash2 size={16} />
                </Button>
                <Button 
                  variant="default" 
                  className="h-9 shrink-0 bg-primary/20 text-primary hover:bg-primary/30" 
                  onClick={handleUseSet} 
                  disabled={!currentSet || currentSet.files.length === 0}
                >
                  USE ENTIRE SET
                </Button>
              </>
            )}
          </div>

          {/* Upload Area */}
          <div className="shrink-0 flex items-center justify-between bg-secondary/30 border border-border rounded-lg p-3">
            <div className="flex flex-col">
              <span className="text-sm font-medium">Upload Files to Set</span>
              <span className="text-xs text-muted-foreground">Select one or more images/videos.</span>
            </div>
            <Button 
              variant="secondary" 
              onClick={() => fileInputRef.current?.click()}
              disabled={!selectedSetName || isCreating || isUploading}
            >
              {isUploading ? `Processing ${Math.round(uploadProgress)}%` : <><Upload size={16} className="mr-2" /> Upload</>}
            </Button>
            <input type="file" multiple hidden ref={fileInputRef} onChange={handleUpload} accept="image/*,video/*" />
          </div>

          {/* Gallery Area */}
          <div className="flex items-center justify-between mt-2">
            <span className="text-sm font-medium">Gallery</span>
            {selectedFiles.size > 0 && (
              <div className="flex items-center gap-2">
                <Button variant="default" size="sm" className="h-7 text-xs bg-primary/20 text-primary hover:bg-primary/30" onClick={handleUseSelectedFiles}>
                  Use {selectedFiles.size} Item(s)
                </Button>
                <Button variant="destructive" size="sm" className="h-7 text-xs" onClick={handleDeleteSelectedFiles}>
                  Delete {selectedFiles.size} Item(s)
                </Button>
              </div>
            )}
          </div>
          
          <div className="flex-1 overflow-y-auto min-h-[300px] border border-border rounded-lg bg-black/50 p-4">
            {!currentSet ? (
              <div className="w-full h-full flex items-center justify-center text-muted-foreground text-sm">
                No set selected
              </div>
            ) : currentSet.files.length === 0 ? (
              <div className="w-full h-full flex flex-col items-center justify-center text-muted-foreground text-sm opacity-50">
                <ImageIcon size={32} className="mb-2" />
                This set is empty. Upload some files!
              </div>
            ) : (
              <div className="grid grid-cols-3 sm:grid-cols-4 md:grid-cols-5 gap-3">
                {currentSet.files.map((file) => {
                  const isVid = file.filename.toLowerCase().endsWith('.mp4');
                  const isSelected = selectedFiles.has(file.filename);
                  return (
                    <div 
                      key={file.filename} 
                      className={`relative group aspect-square rounded-md overflow-hidden border-2 cursor-pointer transition-colors ${isSelected ? 'border-primary' : 'border-transparent hover:border-muted-foreground/50'}`}
                      onClick={() => toggleFileSelection(file.filename)}
                    >
                      {/* Checkbox Overlay */}
                      <div className={`absolute top-2 right-2 z-10 bg-background/80 rounded-sm border ${isSelected ? 'border-primary' : 'border-border opacity-0 group-hover:opacity-100'}`}>
                        <div className="w-4 h-4 flex items-center justify-center">
                          {isSelected && <div className="w-2 h-2 bg-primary rounded-sm" />}
                        </div>
                      </div>
                      
                      {isVid ? (
                        <VideoThumbnail url={file.url} initialDuration={file.duration} />
                      ) : (
                        <>
                          <img 
                            src={`${file.url}&res=${galleryRes || '384'}`} 
                            className="w-full h-full object-contain bg-black" 
                            alt={file.filename} 
                          />
                          <div className="absolute bottom-1 left-1 bg-black/60 rounded px-1.5 py-0.5 text-[10px] font-mono text-white flex items-center">
                            <ImageIcon size={10} className="mr-1" /> IMG
                          </div>
                        </>
                      )}
                    </div>
                  );
                })}
              </div>
            )}
          </div>

        </div>
      </DialogContent>
    </Dialog>
  );
}
