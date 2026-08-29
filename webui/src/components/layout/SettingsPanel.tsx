import { useState, useEffect, useCallback } from 'react';
import { X } from 'lucide-react';
import { toast } from 'sonner';
import { Slider } from '@/components/ui/slider';
import { Switch } from '@/components/ui/switch';
import { Checkbox } from '@/components/ui/checkbox';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { ImmichExportConfig } from '@/components/shared/ImmichExportConfig';
import { api } from '@/services/api';
import { 
  SWAP_MODELS, 
  RESTORE_MODELS, 
  EXECUTION_PROVIDERS, 
  MASK_TYPES, 
  MASK_REGIONS, 
  OCCLUSION_MODELS,
  PREVIEW_RESOLUTIONS,
  GALLERY_RESOLUTIONS 
} from '@/config';
import type { SettingsState } from '@/types';

interface SettingsPanelProps {
  open: boolean;
  onClose: () => void;
  settings: SettingsState;
}

export function SettingsPanel({ open, onClose, settings }: SettingsPanelProps) {
  const [isConnecting, setIsConnecting] = useState(false);
  const [isConnected, setIsConnected] = useState(false);

  const testImmichConnection = useCallback(async (showToast = false) => {
    if (!settings.immichUrl || !settings.immichApiKey) return;
    setIsConnecting(true);
    try {
      const data = await api.testImmich(settings.immichUrl, settings.immichApiKey);
      setIsConnected(data.success);
      if (showToast) {
        if (data.success) toast.success(data.message || "Connected to Immich successfully");
        else toast.error(data.message || "Failed to connect to Immich");
      }
    } catch (e: any) {
      setIsConnected(false);
      if (showToast) toast.error(e.message || "Connection failed");
    } finally {
      setIsConnecting(false);
    }
  }, [settings.immichUrl, settings.immichApiKey]);

  // Auto-connect on mount if we have credentials
  useEffect(() => {
    if (settings.immichUrl && settings.immichApiKey) {
      testImmichConnection(false);
    }
  }, [settings.immichUrl, settings.immichApiKey, testImmichConnection]);

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
                {EXECUTION_PROVIDERS.map(p => (
                  <SelectItem key={p.id} value={p.id}>{p.label}</SelectItem>
                ))}
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
                {SWAP_MODELS.map(m => (
                  <SelectItem key={m.id} value={m.id}>{m.label}</SelectItem>
                ))}
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
                {RESTORE_MODELS.map(m => (
                  <SelectItem key={m.id} value={m.id}>{m.label}</SelectItem>
                ))}
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
            {MASK_TYPES.map(mask => (
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

          {settings.maskTypes.includes('occlusion') && (
            <div className="pl-6 space-y-1.5 mt-2 border-l border-border/50">
              <label className="text-[10px] text-muted-foreground font-medium">Occlusion Mask Model</label>
              <Select value={settings.occlusionModel} onValueChange={settings.setOcclusionModel}>
                <SelectTrigger className="w-full text-xs h-8">
                  <SelectValue placeholder="Select occlusion model" />
                </SelectTrigger>
                <SelectContent>
                  {OCCLUSION_MODELS.map(m => (
                    <SelectItem key={m.id} value={m.id}>
                      <div className="flex flex-col text-left">
                        <span className="font-medium text-xs">{m.label}</span>
                        {m.description && <span className="text-[10px] text-muted-foreground">{m.description}</span>}
                      </div>
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>
            </div>
          )}

          {settings.maskTypes.includes('region') && (
            <div className="pl-6 space-y-2 mt-2 border-l border-border/50">
              <label className="text-[10px] text-muted-foreground">Select Regions</label>
              <div className="grid grid-cols-2 gap-2">
                {MASK_REGIONS.map(region => (
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
          <label className="flex justify-between text-xs text-muted-foreground">
            Face Scan Sample Limit <span className="font-mono text-primary">{settings.scanSampleCount[0]}</span>
          </label>
          <Slider value={settings.scanSampleCount} onValueChange={settings.setScanSampleCount} max={20} min={1} step={1} />
        </div>
        
        <div className="space-y-2">
          <label className="text-xs text-muted-foreground">Preview Resolution</label>
          <Select value={settings.previewRes} onValueChange={settings.setPreviewRes}>
            <SelectTrigger className="w-full text-xs h-8">
              <SelectValue placeholder="Select resolution" />
            </SelectTrigger>
            <SelectContent>
              {PREVIEW_RESOLUTIONS.map(r => (
                <SelectItem key={r.id} value={r.id}>{r.label}</SelectItem>
              ))}
            </SelectContent>
          </Select>
        </div>

        <div className="space-y-2">
          <label className="text-xs text-muted-foreground">Gallery Resolution (On-the-Fly)</label>
          <Select value={settings.galleryRes} onValueChange={settings.setGalleryRes}>
            <SelectTrigger className="w-full text-xs h-8">
              <SelectValue placeholder="Select gallery resolution" />
            </SelectTrigger>
            <SelectContent>
              {GALLERY_RESOLUTIONS.map(r => (
                <SelectItem key={r.id} value={r.id}>{r.label}</SelectItem>
              ))}
            </SelectContent>
          </Select>
        </div>

        <div className="h-px bg-border w-full mt-4" />
        
        {/* Immich Settings Section */}
        <div className="space-y-4 pt-2">
          <div className="flex items-center justify-between">
            <h3 className="font-mono text-[11px] tracking-widest text-primary">IMMICH INTEGRATION</h3>
          </div>
          
          <div className="space-y-2">
            <label className="text-xs text-muted-foreground">Immich Server URL</label>
            <input 
              type="text" 
              className="flex h-8 w-full rounded-md border border-input bg-transparent px-3 py-1 text-sm shadow-sm transition-colors placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-ring"
              placeholder="http://localhost:2283"
              value={settings.immichUrl}
              onChange={(e) => {
                settings.setImmichUrl(e.target.value);
                setIsConnected(false);
              }}
            />
          </div>

          <div className="space-y-2">
            <label className="text-xs text-muted-foreground">API Key</label>
            <input 
              type="password" 
              className="flex h-8 w-full rounded-md border border-input bg-transparent px-3 py-1 text-sm shadow-sm transition-colors placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-ring"
              placeholder="Enter API Key"
              value={settings.immichApiKey}
              onChange={(e) => {
                settings.setImmichApiKey(e.target.value);
                setIsConnected(false);
              }}
            />
            <button 
              className="w-full mt-2 h-8 rounded-md bg-secondary text-secondary-foreground text-xs font-medium hover:bg-secondary/80 flex items-center justify-center transition-colors disabled:opacity-50"
              onClick={() => testImmichConnection(true)}
              disabled={isConnecting || !settings.immichUrl || !settings.immichApiKey}
            >
              {isConnecting ? "Connecting..." : isConnected ? "✓ Connected" : "Connect to Immich"}
            </button>
          </div>

          <div className="space-y-1.5">
            <div className="flex items-center justify-between">
              <label className="text-xs text-muted-foreground">Immich Local Path (Hardlink)</label>
              <span className="text-[10px] text-muted-foreground/60 font-mono">Optional</span>
            </div>
            <input 
              type="text" 
              className="flex h-8 w-full rounded-md border border-input bg-transparent px-3 py-1 text-xs shadow-sm transition-colors placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-ring font-mono"
              placeholder="e.g. D:\immich\upload (Default: uni-face.ini)"
              value={settings.immichLocalPath}
              onChange={(e) => settings.setImmichLocalPath(e.target.value)}
            />
            <p className="text-[10px] text-muted-foreground/70 leading-tight">
              Host directory of Immich library for instant 0 MB hardlinks. Leave blank to use uni-face.ini.
            </p>
          </div>

          {isConnected && (
            <>
              <div className="flex items-center justify-between pt-2 border-t border-border mt-4">
                <label className="text-xs font-medium text-foreground">Auto-Save to Immich</label>
                <Switch checked={settings.immichAutoSave} onCheckedChange={settings.setImmichAutoSave} />
              </div>

              {settings.immichAutoSave && (
                <div className="pl-2 border-l-2 border-border space-y-4">
                  <ImmichExportConfig
                    immichUrl={settings.immichUrl}
                    immichApiKey={settings.immichApiKey}
                    isNewAlbum={settings.immichNewAlbum}
                    onIsNewAlbumChange={settings.setImmichNewAlbum}
                    albumName={settings.immichAlbum}
                    onAlbumNameChange={settings.setImmichAlbum}
                    tags={settings.immichTags}
                    onTagsChange={settings.setImmichTags}
                  />
                  <div className="flex items-center justify-between">
                    <label className="text-xs text-muted-foreground">Delete local files after upload</label>
                    <Switch checked={settings.immichDeleteLocal} onCheckedChange={settings.setImmichDeleteLocal} />
                  </div>
                </div>
              )}
            </>
          )}
        </div>

        <div className="h-px bg-border w-full" />

        {/* Workspace Storage Management */}
        <div className="space-y-3">
          <label className="text-xs font-medium text-foreground flex items-center justify-between">
            <span>Storage & Temporary Cache</span>
          </label>
          <p className="text-[11px] text-muted-foreground leading-relaxed">
            Target Sets and Active Inputs are preserved during your session. You can free disk space by clearing one-off upload files.
          </p>
          <button
            type="button"
            className="w-full text-xs h-8 rounded-md border border-border bg-secondary/50 text-foreground hover:bg-destructive/20 hover:text-destructive hover:border-destructive/40 font-mono transition-colors flex items-center justify-center gap-1.5"
            onClick={async () => {
              try {
                const res = await api.clearTempWorkspace();
                toast.success(`Cleared ${res.deleted_count} temporary files (${(res.reclaimed_bytes / (1024 * 1024)).toFixed(1)} MB reclaimed)`);
              } catch (e: any) {
                toast.error('Failed to clear temporary workspace');
              }
            }}
          >
            <span>🗑️ Clear Temporary Uploads</span>
          </button>
        </div>

        <p className="text-[11px] text-muted-foreground pt-2 leading-relaxed">
          All settings are saved automatically to your browser.
        </p>

        {/* Spacer for bottom bar */}
        <div className="h-20" />
      </div>
      </div>
    </aside>
  );
}
