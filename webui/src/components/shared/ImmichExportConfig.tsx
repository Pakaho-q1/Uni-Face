import { useState, useEffect, useCallback, useRef } from 'react';
import type { ChangeEvent } from 'react';
import { Search, ChevronDown, Check, X } from 'lucide-react';
import { Switch } from '@/components/ui/switch';
import { TagInput } from '@/components/ui/tag-input';
import { api } from '@/services/api';
import type { ImmichAlbum, ImmichTag } from '@/types';

interface ImmichExportConfigProps {
  isNewAlbum: boolean;
  onIsNewAlbumChange: (val: boolean) => void;
  albumName: string;
  onAlbumNameChange: (val: string) => void;
  tags: string[];
  onTagsChange: (val: string[]) => void;
  immichUrl: string;
  immichApiKey: string;
}

function SearchableAlbumSelect({
  value,
  onChange,
  albums,
  disabled,
  placeholder = "-- Select an Album --"
}: {
  value: string;
  onChange: (val: string) => void;
  albums: ImmichAlbum[];
  disabled?: boolean;
  placeholder?: string;
}) {
  const [open, setOpen] = useState(false);
  const [search, setSearch] = useState('');
  const containerRef = useRef<HTMLDivElement>(null);
  const searchInputRef = useRef<HTMLInputElement>(null);

  useEffect(() => {
    const handleClickOutside = (e: MouseEvent) => {
      if (containerRef.current && !containerRef.current.contains(e.target as Node)) {
        setOpen(false);
      }
    };
    document.addEventListener('mousedown', handleClickOutside);
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, []);

  useEffect(() => {
    if (open) {
      setTimeout(() => searchInputRef.current?.focus(), 50);
    } else {
      setSearch('');
    }
  }, [open]);

  const filteredAlbums = albums.filter(a => {
    const name = a.name || a.albumName || '';
    return name.toLowerCase().includes(search.toLowerCase());
  });

  return (
    <div ref={containerRef} className="relative w-full">
      {/* Trigger Button */}
      <button
        type="button"
        disabled={disabled}
        onClick={() => setOpen(prev => !prev)}
        className="flex h-9 w-full items-center justify-between rounded-md border border-input bg-background px-3 py-1 text-sm shadow-sm transition-colors hover:bg-secondary/50 focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-ring disabled:cursor-not-allowed disabled:opacity-50 text-left"
      >
        <span className={value ? "text-foreground truncate" : "text-muted-foreground truncate text-xs"}>
          {value || placeholder}
        </span>
        <ChevronDown size={14} className={`shrink-0 ml-2 text-muted-foreground transition-transform duration-200 ${open ? 'rotate-180' : ''}`} />
      </button>

      {/* Dropdown Popover */}
      {open && (
        <div className="absolute top-full left-0 mt-1 w-full z-50 rounded-md border border-border bg-popover text-popover-foreground shadow-2xl overflow-hidden animate-in fade-in-0 zoom-in-95">
          {/* Search Bar */}
          <div className="p-2 border-b border-border flex items-center gap-2 bg-secondary/30">
            <Search size={14} className="text-muted-foreground shrink-0" />
            <input
              ref={searchInputRef}
              type="text"
              placeholder="Search albums..."
              value={search}
              onChange={(e) => setSearch(e.target.value)}
              className="w-full bg-transparent text-xs focus:outline-none placeholder:text-muted-foreground"
            />
            {search && (
              <button 
                type="button"
                onClick={() => setSearch('')}
                className="text-muted-foreground hover:text-foreground"
                title="Clear search"
              >
                <X size={12} />
              </button>
            )}
          </div>

          {/* Album List */}
          <div className="max-h-52 overflow-y-auto custom-scrollbar p-1">
            {value && (
              <button
                type="button"
                className="w-full text-left px-2.5 py-1.5 text-xs text-muted-foreground hover:text-destructive hover:bg-destructive/10 rounded-sm transition-colors flex items-center justify-between"
                onClick={() => {
                  onChange('');
                  setOpen(false);
                }}
              >
                <span>-- Clear Selection --</span>
                <X size={12} />
              </button>
            )}

            {filteredAlbums.length === 0 ? (
              <div className="py-4 text-center text-xs text-muted-foreground">
                {search ? `No albums found matching "${search}"` : 'No albums available'}
              </div>
            ) : (
              filteredAlbums.map((a) => {
                const name = a.name || a.albumName || '';
                const isSelected = name === value;
                return (
                  <button
                    key={a.id}
                    type="button"
                    onClick={() => {
                      onChange(name);
                      setOpen(false);
                    }}
                    className={`w-full text-left px-2.5 py-1.5 text-xs rounded-sm transition-colors flex items-center justify-between ${
                      isSelected 
                        ? 'bg-primary/20 text-primary font-medium' 
                        : 'hover:bg-secondary text-foreground'
                    }`}
                  >
                    <span className="truncate mr-2">{name}</span>
                    {isSelected && <Check size={14} className="shrink-0 text-primary" />}
                  </button>
                );
              })
            )}
          </div>

          {albums.length > 0 && (
            <div className="px-2.5 py-1 text-[10px] text-muted-foreground bg-secondary/20 border-t border-border/50 flex justify-between">
              <span>{filteredAlbums.length} of {albums.length} albums</span>
            </div>
          )}
        </div>
      )}
    </div>
  );
}

export function ImmichExportConfig({
  isNewAlbum, onIsNewAlbumChange,
  albumName, onAlbumNameChange,
  tags, onTagsChange,
  immichUrl, immichApiKey
}: ImmichExportConfigProps) {
  const [remoteAlbums, setRemoteAlbums] = useState<ImmichAlbum[]>([]);
  const [remoteTags, setRemoteTags] = useState<ImmichTag[]>([]);
  const [isLoading, setIsLoading] = useState(false);

  const fetchImmichData = useCallback(async () => {
    if (!immichUrl || !immichApiKey) return;
    setIsLoading(true);
    try {
      const [albumData, tagData] = await Promise.all([
        api.getImmichAlbums(immichUrl, immichApiKey),
        api.getImmichTags(immichUrl, immichApiKey),
      ]);
      
      if (albumData.success) setRemoteAlbums(albumData.albums || []);
      if (tagData.success) setRemoteTags(tagData.tags || []);
    } catch (e) {
      console.error("Failed to fetch Immich data", e);
    } finally {
      setIsLoading(false);
    }
  }, [immichUrl, immichApiKey]);

  useEffect(() => {
    fetchImmichData();
  }, [fetchImmichData]);

  return (
    <div className="flex flex-col gap-4 p-4 border rounded-xl bg-card/50">
      <div className="flex items-center justify-between">
        <label className="text-sm font-medium">Create New Album</label>
        <Switch checked={isNewAlbum} onCheckedChange={onIsNewAlbumChange} />
      </div>

      <div className="flex flex-col gap-2">
        <div className="flex justify-between items-center">
          <label className="text-xs text-muted-foreground">
            {isNewAlbum ? 'New Album Name' : 'Select Existing Album'}
            {isLoading && !isNewAlbum && ' (Loading...)'}
          </label>
          <button type="button" onClick={fetchImmichData} className="text-xs text-blue-500 hover:underline" title="Refresh Albums and Tags">
            Refresh Lists
          </button>
        </div>
        
        {isNewAlbum ? (
          <input 
            type="text" 
            placeholder="e.g. Uni-Face Swaps" 
            value={albumName} 
            onChange={(e: ChangeEvent<HTMLInputElement>) => onAlbumNameChange(e.target.value)} 
            className="flex h-9 w-full rounded-md border border-input bg-transparent px-3 py-1 text-sm shadow-sm transition-colors placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-ring"
          />
        ) : (
          <SearchableAlbumSelect
            value={albumName}
            onChange={onAlbumNameChange}
            albums={remoteAlbums}
            disabled={isLoading}
          />
        )}
      </div>

      <div className="flex flex-col gap-2">
        <label className="text-xs text-muted-foreground">
          Tags 
          {isLoading && ' (Loading existing tags...)'}
        </label>
        <TagInput tags={tags} setTags={onTagsChange} placeholder="Add tag and press Enter..." />
        {!isLoading && remoteTags.length > 0 && (
          <div className="flex flex-wrap gap-1 mt-1">
            <span className="text-[10px] text-muted-foreground mr-1">Available tags:</span>
            {remoteTags.map(t => (
              <button 
                key={t.id} 
                className="text-[10px] bg-secondary px-1.5 rounded text-foreground hover:bg-primary/20 transition-colors"
                onClick={() => {
                  if (!tags.includes(t.name)) onTagsChange([...tags, t.name]);
                }}
              >
                {t.name}
              </button>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}
