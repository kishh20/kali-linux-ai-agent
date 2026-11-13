import React from 'react';
import { 
  Play, 
  Settings2, 
  Clock, 
  ShieldAlert, 
  CheckCircle2, 
  Sparkles,
  ArrowRight
} from 'lucide-react';
import { Practical } from '../types';

interface PracticalCardProps {
  practical: Practical;
  onSelect: (practical: Practical) => void;
  onQuickRun: (practical: Practical) => void;
  isExecuting?: boolean;
}

export const PracticalCard: React.FC<PracticalCardProps> = ({ 
  practical, 
  onSelect, 
  onQuickRun,
  isExecuting = false 
}) => {
  const categoryColors: Record<string, string> = {
    Administration: 'bg-blue-500/10 text-blue-400 border-blue-500/30',
    Scripting: 'bg-emerald-500/10 text-emerald-400 border-emerald-500/30',
    Security: 'bg-rose-500/10 text-rose-400 border-rose-500/30',
    Networking: 'bg-cyan-500/10 text-cyan-400 border-cyan-500/30',
    System: 'bg-purple-500/10 text-purple-400 border-purple-500/30',
  };

  const difficultyColors: Record<string, string> = {
    Beginner: 'text-emerald-400',
    Intermediate: 'text-amber-400',
    Advanced: 'text-rose-400',
  };

  const formattedNum = String(practical.number).padStart(2, '0');

  return (
    <div className="glass-card rounded-xl p-5 flex flex-col justify-between group hover:border-kali-cyan/50 hover:shadow-lg hover:shadow-kali-cyan/5 transition-all">
      <div>
        {/* Top Header: Number and Category */}
        <div className="flex items-center justify-between mb-3">
          <span className="font-mono text-sm font-bold text-kali-cyan px-2.5 py-0.5 rounded bg-kali-cyan/10 border border-kali-cyan/30">
            #{formattedNum}
          </span>
          <div className="flex items-center space-x-2">
            {practical.requires_sudo && (
              <span className="text-[10px] font-mono px-2 py-0.5 rounded bg-amber-500/10 text-amber-400 border border-amber-500/30">
                sudo
              </span>
            )}
            <span className={`text-[10px] font-mono px-2 py-0.5 rounded border ${categoryColors[practical.category] || 'bg-slate-800 text-slate-300 border-slate-700'}`}>
              {practical.category}
            </span>
          </div>
        </div>

        {/* Title */}
        <h3 className="font-semibold text-white text-base mb-2 group-hover:text-kali-cyan transition">
          {practical.title}
        </h3>

        {/* Aim / Description */}
        <p className="text-xs text-slate-400 line-clamp-2 leading-relaxed mb-4">
          {practical.aim}
        </p>
      </div>

      {/* Meta Footer & Buttons */}
      <div>
        <div className="flex items-center justify-between text-[11px] text-slate-500 mb-4 pb-3 border-b border-slate-800/80">
          <div className="flex items-center space-x-1.5">
            <Clock className="w-3.5 h-3.5" />
            <span>~{practical.estimated_minutes} mins</span>
          </div>
          <div className="flex items-center space-x-1">
            <span>Difficulty:</span>
            <span className={`font-medium ${difficultyColors[practical.difficulty] || 'text-slate-300'}`}>
              {practical.difficulty}
            </span>
          </div>
        </div>

        {/* Actions */}
        <div className="flex items-center space-x-2">
          <button
            onClick={() => onSelect(practical)}
            className="flex-1 flex items-center justify-center space-x-1.5 py-2 px-3 rounded-lg bg-slate-900 border border-slate-700 text-xs text-slate-300 font-medium hover:bg-slate-800 hover:text-white hover:border-slate-600 transition"
          >
            <Settings2 className="w-3.5 h-3.5 text-slate-400" />
            <span>Configure & Plan</span>
          </button>

          <button
            onClick={() => onQuickRun(practical)}
            disabled={isExecuting}
            className="flex items-center justify-center space-x-1.5 py-2 px-3.5 rounded-lg bg-kali-cyan text-black text-xs font-semibold hover:bg-kali-cyanHover disabled:opacity-50 disabled:cursor-not-allowed transition shadow-sm shadow-kali-cyan/20"
          >
            <Play className="w-3.5 h-3.5 fill-black" />
            <span>RUN</span>
          </button>
        </div>
      </div>
    </div>
  );
};
