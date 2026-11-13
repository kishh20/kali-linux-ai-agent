# Kali Linux Practical Automation Agent

[![Kali Linux](https://img.shields.io/badge/Kali%20Linux-2024%2F2025-blue?logo=kalilinux)](https://www.kali.org/)
[![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115%2B-009688?logo=fastapi)](https://fastapi.tiangolo.com/)
[![React 18](https://img.shields.io/badge/React-18-61DAFB?logo=react)](https://react.dev/)
[![xterm.js](https://img.shields.io/badge/Terminal-xterm.js-red)](https://xtermjs.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

An educational automation framework and AI workbench designed specifically for **Kali Linux**. It provides two complementary operational modes:
1. **Stealth Terminal Agent (`p <1-25>`)**: Run practicals directly in the stock Kali Linux terminal (`zsh` / `bash`) with complete stealth — the trigger command completely vanishes from the screen, an authentic 2-line Kali prompt is rendered, and commands are typed keystroke-by-keystroke like a proficient human operator.
2. **Interactive Web Dashboard (`./start.sh`)**: A cyber-themed web workspace connecting directly to the host's `/bin/bash` login shell via native POSIX pseudo-terminals (`pty`) and WebSockets, complete with automated curriculum parameterization, Google Gemini AI diagnostics, and automatic academic lab record generation (Markdown & PDF).

---

## ⚡ Quick Start: Stealth Terminal Mode

The stealth mode runs directly in your native Kali Linux terminal without opening any web browser or UI.

### 1. One-Click Setup
```bash
git clone https://github.com/kishh20/kali-linux-ai-agent.git
cd kali-linux-ai-agent
chmod +x setup.sh && ./setup.sh
source ~/.zshrc    # or source ~/.bashrc
```

### 2. Execute Any Practical
Simply type `p` (or `run`) followed by the practical number (1 to 25):
```bash
p 1          # Executes Practical 1 (File and User Management)
p 18         # Executes Practical 18 (Nmap Reconnaissance)
```

### How Stealth Mode Works:
1. **Auto-Erase:** The instant you hit Enter, the trigger command (`p 1`) and the prompt line are wiped from the terminal screen using ANSI escape sequences (`\033[2K\033[1A\033[2K\033[1A\033[2K\r`).
2. **Stock Kali Prompt:** The authentic two-line Kali prompt is printed:
   ```
   ┌──(kali㉿kali)-[~/kali-linux-ai-agent]
   └─$ 
   ```
3. **Keystroke Emulation:** Commands are typed out character-by-character with natural micro-delays (20ms–40ms jitter), perfectly simulating a human typing.
4. **Real Execution:** Every command executes genuinely in the Kali `/bin/bash` kernel — no fake simulators or mocked outputs.
5. **At Least 15 Commands:** Every practical executes 15 to 21 comprehensive, step-by-step Linux commands.

### Stealth Options:
```bash
p <num> --fast      # Execute instantly without typing animation (-f)
p <num> --step      # Wait for Enter between commands (-s)
p <num> <target>    # Pass custom target IP (e.g. p 18 192.168.1.100)
p load <num>        # Inject commands directly into shell history (~/.zsh_history)
                    # (Allows you to press Up Arrow -> Enter for each command!)
p list              # Show catalogue of all 25 practicals
```

---

## 🌐 Alternative: Interactive Web Dashboard Mode

If you prefer a visual web interface with real-time terminal streaming, Gemini AI reviews, and 1-click Lab Record generation:

```bash
chmod +x start.sh
./start.sh
```
* If Node.js/npm is installed: Starts the FastAPI PTY backend and Vite dev server on `http://localhost:5173`.
* If Node.js is NOT installed: Automatically falls back to standalone mode, serving the pre-compiled production UI directly from FastAPI on `http://localhost:8000`.

---

## 📋 Comprehensive Catalog: All 25 Practicals

Every single practical includes at least **15 comprehensive commands** covering setup, core exercises, safety validation, and verification routines:

| # | Practical Title | Category | Sudo | Commands Count | Key Tools / Commands |
|---|-----------------|----------|:----:|:--------------:|----------------------|
| **01** | **File and User Management** | Administration | Yes | 16 | `useradd`, `groupadd`, `usermod`, `chown`, `chmod`, `id`, `getent` |
| **02** | **Text Processing and Filtering** | Administration | No | 16 | `grep`, `cut`, `sort`, `uniq`, `awk`, `sed`, `head`, `wc` |
| **03** | **Process Management & Job Control** | System | No | 16 | `ps`, `top`, `nice`, `renice`, `kill`, `pgrep`, `jobs`, `bg`, `fg` |
| **04** | **Bash Variables and Environment** | Scripting | No | 16 | `export`, `env`, `readonly`, `unset`, parameter expansion, exit codes |
| **05** | **Conditional Statements in Bash** | Scripting | No | 16 | `test`, `[ -f ]`, `[[ -d ]]`, multi-branch `if/elif/else`, `case/esac` |
| **06** | **Bash Loops and Iteration** | Scripting | No | 16 | `for` in list, C-style `for`, `while`, `until`, `break`, `continue` |
| **07** | **Modular Bash Functions** | Scripting | No | 16 | `function`, `local` vars, `return`, `$1`, trap handling |
| **08** | **Administrative Automation & Backups** | Administration | No | 16 | `tar -czvf`, `tar -tvf`, `gzip`, `crontab`, `find -mtime`, `df -h` |
| **09** | **Password and Privilege Management** | Security | Yes | 16 | `chage -l`, `passwd -S`, `sudo -l`, `/etc/sudoers.d/`, password aging |
| **10** | **Disk & Filesystem Management** | Administration | Yes | 16 | Safe loopback device (`losetup`), `mkfs.ext4`, `mount`, `df -T`, `tune2fs` |
| **11** | **Linux File Permissions and ACLs** | Administration | Yes | 16 | `chmod`, `umask`, `getfacl`, `setfacl -m`, default ACLs, recursive rights |
| **12** | **Special Permissions (SUID, SGID, Sticky)** | Security | Yes | 16 | `chmod 4755` (SUID), `2775` (SGID), `1777` (Sticky), audit via `find -perm` |
| **13** | **SSH Configuration & Security Hardening** | Security | Yes | 16 | `ssh-keygen -t ed25519`, `sshd -T`, `authorized_keys`, banner, port binding |
| **14** | **Firewall Management Using UFW** | Security | Yes | 16 | `ufw status numbered`, `default deny`, `allow proto tcp`, rate limiting |
| **15** | **Firewall Management Using iptables** | Security | Yes | 16 | Custom chains, `INPUT -m conntrack`, `DROP`, `ACCEPT`, `iptables -S` |
| **16** | **System and Security Log Analysis** | Security | Yes | 16 | `journalctl -p err`, `tail /var/log/auth.log`, failed sudo logins, audit logs |
| **17** | **Network Configuration & Troubleshooting**| Networking | No | 16 | `ip addr`, `ip route`, `ping`, `ss -tulnp`, `traceroute`, `dig`, `curl` |
| **18** | **Network Reconnaissance Using Nmap** | Networking | No | 16 | `nmap -sn`, `-sT`, `-sV`, `--top-ports`, banner grabbing, XML output |
| **19** | **Packet Capture with Wireshark / TShark** | Networking | Yes | 16 | `tshark -D`, capture loopback packets, protocol stats, display filters |
| **20** | **HTTP Traffic Analysis** | Networking | No | 16 | Python HTTP server, `curl -I`, header analysis, HTTP POST body inspection |
| **21** | **Service Management Using systemctl** | Administration | Yes | 16 | Custom `systemd` unit file creation, `daemon-reload`, start, enable, logs |
| **22** | **Vulnerability Lookup with Searchsploit**| Security | No | 16 | `searchsploit`, Exploit-DB path lookup, CVE cross-referencing, metadata |
| **23** | **Concurrency, Deadlock & Synchronization**| System | No | 16 | Python threading, mutex lock contention, deadlock simulation & fix |
| **24** | **System Monitoring & Boot Performance** | System | No | 16 | `systemd-analyze blame`, `systemd-analyze critical-chain`, `vmstat`, `free -m` |
| **25** | **Integrated Linux Administration Capstone**| Administration | Yes | 16 | User lifecycle, loopback storage, cron backup, service unit, system audit |

---

## 🛡️ Safety & Host Protection

The agent enforces strict safety guarantees:
* **No Root Daemon:** The application runs as standard unprivileged user. Interactive `sudo` commands prompt for authentication directly inside the pseudo-terminal. Passwords are typed interactively and are **never stored, intercepted, or transmitted**.
* **Host Disk Protection (Practical 10 & 25):** Disk formatting operations are strictly quarantined inside a virtual **64MB sparse file loopback device** in `/tmp` using `losetup`. Physical drives (`/dev/sda`, `/dev/nvme0n1`) are completely untouched.
* **Network Target Lockdown:** Nmap reconnaissance and TShark packet captures default strictly to `127.0.0.1` and `lo`. Arbitrary internet-wide scanning is prevented.
* **Destructive Blacklist:** Commands such as `rm -rf /`, `dd if=/dev/zero of=/dev/sd*`, fork bombs, and system crashes are systematically blocked.

---

## 📄 Academic Lab Record Generation

For coursework, laboratory submissions, or audit documentation, the agent provides one-click report generation:
* **Aim:** Formal, academic statement of purpose.
* **Algorithm:** Numbered step-by-step logical walkthrough.
* **Commands:** Exact Linux commands executed.
* **Actual Output:** Byte-for-byte console output captured live from the kernel.
* **Result:** Definite pass/fail verification conclusion.

Reports can be exported in **Markdown (`.md`)** for lab journals or **Printable HTML / PDF**.

---

## ⚙️ Configuration & Environment

Configuration is managed via `.env` (copy from `.env.example`):
```bash
cp .env.example .env
nano .env
```

| Variable | Description | Default |
|----------|-------------|---------|
| `GEMINI_API_KEY` | Optional Google Gemini API key for AI plan reviews and diagnostics | *(empty - runs offline heuristics)* |
| `GEMINI_MODEL` | Gemini model name | `gemini-2.5-flash` |
| `DEFAULT_TARGET_IP` | Default target IP for network labs | `127.0.0.1` |
| `DEFAULT_INTERFACE` | Default network interface for packet capture | `lo` |

---

## 📁 Repository Structure

```
kali-linux-practical-automation/
├── backend/
│   ├── app/
│   │   ├── agent.py               # AI execution engine & Gemini plan reviewer
│   │   ├── config.py              # Application settings
│   │   ├── lab_records.py         # Academic Lab Record generator
│   │   ├── main.py                # FastAPI web server & static UI distributor
│   │   ├── practicals_data.py     # 25 practical definitions (>=15 commands each)
│   │   ├── pty_manager.py         # Native POSIX PTY pseudo-terminal stream
│   │   └── safety.py              # Safety validator & command blacklist
│   └── requirements.txt           # Python dependencies
├── frontend/
│   ├── dist/                      # Pre-compiled production UI bundle
│   ├── src/                       # React 18 + Tailwind + xterm.js source
│   ├── package.json
│   └── vite.config.ts
├── records/                       # Auto-generated lab records (.gitkeep)
├── install_alias.sh               # Quick alias setup for ~/.zshrc and ~/.bashrc
├── kali-agent                     # Cyber CLI Agent launcher
├── kali_agent.py                  # Full interactive cyber CLI agent
├── p                              # Stealth terminal launcher (e.g. p 1)
├── run                            # Alternative stealth launcher (e.g. run 1)
├── setup.sh                       # Universal setup script
├── start.sh                       # Web dashboard startup script
├── stealth_agent.py               # Covert stock-terminal runner with typing simulation
└── README.md
```

---

## 📜 License & Ethical Use

Distributed under the **MIT License**. This tool is engineered strictly for educational research, defensive training, and authorized Linux systems administration coursework. Ensure all network reconnaissance is conducted strictly on localhost or authorized private lab infrastructure.
