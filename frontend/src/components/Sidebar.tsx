import React from 'react';
import { 
  LayoutDashboard, 
  Terminal, 
  History, 
  Settings, 
  Info, 
  ShieldAlert, 
  CheckCircle2, 
  Cpu,
  Flame
} from 'lucide-react';
import { SystemStatus } from '../types';

interface SidebarProps {
  currentTab: string;
  setCurrentTab: (tab: string) => void;
  systemStatus: SystemStatus | null;
}

export const Sidebar: React.FC<SidebarProps> = ({ currentTab, setCurrentTab, systemStatus }) => {
  const isKali = systemStatus?.is_kali ?? false;
  const terminalActive = systemStatus?.terminal_active ?? false;
  const username = systemStatus?.diagnostics?.current_user || 'kali';

  const navItems = [
    { id: 'dashboard', label: 'Dashboard', icon: LayoutDashboard },
    { id: 'practicals', label: 'All Practicals', icon: Terminal, badge: '25' },
    { id: 'history', label: 'Execution History', icon: History, count: systemStatus?.completed_count },
    { id: 'settings', label: 'Settings', icon: Settings },
    { id: 'about', label: 'About', icon: Info },
  ];

  return (
    <aside className="w-64 bg-kali-card border-r border-kali-border flex flex-col h-screen select-none shrink-0 z-20">
      {/* Brand Header */}
      <div className="p-5 border-b border-kali-border flex items-center space-x-3">
        <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-kali-cyan via-kali-blue to-purple-600 flex items-center justify-center shadow-lg shadow-kali-cyan/20">
          <Flame className="w-6 h-6 text-black fill-black" />
        </div>
        <div>
          <div className="flex items-center space-x-1.5">
            <h1 className="font-bold text-white tracking-wide text-base">Kali AI Agent</h1>
            <span className="text-[10px] font-mono px-1.5 py-0.5 rounded bg-kali-cyan/10 text-kali-cyan border border-kali-cyan/30">
              v1.0
            </span>
          </div>
          <p className="text-xs text-kali-textMuted font-mono">Real PTY Automation</p>
        </div>
      </div>

      {/* Navigation */}
      <nav className="flex-1 p-3 space-y-1 overflow-y-auto">
        <div className="px-3 py-2 text-[11px] font-semibold tracking-wider text-slate-500 uppercase">
          Navigation
        </div>
        {navItems.map((item) => {
          const Icon = item.icon;
          const isActive = currentTab === item.id;
          return (
            <button
              key={item.id}
              onClick={() => setCurrentTab(item.id)}
              className={`w-full flex items-center justify-between px-3.5 py-2.5 rounded-lg text-sm font-medium transition-all ${
                isActive
                  ? 'bg-kali-cyan/15 text-kali-cyan border border-kali-cyan/30 shadow-sm'
                  : 'text-slate-300 hover:bg-slate-800/60 hover:text-white'
              }`}
            >
              <div className="flex items-center space-x-3">
                <Icon className={`w-4 h-4 ${isActive ? 'text-kali-cyan' : 'text-slate-400'}`} />
                <span>{item.label}</span>
              </div>
              {item.badge && (
                <span className="text-[10px] font-mono px-1.5 py-0.5 rounded bg-slate-800 text-slate-300 border border-slate-700">
                  {item.badge}
                </span>
              )}
              {item.count !== undefined && item.count > 0 && (
                <span className="text-[10px] font-mono px-1.5 py-0.5 rounded bg-kali-green/10 text-kali-green border border-kali-green/30">
                  {item.count}
                </span>
              )}
            </button>
          );
        })}
      </nav>

      {/* Kali System & Terminal Status Widget */}
      <div className="p-4 border-t border-kali-border bg-slate-950/40">
        <div className="text-[11px] font-semibold text-slate-500 uppercase tracking-wider mb-2">
          Host Environment
        </div>
        
        {/* OS Status */}
        <div className="flex items-center justify-between py-1.5 px-2 rounded bg-slate-900/60 border border-slate-800/80 mb-2">
          <div className="flex items-center space-x-2">
            <Cpu className="w-3.5 h-3.5 text-slate-400" />
            <span className="text-xs text-slate-300 truncate max-w-[110px]">
              {systemStatus?.diagnostics?.distro_name || 'Detecting...'}
            </span>
          </div>
          {isKali ? (
            <span className="flex items-center text-[10px] text-kali-green font-mono">
              <span className="w-1.5 h-1.5 rounded-full bg-kali-green mr-1 animate-pulse"></span>
              Kali
            </span>
          ) : (
            <span className="flex items-center text-[10px] text-amber-400 font-mono">
              <span className="w-1.5 h-1.5 rounded-full bg-amber-400 mr-1"></span>
              {systemStatus?.diagnostics?.os_name || 'Non-POSIX'}
            </span>
          )}
        </div>

        {/* PTY Session Status */}
        <div className="flex items-center justify-between py-1.5 px-2 rounded bg-slate-900/60 border border-slate-800/80">
          <div className="flex items-center space-x-2">
            <Terminal className="w-3.5 h-3.5 text-slate-400" />
            <span className="text-xs text-slate-300 truncate">
              {username}@bash
            </span>
          </div>
          <span className={`text-[10px] font-mono ${terminalActive ? 'text-kali-green' : 'text-slate-500'}`}>
            {terminalActive ? 'PTY Active' : 'Offline'}
          </span>
        </div>
      </div>
    </aside>
  );
};
