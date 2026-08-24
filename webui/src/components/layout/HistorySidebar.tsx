import { useRef, useCallback } from 'react';
import { X, RefreshCcw, Download, Trash2, PlayCircle, ChevronLeft, ChevronRight } from 'lucide-react';
import { Checkbox } from '@/components/ui/checkbox';
import { Dialog, DialogContent, DialogTitle, DialogDescription } from '@/components/ui/dialog';
import type { HistoryItem } from '@/hooks/useHistory';

interface HistorySidebarProps {
  open: boolean;
  onClose: () => void;
  history: HistoryItem[];
  hasMore: boolean;
  onLoadMore: () => void;
  onRefresh: () => void;
  selectedItems: Set<string>;
  onToggleSelect: (filename: string, checked: boolean) => void;
  onToggleSelectAll: (checked: boolean) => void;
  onBulkDelete: () => void;
  onBulkDownload: () => void;
  lightboxItem: HistoryItem | null;
  setLightboxItem: (item: HistoryItem | null) => void;
}

export function HistorySidebar({
  open, onClose, history, hasMore, onLoadMore, onRefresh,
  selectedItems, onToggleSelect, onToggleSelectAll,
  onBulkDelete, onBulkDownload,
  lightboxItem, setLightboxItem
}: HistorySidebarProps) {
  
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

  return (
    <>
      <aside className={`shrink-0 h-full bg-card transition-all duration-300 relative z-10 ${open ? 'w-[320px] border-r border-border' : 'w-0 overflow-hidden border-none'}`}>
        <div className="w-[320px] h-full flex flex-col relative">
          <div className="h-14 shrink-0 flex items-center justify-between px-4 border-b border-border font-mono text-[11px] tracking-widest text-muted-foreground whitespace-nowrap">
            OUTPUT LIBRARY
            <div className="flex gap-2">
              <button className="p-1 hover:text-foreground transition-colors" onClick={onRefresh} title="Refresh"><RefreshCcw size={14}/></button>
              <button className="p-1 hover:text-foreground transition-colors" onClick={onClose}><X size={16}/></button>
            </div>
          </div>
          
          <div className="flex-1 overflow-y-auto p-3">
            <div className="grid grid-cols-2 gap-2">
              {history.length === 0 ? (
                <div className="col-span-2 text-center text-muted-foreground text-xs p-10 border border-dashed border-border rounded-xl">
                  No history yet.<br/>Click START to begin.
                </div>
              ) : (
                history.map((item) => (
                  <div 
                    key={item.filename} 
                    className={`aspect-square bg-muted border rounded-xl cursor-pointer overflow-hidden relative flex items-center justify-center transition-all hover:-translate-y-[1px] ${selectedItems.has(item.filename) ? 'border-primary border-2' : 'border-border hover:border-primary/50'}`}
                  >
                    <div className={`absolute top-1.5 left-1.5 z-10 transition-opacity ${selectedItems.has(item.filename) ? 'opacity-100' : 'opacity-0 group-hover:opacity-100'}`} onClick={(e) => e.stopPropagation()}>
                      <Checkbox checked={selectedItems.has(item.filename)} onCheckedChange={(c) => onToggleSelect(item.filename, !!c)} />
                    </div>
                    <div className="w-full h-full relative flex items-center justify-center group" onClick={() => setLightboxItem(item)}>
                      {item.type === 'video' ? (
                        <>
                          <video src={item.url} muted loop playsInline preload="none" className="w-full h-full object-cover pointer-events-none" />
                          <div className="absolute inset-0 bg-black/20 flex items-center justify-center pointer-events-none">
                            <PlayCircle size={28} className="text-white/80" />
                          </div>
                        </>
                      ) : (
                        <img src={item.url} alt={item.filename} loading="lazy" className="w-full h-full object-cover pointer-events-none" />
                      )}
                    </div>
                  </div>
                ))
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
                <Checkbox checked={selectedItems.size === history.length} onCheckedChange={(c) => onToggleSelectAll(!!c)} />
                <span className="font-mono text-xs">{selectedItems.size}</span>
              </div>
              <div className="w-px h-5 bg-border" />
              <button className="text-foreground hover:text-primary transition-colors" onClick={onBulkDownload}><Download size={16} /></button>
              <button className="text-destructive hover:text-red-400 transition-colors" onClick={onBulkDelete}><Trash2 size={16} /></button>
            </div>
          )}
        </div>
      </aside>

      {/* Lightbox Modal */}
      <Dialog open={!!lightboxItem} onOpenChange={(o) => !o && setLightboxItem(null)}>
        <DialogContent className="max-w-5xl p-0 overflow-hidden border-none bg-black/95 shadow-2xl">
          <DialogTitle className="hidden">Preview</DialogTitle>
          <DialogDescription className="hidden">Lightbox preview of output</DialogDescription>
          {lightboxItem && (() => {
            const currentIndex = history.findIndex(h => h.filename === lightboxItem.filename);
            const hasPrev = currentIndex > 0;
            const hasNext = currentIndex < history.length - 1;

            return (
              <div className="flex items-center justify-center w-full h-[85vh] relative group">
                {hasPrev && (
                  <button className="absolute left-4 z-50 p-3 rounded-full bg-black/40 text-white hover:bg-black/80 transition-all opacity-0 group-hover:opacity-100 backdrop-blur-sm"
                    onClick={(e) => { e.stopPropagation(); setLightboxItem(history[currentIndex - 1]) }}>
                    <ChevronLeft size={32} />
                  </button>
                )}
                {hasNext && (
                  <button className="absolute right-4 z-50 p-3 rounded-full bg-black/40 text-white hover:bg-black/80 transition-all opacity-0 group-hover:opacity-100 backdrop-blur-sm"
                    onClick={(e) => { e.stopPropagation(); setLightboxItem(history[currentIndex + 1]) }}>
                    <ChevronRight size={32} />
                  </button>
                )}
                {lightboxItem.type === 'video' ? (
                  <video src={lightboxItem.url} controls autoPlay loop className="max-w-full max-h-full object-contain" />
                ) : (
                  <img src={lightboxItem.url} alt="Preview" className="max-w-full max-h-full object-contain" />
                )}
              </div>
            )
          })()}
        </DialogContent>
      </Dialog>
    </>
  );
}
