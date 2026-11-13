import os
import json
import asyncio
from typing import Dict, Any, Optional
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException, Body
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, PlainTextResponse

from app.config import load_settings, save_settings
from app.pty_manager import pty_manager
from app.practicals_data import get_all_practicals, get_practical_by_id
from app.agent import agent
from app.lab_records import load_history

app = FastAPI(
    title="Kali Linux AI Practical Automation Agent",
    description="Real Kali Linux terminal automation backend with PTY integration and Gemini AI intelligence",
    version="1.0.0"
)

# Enable CORS for frontend UI
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def on_startup():
    print("[Main] Initializing Kali Linux PTY Manager...")
    await pty_manager.start()

@app.get("/api/status")
async def get_system_status():
    """Return live system environment diagnostics, Kali detection, and tooling status."""
    diagnostics = pty_manager.get_system_diagnostics()
    history = load_history()
    
    completed = sum(1 for h in history if h.get("status") == "SUCCESS")
    failed = sum(1 for h in history if h.get("status") in ["FAILED", "ERROR"])
    
    return {
        "diagnostics": diagnostics,
        "is_kali": diagnostics.get("is_kali", False),
        "terminal_active": pty_manager.is_running,
        "total_practicals": 25,
        "completed_count": completed,
        "failed_count": failed,
        "is_executing": agent.is_executing
    }

@app.get("/api/practicals")
async def list_practicals():
    """Return catalog of all 25 Kali Linux practicals."""
    return {"practicals": get_all_practicals()}

@app.get("/api/practicals/{practical_id}")
async def get_practical(practical_id: int):
    """Retrieve full specification for a single practical."""
    p = get_practical_by_id(practical_id)
    if not p:
        raise HTTPException(status_code=404, detail=f"Practical {practical_id} not found.")
    return p

@app.post("/api/practicals/{practical_id}/plan")
async def prepare_plan(practical_id: int, payload: Dict[str, Any] = Body(default={})):
    """Generate and validate step-by-step execution plan."""
    user_inputs = payload.get("inputs", {})
    try:
        plan = await agent.prepare_plan(practical_id, user_inputs)
        return plan
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error preparing execution plan: {e}")

@app.post("/api/practicals/{practical_id}/execute")
async def execute_practical(practical_id: int, payload: Dict[str, Any] = Body(default={})):
    """Trigger step-by-step execution through the real Kali PTY terminal."""
    if agent.is_executing:
        raise HTTPException(status_code=409, detail="An execution is already actively running.")
    
    user_inputs = payload.get("inputs", {})
    try:
        plan = await agent.prepare_plan(practical_id, user_inputs)
        # Run execution asynchronously in background task so API responds immediately
        asyncio.create_task(agent.execute_practical(plan))
        return {
            "status": "RUNNING",
            "message": f"Practical {practical_id} started in Kali terminal.",
            "plan": plan
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/practicals/stop")
async def stop_execution():
    """Abort ongoing practical execution."""
    await agent.abort_execution()
    return {"status": "ABORT_REQUESTED"}

@app.post("/api/terminal/reset")
async def reset_terminal():
    """Reset terminal PTY session."""
    await pty_manager.reset()
    return {"status": "RESET_COMPLETED"}

@app.post("/api/terminal/clear")
async def clear_terminal():
    """Send screen clear command to PTY."""
    pty_manager.write_input("\x0cclear\n")
    return {"status": "CLEARED"}

@app.get("/api/history")
async def get_history():
    """Return execution history records."""
    return {"history": load_history()}

@app.get("/api/history/{record_id}/markdown")
async def get_history_markdown(record_id: str):
    """Retrieve markdown report for an execution."""
    history = load_history()
    for item in history:
        if item.get("id") == record_id:
            md = item.get("markdown_record", "")
            return PlainTextResponse(md, media_type="text/markdown")
    raise HTTPException(status_code=404, detail="Record not found.")

@app.get("/api/history/{record_id}/html")
async def get_history_html(record_id: str):
    """Retrieve printable HTML lab record."""
    history = load_history()
    for item in history:
        if item.get("id") == record_id:
            html = item.get("html_record", "")
            return HTMLResponse(html)
    raise HTTPException(status_code=404, detail="Record not found.")

@app.post("/api/ai/explain")
async def explain_output(payload: Dict[str, Any] = Body(...)):
    """Explain command output using Gemini AI."""
    command = payload.get("command", "")
    output = payload.get("output", "")
    explanation = await agent.explain_output(command, output)
    return {"explanation": explanation}

@app.get("/api/settings")
async def get_settings():
    """Get current configuration."""
    return load_settings()

@app.post("/api/settings")
async def update_settings(new_settings: Dict[str, Any] = Body(...)):
    """Update configuration settings."""
    updated = save_settings(new_settings)
    return updated

@app.websocket("/ws/terminal")
async def websocket_terminal_endpoint(websocket: WebSocket):
    """
    Bi-directional WebSocket connection connected directly to the real Kali Linux PTY.
    Streams raw terminal byte streams and accepts direct client keyboard input.
    """
    await websocket.accept()
    pty_manager.subscribe(websocket)

    # Immediately transmit existing terminal buffer so user doesn't lose context
    if pty_manager.terminal_buffer:
        try:
            await websocket.send_text(json.dumps({
                "type": "terminal_output",
                "data": pty_manager.terminal_buffer
            }))
        except Exception:
            pass

    try:
        while True:
            raw_msg = await websocket.receive_text()
            try:
                msg = json.loads(raw_msg)
                msg_type = msg.get("type")

                if msg_type == "input":
                    data = msg.get("data", "")
                    pty_manager.write_input(data)

                elif msg_type == "resize":
                    cols = msg.get("cols", 120)
                    rows = msg.get("rows", 32)
                    pty_manager.resize(cols, rows)

                elif msg_type == "ping":
                    await websocket.send_text(json.dumps({"type": "pong"}))

            except json.JSONDecodeError:
                # Raw text input fallback
                pty_manager.write_input(raw_msg)

    except WebSocketDisconnect:
        pty_manager.unsubscribe(websocket)
    except Exception as e:
        print(f"[WebSocket] Exception: {e}")
        pty_manager.unsubscribe(websocket)

# Mount static frontend production build if present (enables zero-node execution)
from pathlib import Path
from fastapi.staticfiles import StaticFiles

FRONTEND_DIST = Path(__file__).resolve().parent.parent.parent / "frontend" / "dist"
if FRONTEND_DIST.exists():
    app.mount("/", StaticFiles(directory=str(FRONTEND_DIST), html=True), name="static")

