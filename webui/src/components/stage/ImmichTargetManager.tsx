import React, { useState, useEffect, useCallback, useMemo, useRef } from 'react';
import { Cloud, Search, Video, Image as ImageIcon, Check, Loader2, User, Folder, Tag, X, ChevronDown } from 'lucide-react';
import { toast } from 'sonner';
import { useVirtualizer } from '@tanstack/react-virtual';

import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogDescription } from '@/components/ui/dialog';
import { Button } from '@/components/ui/button';
import { ENDPOINTS } from '@/config/endpoints';
import { api } from '@/services/api';
import type { 
  ImmichPerson, 
  ImmichAlbum, 
  ImmichTag, 
  ImmichAsset, 
  ImmichCategoryType, 
  TargetFile 
} from '@/types';

interface ImmichTargetManagerProps {
  open: boolean;
  onOpenChange: (open: boolean) => void;
  immichUrl: string;
  immichApiKey: string;
  immichLocalPath?: string;
  onSelectTargets: (files: TargetFile[]) => void;
}

function formatDuration(duration?: number): string {
  if (!duration || isNaN(duration)) return "MP4";
  const minutes = Math.floor(duration / 60);
  const seconds = Math.floor(duration % 60);
  return `${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`;
}

interface ImmichAssetCardProps {
  asset: ImmichAsset;
  isSelected: boolean;
  thumbUrl: string;
  onToggle: (id: string) => void;
}

const ImmichAssetCard = React.memo(function ImmichAssetCard({
  asset,
  isSelected,
  thumbUrl,
  onToggle,
}: ImmichAssetCardProps) {
  const isVid = asset.type === 'video';

  return (
    <div
      className={`relative group aspect-square rounded-md overflow-hidden border-2 cursor-pointer transition-colors ${
        isSelected 
          ? 'border-primary shadow-[0_0_12px_rgba(var(--primary),0.3)]' 
          : 'border-transparent hover:border-muted-foreground/50'
      }`}
      onClick={() => onToggle(asset.id)}
    >
      {/* Checkbox Overlay */}
      <div className={`absolute top-2 right-2 z-10 bg-background/80 rounded-sm border transition-opacity ${
        isSelected ? 'border-primary' : 'border-border opacity-0 group-hover:opacity-100'
      }`}>
        <div className="w-4 h-4 flex items-center justify-center">
          {isSelected && <div className="w-2 h-2 bg-primary rounded-sm" />}
        </div>
      </div>

      {/* Crisp Image Thumbnail from Immich */}
      <img 
        src={thumbUrl} 
        className="w-full h-full object-cover bg-zinc-900" 
        alt={asset.filename} 
        loading="lazy" 
        onError={(e) => {
          e.currentTarget.src = 'data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" width="40" height="40"><rect fill="%23222" width="40" height="40"/><text fill="%23666" x="50%" y="50%" dominant-baseline="middle" text-anchor="middle" font-size="10">ERR</text></svg>';
        }}
      />

      {/* Type Badge */}
      {isVid ? (
        <div className="absolute bottom-1 left-1 bg-black/70 rounded px-1.5 py-0.5 text-[10px] font-mono text-white flex items-center pointer-events-none">
          <Video size={10} className="mr-1 text-blue-400" /> {formatDuration(asset.duration)}
        </div>
      ) : (
        <div className="absolute bottom-1 left-1 bg-black/70 rounded px-1.5 py-0.5 text-[10px] font-mono text-white flex items-center pointer-events-none">
          <ImageIcon size={10} className="mr-1 text-zinc-400" /> IMG
        </div>
      )}
    </div>
  );
});

