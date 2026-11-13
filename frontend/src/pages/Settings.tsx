import React, { useState, useEffect } from 'react';
import { 
  Settings as SettingsIcon, 
  Key, 
  Cpu, 
  Shield, 
  Network, 
  Terminal, 
  Save, 
  Check, 
  AlertCircle 
} from 'lucide-react';
import { Settings as SettingsType } from '../types';
import { fetchSettings, updateSettings } from '../services/api';

export const Settings: React.FC = () => {
  const [settings, setSettings] = useState<SettingsType>({
    gemini_api_key: '',
    gemini_model: 'gemini-2.5-flash',
    default_target_ip: '127.0.0.1',
    default_interface: 'lo',
    shell_path: '/bin/bash',
    pty_cols: 120,
    pty_rows: 32,
    safe_mode: true,
    theme: 'kali-dark',
    auto_verify: true
  });

  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [savedSuccess, setSavedSuccess] = useState(false);
  const [showApiKey, setShowApiKey] = useState(false);

  useEffect(() => {
    fetchSettings()
      .then((data) => {
        setSettings(data);
        setLoading(false);
      })
      .catch((err) => {
        console.error('Error fetching settings:', err);
        setLoading(false);
      });
  }, []);

  const handleSave = async (e: React.FormEvent) => {
    e.preventDefault();
    setSaving(true);
    try {
      const updated = await updateSettings(settings);
      setSettings(updated);
      setSavedSuccess(true);
      setTimeout(() => setSavedSuccess(false), 2500);
    } catch (err: any) {
      alert(`Failed to save settings: ${err.message}`);
    } finally {
      setSaving(false);
    }
  };

  if (loading) {
    return <div className="p-8 text-center text-slate-500 text-sm">Loading settings...</div>;
  }

  return (
    <div className="flex-1 p-6 overflow-y-auto space-y-6 max-w-4xl">
      
      {/* Title */}
      <div>
        <h2 className="text-xl font-bold text-white tracking-tight flex items-center space-x-2">
          <SettingsIcon className="w-5 h-5 text-kali-cyan" />
          <span>Application and Shell Configuration</span>
        </h2>
        <p className="text-xs text-slate-400 mt-1">
          Configure Gemini AI integration, default lab network interfaces, shell parameters, and execution safety policies.
        </p>
      </div>

      <form onSubmit={handleSave} className="space-y-6">
        
        {/* Gemini AI Intelligence Section */}
        <div className="glass-card rounded-xl p-5 border border-kali-border space-y-4">
          <div className="flex items-center space-x-2 pb-3 border-b border-slate-800">
            <Key className="w-4 h-4 text-kali-cyan" />
            <h3 className="text-sm font-bold text-white">Google Gemini AI Intelligence</h3>
          </div>

          <div className="space-y-3">
            <div>
              <label className="block text-xs font-medium text-slate-300 mb-1">
                Gemini API Key
              </label>
              <div className="relative">
                <input
                  type={showApiKey ? 'text' : 'password'}
                  value={settings.gemini_api_key}
                  onChange={(e) => setSettings({ ...settings, gemini_api_key: e.target.value })}
                  placeholder="AIzaSy..."
                  className="w-full px-3 py-2 pr-20 rounded-lg bg-slate-900 border border-slate-700 text-xs text-white font-mono focus:outline-none focus:border-kali-cyan"
                />
                <button
                  type="button"
                  onClick={() => setShowApiKey(!showApiKey)}
                  className="absolute right-2 top-1/2 -translate-y-1/2 px-2 py-0.5 rounded text-[10px] bg-slate-800 text-slate-400 hover:text-white"
                >
                  {showApiKey ? 'Hide' : 'Show'}
                </button>
              </div>
              <p className="text-[11px] text-slate-500 mt-1">
                Used for adaptive execution planning, intelligent terminal error diagnostics, and record generation.
                If empty, the agent uses the built-in deterministic rule heuristics.
              </p>
            </div>

            <div>
              <label className="block text-xs font-medium text-slate-300 mb-1">
                Gemini Model
              </label>
              <select
                value={settings.gemini_model}
                onChange={(e) => setSettings({ ...settings, gemini_model: e.target.value })}
                className="w-full px-3 py-2 rounded-lg bg-slate-900 border border-slate-700 text-xs text-white font-mono focus:outline-none focus:border-kali-cyan"
              >
                <option value="gemini-2.5-flash">gemini-2.5-flash (Fast & Recommended)</option>
                <option value="gemini-2.5-pro">gemini-2.5-pro (Deep Reasoning)</option>
                <option value="gemini-1.5-flash">gemini-1.5-flash (Legacy)</option>
              </select>
            </div>
          </div>
        </div>

        {/* Network & Lab Defaults */}
        <div className="glass-card rounded-xl p-5 border border-kali-border space-y-4">
          <div className="flex items-center space-x-2 pb-3 border-b border-slate-800">
            <Network className="w-4 h-4 text-kali-cyan" />
            <h3 className="text-sm font-bold text-white">Lab & Network Defaults</h3>
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
            <div>
              <label className="block text-xs font-medium text-slate-300 mb-1">
                Authorized Lab Target IP
              </label>
              <input
                type="text"
                value={settings.default_target_ip}
                onChange={(e) => setSettings({ ...settings, default_target_ip: e.target.value })}
                className="w-full px-3 py-2 rounded-lg bg-slate-900 border border-slate-700 text-xs text-white font-mono focus:outline-none focus:border-kali-cyan"
              />
              <p className="text-[11px] text-slate-500 mt-1">Restricted to localhost (127.0.0.1) or private lab subnets.</p>
            </div>

            <div>
              <label className="block text-xs font-medium text-slate-300 mb-1">
                Default Capture Interface
              </label>
              <input
                type="text"
                value={settings.default_interface}
                onChange={(e) => setSettings({ ...settings, default_interface: e.target.value })}
                className="w-full px-3 py-2 rounded-lg bg-slate-900 border border-slate-700 text-xs text-white font-mono focus:outline-none focus:border-kali-cyan"
              />
              <p className="text-[11px] text-slate-500 mt-1">Default interface for Wireshark and tshark (lo, eth0, wlan0).</p>
            </div>
          </div>
        </div>

        {/* Shell & Safety Controls */}
        <div className="glass-card rounded-xl p-5 border border-kali-border space-y-4">
          <div className="flex items-center space-x-2 pb-3 border-b border-slate-800">
            <Shield className="w-4 h-4 text-kali-cyan" />
            <h3 className="text-sm font-bold text-white">Kali Shell & Safety Safeguards</h3>
          </div>

          <div className="space-y-3">
            <div>
              <label className="block text-xs font-medium text-slate-300 mb-1">
                Login Shell Executable
              </label>
              <input
                type="text"
                value={settings.shell_path}
                onChange={(e) => setSettings({ ...settings, shell_path: e.target.value })}
                className="w-full px-3 py-2 rounded-lg bg-slate-900 border border-slate-700 text-xs text-white font-mono focus:outline-none focus:border-kali-cyan"
              />
              <p className="text-[11px] text-slate-500 mt-1">Full path to interactive shell (typically /bin/bash on Kali Linux).</p>
            </div>

            <div className="pt-2 space-y-2">
              <label className="flex items-center space-x-2.5 cursor-pointer">
                <input
                  type="checkbox"
                  checked={settings.safe_mode}
                  onChange={(e) => setSettings({ ...settings, safe_mode: e.target.checked })}
                  className="rounded bg-slate-900 border-slate-700 text-kali-cyan focus:ring-0"
                />
                <span className="text-xs text-slate-200">
                  Enable Strict Lab Safeguards (blocks destructive commands like disk wipes or fork bombs)
                </span>
              </label>

              <label className="flex items-center space-x-2.5 cursor-pointer">
                <input
                  type="checkbox"
                  checked={settings.auto_verify}
                  onChange={(e) => setSettings({ ...settings, auto_verify: e.target.checked })}
                  className="rounded bg-slate-900 border-slate-700 text-kali-cyan focus:ring-0"
                />
                <span className="text-xs text-slate-200">
                  Automatically run post-execution verification checks
                </span>
              </label>
            </div>
          </div>
        </div>

        {/* Save Button */}
        <div className="flex items-center space-x-4">
          <button
            type="submit"
            disabled={saving}
            className="flex items-center space-x-2 px-6 py-2.5 rounded-lg bg-kali-cyan text-black font-bold text-xs hover:bg-kali-cyanHover transition shadow-lg shadow-kali-cyan/20"
          >
            <Save className="w-4 h-4 fill-black" />
            <span>{saving ? 'Saving...' : 'Save Configuration'}</span>
          </button>

          {savedSuccess && (
            <div className="flex items-center space-x-1.5 text-xs text-kali-green font-mono">
              <Check className="w-4 h-4" />
              <span>Settings updated successfully!</span>
            </div>
          )}
        </div>

      </form>

    </div>
  );
};
