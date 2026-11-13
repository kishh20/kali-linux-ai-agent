#!/usr/bin/env bash
# ==============================================================================
# Kali Linux Practical Automation - Global Setup Script
# ==============================================================================
set -e

DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" >/dev/null 2>&1 && pwd)"
cd "$DIR"

echo -e "\033[1;36m==============================================================\033[0m"
echo -e "\033[1;36m       KALI LINUX AI PRACTICAL AUTOMATION AGENT - SETUP       \033[0m"
echo -e "\033[1;36m==============================================================\033[0m"

# Ensure execution permissions on all scripts
chmod +x "$DIR/setup.sh" "$DIR/install_alias.sh" "$DIR/start.sh" "$DIR/p" "$DIR/run" "$DIR/kali-agent" "$DIR/stealth_agent.py" "$DIR/kali_agent.py" 2>/dev/null || true

# Check Python 3
if ! command -v python3 &>/dev/null; then
    echo -e "\033[1;31m[-] Python 3 not found. Installing...\033[0m"
    sudo apt update && sudo apt install -y python3 python3-pip python3-venv
fi

# Run alias installation
"$DIR/install_alias.sh"

echo -e "\033[1;32m[+] Ready to go! Choose your mode:\033[0m"
echo -e "  1. \033[1;33mStealth Terminal Mode:\033[0m  Type \033[1;32mp <1-25>\033[0m directly in terminal"
echo -e "  2. \033[1;33mWeb Dashboard Mode:\033[0m      Run \033[1;32m./start.sh\033[0m (opens on port 8000)"
echo -e "  3. \033[1;33mCyber CLI Agent:\033[0m         Run \033[1;32m./kali-agent\033[0m"
echo -e "\033[1;36m==============================================================\033[0m\n"