export function ImmichTargetManager({
  open,
  onOpenChange,
  immichUrl,
  immichApiKey,
  immichLocalPath,
  onSelectTargets
}: ImmichTargetManagerProps) {
  const [categoryType, setCategoryType] = useState<ImmichCategoryType>('people');
  
  // Category data
  const [people, setPeople] = useState<ImmichPerson[]>([]);
  const [albums, setAlbums] = useState<ImmichAlbum[]>([]);
  const [tags, setTags] = useState<ImmichTag[]>([]);
  const [isCategoryLoading, setIsCategoryLoading] = useState(false);

  // Selection
  const [selectedId, setSelectedId] = useState<string>('');
  const [searchQuery, setSearchQuery] = useState<string>('');
  const [comboboxOpen, setComboboxOpen] = useState(false);
  const containerRef = useRef<HTMLDivElement>(null);
  const searchInputRef = useRef<HTMLInputElement>(null);
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

  useEffect(() => {
    const handleClickOutside = (e: MouseEvent) => {
      if (containerRef.current && !containerRef.current.contains(e.target as Node)) {
        setComboboxOpen(false);
      }
    };
    document.addEventListener('mousedown', handleClickOutside);
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, []);

  useEffect(() => {
    if (comboboxOpen) {
      setTimeout(() => searchInputRef.current?.focus(), 50);
    } else {
      setSearchQuery('');
    }
  }, [comboboxOpen]);

  // Asset Gallery
  const [assets, setAssets] = useState<ImmichAsset[]>([]);
  const [isAssetsLoading, setIsAssetsLoading] = useState(false);
  const [selectedAssetIds, setSelectedAssetIds] = useState<Set<string>>(new Set());

  // Importing state
  const [isImporting, setIsImporting] = useState(false);

  // Load category list when modal opens or category type changes
  const fetchCategoryList = useCallback(async () => {
    if (!immichUrl || !immichApiKey) return;
    setIsCategoryLoading(true);
    try {
      if (categoryType === 'people') {
        const res = await api.getImmichPeople(immichUrl, immichApiKey);
        setPeople(res.people || []);
      } else if (categoryType === 'albums') {
        const res = await api.getImmichAlbums(immichUrl, immichApiKey);
        setAlbums(res.albums || []);
      } else if (categoryType === 'tags') {
        const res = await api.getImmichTags(immichUrl, immichApiKey);
        setTags(res.tags || []);
      }
    } catch (e: any) {
      console.error(e);
      toast.error(`Failed to load ${categoryType}`);
    } finally {
      setIsCategoryLoading(false);
    }
  }, [categoryType, immichUrl, immichApiKey]);

  useEffect(() => {
    if (open) {
      fetchCategoryList();
      setSelectedId('');
      setSearchQuery('');
      setAssets([]);
      setSelectedAssetIds(new Set());
    }
  }, [open, categoryType, fetchCategoryList]);

  // Load assets when selectedId changes
  useEffect(() => {
    if (!selectedId || !immichUrl || !immichApiKey) {
      setAssets([]);
      setSelectedAssetIds(new Set());
      return;
    }

    const loadAssets = async () => {
      setIsAssetsLoading(true);
      try {
        const res = await api.getImmichCategoryAssets(immichUrl, immichApiKey, categoryType, selectedId);
        setAssets(res.assets || []);
        setSelectedAssetIds(new Set());
      } catch (e: any) {
        console.error(e);
        toast.error('Failed to load media assets');
      } finally {
        setIsAssetsLoading(false);
      }
    };

    loadAssets();
  }, [selectedId, categoryType, immichUrl, immichApiKey]);

  // Reset scroll when category or selectedId changes
  useEffect(() => {
    if (scrollContainerRef.current) {
      scrollContainerRef.current.scrollTop = 0;
    }
  }, [selectedId, categoryType]);

  const rowCount = Math.ceil(assets.length / columns);
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

  // Filter items in Combobox based on search query
  const filteredItems = useMemo(() => {
    const query = searchQuery.toLowerCase().trim();
    if (categoryType === 'people') {
      return people.filter(p => p.name.toLowerCase().includes(query));
    }
    if (categoryType === 'albums') {
      return albums.filter(a => ((a.name || a.albumName || '').toLowerCase().includes(query)));
    }
    if (categoryType === 'tags') {
      return tags.filter(t => t.name.toLowerCase().includes(query));
    }
    return [];
  }, [categoryType, searchQuery, people, albums, tags]);

  // Selected item label
  const selectedItemLabel = useMemo(() => {
    if (!selectedId) return '';
    if (categoryType === 'people') {
      const p = people.find(item => item.id === selectedId);
      return p ? p.name : '';
    }
    if (categoryType === 'albums') {
      const a = albums.find(item => item.id === selectedId);
      return a ? (a.name || a.albumName || '') : '';
    }
    if (categoryType === 'tags') {
      const t = tags.find(item => item.id === selectedId);
      return t ? t.name : '';
    }
    return '';
  }, [selectedId, categoryType, people, albums, tags]);

  // Stable toggle callback with pure functional update: renders ONLY toggled item
  const toggleAssetSelection = useCallback((assetId: string) => {
    setSelectedAssetIds(prev => {
      const next = new Set(prev);
      if (next.has(assetId)) next.delete(assetId);
      else next.add(assetId);
      return next;
    });
  }, []);

  const handleClearSelection = useCallback(() => {
    setSelectedAssetIds(new Set());
  }, []);

  const handleToggleSelectAll = useCallback(() => {
    if (assets.length === 0) return;
    setSelectedAssetIds(prev => {
      if (prev.size === assets.length) {
        return new Set();
      }
      return new Set(assets.map(a => a.id));
    });
  }, [assets]);

  const handleUseTargets = async () => {
    if (assets.length === 0) return;
    
    // If specific assets selected, use them; otherwise use all assets
    const targetAssetIds = selectedAssetIds.size > 0 
      ? Array.from(selectedAssetIds) 
      : assets.map(a => a.id);

    setIsImporting(true);
    try {
      const res = await api.importImmichTargets(immichUrl, immichApiKey, targetAssetIds, immichLocalPath);
      if (res.success && res.imported.length > 0) {
        if (res.import_method === 'hardlink') {
          toast.success(`⚡ Instant Hardlink (0 MB used)`, {
            description: `Imported ${res.imported.length} target files via direct filesystem link`
          });
        } else if (res.import_method === 'download') {
          toast.success(`☁️ Download Complete`, {
            description: `Downloaded ${res.imported.length} target files from Immich Server`
          });
        } else {
          toast.success(res.message || `Imported ${res.imported.length} target files from Immich!`);
        }
        onSelectTargets(res.imported);
        onOpenChange(false);
      } else {
        toast.error(res.message || 'Failed to import target files');
      }
    } catch (e: any) {
      console.error(e);
      toast.error('Import failed', { description: e.message });
    } finally {
      setIsImporting(false);
    }
  };

  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      <DialogContent className="sm:max-w-[750px] bg-background border-border flex flex-col max-h-[88vh]">
        <DialogHeader>
          <DialogTitle className="font-mono tracking-widest flex items-center gap-2">
            <Cloud size={18} className="text-primary" /> IMMICH TARGET BROWSER
          </DialogTitle>
          <DialogDescription className="text-xs">
            Browse and import media from your Immich Library (People, Albums, Tags) directly into Uni-Face.
          </DialogDescription>
        </DialogHeader>

        <div className="flex flex-col gap-4 mt-2 overflow-hidden">
          
          {/* Category Tabs: People / Albums / Tags */}
          <div className="flex items-center gap-2 bg-secondary/50 p-1 rounded-lg border border-border">
            <button
              className={`flex-1 flex items-center justify-center gap-2 py-1.5 px-3 rounded-md text-xs font-mono transition-colors ${
                categoryType === 'people' 
                  ? 'bg-primary text-primary-foreground font-semibold shadow-sm' 
                  : 'text-muted-foreground hover:bg-background/50 hover:text-foreground'
              }`}
              onClick={() => { setCategoryType('people'); setSelectedId(''); }}
            >
              <User size={14} /> People (Faces)
            </button>
            <button
              className={`flex-1 flex items-center justify-center gap-2 py-1.5 px-3 rounded-md text-xs font-mono transition-colors ${
                categoryType === 'albums' 
                  ? 'bg-primary text-primary-foreground font-semibold shadow-sm' 
                  : 'text-muted-foreground hover:bg-background/50 hover:text-foreground'
              }`}
              onClick={() => { setCategoryType('albums'); setSelectedId(''); }}
            >
              <Folder size={14} /> Albums
            </button>
            <button
              className={`flex-1 flex items-center justify-center gap-2 py-1.5 px-3 rounded-md text-xs font-mono transition-colors ${
                categoryType === 'tags' 
                  ? 'bg-primary text-primary-foreground font-semibold shadow-sm' 
                  : 'text-muted-foreground hover:bg-background/50 hover:text-foreground'
              }`}
              onClick={() => { setCategoryType('tags'); setSelectedId(''); }}
            >
              <Tag size={14} /> Tags
            </button>
          </div>

          {/* Top Control Bar: Searchable Combobox & Action Button */}
          <div className="flex items-center gap-2 shrink-0">
            <div ref={containerRef} className="flex-1 min-w-0 relative">
              {/* Trigger Button */}
              <button
                type="button"
                disabled={isCategoryLoading}
                onClick={() => setComboboxOpen(prev => !prev)}
                className="flex h-9 w-full items-center justify-between rounded-md border border-input bg-background px-3 py-1 text-sm shadow-sm transition-colors hover:bg-secondary/50 focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-ring disabled:cursor-not-allowed disabled:opacity-50 text-left min-w-0"
              >
                <div className="flex items-center gap-2 min-w-0 flex-1 truncate">
                  {selectedId ? (
                    <>
                      {categoryType === 'people' && (
                        <img 
                          src={ENDPOINTS.IMMICH_PERSON_THUMB(selectedId, immichUrl, immichApiKey)} 
                          className="w-5 h-5 rounded-full object-cover border border-border bg-zinc-800 shrink-0"
                          alt="avatar"
                          onError={(e) => { e.currentTarget.style.display = 'none'; }}
                        />
                      )}
                      <span className="font-medium text-foreground truncate">{selectedItemLabel}</span>
                    </>
                  ) : (
                    <span className="text-muted-foreground text-xs truncate">
                      {isCategoryLoading 
                        ? `Loading ${categoryType}...` 
                        : `-- Select ${categoryType === 'people' ? 'Person' : categoryType === 'albums' ? 'Album' : 'Tag'} --`}
                    </span>
                  )}
                </div>
                <ChevronDown size={14} className={`shrink-0 ml-2 text-muted-foreground transition-transform duration-200 ${comboboxOpen ? 'rotate-180' : ''}`} />
              </button>

              {/* Combobox Dropdown Popover */}
              {comboboxOpen && (
                <div className="absolute top-full left-0 mt-1 w-full z-50 rounded-md border border-border bg-popover text-popover-foreground shadow-2xl overflow-hidden animate-in fade-in-0 zoom-in-95">
                  {/* Search Bar */}
                  <div className="p-2 border-b border-border flex items-center gap-2 bg-secondary/30">
                    <Search size={14} className="text-muted-foreground shrink-0" />
                    <input
                      ref={searchInputRef}
                      type="text"
                      placeholder={`Search ${categoryType}...`}
                      className="w-full bg-transparent text-xs text-foreground focus:outline-none placeholder:text-muted-foreground"
                      value={searchQuery}
                      onChange={(e) => setSearchQuery(e.target.value)}
                    />
                    {searchQuery && (
                      <button 
                        type="button"
                        onClick={() => setSearchQuery('')} 
                        className="text-muted-foreground hover:text-foreground"
                        title="Clear search"
                      >
                        <X size={12} />
                      </button>
                    )}
                  </div>

                  {/* Item List */}
                  <div className="max-h-52 overflow-y-auto custom-scrollbar p-1">
                    {selectedId && (
                      <button
                        type="button"
                        className="w-full text-left px-2.5 py-1.5 text-xs text-muted-foreground hover:text-destructive hover:bg-destructive/10 rounded-sm transition-colors flex items-center justify-between"
                        onClick={() => {
                          setSelectedId('');
                          setComboboxOpen(false);
                        }}
                      >
                        <span>-- Clear Selection --</span>
                        <X size={12} />
                      </button>
                    )}

                    {filteredItems.length === 0 ? (
                      <div className="py-4 text-center text-xs text-muted-foreground">
                        {searchQuery ? `No ${categoryType} found matching "${searchQuery}"` : `No ${categoryType} available`}
                      </div>
                    ) : (
                      filteredItems.map((item: any) => {
                        const isSelected = item.id === selectedId;
                        const name = item.name || item.albumName || '';
                        return (
                          <button
                            key={item.id}
                            type="button"
                            onClick={() => {
                              setSelectedId(item.id);
                              setComboboxOpen(false);
                            }}
                            className={`w-full text-left px-2.5 py-1.5 text-xs rounded-sm transition-colors flex items-center justify-between ${
                              isSelected 
                                ? 'bg-primary/20 text-primary font-medium' 
                                : 'hover:bg-secondary text-foreground'
                            }`}
                          >
                            <div className="flex items-center gap-2 min-w-0 flex-1 truncate mr-2">
                              {categoryType === 'people' && (
                                <img 
                                  src={ENDPOINTS.IMMICH_PERSON_THUMB(item.id, immichUrl, immichApiKey)} 
                                  className="w-5 h-5 rounded-full object-cover border border-border shrink-0 bg-zinc-800" 
                                  alt={item.name}
                                  onError={(e) => { e.currentTarget.style.display = 'none'; }}
                                />
                              )}
                              <span className="truncate">{name}</span>
                            </div>
                            <div className="flex items-center gap-1.5 shrink-0">
                              {item.assetCount !== undefined && (
                                <span className="text-[10px] font-mono text-muted-foreground">
                                  {item.assetCount}
                                </span>
                              )}
                              {isSelected && <Check size={14} className="shrink-0 text-primary" />}
                            </div>
                          </button>
                        );
                      })
                    )}
                  </div>

                  {/* Summary Footer */}
                  {filteredItems.length > 0 && (
                    <div className="px-2.5 py-1 text-[10px] text-muted-foreground bg-secondary/20 border-t border-border/50 flex justify-between">
                      <span>{filteredItems.length} of {categoryType === 'people' ? people.length : categoryType === 'albums' ? albums.length : tags.length} {categoryType}</span>
                    </div>
                  )}
                </div>
              )}
            </div>

            {/* Dynamic Primary Action Button */}
            <Button
              variant="default"
              className="h-9 px-4 shrink-0 font-mono text-xs tracking-wider bg-primary/20 text-primary hover:bg-primary/30 border border-primary/40 disabled:opacity-40"
              disabled={!selectedId || assets.length === 0 || isImporting || isAssetsLoading}
              onClick={handleUseTargets}
            >
              {isImporting ? (
                <><Loader2 size={14} className="animate-spin mr-2" /> IMPORTING...</>
              ) : selectedAssetIds.size > 0 ? (
                `USE ${selectedAssetIds.size} ITEM(S)`
              ) : (
                `USE ENTIRE SET (${assets.length})`
              )}
            </Button>
          </div>

          {/* Gallery Header */}
          <div className="flex items-center justify-between mt-1">
            <span className="text-xs font-mono tracking-wider text-muted-foreground uppercase">
              Gallery {assets.length > 0 && `(${assets.length} items)`}
            </span>
            <div className="flex items-center gap-2">
              {assets.length > 0 && (
                <Button
                  variant="ghost"
                  size="sm"
                  className="h-6 text-[10px] text-muted-foreground hover:text-foreground"
                  onClick={handleToggleSelectAll}
                >
                  {selectedAssetIds.size === assets.length ? 'Deselect All' : 'Select All'}
                </Button>
              )}
              {selectedAssetIds.size > 0 && (
                <Button
                  variant="ghost"
                  size="sm"
                  className="h-6 text-[10px] text-muted-foreground hover:text-foreground"
                  onClick={handleClearSelection}
                >
                  Clear Selection ({selectedAssetIds.size})
                </Button>
              )}
            </div>
          </div>

          {/* Virtualized Gallery Grid */}
          <div
            ref={scrollContainerRef}
            className="flex-1 overflow-y-auto min-h-[300px] max-h-[50vh] border border-border rounded-lg bg-black/50 p-3"
          >
            {isAssetsLoading ? (
              <div className="w-full h-full flex flex-col items-center justify-center text-muted-foreground gap-2 py-16">
                <Loader2 size={24} className="animate-spin text-primary" />
                <span className="text-xs font-mono">Loading media from Immich...</span>
              </div>
            ) : !selectedId ? (
              <div className="w-full h-full flex flex-col items-center justify-center text-muted-foreground text-xs opacity-50 py-16 text-center">
                <Cloud size={32} className="mb-2" />
                Select a {categoryType === 'people' ? 'person' : categoryType === 'albums' ? 'album' : 'tag'} above to view media.
              </div>
            ) : assets.length === 0 ? (
              <div className="w-full h-full flex flex-col items-center justify-center text-muted-foreground text-xs opacity-50 py-16 text-center">
                <ImageIcon size={32} className="mb-2" />
                No media found in this {categoryType.slice(0, -1)}.
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
                  const rowAssets = assets.slice(startIndex, startIndex + columns);

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
                      {rowAssets.map((asset) => (
                        <ImmichAssetCard
                          key={asset.id}
                          asset={asset}
                          isSelected={selectedAssetIds.has(asset.id)}
                          thumbUrl={ENDPOINTS.IMMICH_ASSET_THUMB(asset.id, immichUrl, immichApiKey)}
                          onToggle={toggleAssetSelection}
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
