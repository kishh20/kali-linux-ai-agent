#!/usr/bin/env python3
"""
==============================================================================
Kali Linux Practical Automation - Stealth Native Terminal Agent
==============================================================================
Executes curriculum practicals directly inside the native Kali Linux terminal
with zero trace of the automation agent.

Features:
- Instant wipe of trigger command (`p <1-25>`) using ANSI escape sequences
- Authentic two-line Kali Linux zsh/bash prompt rendering
- Proficient human keystroke emulation with realistic micro-jitter
- Direct execution in native host `/bin/bash`
- Shell history injection mode (`p load <num>`)
- Graceful Ctrl+C signal handling
==============================================================================
"""

import os
import sys
import time
import random
import signal
import socket
import getpass
import subprocess
from pathlib import Path

# Setup paths and environment
BASE_DIR = Path(__file__).resolve().parent
SHELL_EXE = "/bin/bash" if os.path.exists("/bin/bash") else None

# Clean SIGINT (Ctrl+C) handling
def sigint_handler(signum, frame):
    sys.stdout.write("^C\n")
    sys.stdout.flush()
    sys.exit(130)

signal.signal(signal.SIGINT, sigint_handler)

# Load practicals data from backend
sys.path.insert(0, str(BASE_DIR / "backend"))
try:
    from app.practicals_data import PRACTICALS, get_practical_by_id
except ImportError:
    sys.stderr.write("[-] Error: Could not load backend/app/practicals_data.py\n")
    sys.exit(1)


def print_kali_prompt():
    """Render authentic Kali Linux zsh/bash two-line prompt."""
    user = getpass.getuser()
    host = socket.gethostname()
    cwd = os.getcwd()
    home = os.path.expanduser("~")
    
    if cwd == home:
        cwd_disp = "~"
    elif cwd.startswith(home):
        cwd_disp = "~" + cwd[len(home):]
    else:
        cwd_disp = cwd

    user_color = "\033[1;31m" if user == "root" else "\033[1;34m"
    symbol = "#" if user == "root" else "$"

    prompt = (
        f"\033[1;34m┌──({user_color}{user}㉿{host}\033[1;34m)-[\033[0m{cwd_disp}\033[1;34m]\033[0m\n"
        f"\033[1;34m└─\033[1;32m{symbol}\033[0m "
    )
    sys.stdout.write(prompt)
    sys.stdout.flush()


def human_type(text: str, fast: bool = False, min_delay: float = 0.015, max_delay: float = 0.038):
    """Simulate authentic, proficient human touch-typing with natural micro-delays."""
    if fast:
        sys.stdout.write(text + "\n")
        sys.stdout.flush()
        return

    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        if char in (' ', '-', '_', '/', '.', '$', '|', '>', ';'):
            time.sleep(random.uniform(0.025, 0.055))
        else:
            time.sleep(random.uniform(min_delay, max_delay))
    
    time.sleep(random.uniform(0.10, 0.20))
    sys.stdout.write('\n')
    sys.stdout.flush()


def print_help():
    """Print elegant terminal help and practical listing."""
    print("\033[1;36m==============================================================\033[0m")
    print("\033[1;36m      KALI LINUX PRACTICAL AUTOMATION - STEALTH RUNNER        \033[0m")
    print("\033[1;36m==============================================================\033[0m")
    print("Usage: \033[1;32mp <1-25>\033[0m [options] [target_ip]")
    print()
    print("Modes:")
    print("  \033[1;33mp <num>\033[0m               Run practical with stealth typing & auto-erase")
    print("  \033[1;33mp <num> --fast\033[0m        Execute immediately without typing animation (-f)")
    print("  \033[1;33mp <num> --step\033[0m        Step-by-step mode (press Enter between commands) (-s)")
    print("  \033[1;33mp <num> --no-erase\033[0m    Do not erase the trigger command line")
    print("  \033[1;33mp load <num>\033[0m          Inject commands into shell history (press Up Arrow -> Enter)")
    print("  \033[1;33mp list\033[0m                List all 25 available practicals")
    print()
    print("Examples:")
    print("  p 1                   # Run Practical 1 (File & User Management)")
    print("  p 18 192.168.1.100    # Run Practical 18 (Nmap) against target IP")
    print("  p load 14             # Inject UFW firewall commands into ~/.zsh_history")
    print("\033[1;36m==============================================================\033[0m")


def list_practicals():
    """List all available practicals."""
    print("\033[1;34m[*] Available Kali Linux Practicals (1-25):\033[0m\n")
    for p in PRACTICALS:
        num = p['number']
        title = p['title']
        cat = p.get('category', 'General')
        cmds_count = len(p.get('default_commands', [])) + len(p.get('verification_commands', []))
        print(f"  \033[1;32m{num:>2}\033[0m: \033[1m{title:<44}\033[0m \033[2m[{cat}] ({cmds_count} cmds)\033[0m")
    print("\nRun any practical using: \033[1;32mp <number>\033[0m")


