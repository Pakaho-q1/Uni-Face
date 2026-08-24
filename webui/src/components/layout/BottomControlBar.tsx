import { Square, CirclePlay, Video, VideoOff } from 'lucide-react';

interface BottomControlBarProps {
  running: boolean;
  uploading: boolean;
  progress: number;
  previewVisible: boolean;
  onToggleRun: () => void;
  onTogglePreview: () => void;
}

export function BottomControlBar({
  running,
  uploading,
  progress,
  previewVisible,
  visible = true,
  onToggleRun,
  onTogglePreview
}: BottomControlBarProps & { visible?: boolean }) {
  return (
    <div className={`fixed bottom-6 left-1/2 -translate-x-1/2 z-50 glass px-3 py-2 rounded-2xl flex items-center gap-3 w-11/12 max-w-md transition-all duration-300 ${visible ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-10 pointer-events-none'}`}>
      
      <button 
        className={`flex-1 flex items-center justify-center gap-2 py-3 px-4 rounded-xl font-mono text-sm tracking-widest font-bold transition-all active:scale-95 ${
          running 
            ? 'bg-destructive/10 text-destructive hover:bg-destructive hover:text-destructive-foreground border border-destructive/20' 
            : 'bg-primary text-primary-foreground hover:bg-primary/90 hover:shadow-[0_0_20px_rgba(var(--primary),0.4)]'
        }`}
        onClick={onToggleRun}
      >
        {running ? <Square size={18} fill="currentColor" /> : <CirclePlay size={18} fill="currentColor" />}
        <span>{uploading ? 'UPLOADING...' : (running ? 'CANCEL' : 'START')}</span>
      </button>

      {running && (
        <div className="absolute -top-3 left-1/2 -translate-x-1/2 w-[95%] h-1 bg-secondary rounded-full overflow-hidden">
          <div 
            className="h-full bg-primary transition-all duration-300 ease-out relative"
            style={{ width: `${progress}%` }}
          >
            <div className="absolute top-0 right-0 bottom-0 left-0 bg-white/20 animate-pulse" />
          </div>
        </div>
      )}

      <button 
        className={`shrink-0 flex items-center justify-center w-[120px] gap-2 py-3 px-4 rounded-xl font-mono text-[11px] tracking-wider transition-all border ${
          previewVisible 
            ? 'bg-transparent text-foreground border-border hover:bg-muted' 
            : 'bg-muted/50 text-muted-foreground border-transparent'
        }`}
        onClick={onTogglePreview}
      >
        {previewVisible ? <Video size={16} /> : <VideoOff size={16} />}
        <span>{previewVisible ? 'PREVIEW' : 'HIDDEN'}</span>
      </button>
    </div>
  );
}
