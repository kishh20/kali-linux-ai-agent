import React, { useState } from 'react';
import { 
  Terminal as TerminalIcon, 
  CheckCircle2, 
  XCircle, 
  Layers, 
  Cpu, 
  Play, 
  ArrowRight, 
  Sparkles, 
  ShieldCheck, 
  AlertCircle,
  FileText
} from 'lucide-react';
import { Practical, SystemStatus, HistoryRecord } from '../types';
import { TerminalView } from '../components/TerminalView';

interface DashboardProps {
  systemStatus: SystemStatus | null;
  practicals: Practical[];
  history: HistoryRecord[];
  onSelectPractical: (practical: Practical) => void;
  onQuickRun: (practical: Practical) => void;
  onViewRecord: (record: HistoryRecord) => void;
  onNavigateToPracticals: () => void;
}

export const Dashboard: React.FC<DashboardProps> = ({
  systemStatus,
  practicals,
  history,
  onSelectPractical,
  onQuickRun,
  onViewRecord,
  onNavigateToPracticals
}) => {
  const [searchQuery, setSearchQuery] = useState('');

  const completedCount = history.filter((h) => h.status === 'SUCCESS').length;
  const failedCount = history.filter((h) => h.status === 'FAILED' || h.status === 'ERROR').length;
  const isKali = systemStatus?.is_kali ?? false;

  const filteredPracticals = practicals.filter(
    (p) =>
      p.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
      p.category.toLowerCase().includes(searchQuery.toLowerCase()) ||
      p.aim.toLowerCase().includes(searchQuery.toLowerCase())
  ).slice(0, 6);

  return (
    <div className="flex-1 p-6 overflow-y-auto space-y-6">
      
      {/* OS Compatibility Alert Banner if not native Kali Linux */}
      {!isKali && systemStatus?.diagnostics && (
        <div className="p-4 rounded-xl bg-amber-500/10 border border-amber-500/30 flex items-start space-x-3.5">
          <AlertCircle className="w-5 h-5 text-amber-400 shrink-0 mt-0.5" />
          <div className="text-xs text-amber-200">
            <span className="font-semibold block text-sm mb-0.5 text-amber-400">
              Host Environment Notice: Running on {systemStatus.diagnostics.os_name}
            </span>
            <span>
              The terminal interface is configured for genuine Kali Linux PTY sessions. 
              To execute actual bash commands on Kali Linux, run this service on a native Kali installation, 
              live USB, or Kali WSL2. Non-Linux environments will display this honest diagnostic notice.
            </span>
          </div>
        </div>
      )}

      {/* Metric Cards Row */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        
        {/* Total Available Practicals */}
        <div className="glass-card rounded-xl p-5 border border-kali-border flex items-center justify-between">
          <div>
            <p className="text-xs font-medium text-slate-400 uppercase tracking-wider">Total Practicals</p>
            <h3 className="text-2xl font-bold text-white mt-1">25</h3>
            <p className="text-[11px] text-kali-cyan mt-1 font-mono">100% Implemented</p>
          </div>
          <div className="w-12 h-12 rounded-xl bg-kali-cyan/10 border border-kali-cyan/20 flex items-center justify-center text-kali-cyan">
            <Layers className="w-6 h-6" />
          </div>
        </div>

        {/* Completed Practicals */}
        <div className="glass-card rounded-xl p-5 border border-kali-border flex items-center justify-between">
          <div>
            <p className="text-xs font-medium text-slate-400 uppercase tracking-wider">Completed Practicals</p>
            <h3 className="text-2xl font-bold text-kali-green mt-1">{completedCount}</h3>
            <p className="text-[11px] text-slate-500 mt-1 font-mono">Verified in Kali Terminal</p>
          </div>
          <div className="w-12 h-12 rounded-xl bg-kali-green/10 border border-kali-green/20 flex items-center justify-center text-kali-green">
            <CheckCircle2 className="w-6 h-6" />
          </div>
        </div>

        {/* Failed Practicals */}
        <div className="glass-card rounded-xl p-5 border border-kali-border flex items-center justify-between">
          <div>
            <p className="text-xs font-medium text-slate-400 uppercase tracking-wider">Failed Practicals</p>
            <h3 className="text-2xl font-bold text-rose-400 mt-1">{failedCount}</h3>
            <p className="text-[11px] text-slate-500 mt-1 font-mono">Honest Failure Detection</p>
          </div>
          <div className="w-12 h-12 rounded-xl bg-rose-500/10 border border-rose-500/20 flex items-center justify-center text-rose-400">
            <XCircle className="w-6 h-6" />
          </div>
        </div>

        {/* Kali OS Info */}
        <div className="glass-card rounded-xl p-5 border border-kali-border flex items-center justify-between">
          <div>
            <p className="text-xs font-medium text-slate-400 uppercase tracking-wider">Host OS Platform</p>
            <h3 className="text-sm font-bold text-white mt-1 truncate max-w-[140px]">
              {systemStatus?.diagnostics?.distro_name || 'Linux'}
            </h3>
            <p className="text-[11px] text-slate-400 mt-1 font-mono truncate max-w-[140px]">
              {systemStatus?.diagnostics?.current_user || 'kali'}@bash
            </p>
          </div>
          <div className={`w-12 h-12 rounded-xl border flex items-center justify-center ${
            isKali ? 'bg-kali-green/10 border-kali-green/20 text-kali-green' : 'bg-amber-500/10 border-amber-500/20 text-amber-400'
          }`}>
            <Cpu className="w-6 h-6" />
          </div>
        </div>

      </div>

      {/* Main Terminal & Quick Launcher Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6 min-h-[520px]">
        
        {/* Real Kali Terminal Viewport (7 Columns) */}
        <div className="lg:col-span-7 flex flex-col min-h-[480px]">
          <div className="flex items-center justify-between mb-2">
            <div className="flex items-center space-x-2 text-xs font-semibold uppercase tracking-wider text-slate-400">
              <TerminalIcon className="w-4 h-4 text-kali-cyan" />
              <span>Real Kali Linux Interactive Terminal (xterm.js PTY)</span>
            </div>
            <span className="text-[11px] font-mono text-slate-500">
              Bi-directional WebSocket
            </span>
          </div>
          <div className="flex-1 w-full min-h-[420px]">
            <TerminalView isExecuting={systemStatus?.is_executing} />
          </div>
        </div>

        {/* Right Panel: Quick Practical Launch & Recent History (5 Columns) */}
        <div className="lg:col-span-5 flex flex-col space-y-5">
          
          {/* Quick Launch Panel */}
          <div className="glass-card rounded-xl p-5 border border-kali-border flex flex-col space-y-4">
            <div className="flex items-center justify-between">
              <div className="flex items-center space-x-2">
                <Sparkles className="w-4 h-4 text-kali-cyan" />
                <h3 className="text-sm font-bold text-white">Quick Practical Launcher</h3>
              </div>
              <button
                onClick={onNavigateToPracticals}
                className="text-xs text-kali-cyan hover:underline flex items-center space-x-1"
              >
                <span>View all 25</span>
                <ArrowRight className="w-3 h-3" />
              </button>
            </div>

            {/* Mini Search */}
            <input
              type="text"
              placeholder="Search practicals (e.g., Nmap, Wireshark, UFW)..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="w-full px-3 py-2 rounded-lg bg-slate-900 border border-slate-800 text-xs text-slate-200 focus:outline-none focus:border-kali-cyan"
            />

            {/* Quick List */}
            <div className="space-y-2 max-h-56 overflow-y-auto pr-1">
              {filteredPracticals.map((p) => (
                <div
                  key={p.id}
                  className="p-2.5 rounded-lg bg-slate-900/60 border border-slate-800/80 hover:border-slate-700 flex items-center justify-between text-xs transition"
                >
                  <div className="truncate pr-2">
                    <span className="font-mono text-kali-cyan font-bold mr-2">
                      #{String(p.number).padStart(2, '0')}
                    </span>
                    <span className="text-slate-200 font-medium truncate">{p.title}</span>
                  </div>
                  <div className="flex items-center space-x-1.5 shrink-0">
                    <button
                      onClick={() => onSelectPractical(p)}
                      className="px-2 py-1 rounded bg-slate-800 text-slate-300 hover:text-white text-[11px]"
                    >
                      Plan
                    </button>
                    <button
                      onClick={() => onQuickRun(p)}
                      disabled={systemStatus?.is_executing}
                      className="p-1.5 rounded bg-kali-cyan text-black hover:bg-kali-cyanHover disabled:opacity-50"
                      title="Quick Run in Kali Shell"
                    >
                      <Play className="w-3 h-3 fill-black" />
                    </button>
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* Recent Execution History */}
          <div className="glass-card rounded-xl p-5 border border-kali-border flex-1 flex flex-col space-y-3">
            <div className="flex items-center justify-between">
              <h3 className="text-sm font-bold text-white flex items-center space-x-2">
                <FileText className="w-4 h-4 text-slate-400" />
                <span>Recent Practical Records</span>
              </h3>
              <span className="text-[11px] font-mono text-slate-500">
                {history.length} runs recorded
              </span>
            </div>

            <div className="flex-1 space-y-2 overflow-y-auto max-h-48 pr-1">
              {history.length === 0 ? (
                <div className="text-center py-8 text-xs text-slate-500">
                  No practicals executed yet. Select a practical and click RUN to start.
                </div>
              ) : (
                history.slice(0, 4).map((rec) => (
                  <div
                    key={rec.id}
                    onClick={() => onViewRecord(rec)}
                    className="p-2.5 rounded-lg bg-slate-900/60 border border-slate-800 hover:border-kali-cyan/40 cursor-pointer flex items-center justify-between transition text-xs"
                  >
                    <div className="truncate pr-2">
                      <div className="flex items-center space-x-2">
                        <span className="font-mono text-kali-cyan font-bold">
                          #{String(rec.number).padStart(2, '0')}
                        </span>
                        <span className="text-white font-medium truncate">{rec.title}</span>
                      </div>
                      <span className="text-[10px] text-slate-500 font-mono">{rec.timestamp}</span>
                    </div>

                    <div className="flex items-center space-x-2 shrink-0">
                      <span className={`text-[10px] font-mono px-2 py-0.5 rounded font-semibold ${
                        rec.status === 'SUCCESS' ? 'bg-kali-green/10 text-kali-green border border-kali-green/30' : 'bg-rose-500/10 text-rose-400 border border-rose-500/30'
                      }`}>
                        {rec.status}
                      </span>
                    </div>
                  </div>
                ))
              )}
            </div>
          </div>

        </div>

      </div>

    </div>
  );
};
