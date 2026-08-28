import { useState, useEffect } from 'react';
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogDescription, DialogFooter } from '@/components/ui/dialog';
import { Button } from '@/components/ui/button';
import { Slider } from '@/components/ui/slider';
import { Loader2, User, CheckCircle2 } from 'lucide-react';
import { toast } from 'sonner';

export interface ExtractedFace {
  id: string;
  url: string; // base64 or relative URL
}

interface ReferenceFaceSelectorProps {
  open: boolean;
  onOpenChange: (open: boolean) => void;
  platform: string;
  apiBase: string;
  targetType: "upload" | "set";
  sampleCount: number;
  targetFiles: File[];
  targetSetFiles: string[];
  initialFaces?: ExtractedFace[];
  initialThreshold?: number;
  onConfirm: (faces: ExtractedFace[], threshold: number) => void;
}

export function ReferenceFaceSelector({
  open, onOpenChange, platform, apiBase, targetType, sampleCount, targetFiles, targetSetFiles,
  initialFaces = [], initialThreshold = 0.6, onConfirm
}: ReferenceFaceSelectorProps) {
  
  const [isScanning, setIsScanning] = useState(false);
  const [scannedFaces, setScannedFaces] = useState<ExtractedFace[]>([]);
  const [selectedFaceIds, setSelectedFaceIds] = useState<Set<string>>(new Set());
  const [threshold, setThreshold] = useState<number[]>([initialThreshold]);

  const totalItems = targetType === "upload" ? targetFiles.length : targetSetFiles.length;
  const [scanRange, setScanRange] = useState<number[]>([0, Math.max(1, totalItems)]);

  // Reset or initialize state when modal opens
  useEffect(() => {
    if (open) {
      if (initialFaces && initialFaces.length > 0) {
        setScannedFaces([...initialFaces]);
        setSelectedFaceIds(new Set(initialFaces.map(f => f.id)));
      } else {
        setScannedFaces([]);
        setSelectedFaceIds(new Set());
      }
      setThreshold([initialThreshold]);
      setScanRange([0, Math.max(1, totalItems)]);
    }
  }, [open, totalItems, initialFaces, initialThreshold]);

  const handleScan = async () => {
    // Validate inputs
    if (targetType === "upload" && targetFiles.length === 0) {
      toast.error("No target files selected to scan.");
      return;
    }
    if (targetType === "set" && targetSetFiles.length === 0) {
      toast.error("No target set files selected to scan.");
      return;
    }

    setIsScanning(true);
    setScannedFaces([]);
    setSelectedFaceIds(new Set());

    try {
      const fd = new FormData();
      fd.append('target_type', targetType);
      fd.append('sample_count', sampleCount.toString());
      
      if (targetType === "upload") {
        const slice = targetFiles.slice(scanRange[0], scanRange[1]); 
        const shuffled = [...slice].sort(() => 0.5 - Math.random());
        const filesToScan = shuffled.slice(0, sampleCount);
        filesToScan.forEach(f => fd.append('files', f));
      } else {
        const slice = targetSetFiles.slice(scanRange[0], scanRange[1]);
        const shuffled = [...slice].sort(() => 0.5 - Math.random());
        const filesToScan = shuffled.slice(0, sampleCount);
        filesToScan.forEach(f => fd.append('file_ids', f));
      }

      const res = await fetch(`${apiBase}/api/v1/extract-faces`, {
        method: 'POST',
        headers: { 'X-Client-Platform': platform },
        body: fd
      });

      if (!res.ok) throw new Error(await res.text());
      
      const data = await res.json();
      if (data.faces && data.faces.length > 0) {
        setScannedFaces(data.faces);
      } else {
        toast.info("No faces detected in the target media.");
      }
    } catch (e: any) {
      console.error(e);
      toast.error(e.message || "Failed to scan faces");
    } finally {
      setIsScanning(false);
    }
  };

  const toggleFace = (id: string) => {
    const next = new Set(selectedFaceIds);
    if (next.has(id)) next.delete(id);
    else next.add(id);
    setSelectedFaceIds(next);
  };

  const handleConfirm = () => {
    const selected = scannedFaces.filter(f => selectedFaceIds.has(f.id));
    onConfirm(selected, threshold[0]);
    onOpenChange(false);
  };

  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      <DialogContent className="sm:max-w-[500px] bg-background border-border flex flex-col max-h-[85vh]">
        <DialogHeader>
          <DialogTitle className="font-mono tracking-widest flex items-center gap-2">
            <User size={18} /> SPECIFIC FACE FILTER
          </DialogTitle>
          <DialogDescription className="text-xs">
            Scan target media to find faces, then select exactly who you want to swap.
          </DialogDescription>
        </DialogHeader>

        <div className="flex flex-col gap-4 mt-2 overflow-y-auto">
          
          {!isScanning && scannedFaces.length === 0 && (
            <div className="flex flex-col items-center justify-center p-8 border border-dashed border-border rounded-xl bg-secondary/20">
              <User size={32} className="text-muted-foreground mb-3 opacity-50" />
              <p className="text-xs text-muted-foreground text-center mb-6">
                Click below to scan your selected targets for faces.
              </p>

              {totalItems > sampleCount && (
                <div className="w-full max-w-[250px] mb-6 space-y-2">
                  <div className="flex justify-between items-center mb-2">
                    <label className="text-[10px] text-muted-foreground uppercase tracking-wider font-semibold">Random Scan Range</label>
                    <span className="font-mono text-[10px] text-primary">[{scanRange[0]} - {scanRange[1]}]</span>
                  </div>
                  <Slider
                    value={scanRange}
                    onValueChange={(val) => {
                      if (val.length === 2 && val[1] - val[0] >= Math.min(sampleCount, totalItems)) {
                        setScanRange(val);
                      }
                    }}
                    max={totalItems}
                    min={0}
                    step={1}
                  />
                  <p className="text-[10px] text-muted-foreground/70 text-center leading-tight pt-1">
                    Randomly selects {sampleCount} items from this range.
                  </p>
                </div>
              )}

              <Button onClick={handleScan} className="h-8 text-xs bg-primary/20 text-primary hover:bg-primary/30">
                Start Scanning
              </Button>
            </div>
          )}

          {isScanning && (
            <div className="flex flex-col items-center justify-center p-12 border border-border rounded-xl bg-secondary/10">
              <Loader2 size={32} className="text-primary animate-spin mb-3" />
              <p className="text-sm font-medium animate-pulse">Scanning media...</p>
              <p className="text-xs text-muted-foreground mt-1">Extracting faces from target files</p>
            </div>
          )}

          {!isScanning && scannedFaces.length > 0 && (
            <>
              <div className="flex items-center justify-between">
                <span className="text-xs font-medium">Select Faces ({selectedFaceIds.size} selected)</span>
                <div className="flex gap-2">
                  <Button variant="outline" size="sm" className="h-6 text-[10px]" onClick={() => {
                    setScannedFaces([]);
                    setSelectedFaceIds(new Set());
                  }}>
                    Adjust Scan Range
                  </Button>
                  <Button variant="secondary" size="sm" className="h-6 text-[10px]" onClick={handleScan}>
                    Quick Rescan
                  </Button>
                </div>
              </div>
              
              <div className="grid grid-cols-4 gap-2">
                {scannedFaces.map(face => {
                  const isSelected = selectedFaceIds.has(face.id);
                  return (
                    <div 
                      key={face.id}
                      onClick={() => toggleFace(face.id)}
                      className={`relative aspect-square rounded-lg overflow-hidden cursor-pointer transition-all border-2 ${isSelected ? 'border-primary ring-2 ring-primary/20 shadow-[0_0_15px_rgba(var(--primary),0.3)] scale-95' : 'border-transparent hover:border-border'}`}
                    >
                      <img src={face.url} alt="Face crop" className="w-full h-full object-cover" />
                      {isSelected && (
                        <div className="absolute top-1 right-1 bg-primary text-primary-foreground rounded-full shadow-sm">
                          <CheckCircle2 size={16} />
                        </div>
                      )}
                    </div>
                  );
                })}
              </div>

              <div className="h-px bg-border w-full my-2" />

              <div className="space-y-3">
                <div className="flex justify-between items-center">
                  <label className="text-xs font-medium">Similarity Threshold</label>
                  <span className="font-mono text-xs text-primary">{threshold[0].toFixed(2)}</span>
                </div>
                <Slider 
                  value={threshold} 
                  onValueChange={setThreshold} 
                  max={1.0} min={0.1} step={0.05} 
                />
                <p className="text-[10px] text-muted-foreground leading-relaxed">
                  How strict should the face matching be? <br/>
                  <strong className="text-foreground">0.8 - 1.0:</strong> Very strict, only near-identical angles match.<br/>
                  <strong className="text-foreground">0.4 - 0.6:</strong> Balanced (Recommended).<br/>
                  <strong className="text-foreground">0.1 - 0.3:</strong> Loose, might swap unintended faces.
                </p>
              </div>
            </>
          )}

        </div>

        <DialogFooter className="mt-4 border-t border-border pt-4">
          <Button variant="outline" onClick={() => onOpenChange(false)}>Cancel</Button>
          <Button 
            onClick={handleConfirm}
            disabled={isScanning}
          >
            {scannedFaces.length > 0 && selectedFaceIds.size === 0 ? "Clear Filter (Select 0)" : "Confirm Selection"}
          </Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  );
}
