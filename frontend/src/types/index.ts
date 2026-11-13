export interface PracticalInput {
  key: string;
  label: string;
  type: 'string' | 'number' | 'boolean';
  default: any;
  description: string;
}

export interface Practical {
  id: number;
  number: number;
  title: string;
  category: 'Administration' | 'Scripting' | 'Security' | 'Networking' | 'System';
  difficulty: 'Beginner' | 'Intermediate' | 'Advanced';
  estimated_minutes: number;
  requires_sudo: boolean;
  is_destructive: boolean;
  tools_required: string[];
  aim: string;
  objective: string;
  algorithm: string[];
  required_inputs: PracticalInput[];
  default_commands: string[];
  verification_commands: string[];
  explanation: string;
}

export interface PlanStep {
  step_number: number;
  command: string;
  description: string;
  requires_sudo: boolean;
  risk_level: 'SAFE' | 'SENSITIVE' | 'CRITICAL_BLOCKED';
}

export interface ExecutionPlan {
  practical_id: number;
  number: number;
  title: string;
  category: string;
  aim: string;
  algorithm: string[];
  inputs: Record<string, any>;
  steps: PlanStep[];
  requires_confirmation: boolean;
  confirmation_reasons: string[];
  ai_notes: string;
}

export interface HistoryRecord {
  id: string;
  timestamp: string;
  practical_id: number;
  number: number;
  title: string;
  category: string;
  aim: string;
  algorithm: string[];
  commands: string[];
  output: string;
  status: 'SUCCESS' | 'FAILED' | 'ABORTED' | 'ERROR';
  duration_seconds: number;
  explanation: string;
  error?: string | null;
  markdown_record?: string;
  html_record?: string;
}

export interface SystemDiagnostics {
  platform: string;
  os_name: string;
  kernel_release: string;
  architecture: string;
  current_user: string;
  is_posix: boolean;
  is_kali: boolean;
  distro_name: string;
  distro_id: string;
  shell_available: boolean;
  shell_path: string;
  tools: Record<string, { installed: boolean; path: string }>;
  status_message: string;
  can_execute: boolean;
}

export interface SystemStatus {
  diagnostics: SystemDiagnostics;
  is_kali: boolean;
  terminal_active: boolean;
  total_practicals: number;
  completed_count: number;
  failed_count: number;
  is_executing: boolean;
}

export interface Settings {
  gemini_api_key: string;
  gemini_model: string;
  default_target_ip: string;
  default_interface: string;
  shell_path: string;
  pty_cols: number;
  pty_rows: number;
  safe_mode: boolean;
  theme: string;
  auto_verify: boolean;
}
