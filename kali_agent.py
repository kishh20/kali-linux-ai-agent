#!/usr/bin/env bash
""":"
# Self-executing Python script
exec python3 "$0" "$@"
"""
import os
import sys
import time
import json
import shutil
import getpass
import platform
import subprocess
from pathlib import Path
from typing import Dict, Any, List, Optional

# Set up paths
BASE_DIR = Path(__file__).resolve().parent
RECORDS_DIR = BASE_DIR / "records"
RECORDS_DIR.mkdir(parents=True, exist_ok=True)
CONFIG_FILE = BASE_DIR / "agent_config.json"

# ANSI Color Codes for Kali Cyber Terminal
C_RESET = "\033[0m"
C_BOLD = "\033[1m"
C_CYAN = "\033[1;36m"
C_GREEN = "\033[1;32m"
C_BLUE = "\033[1;34m"
C_AMBER = "\033[1;33m"
C_RED = "\033[1;31m"
C_PURPLE = "\033[1;35m"
C_DIM = "\033[2m"

# Load practicals data
sys.path.insert(0, str(BASE_DIR / "backend"))
try:
    from app.practicals_data import PRACTICALS, get_practical_by_id
    from app.safety import check_command_safety, validate_target_ip, sanitize_inputs
except ImportError:
    print(f"{C_RED}[!] Error loading backend practical modules. Make sure backend/app/ exists.{C_RESET}")
    sys.exit(1)

# Default configuration
DEFAULT_CONFIG = {
    "gemini_api_key": os.getenv("GEMINI_API_KEY", ""),
    "gemini_model": os.getenv("GEMINI_MODEL", "gemini-2.5-flash"),
    "default_target_ip": "127.0.0.1",
    "default_interface": "lo",
    "safe_mode": True
}

def load_config() -> Dict[str, Any]:
    cfg = DEFAULT_CONFIG.copy()
    if CONFIG_FILE.exists():
        try:
            with open(CONFIG_FILE, "r") as f:
                cfg.update(json.load(f))
        except Exception:
            pass
    if os.getenv("GEMINI_API_KEY"):
        cfg["gemini_api_key"] = os.getenv("GEMINI_API_KEY")
    return cfg

def save_config(cfg: Dict[str, Any]):
    try:
        with open(CONFIG_FILE, "w") as f:
            json.dump(cfg, f, indent=2)
    except Exception as e:
        print(f"{C_RED}[-] Failed to save config: {e}{C_RESET}")

def clear_screen():
    print("\033[H\033[J", end="")

def print_banner():
    banner = f"""{C_CYAN}
  ██████╗ ███████╗    ███████╗██╗██████╗ ███╗   ███╗
 ██╔════╝██╔════╝    ██╔════╝██║██╔══██╗████╗ ████║
 ██║     █████╗      █████╗  ██║██████╔╝██╔████╔██║
 ██║     ██╔══╝      ██╔══╝  ██║██╔══██╗██║╚██╔╝██║
 ╚██████╗███████╗    ██║     ██║██║  ██║██║ ╚═╝ ██║
  ╚═════╝╚══════╝    ╚═╝     ╚═╝╚═╝  ╚═╝╚═╝     ╚═╝
  {C_BOLD}KALI LINUX AI PRACTICAL AUTOMATION AGENT{C_RESET}
  {C_DIM}Genuine Kali Terminal Execution &bull; 25 Practicals Supported{C_RESET}
"""
    print(banner)

def get_system_status():
    user = getpass.getuser()
    distro = "Linux"
    if os.path.exists("/etc/os-release"):
        with open("/etc/os-release", "r") as f:
            for line in f:
                if line.startswith("PRETTY_NAME="):
                    distro = line.split("=", 1)[1].strip().strip('"')
    return user, distro

def execute_shell_command(cmd: str) -> int:
    """Execute command in the genuine Kali Bash shell with real-time output and interactive input."""
    # Execute through bash interactive login mode
    process = subprocess.Popen(
        cmd,
        shell=True,
        executable="/bin/bash"
    )
    process.communicate()
    return process.returncode

