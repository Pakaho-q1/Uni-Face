import { X } from 'lucide-react';
import { Slider } from '@/components/ui/slider';
import { Switch } from '@/components/ui/switch';
import { Checkbox } from '@/components/ui/checkbox';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { useStickyState } from '@/hooks/useStickyState';

interface SettingsPanelProps {
  open: boolean;
  onClose: () => void;
  settings: ReturnType<typeof useSettings>;
}

export function useSettings() {
  const [executionProvider, setExecutionProvider] = useStickyState('cpu', 'setting_executionProvider');
  const [executionThreadCount, setExecutionThreadCount] = useStickyState([4], 'setting_executionThreadCount');
  const [swapModel, setSwapModel] = useStickyState('inswapper_128', 'setting_swapModel');
  const [swapWeight, setSwapWeight] = useStickyState([65], 'setting_swapWeight');
  const [restoreModel, setRestoreModel] = useStickyState('gfpgan_1.4', 'setting_restoreModel');
  const [restoreWeight, setRestoreWeight] = useStickyState([100], 'setting_restoreWeight');
  const [restoreBlend, setRestoreBlend] = useStickyState([100], 'setting_restoreBlend');
  const [faceRestore, setFaceRestore] = useStickyState(true, 'setting_faceRestore');
  const [colorMatch, setColorMatch] = useStickyState(false, 'setting_colorMatch');
  const [similarity, setSimilarity] = useStickyState(false, 'setting_similarity');
  const [previewFreq, setPreviewFreq] = useStickyState([15], 'setting_previewFreq');
  const [previewRes, setPreviewRes] = useStickyState('320', 'setting_previewRes');
  const [maskTypes, setMaskTypes] = useStickyState<string[]>(['box'], 'setting_maskTypes');
  const [maskRegions, setMaskRegions] = useStickyState<string[]>(['skin', 'l_brow', 'r_brow', 'l_eye', 'r_eye', 'nose', 'mouth', 'u_lip', 'l_lip'], 'setting_maskRegions');
  const [skipExisting, setSkipExisting] = useStickyState(true, 'setting_skipExisting');
  const [hashChunkSize, setHashChunkSize] = useStickyState([100], 'setting_hashChunkSize');

  return {
    executionProvider, setExecutionProvider,
    executionThreadCount, setExecutionThreadCount,
    swapModel, setSwapModel,
    swapWeight, setSwapWeight,
    restoreModel, setRestoreModel,
    restoreWeight, setRestoreWeight,
    restoreBlend, setRestoreBlend,
    faceRestore, setFaceRestore,
    colorMatch, setColorMatch,
    similarity, setSimilarity,
    previewFreq, setPreviewFreq,
    previewRes, setPreviewRes,
    maskTypes, setMaskTypes,
    maskRegions, setMaskRegions,
    skipExisting, setSkipExisting,
    hashChunkSize, setHashChunkSize
  };
}

