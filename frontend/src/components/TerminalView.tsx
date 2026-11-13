import React, { useEffect, useRef, useState } from 'react';
import { Terminal as XTerm } from '@xterm/xterm';
import { FitAddon } from '@xterm/addon-fit';
import { WebLinksAddon } from '@xterm/addon-web-links';
import { 
  Square, 
  Trash2, 
  RotateCcw, 
  Copy, 
  Download, 
  Maximize2, 
  Minimize2, 
  Check, 
  KeyRound,
  Terminal as TerminalIcon 
} from 'lucide-react';
import { wsClient } from '../services/websocket';
import { clearTerminal, resetTerminal, stopExecution } from '../services/api';

interface TerminalViewProps {
  onOutputReceived?: (text: string) => void;
  isExecuting?: boolean;
}

export const TerminalView: React.FC<TerminalViewProps> = ({ onOutputReceived, isExecuting = false }) => {
  const terminalRef = useRef<HTMLDivElement | null>(null);
  const xtermInstance = useRef<XTerm | null>(null);
  const fitAddonRef = useRef<FitAddon | null>(null);
  const terminalBufferRef = useRef<string>('');
  
  const [copied, setCopied] = useState(false);
  const [isFullscreen, setIsFullscreen] = useState(false);
  const [connected, setConnected] = useState(false);

  useEffect(() => {
    if (!terminalRef.current) return;

    // Initialize xterm.js instance with Kali cyber dark theme
    const term = new XTerm({
      cursorBlink: true,
      cursorStyle: 'block',
      fontFamily: "'JetBrains Mono', 'Fira Code', 'Consolas', monospace",
      fontSize: 13,
      lineHeight: 1.25,
      theme: {
        background: '#07090e',
        foreground: '#e2e8f0',
        cursor: '#00d2ff',
        cursorAccent: '#07090e',
        selectionBackground: 'rgba(0, 210, 255, 0.3)',
        black: '#0f172a',
        red: '#f43f5e',
        green: '#10b981',
        yellow: '#f59e0b',
        blue: '#38bdf8',
        magenta: '#c084fc',
        cyan: '#00d2ff',
        white: '#f8fafc',
        brightBlack: '#475569',
        brightRed: '#fb7185',
        brightGreen: '#34d399',
        brightYellow: '#fbbf24',
        brightBlue: '#60a5fa',
        brightMagenta: '#e879f9',
        brightCyan: '#38bdf8',
        brightWhite: '#ffffff',
      },
      convertEol: true,
      scrollback: 5000,
    });

    const fitAddon = new FitAddon();
    term.loadAddon(fitAddon);
    term.loadAddon(new WebLinksAddon());

    term.open(terminalRef.current);
    fitAddon.fit();

    xtermInstance.current = term;
    fitAddonRef.current = fitAddon;

    // Connect WebSocket
    wsClient.connect();

    // Listen to user interactive keystrokes and pipe to backend master PTY
    const onDataDispose = term.onData((data) => {
      wsClient.sendInput(data);
    });

    // Subscribe to WebSocket incoming terminal streams
    const unsubscribe = wsClient.subscribe((msg) => {
      if (msg.type === 'terminal_output' && msg.data) {
        term.write(msg.data);
        terminalBufferRef.current += msg.data;
        if (onOutputReceived) {
          onOutputReceived(msg.data);
        }
      } else if (msg.type === 'connection_status') {
        setConnected(msg.connected);
        if (msg.connected) {
          // Sync size on connect
          try {
            fitAddon.fit();
            wsClient.sendResize(term.cols, term.rows);
          } catch (e) {}
        }
      } else if (msg.type === 'terminal_reset') {
        term.clear();
        terminalBufferRef.current = '';
        term.write('\x1b[1;36m[Kali AI Agent] Terminal bash session re-initialized.\x1b[0m\r\n');
      }
    });

    // Resize observer to auto-fit terminal to container changes
    const resizeObserver = new ResizeObserver(() => {
      try {
        fitAddon.fit();
        wsClient.sendResize(term.cols, term.rows);
      } catch (err) {}
    });
    resizeObserver.observe(terminalRef.current);

    return () => {
      onDataDispose.dispose();
      unsubscribe();
      resizeObserver.disconnect();
      term.dispose();
    };
  }, []);

  const handleCopy = () => {
    const text = terminalBufferRef.current || xtermInstance.current?.getSelection() || '';
    if (text) {
      navigator.clipboard.writeText(text);
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    }
  };

  const handleDownload = () => {
    const text = terminalBufferRef.current;
    if (!text) return;
    const blob = new Blob([text], { type: 'text/plain;charset=utf-8' });
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.download = `kali_terminal_session_${new Date().toISOString().replace(/[:.]/g, '-')}.log`;
    link.click();
    URL.revokeObjectURL(url);
  };

  const handleClear = async () => {
    xtermInstance.current?.clear();
    terminalBufferRef.current = '';
    await clearTerminal();
  };

  const handleRestart = async () => {
    if (confirm('Restart terminal? Current running commands will be killed.')) {
      await resetTerminal();
    }
  };

  const handleStop = async () => {
    await stopExecution();
  };

  return (
    <div className={`flex flex-col bg-[#07090e] border border-kali-border rounded-xl overflow-hidden shadow-2xl transition-all ${
      isFullscreen ? 'fixed inset-4 z-50' : 'h-full w-full'
    }`}>
      {/* Terminal Title Bar */}
      <div className="bg-[#0b0f17] border-b border-kali-border px-4 py-2.5 flex items-center justify-between select-none">
        <div className="flex items-center space-x-3">
          {/* Window control dots */}
          <div className="flex items-center space-x-1.5">
            <span className="w-3 h-3 rounded-full bg-rose-500/80 inline-block"></span>
            <span className="w-3 h-3 rounded-full bg-amber-500/80 inline-block"></span>
            <span className="w-3 h-3 rounded-full bg-emerald-500/80 inline-block"></span>
          </div>

          <div className="flex items-center space-x-2 text-xs font-mono text-slate-300">
            <TerminalIcon className="w-3.5 h-3.5 text-kali-cyan" />
            <span className="font-semibold text-white">kali@agent:</span>
            <span className="text-slate-400">/bin/bash (Interactive PTY)</span>
          </div>

          {/* Sudo Hint Pill */}
          <div className="hidden lg:flex items-center space-x-1 px-2 py-0.5 rounded bg-slate-800/80 border border-slate-700 text-[11px] text-slate-400 font-mono">
            <KeyRound className="w-3 h-3 text-amber-400" />
            <span>Interactive typing & sudo supported</span>
          </div>
        </div>

        {/* Action Controls */}
        <div className="flex items-center space-x-1.5">
          {isExecuting && (
            <button
              onClick={handleStop}
              title="Stop Running Command (SIGINT / Ctrl+C)"
              className="flex items-center space-x-1 px-2.5 py-1 rounded bg-rose-950/80 border border-rose-700 text-rose-300 hover:bg-rose-900 text-xs font-mono transition"
            >
              <Square className="w-3 h-3 fill-rose-300" />
              <span>Stop</span>
            </button>
          )}

          <button
            onClick={handleCopy}
            title="Copy Terminal Text"
            className="p-1.5 rounded hover:bg-slate-800 text-slate-400 hover:text-white transition"
          >
            {copied ? <Check className="w-3.5 h-3.5 text-kali-green" /> : <Copy className="w-3.5 h-3.5" />}
          </button>

          <button
            onClick={handleDownload}
            title="Download Session Log"
            className="p-1.5 rounded hover:bg-slate-800 text-slate-400 hover:text-white transition"
          >
            <Download className="w-3.5 h-3.5" />
          </button>

          <button
            onClick={handleClear}
            title="Clear Terminal (clear)"
            className="p-1.5 rounded hover:bg-slate-800 text-slate-400 hover:text-white transition"
          >
            <Trash2 className="w-3.5 h-3.5" />
          </button>

          <button
            onClick={handleRestart}
            title="Restart Bash Shell"
            className="p-1.5 rounded hover:bg-slate-800 text-slate-400 hover:text-white transition"
          >
            <RotateCcw className="w-3.5 h-3.5" />
          </button>

          <button
            onClick={() => {
              setIsFullscreen(!isFullscreen);
              setTimeout(() => fitAddonRef.current?.fit(), 100);
            }}
            title={isFullscreen ? 'Exit Fullscreen' : 'Fullscreen'}
            className="p-1.5 rounded hover:bg-slate-800 text-slate-400 hover:text-white transition"
          >
            {isFullscreen ? <Minimize2 className="w-3.5 h-3.5" /> : <Maximize2 className="w-3.5 h-3.5" />}
          </button>
        </div>
      </div>

      {/* Terminal Viewport */}
      <div 
        ref={terminalRef} 
        className="flex-1 w-full h-full p-2 overflow-hidden cursor-text"
        onClick={() => xtermInstance.current?.focus()}
      />
    </div>
  );
};