def call_gemini(prompt: str) -> Optional[str]:
    """Optional Gemini AI call for error diagnosis or explanation."""
    cfg = load_config()
    api_key = cfg.get("gemini_api_key")
    if not api_key:
        return None
    try:
        from google import genai
        client = genai.Client(api_key=api_key)
        res = client.models.generate_content(
            model=cfg.get("gemini_model", "gemini-2.5-flash"),
            contents=prompt
        )
        if res and res.text:
            return res.text.strip()
    except Exception:
        pass
    return None

def run_practical(practical: Dict[str, Any], custom_inputs: Optional[Dict[str, Any]] = None):
    """Execute a single practical in the Kali Linux terminal."""
    clear_screen()
    print_banner()

    user, distro = get_system_status()
    num_str = f"#{practical['number']:02d}"
    print(f"{C_BOLD}{C_CYAN}=== RUNNING PRACTICAL {num_str}: {practical['title']} ==={C_RESET}")
    print(f"{C_DIM}Category: {practical['category']} | Difficulty: {practical['difficulty']} | Host: {user}@{distro}{C_RESET}\n")

    print(f"{C_BOLD}{C_GREEN}[AIM]{C_RESET}")
    print(f"  {practical['aim']}\n")

    print(f"{C_BOLD}{C_BLUE}[OBJECTIVE]{C_RESET}")
    print(f"  {practical['objective']}\n")

    # Handle parameters
    final_inputs = {}
    if practical.get("required_inputs"):
        print(f"{C_BOLD}{C_AMBER}[REQUIRED INPUTS]{C_RESET}")
        for inp in practical["required_inputs"]:
            key = inp["key"]
            if custom_inputs and key in custom_inputs:
                final_inputs[key] = custom_inputs[key]
                print(f"  {inp['label']}: {final_inputs[key]} (custom)")
            else:
                default = inp["default"]
                prompt_text = f"  {inp['label']} [{default}]: "
                try:
                    val = input(prompt_text).strip()
                    final_inputs[key] = val if val else default
                except (KeyboardInterrupt, EOFError):
                    print(f"\n{C_AMBER}[*] Practical aborted by user.{C_RESET}")
                    return
        print()

    # Prepare formatted commands
    commands = []
    for cmd_tmpl in practical.get("default_commands", []):
        cmd = cmd_tmpl
        for k, v in final_inputs.items():
            cmd = cmd.replace(f"{{{k}}}", str(v))
        commands.append(cmd)

    # Validate commands with safety engine
    print(f"{C_BOLD}{C_CYAN}[EXECUTION PLAN - {len(commands)} STEPS]{C_RESET}")
    sensitive_steps = []
    for idx, cmd in enumerate(commands, start=1):
        safety = check_command_safety(cmd)
        if not safety["allowed"]:
            print(f"{C_RED}[!] CRITICAL SAFETY ERROR in Step {idx}: {safety['reason']}{C_RESET}")
            input(f"\n{C_AMBER}Press Enter to return to menu...{C_RESET}")
            return
        if safety["requires_confirmation"]:
            sensitive_steps.append((idx, cmd, safety["reason"]))
        
        sudo_tag = f"{C_AMBER}[sudo]{C_RESET} " if "sudo" in cmd else ""
        print(f"  {C_DIM}{idx:02d}.{C_RESET} {sudo_tag}{C_GREEN}$ {cmd}{C_RESET}")

    print()

    # Safety confirmation if needed
    if sensitive_steps:
        print(f"{C_BOLD}{C_AMBER}[!] SAFETY CONFIRMATION REQUIRED:{C_RESET}")
        for idx, cmd, reason in sensitive_steps:
            print(f"  - Step {idx}: {reason}")
        try:
            confirm = input(f"\n{C_BOLD}Authorize execution on this Kali Linux machine? (y/N): {C_RESET}").strip().lower()
            if confirm != 'y' and confirm != 'yes':
                print(f"{C_AMBER}[*] Execution cancelled by user.{C_RESET}")
                time.sleep(1)
                return
        except (KeyboardInterrupt, EOFError):
            return

    # Ready prompt
    try:
        input(f"\n{C_BOLD}{C_CYAN}Press Enter to start execution in your Kali Linux shell...{C_RESET}")
    except (KeyboardInterrupt, EOFError):
        return

    print(f"\n{C_CYAN}==================== [STARTING SHELL EXECUTION] ===================={C_RESET}\n")

    executed_cmds = []
    accumulated_output = []
    start_time = time.time()
    practical_status = "SUCCESS"
    failed_step = None

    for idx, cmd in enumerate(commands, start=1):
        print(f"{C_BOLD}{C_BLUE}--- [Step {idx}/{len(commands)}] ---{C_RESET}")
        print(f"{C_BOLD}{C_GREEN}kali@agent:$ {cmd}{C_RESET}")

        executed_cmds.append(cmd)
        
        # Execute genuine command directly in Kali Linux shell!
        exit_code = execute_shell_command(cmd)

        if exit_code != 0:
            practical_status = "FAILED"
            failed_step = (idx, cmd, exit_code)
            print(f"\n{C_BOLD}{C_RED}[-] Step {idx} FAILED with exit code {exit_code}!{C_RESET}")
            
            # Diagnose with Gemini if available
            diagnosis = call_gemini(f"A Kali Linux command failed during lab: '{cmd}' with exit code {exit_code}. Provide a 2 sentence diagnosis and fix.")
            if diagnosis:
                print(f"{C_PURPLE}[AI Diagnosis]: {diagnosis}{C_RESET}")
            break
        else:
            print(f"{C_DIM}[Step {idx} completed successfully]{C_RESET}\n")

    # Verification if all steps succeeded
    if practical_status == "SUCCESS" and practical.get("verification_commands"):
        print(f"{C_BOLD}{C_CYAN}--- [Running Verification Checks] ---{C_RESET}")
        for v_cmd in practical["verification_commands"]:
            print(f"{C_GREEN}kali@agent:$ {v_cmd}{C_RESET}")
            v_code = execute_shell_command(v_cmd)
            if v_code != 0:
                practical_status = "FAILED"
                print(f"{C_RED}[-] Verification command failed: {v_cmd}{C_RESET}")
                break

    duration = round(time.time() - start_time, 2)
    print(f"\n{C_CYAN}==================== [EXECUTION COMPLETE] ===================={C_RESET}\n")

    if practical_status == "SUCCESS":
        print(f"{C_BOLD}{C_GREEN}✓ PRACTICAL COMPLETED SUCCESSFULLY!{C_RESET}")
        print(f"  Duration: {duration} seconds | Status: VERIFIED PASSED")
    else:
        print(f"{C_BOLD}{C_RED}✗ PRACTICAL EXECUTION FAILED{C_RESET}")
        if failed_step:
            print(f"  Failed at Step {failed_step[0]}: {failed_step[1]} (Exit Code: {failed_step[2]})")

    # Generate and save official Lab Record
    record_filename = f"Practical_{practical['number']:02d}_{practical['title'].replace(' ', '_')}.md"
    record_path = RECORDS_DIR / record_filename

    algo_text = "\n".join([f"{step}" for step in practical['algorithm']])
    cmds_text = "\n".join([f"$ {c}" for c in executed_cmds])

    record_content = f"""# PRACTICAL RECORD: EXPERIMENT {practical['number']}
## {practical['title']}

**Date of Execution:** {time.strftime('%Y-%m-%d %H:%M:%S')}  
**Execution Status:** {"[SUCCESS] PASSED" if practical_status == "SUCCESS" else "[FAILED] INCOMPLETE"}  
**Operating System:** {distro}  
**User:** {user}  
**Duration:** {duration}s  

---

### 1. AIM
{practical['aim']}

---

### 2. ALGORITHM
```text
{algo_text}
```

---

### 3. COMMANDS EXECUTED
```bash
{cmds_text}
```

---

### 4. TECHNICAL EXPLANATION
{practical['explanation']}

---

### 5. RESULT
The practical experiment **'{practical['title']}'** was {"successfully completed and verified on Kali Linux." if practical_status == "SUCCESS" else "executed with errors. Check terminal output for details."}
"""

    with open(record_path, "w", encoding="utf-8") as rf:
        rf.write(record_content)

    print(f"\n{C_BOLD}{C_CYAN}[+] Official Lab Record Saved:{C_RESET}")
    print(f"    {C_GREEN}{record_path}{C_RESET}")

    try:
        input(f"\n{C_DIM}Press Enter to return to menu...{C_RESET}")
    except (KeyboardInterrupt, EOFError):
        pass

