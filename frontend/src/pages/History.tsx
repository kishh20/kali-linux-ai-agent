import React, { useState } from 'react';
import { 
  History as HistoryIcon, 
  FileText, 
  Download, 
  Printer, 
  CheckCircle2, 
  XCircle, 
  Search,
  ExternalLink 
} from 'lucide-react';
import { HistoryRecord } from '../types';

interface HistoryProps {
  history: HistoryRecord[];
  onViewRecord: (record: HistoryRecord) => void;
}

export const History: React.FC<HistoryProps> = ({ history, onViewRecord }) => {
  const [search, setSearch] = useState('');

  const filtered = history.filter(
    (h) =>
      h.title.toLowerCase().includes(search.toLowerCase()) ||
      String(h.number).includes(search) ||
      h.status.toLowerCase().includes(search.toLowerCase())
  );

  return (
    <div className="flex-1 p-6 overflow-y-auto space-y-6">
      
      {/* Title */}
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-xl font-bold text-white tracking-tight flex items-center space-x-2">
            <HistoryIcon className="w-5 h-5 text-kali-cyan" />
            <span>Execution History & Generated Lab Records</span>
          </h2>
          <p className="text-xs text-slate-400 mt-1">
            Complete audit trail of all executed Kali Linux practicals, exit codes, raw outputs, and formatted academic reports.
          </p>
        </div>

        <div className="text-xs font-mono text-slate-400">
          Total Runs: <span className="text-kali-cyan font-bold">{history.length}</span>
        </div>
      </div>

      {/* Search Input */}
      <div className="relative w-full md:w-80">
        <Search className="w-4 h-4 text-slate-400 absolute left-3 top-1/2 -translate-y-1/2" />
        <input
          type="text"
          placeholder="Filter history records..."
          value={search}
          onChange={(e) => setSearch(e.target.value)}
          className="w-full pl-9 pr-3 py-2 rounded-lg bg-slate-900 border border-slate-700 text-xs text-white placeholder-slate-500 focus:outline-none focus:border-kali-cyan font-mono"
        />
      </div>

      {/* History Table */}
      <div className="glass-card rounded-xl border border-kali-border overflow-hidden">
        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs text-slate-300">
            <thead className="bg-slate-950/60 text-slate-400 font-mono uppercase text-[11px] border-b border-kali-border">
              <tr>
                <th className="py-3 px-4">#</th>
                <th className="py-3 px-4">Practical Title</th>
                <th className="py-3 px-4">Timestamp</th>
                <th className="py-3 px-4">Status</th>
                <th className="py-3 px-4">Duration</th>
                <th className="py-3 px-4">Commands</th>
                <th className="py-3 px-4 text-right">Actions</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-800/80">
              {filtered.length === 0 ? (
                <tr>
                  <td colSpan={7} className="py-12 text-center text-slate-500">
                    No matching execution records found.
                  </td>
                </tr>
              ) : (
                filtered.map((item) => {
                  const isSuccess = item.status === 'SUCCESS';
                  return (
                    <tr key={item.id} className="hover:bg-slate-900/40 transition">
                      <td className="py-3 px-4 font-mono font-bold text-kali-cyan">
                        #{String(item.number).padStart(2, '0')}
                      </td>
                      <td className="py-3 px-4 font-medium text-white">
                        {item.title}
                      </td>
                      <td className="py-3 px-4 font-mono text-slate-400">
                        {item.timestamp}
                      </td>
                      <td className="py-3 px-4">
                        <span className={`inline-flex items-center space-x-1 px-2 py-0.5 rounded text-[10px] font-mono font-semibold ${
                          isSuccess
                            ? 'bg-kali-green/10 text-kali-green border border-kali-green/30'
                            : 'bg-rose-500/10 text-rose-400 border border-rose-500/30'
                        }`}>
                          {isSuccess ? <CheckCircle2 className="w-3 h-3" /> : <XCircle className="w-3 h-3" />}
                          <span>{item.status}</span>
                        </span>
                      </td>
                      <td className="py-3 px-4 font-mono text-slate-400">
                        {item.duration_seconds}s
                      </td>
                      <td className="py-3 px-4 font-mono text-slate-400">
                        {item.commands?.length || 0} cmds
                      </td>
                      <td className="py-3 px-4 text-right">
                        <div className="flex items-center justify-end space-x-2">
                          <button
                            onClick={() => onViewRecord(item)}
                            className="flex items-center space-x-1 px-2.5 py-1 rounded bg-slate-800 text-slate-200 hover:bg-slate-700 text-xs font-medium transition"
                          >
                            <FileText className="w-3.5 h-3.5 text-kali-cyan" />
                            <span>Lab Record</span>
                          </button>
                          <a
                            href={`/api/history/${item.id}/html`}
                            target="_blank"
                            rel="noopener noreferrer"
                            className="p-1 rounded hover:bg-slate-800 text-slate-400 hover:text-white transition"
                            title="Print / View HTML"
                          >
                            <ExternalLink className="w-3.5 h-3.5" />
                          </a>
                        </div>
                      </td>
                    </tr>
                  );
                })
              )}
            </tbody>
          </table>
        </div>
      </div>

    </div>
  );
};
