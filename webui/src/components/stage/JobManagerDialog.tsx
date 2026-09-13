import { useState, useEffect, useCallback, useRef } from 'react';
import { 
  ListTodo, 
  RotateCcw, 
  Trash2, 
  Square, 
  RefreshCw, 
  CheckCircle2, 
  AlertCircle, 
  Loader2, 
  User, 
  Clock, 
  Sparkles
} from 'lucide-react';
import { toast } from 'sonner';

import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogDescription } from '@/components/ui/dialog';
import { Button } from '@/components/ui/button';
import { API_BASE, ENDPOINTS } from '@/config';
import { api } from '@/services/api';
import type { JobRecord } from '@/types';

interface JobManagerDialogProps {
  open: boolean;
  onOpenChange: (open: boolean) => void;
  onJobStarted?: () => void;
}

type TabType = 'all' | 'active' | 'completed' | 'failed';

export function JobManagerDialog({ open, onOpenChange, onJobStarted }: JobManagerDialogProps) {
  const [jobs, setJobs] = useState<JobRecord[]>([]);
  const [serverActiveCount, setServerActiveCount] = useState<number>(0);
  const [loading, setLoading] = useState(false);
  const [currentTab, setCurrentTab] = useState<TabType>('all');
  const [actionLoading, setActionLoading] = useState<string | null>(null);
  
  const pollingRef = useRef<ReturnType<typeof setInterval> | null>(null);

  const fetchJobs = useCallback(async (showSpinner = false) => {
    if (showSpinner) setLoading(true);
    try {
      const data = await api.getJobs(currentTab === 'all' ? undefined : currentTab);
      setJobs(data.jobs || []);
      if (typeof data.active_count === 'number') {
        setServerActiveCount(data.active_count);
      }
    } catch (e: any) {
      console.error('Failed to fetch jobs', e);
    } finally {
      if (showSpinner) setLoading(false);
    }
  }, [currentTab]);

  useEffect(() => {
    if (open) {
      fetchJobs(true);
      // Auto-poll every 2.5 seconds while modal is open to see live progress
      pollingRef.current = setInterval(() => {
        fetchJobs(false);
      }, 2500);
    } else {
      if (pollingRef.current) clearInterval(pollingRef.current);
    }

    return () => {
      if (pollingRef.current) clearInterval(pollingRef.current);
    };
  }, [open, fetchJobs]);

  const handleCancel = async (jobId: string) => {
    setActionLoading(jobId);
    try {
      await api.cancelJob(jobId);
      toast.info('Job cancelled');
      await fetchJobs(false);
    } catch (e: any) {
      toast.error('Failed to cancel job', { description: e.message });
    } finally {
      setActionLoading(null);
    }
  };

  const handleRetry = async (jobId: string) => {
    setActionLoading(jobId);
    try {
      console.log(`[JobManager] Sending retry request for job: ${jobId}`);
      await api.retryJob(jobId);
      // In-place update card status immediately for instant UX feedback
      setJobs(prev => prev.map(j => j.id === jobId ? { ...j, status: 'pending', error: undefined } : j));
      toast.success('Job resumed in-place');
      // Switch to active tab so card doesn't vanish from failed filter
      if (currentTab === 'failed') {
        setCurrentTab('active');
      }
      if (onJobStarted) onJobStarted();
      await fetchJobs(false);
    } catch (e: any) {
      console.error(`[JobManager] Failed to retry job ${jobId}:`, e);
      toast.error('Failed to retry job', { description: e.message });
    } finally {
      setActionLoading(null);
    }
  };

  const handleRerun = async (jobId: string) => {
    setActionLoading(jobId);
    try {
      await api.rerunJob(jobId);
      toast.success('Job re-queued successfully');
      if (onJobStarted) onJobStarted();
      await fetchJobs(false);
    } catch (e: any) {
      toast.error('Failed to rerun job', { description: e.message });
    } finally {
      setActionLoading(null);
    }
  };

  const handleDelete = async (jobId: string) => {
    setActionLoading(jobId);
    try {
      await api.deleteJob(jobId);
      setJobs(prev => prev.filter(j => j.id !== jobId));
      toast.success('Job removed from history');
    } catch (e: any) {
      toast.error('Failed to delete job', { description: e.message });
    } finally {
      setActionLoading(null);
    }
  };

  const handleClearCompleted = async () => {
    try {
      const count = await api.clearCompletedJobs();
      toast.success(`Cleared ${count} finished jobs`);
      await fetchJobs(false);
    } catch (e: any) {
      toast.error('Failed to clear jobs', { description: e.message });
    }
  };

  const formatTimestamp = (ts?: string) => {
    if (!ts) return '';
    try {
      const date = new Date(ts.endsWith('Z') ? ts : `${ts}Z`);
      return date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit', second: '2-digit' });
    } catch {
      return ts;
    }
  };

  const activeCount = serverActiveCount;

  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      <DialogContent className="sm:max-w-[780px] w-full max-h-[88vh] flex flex-col p-4 md:p-6 bg-background border-border shadow-2xl">
        <DialogHeader className="shrink-0">
          <div className="flex items-center justify-between">
            <DialogTitle className="font-mono tracking-widest flex items-center gap-2 text-base md:text-lg">
              <ListTodo size={20} className="text-primary" /> JOB MANAGER
              {activeCount > 0 && (
                <span className="bg-primary/20 text-primary px-2 py-0.5 rounded-full text-xs font-mono animate-pulse">
                  {activeCount} active
                </span>
              )}
            </DialogTitle>
          </div>
          <DialogDescription className="text-xs text-muted-foreground">
            View status of all queued tasks, cancel running swaps, retry failed jobs, or rerun previous configs.
          </DialogDescription>
        </DialogHeader>

        {/* Filter Tabs & Quick Actions */}
        <div className="shrink-0 flex items-center justify-between gap-2 border-b border-border pb-3 pt-1">
          <div className="flex items-center gap-1 bg-secondary/50 p-1 rounded-lg border border-border">
            {(['all', 'active', 'completed', 'failed'] as TabType[]).map((tab) => (
              <button
                key={tab}
                className={`px-3 py-1 text-xs font-mono rounded-md transition-colors capitalize ${
                  currentTab === tab 
                    ? 'bg-primary text-primary-foreground font-semibold shadow-sm' 
                    : 'text-muted-foreground hover:bg-background/50 hover:text-foreground'
                }`}
                onClick={() => setCurrentTab(tab)}
              >
                {tab}
              </button>
            ))}
          </div>

          <div className="flex items-center gap-2">
            <Button 
              variant="ghost" 
              size="sm" 
              onClick={() => fetchJobs(true)} 
              disabled={loading}
              className="h-8 px-2.5 text-xs text-muted-foreground hover:text-foreground"
              title="Refresh"
            >
              <RefreshCw size={14} className={loading ? 'animate-spin text-primary' : ''} />
            </Button>
            <Button
              variant="outline"
              size="sm"
              onClick={handleClearCompleted}
              className="h-8 text-xs font-mono border-border text-muted-foreground hover:text-destructive hover:border-destructive/40"
            >
              <Trash2 size={13} className="mr-1" /> Clear Completed
            </Button>
          </div>
        </div>

        {/* Jobs List */}
        <div className="flex-1 overflow-y-auto custom-scrollbar flex flex-col gap-2.5 pr-1 min-h-[220px]">
          {loading && jobs.length === 0 ? (
            <div className="flex-1 flex flex-col items-center justify-center gap-2 py-16 text-muted-foreground text-xs">
              <Loader2 size={24} className="animate-spin text-primary" />
              <span>Loading jobs...</span>
            </div>
          ) : jobs.length === 0 ? (
            <div className="flex-1 flex flex-col items-center justify-center gap-3 py-16 text-muted-foreground text-center">
              <Sparkles size={36} className="opacity-30" />
              <div className="flex flex-col gap-1">
                <span className="text-sm font-medium text-foreground">No jobs in queue</span>
                <span className="text-xs">Jobs you run will appear here with live progress.</span>
              </div>
            </div>
          ) : (
            jobs.map((job) => {
              const isOngoing = job.status === 'processing' || job.status === 'pending';
              const isFailed = job.status === 'failed' || job.status === 'cancelled';
              const isCompleted = job.status === 'completed';
              const isCurrentAction = actionLoading === job.id;

              return (
                <div 
                  key={job.id} 
                  className={`flex flex-col gap-2.5 p-3 rounded-xl border transition-all ${
                    isOngoing 
                      ? 'bg-secondary/70 border-primary/40 shadow-sm' 
                      : 'bg-secondary/30 border-border/80 hover:border-border'
                  }`}
                >
                  {/* Row 1: Source Thumbnail, ID, Time, and Status Badge */}
                  <div className="flex items-center justify-between gap-3">
                    <div className="flex items-center gap-3 min-w-0 flex-1">
                      {/* Source Thumbnail */}
                      <div className="w-11 h-11 shrink-0 rounded-lg bg-background border border-border overflow-hidden flex items-center justify-center">
                        {job.source_type === 'image' && job.source_file_id ? (
                          <img 
                            src={`${API_BASE}${ENDPOINTS.UPLOAD_FILE(job.source_file_id)}`} 
                            alt={job.source_name || 'source'} 
                            className="w-full h-full object-cover"
                            onError={(e) => {
                              // Fallback on missing file
                              e.currentTarget.style.display = 'none';
                            }}
                          />
                        ) : (
                          <User size={18} className="text-muted-foreground" />
                        )}
                      </div>

                      {/* Job Metadata */}
                      <div className="flex flex-col min-w-0 flex-1">
                        <div className="flex items-center gap-2">
                          <span className="font-mono text-xs font-semibold text-foreground">
                            #{job.id.length > 20 ? job.id.slice(0, 8) : job.id}
                          </span>
                          <span className="text-[10px] font-mono text-muted-foreground flex items-center gap-1">
                            <Clock size={10} /> {formatTimestamp(job.created_at)}
                          </span>
                        </div>
                        <span className="text-xs text-muted-foreground truncate">
                          Source: <strong className="text-foreground font-normal">{job.source_name || 'Image'}</strong>
                          {job.target_summary && (
                            <> • Target: <span className="text-foreground">{job.target_summary}</span></>
                          )}
                        </span>
                      </div>
                    </div>

                    {/* Status Badge */}
                    <div className="shrink-0">
                      {isOngoing && (
                        <span className="bg-amber-500/15 text-amber-400 border border-amber-500/30 px-2.5 py-1 rounded-md text-[10px] font-mono font-semibold flex items-center gap-1.5 shadow-sm">
                          <Loader2 size={11} className="animate-spin" />
                          {job.status.toUpperCase()}
                        </span>
                      )}
                      {isCompleted && (
                        <span className="bg-emerald-500/15 text-emerald-400 border border-emerald-500/30 px-2.5 py-1 rounded-md text-[10px] font-mono font-semibold flex items-center gap-1.5 shadow-sm">
                          <CheckCircle2 size={12} />
                          COMPLETED
                        </span>
                      )}
                      {isFailed && (
                        <span className="bg-rose-500/15 text-rose-400 border border-rose-500/30 px-2.5 py-1 rounded-md text-[10px] font-mono font-semibold flex items-center gap-1.5 shadow-sm">
                          <AlertCircle size={12} />
                          {job.status.toUpperCase()}
                        </span>
                      )}
                    </div>
                  </div>

                  {/* Error display if failed */}
                  {job.error && (
                    <div className="text-[11px] font-mono text-rose-400 bg-rose-500/10 border border-rose-500/20 px-2.5 py-1.5 rounded-lg break-all">
                      {job.error}
                    </div>
                  )}

                  {/* Row 2: Progress bar, Counts, and Actions */}
                  <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2.5 pt-1 border-t border-border/40">
                    <div className="flex-1 flex flex-col gap-1 min-w-[140px]">
                      <div className="flex items-center justify-between text-[10px] font-mono text-muted-foreground">
                        <span>
                          {job.total_frames > 0 
                            ? `${job.frames_done}/${job.total_frames} frames` 
                            : `${job.target_count} target file(s)`}
                        </span>
                        <span className="font-semibold text-foreground">{job.progress.toFixed(1)}%</span>
                      </div>
                      <div className="w-full bg-background/80 h-1.5 rounded-full overflow-hidden border border-border/50">
                        <div 
                          className={`h-full transition-all duration-300 ${
                            isCompleted ? 'bg-emerald-500' : isFailed ? 'bg-rose-500' : 'bg-primary'
                          }`}
                          style={{ width: `${Math.min(100, Math.max(0, job.progress))}%` }}
                        />
                      </div>
                    </div>

                    {/* Contextual Action Buttons */}
                    <div className="flex items-center justify-end gap-2 shrink-0">
                      {isOngoing && (
                        <button
                          onClick={() => handleCancel(job.id)}
                          disabled={isCurrentAction}
                          className="h-8 px-3 rounded-lg bg-destructive/10 text-destructive hover:bg-destructive hover:text-white border border-destructive/20 text-xs font-mono font-medium flex items-center gap-1.5 transition-colors disabled:opacity-50"
                        >
                          {isCurrentAction ? <Loader2 size={12} className="animate-spin" /> : <Square size={11} fill="currentColor" />}
                          <span>Cancel</span>
                        </button>
                      )}

                      {isFailed && (
                        <button
                          onClick={() => handleRetry(job.id)}
                          disabled={isCurrentAction}
                          className="h-8 px-3 rounded-lg bg-secondary hover:bg-primary hover:text-primary-foreground border border-border text-xs font-mono font-medium flex items-center gap-1.5 transition-colors disabled:opacity-50"
                        >
                          {isCurrentAction ? <Loader2 size={12} className="animate-spin" /> : <RefreshCw size={12} />}
                          <span>Retry</span>
                        </button>
                      )}

                      {isCompleted && (
                        <button
                          onClick={() => handleRerun(job.id)}
                          disabled={isCurrentAction}
                          className="h-8 px-3 rounded-lg bg-primary/10 text-primary hover:bg-primary hover:text-primary-foreground border border-primary/30 text-xs font-mono font-medium flex items-center gap-1.5 transition-colors disabled:opacity-50"
                        >
                          {isCurrentAction ? <Loader2 size={12} className="animate-spin" /> : <RotateCcw size={12} />}
                          <span>Rerun</span>
                        </button>
                      )}

                      <button
                        onClick={() => handleDelete(job.id)}
                        disabled={isCurrentAction}
                        className="h-8 w-8 rounded-lg text-muted-foreground hover:text-destructive hover:bg-destructive/10 border border-transparent hover:border-destructive/20 flex items-center justify-center transition-colors disabled:opacity-50"
                        title="Delete Job"
                      >
                        <Trash2 size={14} />
                      </button>
                    </div>
                  </div>
                </div>
              );
            })
          )}
        </div>
      </DialogContent>
    </Dialog>
  );
}
