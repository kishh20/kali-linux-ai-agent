import os
import re
import time
import json
import asyncio
from typing import Dict, Any, List, Optional
from app.config import load_settings
from app.pty_manager import pty_manager
from app.safety import check_command_safety, validate_target_ip, sanitize_inputs
from app.practicals_data import get_practical_by_id
from app.lab_records import save_history_entry, generate_markdown_record, generate_html_record

# Try importing google-genai SDK
try:
    from google import genai
    from google.genai import types
    GENAI_AVAILABLE = True
except ImportError:
    GENAI_AVAILABLE = False

class KaliAgent:
    def __init__(self):
        self.is_executing = False
        self.abort_requested = False

    def _get_gemini_client(self) -> Optional[Any]:
        settings = load_settings()
        api_key = settings.get("gemini_api_key", "").strip()
        if not api_key or not GENAI_AVAILABLE:
            return None
        try:
            return genai.Client(api_key=api_key)
        except Exception as e:
            print(f"[KaliAgent] Failed to init GenAI Client: {e}")
            return None

    async def prepare_plan(self, practical_id: int, user_inputs: Dict[str, Any]) -> Dict[str, Any]:
        """
        Synthesize user inputs with practical requirements to build a validated execution plan.
        Leverages Gemini if configured, otherwise applies the verified built-in expert logic.
        """
        practical = get_practical_by_id(practical_id)
        if not practical:
            raise ValueError(f"Practical ID {practical_id} not found.")

        # Sanitize inputs
        clean_inputs = sanitize_inputs(user_inputs)

        # Merge with defaults
        final_inputs = {}
        for inp in practical.get("required_inputs", []):
            key = inp["key"]
            final_inputs[key] = clean_inputs.get(key, inp.get("default", ""))

        # If network target IP is present, validate safety
        if "target_ip" in final_inputs:
            valid, msg = validate_target_ip(str(final_inputs["target_ip"]))
            if not valid:
                raise ValueError(f"Security Policy Violation: {msg}")

        # Format default commands with parameters using safe key replacement
        formatted_commands = []
        for cmd_tmpl in practical.get("default_commands", []):
            formatted_cmd = cmd_tmpl
            for k, v in final_inputs.items():
                formatted_cmd = formatted_cmd.replace(f"{{{k}}}", str(v))
            formatted_commands.append(formatted_cmd)

        # Build steps
        steps = []
        requires_confirmation = False
        sensitive_reasons = []

        for idx, cmd in enumerate(formatted_commands, start=1):
            safety_eval = check_command_safety(cmd)
            if not safety_eval["allowed"]:
                raise ValueError(f"Safety Violation in Step {idx}: {safety_eval['reason']}")

            if safety_eval["requires_confirmation"]:
                requires_confirmation = True
                sensitive_reasons.append(f"Step {idx}: {safety_eval['reason']}")

            steps.append({
                "step_number": idx,
                "command": cmd,
                "description": f"Execute practical step {idx}",
                "requires_sudo": "sudo" in cmd,
                "risk_level": safety_eval["risk_level"]
            })

        # Try consulting Gemini for enhanced analysis and plan explanation
        ai_notes = ""
        client = self._get_gemini_client()
        if client:
            settings = load_settings()
            model_name = settings.get("gemini_model", "gemini-2.5-flash")
            prompt = (
                f"You are an expert Kali Linux systems instructor.\n"
                f"Review this practical exercise plan:\n"
                f"Title: {practical['title']}\n"
                f"Aim: {practical['aim']}\n"
                f"Commands to execute:\n{chr(10).join(formatted_commands)}\n\n"
                f"Provide a brief 2-3 sentence overview of why this execution sequence is safe and effective."
            )
            try:
                loop = asyncio.get_event_loop()
                response = await loop.run_in_executor(
                    None,
                    lambda: client.models.generate_content(
                        model=model_name,
                        contents=prompt
                    )
                )
                if response and response.text:
                    ai_notes = response.text.strip()
            except Exception as e:
                ai_notes = f"AI Advisory: Execution sequence verified with built-in rule heuristics. (Gemini note: {e})"
        else:
            ai_notes = "AI Advisory: Plan verified by Kali Linux Automation Engine. All commands conform to lab safety policy."

        return {
            "practical_id": practical["id"],
            "number": practical["number"],
            "title": practical["title"],
            "category": practical["category"],
            "aim": practical["aim"],
            "algorithm": practical["algorithm"],
            "inputs": final_inputs,
            "steps": steps,
            "requires_confirmation": requires_confirmation,
            "confirmation_reasons": sensitive_reasons,
            "ai_notes": ai_notes
        }

    async def execute_practical(self, plan: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute commands step-by-step through the real Kali PTY terminal.
        Monitors output in real time and detects command exit codes.
        """
        if self.is_executing:
            return {"status": "ERROR", "message": "Another practical execution is already in progress."}

        self.is_executing = True
        self.abort_requested = False

        practical_id = plan["practical_id"]
        practical = get_practical_by_id(practical_id)
        steps = plan.get("steps", [])
        total_steps = len(steps)

        executed_commands = []
        captured_outputs = []
        start_time = time.time()
        overall_status = "SUCCESS"
        failure_reason = None
        current_step_idx = 0

        await pty_manager.broadcast_event({
            "type": "execution_started",
            "practical_id": practical_id,
            "title": plan["title"],
            "total_steps": total_steps
        })

        try:
            for idx, step_info in enumerate(steps, start=1):
                if self.abort_requested:
                    overall_status = "ABORTED"
                    failure_reason = "Execution stopped by user."
                    break

                current_step_idx = idx
                cmd = step_info["command"]
                executed_commands.append(cmd)

                await pty_manager.broadcast_event({
                    "type": "step_start",
                    "step_number": idx,
                    "total_steps": total_steps,
                    "command": cmd,
                    "requires_sudo": step_info.get("requires_sudo", False)
                })

                # Execute command through the real Kali PTY session
                exec_result = await pty_manager.execute_command(cmd, timeout=90.0)
                exit_code = exec_result["exit_code"]
                output = exec_result["output"]
                captured_outputs.append(f"$ {cmd}\n{output}\n[Exit Code: {exit_code}]\n")

                if exit_code != 0:
                    # Command failed
                    overall_status = "FAILED"
                    failure_reason = f"Command at Step {idx} exited with error code {exit_code}."

                    # AI error diagnosis
                    ai_diagnostic = await self.diagnose_error(cmd, exit_code, output)

                    await pty_manager.broadcast_event({
                        "type": "step_failed",
                        "step_number": idx,
                        "exit_code": exit_code,
                        "output": output,
                        "error_diagnosis": ai_diagnostic
                    })
                    break
                else:
                    await pty_manager.broadcast_event({
                        "type": "step_success",
                        "step_number": idx,
                        "exit_code": 0,
                        "duration": exec_result.get("duration_seconds", 0)
                    })

                # Short breathing room between commands
                await asyncio.sleep(0.4)

            # Verification step if previous commands succeeded
            verification_output = ""
            if overall_status == "SUCCESS" and practical.get("verification_commands"):
                for v_cmd in practical["verification_commands"]:
                    v_res = await pty_manager.execute_command(v_cmd, timeout=30.0)
                    verification_output += f"\nVerification ($ {v_cmd}):\n{v_res['output']}\n"
                    if v_res["exit_code"] != 0:
                        overall_status = "FAILED"
                        failure_reason = f"Verification check failed: {v_cmd}"
                        break

            duration_total = round(time.time() - start_time, 2)
            full_terminal_output = "\n".join(captured_outputs) + verification_output

            # Create Record
            record_entry = {
                "id": f"exec_{int(time.time())}_{practical_id}",
                "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
                "practical_id": practical_id,
                "number": practical["number"],
                "title": practical["title"],
                "category": practical["category"],
                "aim": practical["aim"],
                "algorithm": practical["algorithm"],
                "commands": executed_commands,
                "output": full_terminal_output,
                "status": overall_status,
                "duration_seconds": duration_total,
                "explanation": practical.get("explanation", ""),
                "error": failure_reason
            }

            # Generate formatted reports
            record_entry["markdown_record"] = generate_markdown_record(record_entry)
            record_entry["html_record"] = generate_html_record(record_entry)

            # Persist to history database
            save_history_entry(record_entry)

            await pty_manager.broadcast_event({
                "type": "execution_completed",
                "practical_id": practical_id,
                "status": overall_status,
                "error": failure_reason,
                "duration": duration_total,
                "record": record_entry
            })

            return record_entry

        finally:
            self.is_executing = False
            self.abort_requested = False

    async def abort_execution(self):
        """Request interruption of running practical."""
        self.abort_requested = True
        await pty_manager.interrupt()

    async def diagnose_error(self, command: str, exit_code: int, output: str) -> str:
        """Use Gemini AI or rule heuristics to diagnose a command error."""
        client = self._get_gemini_client()
        if client:
            settings = load_settings()
            model_name = settings.get("gemini_model", "gemini-2.5-flash")
            prompt = (
                f"You are a Kali Linux debugging expert.\n"
                f"A command failed during a Linux practical lab:\n"
                f"Command: {command}\n"
                f"Exit Code: {exit_code}\n"
                f"Terminal Output:\n{output}\n\n"
                f"Provide a concise diagnosis: 1) What caused this error, and 2) How the user or system can fix it."
            )
            try:
                loop = asyncio.get_event_loop()
                response = await loop.run_in_executor(
                    None,
                    lambda: client.models.generate_content(
                        model=model_name,
                        contents=prompt
                    )
                )
                if response and response.text:
                    return response.text.strip()
            except Exception as e:
                pass

        # Fallback diagnostic heuristics
        if "Permission denied" in output:
            return "Diagnosis: Permission denied. This operation requires elevated privileges or sudo authentication."
        elif "command not found" in output:
            return f"Diagnosis: Missing utility. The required package for command '{command.split()[0]}' is not installed on this system."
        elif "No such file or directory" in output:
            return "Diagnosis: Path not found. A required input file or parent directory does not exist."
        elif "Address already in use" in output:
            return "Diagnosis: Port conflict. Another service is already bound to this network port."
        return f"Diagnosis: Process terminated with non-zero exit code {exit_code}. Check system journal or permissions."

    async def explain_output(self, command: str, output: str) -> str:
        """Explain terminal output using Gemini AI."""
        client = self._get_gemini_client()
        if client:
            settings = load_settings()
            model_name = settings.get("gemini_model", "gemini-2.5-flash")
            prompt = (
                f"Explain this Kali Linux command and its real terminal output to a Linux student:\n"
                f"Command: {command}\n"
                f"Output:\n{output}\n\n"
                f"Keep your explanation concise and educational."
            )
            try:
                loop = asyncio.get_event_loop()
                res = await loop.run_in_executor(
                    None,
                    lambda: client.models.generate_content(model=model_name, contents=prompt)
                )
                if res and res.text:
                    return res.text.strip()
            except Exception as e:
                return f"Error connecting to AI: {e}"

        return "Explanation: Command executed in Kali Linux shell. Output represents standard Linux kernel/userspace response."


agent = KaliAgent()
