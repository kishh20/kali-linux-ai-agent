import { Practical, ExecutionPlan, HistoryRecord, SystemStatus, Settings } from '../types';

const API_BASE = '/api';

export async function fetchSystemStatus(): Promise<SystemStatus> {
  const res = await fetch(`${API_BASE}/status`);
  if (!res.ok) throw new Error('Failed to fetch system status');
  return res.json();
}

export async function fetchAllPracticals(): Promise<Practical[]> {
  const res = await fetch(`${API_BASE}/practicals`);
  if (!res.ok) throw new Error('Failed to fetch practicals');
  const data = await res.json();
  return data.practicals;
}

export async function fetchPracticalById(id: number): Promise<Practical> {
  const res = await fetch(`${API_BASE}/practicals/${id}`);
  if (!res.ok) throw new Error(`Failed to fetch practical ${id}`);
  return res.json();
}

export async function generateExecutionPlan(id: number, inputs: Record<string, any>): Promise<ExecutionPlan> {
  const res = await fetch(`${API_BASE}/practicals/${id}/plan`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ inputs })
  });
  if (!res.ok) {
    const err = await res.json().catch(() => ({ detail: 'Failed to generate plan' }));
    throw new Error(err.detail || 'Plan generation error');
  }
  return res.json();
}

export async function startExecution(id: number, inputs: Record<string, any>): Promise<any> {
  const res = await fetch(`${API_BASE}/practicals/${id}/execute`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ inputs })
  });
  if (!res.ok) {
    const err = await res.json().catch(() => ({ detail: 'Failed to execute practical' }));
    throw new Error(err.detail || 'Execution trigger error');
  }
  return res.json();
}

export async function stopExecution(): Promise<void> {
  await fetch(`${API_BASE}/practicals/stop`, { method: 'POST' });
}

export async function resetTerminal(): Promise<void> {
  await fetch(`${API_BASE}/terminal/reset`, { method: 'POST' });
}

export async function clearTerminal(): Promise<void> {
  await fetch(`${API_BASE}/terminal/clear`, { method: 'POST' });
}

export async function fetchHistory(): Promise<HistoryRecord[]> {
  const res = await fetch(`${API_BASE}/history`);
  if (!res.ok) throw new Error('Failed to fetch history');
  const data = await res.json();
  return data.history;
}

export async function explainTerminalOutput(command: string, output: string): Promise<string> {
  const res = await fetch(`${API_BASE}/ai/explain`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ command, output })
  });
  if (!res.ok) return 'Failed to query AI explanation.';
  const data = await res.json();
  return data.explanation;
}

export async function fetchSettings(): Promise<Settings> {
  const res = await fetch(`${API_BASE}/settings`);
  if (!res.ok) throw new Error('Failed to fetch settings');
  return res.json();
}

export async function updateSettings(settings: Partial<Settings>): Promise<Settings> {
  const res = await fetch(`${API_BASE}/settings`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(settings)
  });
  if (!res.ok) throw new Error('Failed to update settings');
  return res.json();
}
