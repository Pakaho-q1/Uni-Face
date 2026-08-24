import { useState, useCallback } from 'react';

export type HistoryItem = {
  filename: string;
  url: string;
  type: string;
  created_at: number;
}

export function useHistory(apiBase: string, platform: string) {
  const [history, setHistory] = useState<HistoryItem[]>([]);
  const [totalHistory, setTotalHistory] = useState<number>(0);
  const [historyPage, setHistoryPage] = useState<number>(0);
  const [hasMoreHistory, setHasMoreHistory] = useState<boolean>(true);
  const [selectedItems, setSelectedItems] = useState<Set<string>>(new Set());

  const fetchHistory = useCallback(async (page: number = 0, append: boolean = false) => {
    try {
      const limit = 30;
      const skip = page * limit;
      const res = await fetch(`${apiBase}/api/v1/history?skip=${skip}&limit=${limit}`, { 
        headers: { 'X-Client-Platform': platform } 
      });
      const data = await res.json();
      const formattedHistory = (data.history || []).map((item: any) => ({
        ...item,
        url: item.url.startsWith('http') ? item.url : `${apiBase}${item.url}`
      }));
      
      setTotalHistory(data.total || 0);
      setHasMoreHistory(formattedHistory.length === limit);
      
      if (append) {
        setHistory(prev => {
          // Prevent duplicates by checking filenames
          const existing = new Set(prev.map(p => p.filename));
          const newItems = formattedHistory.filter((h: HistoryItem) => !existing.has(h.filename));
          return [...prev, ...newItems];
        });
      } else {
        setHistory(formattedHistory);
      }
      setHistoryPage(page);
    } catch (e) {
      console.error("Failed to fetch history");
    }
  }, [apiBase, platform]);

  const bulkDelete = async () => {
    const files = Array.from(selectedItems);
    if (!files.length) return;
    
    const isDeletingAllVisible = files.length === history.length;
    const deleteAll = isDeletingAllVisible && totalHistory > history.length;
    
    let confirmMsg = `คุณต้องการลบผลลัพธ์จำนวน ${files.length} รายการ ใช่หรือไม่?`;
    if (deleteAll) {
      confirmMsg = `คุณเลือกรูปภาพทั้งหมดที่แสดงอยู่ (${files.length} รูป)\nคุณต้องการลบทั้งหมดที่มีในระบบ (${totalHistory} รูป) ใช่หรือไม่?\n\n(หากต้องการลบเฉพาะที่แสดง ให้กดยกเลิกแล้วเลือกทีละรูป)`;
    }
    
    if (!window.confirm(confirmMsg)) return;
    
    await fetch(`${apiBase}/api/v1/history`, {
      method: 'DELETE',
      headers: { 'Content-Type': 'application/json', 'X-Client-Platform': platform },
      body: JSON.stringify({ filenames: files, delete_all: deleteAll })
    });
    setSelectedItems(new Set());
    fetchHistory(0, false);
  };

  const bulkDownload = async () => {
    const files = Array.from(selectedItems);
    if (!files.length) return;
    
    const res = await fetch(`${apiBase}/api/v1/history/download`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', 'X-Client-Platform': platform },
      body: JSON.stringify({ filenames: files })
    });
    
    const blob = await res.blob();
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = files.length === 1 ? files[0] : `uni-face-export-${Date.now()}.zip`;
    document.body.appendChild(a);
    a.click();
    a.remove();
    window.URL.revokeObjectURL(url);
  };

  const toggleSelection = (filename: string, checked: boolean) => {
    const newSet = new Set(selectedItems);
    if (checked) newSet.add(filename);
    else newSet.delete(filename);
    setSelectedItems(newSet);
  };

  const toggleSelectAll = (checked: boolean) => {
    if (checked) {
      setSelectedItems(new Set(history.map(h => h.filename)));
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
