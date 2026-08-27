import { useState, useRef, useEffect } from 'react';
import { Upload, X, Trash2, Plus, Image as ImageIcon, Video } from 'lucide-react';
import SparkMD5 from 'spark-md5';

import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogDescription } from '@/components/ui/dialog';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { Button } from '@/components/ui/button';

interface TargetFile {
  filename: string;
  file_id: string;
  url: string;
}

interface TargetSet {
  name: string;
  files: TargetFile[];
}

interface TargetSetManagerProps {
  open: boolean;
  platform: string;
  chunkSizeMB: number;
  onOpenChange: (open: boolean) => void;
  onSelectSet: (files: TargetFile[]) => void;
}

export function TargetSetManager({ open, platform, chunkSizeMB, onOpenChange, onSelectSet }: TargetSetManagerProps) {
  const [sets, setSets] = useState<TargetSet[]>([]);
  const [selectedSetName, setSelectedSetName] = useState<string>('');
  
  const [isCreating, setIsCreating] = useState(false);
  const [newSetName, setNewSetName] = useState('');
  
  const [selectedFiles, setSelectedFiles] = useState<Set<string>>(new Set());
  const [isUploading, setIsUploading] = useState(false);
  const [uploadProgress, setUploadProgress] = useState(0);

  const fileInputRef = useRef<HTMLInputElement>(null);

  // Fetch sets when dialog opens
  useEffect(() => {
    if (open) {
      fetchSets();
    }
  }, [open]);

  const fetchSets = async () => {
    try {
      const res = await fetch('/api/v1/target-sets', {
        headers: { 'X-Client-Platform': platform }
      });
      const data = await res.json();
      setSets(data.target_sets || []);
      
      // If we don't have a selection but we have sets, pick the first one
      if (!selectedSetName && data.target_sets && data.target_sets.length > 0) {
        setSelectedSetName(data.target_sets[0].name);
      }
    } catch (e) {
      console.error('Failed to fetch target sets:', e);
    }
  };

  const currentSet = sets.find(s => s.name === selectedSetName);

  const handleUseSet = () => {
    if (currentSet) {
      onSelectSet(currentSet.files);
      onOpenChange(false);
    }
  };

  const handleCreateSet = async () => {
    if (!newSetName.trim()) return;
    const fd = new FormData();
    fd.append('name', newSetName);
    try {
      const res = await fetch('/api/v1/target-sets', { 
        method: 'POST', 
        body: fd,
        headers: { 'X-Client-Platform': platform }
      });
      if (res.ok) {
        const data = await res.json();
        setIsCreating(false);
        setNewSetName('');
        setSelectedSetName(data.name);
        await fetchSets();
      }
    } catch (e) {
      console.error(e);
    }
  };

  const handleDeleteSet = async () => {
    if (!selectedSetName) return;
    if (!confirm(`Are you sure you want to delete set "${selectedSetName}"?`)) return;
    
    try {
      await fetch(`/api/v1/target-sets/${encodeURIComponent(selectedSetName)}`, { 
        method: 'DELETE',
        headers: { 'X-Client-Platform': platform }
      });
      const newSets = sets.filter(s => s.name !== selectedSetName);
      setSets(newSets);
      setSelectedSetName(newSets.length > 0 ? newSets[0].name : '');
    } catch (e) {
      console.error(e);
    }
  };

  const handleDeleteSelectedFiles = async () => {
    if (!selectedSetName || selectedFiles.size === 0) return;
    
    try {
      const res = await fetch(`/api/v1/target-sets/${encodeURIComponent(selectedSetName)}/delete-files`, {
        method: 'POST',
        headers: { 
          'Content-Type': 'application/json',
          'X-Client-Platform': platform 
        },
        body: JSON.stringify({ filenames: Array.from(selectedFiles) })
      });
      if (res.ok) {
        setSelectedFiles(new Set());
        await fetchSets();
      }
    } catch (e) {
      console.error(e);
    }
  };

  const toggleFileSelection = (filename: string) => {
    const next = new Set(selectedFiles);
    if (next.has(filename)) next.delete(filename);
    else next.add(filename);
    setSelectedFiles(next);
  };

  // Chunked Hashing implementation
  const calculateHash = (file: File): Promise<string> => {
    return new Promise((resolve, reject) => {
      const chunkSize = (chunkSizeMB || 100) * 1024 * 1024;
      const chunks = Math.ceil(file.size / chunkSize);
      let currentChunk = 0;
      const spark = new SparkMD5.ArrayBuffer();
      const fileReader = new FileReader();

      fileReader.onload = (e) => {
        if (e.target?.result) {
          spark.append(e.target.result as ArrayBuffer);
        }
        currentChunk++;
        if (currentChunk < chunks) {
          loadNext();
        } else {
          resolve(spark.end());
        }
      };
      fileReader.onerror = () => reject(fileReader.error);

      const loadNext = () => {
        const start = currentChunk * chunkSize;
        const end = Math.min(start + chunkSize, file.size);
        fileReader.readAsArrayBuffer(file.slice(start, end));
      };
      loadNext();
    });
  };

  const handleUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const files = e.target.files;
    if (!files || files.length === 0 || !selectedSetName) return;

    setIsUploading(true);
    setUploadProgress(0);
    
    try {
      // 1. Calculate hashes (dynamic batching based on size limit)
      const fileHashes: { filename: string, hash: string, file: File }[] = [];
      const maxMemoryBytes = (chunkSizeMB || 100) * 1024 * 1024;
      
      let currentBatch: File[] = [];
      let currentBatchMemory = 0;
      let completed = 0;

      const processBatch = async (batch: File[]) => {
        const batchPromises = batch.map(async (file) => {
          const hash = await calculateHash(file);
          return { filename: file.name, hash, file };
        });
        const results = await Promise.all(batchPromises);
        fileHashes.push(...results);
        completed += batch.length;
        setUploadProgress((completed / files.length) * 50);
      };

      for (let i = 0; i < files.length; i++) {
        const file = files[i];
        const footprint = Math.min(file.size, maxMemoryBytes);

        // If adding this file exceeds the memory limit (and batch is not empty), process the batch first
        if (currentBatchMemory + footprint > maxMemoryBytes && currentBatch.length > 0) {
          await processBatch(currentBatch);
          currentBatch = [];
          currentBatchMemory = 0;
        }

        currentBatch.push(file);
        currentBatchMemory += footprint;
      }

      // Process any remaining files in the final batch
      if (currentBatch.length > 0) {
        await processBatch(currentBatch);
      }

      // 2. Preflight check
      setUploadProgress(60);
      const preflightRes = await fetch('/api/v1/target-sets/preflight', {
        method: 'POST',
        headers: { 
          'Content-Type': 'application/json',
          'X-Client-Platform': platform
        },
        body: JSON.stringify({ files: fileHashes.map(f => ({ filename: f.filename, hash: f.hash })) })
      });
      const preflightData = await preflightRes.json();
      
      const exists = preflightData.results.filter((r: any) => r.status === 'exists');
      const newFiles = preflightData.results.filter((r: any) => r.status === 'new');

      // 3. Link existing
      setUploadProgress(70);
      if (exists.length > 0) {
        await fetch(`/api/v1/target-sets/${encodeURIComponent(selectedSetName)}/link`, {
          method: 'POST',
          headers: { 
            'Content-Type': 'application/json',
            'X-Client-Platform': platform
          },
          body: JSON.stringify({ files: exists })
        });
      }

      // 4. Upload new
      setUploadProgress(80);
      if (newFiles.length > 0) {
        const fd = new FormData();
        const hashesStr: string[] = [];
        
        newFiles.forEach((nf: any) => {
          const originalObj = fileHashes.find(f => f.filename === nf.filename);
          if (originalObj) {
            fd.append('files', originalObj.file);
            hashesStr.push(originalObj.hash);
          }
        });
        
        await fetch(`/api/v1/target-sets/${encodeURIComponent(selectedSetName)}/upload`, {
          method: 'POST',
          headers: { 'X-Client-Platform': platform },
          body: fd
        });
      }

      setUploadProgress(100);
      await fetchSets();
      
    } catch (e) {
      console.error('Upload failed:', e);
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
                      
                      {/* Media */}
                      {isVid ? (
                        <video src={file.url} className="w-full h-full object-cover bg-black" />
                      ) : (
                        <img src={file.url} className="w-full h-full object-cover bg-black" alt={file.filename} />
                      )}
                      
                      {isVid && (
                        <div className="absolute bottom-1 left-1 bg-black/60 rounded px-1 text-[10px] text-white flex items-center">
                          <Video size={10} className="mr-1" /> MP4
                        </div>
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
