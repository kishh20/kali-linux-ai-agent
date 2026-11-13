import React, { useState } from 'react';
import { 
  X, 
  Copy, 
  Download, 
  Printer, 
  Check, 
  FileText, 
  Code, 
  Terminal, 
  ShieldCheck, 
  ShieldAlert 
} from 'lucide-react';
import { HistoryRecord } from '../types';

interface LabRecordModalProps {
  record: HistoryRecord | null;
  isOpen: boolean;
  onClose: () => void;
}

export const LabRecordModal: React.FC<LabRecordModalProps> = ({ record, isOpen, onClose }) => {
  if (!isOpen || !record) return null;

  const [activeTab, setActiveTab] = useState<'rendered' | 'markdown'>('rendered');
  const [copied, setCopied] = useState(false);

  const isSuccess = record.status === 'SUCCESS';

  const handleCopyMarkdown = () => {
    if (record.markdown_record) {
      navigator.clipboard.writeText(record.markdown_record);
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    }
  };

  const handleDownloadMarkdown = () => {
    if (!record.markdown_record) return;
    const blob = new Blob([record.markdown_record], { type: 'text/markdown;charset=utf-8' });
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.download = `Practical_${record.number}_${record.title.replace(/\s+/g, '_')}_Record.md`;
    link.click();
    URL.revokeObjectURL(url);
  };

  const handlePrint = () => {
    window.open(`/api/history/${record.id}/html`, '_blank');
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/85 backdrop-blur-sm animate-in fade-in duration-150">
      <div className="relative w-full max-w-4xl max-h-[92vh] bg-kali-card border border-kali-border rounded-2xl shadow-2xl flex flex-col overflow-hidden">
        
        {/* Header */}
        <div className="p-6 border-b border-kali-border flex items-center justify-between bg-slate-900/60">
          <div className="flex items-center space-x-3">
            <div className="p-2.5 rounded-xl bg-kali-cyan/10 border border-kali-cyan/30 text-kali-cyan">
              <FileText className="w-5 h-5" />
            </div>
            <div>
              <div className="flex items-center space-x-2">
                <span className="font-mono text-xs font-bold text-kali-cyan">
                  EXPERIMENT #{String(record.number).padStart(2, '0')}
                </span>
                <span className={`text-[10px] font-mono px-2 py-0.5 rounded font-semibold ${
                  isSuccess ? 'bg-kali-green/15 text-kali-green border border-kali-green/30' : 'bg-rose-500/15 text-rose-400 border border-rose-500/30'
                }`}>
                  {record.status}
                </span>
              </div>
              <h2 className="text-lg font-bold text-white tracking-tight">
                {record.title}
              </h2>
            </div>
          </div>

          <div className="flex items-center space-x-2">
            <button
              onClick={handlePrint}
              title="Print / PDF View"
              className="p-2 rounded-lg bg-slate-900 border border-slate-700 text-slate-300 hover:text-white transition"
            >
              <Printer className="w-4 h-4" />
            </button>
            <button
              onClick={handleDownloadMarkdown}
              title="Download Markdown Record"
              className="p-2 rounded-lg bg-slate-900 border border-slate-700 text-slate-300 hover:text-white transition"
            >
              <Download className="w-4 h-4" />
            </button>
            <button
              onClick={handleCopyMarkdown}
              title="Copy Markdown"
              className="p-2 rounded-lg bg-slate-900 border border-slate-700 text-slate-300 hover:text-white transition"
            >
              {copied ? <Check className="w-4 h-4 text-kali-green" /> : <Copy className="w-4 h-4" />}
            </button>
            <button
              onClick={onClose}
              className="p-2 rounded-lg text-slate-400 hover:text-white hover:bg-slate-800 transition"
            >
              <X className="w-5 h-5" />
            </button>
          </div>
        </div>

        {/* Tabs */}
        <div className="px-6 border-b border-kali-border bg-slate-950/40 flex items-center space-x-2">
          <button
            onClick={() => setActiveTab('rendered')}
            className={`py-3 px-4 border-b-2 text-xs font-medium transition ${
              activeTab === 'rendered'
                ? 'border-kali-cyan text-kali-cyan'
                : 'border-transparent text-slate-400 hover:text-slate-200'
            }`}
          >
            Formatted Practical Record
          </button>
          <button
            onClick={() => setActiveTab('markdown')}
            className={`py-3 px-4 border-b-2 text-xs font-medium transition ${
              activeTab === 'markdown'
                ? 'border-kali-cyan text-kali-cyan'
                : 'border-transparent text-slate-400 hover:text-slate-200'
            }`}
          >
            Raw Markdown
          </button>
        </div>

        {/* Body */}
        <div className="flex-1 p-6 overflow-y-auto space-y-6 text-sm">
          {activeTab === 'rendered' ? (
            <div className="space-y-6">
              
              {/* Aim */}
              <div>
                <h3 className="text-xs font-bold text-kali-cyan uppercase tracking-wider mb-1.5 flex items-center space-x-1.5">
                  <span>1. AIM</span>
                </h3>
                <div className="p-3.5 rounded-lg bg-slate-900/80 border border-slate-800 text-slate-200 text-xs leading-relaxed">
                  {record.aim}
                </div>
              </div>

              {/* Algorithm */}
              <div>
                <h3 className="text-xs font-bold text-kali-cyan uppercase tracking-wider mb-1.5">
                  2. ALGORITHM
                </h3>
                <div className="p-3.5 rounded-lg bg-slate-900/80 border border-slate-800 space-y-1 text-xs text-slate-300">
                  {Array.isArray(record.algorithm) ? (
                    record.algorithm.map((step, idx) => (
                      <div key={idx} className="flex items-start space-x-2">
                        <span className="text-slate-500 font-mono select-none">{idx + 1}.</span>
                        <span>{step.replace(/^\d+\.\s*/, '')}</span>
                      </div>
                    ))
                  ) : (
                    <p>{record.algorithm}</p>
                  )}
                </div>
              </div>

              {/* Commands Executed */}
              <div>
                <h3 className="text-xs font-bold text-kali-cyan uppercase tracking-wider mb-1.5">
                  3. COMMANDS EXECUTED IN KALI TERMINAL
                </h3>
                <div className="p-3.5 rounded-lg bg-[#07090e] border border-slate-800 font-mono text-xs text-kali-green space-y-1 overflow-x-auto">
                  {record.commands.map((cmd, idx) => (
                    <div key={idx} className="flex items-start space-x-2">
                      <span className="text-slate-500 select-none">$</span>
                      <span className="text-slate-200">{cmd}</span>
                    </div>
                  ))}
                </div>
              </div>

              {/* Actual Terminal Output */}
              <div>
                <h3 className="text-xs font-bold text-kali-cyan uppercase tracking-wider mb-1.5 flex items-center justify-between">
                  <span>4. ACTUAL TERMINAL OUTPUT</span>
                  <span className="text-[10px] text-slate-500 font-mono font-normal">Genuine Kali Linux PTY Stream</span>
                </h3>
                <pre className="p-4 rounded-lg bg-[#07090e] border border-slate-800 font-mono text-xs text-slate-300 whitespace-pre-wrap max-h-72 overflow-y-auto leading-relaxed">
                  {record.output || '[No output recorded]'}
                </pre>
              </div>

              {/* Explanation & Technical Analysis */}
              <div>
                <h3 className="text-xs font-bold text-kali-cyan uppercase tracking-wider mb-1.5">
                  5. TECHNICAL ANALYSIS & COMMAND EXPLANATION
                </h3>
                <div className="p-3.5 rounded-lg bg-slate-900/80 border border-slate-800 text-xs text-slate-300 leading-relaxed">
                  {record.explanation}
                </div>
              </div>

              {/* Result */}
              <div>
                <h3 className="text-xs font-bold text-kali-cyan uppercase tracking-wider mb-1.5">
                  6. RESULT
                </h3>
                <div className={`p-4 rounded-lg border text-xs leading-relaxed ${
                  isSuccess 
                    ? 'bg-kali-green/10 border-kali-green/30 text-emerald-300' 
                    : 'bg-rose-500/10 border-rose-500/30 text-rose-300'
                }`}>
                  <p>
                    <strong>Conclusion:</strong> The practical experiment <strong>'{record.title}'</strong> was{' '}
                    {isSuccess 
                      ? 'successfully executed and verified on the Kali Linux terminal.' 
                      : `completed with execution status: ${record.status}. Errors were captured during testing.`}
                  </p>
                </div>
              </div>

            </div>
          ) : (
            <textarea
              readOnly
              value={record.markdown_record || ''}
              className="w-full h-[500px] p-4 rounded-lg bg-[#07090e] border border-slate-800 font-mono text-xs text-slate-300 focus:outline-none resize-none"
            />
          )}
        </div>

        {/* Footer */}
        <div className="p-4 border-t border-kali-border bg-slate-950/60 flex items-center justify-between text-xs text-slate-400">
          <span>Executed: {record.timestamp} &bull; Duration: {record.duration_seconds}s</span>
          <button
            onClick={handleDownloadMarkdown}
            className="flex items-center space-x-1.5 px-4 py-2 rounded-lg bg-kali-cyan text-black font-semibold hover:bg-kali-cyanHover transition"
          >
            <Download className="w-3.5 h-3.5" />
            <span>Download Practical Record (.md)</span>
          </button>
        </div>

      </div>
    </div>
  );
};
