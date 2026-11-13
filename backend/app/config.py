import os
import json
from pathlib import Path
from typing import Dict, Any
from dotenv import load_dotenv

# Load .env if present
load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(parents=True, exist_ok=True)

SETTINGS_FILE = DATA_DIR / "settings.json"
HISTORY_FILE = DATA_DIR / "history.json"

DEFAULT_SETTINGS: Dict[str, Any] = {
    "gemini_api_key": os.getenv("GEMINI_API_KEY", ""),
    "gemini_model": os.getenv("GEMINI_MODEL", "gemini-2.5-flash"),
    "default_target_ip": "127.0.0.1",
    "default_interface": "lo",
    "shell_path": "/bin/bash",
    "pty_cols": 120,
    "pty_rows": 32,
    "safe_mode": True,
    "theme": "kali-dark",
    "auto_verify": True
}

def load_settings() -> Dict[str, Any]:
    settings = DEFAULT_SETTINGS.copy()
    if SETTINGS_FILE.exists():
        try:
            with open(SETTINGS_FILE, "r", encoding="utf-8") as f:
                saved = json.load(f)
                settings.update(saved)
        except Exception as e:
            print(f"[Config] Error loading settings.json: {e}")
            
    # Environment variables override file settings if provided
    if os.getenv("GEMINI_API_KEY"):
        settings["gemini_api_key"] = os.getenv("GEMINI_API_KEY")
    return settings

def save_settings(new_settings: Dict[str, Any]) -> Dict[str, Any]:
    current = load_settings()
    current.update(new_settings)
    try:
        with open(SETTINGS_FILE, "w", encoding="utf-8") as f:
            json.dump(current, f, indent=2)
    except Exception as e:
        print(f"[Config] Error saving settings: {e}")
    return current
