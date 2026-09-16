import { useState, useEffect, useCallback } from "react";
import {
  X,
  ChevronDown,
  ChevronRight,
  Sparkles,
  ScanFace,
  Cpu,
  HardDrive,
  Trash2,
  RotateCcw,
} from "lucide-react";
import { toast } from "sonner";
import { Slider } from "@/components/ui/slider";
import { Switch } from "@/components/ui/switch";
import { Checkbox } from "@/components/ui/checkbox";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import { ImmichExportConfig } from "@/components/shared/ImmichExportConfig";
import { api } from "@/services/api";
import {
  SWAP_MODELS,
  RESTORE_MODELS,
  EXECUTION_PROVIDERS,
  FACE_BOOST_OPTIONS,
  MASK_TYPES,
  MASK_REGIONS,
  OCCLUSION_MODELS,
  TARGET_GENDERS,
  FACE_ORDERS,
  PREVIEW_RESOLUTIONS,
  GALLERY_RESOLUTIONS,
} from "@/config";
import type { SettingsState } from "@/types";

interface SettingsPanelProps {
  open: boolean;
  onClose: () => void;
  settings: SettingsState;
}

export function SettingsPanel({ open, onClose, settings }: SettingsPanelProps) {
  const [isConnecting, setIsConnecting] = useState(false);
  const [isConnected, setIsConnected] = useState(false);

  // Collapsible Accordion Sections
  const [openSections, setOpenSections] = useState({
    quality: true,
    detection: false,
    performance: false,
    storage: false,
  });

  const toggleSection = (key: keyof typeof openSections) => {
    setOpenSections((prev) => ({ ...prev, [key]: !prev[key] }));
  };

  const testImmichConnection = useCallback(
    async (showToast = false) => {
      if (!settings.immichUrl || !settings.immichApiKey) return;
      setIsConnecting(true);
      try {
        const data = await api.testImmich(
          settings.immichUrl,
          settings.immichApiKey,
        );
        setIsConnected(data.success);
        if (showToast) {
          if (data.success)
            toast.success(data.message || "Connected to Immich successfully");
          else toast.error(data.message || "Failed to connect to Immich");
        }
      } catch (e: any) {
        setIsConnected(false);
        if (showToast) toast.error(e.message || "Connection failed");
      } finally {
        setIsConnecting(false);
      }
    },
    [settings.immichUrl, settings.immichApiKey],
  );

  useEffect(() => {
    if (settings.immichUrl && settings.immichApiKey) {
      testImmichConnection(false);
    }
  }, [settings.immichUrl, settings.immichApiKey, testImmichConnection]);

  return (
    <aside
      className={`absolute md:relative right-0 top-0 bottom-0 z-[60] md:z-10 shrink-0 h-full bg-card transition-all duration-300 overflow-hidden ${
        open
          ? "w-[85vw] max-w-[320px] md:w-[320px] border-l border-border shadow-2xl md:shadow-none"
          : "w-0 border-none"
      }`}
    >
      <div className="w-[85vw] max-w-[320px] md:w-[320px] h-full flex flex-col relative">
        {/* Header */}
        <div className="h-12 shrink-0 flex items-center justify-between px-4 border-b border-border font-mono text-xs tracking-widest text-muted-foreground whitespace-nowrap">
          <span>SETTINGS</span>
          <button
            className="p-1 hover:text-foreground transition-colors rounded-md hover:bg-secondary"
            onClick={onClose}
          >
            <X size={16} />
          </button>
        </div>

        {/* Scrollable Accordions */}
        <div className="flex-1 overflow-y-auto p-3 space-y-3">
          {/* SECTION 1: Quality & Swapping */}
          <div className="border border-border/70 rounded-xl overflow-hidden bg-background/50">
            <button
              type="button"
              onClick={() => toggleSection("quality")}
              className="w-full flex items-center justify-between px-3 py-2.5 bg-secondary/30 hover:bg-secondary/50 transition-colors text-left font-medium"
            >
              <div className="flex items-center gap-2">
                <Sparkles size={15} className="text-primary" />
                <span className="text-xs font-mono font-semibold text-foreground tracking-wide">
                  คุณภาพ & สลับหน้า
                </span>
              </div>
              {openSections.quality ? (
                <ChevronDown size={14} className="text-muted-foreground" />
              ) : (
                <ChevronRight size={14} className="text-muted-foreground" />
              )}
            </button>

            {openSections.quality && (
              <div className="p-3 space-y-3.5 text-xs">
                {/* Face Boost Dropdown */}
                <div className="space-y-1">
                  <div className="flex justify-between items-center">
                    <label className="text-muted-foreground font-medium">
                      Face Boost (ReActor)
                    </label>
                    <span className="font-mono text-[10px] text-primary">
                      {settings.faceBoost}
                    </span>
                  </div>
                  <Select
                    value={settings.faceBoost}
                    onValueChange={settings.setFaceBoost}
                  >
                    <SelectTrigger className="w-full h-8 text-xs bg-secondary/50 border-border">
                      <SelectValue placeholder="Select Face Boost" />
                    </SelectTrigger>
                    <SelectContent>
                      {FACE_BOOST_OPTIONS.map((opt) => (
                        <SelectItem key={opt.id} value={opt.id}>
                          {opt.label}
                        </SelectItem>
                      ))}
                    </SelectContent>
                  </Select>
                </div>

                {/* Restore Source Face Toggle */}
                <div className="flex items-center justify-between py-0.5">
                  <div className="space-y-0.5">
                    <label className="text-foreground">
                      Restore Source Face
                    </label>
                    <p className="text-[10px] text-muted-foreground leading-tight">
                      Enhance source before feature extraction
                    </p>
                  </div>
                  <Switch
                    checked={settings.restoreSourceFace}
                    onCheckedChange={settings.setRestoreSourceFace}
                  />
                </div>

                {/* Target Hair Protection Toggle */}
                <div className="flex items-center justify-between py-0.5">
                  <div className="space-y-0.5">
                    <label className="text-foreground">
                      Target Hair Protect
                    </label>
                    <p className="text-[10px] text-muted-foreground leading-tight">
                      Soft-blend bangs & hairline (BiSeNet)
                    </p>
                  </div>
                  <Switch
                    checked={settings.targetHairProtect}
                    onCheckedChange={settings.setTargetHairProtect}
                  />
                </div>

                <div className="h-px bg-border/50 w-full my-1" />

                {/* Stage 1 Swap Model */}
                <div className="space-y-1">
                  <label className="text-muted-foreground font-medium">
                    Stage 1 Swap Model
                  </label>
                  <Select
                    value={settings.swapModel}
                    onValueChange={settings.setSwapModel}
                  >
                    <SelectTrigger className="w-full h-8 text-xs bg-secondary/50 border-border">
                      <SelectValue placeholder="Select swap model" />
                    </SelectTrigger>
                    <SelectContent>
                      {SWAP_MODELS.map((m) => (
                        <SelectItem key={m.id} value={m.id}>
                          {m.label}
                        </SelectItem>
                      ))}
                    </SelectContent>
                  </Select>
                </div>

                {/* Swap Weight */}
                <div className="space-y-1">
                  <div className="flex justify-between items-center">
                    <label className="text-muted-foreground">Swap Weight</label>
                    <span className="font-mono text-primary font-medium">
                      {settings.swapWeight[0]}%
                    </span>
                  </div>
                  <Slider
                    value={settings.swapWeight}
                    onValueChange={settings.setSwapWeight}
                    max={100}
                    step={1}
                  />
                </div>

                {/* Stage 1 Restore */}
                <div className="space-y-2 pt-1 border-t border-border/40">
                  <div className="flex items-center justify-between">
                    <label className="text-foreground font-medium">
                      Stage 1 Restore
                    </label>
                    <Switch
                      checked={settings.stage1Restore}
                      onCheckedChange={settings.setStage1Restore}
                    />
                  </div>

                  {settings.stage1Restore && (
                    <div className="pl-3 space-y-2.5 border-l-2 border-primary/40 pt-1">
                      <div className="space-y-1">
                        <label className="text-[10px] text-muted-foreground">
                          Restorer Model
                        </label>
                        <Select
                          value={settings.restoreModel}
                          onValueChange={settings.setRestoreModel}
                        >
                          <SelectTrigger className="w-full text-xs h-7">
                            <SelectValue placeholder="Model" />
                          </SelectTrigger>
                          <SelectContent>
                            {RESTORE_MODELS.map((m) => (
                              <SelectItem key={m.id} value={m.id}>
                                {m.label}
                              </SelectItem>
                            ))}
                          </SelectContent>
                        </Select>
                      </div>

                      <div className="space-y-1">
                        <div className="flex justify-between text-[10px] text-muted-foreground">
                          <span>Weight</span>
                          <span className="font-mono text-primary">
                            {settings.restoreWeight[0]}%
                          </span>
                        </div>
                        <Slider
                          value={settings.restoreWeight}
                          onValueChange={settings.setRestoreWeight}
                          max={100}
                          step={1}
                        />
                      </div>

                      <div className="space-y-1">
                        <div className="flex justify-between text-[10px] text-muted-foreground">
                          <span>Blend</span>
                          <span className="font-mono text-primary">
                            {settings.restoreBlend[0]}%
                          </span>
                        </div>
                        <Slider
                          value={settings.restoreBlend}
                          onValueChange={settings.setRestoreBlend}
                          max={100}
                          step={1}
                        />
                      </div>
                    </div>
                  )}
                </div>

                {/* Dual Swap (Stage 2) */}
                <div className="space-y-2 pt-1 border-t border-border/40">
                  <div className="flex items-center justify-between">
                    <div className="space-y-0.5">
                      <label className="text-foreground font-medium">
                        Dual Swap (2-Stage)
                      </label>
                      <p className="text-[10px] text-muted-foreground">
                        Refinement pass for high resemblance
                      </p>
                    </div>
                    <Switch
                      checked={settings.dualSwap}
                      onCheckedChange={settings.setDualSwap}
                    />
                  </div>

                  {settings.dualSwap && (
                    <div className="pl-3 space-y-2.5 border-l-2 border-primary/40 pt-1">
                      <div className="space-y-1">
                        <label className="text-[10px] text-muted-foreground">
                          Stage 2 Model
                        </label>
                        <Select
                          value={settings.swapModel2}
                          onValueChange={settings.setSwapModel2}
                        >
                          <SelectTrigger className="w-full text-xs h-7">
                            <SelectValue placeholder="Stage 2 Model" />
                          </SelectTrigger>
                          <SelectContent>
                            {SWAP_MODELS.map((m) => (
                              <SelectItem key={m.id} value={m.id}>
                                {m.label}
                              </SelectItem>
                            ))}
                          </SelectContent>
                        </Select>
                      </div>

                      <div className="space-y-1">
                        <div className="flex justify-between text-[10px] text-muted-foreground">
                          <span>Stage 2 Weight</span>
                          <span className="font-mono text-primary">
                            {settings.swapWeight2[0]}%
                          </span>
                        </div>
                        <Slider
                          value={settings.swapWeight2}
                          onValueChange={settings.setSwapWeight2}
                          max={100}
                          step={1}
                        />
                      </div>

                      {/* Stage 2 Restore */}
                      <div className="flex items-center justify-between pt-1">
                        <span className="text-[10px] text-muted-foreground">
                          Stage 2 Restore
                        </span>
                        <Switch
                          checked={settings.stage2Restore}
                          onCheckedChange={settings.setStage2Restore}
                        />
                      </div>

                      {settings.stage2Restore && (
                        <div className="space-y-2 pt-1">
                          <Select
                            value={settings.restoreModel2}
                            onValueChange={settings.setRestoreModel2}
                          >
                            <SelectTrigger className="w-full text-xs h-7">
                              <SelectValue placeholder="Stage 2 Restorer" />
                            </SelectTrigger>
                            <SelectContent>
                              {RESTORE_MODELS.map((m) => (
                                <SelectItem key={m.id} value={m.id}>
                                  {m.label}
                                </SelectItem>
                              ))}
                            </SelectContent>
                          </Select>

                          <div className="space-y-1">
                            <div className="flex justify-between text-[10px] text-muted-foreground">
                              <span>Weight</span>
                              <span className="font-mono text-primary">
                                {settings.restoreWeight2[0]}%
                              </span>
                            </div>
                            <Slider
                              value={settings.restoreWeight2}
                              onValueChange={settings.setRestoreWeight2}
                              max={100}
                              step={1}
                            />
                          </div>

                          <div className="space-y-1">
                            <div className="flex justify-between text-[10px] text-muted-foreground">
                              <span>Blend</span>
                              <span className="font-mono text-primary">
                                {settings.restoreBlend2[0]}%
                              </span>
                            </div>
                            <Slider
                              value={settings.restoreBlend2}
                              onValueChange={settings.setRestoreBlend2}
                              max={100}
                              step={1}
                            />
                          </div>
                        </div>
                      )}
                    </div>
                  )}
                </div>

                {/* Color Match & Similarity */}
                <div className="space-y-2 pt-1 border-t border-border/40">
                  <div className="flex items-center justify-between">
                    <label className="text-muted-foreground">Color Match</label>
                    <Switch
                      checked={settings.colorMatch}
                      onCheckedChange={settings.setColorMatch}
                    />
                  </div>
                  <div className="flex items-center justify-between">
                    <label className="text-muted-foreground">
                      Similarity Check
                    </label>
                    <Switch
                      checked={settings.similarity}
                      onCheckedChange={settings.setSimilarity}
                    />
                  </div>
                </div>
              </div>
            )}
          </div>

          {/* SECTION 2: Detection & Masking */}
          <div className="border border-border/70 rounded-xl overflow-hidden bg-background/50">
            <button
              type="button"
              onClick={() => toggleSection("detection")}
              className="w-full flex items-center justify-between px-3 py-2.5 bg-secondary/30 hover:bg-secondary/50 transition-colors text-left font-medium"
            >
              <div className="flex items-center gap-2">
                <ScanFace size={15} className="text-primary" />
                <span className="text-xs font-mono font-semibold text-foreground tracking-wide">
                  ตรวจจับ & มาสก์
                </span>
              </div>
              {openSections.detection ? (
                <ChevronDown size={14} className="text-muted-foreground" />
              ) : (
                <ChevronRight size={14} className="text-muted-foreground" />
              )}
            </button>

            {openSections.detection && (
              <div className="p-3 space-y-3.5 text-xs">
                {/* Target Gender Filter */}
                <div className="space-y-1.5">
                  <div className="flex items-center justify-between">
                    <label className="text-foreground font-medium">
                      Gender Filter
                    </label>
                    <Switch
                      checked={settings.genderFilter}
                      onCheckedChange={settings.setGenderFilter}
                    />
                  </div>
                  {settings.genderFilter && (
                    <Select
                      value={settings.targetGender}
                      onValueChange={settings.setTargetGender}
                    >
                      <SelectTrigger className="w-full h-8 text-xs bg-secondary/50 border-border">
                        <SelectValue placeholder="Select Gender" />
                      </SelectTrigger>
                      <SelectContent>
                        {TARGET_GENDERS.map((g) => (
                          <SelectItem key={g.id} value={g.id}>
                            {g.label}
                          </SelectItem>
                        ))}
                      </SelectContent>
                    </Select>
                  )}
                </div>

                {/* Face Order */}
                <div className="space-y-1">
                  <label className="text-muted-foreground font-medium">
                    Face Priority
                  </label>
                  <Select
                    value={settings.faceOrder}
                    onValueChange={settings.setFaceOrder}
                  >
                    <SelectTrigger className="w-full h-8 text-xs bg-secondary/50 border-border">
                      <SelectValue placeholder="Face Priority" />
                    </SelectTrigger>
                    <SelectContent>
                      {FACE_ORDERS.map((o) => (
                        <SelectItem key={o.id} value={o.id}>
                          {o.label}
                        </SelectItem>
                      ))}
                    </SelectContent>
                  </Select>
                </div>

                {/* Detection & Landmark Scores */}
                <div className="space-y-2 pt-1 border-t border-border/40">
                  <div className="space-y-1">
                    <div className="flex justify-between items-center">
                      <label className="text-muted-foreground">
                        Detection Score
                      </label>
                      <span className="font-mono text-primary font-medium">
                        {settings.faceDetectorScore[0]}%
                      </span>
                    </div>
                    <Slider
                      value={settings.faceDetectorScore}
                      onValueChange={settings.setFaceDetectorScore}
                      min={30}
                      max={95}
                      step={1}
                    />
                  </div>

                  <div className="space-y-1">
                    <div className="flex justify-between items-center">
                      <label className="text-muted-foreground">
                        Landmark Score
                      </label>
                      <span className="font-mono text-primary font-medium">
                        {settings.faceLandmarkScore[0]}%
                      </span>
                    </div>
                    <Slider
                      value={settings.faceLandmarkScore}
                      onValueChange={settings.setFaceLandmarkScore}
                      min={30}
                      max={90}
                      step={1}
                    />
                  </div>
                </div>

                {/* Visual Boundary Tools Master Toggle */}
                <div className="space-y-2 pt-1 border-t border-border/40">
                  <div className="flex items-center justify-between">
                    <div className="space-y-0.5">
                      <label className="text-foreground font-medium">
                        Boundary Tuner Button
                      </label>
                      <p className="text-[10px] text-muted-foreground">
                        Show visual boundary button in source cards
                      </p>
                    </div>
                    <Switch
                      checked={settings.enableFaceCleanTools}
                      onCheckedChange={(checked) => {
                        settings.setEnableFaceCleanTools(checked);
                        if (!checked) {
                          settings.setCleanSourceFace(false);
                          settings.setMaskPadding([0, 0, 0, 0]);
                        }
                      }}
                    />
                  </div>

                  {settings.enableFaceCleanTools &&
                    settings.maskPadding.some((p) => p > 0) && (
                      <div className="flex items-center justify-between text-[10px] font-mono bg-secondary/40 p-2 rounded border border-border">
                        <span>
                          Padding: T:{settings.maskPadding[0]}% B:
                          {settings.maskPadding[2]}% L:
                          {settings.maskPadding[3]}% R:
                          {settings.maskPadding[1]}%
                        </span>
                        <button
                          type="button"
                          className="text-primary hover:underline"
                          onClick={() => {
                            settings.setMaskPadding([0, 0, 0, 0]);
                            toast.info("Mask padding reset to 0");
                          }}
                        >
                          Reset
                        </button>
                      </div>
                    )}
                </div>

                {/* Mask Types (Parser) */}
                <div className="space-y-2 pt-1 border-t border-border/40">
                  <label className="text-muted-foreground font-medium block">
                    Mask Types
                  </label>
                  <div className="grid grid-cols-2 gap-2">
                    {MASK_TYPES.map((mask) => (
                      <div
                        key={mask.id}
                        className="flex items-center space-x-1.5"
                      >
                        <Checkbox
                          id={`mask-${mask.id}`}
                          checked={settings.maskTypes.includes(mask.id)}
                          onCheckedChange={(checked) => {
                            if (checked) {
                              settings.setMaskTypes([
                                ...settings.maskTypes,
                                mask.id,
                              ]);
                            } else {
                              const filtered = settings.maskTypes.filter(
                                (m) => m !== mask.id,
                              );
                              settings.setMaskTypes(
                                filtered.length > 0 ? filtered : ["box"],
                              );
                            }
                          }}
                        />
                        <label
                          htmlFor={`mask-${mask.id}`}
                          className="text-[11px] cursor-pointer text-muted-foreground hover:text-foreground"
                        >
                          {mask.label}
                        </label>
                      </div>
                    ))}
                  </div>

                  {settings.maskTypes.includes("occlusion") && (
                    <div className="pl-2 space-y-1 border-l-2 border-border/70 pt-1">
                      <label className="text-[10px] text-muted-foreground">
                        Occlusion Model
                      </label>
                      <Select
                        value={settings.occlusionModel}
                        onValueChange={settings.setOcclusionModel}
                      >
                        <SelectTrigger className="w-full h-7 text-xs">
                          <SelectValue placeholder="Model" />
                        </SelectTrigger>
                        <SelectContent>
                          {OCCLUSION_MODELS.map((m) => (
                            <SelectItem key={m.id} value={m.id}>
                              {m.label}
                            </SelectItem>
                          ))}
                        </SelectContent>
                      </Select>
                    </div>
                  )}

                  {settings.maskTypes.includes("region") && (
                    <div className="pl-2 space-y-1 border-l-2 border-border/70 pt-1">
                      <label className="text-[10px] text-muted-foreground">
                        Regions
                      </label>
                      <div className="grid grid-cols-2 gap-1.5">
                        {MASK_REGIONS.map((r) => (
                          <div
                            key={r.id}
                            className="flex items-center space-x-1"
                          >
                            <Checkbox
                              id={`reg-${r.id}`}
                              checked={settings.maskRegions.includes(r.id)}
                              onCheckedChange={(checked) => {
                                if (checked) {
                                  settings.setMaskRegions([
                                    ...settings.maskRegions,
                                    r.id,
                                  ]);
                                } else {
                                  settings.setMaskRegions(
                                    settings.maskRegions.filter(
                                      (id) => id !== r.id,
                                    ),
                                  );
                                }
                              }}
                            />
                            <label
                              htmlFor={`reg-${r.id}`}
                              className="text-[10px] text-muted-foreground cursor-pointer"
                            >
                              {r.label}
                            </label>
                          </div>
                        ))}
                      </div>
                    </div>
                  )}
                </div>
              </div>
            )}
          </div>

          {/* SECTION 3: Performance & System */}
          <div className="border border-border/70 rounded-xl overflow-hidden bg-background/50">
            <button
              type="button"
              onClick={() => toggleSection("performance")}
              className="w-full flex items-center justify-between px-3 py-2.5 bg-secondary/30 hover:bg-secondary/50 transition-colors text-left font-medium"
            >
              <div className="flex items-center gap-2">
                <Cpu size={15} className="text-primary" />
                <span className="text-xs font-mono font-semibold text-foreground tracking-wide">
                  ความเร็ว & ระบบ
                </span>
              </div>
              {openSections.performance ? (
                <ChevronDown size={14} className="text-muted-foreground" />
              ) : (
                <ChevronRight size={14} className="text-muted-foreground" />
              )}
            </button>

            {openSections.performance && (
              <div className="p-3 space-y-3 text-xs">
                {/* Provider */}
                <div className="space-y-1">
                  <label className="text-muted-foreground font-medium">
                    Execution Provider
                  </label>
                  <Select
                    value={settings.executionProvider}
                    onValueChange={settings.setExecutionProvider}
                  >
                    <SelectTrigger className="w-full h-8 text-xs bg-secondary/50 border-border">
                      <SelectValue placeholder="Provider" />
                    </SelectTrigger>
                    <SelectContent>
                      {EXECUTION_PROVIDERS.map((p) => (
                        <SelectItem key={p.id} value={p.id}>
                          {p.label}
                        </SelectItem>
                      ))}
                    </SelectContent>
                  </Select>
                </div>

                {/* Threads */}
                <div className="space-y-1">
                  <div className="flex justify-between items-center">
                    <label className="text-muted-foreground">
                      Thread Count
                    </label>
                    <span className="font-mono text-primary font-medium">
                      {settings.executionThreadCount[0]}
                    </span>
                  </div>
                  <Slider
                    value={settings.executionThreadCount}
                    onValueChange={settings.setExecutionThreadCount}
                    max={32}
                    min={1}
                    step={1}
                  />
                </div>

                {/* Hash Chunk */}
                <div className="space-y-1">
                  <div className="flex justify-between items-center">
                    <label className="text-muted-foreground">
                      Hash Chunk Size
                    </label>
                    <span className="font-mono text-primary font-medium">
                      {settings.hashChunkSize[0]} MB
                    </span>
                  </div>
                  <Slider
                    value={settings.hashChunkSize}
                    onValueChange={settings.setHashChunkSize}
                    max={500}
                    min={5}
                    step={5}
                  />
                </div>

                {/* Preview Frequency & Face Scan Limit */}
                <div className="space-y-1 pt-1 border-t border-border/40">
                  <div className="flex justify-between items-center">
                    <label className="text-muted-foreground">
                      Preview Frame Every
                    </label>
                    <span className="font-mono text-primary font-medium">
                      {settings.previewFreq[0]}
                    </span>
                  </div>
                  <Slider
                    value={settings.previewFreq}
                    onValueChange={settings.setPreviewFreq}
                    max={60}
                    min={1}
                    step={1}
                  />
                </div>

                <div className="space-y-1">
                  <div className="flex justify-between items-center">
                    <label className="text-muted-foreground">
                      Face Scan Limit
                    </label>
                    <span className="font-mono text-primary font-medium">
                      {settings.scanSampleCount[0]}
                    </span>
                  </div>
                  <Slider
                    value={settings.scanSampleCount}
                    onValueChange={settings.setScanSampleCount}
                    max={20}
                    min={1}
                    step={1}
                  />
                </div>

                {/* Resolutions */}
                <div className="grid grid-cols-2 gap-2 pt-1 border-t border-border/40">
                  <div className="space-y-1">
                    <label className="text-[10px] text-muted-foreground">
                      Preview Res
                    </label>
                    <Select
                      value={settings.previewRes}
                      onValueChange={settings.setPreviewRes}
                    >
                      <SelectTrigger className="w-full h-7 text-xs">
                        <SelectValue placeholder="Res" />
                      </SelectTrigger>
                      <SelectContent>
                        {PREVIEW_RESOLUTIONS.map((r) => (
                          <SelectItem key={r.id} value={r.id}>
                            {r.label}
                          </SelectItem>
                        ))}
                      </SelectContent>
                    </Select>
                  </div>

                  <div className="space-y-1">
                    <label className="text-[10px] text-muted-foreground">
                      Gallery Res
                    </label>
                    <Select
                      value={settings.galleryRes}
                      onValueChange={settings.setGalleryRes}
                    >
                      <SelectTrigger className="w-full h-7 text-xs">
                        <SelectValue placeholder="Res" />
                      </SelectTrigger>
                      <SelectContent>
                        {GALLERY_RESOLUTIONS.map((r) => (
                          <SelectItem key={r.id} value={r.id}>
                            {r.label}
                          </SelectItem>
                        ))}
                      </SelectContent>
                    </Select>
                  </div>
                </div>

                {/* Unload Models */}
                <div className="pt-2 border-t border-border/40">
                  <button
                    type="button"
                    className="w-full text-xs h-8 rounded-md border border-border bg-secondary/50 text-foreground hover:bg-primary/20 hover:text-primary transition-colors flex items-center justify-center gap-1.5 font-mono"
                    onClick={async () => {
                      try {
                        const res = await api.unloadModels();
                        toast.success(
                          res.message || "All models unloaded from memory",
                        );
                      } catch {
                        toast.error("Failed to unload models");
                      }
                    }}
                  >
                    <RotateCcw size={13} /> Unload Models
                  </button>
                </div>
              </div>
            )}
          </div>

          {/* SECTION 4: Storage & Immich */}
          <div className="border border-border/70 rounded-xl overflow-hidden bg-background/50">
            <button
              type="button"
              onClick={() => toggleSection("storage")}
              className="w-full flex items-center justify-between px-3 py-2.5 bg-secondary/30 hover:bg-secondary/50 transition-colors text-left font-medium"
            >
              <div className="flex items-center gap-2">
                <HardDrive size={15} className="text-primary" />
                <span className="text-xs font-mono font-semibold text-foreground tracking-wide">
                  การจัดเก็บ & Immich
                </span>
              </div>
              {openSections.storage ? (
                <ChevronDown size={14} className="text-muted-foreground" />
              ) : (
                <ChevronRight size={14} className="text-muted-foreground" />
              )}
            </button>

            {openSections.storage && (
              <div className="p-3 space-y-3 text-xs">
                {/* Skip Existing / Overwrite */}
                <div className="flex items-center justify-between">
                  <div className="space-y-0.5">
                    <label className="text-foreground">Skip Existing</label>
                    <p className="text-[10px] text-muted-foreground">
                      Skip already processed files
                    </p>
                  </div>
                  <Switch
                    checked={settings.skipExisting}
                    onCheckedChange={settings.setSkipExisting}
                  />
                </div>

                {/* Clear Temporary Workspace Cache */}
                <button
                  type="button"
                  className="w-full text-xs h-8 rounded-md border border-border bg-secondary/50 text-foreground hover:bg-destructive/20 hover:text-destructive transition-colors flex items-center justify-center gap-1.5 font-mono"
                  onClick={async () => {
                    try {
                      const res = await api.clearTempWorkspace();
                      toast.success(
                        `Cleared ${res.deleted_count} files (${(res.reclaimed_bytes / (1024 * 1024)).toFixed(1)} MB reclaimed)`,
                      );
                    } catch {
                      toast.error("Failed to clear temporary workspace");
                    }
                  }}
                >
                  <Trash2 size={13} /> Clear Temp Uploads
                </button>

                <div className="h-px bg-border/50 w-full my-1" />

                {/* Immich Integration */}
                <div className="space-y-2">
                  <div className="flex items-center justify-between">
                    <span className="font-mono text-[10px] text-primary font-semibold uppercase">
                      Immich Integration
                    </span>
                    {isConnected && (
                      <span className="text-[9px] font-mono text-emerald-400 bg-emerald-500/10 px-1 rounded">
                        Connected
                      </span>
                    )}
                  </div>

                  <div className="space-y-1">
                    <label className="text-[10px] text-muted-foreground">
                      Server URL
                    </label>
                    <input
                      type="text"
                      className="flex h-7 w-full rounded-md border border-input bg-transparent px-2 text-xs shadow-sm font-mono placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-ring"
                      placeholder="http://localhost:2283"
                      value={settings.immichUrl}
                      onChange={(e) => {
                        settings.setImmichUrl(e.target.value);
                        setIsConnected(false);
                      }}
                    />
                  </div>

                  <div className="space-y-1">
                    <label className="text-[10px] text-muted-foreground">
                      API Key
                    </label>
                    <input
                      type="password"
                      className="flex h-7 w-full rounded-md border border-input bg-transparent px-2 text-xs shadow-sm font-mono placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-ring"
                      placeholder="Enter API Key"
                      value={settings.immichApiKey}
                      onChange={(e) => {
                        settings.setImmichApiKey(e.target.value);
                        setIsConnected(false);
                      }}
                    />
                  </div>

                  <button
                    type="button"
                    className="w-full mt-1 h-7 rounded-md bg-secondary text-secondary-foreground text-xs font-medium hover:bg-secondary/80 flex items-center justify-center transition-colors disabled:opacity-50"
                    onClick={() => testImmichConnection(true)}
                    disabled={
                      isConnecting ||
                      !settings.immichUrl ||
                      !settings.immichApiKey
                    }
                  >
                    {isConnecting
                      ? "Connecting..."
                      : isConnected
                        ? "✓ Connected"
                        : "Connect to Immich"}
                  </button>

                  <div className="space-y-1 pt-1">
                    <label className="text-[10px] text-muted-foreground">
                      Local Path (Hardlink)
                    </label>
                    <input
                      type="text"
                      className="flex h-7 w-full rounded-md border border-input bg-transparent px-2 text-xs shadow-sm font-mono placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-ring"
                      placeholder="Optional: D:\immich\upload"
                      value={settings.immichLocalPath}
                      onChange={(e) =>
                        settings.setImmichLocalPath(e.target.value)
                      }
                    />
                  </div>

                  {isConnected && (
                    <div className="space-y-2 pt-2 border-t border-border/40">
                      <div className="flex items-center justify-between">
                        <label className="text-foreground">
                          Auto-Save to Immich
                        </label>
                        <Switch
                          checked={settings.immichAutoSave}
                          onCheckedChange={settings.setImmichAutoSave}
                        />
                      </div>

                      {settings.immichAutoSave && (
                        <div className="pl-2 border-l-2 border-border/70 space-y-2">
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
                          <div className="flex items-center justify-between pt-1">
                            <label className="text-[10px] text-muted-foreground">
                              Delete local after upload
                            </label>
                            <Switch
                              checked={settings.immichDeleteLocal}
                              onCheckedChange={settings.setImmichDeleteLocal}
                            />
                          </div>
                        </div>
                      )}
                    </div>
                  )}
                </div>
              </div>
            )}
          </div>

          <div className="text-[10px] text-muted-foreground/80 text-center font-mono py-1">
            Auto-saved to local browser storage
          </div>

          {/* Bottom Spacer */}
          <div className="h-16" />
        </div>
      </div>
    </aside>
  );
}
