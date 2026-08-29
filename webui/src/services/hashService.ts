/**
 * Chunked MD5 Hashing and Upload Orchestration Service
 */

import SparkMD5 from 'spark-md5';
import { api } from '@/services/api';

/**
 * Calculates MD5 hash of a large file using streaming chunks to prevent memory spikes.
 */
export function calculateFileHash(file: File, chunkSizeMB: number = 100): Promise<string> {
  return new Promise((resolve, reject) => {
    const chunkSize = Math.max(1, chunkSizeMB) * 1024 * 1024;
    const chunks = Math.ceil(file.size / chunkSize);
    let currentChunk = 0;
    const spark = new SparkMD5.ArrayBuffer();
    const fileReader = new FileReader();

    fileReader.onload = (e) => {
      if (e.target?.result) {
        spark.append(e.target.result as ArrayBuffer);
      }
      currentChunk++;
      if (currentChunk < chunks) {
        loadNext();
      } else {
        resolve(spark.end());
      }
    };
    fileReader.onerror = () => reject(fileReader.error);

    const loadNext = () => {
      const start = currentChunk * chunkSize;
      const end = Math.min(start + chunkSize, file.size);
      fileReader.readAsArrayBuffer(file.slice(start, end));
    };
    loadNext();
  });
}

/**
 * Orchestrates preflight check and batch upload for Target Sets.
 */
export async function uploadFilesToTargetSet(
  setName: string,
  files: FileList | File[],
  chunkSizeMB: number,
  onProgress?: (pct: number) => void
): Promise<void> {
  const fileArray = Array.from(files);
  if (fileArray.length === 0 || !setName) return;

  const fileHashes: { filename: string; hash: string; file: File }[] = [];
  const maxMemoryBytes = Math.max(1, chunkSizeMB) * 1024 * 1024;

  let currentBatch: File[] = [];
  let currentBatchMemory = 0;
  let completed = 0;

  const processBatch = async (batch: File[]) => {
    const batchPromises = batch.map(async (file) => {
      const hash = await calculateFileHash(file, chunkSizeMB);
      return { filename: file.name, hash, file };
    });
    const results = await Promise.all(batchPromises);
    fileHashes.push(...results);
    completed += batch.length;
    if (onProgress) onProgress((completed / fileArray.length) * 50);
  };

  for (let i = 0; i < fileArray.length; i++) {
    const file = fileArray[i];
    const footprint = Math.min(file.size, maxMemoryBytes);

    if (currentBatchMemory + footprint > maxMemoryBytes && currentBatch.length > 0) {
      await processBatch(currentBatch);
      currentBatch = [];
      currentBatchMemory = 0;
    }

    currentBatch.push(file);
    currentBatchMemory += footprint;
  }

  if (currentBatch.length > 0) {
    await processBatch(currentBatch);
  }

  // Preflight check
  if (onProgress) onProgress(60);
  const preflightData = await api.preflightTargetSet(
    fileHashes.map(f => ({ filename: f.filename, hash: f.hash }))
  );

  const exists = preflightData.results.filter(r => r.status === 'exists');
  const newFiles = preflightData.results.filter(r => r.status === 'new');

  // Link existing
  if (onProgress) onProgress(70);
  if (exists.length > 0) {
    await api.linkTargetSetFiles(setName, exists);
  }

  // Upload new
  if (onProgress) onProgress(80);
  if (newFiles.length > 0) {
    const fd = new FormData();
    newFiles.forEach(nf => {
      const originalObj = fileHashes.find(f => f.filename === nf.filename);
      if (originalObj) {
        fd.append('files', originalObj.file);
      }
    });
    await api.uploadTargetSetFiles(setName, fd);
  }

  if (onProgress) onProgress(100);
}
