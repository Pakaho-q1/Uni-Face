import { useState, useEffect, useCallback, useMemo } from 'react';
import { Cloud, Search, Video, Image as ImageIcon, Check, Loader2, User, Folder, Tag, X } from 'lucide-react';
import { toast } from 'sonner';

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

  const toggleAssetSelection = (assetId: string) => {
    const next = new Set(selectedAssetIds);
    if (next.has(assetId)) next.delete(assetId);
    else next.add(assetId);
    setSelectedAssetIds(next);
  };

  const handleClearSelection = () => {
    setSelectedAssetIds(new Set());
  };

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
          <div className="flex items-center gap-2 shrink-0 relative">
            <div className="flex-1 relative">
              <div 
                className="flex items-center justify-between h-10 bg-secondary/40 border border-border rounded-md px-3 text-sm cursor-pointer hover:border-primary/50 transition-colors"
                onClick={() => setComboboxOpen(!comboboxOpen)}
              >
                <div className="flex items-center gap-2 overflow-hidden truncate">
                  {selectedId ? (
                    <>
                      {categoryType === 'people' && (
                        <img 
                          src={ENDPOINTS.IMMICH_PERSON_THUMB(selectedId, immichUrl, immichApiKey)} 
                          className="w-6 h-6 rounded-full object-cover border border-border bg-zinc-800"
                          alt="avatar"
                          onError={(e) => { e.currentTarget.style.display = 'none'; }}
                        />
                      )}
                      <span className="font-medium text-foreground truncate">{selectedItemLabel}</span>
                    </>
                  ) : (
                    <span className="text-muted-foreground text-xs">
                      {isCategoryLoading 
                        ? `Loading ${categoryType}...` 
                        : `Select ${categoryType === 'people' ? 'Person' : categoryType === 'albums' ? 'Album' : 'Tag'}...`}
                    </span>
                  )}
                </div>
                <Search size={14} className="text-muted-foreground shrink-0" />
              </div>

              {/* Combobox Dropdown Popover */}
              {comboboxOpen && (
                <div className="absolute top-11 left-0 right-0 z-50 bg-popover border border-border rounded-md shadow-2xl overflow-hidden max-h-60 flex flex-col animate-in fade-in-50 zoom-in-95">
                  <div className="p-2 border-b border-border bg-secondary/30 flex items-center gap-2">
                    <Search size={14} className="text-muted-foreground ml-1" />
                    <input
                      type="text"
                      autoFocus
                      placeholder={`Search ${categoryType}...`}
                      className="w-full bg-transparent text-xs text-foreground focus:outline-none placeholder:text-muted-foreground"
                      value={searchQuery}
                      onChange={(e) => setSearchQuery(e.target.value)}
                    />
                    {searchQuery && (
                      <button onClick={() => setSearchQuery('')} className="text-muted-foreground hover:text-foreground">
                        <X size={12} />
                      </button>
                    )}
                  </div>

                  <div className="overflow-y-auto p-1 max-h-48 custom-scrollbar">
                    {filteredItems.length === 0 ? (
                      <div className="text-center py-4 text-xs text-muted-foreground">
                        No {categoryType} found.
                      </div>
                    ) : (
                      filteredItems.map((item: any) => {
                        const isSelected = item.id === selectedId;
                        return (
                          <div
                            key={item.id}
                            className={`flex items-center justify-between p-2 rounded-md cursor-pointer text-xs transition-colors ${
                              isSelected ? 'bg-primary/20 text-primary font-medium' : 'hover:bg-secondary text-foreground'
                            }`}
                            onClick={() => {
                              setSelectedId(item.id);
                              setComboboxOpen(false);
                              setSearchQuery('');
                            }}
                          >
                            <div className="flex items-center gap-2.5 overflow-hidden truncate">
                              {categoryType === 'people' && (
                                <img 
                                  src={ENDPOINTS.IMMICH_PERSON_THUMB(item.id, immichUrl, immichApiKey)} 
                                  className="w-6 h-6 rounded-full object-cover border border-border shrink-0 bg-zinc-800" 
                                  alt={item.name}
                                  onError={(e) => { e.currentTarget.style.display = 'none'; }}
                                />
                              )}
                              <span className="truncate">{item.name || item.albumName}</span>
                            </div>
                            {item.assetCount !== undefined && (
                              <span className="text-[10px] font-mono text-muted-foreground ml-2">
                                {item.assetCount}
                              </span>
                            )}
                            {isSelected && <Check size={14} className="text-primary ml-2 shrink-0" />}
                          </div>
                        );
                      })
                    )}
                  </div>
                </div>
              )}
            </div>

            {/* Dynamic Primary Action Button */}
            <Button
              variant="default"
              className="h-10 px-4 shrink-0 font-mono text-xs tracking-wider bg-primary/20 text-primary hover:bg-primary/30 border border-primary/40 disabled:opacity-40"
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

          {/* Gallery Grid (Renders crisp image thumbnails for both photos & videos) */}
          <div className="flex-1 overflow-y-auto min-h-[300px] border border-border rounded-lg bg-black/50 p-3">
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
              <div className="grid grid-cols-3 sm:grid-cols-4 md:grid-cols-5 gap-3">
                {assets.map((asset) => {
                  const isSelected = selectedAssetIds.has(asset.id);
                  const isVid = asset.type === 'video';
                  const thumbUrl = ENDPOINTS.IMMICH_ASSET_THUMB(asset.id, immichUrl, immichApiKey);

                  return (
                    <div
                      key={asset.id}
                      className={`relative group aspect-square rounded-md overflow-hidden border-2 cursor-pointer transition-colors ${
                        isSelected 
                          ? 'border-primary shadow-[0_0_12px_rgba(var(--primary),0.3)]' 
                          : 'border-transparent hover:border-muted-foreground/50'
                      }`}
                      onClick={() => toggleAssetSelection(asset.id)}
                    >
                      {/* Checkbox Overlay */}
                      <div className={`absolute top-2 right-2 z-10 bg-background/80 rounded-sm border ${
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
                        <div className="absolute bottom-1 left-1 bg-black/70 rounded px-1.5 py-0.5 text-[10px] font-mono text-white flex items-center">
                          <Video size={10} className="mr-1 text-blue-400" /> {formatDuration(asset.duration)}
                        </div>
                      ) : (
                        <div className="absolute bottom-1 left-1 bg-black/70 rounded px-1.5 py-0.5 text-[10px] font-mono text-white flex items-center">
                          <ImageIcon size={10} className="mr-1 text-zinc-400" /> IMG
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
