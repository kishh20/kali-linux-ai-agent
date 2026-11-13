import re
import ipaddress
from typing import Tuple, List, Dict, Any

# Critical commands that should never be executed
BLOCKED_PATTERNS = [
    r"rm\s+-rf\s+/\s*$",
    r"rm\s+-rf\s+/\*",
    r":\(\)\s*\{\s*:\s*\|\s*:\s*&\s*\}\s*;\s*:",   # Fork bomb
    r"mkfs\.(ext[234]|xfs|btrfs|vfat)\s+/dev/sd[a-z][0-9]*\b",
    r"mkfs\.(ext[234]|xfs|btrfs|vfat)\s+/dev/nvme[0-9]n[0-9]\b",
    r"dd\s+if=.*\s+of=/dev/(sd[a-z]|nvme[0-9]|hd[a-z])\b",
    r">\s*/dev/(sd[a-z]|nvme[0-9]|hd[a-z])\b",
    r"chmod\s+-R\s+[07]{3,4}\s+/\s*$",
    r"chown\s+-R\s+.*\s+/\s*$",
    r"cat\s+/dev/(urandom|zero)\s*>\s*/dev/sd[a-z]",
]

# Sensitive operations that require explicit user confirmation
SENSITIVE_PATTERNS = [
    r"\bsudo\s+ufw\b",
    r"\biptables\b",
    r"\bmkfs\b",
    r"\blosetup\b",
    r"\bmount\b",
    r"\bumount\b",
    r"\buserdel\b",
    r"\bgroupdel\b",
    r"\bpasswd\b",
    r"\bchage\b",
    r"\bvisudo\b",
    r"/etc/sudoers",
    r"\bshutdown\b",
    r"\breboot\b",
    r"\binit\s+[06]\b",
    r"\bsystemctl\s+(reboot|poweroff|halt)\b",
]

def validate_target_ip(ip_or_host: str) -> Tuple[bool, str]:
    """Ensure network scanning targets are restricted to localhost or authorized private lab IPs."""
    ip_or_host = ip_or_host.strip()
    if not ip_or_host:
        return False, "Target IP or hostname cannot be empty."
    
    if ip_or_host in ["localhost", "127.0.0.1", "::1", "scanme.nmap.org"]:
        return True, "Authorized lab target (Localhost/Testbed)."
        
    try:
        ip_obj = ipaddress.ip_address(ip_or_host)
        if ip_obj.is_loopback:
            return True, "Loopback address (Safe lab target)."
        if ip_obj.is_private:
            return True, f"Private network address ({ip_or_host}) allowed for local lab testing."
        return False, f"Target {ip_or_host} is a public internet address. Network reconnaissance is restricted to localhost or authorized lab private IP ranges."
    except ValueError:
        # Hostname provided
        if ip_or_host.endswith(".local") or ip_or_host.endswith(".lab"):
            return True, "Local network domain authorized."
        return False, f"Hostname '{ip_or_host}' must be localhost or local lab domain for safety."

def check_command_safety(command: str) -> Dict[str, Any]:
    """Analyze command for destructive patterns and sensitive operations."""
    cleaned = command.strip()
    
    for pat in BLOCKED_PATTERNS:
        if re.search(pat, cleaned, re.IGNORECASE):
            return {
                "allowed": False,
                "risk_level": "CRITICAL_BLOCKED",
                "reason": f"Command contains potentially catastrophic destructive pattern matching: {pat}",
                "requires_confirmation": False
            }
            
    for pat in SENSITIVE_PATTERNS:
        if re.search(pat, cleaned, re.IGNORECASE):
            return {
                "allowed": True,
                "risk_level": "SENSITIVE",
                "reason": "Command modifies system state (firewall, users, disk mounts, or privileges). Confirmation required.",
                "requires_confirmation": True
            }
            
    return {
        "allowed": True,
        "risk_level": "SAFE",
        "reason": "Standard practical command.",
        "requires_confirmation": False
    }

def sanitize_inputs(inputs: Dict[str, Any]) -> Dict[str, Any]:
    """Sanitize user-provided values to prevent shell injection escapes."""
    sanitized = {}
    for k, v in inputs.items():
        if isinstance(v, str):
            # Strip dangerous characters like semicolons or pipe escapes from variable parameters
            # allow standard path characters, alphanumeric, dots, dashes, underscores
            cleaned = re.sub(r"[;&|`$><]", "", v).strip()
            sanitized[k] = cleaned
        else:
            sanitized[k] = v
    return sanitized
