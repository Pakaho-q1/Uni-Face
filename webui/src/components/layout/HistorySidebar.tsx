import { useRef, useCallback, useState } from 'react';
import { X, RefreshCcw, Download, Trash2, Loader2, CloudUpload, Video, Image as ImageIcon } from 'lucide-react';
import { Checkbox } from '@/components/ui/checkbox';
import { Dialog, DialogContent, DialogTitle, DialogDescription, DialogFooter } from '@/components/ui/dialog';
import { Button } from '@/components/ui/button';
import { ImmichExportConfig } from '@/components/shared/ImmichExportConfig';
import { toast } from 'sonner';
import { api } from '@/services/api';
import type { HistoryItem, SettingsState } from '@/types';

interface HistorySidebarProps {
  open: boolean;
  onClose: () => void;
  history: HistoryItem[];
  totalHistory: number;
  hasMore: boolean;
  onLoadMore: () => void;
  onRefresh: () => void;
  selectedItems: Set<string>;
  onToggleSelect: (filename: string, checked: boolean) => void;
  onToggleSelectAll: (checked: boolean) => void;
  onBulkDelete: () => void;
  onBulkDownload: () => Promise<boolean>;
  lightboxItem: HistoryItem | null;
  setLightboxItem: (item: HistoryItem | null) => void;
  settings: SettingsState;
}

