import React from 'react';
import { 
  Info, 
  Terminal, 
  ShieldCheck, 
  Cpu, 
  Layers, 
  Sparkles, 
  Flame, 
  CheckCircle2, 
  HardDrive 
} from 'lucide-react';

export const About: React.FC = () => {
  return (
    <div className="flex-1 p-6 overflow-y-auto space-y-6 max-w-4xl text-slate-300">
      
      {/* Hero Header */}
      <div className="p-6 rounded-2xl bg-gradient-to-r from-kali-card via-slate-900 to-[#07090e] border border-kali-border flex items-center space-x-5">
        <div className="w-16 h-16 rounded-2xl bg-gradient-to-br from-kali-cyan via-kali-blue to-purple-600 flex items-center justify-center shadow-xl shadow-kali-cyan/25 shrink-0">
          <Flame className="w-9 h-9 text-black fill-black" />
        </div>
        <div>
          <h2 className="text-2xl font-bold text-white tracking-tight">
            Kali Linux AI Practical Automation Agent
          </h2>
          <p className="text-xs text-kali-cyan font-mono mt-1">
            Real Interactive Terminal Automation Engine &bull; Version 1.0.0
          </p>
          <p className="text-xs text-slate-400 mt-2 leading-relaxed">
            An automated educational agent platform engineered specifically for Kali Linux. 
            Executes all 25 curriculum practicals directly inside a real interactive Bash shell 
            with real-time PTY streaming, Gemini AI intelligence, and academic record generation.
          </p>
        </div>
      </div>

      {/* Core Architectural Pillars */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        
        <div className="glass-card rounded-xl p-5 border border-kali-border space-y-2">
          <div className="w-9 h-9 rounded-lg bg-kali-cyan/10 border border-kali-cyan/20 flex items-center justify-center text-kali-cyan">
            <Terminal className="w-5 h-5" />
          </div>
          <h3 className="text-sm font-bold text-white">Genuine Kali PTY</h3>
          <p className="text-xs text-slate-400 leading-relaxed">
            Directly binds to <code className="text-kali-cyan">/bin/bash -l -i</code> via Python PTY. 
            Streams raw byte-for-byte ANSI output over WebSockets directly to xterm.js with zero simulation.
          </p>
        </div>

        <div className="glass-card rounded-xl p-5 border border-kali-border space-y-2">
          <div className="w-9 h-9 rounded-lg bg-purple-500/10 border border-purple-500/20 flex items-center justify-center text-purple-400">
            <Sparkles className="w-5 h-5" />
          </div>
          <h3 className="text-sm font-bold text-white">Gemini AI Intelligence</h3>
          <p className="text-xs text-slate-400 leading-relaxed">
            Leverages Google Gemini for adaptive execution planning, intelligent terminal error diagnosis, 
            interactive explanation, and academic practical record formatting.
          </p>
        </div>

        <div className="glass-card rounded-xl p-5 border border-kali-border space-y-2">
          <div className="w-9 h-9 rounded-lg bg-kali-green/10 border border-kali-green/20 flex items-center justify-center text-kali-green">
            <ShieldCheck className="w-5 h-5" />
          </div>
          <h3 className="text-sm font-bold text-white">Production Safeguards</h3>
          <p className="text-xs text-slate-400 leading-relaxed">
            Executes under the active Linux user's permissions. Uses safe virtual loopback images 
            for disk practicals and restricts network scans strictly to authorized lab targets.
          </p>
        </div>

      </div>

      {/* Safety & Execution Integrity Guarantees */}
      <div className="glass-card rounded-xl p-5 border border-kali-border space-y-3">
        <h3 className="text-sm font-bold text-white flex items-center space-x-2">
          <ShieldCheck className="w-4 h-4 text-kali-green" />
          <span>Safety & Execution Integrity Guarantees</span>
        </h3>
        <ul className="space-y-2 text-xs text-slate-300">
          <li className="flex items-start space-x-2">
            <CheckCircle2 className="w-4 h-4 text-kali-green shrink-0 mt-0.5" />
            <span><strong>Never Fakes Execution:</strong> Commands are genuinely executed inside Kali Linux. If an error or non-zero exit code occurs, it is honestly reported.</span>
          </li>
          <li className="flex items-start space-x-2">
            <CheckCircle2 className="w-4 h-4 text-kali-green shrink-0 mt-0.5" />
            <span><strong>Interactive Sudo Support:</strong> Normal sudo prompts are presented in the embedded terminal. Sudo passwords are typed directly into the shell and are never stored or logged by the backend.</span>
          </li>
          <li className="flex items-start space-x-2">
            <CheckCircle2 className="w-4 h-4 text-kali-green shrink-0 mt-0.5" />
            <span><strong>Virtual Loopback Devices:</strong> Practical 10 (Disk Management) creates a temporary 64MB sparse virtual disk file and mounts it as a loop device, guaranteeing physical host drives are never touched.</span>
          </li>
          <li className="flex items-start space-x-2">
            <CheckCircle2 className="w-4 h-4 text-kali-green shrink-0 mt-0.5" />
            <span><strong>Authorized Lab Targets:</strong> Network scanning (Nmap) and packet capturing (Wireshark/tshark) are locked to loopback (127.0.0.1) or user-specified private lab IP ranges.</span>
          </li>
        </ul>
      </div>

      {/* Curriculum Coverage Summary */}
      <div className="glass-card rounded-xl p-5 border border-kali-border space-y-3">
        <h3 className="text-sm font-bold text-white flex items-center space-x-2">
          <Layers className="w-4 h-4 text-kali-cyan" />
          <span>Full Curriculum Coverage: All 25 Practicals</span>
        </h3>
        <p className="text-xs text-slate-400">
          The agent contains dedicated algorithmic execution sequences for each practical:
        </p>
        <div className="grid grid-cols-1 sm:grid-cols-2 gap-2 text-xs font-mono">
          <div className="p-2 rounded bg-slate-900/60 border border-slate-800">1. File & User Management</div>
          <div className="p-2 rounded bg-slate-900/60 border border-slate-800">2. Text Processing (grep/cut/awk/sed)</div>
          <div className="p-2 rounded bg-slate-900/60 border border-slate-800">3. Process Management & Signals</div>
          <div className="p-2 rounded bg-slate-900/60 border border-slate-800">4. Bash Variables & Expansion</div>
          <div className="p-2 rounded bg-slate-900/60 border border-slate-800">5. Conditional Statements (if/case)</div>
          <div className="p-2 rounded bg-slate-900/60 border border-slate-800">6. Bash Loops (for/while/until)</div>
          <div className="p-2 rounded bg-slate-900/60 border border-slate-800">7. Modular Bash Functions & Traps</div>
          <div className="p-2 rounded bg-slate-900/60 border border-slate-800">8. Administrative Automation & Tar</div>
          <div className="p-2 rounded bg-slate-900/60 border border-slate-800">9. Password & Privilege (chage/sudo)</div>
          <div className="p-2 rounded bg-slate-900/60 border border-slate-800">10. Disk Management & Filesystems</div>
          <div className="p-2 rounded bg-slate-900/60 border border-slate-800">11. Linux File Permissions & ACLs</div>
          <div className="p-2 rounded bg-slate-900/60 border border-slate-800">12. Special Permissions (SUID/SGID/Sticky)</div>
          <div className="p-2 rounded bg-slate-900/60 border border-slate-800">13. SSH Keypairs & Hardening</div>
          <div className="p-2 rounded bg-slate-900/60 border border-slate-800">14. Firewall Using UFW</div>
          <div className="p-2 rounded bg-slate-900/60 border border-slate-800">15. Firewall Using iptables & Chains</div>
          <div className="p-2 rounded bg-slate-900/60 border border-slate-800">16. System & Security Log Analysis</div>
          <div className="p-2 rounded bg-slate-900/60 border border-slate-800">17. Network Diagnostics (ip/ping/ss)</div>
          <div className="p-2 rounded bg-slate-900/60 border border-slate-800">18. Network Reconnaissance (Nmap)</div>
          <div className="p-2 rounded bg-slate-900/60 border border-slate-800">19. Packet Capture (Wireshark/tshark)</div>
          <div className="p-2 rounded bg-slate-900/60 border border-slate-800">20. HTTP Traffic Analysis & Curl</div>
          <div className="p-2 rounded bg-slate-900/60 border border-slate-800">21. Service Management (systemctl)</div>
          <div className="p-2 rounded bg-slate-900/60 border border-slate-800">22. Vulnerability Search (Searchsploit)</div>
          <div className="p-2 rounded bg-slate-900/60 border border-slate-800">23. Concurrency, Deadlock & Mutex</div>
          <div className="p-2 rounded bg-slate-900/60 border border-slate-800">24. Boot Analysis & Monitoring</div>
          <div className="p-2 rounded bg-slate-900/60 border border-slate-800">25. Integrated Admin Capstone</div>
        </div>
      </div>

    </div>
  );
};