export function SettingsPanel({ open, onClose, settings }: SettingsPanelProps) {
  return (
    <aside className={`absolute md:relative right-0 top-0 bottom-0 z-[60] md:z-10 shrink-0 h-full bg-card transition-all duration-300 overflow-hidden ${open ? 'w-[85vw] max-w-[300px] md:w-[300px] border-l border-border shadow-2xl md:shadow-none' : 'w-0 border-none'}`}>
      <div className="w-[85vw] max-w-[300px] md:w-[300px] h-full flex flex-col relative">
        <div className="h-14 shrink-0 flex items-center justify-between px-4 border-b border-border font-mono text-[11px] tracking-widest text-muted-foreground whitespace-nowrap">
          SETTINGS
          <button className="p-1 hover:text-foreground transition-colors" onClick={onClose}><X size={16}/></button>
        </div>
      
      <div className="flex-1 overflow-y-auto p-4 space-y-6">
        
        {/* Basic Config */}
        <div className="space-y-4">
          <div className="space-y-2">
            <label className="flex justify-between text-xs text-muted-foreground">Execution Provider</label>
            <Select value={settings.executionProvider} onValueChange={settings.setExecutionProvider}>
              <SelectTrigger className="w-full h-9 text-xs bg-secondary border-border">
                <SelectValue placeholder="Select Provider" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="cpu">CPU (Slow)</SelectItem>
                <SelectItem value="cuda">CUDA (Nvidia GPU)</SelectItem>
                <SelectItem value="trt">TensorRT (Fastest)</SelectItem>
              </SelectContent>
            </Select>
          </div>

          <div className="space-y-2">
            <label className="flex justify-between text-xs text-muted-foreground">
              Thread Count <span className="font-mono text-primary">{settings.executionThreadCount[0]}</span>
            </label>
            <Slider value={settings.executionThreadCount} onValueChange={settings.setExecutionThreadCount} max={32} min={1} step={1} />
          </div>

          <div className="space-y-2">
            <label className="flex justify-between text-xs text-muted-foreground">
              Hash Chunk Size (MB) <span className="font-mono text-primary">{settings.hashChunkSize[0]}MB</span>
            </label>
            <Slider value={settings.hashChunkSize} onValueChange={settings.setHashChunkSize} max={500} min={5} step={5} />
          </div>

          <div className="space-y-2">
            <label className="flex justify-between text-xs text-muted-foreground">Swap Model</label>
            <Select value={settings.swapModel} onValueChange={settings.setSwapModel}>
              <SelectTrigger className="w-full h-9 text-xs bg-secondary border-border">
                <SelectValue placeholder="Select swap model" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="inswapper_128">inswapper_128</SelectItem>
                <SelectItem value="inswapper_128_fp16">inswapper_128_fp16</SelectItem>
                <SelectItem value="hyperswap_1b_256">hyperswap_1b_256</SelectItem>
                <SelectItem value="hyperswap_1c_256">hyperswap_1c_256</SelectItem>
              </SelectContent>
            </Select>
          </div>
          
          <div className="space-y-2">
            <label className="flex justify-between text-xs text-muted-foreground">
              Swap Weight <span className="font-mono text-primary">{settings.swapWeight[0]}%</span>
            </label>
            <Slider value={settings.swapWeight} onValueChange={settings.setSwapWeight} max={100} step={1} />
          </div>
        </div>

        <div className="h-px bg-border w-full" />

        {/* Restore Config */}
        <div className="space-y-4">
          <div className="space-y-2">
            <label className="flex justify-between text-xs text-muted-foreground">Restore Model</label>
            <Select value={settings.restoreModel} onValueChange={settings.setRestoreModel}>
              <SelectTrigger className="w-full h-9 text-xs bg-secondary border-border">
                <SelectValue placeholder="Select restore model" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="gfpgan_1.4">gfpgan_1.4</SelectItem>
                <SelectItem value="codeformer">codeformer</SelectItem>
                <SelectItem value="gpen_bfr_256">gpen_bfr_256</SelectItem>
                <SelectItem value="gpen_bfr_512">gpen_bfr_512</SelectItem>
                <SelectItem value="gpen_bfr_1024">gpen_bfr_1024</SelectItem>
                <SelectItem value="restoreformer_plus_plus">restoreformer_plus_plus</SelectItem>
              </SelectContent>
            </Select>
          </div>
          
          <div className="space-y-2">
            <label className="flex justify-between text-xs text-muted-foreground">
              Restore Weight <span className="font-mono text-primary">{settings.restoreWeight[0]}%</span>
            </label>
            <Slider value={settings.restoreWeight} onValueChange={settings.setRestoreWeight} max={100} step={1} />
          </div>
          
          <div className="space-y-2">
            <label className="flex justify-between text-xs text-muted-foreground">
              Restore Blend <span className="font-mono text-primary">{settings.restoreBlend[0]}%</span>
            </label>
            <Slider value={settings.restoreBlend} onValueChange={settings.setRestoreBlend} max={100} step={1} />
          </div>
        </div>

        <div className="h-px bg-border w-full" />

        {/* Mask Settings */}
        <div className="space-y-4">
          <label className="flex justify-between text-xs text-muted-foreground">Masking Types</label>
          <div className="space-y-3">
            {[
              { id: 'box', label: 'Box (Default)' },
              { id: 'occlusion', label: 'Occlusion (Hands, Hair)' },
              { id: 'region', label: 'Face Region Only' },
              { id: 'eyes', label: 'Priority Eyes (Force)' }
            ].map(mask => (
              <div key={mask.id} className="flex items-center space-x-2">
                <Checkbox 
                  id={`mask-${mask.id}`} 
                  checked={settings.maskTypes.includes(mask.id)}
                  onCheckedChange={(checked) => {
                    if (checked) {
                      settings.setMaskTypes([...settings.maskTypes, mask.id]);
                    } else {
                      const newMasks = settings.maskTypes.filter(m => m !== mask.id);
                      settings.setMaskTypes(newMasks.length > 0 ? newMasks : ['box']);
                    }
                  }}
                />
                <label htmlFor={`mask-${mask.id}`} className="text-xs leading-none peer-disabled:cursor-not-allowed peer-disabled:opacity-70">
                  {mask.label}
                </label>
              </div>
            ))}
          </div>

          {settings.maskTypes.includes('region') && (
            <div className="pl-6 space-y-2 mt-2 border-l border-border/50">
              <label className="text-[10px] text-muted-foreground">Select Regions</label>
              <div className="grid grid-cols-2 gap-2">
                {[
                  { id: 'skin', label: 'Skin' },
                  { id: 'l_brow', label: 'Left Brow' },
                  { id: 'r_brow', label: 'Right Brow' },
                  { id: 'l_eye', label: 'Left Eye' },
                  { id: 'r_eye', label: 'Right Eye' },
                  { id: 'nose', label: 'Nose' },
                  { id: 'mouth', label: 'Mouth' },
                  { id: 'u_lip', label: 'Upper Lip' },
                  { id: 'l_lip', label: 'Lower Lip' }
                ].map(region => (
                  <div key={region.id} className="flex items-center space-x-2">
                    <Checkbox 
                      id={`region-${region.id}`} 
                      checked={settings.maskRegions.includes(region.id)}
                      onCheckedChange={(checked) => {
                        if (checked) {
                          settings.setMaskRegions([...settings.maskRegions, region.id]);
                        } else {
                          settings.setMaskRegions(settings.maskRegions.filter(r => r !== region.id));
                        }
                      }}
                    />
                    <label htmlFor={`region-${region.id}`} className="text-[10px] leading-none text-muted-foreground">
                      {region.label}
                    </label>
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>
        
        <div className="h-px bg-border w-full" />

        {/* Toggles */}
        <div className="space-y-4">
          <div className="flex items-center justify-between">
            <label className="text-xs text-muted-foreground">Face Restore</label>
            <Switch checked={settings.faceRestore} onCheckedChange={settings.setFaceRestore} />
          </div>
          <div className="flex items-center justify-between">
            <label className="text-xs text-muted-foreground">Color Match</label>
            <Switch checked={settings.colorMatch} onCheckedChange={settings.setColorMatch} />
          </div>
          <div className="flex items-center justify-between">
            <label className="text-xs text-muted-foreground">Similarity Check</label>
            <Switch checked={settings.similarity} onCheckedChange={settings.setSimilarity} />
          </div>
          <div className="flex items-center justify-between">
            <label className="text-xs text-muted-foreground">Skip Existing / Overwrite (Retry System)</label>
            <Switch checked={settings.skipExisting} onCheckedChange={settings.setSkipExisting} />
          </div>
        </div>

        <div className="h-px bg-border w-full" />
        
        <div className="space-y-2">
          <label className="flex justify-between text-xs text-muted-foreground">
            Preview Frame Every <span className="font-mono text-primary">{settings.previewFreq[0]}</span>
          </label>
          <Slider value={settings.previewFreq} onValueChange={settings.setPreviewFreq} max={60} min={1} step={1} />
        </div>
        
        <div className="space-y-2">
          <label className="text-xs text-muted-foreground">Preview Resolution</label>
          <Select value={settings.previewRes} onValueChange={settings.setPreviewRes}>
            <SelectTrigger className="w-full text-xs h-8">
              <SelectValue placeholder="Select resolution" />
            </SelectTrigger>
            <SelectContent>
              <SelectItem value="320">320p (Fastest)</SelectItem>
              <SelectItem value="480">480p</SelectItem>
              <SelectItem value="720">720p (High Quality)</SelectItem>
            </SelectContent>
          </Select>
        </div>

        <p className="text-[11px] text-muted-foreground pt-4 leading-relaxed">
          All settings are saved automatically to your browser.
        </p>

        {/* Spacer for bottom bar */}
        <div className="h-20" />
      </div>
      </div>
    </aside>
  );
}
