import { useState, useRef } from 'react';
import type { KeyboardEvent, ChangeEvent } from 'react';
import { X, Plus } from 'lucide-react';

interface TagInputProps {
  tags: string[];
  setTags: (tags: string[]) => void;
  placeholder?: string;
}

export function TagInput({ tags, setTags, placeholder = "Type & press Enter/Space/," }: TagInputProps) {
  const [inputValue, setInputValue] = useState('');
  const inputRef = useRef<HTMLInputElement>(null);
  
  const addTag = (value: string) => {
    const newTag = value.trim().replace(/,/g, '');
    if (newTag && !tags.includes(newTag)) {
      setTags([...tags, newTag]);
    }
    setInputValue('');
  };

  const handleKeyDown = (e: KeyboardEvent<HTMLInputElement>) => {
    if (e.key === 'Enter' || e.key === ',') {
      e.preventDefault();
      addTag(inputValue);
    } else if (e.key === 'Backspace' && inputValue === '' && tags.length > 0) {
      setTags(tags.slice(0, -1));
    }
  };

  const handleChange = (e: ChangeEvent<HTMLInputElement>) => {
    const val = e.target.value;
    if (val.endsWith(',') || val.endsWith(' ')) {
      addTag(val);
    } else {
      setInputValue(val);
    }
  };

  const removeTag = (tagToRemove: string) => {
    setTags(tags.filter(t => t !== tagToRemove));
  };

  return (
    <div className="flex flex-wrap items-center gap-2 p-2 border rounded-md bg-transparent focus-within:ring-1 focus-within:ring-ring">
      {tags.map(tag => (
        <span key={tag} className="inline-flex items-center gap-1 px-2 py-1 text-xs font-medium bg-secondary text-secondary-foreground rounded-full">
          {tag}
          <button
            type="button"
            className="text-muted-foreground hover:text-foreground transition-colors ml-1 focus:outline-none"
            onClick={() => removeTag(tag)}
          >
            <X size={12} />
          </button>
        </span>
      ))}
      <div className="flex flex-1 items-center gap-1 min-w-[120px]">
        <input
          ref={inputRef}
          type="text"
          value={inputValue}
          onChange={handleChange}
          onKeyDown={handleKeyDown}
          onBlur={() => addTag(inputValue)}
          placeholder={tags.length === 0 ? placeholder : ""}
          className="flex-1 border-0 focus-visible:ring-0 p-0 h-7 bg-transparent text-sm focus:outline-none"
        />
        {inputValue.trim() && (
          <button
            type="button"
            onMouseDown={(e) => { e.preventDefault(); addTag(inputValue); inputRef.current?.focus(); }}
            className="text-primary hover:bg-primary/20 p-1 rounded transition-colors"
          >
            <Plus size={16} />
          </button>
        )}
      </div>
    </div>
  );
}
