import { useState, useEffect, useRef, useCallback } from 'react';
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogDescription, DialogFooter } from '@/components/ui/dialog';
import { Button } from '@/components/ui/button';
import { Slider } from '@/components/ui/slider';
import { Loader2, Undo2, Check, Eye, Layers } from 'lucide-react';
import { toast } from 'sonner';
import { api } from '@/services/api';

interface FaceCleanDialogProps {
  open: boolean;
  onOpenChange: (open: boolean) => void;
  file?: File | null;
  fileId?: string;
  sourcePreviewUrl?: string;
  maskPadding: number[];
  maskBlur?: number[];
  onSave: (padding: number[], blur: number) => void;
}

export function FaceCleanDialog({
  open,
  onOpenChange,
  file,
  fileId,
  sourcePreviewUrl,
  maskPadding: initialMaskPadding,
  maskBlur: initialMaskBlur,
  onSave,
}: FaceCleanDialogProps) {
  // maskPadding: [top, right, bottom, left]
  const [padding, setPadding] = useState<number[]>(initialMaskPadding || [0, 0, 0, 0]);
  const [blur, setBlur] = useState<number>(initialMaskBlur?.[0] ?? 30);
  
  const [viewMode, setViewMode] = useState<'overlay' | 'alpha'>('overlay');
  const [isLoading, setIsLoading] = useState(false);
  const [originalCrop, setOriginalCrop] = useState<string | null>(null);
  const [errorMsg, setErrorMsg] = useState<string | null>(null);

  const alphaCanvasRef = useRef<HTMLCanvasElement | null>(null);

  const drawAlphaCanvas = useCallback(() => {
    const alphaCanvas = alphaCanvasRef.current;
    if (alphaCanvas) {
      const ctx = alphaCanvas.getContext('2d');
      if (ctx) {
        ctx.clearRect(0, 0, 512, 512);
        // Base: Black background (outside face / unswapped)
        ctx.fillStyle = '#000000';
        ctx.fillRect(0, 0, 512, 512);

        // White active face box with 4-way padding applied
        const top = (padding[0] / 100) * 512;
        const bottom = 512 - (padding[2] / 100) * 512;
        const left = (padding[3] / 100) * 512;
        const right = 512 - (padding[1] / 100) * 512;
        const w = Math.max(0, right - left);
        const h = Math.max(0, bottom - top);

        ctx.fillStyle = '#ffffff';
        ctx.fillRect(left, top, w, h);
      }
    }
  }, [padding]);

  useEffect(() => {
    drawAlphaCanvas();
  }, [padding, viewMode, drawAlphaCanvas]);

  useEffect(() => {
    if (open) {
      setPadding(initialMaskPadding && initialMaskPadding.length === 4 ? [...initialMaskPadding] : [0, 0, 0, 0]);
      setBlur(initialMaskBlur?.[0] ?? 30);
      setErrorMsg(null);
      loadPreview();
    }
  }, [open, file, fileId, initialMaskPadding, initialMaskBlur]);

  const loadPreview = async () => {
    if (!file && !fileId) {
      setErrorMsg('No image selected');
      return;
    }

    setIsLoading(true);
    setErrorMsg(null);
    try {
      const res = await api.cleanFacePreview(file || fileId!);
      if (res.success && res.original_crop) {
        setOriginalCrop(res.original_crop);
      } else {
        setErrorMsg(res.error || 'Failed to detect face');
      }
    } catch (e: any) {
      console.error('Boundary preview error:', e);
      setErrorMsg(e.message || 'Error processing preview');
    } finally {
      setIsLoading(false);
    }
  };

  const handleApply = () => {
    onSave(padding, blur);
    toast.success('Face boundary settings saved');
    onOpenChange(false);
  };

  const handleReset = () => {
    setPadding([0, 0, 0, 0]);
    setBlur(30);
    setViewMode('overlay');
  };

  const setPaddingIndex = (index: number, val: number) => {
    setPadding((prev) => {
      const next = [...prev];
      next[index] = val;
      return next;
    });
  };

  const activeImageSrc = originalCrop || sourcePreviewUrl;

  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      <DialogContent className="sm:max-w-[740px] bg-background border-border flex flex-col max-h-[90vh] p-6 overflow-hidden">
        <DialogHeader>
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-2">
              <span className="font-mono text-xs px-2 py-0.5 rounded bg-primary/20 text-primary border border-primary/30">
                VISUAL TUNER
              </span>
              <DialogTitle className="font-mono text-base tracking-wider text-foreground">
                FACE BOUNDARY & PADDING
              </DialogTitle>
            </div>
            <span className="text-[10px] font-mono px-2 py-0.5 rounded border bg-secondary/50 text-muted-foreground border-border">
              4-Way Cutout & Feathering
            </span>
          </div>
          <DialogDescription className="text-xs text-muted-foreground">
            Adjust 4-way mask padding to trim the forehead, chin, or side seams for seamless face blending.
          </DialogDescription>
        </DialogHeader>

        <div className="grid grid-cols-1 md:grid-cols-12 gap-5 mt-2 flex-1 overflow-y-auto">
          {/* Left Column: Visual Canvas & Overlay (5 cols) */}
          <div className="md:col-span-5 flex flex-col items-center gap-3">
            <div className="relative w-full aspect-square rounded-xl overflow-hidden bg-black border border-border flex items-center justify-center group shadow-inner">
              {isLoading ? (
                <div className="flex flex-col items-center gap-2 text-muted-foreground">
                  <Loader2 size={28} className="animate-spin text-primary" />
                  <span className="text-xs font-mono">Preparing face preview...</span>
                </div>
              ) : errorMsg ? (
                <div className="p-4 text-center text-xs text-destructive font-mono">
                  {errorMsg}
                </div>
              ) : viewMode === 'alpha' ? (
                /* Alpha Mask Preview Channel */
                <div className="relative w-full h-full bg-black flex items-center justify-center overflow-hidden">
                  <canvas
                    ref={alphaCanvasRef}
                    width={512}
                    height={512}
                    style={{
                      filter: blur > 0 ? `blur(${(blur / 100) * 12}px)` : undefined,
                    }}
                    className="w-full h-full object-contain select-none transition-[filter] duration-75"
                  />
                  <div className="absolute top-2 left-2 pointer-events-none">
                    <span className="text-[9px] font-mono bg-black/80 text-white/90 border border-white/20 px-1.5 py-0.5 rounded shadow">
                      ALPHA MASK ({blur}% FEATHER)
                    </span>
                  </div>
                  <div className="absolute bottom-2 left-2 pointer-events-none">
                    <span className="text-[9px] font-mono text-muted-foreground bg-black/75 px-1.5 py-0.5 rounded">
                      White = Swapped · Black = Preserved
                    </span>
                  </div>
                </div>
              ) : activeImageSrc ? (
                /* Face + Mask Overlay View */
                <>
                  <img
                    src={activeImageSrc}
                    alt="Face crop"
                    className="w-full h-full object-cover select-none"
                  />

                  {/* Interactive Mask Shading Overlay */}
                  <div className="absolute inset-0 pointer-events-none">
                    {/* Top Mask Cutout Shading */}
                    {padding[0] > 0 && (
                      <div
                        style={{ height: `${padding[0]}%` }}
                        className="absolute top-0 left-0 w-full bg-red-950/60 border-b-2 border-red-500/80 backdrop-blur-[1px] flex items-center justify-center transition-all duration-75"
                      >
                        <span className="text-[10px] font-mono text-red-200 bg-black/70 px-1.5 py-0.5 rounded shadow">
                          TOP {padding[0]}%
                        </span>
                      </div>
                    )}

                    {/* Bottom Mask Cutout Shading */}
                    {padding[2] > 0 && (
                      <div
                        style={{ height: `${padding[2]}%` }}
                        className="absolute bottom-0 left-0 w-full bg-red-950/60 border-t-2 border-red-500/80 backdrop-blur-[1px] flex items-center justify-center transition-all duration-75"
                      >
                        <span className="text-[10px] font-mono text-red-200 bg-black/70 px-1.5 py-0.5 rounded shadow">
                          BOTTOM {padding[2]}%
                        </span>
                      </div>
                    )}

                    {/* Left Mask Cutout Shading */}
                    {padding[3] > 0 && (
                      <div
                        style={{ width: `${padding[3]}%` }}
                        className="absolute top-0 left-0 h-full bg-red-950/60 border-r-2 border-red-500/80 backdrop-blur-[1px] flex items-center justify-center transition-all duration-75"
                      >
                        <span className="text-[9px] font-mono text-red-200 bg-black/70 px-1 py-0.5 rounded rotate-90 shadow">
                          LEFT {padding[3]}%
                        </span>
                      </div>
                    )}

                    {/* Right Mask Cutout Shading */}
                    {padding[1] > 0 && (
                      <div
                        style={{ width: `${padding[1]}%` }}
                        className="absolute top-0 right-0 h-full bg-red-950/60 border-l-2 border-red-500/80 backdrop-blur-[1px] flex items-center justify-center transition-all duration-75"
                      >
                        <span className="text-[9px] font-mono text-red-200 bg-black/70 px-1.5 py-0.5 rounded -rotate-90 shadow">
                          RIGHT {padding[1]}%
                        </span>
                      </div>
                    )}

                    {/* Active Swap Face Bounding Frame */}
                    <div
                      style={{
                        top: `${padding[0]}%`,
                        bottom: `${padding[2]}%`,
                        left: `${padding[3]}%`,
                        right: `${padding[1]}%`,
                      }}
                      className="absolute border border-dashed border-emerald-400/80 rounded-sm pointer-events-none transition-all duration-75 shadow-[0_0_12px_rgba(52,211,153,0.2)]"
                    >
                      <span className="absolute bottom-1 right-1 text-[9px] font-mono text-emerald-400 bg-black/80 px-1 rounded">
                        ACTIVE MASK
                      </span>
                    </div>
                  </div>
                </>
              ) : (
                <span className="text-xs text-muted-foreground font-mono">No preview available</span>
              )}
            </div>

            {/* View Mode Toggle Buttons */}
            <div className="flex w-full bg-secondary/40 border border-border p-0.5 rounded-lg text-xs font-mono">
              <button
                type="button"
                className={`flex-1 py-1 rounded-md transition-colors flex items-center justify-center gap-1.5 ${
                  viewMode === 'overlay'
                    ? 'bg-primary text-primary-foreground font-semibold shadow-sm'
                    : 'text-muted-foreground hover:text-foreground'
                }`}
                onClick={() => setViewMode('overlay')}
              >
                <Eye size={12} /> Face + Overlay
              </button>
              <button
                type="button"
                className={`flex-1 py-1 rounded-md transition-colors flex items-center justify-center gap-1.5 ${
                  viewMode === 'alpha'
                    ? 'bg-primary text-primary-foreground font-semibold shadow-sm'
                    : 'text-muted-foreground hover:text-foreground'
                }`}
                onClick={() => setViewMode('alpha')}
              >
                <Layers size={12} /> Alpha Mask
              </button>
            </div>
          </div>

          {/* Right Column: Interactive Sliders & Boundary Controls (7 cols) */}
          <div className="md:col-span-7 flex flex-col gap-4">
            {/* Feature 1: Mask Feather Blur Slider */}
            <div className="bg-secondary/30 border border-border p-3.5 rounded-xl flex flex-col gap-2">
              <div className="flex items-center justify-between">
                <span className="text-xs font-mono font-medium text-foreground uppercase tracking-wider">
                  Mask Feather Blur
                </span>
                <span className="font-mono text-[11px] text-primary font-semibold">
                  {blur}%
                </span>
              </div>
              <Slider
                value={[blur]}
                min={0}
                max={100}
                step={1}
                onValueChange={([val]) => setBlur(val)}
                className="py-1"
              />
              <span className="text-[10px] text-muted-foreground leading-tight">
                Gaussian feathering applied to mask boundaries for seamless blending with target skin & hairline. (Default: 30%)
              </span>
            </div>

            {/* Feature 2: 4-Way Mask Padding Sliders */}
            <div className="bg-secondary/30 border border-border p-3.5 rounded-xl flex flex-col gap-3.5">
              <div className="flex items-center justify-between border-b border-border/60 pb-2">
                <span className="text-xs font-mono font-medium text-foreground uppercase tracking-wider">
                  4-Way Mask Padding
                </span>
                <span className="text-[10px] text-muted-foreground font-mono">
                  Trims outer boundary
                </span>
              </div>

              {/* Top Padding Slider */}
              <div className="flex flex-col gap-1.5">
                <div className="flex justify-between items-center text-xs">
                  <span className="font-mono text-[11px] text-foreground flex items-center gap-1">
                    ⬆️ Top Padding (Forehead / Hairline)
                  </span>
                  <span className="font-mono text-[11px] text-primary font-semibold">
                    {padding[0]}%
                  </span>
                </div>
                <Slider
                  value={[padding[0]]}
                  min={0}
                  max={40}
                  step={1}
                  onValueChange={([val]) => setPaddingIndex(0, val)}
                  className="py-1"
                />
                <span className="text-[10px] text-muted-foreground leading-tight">
                  Higher values protect target's natural forehead and hairline. Recommended: 10% - 20%.
                </span>
              </div>

              {/* Bottom Padding Slider */}
              <div className="flex flex-col gap-1.5 pt-1">
                <div className="flex justify-between items-center text-xs">
                  <span className="font-mono text-[11px] text-foreground flex items-center gap-1">
                    ⬇️ Bottom Padding (Chin / Jawline)
                  </span>
                  <span className="font-mono text-[11px] text-primary font-semibold">
                    {padding[2]}%
                  </span>
                </div>
                <Slider
                  value={[padding[2]]}
                  min={0}
                  max={30}
                  step={1}
                  onValueChange={([val]) => setPaddingIndex(2, val)}
                  className="py-1"
                />
              </div>

              {/* Left & Right Sliders Grid */}
              <div className="grid grid-cols-2 gap-3 pt-1">
                <div className="flex flex-col gap-1.5">
                  <div className="flex justify-between items-center text-xs">
                    <span className="font-mono text-[11px] text-foreground">⬅️ Left (Cheek)</span>
                    <span className="font-mono text-[11px] text-primary">{padding[3]}%</span>
                  </div>
                  <Slider
                    value={[padding[3]]}
                    min={0}
                    max={30}
                    step={1}
                    onValueChange={([val]) => setPaddingIndex(3, val)}
                    className="py-1"
                  />
                </div>

                <div className="flex flex-col gap-1.5">
                  <div className="flex justify-between items-center text-xs">
                    <span className="font-mono text-[11px] text-foreground">➡️ Right (Cheek)</span>
                    <span className="font-mono text-[11px] text-primary">{padding[1]}%</span>
                  </div>
                  <Slider
                    value={[padding[1]]}
                    min={0}
                    max={30}
                    step={1}
                    onValueChange={([val]) => setPaddingIndex(1, val)}
                    className="py-1"
                  />
                </div>
              </div>

              {/* Quick Presets */}
              <div className="flex items-center gap-2 pt-2 border-t border-border/40">
                <span className="text-[10px] text-muted-foreground font-mono">Presets:</span>
                <button
                  type="button"
                  className="text-[10px] font-mono px-2 py-0.5 rounded bg-secondary hover:bg-secondary/80 text-foreground border border-border"
                  onClick={() => setPadding([0, 0, 0, 0])}
                >
                  Full (0%)
                </button>
                <button
                  type="button"
                  className="text-[10px] font-mono px-2 py-0.5 rounded bg-secondary hover:bg-secondary/80 text-foreground border border-border"
                  onClick={() => setPadding([15, 0, 0, 0])}
                >
                  Top 15% (Hairline Safe)
                </button>
                <button
                  type="button"
                  className="text-[10px] font-mono px-2 py-0.5 rounded bg-secondary hover:bg-secondary/80 text-foreground border border-border"
                  onClick={() => setPadding([25, 0, 0, 0])}
                >
                  Top 25% (Low Forehead)
                </button>
              </div>
            </div>
          </div>
        </div>

        <DialogFooter className="mt-4 pt-3 border-t border-border flex items-center justify-between">
          <Button variant="ghost" size="sm" className="h-8 text-xs font-mono" onClick={handleReset}>
            <Undo2 size={12} className="mr-1" /> Reset Defaults
          </Button>
          <div className="flex items-center gap-2">
            <Button variant="outline" size="sm" className="h-8 text-xs" onClick={() => onOpenChange(false)}>
              Cancel
            </Button>
            <Button variant="default" size="sm" className="h-8 text-xs font-mono bg-primary text-primary-foreground" onClick={handleApply}>
              <Check size={12} className="mr-1" /> Apply & Save
            </Button>
          </div>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  );
}