def search_practicals():
    clear_screen()
    print_banner()
    query = input(f"{C_BOLD}{C_CYAN}Search practicals (e.g. nmap, wireshark, ufw, permissions): {C_RESET}").strip().lower()
    if not query:
        return

    matches = []
    for p in PRACTICALS:
        if (query in p['title'].lower() or 
            query in p['aim'].lower() or 
            query in p['category'].lower() or
            any(query in t for t in p.get('tools_required', []))):
            matches.append(p)

    print(f"\n{C_BOLD}Search Results for '{query}' ({len(matches)} matches):{C_RESET}")
    print(f"{C_DIM}{'=' * 65}{C_RESET}")
    for p in matches:
        sudo_tag = f"{C_AMBER}[sudo]{C_RESET}" if p.get('requires_sudo') else "      "
        print(f"  {C_BOLD}{C_CYAN}#{p['number']:02d}{C_RESET} {sudo_tag} {C_BOLD}{p['title']}{C_RESET}")
        print(f"       {C_DIM}{p['aim'][:75]}...{C_RESET}")
    print(f"{C_DIM}{'=' * 65}{C_RESET}")

    choice = input(f"\nEnter Practical number to run (or Enter to cancel): ").strip()
    if choice.isdigit():
        p = get_practical_by_id(int(choice))
        if p:
            run_practical(p)

