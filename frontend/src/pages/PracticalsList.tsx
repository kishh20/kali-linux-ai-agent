import React, { useState } from 'react';
import { Search, Filter, Terminal, Sparkles } from 'lucide-react';
import { Practical } from '../types';
import { PracticalCard } from '../components/PracticalCard';

interface PracticalsListProps {
  practicals: Practical[];
  onSelectPractical: (practical: Practical) => void;
  onQuickRun: (practical: Practical) => void;
  isExecuting?: boolean;
}

export const PracticalsList: React.FC<PracticalsListProps> = ({
  practicals,
  onSelectPractical,
  onQuickRun,
  isExecuting = false
}) => {
  const [search, setSearch] = useState('');
  const [selectedCategory, setSelectedCategory] = useState<string>('All');
  const [selectedDifficulty, setSelectedDifficulty] = useState<string>('All');

  const categories = ['All', 'Administration', 'Scripting', 'Security', 'Networking', 'System'];
  const difficulties = ['All', 'Beginner', 'Intermediate', 'Advanced'];

  const filtered = practicals.filter((p) => {
    const matchesSearch =
      p.title.toLowerCase().includes(search.toLowerCase()) ||
      p.aim.toLowerCase().includes(search.toLowerCase()) ||
      String(p.number).includes(search);
    const matchesCategory = selectedCategory === 'All' || p.category === selectedCategory;
    const matchesDiff = selectedDifficulty === 'All' || p.difficulty === selectedDifficulty;
    return matchesSearch && matchesCategory && matchesDiff;
  });

  return (
    <div className="flex-1 p-6 overflow-y-auto space-y-6">
      
      {/* Title & Stats */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <h2 className="text-xl font-bold text-white tracking-tight flex items-center space-x-2">
            <Terminal className="w-5 h-5 text-kali-cyan" />
            <span>Complete Practical Curriculum</span>
            <span className="text-xs font-mono px-2 py-0.5 rounded bg-kali-cyan/10 text-kali-cyan border border-kali-cyan/30">
              25 Questions
            </span>
          </h2>
          <p className="text-xs text-slate-400 mt-1">
            Select any practical question to configure parameters, preview the AI execution sequence, and run live in Kali Linux.
          </p>
        </div>
      </div>

      {/* Search and Filters Bar */}
      <div className="glass-card rounded-xl p-4 border border-kali-border flex flex-col md:flex-row gap-4 items-center justify-between">
        
        {/* Search Input */}
        <div className="relative w-full md:w-96">
          <Search className="w-4 h-4 text-slate-400 absolute left-3 top-1/2 -translate-y-1/2" />
          <input
            type="text"
            placeholder="Search practicals by title, tool, or aim..."
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            className="w-full pl-9 pr-3 py-2 rounded-lg bg-slate-900 border border-slate-700 text-xs text-white placeholder-slate-500 focus:outline-none focus:border-kali-cyan font-mono"
          />
        </div>

        {/* Category Filter Pills */}
        <div className="flex items-center space-x-1.5 overflow-x-auto w-full md:w-auto pb-1 md:pb-0">
          {categories.map((cat) => (
            <button
              key={cat}
              onClick={() => setSelectedCategory(cat)}
              className={`px-3 py-1.5 rounded-lg text-xs font-medium whitespace-nowrap transition ${
                selectedCategory === cat
                  ? 'bg-kali-cyan text-black font-semibold shadow-sm shadow-kali-cyan/20'
                  : 'bg-slate-900 text-slate-400 hover:text-white hover:bg-slate-800'
              }`}
            >
              {cat}
            </button>
          ))}
        </div>

      </div>

      {/* Practicals Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-5">
        {filtered.map((practical) => (
          <PracticalCard
            key={practical.id}
            practical={practical}
            onSelect={onSelectPractical}
            onQuickRun={onQuickRun}
            isExecuting={isExecuting}
          />
        ))}
      </div>

      {filtered.length === 0 && (
        <div className="py-16 text-center text-slate-500 text-sm">
          No practical questions matched your search criteria.
        </div>
      )}

    </div>
  );
};