def load_into_shell_history(practical_num: int):
    """
    Inject commands directly into Kali shell history (~/.zsh_history and ~/.bash_history).
    The user can then literally press [Up Arrow] -> [Enter] for each command in their stock shell!
    """
    p = get_practical_by_id(practical_num)
    if not p:
        sys.stderr.write(f"[-] Error: Practical #{practical_num} not found (1-25).\n")
        return 1

    inputs = {inp["key"]: inp["default"] for inp in p.get("required_inputs", [])}
    commands = []
    for cmd_tmpl in p.get("default_commands", []):
        cmd = cmd_tmpl
        for k, v in inputs.items():
            cmd = cmd.replace(f"{{{k}}}", str(v))
        commands.append(cmd)

    if p.get("verification_commands"):
        for v_cmd_tmpl in p["verification_commands"]:
            cmd = v_cmd_tmpl
            for k, v in inputs.items():
                cmd = cmd.replace(f"{{{k}}}", str(v))
            commands.append(cmd)

    home = Path.home()
    now = int(time.time())

    # Append to ~/.zsh_history (Zsh format: ': timestamp:0;command\n')
    zsh_hist = home / ".zsh_history"
    try:
        with open(zsh_hist, "a", encoding="latin-1") as f:
            for idx, cmd in enumerate(commands):
                f.write(f": {now + idx}:0;{cmd}\n")
    except Exception:
        pass

    # Append to ~/.bash_history
    bash_hist = home / ".bash_history"
    try:
        with open(bash_hist, "a", encoding="utf-8") as f:
            for cmd in commands:
                f.write(f"{cmd}\n")
    except Exception:
        pass

    # Clear trigger command line
    sys.stdout.write("\033[1A\033[2K\r")
    sys.stdout.flush()

    # Inform user unobtrusively
    print(f"\033[1;32m[+]\033[0m Loaded {len(commands)} commands for Practical {practical_num} into shell history.")
    print("    Press \033[1m[Up Arrow]\033[0m then \033[1m[Enter]\033[0m to run each command step-by-step!")
    return 0


def execute_practical(practical_num: int, extra_args: list = []):
    p = get_practical_by_id(practical_num)
    if not p:
        sys.stderr.write(f"[-] Error: Practical #{practical_num} not found (1-25).\n")
        return 1

    # Check flags
    if any(a in extra_args for a in ("--hist", "--load", "load", "hist")):
        return load_into_shell_history(practical_num)

    step_mode = any(a in extra_args for a in ("--step", "-s", "step"))
    fast_mode = any(a in extra_args for a in ("--fast", "-f", "fast"))
    no_erase = any(a in extra_args for a in ("--no-erase", "-ne"))

    # Resolve required inputs / parameter overrides
    inputs = {inp["key"]: inp["default"] for inp in p.get("required_inputs", [])}

    # Positional target parameter
    pos_args = [a for a in extra_args if not a.startswith("-") and a not in ("load", "hist", "step", "fast")]
    if pos_args and p.get("required_inputs"):
        first_key = p["required_inputs"][0]["key"]
        inputs[first_key] = pos_args[0]

    # Format commands
    commands = []
    for cmd_tmpl in p.get("default_commands", []):
        cmd = cmd_tmpl
        for k, v in inputs.items():
            cmd = cmd.replace(f"{{{k}}}", str(v))
        commands.append(cmd)

    # Verification commands
    v_commands = []
    if p.get("verification_commands"):
        for v_cmd_tmpl in p["verification_commands"]:
            cmd = v_cmd_tmpl
            for k, v in inputs.items():
                cmd = cmd.replace(f"{{{k}}}", str(v))
            v_commands.append(cmd)

    all_commands = commands + v_commands

    # ERASE TRIGGER COMMAND
    # Erases the 2-line Kali prompt and command invocation line ("p 1")
    if not no_erase:
        sys.stdout.write("\033[2K\033[1A\033[2K\033[1A\033[2K\r")
        sys.stdout.flush()

    # Execute each command with authentic typing simulation
    for idx, cmd in enumerate(all_commands):
        try:
            # Print authentic Kali prompt
            print_kali_prompt()
            
            # Type out command keystroke-by-keystroke
            human_type(cmd, fast=fast_mode)

            # Genuinely execute command in Kali bash shell
            proc = subprocess.Popen(cmd, shell=True, executable=SHELL_EXE)
            proc.communicate()

            if proc.returncode != 0:
                # Command failed or exited with non-zero
                break

            # If in step mode, wait for user to press Enter to type next command
            if step_mode and idx < len(all_commands) - 1:
                try:
                    input()
                except (KeyboardInterrupt, EOFError):
                    break
            elif idx < len(all_commands) - 1:
                # Natural delay between commands
                delay = 0.05 if fast_mode else random.uniform(0.5, 0.9)
                time.sleep(delay)

        except KeyboardInterrupt:
            sys.stdout.write("^C\n")
            sys.stdout.flush()
            break

    return 0


def main():
    args = sys.argv[1:]
    if not args or args[0] in ("-h", "--help", "help"):
        print_help()
        return 0

    first = args[0].lower()

    if first in ("list", "ls", "-l", "--list"):
        list_practicals()
        return 0

    if first in ("load", "hist") and len(args) > 1 and args[1].isdigit():
        return load_into_shell_history(int(args[1]))

    if first.isdigit():
        return execute_practical(int(first), args[1:])

    # Support shorthand like p1, p01, #1
    cleaned = first.lstrip("p").lstrip("#")
    if cleaned.isdigit():
        return execute_practical(int(cleaned), args[1:])

    # Unrecognized syntax
    print_help()
    return 1


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        sys.stdout.write("\n")
        sys.exit(130)
