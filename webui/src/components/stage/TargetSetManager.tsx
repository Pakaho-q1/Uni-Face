import React, { useState, useRef, useEffect, useCallback, useMemo } from 'react';
import { Upload, X, Trash2, Plus, Image as ImageIcon, Video } from 'lucide-react';
import { toast } from 'sonner';
import { useVirtualizer } from '@tanstack/react-virtual';

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

function formatDuration(duration?: number): string {
  if (!duration || isNaN(duration)) return "MP4";
  const minutes = Math.floor(duration / 60);
  const seconds = Math.floor(duration % 60);
  return `${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`;
}

const VideoThumbnail = React.memo(function VideoThumbnail({
  url,
  initialDuration,
}: {
  url: string;
  initialDuration?: number;
}) {
  const [duration, setDuration] = useState<string>(() => formatDuration(initialDuration));

  const handleLoadedMetadata = (e: React.SyntheticEvent<HTMLVideoElement, Event>) => {
    if (initialDuration && !isNaN(initialDuration)) return;
    const video = e.currentTarget;
    if (video.duration && !isNaN(video.duration)) {
      setDuration(formatDuration(video.duration));
    }
  };

  return (
    <>
      <video
        src={url}
        className="w-full h-full object-contain bg-black"
        onLoadedMetadata={handleLoadedMetadata}
        preload="metadata"
      />
      <div className="absolute bottom-1 left-1 bg-black/60 rounded px-1.5 py-0.5 text-[10px] font-mono text-white flex items-center pointer-events-none">
        <Video size={10} className="mr-1 text-blue-400" /> {duration}
      </div>
    </>
  );
});

interface TargetFileCardProps {
  file: TargetFile;
  isSelected: boolean;
  galleryRes?: string;
  onToggle: (filename: string) => void;
}

const TargetFileCard = React.memo(function TargetFileCard({
  file,
  isSelected,
  galleryRes,
  onToggle,
}: TargetFileCardProps) {
  const isVid = file.filename.toLowerCase().endsWith('.mp4');

  return (
    <div
      className={`relative group aspect-square rounded-md overflow-hidden border-2 cursor-pointer transition-colors ${
        isSelected
          ? 'border-primary shadow-[0_0_10px_rgba(var(--primary),0.3)]'
          : 'border-transparent hover:border-muted-foreground/50'
      }`}
      onClick={() => onToggle(file.filename)}
    >
      {/* Checkbox Overlay */}
      <div
        className={`absolute top-2 right-2 z-10 bg-background/80 rounded-sm border transition-opacity ${
          isSelected ? 'border-primary' : 'border-border opacity-0 group-hover:opacity-100'
        }`}
      >
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
            loading="lazy"
          />
          <div className="absolute bottom-1 left-1 bg-black/60 rounded px-1.5 py-0.5 text-[10px] font-mono text-white flex items-center pointer-events-none">
            <ImageIcon size={10} className="mr-1 text-zinc-400" /> IMG
          </div>
        </>
      )}
    </div>
  );
});

