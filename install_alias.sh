#!/usr/bin/env bash
# ==============================================================================
# Kali Linux Practical Automation - One-Click Stealth Setup
# ==============================================================================
DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" >/dev/null 2>&1 && pwd)"

# Ensure scripts have execute permissions
chmod +x "$DIR/p" "$DIR/run" "$DIR/kali-agent" "$DIR/stealth_agent.py" "$DIR/kali_agent.py" "$DIR/start.sh" "$DIR/install_alias.sh" 2>/dev/null || true

# Construct exact alias command with escaped quotes so paths with spaces work 100%
ALIAS_BLOCK="
# --- Kali Practical Automation Stealth Aliases ---
alias p='python3 \"$DIR/stealth_agent.py\"'
alias run='python3 \"$DIR/stealth_agent.py\"'
"

# Add to ~/.zshrc if exists
if [ -f "$HOME/.zshrc" ]; then
    if ! grep -q "stealth_agent.py" "$HOME/.zshrc" 2>/dev/null; then
        echo -e "$ALIAS_BLOCK" >> "$HOME/.zshrc"
        echo "[+] Added alias 'p' and 'run' to $HOME/.zshrc"
    else
        echo "[*] Alias already present in $HOME/.zshrc"
    fi
fi

# Add to ~/.bashrc if exists
if [ -f "$HOME/.bashrc" ]; then
    if ! grep -q "stealth_agent.py" "$HOME/.bashrc" 2>/dev/null; then
        echo -e "$ALIAS_BLOCK" >> "$HOME/.bashrc"
        echo "[+] Added alias 'p' and 'run' to $HOME/.bashrc"
    else
        echo "[*] Alias already present in $HOME/.bashrc"
    fi
fi

echo -e "\n\033[1;32m[✓] Stealth Alias Setup Complete!\033[0m"
echo -e "You can now run practicals directly in any native Kali terminal:"
echo -e "  \033[1;33mp 1\033[0m            Run Practical 1"
echo -e "  \033[1;33mp 18\033[0m           Run Practical 18"
echo -e "  \033[1;33mp load <num>\033[0m   Load into shell history (press Up Arrow -> Enter)"
echo -e "  \033[1;33mp list\033[0m         List all 25 practicals"
echo -e "\nTo activate in your current terminal session immediately, run:"
echo -e "  \033[1;36msource ~/.zshrc\033[0m  (or \033[1;36msource ~/.bashrc\033[0m)\n"
