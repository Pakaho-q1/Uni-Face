import { Settings2, LayoutGrid } from 'lucide-react';

interface TopNavProps {
  leftOpen: boolean;
  rightOpen: boolean;
  toggleLeft: () => void;
  toggleRight: () => void;
}

export function TopNav({ leftOpen, rightOpen, toggleLeft, toggleRight }: TopNavProps) {
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
      
      <button 
        className={`w-10 h-10 flex items-center justify-center rounded-lg transition-colors border ${
          rightOpen ? 'bg-primary/10 text-primary border-primary/30' : 'text-muted-foreground border-transparent hover:bg-muted hover:text-foreground'
        }`}
        onClick={toggleRight}
        title="Settings"
      >
        <Settings2 size={20} />
      </button>
    </header>
  );
}
