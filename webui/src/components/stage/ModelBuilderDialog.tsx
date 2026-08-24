import React, { useState } from 'react';
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogDescription, DialogFooter } from '@/components/ui/dialog';
import { Button } from '@/components/ui/button';
import { Upload, X, Loader2 } from 'lucide-react';

interface ModelBuilderDialogProps {
  open: boolean;
  onClose: () => void;
  apiBase: string;
  platform: string;
  onModelBuilt: () => void;
}

export function ModelBuilderDialog({ open, onClose, apiBase, platform, onModelBuilt }: ModelBuilderDialogProps) {
  const [modelName, setModelName] = useState('');
  const [files, setFiles] = useState<File[]>([]);
  const [isBuilding, setIsBuilding] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files) {
      setFiles(prev => [...prev, ...Array.from(e.target.files!)]);
    }
  };

  const removeFile = (index: number) => {
    setFiles(prev => prev.filter((_, i) => i !== index));
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

      const res = await fetch(`${apiBase}/api/v1/face-models/build`, {
        method: 'POST',
        headers: { 'X-Client-Platform': platform },
        body: formData
      });

      const data = await res.json();
      if (!res.ok) {
        throw new Error(data.detail || "Failed to build model.");
      }

      alert(`Successfully built model '${data.model_name}' with ${data.faces_extracted} faces extracted!`);
      onModelBuilt();
      onClose();
      setModelName('');
      setFiles([]);
    } catch (err: any) {
      setError(err.message);
    } finally {
      setIsBuilding(false);
    }
  };

  return (
    <Dialog open={open} onOpenChange={(val) => !val && onClose()}>
      <DialogContent className="sm:max-w-[500px]">
        <DialogHeader>
          <DialogTitle>Build Face Model</DialogTitle>
          <DialogDescription>
            Upload multiple images of the same person from different angles and expressions to build a high-quality .safetensors model.
          </DialogDescription>
        </DialogHeader>

        <div className="space-y-4 py-4">
          <div className="space-y-2">
            <label className="text-sm font-medium">Model Name</label>
            <input 
              type="text"
              className="flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background file:border-0 file:bg-transparent file:text-sm file:font-medium placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50"
              placeholder="e.g. john_doe" 
              value={modelName} 
              onChange={(e: React.ChangeEvent<HTMLInputElement>) => setModelName(e.target.value)} 
              disabled={isBuilding}
            />
          </div>

          <div className="space-y-2">
            <label className="text-sm font-medium">Training Images ({files.length})</label>
            <div className="border-2 border-dashed border-border rounded-lg p-6 text-center hover:bg-secondary/50 transition-colors">
              <label className="cursor-pointer flex flex-col items-center gap-2">
                <Upload className="h-8 w-8 text-muted-foreground" />
                <span className="text-sm font-medium text-foreground">Click to upload images</span>
                <span className="text-xs text-muted-foreground">Select multiple files (JPG, PNG)</span>
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
            
            {files.length > 0 && (
              <div className="mt-4 max-h-[150px] overflow-y-auto space-y-2 border border-border rounded-md p-2">
                {files.map((file, i) => (
                  <div key={i} className="flex items-center justify-between text-xs bg-secondary px-2 py-1.5 rounded">
                    <span className="truncate max-w-[200px]">{file.name}</span>
                    <button 
                      onClick={() => removeFile(i)} 
                      disabled={isBuilding}
                      className="text-muted-foreground hover:text-destructive"
                    >
                      <X size={14} />
                    </button>
                  </div>
                ))}
              </div>
            )}
          </div>
          
          {error && <div className="text-sm text-destructive font-medium">{error}</div>}
        </div>

        <DialogFooter>
          <Button variant="outline" onClick={onClose} disabled={isBuilding}>Cancel</Button>
          <Button onClick={handleBuild} disabled={isBuilding}>
            {isBuilding ? <><Loader2 className="mr-2 h-4 w-4 animate-spin" /> Building...</> : 'Build Model'}
          </Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  );
}