export function HistorySidebar({
  open, onClose, history, totalHistory, hasMore, onLoadMore, onRefresh,
  selectedItems, onToggleSelect, onToggleSelectAll,
  onBulkDelete, onBulkDownload,
  lightboxItem, setLightboxItem, settings
}: HistorySidebarProps) {
  const [isDownloading, setIsDownloading] = useState(false);
  const [downloadConfirmOpen, setDownloadConfirmOpen] = useState(false);
  
  const [immichModalOpen, setImmichModalOpen] = useState(false);
  const [isExporting, setIsExporting] = useState(false);
  
  // Local state for Immich manual export modal (initialized from settings)
  const [exportNewAlbum, setExportNewAlbum] = useState(false);
  const [exportAlbumName, setExportAlbumName] = useState("");
  const [exportTags, setExportTags] = useState<string[]>([]);
  
  const observerRef = useRef<IntersectionObserver | null>(null);
  const bottomElementRef = useCallback((node: HTMLDivElement | null) => {
    if (observerRef.current) observerRef.current.disconnect();
    if (node && hasMore) {
      const observer = new IntersectionObserver((entries) => {
        if (entries[0].isIntersecting) onLoadMore();
      }, { threshold: 0.1 });
      observer.observe(node);
      observerRef.current = observer;
    }
  }, [hasMore, onLoadMore]);

  const getSelectedSizeText = () => {
    let total = 0;
    let missingSize = false;
    selectedItems.forEach(filename => {
      const item = history.find(h => h.filename === filename);
      if (item && item.size) total += item.size;
      else missingSize = true;
    });
    const mb = (total / (1024 * 1024)).toFixed(2);
    return missingSize ? `${mb} MB (estimated)` : `${mb} MB`;
  };

  const handleDownloadConfirm = async () => {
    setDownloadConfirmOpen(false);
    setIsDownloading(true);
    await onBulkDownload();
    setIsDownloading(false);
  };

  const openImmichExport = () => {
    if (!settings.immichUrl || !settings.immichApiKey) {
      toast.error("Please connect to Immich in Settings first.");
      return;
    }
    setExportNewAlbum(settings.immichNewAlbum);
    setExportAlbumName(settings.immichAlbum);
    setExportTags(settings.immichTags || []);
    setImmichModalOpen(true);
  };

  const handleImmichExport = async () => {
    if (selectedItems.size === 0) return;
    setIsExporting(true);
    try {
      const data = await api.exportToImmich({
        url: settings.immichUrl,
        api_key: settings.immichApiKey,
        new_album: exportNewAlbum,
        album: exportAlbumName,
        tags: exportTags,
        filenames: Array.from(selectedItems)
      });
      if (data.success) {
        toast.success(`Exported ${selectedItems.size} files to Immich!`);
        setImmichModalOpen(false);
      } else {
        toast.error(data.message || "Export failed.");
      }
    } catch (e: any) {
      toast.error(e.message || "Export failed.");
    } finally {
      setIsExporting(false);
    }
  };

  return (
    <>
      <aside className={`absolute md:relative left-0 top-0 bottom-0 z-[60] md:z-10 shrink-0 h-full bg-card transition-all duration-300 overflow-hidden ${open ? 'w-[85vw] max-w-[300px] md:w-[300px] border-r border-border shadow-2xl md:shadow-none' : 'w-0 border-none'}`}>
        <div className="w-[85vw] max-w-[300px] md:w-[300px] h-full flex flex-col relative">
          
          <div className="h-14 shrink-0 flex items-center justify-between px-4 border-b border-border">
            <h2 className="font-mono text-[11px] tracking-widest text-muted-foreground uppercase flex items-center gap-2">
              Output Library
              <span className="bg-primary/20 text-primary px-1.5 py-0.5 rounded text-[9px]">{totalHistory}</span>
            </h2>
            <div className="flex items-center gap-2">
              <button onClick={onRefresh} className="text-muted-foreground hover:text-foreground transition-colors p-1" title="Refresh">
                <RefreshCcw size={14} />
              </button>
              <button onClick={onClose} className="text-muted-foreground hover:text-foreground transition-colors md:hidden p-1">
                <X size={16} />
              </button>
            </div>
          </div>

          <div className="flex-1 overflow-y-auto overflow-x-hidden custom-scrollbar">
            <div className="grid grid-cols-2 gap-1.5 p-1.5">
              {history.length === 0 ? (
                <div className="col-span-2 text-center text-xs text-muted-foreground py-8">
                  No outputs yet
                </div>
              ) : (
                history.map((item) => {
                  const isSelected = selectedItems.has(item.filename);
                  const isVid = item.type === 'video' || item.filename.toLowerCase().endsWith('.mp4');

                  return (
                    <div 
                      key={item.filename} 
                      className={`relative group aspect-square rounded-md overflow-hidden border-2 cursor-pointer transition-colors ${isSelected ? 'border-primary' : 'border-transparent hover:border-muted-foreground/50'} bg-secondary`}
                      onClick={() => {
                        if (selectedItems.size > 0) {
                          onToggleSelect(item.filename, !isSelected);
                        } else {
                          setLightboxItem(item);
                        }
                      }}
                    >
                      <div className={`absolute top-1.5 left-1.5 z-10 transition-opacity ${isSelected ? 'opacity-100' : 'opacity-0 group-hover:opacity-100'}`} onClick={(e) => e.stopPropagation()}>
                        <Checkbox checked={isSelected} onCheckedChange={(c) => onToggleSelect(item.filename, !!c)} />
                      </div>

                      {isVid ? (
                        <>
                          <video src={`${item.url}#t=0.001`} muted loop playsInline preload="metadata" className="w-full h-full object-contain pointer-events-none bg-black" />
                          <div className="absolute bottom-1 left-1 bg-black/60 rounded px-1.5 py-0.5 text-[10px] font-mono text-white flex items-center pointer-events-none">
                            <Video size={10} className="mr-1" /> VDO
                          </div>
                        </>
                      ) : (
                        <>
                          <img 
                            src={`${item.url}&res=${settings.galleryRes || '384'}`} 
                            alt={item.filename} 
                            loading="lazy" 
                            className="w-full h-full object-contain pointer-events-none bg-black" 
                          />
                          <div className="absolute bottom-1 left-1 bg-black/60 rounded px-1.5 py-0.5 text-[10px] font-mono text-white flex items-center pointer-events-none">
                            <ImageIcon size={10} className="mr-1" /> IMG
                          </div>
                        </>
                      )}
                    </div>
                  );
                })
              )}
              {hasMore && history.length > 0 && <div ref={bottomElementRef} className="col-span-2 h-5" />}
            </div>
            {/* Spacer for bottom bar */}
            <div className="h-24" />
          </div>

          {/* Floating Bulk Actions for Sidebar */}
          {selectedItems.size > 0 && (
            <div className="absolute bottom-6 left-1/2 -translate-x-1/2 z-50 glass px-4 py-2 rounded-xl flex items-center gap-4 whitespace-nowrap shadow-xl">
              <div className="flex items-center gap-2">
                <Checkbox 
                  checked={selectedItems.size > 0 && selectedItems.size >= totalHistory} 
                  onCheckedChange={(c) => onToggleSelectAll(!!c)} 
                />
                <span className="font-mono text-xs">{selectedItems.size}</span>
              </div>
              <div className="w-px h-5 bg-border" />
              <button 
                className={`transition-colors ${isDownloading ? 'text-primary' : 'text-foreground hover:text-primary'}`} 
                onClick={() => !isDownloading && setDownloadConfirmOpen(true)}
                disabled={isDownloading}
                title="Download Selected"
              >
                {isDownloading ? <Loader2 size={16} className="animate-spin" /> : <Download size={16} />}
              </button>
              <button 
                className="text-foreground hover:text-[#b1b2ff] transition-colors" 
                onClick={openImmichExport} 
                disabled={isDownloading}
                title="Export to Immich"
              >
                <CloudUpload size={16} />
              </button>
              <button className="text-destructive hover:text-red-400 transition-colors" onClick={onBulkDelete} disabled={isDownloading} title="Delete Selected">
                <Trash2 size={16} />
              </button>
            </div>
          )}
        </div>
      </aside>

      {/* Download Confirm Modal */}
      <Dialog open={downloadConfirmOpen} onOpenChange={setDownloadConfirmOpen}>
        <DialogContent className="sm:max-w-md">
          <DialogTitle>Download Selected Files</DialogTitle>
          <DialogDescription>
            You have selected <strong className="text-foreground">{selectedItems.size}</strong> file(s) for download.
            Total estimated size: <strong className="text-foreground">{getSelectedSizeText()}</strong>.
            <br/><br/>
            This will package the files into a single ZIP archive.
          </DialogDescription>
          <DialogFooter className="gap-2 sm:gap-0">
            <Button variant="ghost" onClick={() => setDownloadConfirmOpen(false)}>Cancel</Button>
            <Button onClick={handleDownloadConfirm} disabled={isDownloading}>
              {isDownloading ? (
                <><Loader2 size={16} className="animate-spin mr-2"/> Preparing ZIP...</>
              ) : "Start Download"}
            </Button>
          </DialogFooter>
        </DialogContent>
      </Dialog>

      {/* Immich Export Modal */}
      <Dialog open={immichModalOpen} onOpenChange={setImmichModalOpen}>
        <DialogContent className="sm:max-w-md">
          <DialogTitle>Export to Immich</DialogTitle>
          <DialogDescription>
            Sending <strong className="text-foreground">{selectedItems.size}</strong> file(s) to your Immich server.
          </DialogDescription>
          
          <div className="my-2">
            <ImmichExportConfig
              immichUrl={settings.immichUrl}
              immichApiKey={settings.immichApiKey}
              isNewAlbum={exportNewAlbum}
              onIsNewAlbumChange={setExportNewAlbum}
              albumName={exportAlbumName}
              onAlbumNameChange={setExportAlbumName}
              tags={exportTags}
              onTagsChange={setExportTags}
            />
          </div>

          <DialogFooter className="gap-2 sm:gap-0">
            <Button variant="ghost" onClick={() => setImmichModalOpen(false)}>Cancel</Button>
            <Button onClick={handleImmichExport} disabled={isExporting}>
              {isExporting ? (
                <><Loader2 size={16} className="animate-spin mr-2"/> Exporting...</>
              ) : "Confirm Export"}
            </Button>
          </DialogFooter>
        </DialogContent>
      </Dialog>

      {/* Lightbox Modal */}
      <Dialog open={!!lightboxItem} onOpenChange={(o) => !o && setLightboxItem(null)}>
        <DialogContent className="max-w-[95vw] w-full h-[95vh] p-0 overflow-hidden border-none bg-black/95 shadow-2xl flex items-center justify-center">
          <DialogTitle className="hidden">Preview</DialogTitle>
          <DialogDescription className="hidden">Lightbox preview of output</DialogDescription>
          {lightboxItem && (() => {
            const currentIndex = history.findIndex(h => h.filename === lightboxItem.filename);
            const hasPrev = currentIndex > 0;
            const hasNext = currentIndex < history.length - 1;

            return (
              <div className="flex items-center justify-center w-full h-full relative group overflow-auto">
                
                {/* Edge Click Navigation Areas */}
                {hasPrev && (
                  <div 
                    className="absolute left-0 top-0 w-1/4 h-full z-40 cursor-w-resize"
                    onClick={(e) => { e.stopPropagation(); setLightboxItem(history[currentIndex - 1]); }}
                  />
                )}
                
                {hasNext && (
                  <div 
                    className="absolute right-0 top-0 w-1/4 h-full z-40 cursor-e-resize"
                    onClick={(e) => { e.stopPropagation(); setLightboxItem(history[currentIndex + 1]); }}
                  />
                )}

                {/* Media Content with Zoom Support */}
                <div className="w-full h-full flex items-center justify-center overflow-auto">
                  {lightboxItem.type === 'video' ? (
                    <video src={lightboxItem.url} controls autoPlay loop className="max-w-full max-h-full object-contain" />
                  ) : (
                    <img 
                      src={lightboxItem.url} 
                      alt="Preview" 
                      className="max-w-full max-h-full object-contain cursor-zoom-in active:scale-150 transition-transform duration-200" 
                      title="Click and hold to zoom"
                    />
                  )}
                </div>
              </div>
            );
          })()}
        </DialogContent>
      </Dialog>
    </>
  );
}