def list_all_practicals():
    clear_screen()
    print_banner()
    print(f"{C_BOLD}{C_CYAN}=== ALL 25 KALI LINUX PRACTICAL QUESTIONS ==={C_RESET}\n")
    print(f" {'#':<3} {'Category':<16} {'Difficulty':<12} {'Sudo':<6} {'Title'}")
    print(f" {C_DIM}{'-'*70}{C_RESET}")
    
    for p in PRACTICALS:
        sudo_str = "Yes" if p.get('requires_sudo') else "No"
        diff_color = C_GREEN if p['difficulty'] == "Beginner" else (C_AMBER if p['difficulty'] == "Intermediate" else C_RED)
        print(f" {C_CYAN}#{p['number']:02d}{C_RESET} {p['category']:<16} {diff_color}{p['difficulty']:<12}{C_RESET} {sudo_str:<6} {C_BOLD}{p['title']}{C_RESET}")

    print(f"\n {C_DIM}Enter a number [1-25] to execute, or press Enter to return.{C_RESET}")
    choice = input(f" {C_BOLD}Select Practical: {C_RESET}").strip()
    if choice.isdigit():
        p = get_practical_by_id(int(choice))
        if p:
            run_practical(p)

def view_records():
    clear_screen()
    print_banner()
    print(f"{C_BOLD}{C_CYAN}=== GENERATED LAB RECORDS ==={C_RESET}\n")
    records = list(RECORDS_DIR.glob("*.md"))
    if not records:
        print(f"  {C_DIM}No lab records generated yet. Run a practical to generate records.{C_RESET}")
    else:
        for idx, rec in enumerate(records, start=1):
            print(f"  {C_BOLD}{idx:02d}.{C_RESET} {rec.name}")
    try:
        input(f"\n{C_DIM}Press Enter to return...{C_RESET}")
    except (KeyboardInterrupt, EOFError):
        pass

