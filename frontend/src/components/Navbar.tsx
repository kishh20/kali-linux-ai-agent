import React from 'react';
import { 
  Terminal, 
  RotateCcw, 
  Trash2, 
  ShieldCheck, 
  ShieldAlert, 
  Activity,
  Play
} from 'lucide-react';
import { SystemStatus } from '../types';
import { resetTerminal, clearTerminal } from '../services/api';

interface NavbarProps {
  currentTab: string;
  systemStatus: SystemStatus | null;
  onOpenQuickLaunch: () => void;
  terminalConnected: boolean;
}

export const Navbar: React.FC<NavbarProps> = ({ 
  currentTab, 
  systemStatus, 
  onOpenQuickLaunch,
  terminalConnected 
}) => {
  const isKali = systemStatus?.is_kali ?? false;
  const isExecuting = systemStatus?.is_executing ?? false;

  const tabTitles: Record<string, string> = {
    dashboard: 'Dashboard Overview',
    practicals: 'All 25 Linux Practicals',
    history: 'Execution History & Lab Records',
    settings: 'Agent & Shell Settings',
    about: 'Architecture & Kali Specifications'
  };

  const handleReset = async () => {
    if (confirm('Restart interactive Kali Linux bash session? All current terminal background state will be reset.')) {
      await resetTerminal();
    }
  };

  const handleClear = async () => {
    await clearTerminal();
  };

  return (
    <header className="h-16 bg-kali-card border-b border-kali-border px-6 flex items-center justify-between z-10 shrink-0">
      {/* Title */}
      <div className="flex items-center space-x-4">
        <h2 className="text-lg font-semibold text-white tracking-tight">
          {tabTitles[currentTab] || 'Kali Automation Agent'}
        </h2>
        {isExecuting && (
          <div className="flex items-center space-x-2 px-2.5 py-1 rounded-full bg-kali-cyan/10 border border-kali-cyan/30 text-kali-cyan text-xs font-mono animate-pulse">
            <Activity className="w-3.5 h-3.5" />
            <span>Agent Executing...</span>
          </div>
        )}
      </div>

      {/* Badges and Quick Actions */}
      <div className="flex items-center space-x-3">
        {/* Kali OS Status Indicator */}
        <div 
          title={systemStatus?.diagnostics?.status_message || ''}
          className={`flex items-center space-x-1.5 px-3 py-1.5 rounded-lg border text-xs font-mono transition-all ${
            isKali 
              ? 'bg-kali-green/10 border-kali-green/30 text-kali-green' 
              : 'bg-amber-500/10 border-amber-500/30 text-amber-400'
          }`}
        >
          {isKali ? (
            <>
              <ShieldCheck className="w-3.5 h-3.5" />
              <span>Kali Linux Connected</span>
            </>
          ) : (
            <>
              <ShieldAlert className="w-3.5 h-3.5" />
              <span>{systemStatus?.diagnostics?.distro_name || 'Non-Kali OS'}</span>
            </>
          )}
        </div>

        {/* WebSocket Terminal Status */}
        <div className={`flex items-center space-x-1.5 px-3 py-1.5 rounded-lg border text-xs font-mono ${
          terminalConnected
            ? 'bg-slate-800/80 border-slate-700 text-slate-300'
            : 'bg-rose-950/40 border-rose-800/60 text-rose-400'
        }`}>
          <span className={`w-2 h-2 rounded-full ${terminalConnected ? 'bg-kali-green' : 'bg-rose-500'} ${terminalConnected ? 'animate-pulse' : ''}`} />
          <span>{terminalConnected ? 'PTY Live' : 'PTY Disconnected'}</span>
        </div>

        {/* Clear Terminal Button */}
        <button
          onClick={handleClear}
          title="Clear Terminal Screen (clear)"
          className="p-2 rounded-lg bg-slate-900 border border-slate-800 text-slate-400 hover:text-white hover:border-slate-700 transition"
        >
          <Trash2 className="w-4 h-4" />
        </button>

        {/* Reset Terminal Button */}
        <button
          onClick={handleReset}
          title="Reset & Respawn Bash Session"
          className="p-2 rounded-lg bg-slate-900 border border-slate-800 text-slate-400 hover:text-white hover:border-slate-700 transition"
        >
          <RotateCcw className="w-4 h-4" />
        </button>

        {/* Quick Launch Button */}
        <button
          onClick={onOpenQuickLaunch}
          className="flex items-center space-x-2 px-3.5 py-1.5 rounded-lg bg-kali-cyan text-black font-semibold text-xs hover:bg-kali-cyanHover transition shadow-md shadow-kali-cyan/20"
        >
          <Play className="w-3.5 h-3.5 fill-black" />
          <span>Select Practical</span>
        </button>
      </div>
    </header>
  );
};
