/**
 * Custom hook for output history library management (pagination, bulk download, bulk delete).
 */

import { useState, useCallback } from 'react';
import { toast } from 'sonner';
import { api } from '@/services/api';
import type { HistoryItem } from '@/types';

export function useHistory() {
  const [history, setHistory] = useState<HistoryItem[]>([]);
  const [totalHistory, setTotalHistory] = useState<number>(0);
  const [historyPage, setHistoryPage] = useState<number>(0);
  const [hasMoreHistory, setHasMoreHistory] = useState<boolean>(true);
  const [selectedItems, setSelectedItems] = useState<Set<string>>(new Set());

  const fetchHistory = useCallback(async (page: number = 0, append: boolean = false) => {
    try {
      const limit = 30;
      const skip = page * limit;
      const data = await api.getHistory(skip, limit);
      
      setTotalHistory(data.total || 0);
      setHasMoreHistory((data.history || []).length === limit);
      
      if (append) {
        setHistory(prev => {
          const existing = new Set(prev.map(p => p.filename));
          const newItems = (data.history || []).filter((h: HistoryItem) => !existing.has(h.filename));
          return [...prev, ...newItems];
        });
      } else {
        setHistory(data.history || []);
      }
      setHistoryPage(page);
    } catch (e) {
      console.error("Failed to fetch history", e);
      toast.error("Failed to load output history");
    }
  }, []);

  const bulkDelete = async () => {
    const files = Array.from(selectedItems);
    if (!files.length) return;
    
    const deleteAll = files.length === totalHistory;
    
    let confirmMsg = `Are you sure you want to delete ${files.length} selected item(s)?`;
    if (deleteAll && totalHistory > history.length) {
      confirmMsg = `You selected all ${totalHistory} items in the database. Are you sure you want to delete ALL of them?`;
    }
    
    if (!window.confirm(confirmMsg)) return;
    
    try {
      await api.deleteHistory(files, deleteAll);
      toast.success(`Deleted ${files.length} item(s)`);
      setSelectedItems(new Set());
      fetchHistory(0, false);
    } catch (e: any) {
      toast.error("Failed to delete items", { description: e.message });
    }
  };

  const bulkDownload = async (): Promise<boolean> => {
    const files = Array.from(selectedItems);
    if (!files.length) return false;
    
    try {
      const blob = await api.downloadHistoryZip(files);
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = files.length === 1 ? files[0] : `uni-face-export-${Date.now()}.zip`;
      document.body.appendChild(a);
      a.click();
      a.remove();
      window.URL.revokeObjectURL(url);
      
      setSelectedItems(new Set());
      toast.success("Download started");
      return true;
    } catch (e: any) {
      console.error("Download failed", e);
      toast.error("Download failed", { description: e.message });
      return false;
    }
  };

  const toggleSelection = (filename: string, checked: boolean) => {
    const newSet = new Set(selectedItems);
    if (checked) newSet.add(filename);
    else newSet.delete(filename);
    setSelectedItems(newSet);
  };

  const toggleSelectAll = async (checked: boolean) => {
    if (checked) {
      if (history.length < totalHistory) {
        try {
          const data = await api.getHistory(0, 999999);
          setSelectedItems(new Set((data.history || []).map((h: HistoryItem) => h.filename)));
        } catch (e) {
          console.error("Failed to fetch all history for selection", e);
          toast.error("Failed to select all items");
        }
      } else {
        setSelectedItems(new Set(history.map(h => h.filename)));
      }
    } else {
      setSelectedItems(new Set());
    }
  };

  return {
    history,
    totalHistory,
    historyPage,
    setHistoryPage,
    hasMoreHistory,
    selectedItems,
    fetchHistory,
    bulkDelete,
    bulkDownload,
    toggleSelection,
    toggleSelectAll
  };
}