def configure_settings():
    clear_screen()
    print_banner()
    cfg = load_config()
    print(f"{C_BOLD}{C_CYAN}=== AGENT CONFIGURATION ==={C_RESET}\n")
    print(f"1. Gemini API Key: {'*' * 8 if cfg.get('gemini_api_key') else '(Not Set - Running in offline mode)'}")
    print(f"2. Gemini Model:   {cfg.get('gemini_model')}")
    print(f"3. Lab Target IP:  {cfg.get('default_target_ip')}")
    print(f"4. Interface:      {cfg.get('default_interface')}")
    print()

    key_input = input("Enter Gemini API Key (or press Enter to keep current): ").strip()
    if key_input:
        cfg["gemini_api_key"] = key_input

    save_config(cfg)
    print(f"{C_GREEN}[+] Settings updated.{C_RESET}")
    time.sleep(1)

def main():
    # Check CLI arguments for fast single-practical execution
    if len(sys.argv) > 1:
        if sys.argv[1] in ("--help", "-h"):
            print("Usage: python3 kali_agent.py [--run <1-25>] [--list]")
            sys.exit(0)
        elif sys.argv[1] == "--list":
            list_all_practicals()
            sys.exit(0)
        elif sys.argv[1] == "--run" and len(sys.argv) > 2:
            try:
                num = int(sys.argv[2])
                p = get_practical_by_id(num)
                if p:
                    run_practical(p)
                else:
                    print(f"{C_RED}[-] Practical #{num} not found. Must be 1-25.{C_RESET}")
                sys.exit(0)
            except ValueError:
                print(f"{C_RED}[-] Invalid practical number.{C_RESET}")
                sys.exit(1)

    # Main Interactive Terminal Loop
    while True:
        clear_screen()
        print_banner()
        user, distro = get_system_status()
        print(f"  {C_GREEN}● Shell Connected:{C_RESET} {C_BOLD}{user}@{distro}{C_RESET} | {C_CYAN}25 Practicals Available{C_RESET}\n")

        print(f"  {C_BOLD}[1-25]{C_RESET} Run Practical by Number")
        print(f"  {C_BOLD}[l]{C_RESET}    List All 25 Practicals (with details)")
        print(f"  {C_BOLD}[s]{C_RESET}    Search Practicals by Tool/Keyword (Nmap, UFW, IPTables...)")
        print(f"  {C_BOLD}[r]{C_RESET}    View Saved Lab Records")
        print(f"  {C_BOLD}[c]{C_RESET}    Agent Settings & Gemini API Key")
        print(f"  {C_BOLD}[q]{C_RESET}    Exit\n")

        try:
            choice = input(f"{C_BOLD}{C_CYAN}kali-agent> {C_RESET}").strip().lower()
        except (KeyboardInterrupt, EOFError):
            print("\nExiting Kali Agent. Goodbye!")
            break

        if choice in ('q', 'exit', 'quit'):
            print("Exiting Kali Agent. Goodbye!")
            break
        elif choice == 'l':
            list_all_practicals()
        elif choice == 's':
            search_practicals()
        elif choice == 'r':
            view_records()
        elif choice == 'c':
            configure_settings()
        elif choice.isdigit():
            num = int(choice)
            if 1 <= num <= 25:
                p = get_practical_by_id(num)
                if p:
                    run_practical(p)
            else:
                print(f"{C_RED}[!] Please enter a number between 1 and 25.{C_RESET}")
                time.sleep(1)
        else:
            print(f"{C_AMBER}[!] Unknown option: {choice}{C_RESET}")
            time.sleep(1)

if __name__ == "__main__":
    main()
