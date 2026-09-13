import { Settings2, LayoutGrid, ListTodo } from 'lucide-react';

interface TopNavProps {
  leftOpen: boolean;
  rightOpen: boolean;
  toggleLeft: () => void;
  toggleRight: () => void;
  openJobManager: () => void;
  activeJobCount: number;
}

export function TopNav({ 
  leftOpen, 
  rightOpen, 
  toggleLeft, 
  toggleRight,
  openJobManager,
  activeJobCount
}: TopNavProps) {
  return (
    <header className="h-14 shrink-0 flex items-center justify-between px-4 bg-card border-b border-border z-30">
      <button 
        className={`w-10 h-10 flex items-center justify-center rounded-lg transition-colors border ${
          leftOpen ? 'bg-primary/10 text-primary border-primary/30' : 'text-muted-foreground border-transparent hover:bg-muted hover:text-foreground'
        }`}
        onClick={toggleLeft}
        title="Output Library"
      >
        <LayoutGrid size={20} />
      </button>
      
      <div className="flex items-center gap-2 font-mono text-sm tracking-[0.2em] font-semibold text-foreground">
        <span className="text-primary text-[10px] rotate-45 inline-block">◆</span> UNI-FACE
      </div>
      
      <div className="flex items-center gap-1.5">
        <button 
          className="relative w-10 h-10 flex items-center justify-center rounded-lg transition-colors border text-muted-foreground border-transparent hover:bg-muted hover:text-foreground"
          onClick={openJobManager}
          title="Job Manager"
        >
          <ListTodo size={20} />
          {activeJobCount > 0 && (
            <span className="absolute -top-1 -right-1 min-w-[18px] h-[18px] px-1 bg-primary text-primary-foreground text-[10px] font-mono font-bold rounded-full flex items-center justify-center shadow-md animate-pulse">
              {activeJobCount}
            </span>
          )}
        </button>

        <button 
          className={`w-10 h-10 flex items-center justify-center rounded-lg transition-colors border ${
            rightOpen ? 'bg-primary/10 text-primary border-primary/30' : 'text-muted-foreground border-transparent hover:bg-muted hover:text-foreground'
          }`}
          onClick={toggleRight}
          title="Settings"
        >
          <Settings2 size={20} />
        </button>
      </div>
    </header>
  );
}

