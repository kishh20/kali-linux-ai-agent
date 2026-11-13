@echo off
echo ==========================================================
echo        KALI LINUX AI PRACTICAL AUTOMATION AGENT
echo ==========================================================
echo [*] Notice: Running on Windows. Real PTY execution requires Kali Linux.
echo [*] Starting FastAPI Backend on port 8000...
start cmd /k "cd backend && python -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload"

echo [*] Starting Frontend on port 5173...
start cmd /k "cd frontend && npm.cmd run dev"

echo.
echo ==========================================================
echo   KALI AGENT UI AVAILABLE AT: http://localhost:5173
echo ==========================================================
echo.