export function TargetSetManager({
  open,
  chunkSizeMB,
  galleryRes,
  onOpenChange,
  onSelectSet,
}: TargetSetManagerProps) {
  const [sets, setSets] = useState<TargetSet[]>([]);
  const [selectedSetName, setSelectedSetName] = useState<string>('');

  const [isCreating, setIsCreating] = useState(false);
  const [newSetName, setNewSetName] = useState('');

  const [selectedFiles, setSelectedFiles] = useState<Set<string>>(new Set());
  const [isUploading, setIsUploading] = useState(false);
  const [uploadProgress, setUploadProgress] = useState(0);

  const fileInputRef = useRef<HTMLInputElement>(null);
  const scrollContainerRef = useRef<HTMLDivElement>(null);

  // Responsive Grid Columns
  const [columns, setColumns] = useState(4);
  const [containerWidth, setContainerWidth] = useState(600);

  useEffect(() => {
    const container = scrollContainerRef.current;
    if (!container) return;

    const updateDimensions = () => {
      const width = container.clientWidth;
      if (width > 0) {
        setContainerWidth(width);
        if (width >= 600) setColumns(5);
        else if (width >= 460) setColumns(4);
        else if (width >= 320) setColumns(3);
        else setColumns(2);
      }
    };

    updateDimensions();
    const observer = new ResizeObserver(updateDimensions);
    observer.observe(container);
    return () => observer.disconnect();
  }, [open]);

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

  // Reset scroll and selection when selected set changes
  useEffect(() => {
    if (scrollContainerRef.current) {
      scrollContainerRef.current.scrollTop = 0;
    }
    setSelectedFiles(new Set());
  }, [selectedSetName]);

  const currentSet = sets.find((s) => s.name === selectedSetName);
  const files = useMemo(() => currentSet?.files || [], [currentSet]);
  const rowCount = Math.ceil(files.length / columns);
  const estimatedRowHeight = Math.round(containerWidth / columns + 12);

  const rowVirtualizer = useVirtualizer({
    count: rowCount,
    getScrollElement: () => scrollContainerRef.current,
    estimateSize: () => estimatedRowHeight,
    overscan: 2,
  });

  useEffect(() => {
    rowVirtualizer.measure();
  }, [columns, rowVirtualizer]);

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
      const newSets = sets.filter((s) => s.name !== selectedSetName);
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

  // Stable toggle callback with pure functional update: renders ONLY toggled item
  const toggleFileSelection = useCallback((filename: string) => {
    setSelectedFiles((prev) => {
      const next = new Set(prev);
      if (next.has(filename)) next.delete(filename);
      else next.add(filename);
      return next;
    });
  }, []);

  const handleToggleSelectAll = useCallback(() => {
    if (!currentSet || currentSet.files.length === 0) return;
    setSelectedFiles((prev) => {
      if (prev.size === currentSet.files.length) {
        return new Set();
      }
      return new Set(currentSet.files.map((f) => f.filename));
    });
  }, [currentSet]);

  const handleUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const uploadedFiles = e.target.files;
    if (!uploadedFiles || uploadedFiles.length === 0 || !selectedSetName) return;

    setIsUploading(true);
    setUploadProgress(0);

    try {
      await uploadFilesToTargetSet(selectedSetName, uploadedFiles, chunkSizeMB, setUploadProgress);
      toast.success(`Uploaded ${uploadedFiles.length} file(s) to "${selectedSetName}"`);
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
      const subset = currentSet.files.filter((f) => selectedFiles.has(f.filename));
      onSelectSet(subset);
      onOpenChange(false);
    }
  };

  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      <DialogContent className="sm:max-w-[720px] bg-background border-border flex flex-col max-h-[85vh]">
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
                onChange={(e) => setNewSetName(e.target.value)}
                onKeyDown={(e) => e.key === 'Enter' && handleCreateSet()}
              />
            ) : (
              <Select value={selectedSetName} onValueChange={setSelectedSetName}>
                <SelectTrigger className="flex-1 h-9 bg-secondary/50 border-border">
                  <SelectValue placeholder="Select a target set..." />
                </SelectTrigger>
                <SelectContent>
                  {sets.map((s) => (
                    <SelectItem key={s.name} value={s.name}>
                      {s.name} ({s.files.length})
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>
            )}

            {isCreating ? (
              <>
                <Button variant="default" size="sm" className="h-9" onClick={handleCreateSet}>
                  Create
                </Button>
                <Button variant="ghost" size="icon" className="h-9 w-9" onClick={() => setIsCreating(false)}>
                  <X size={16} />
                </Button>
              </>
            ) : (
              <>
                <Button
                  variant="outline"
                  size="icon"
                  className="h-9 w-9 shrink-0"
                  onClick={() => setIsCreating(true)}
                  title="Create New Set"
                >
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
              {isUploading ? (
                `Processing ${Math.round(uploadProgress)}%`
              ) : (
                <>
                  <Upload size={16} className="mr-2" /> Upload
                </>
              )}
            </Button>
            <input type="file" multiple hidden ref={fileInputRef} onChange={handleUpload} accept="image/*,video/*" />
          </div>

          {/* Gallery Header */}
          <div className="flex items-center justify-between mt-1">
            <span className="text-xs font-mono tracking-wider text-muted-foreground uppercase">
              Gallery {currentSet && currentSet.files.length > 0 && `(${currentSet.files.length} items)`}
            </span>
            <div className="flex items-center gap-2">
              {currentSet && currentSet.files.length > 0 && (
                <Button
                  variant="ghost"
                  size="sm"
                  className="h-7 text-xs text-muted-foreground hover:text-foreground"
                  onClick={handleToggleSelectAll}
                >
                  {selectedFiles.size === currentSet.files.length ? 'Deselect All' : 'Select All'}
                </Button>
              )}
              {selectedFiles.size > 0 && (
                <>
                  <Button
                    variant="default"
                    size="sm"
                    className="h-7 text-xs bg-primary/20 text-primary hover:bg-primary/30"
                    onClick={handleUseSelectedFiles}
                  >
                    Use {selectedFiles.size} Item(s)
                  </Button>
                  <Button
                    variant="destructive"
                    size="sm"
                    className="h-7 text-xs"
                    onClick={handleDeleteSelectedFiles}
                  >
                    Delete {selectedFiles.size} Item(s)
                  </Button>
                </>
              )}
            </div>
          </div>

          {/* Virtualized Gallery Grid */}
          <div
            ref={scrollContainerRef}
            className="flex-1 overflow-y-auto min-h-[320px] max-h-[50vh] border border-border rounded-lg bg-black/50 p-3"
          >
            {!currentSet ? (
              <div className="w-full h-full flex items-center justify-center text-muted-foreground text-sm py-16">
                No set selected
              </div>
            ) : files.length === 0 ? (
              <div className="w-full h-full flex flex-col items-center justify-center text-muted-foreground text-sm opacity-50 py-16">
                <ImageIcon size={32} className="mb-2" />
                This set is empty. Upload some files!
              </div>
            ) : (
              <div
                style={{
                  height: `${rowVirtualizer.getTotalSize()}px`,
                  width: '100%',
                  position: 'relative',
                }}
              >
                {rowVirtualizer.getVirtualItems().map((virtualRow) => {
                  const startIndex = virtualRow.index * columns;
                  const rowFiles = files.slice(startIndex, startIndex + columns);

                  return (
                    <div
                      key={virtualRow.key}
                      data-index={virtualRow.index}
                      ref={rowVirtualizer.measureElement}
                      style={{
                        position: 'absolute',
                        top: 0,
                        left: 0,
                        width: '100%',
                        transform: `translateY(${virtualRow.start}px)`,
                        display: 'grid',
                        gridTemplateColumns: `repeat(${columns}, minmax(0, 1fr))`,
                        gap: '0.75rem',
                        paddingBottom: '0.75rem',
                      }}
                    >
                      {rowFiles.map((file) => (
                        <TargetFileCard
                          key={file.filename}
                          file={file}
                          isSelected={selectedFiles.has(file.filename)}
                          galleryRes={galleryRes}
                          onToggle={toggleFileSelection}
                        />
                      ))}
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
