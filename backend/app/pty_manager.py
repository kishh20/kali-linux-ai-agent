import os
import sys
import time
import json
import shutil
import struct
import select
import asyncio
import getpass
import platform
import subprocess
from pathlib import Path
from typing import Optional, List, Dict, Any, Callable, Set
from fastapi import WebSocket

IS_POSIX = os.name == "posix"
if IS_POSIX:
    import pty
    import termios
    import fcntl

class KaliPTYManager:
    """
    Manages a real Linux pseudo-terminal (PTY) session running /bin/bash on Kali Linux.
    Streams live terminal output to connected WebSockets and receives keystrokes.
    """
    def __init__(self, shell_path: str = "/bin/bash", cols: int = 120, rows: int = 32):
        self.shell_path = shell_path
        self.cols = cols
        self.rows = rows
        
        self.master_fd: Optional[int] = None
        self.process: Optional[subprocess.Popen] = None
        self.is_running: bool = False
        self.terminal_buffer: str = ""
        self.max_buffer_size: int = 200000
        
        self.subscribers: Set[WebSocket] = set()
        self.read_task: Optional[asyncio.Task] = None
        
        # Execution tracking
        self.current_execution: Optional[Dict[str, Any]] = None
        self._command_event: Optional[asyncio.Event] = None
        self._command_output_accumulator: List[str] = []
        self._command_exit_code: Optional[int] = None

    def get_system_diagnostics(self) -> Dict[str, Any]:
        """Detect whether running on Kali Linux, probe tools, and report environment."""
        diag: Dict[str, Any] = {
            "platform": sys.platform,
            "os_name": platform.system(),
            "kernel_release": platform.release(),
            "architecture": platform.machine(),
            "current_user": getpass.getuser(),
            "is_posix": IS_POSIX,
            "is_kali": False,
            "distro_name": "Unknown",
            "distro_id": "unknown",
            "shell_available": os.path.exists(self.shell_path) if IS_POSIX else False,
            "shell_path": self.shell_path,
            "tools": {},
            "status_message": "",
            "can_execute": False
        }

        # Check Linux OS release
        if IS_POSIX:
            os_release_path = Path("/etc/os-release")
            if os_release_path.exists():
                try:
                    with open(os_release_path, "r", encoding="utf-8") as f:
                        lines = f.readlines()
                        os_data = {}
                        for line in lines:
                            if "=" in line:
                                k, v = line.strip().split("=", 1)
                                os_data[k] = v.strip('"')
                        
                        distro_id = os_data.get("ID", "").lower()
                        pretty_name = os_data.get("PRETTY_NAME", "")
                        diag["distro_id"] = distro_id
                        diag["distro_name"] = pretty_name or distro_id
                        
                        if "kali" in distro_id or "kali" in pretty_name.lower():
                            diag["is_kali"] = True
                        elif "debian" in distro_id or "ubuntu" in distro_id:
                            # Debian-based
                            diag["is_kali"] = False
                except Exception as e:
                    diag["status_message"] = f"Failed to read /etc/os-release: {e}"
            else:
                diag["distro_name"] = "POSIX Generic"

            # Check tools installed in Kali
            tools_to_check = [
                "bash", "sudo", "nmap", "tshark", "wireshark",
                "searchsploit", "ufw", "iptables", "systemctl",
                "chage", "grep", "awk", "sed", "gcc", "python3"
            ]
            for tool in tools_to_check:
                path = shutil.which(tool)
                diag["tools"][tool] = {
                    "installed": path is not None,
                    "path": path or ""
                }

            if diag["shell_available"]:
                diag["can_execute"] = True
                if diag["is_kali"]:
                    diag["status_message"] = f"Connected to native Kali Linux shell ({diag['distro_name']})."
                else:
                    diag["status_message"] = f"Connected to Linux shell ({diag['distro_name']})."
            else:
                diag["status_message"] = f"Shell '{self.shell_path}' not found."
        else:
            diag["distro_name"] = f"Windows {platform.release()}"
            diag["is_kali"] = False
            diag["can_execute"] = False
            diag["status_message"] = (
                "Kali Linux PTY Session Offline: Backend is running on Windows. "
                "For real interactive Bash execution and Kali practical automation, "
                "run this service inside Kali Linux or WSL2 Kali."
            )
            # Check if WSL exists on Windows
            wsl_path = shutil.which("wsl")
            diag["tools"]["wsl"] = {"installed": wsl_path is not None, "path": wsl_path or ""}

        return diag

    async def start(self) -> bool:
        """Start interactive bash session in a real PTY (POSIX only)."""
        if not IS_POSIX:
            print("[PTY Manager] Not starting PTY: Not on POSIX/Linux.")
            self.terminal_buffer = (
                "\033[1;33m[KALI AI AGENT - ENVIRONMENT NOTICE]\033[0m\r\n"
                "\033[1;31mHost Operating System: Windows (Non-POSIX)\033[0m\r\n"
                "Interactive PTY bash execution requires a Linux/Kali environment.\r\n"
                "Please run this application directly inside Kali Linux or WSL Kali.\r\n"
                "\r\n"
            )
            return False

        if self.is_running and self.process and self.process.poll() is None:
            return True

        try:
            # Create PTY pair
            master_fd, slave_fd = os.openpty()
            self.master_fd = master_fd

            # Set window size
            self.resize(self.cols, self.rows)

            # Prepare environment
            env = os.environ.copy()
            env["TERM"] = "xterm-256color"
            env["LANG"] = "C.UTF-8"
            env["LC_ALL"] = "C.UTF-8"
            env["COLUMNS"] = str(self.cols)
            env["LINES"] = str(self.rows)
            # Custom prompt for the agent terminal
            env["PS1"] = r"\[\033[01;32m\]kali@agent\[\033[00m\]:\[\033[01;34m\]\w\[\033[00m\]\$ "

            # Spawn interactive login bash shell
            self.process = subprocess.Popen(
                [self.shell_path, "-l", "-i"],
                stdin=slave_fd,
                stdout=slave_fd,
                stderr=slave_fd,
                preexec_fn=os.setsid,
                env=env,
                close_fds=True
            )

            # Close slave fd in parent
            os.close(slave_fd)
            self.is_running = True

            # Start background reader task in asyncio loop
            loop = asyncio.get_event_loop()
            self.read_task = loop.create_task(self._pty_reader_loop())

            print(f"[PTY Manager] Started interactive bash shell (PID: {self.process.pid})")
            return True

        except Exception as e:
            print(f"[PTY Manager] Error spawning PTY: {e}")
            self.is_running = False
            return False

    async def _pty_reader_loop(self):
        """Asynchronously read output chunks from master_fd and broadcast to WebSockets."""
        loop = asyncio.get_event_loop()
        sentinel_prefix = "__AGENT_STATUS__:"

        while self.is_running and self.master_fd is not None:
            try:
                # Use run_in_executor to avoid blocking the asyncio event loop on os.read
                data = await loop.run_in_executor(None, self._read_chunk)
                if not data:
                    # EOF
                    await asyncio.sleep(0.02)
                    continue

                text = data.decode("utf-8", errors="replace")
                
                # Append to circular buffer
                self.terminal_buffer += text
                if len(self.terminal_buffer) > self.max_buffer_size:
                    self.terminal_buffer = self.terminal_buffer[-self.max_buffer_size:]

                # Check for command exit sentinel if waiting for command completion
                if sentinel_prefix in text and self._command_event and not self._command_event.is_set():
                    # Parse exit code
                    parts = text.split(sentinel_prefix)
                    # Output before sentinel
                    self._command_output_accumulator.append(parts[0])
                    status_line = parts[1].split("\r")[0].split("\n")[0].strip()
                    try:
                        self._command_exit_code = int(status_line)
                    except ValueError:
                        self._command_exit_code = 0
                    self._command_event.set()
                elif self._command_event and not self._command_event.is_set():
                    self._command_output_accumulator.append(text)

                # Broadcast to all connected WebSockets
                await self.broadcast_output(text)

            except Exception as e:
                # Terminal closed or error
                print(f"[PTY Manager] Read loop exception: {e}")
                break

        self.is_running = False

    def _read_chunk(self) -> bytes:
        if self.master_fd is None:
            return b""
        try:
            r, _, _ = select.select([self.master_fd], [], [], 0.05)
            if r:
                return os.read(self.master_fd, 4096)
        except (OSError, ValueError):
            return b""
        return b""

    async def broadcast_output(self, text: str):
        """Send terminal output chunk to all active WebSocket clients."""
        dead_sockets = set()
        for ws in self.subscribers:
            try:
                await ws.send_text(json.dumps({
                    "type": "terminal_output",
                    "data": text
                }))
            except Exception:
                dead_sockets.add(ws)
        self.subscribers.difference_update(dead_sockets)

    async def broadcast_event(self, event_data: Dict[str, Any]):
        """Send agent execution progress events to all connected clients."""
        dead_sockets = set()
        for ws in self.subscribers:
            try:
                await ws.send_text(json.dumps(event_data))
            except Exception:
                dead_sockets.add(ws)
        self.subscribers.difference_update(dead_sockets)

    def write_input(self, data: str | bytes):
        """Write user keystrokes / input directly into the bash PTY."""
        if not self.is_running or self.master_fd is None or not IS_POSIX:
            return

        try:
            if isinstance(data, str):
                encoded = data.encode("utf-8")
            else:
                encoded = data
            os.write(self.master_fd, encoded)
        except Exception as e:
            print(f"[PTY Manager] Failed writing input: {e}")

    def resize(self, cols: int, rows: int):
        """Update terminal dimensions in kernel."""
        self.cols = max(20, cols)
        self.rows = max(5, rows)
        if IS_POSIX and self.master_fd is not None:
            try:
                winsize = struct.pack("HHHH", self.rows, self.cols, 0, 0)
                fcntl.ioctl(self.master_fd, termios.TIOCSWINSZ, winsize)
            except Exception as e:
                print(f"[PTY Manager] Resize error: {e}")

    async def execute_command(self, cmd: str, timeout: float = 60.0) -> Dict[str, Any]:
        """
        Execute a command inside the real interactive bash shell and await completion.
        Returns exit code and accumulated output.
        """
        if not self.is_running or self.master_fd is None or not IS_POSIX:
            return {
                "success": False,
                "exit_code": -1,
                "output": "PTY shell is offline or unsupported on this platform.",
                "duration_seconds": 0.0
            }

        start_time = time.time()
        self._command_event = asyncio.Event()
        self._command_output_accumulator = []
        self._command_exit_code = None

        # Format command with exit status sentinel
        # We execute: {cmd} ; echo "__AGENT_STATUS__:$?"
        wrapped_cmd = f"{cmd} ; echo \"__AGENT_STATUS__:$?\"\n"
        self.write_input(wrapped_cmd)

        try:
            await asyncio.wait_for(self._command_event.wait(), timeout=timeout)
            duration = round(time.time() - start_time, 2)
            exit_code = self._command_exit_code if self._command_exit_code is not None else 0
            full_output = "".join(self._command_output_accumulator).strip()
            
            return {
                "success": exit_code == 0,
                "exit_code": exit_code,
                "output": full_output,
                "duration_seconds": duration
            }
        except asyncio.TimeoutError:
            duration = round(time.time() - start_time, 2)
            # Send Ctrl+C to terminate hanging command
            self.write_input("\x03")
            return {
                "success": False,
                "exit_code": 124,  # Timeout exit code
                "output": f"Command timed out after {timeout} seconds. Sent SIGINT (Ctrl+C).",
                "duration_seconds": duration
            }
        finally:
            self._command_event = None

    async def interrupt(self):
        """Send SIGINT (Ctrl+C) to running process."""
        self.write_input("\x03")

    async def reset(self):
        """Terminate existing bash shell and restart a fresh PTY session."""
        if IS_POSIX:
            if self.process and self.process.poll() is None:
                try:
                    self.process.terminate()
                    await asyncio.sleep(0.1)
                    if self.process.poll() is None:
                        self.process.kill()
                except Exception:
                    pass

            if self.master_fd is not None:
                try:
                    os.close(self.master_fd)
                except Exception:
                    pass
                self.master_fd = None

        self.is_running = False
        self.terminal_buffer = ""
        await self.start()
        await self.broadcast_event({"type": "terminal_reset", "message": "Terminal session reset."})

    def subscribe(self, ws: WebSocket):
        self.subscribers.add(ws)

    def unsubscribe(self, ws: WebSocket):
        self.subscribers.discard(ws)


# Global singleton instance
pty_manager = KaliPTYManager()
