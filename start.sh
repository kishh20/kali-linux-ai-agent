#!/usr/bin/env bash
# ==============================================================================
# Kali Linux AI Practical Automation Agent - Startup Script
# ==============================================================================
set -e

echo -e "\033[1;36m==========================================================\033[0m"
echo -e "\033[1;36m       KALI LINUX AI PRACTICAL AUTOMATION AGENT          \033[0m"
echo -e "\033[1;36m==========================================================\033[0m"

DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" >/dev/null 2>&1 && pwd)"
cd "$DIR"

# Verify Linux
if [ "$(uname)" != "Linux" ]; then
    echo -e "\033[1;33m[!] Notice: You are not running on Linux. Genuine PTY interactive execution requires Kali Linux.\033[0m"
fi

# Check Python 3
if ! command -v python3 &>/dev/null; then
    echo -e "\033[1;31m[-] Python 3 is required. Run: sudo apt update && sudo apt install -y python3 python3-pip python3-venv\033[0m"
    exit 1
fi

# Setup Python Virtual Environment if not present
if [ ! -d "venv" ]; then
    echo -e "\033[1;34m[*] Creating Python virtual environment...\033[0m"
    python3 -m venv venv 2>/dev/null || (echo -e "\033[1;33m[!] Note: If venv creation fails, install python3-venv: sudo apt install -y python3-venv\033[0m" && python3 -m pip install --user -r backend/requirements.txt --break-system-packages)
fi

if [ -f "venv/bin/activate" ]; then
    source venv/bin/activate
fi

echo -e "\033[1;34m[*] Installing / verifying backend dependencies...\033[0m"
pip install -r backend/requirements.txt --quiet 2>/dev/null || pip install -r backend/requirements.txt --break-system-packages --quiet

# Check Node.js / npm
HAS_NPM=false
if command -v npm &>/dev/null; then
    HAS_NPM=true
fi

# Clean cleanup on exit
cleanup() {
    echo -e "\n\033[1;33m[*] Shutting down Kali AI Agent services...\033[0m"
    kill "$BACKEND_PID" 2>/dev/null || true
    if [ "$HAS_NPM" = true ] && [ -n "$FRONTEND_PID" ]; then
        kill "$FRONTEND_PID" 2>/dev/null || true
    fi
    exit 0
}
trap cleanup SIGINT SIGTERM EXIT

echo -e "\033[1;32m[+] Starting FastAPI PTY Backend on port 8000...\033[0m"
(cd backend && uvicorn app.main:app --host 0.0.0.0 --port 8000) &
BACKEND_PID=$!

sleep 2

if [ "$HAS_NPM" = true ] && [ -d "frontend" ]; then
    echo -e "\033[1;34m[*] Node.js & npm detected. Starting Vite dev server on port 5173...\033[0m"
    if [ ! -d "frontend/node_modules" ]; then
        echo -e "\033[1;34m[*] Installing frontend npm dependencies...\033[0m"
        (cd frontend && npm install --quiet)
    fi
    (cd frontend && npm run dev -- --host 0.0.0.0) &
    FRONTEND_PID=$!
    
    echo -e "\n\033[1;36m==========================================================\033[0m"
    echo -e "\033[1;32m  KALI AGENT READY AT: http://localhost:5173              \033[0m"
    echo -e "\033[1;32m  OR DIRECT BACKEND AT: http://localhost:8000             \033[0m"
    echo -e "\033[1;36m==========================================================\033[0m"
else
    echo -e "\033[1;33m[*] Running in standalone mode (using pre-built UI bundle). Node.js not required!\033[0m"
    echo -e "\n\033[1;36m==========================================================\033[0m"
    echo -e "\033[1;32m  KALI AGENT READY AT: http://localhost:8000              \033[0m"
    echo -e "\033[1;36m==========================================================\033[0m"
fi

echo -e "Press Ctrl+C to stop services.\n"

wait "$BACKEND_PID"
