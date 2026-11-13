import React, { useState, useEffect } from 'react';
import { 
  X, 
  Play, 
  Square, 
  Sparkles, 
  ShieldAlert, 
  CheckCircle2, 
  Terminal, 
  ListOrdered, 
  Sliders, 
  HelpCircle,
  AlertTriangle,
  RotateCw
} from 'lucide-react';
import { Practical, ExecutionPlan, PlanStep } from '../types';
import { generateExecutionPlan, startExecution, stopExecution } from '../services/api';

interface PracticalDetailModalProps {
  practical: Practical | null;
  isOpen: boolean;
  onClose: () => void;
  isExecuting: boolean;
  currentStep?: { step_number: number; total_steps: number; command: string };
  onExecutionStarted?: () => void;
}

export const PracticalDetailModal: React.FC<PracticalDetailModalProps> = ({
  practical,
  isOpen,
  onClose,
  isExecuting,
  currentStep,
  onExecutionStarted
}) => {
  if (!isOpen || !practical) return null;

  const [activeTab, setActiveTab] = useState<'plan' | 'algorithm' | 'inputs'>('plan');
  const [inputs, setInputs] = useState<Record<string, any>>({});
  const [plan, setPlan] = useState<ExecutionPlan | null>(null);
  const [loadingPlan, setLoadingPlan] = useState(false);
  const [confirmedSafety, setConfirmedSafety] = useState(false);
  const [planError, setPlanError] = useState<string | null>(null);

  // Initialize input defaults
  useEffect(() => {
    const defaultVals: Record<string, any> = {};
    practical.required_inputs.forEach((inp) => {
      defaultVals[inp.key] = inp.default;
    });
    setInputs(defaultVals);
    loadPlan(defaultVals);
  }, [practical]);

  const loadPlan = async (currentInputs: Record<string, any>) => {
    setLoadingPlan(true);
    setPlanError(null);
    try {
      const generated = await generateExecutionPlan(practical.id, currentInputs);
      setPlan(generated);
      // If plan does not require confirmation, default to true
      setConfirmedSafety(!generated.requires_confirmation);
    } catch (err: any) {
      setPlanError(err.message || 'Error generating plan');
    } finally {
      setLoadingPlan(false);
    }
  };

  const handleInputChange = (key: string, val: any) => {
    const updated = { ...inputs, [key]: val };
    setInputs(updated);
  };

  const handleExecute = async () => {
    try {
      await startExecution(practical.id, inputs);
      if (onExecutionStarted) onExecutionStarted();
    } catch (err: any) {
      alert(`Failed to start execution: ${err.message}`);
    }
  };

  const handleStop = async () => {
    await stopExecution();
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/80 backdrop-blur-sm animate-in fade-in duration-150">
      <div className="relative w-full max-w-4xl max-h-[90vh] bg-kali-card border border-kali-border rounded-2xl shadow-2xl flex flex-col overflow-hidden">
        
        {/* Header */}
        <div className="p-6 border-b border-kali-border flex items-start justify-between bg-slate-900/60">
          <div className="flex items-start space-x-4">
            <div className="font-mono text-lg font-bold text-kali-cyan px-3 py-1.5 rounded-lg bg-kali-cyan/10 border border-kali-cyan/30 mt-1">
              #{String(practical.number).padStart(2, '0')}
            </div>
            <div>
              <div className="flex items-center space-x-2 mb-1">
                <span className="text-xs font-mono px-2 py-0.5 rounded bg-slate-800 text-slate-300 border border-slate-700">
                  {practical.category}
                </span>
                {practical.requires_sudo && (
                  <span className="text-xs font-mono px-2 py-0.5 rounded bg-amber-500/10 text-amber-400 border border-amber-500/30">
                    Requires sudo
                  </span>
                )}
                <span className="text-xs text-slate-400">~{practical.estimated_minutes} mins</span>
              </div>
              <h2 className="text-xl font-bold text-white tracking-tight">
                {practical.title}
              </h2>
            </div>
          </div>

          <button
            onClick={onClose}
            className="p-2 rounded-lg text-slate-400 hover:text-white hover:bg-slate-800 transition"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* Tab Navigation */}
        <div className="px-6 border-b border-kali-border bg-slate-950/40 flex items-center space-x-2">
          <button
            onClick={() => setActiveTab('plan')}
            className={`flex items-center space-x-2 py-3 px-4 border-b-2 text-sm font-medium transition ${
              activeTab === 'plan'
                ? 'border-kali-cyan text-kali-cyan'
                : 'border-transparent text-slate-400 hover:text-slate-200'
            }`}
          >
            <Sparkles className="w-4 h-4" />
            <span>AI Execution Plan ({plan?.steps.length || practical.default_commands.length} Steps)</span>
          </button>

          <button
            onClick={() => setActiveTab('inputs')}
            className={`flex items-center space-x-2 py-3 px-4 border-b-2 text-sm font-medium transition ${
              activeTab === 'inputs'
                ? 'border-kali-cyan text-kali-cyan'
                : 'border-transparent text-slate-400 hover:text-slate-200'
            }`}
          >
            <Sliders className="w-4 h-4" />
            <span>Parameters & Inputs ({practical.required_inputs.length})</span>
          </button>

          <button
            onClick={() => setActiveTab('algorithm')}
            className={`flex items-center space-x-2 py-3 px-4 border-b-2 text-sm font-medium transition ${
              activeTab === 'algorithm'
                ? 'border-kali-cyan text-kali-cyan'
                : 'border-transparent text-slate-400 hover:text-slate-200'
            }`}
          >
            <ListOrdered className="w-4 h-4" />
            <span>Objective & Algorithm</span>
          </button>
        </div>

        {/* Modal Body */}
        <div className="flex-1 p-6 overflow-y-auto space-y-6">
          
          {/* TAB 1: AI Execution Plan */}
          {activeTab === 'plan' && (
            <div className="space-y-4">
              {/* Aim Banner */}
              <div className="p-4 rounded-xl bg-slate-900/80 border border-slate-800 text-xs text-slate-300 leading-relaxed">
                <span className="font-semibold text-kali-cyan uppercase tracking-wider block mb-1">Practical Aim:</span>
                {practical.aim}
              </div>

              {/* AI Plan Notes */}
              {plan?.ai_notes && (
                <div className="p-4 rounded-xl bg-kali-cyan/5 border border-kali-cyan/20 flex items-start space-x-3">
                  <Sparkles className="w-4 h-4 text-kali-cyan shrink-0 mt-0.5" />
                  <p className="text-xs text-slate-300 italic">{plan.ai_notes}</p>
                </div>
              )}

              {planError && (
                <div className="p-4 rounded-xl bg-rose-950/40 border border-rose-800 text-xs text-rose-300">
                  <span className="font-semibold block mb-1">Plan Error:</span>
                  {planError}
                </div>
              )}

              {/* Execution Steps */}
              <div className="space-y-2">
                <div className="flex items-center justify-between text-xs text-slate-400 font-semibold uppercase tracking-wider mb-2">
                  <span>Planned Commands to Execute</span>
                  <button
                    onClick={() => loadPlan(inputs)}
                    disabled={loadingPlan}
                    className="flex items-center space-x-1 text-kali-cyan hover:underline text-xs"
                  >
                    <RotateCw className={`w-3 h-3 ${loadingPlan ? 'animate-spin' : ''}`} />
                    <span>Regenerate Plan</span>
                  </button>
                </div>

                {loadingPlan ? (
                  <div className="py-12 text-center text-slate-400 text-sm">
                    Analyzing practical requirements and preparing Kali shell sequence...
                  </div>
                ) : (
                  plan?.steps.map((step) => (
                    <div 
                      key={step.step_number} 
                      className="p-3 rounded-lg bg-slate-900/90 border border-slate-800 hover:border-slate-700 font-mono text-xs flex items-center justify-between space-x-3"
                    >
                      <div className="flex items-center space-x-3 truncate">
                        <span className="text-slate-500 font-bold shrink-0">#{step.step_number}</span>
                        <span className="text-kali-green font-semibold shrink-0">$</span>
                        <span className="text-slate-200 truncate select-all">{step.command}</span>
                      </div>
                      <div className="flex items-center space-x-2 shrink-0">
                        {step.requires_sudo && (
                          <span className="text-[10px] px-1.5 py-0.5 rounded bg-amber-500/10 text-amber-400 border border-amber-500/20">
                            sudo
                          </span>
                        )}
                        <span className={`text-[10px] px-1.5 py-0.5 rounded border ${
                          step.risk_level === 'SAFE' 
                            ? 'bg-slate-800 text-slate-400 border-slate-700' 
                            : 'bg-amber-500/10 text-amber-400 border-amber-500/30'
                        }`}>
                          {step.risk_level}
                        </span>
                      </div>
                    </div>
                  ))
                )}
              </div>

              {/* Safety Confirmation Checkbox if sensitive */}
              {plan?.requires_confirmation && (
                <div className="p-4 rounded-xl bg-amber-500/10 border border-amber-500/30 space-y-2">
                  <div className="flex items-center space-x-2 text-amber-400 font-semibold text-xs">
                    <AlertTriangle className="w-4 h-4" />
                    <span>Safety Confirmation Required</span>
                  </div>
                  <ul className="text-xs text-amber-200/80 list-disc list-inside space-y-1">
                    {plan.confirmation_reasons.map((reason, idx) => (
                      <li key={idx}>{reason}</li>
                    ))}
                  </ul>
                  <label className="flex items-center space-x-2 pt-2 cursor-pointer select-none">
                    <input
                      type="checkbox"
                      checked={confirmedSafety}
                      onChange={(e) => setConfirmedSafety(e.target.checked)}
                      className="rounded bg-slate-900 border-amber-500/50 text-amber-500 focus:ring-0"
                    />
                    <span className="text-xs text-slate-300 font-medium">
                      I authorize execution of these administrative operations in the Kali environment.
                    </span>
                  </label>
                </div>
              )}
            </div>
          )}

          {/* TAB 2: Inputs & Parameters */}
          {activeTab === 'inputs' && (
            <div className="space-y-4">
              <p className="text-xs text-slate-400">
                Customize values used in the practical commands. Sensible lab defaults are pre-filled.
              </p>
              {practical.required_inputs.length === 0 ? (
                <div className="py-8 text-center text-slate-500 text-sm">
                  This practical does not require any additional user inputs. Standard defaults will be executed.
                </div>
              ) : (
                practical.required_inputs.map((inp) => (
                  <div key={inp.key} className="space-y-1.5">
                    <label className="block text-xs font-medium text-slate-200">
                      {inp.label}
                    </label>
                    <input
                      type={inp.type === 'number' ? 'number' : 'text'}
                      value={inputs[inp.key] ?? inp.default}
                      onChange={(e) => handleInputChange(inp.key, inp.type === 'number' ? Number(e.target.value) : e.target.value)}
                      className="w-full px-3 py-2 rounded-lg bg-slate-900 border border-slate-700 text-white font-mono text-xs focus:outline-none focus:border-kali-cyan"
                    />
                    <p className="text-[11px] text-slate-500">{inp.description}</p>
                  </div>
                ))
              )}

              <div className="pt-4 flex justify-end">
                <button
                  onClick={() => {
                    loadPlan(inputs);
                    setActiveTab('plan');
                  }}
                  className="px-4 py-2 rounded-lg bg-slate-800 text-slate-200 hover:bg-slate-700 text-xs font-semibold transition"
                >
                  Apply & Preview Plan &rarr;
                </button>
              </div>
            </div>
          )}

          {/* TAB 3: Objective & Algorithm */}
          {activeTab === 'algorithm' && (
            <div className="space-y-6">
              <div>
                <h4 className="text-xs font-semibold text-kali-cyan uppercase tracking-wider mb-2">
                  Educational Objective
                </h4>
                <p className="text-xs text-slate-300 leading-relaxed p-3.5 rounded-lg bg-slate-900/60 border border-slate-800">
                  {practical.objective}
                </p>
              </div>

              <div>
                <h4 className="text-xs font-semibold text-kali-cyan uppercase tracking-wider mb-2">
                  Algorithmic Execution Sequence
                </h4>
                <ol className="space-y-2">
                  {practical.algorithm.map((step, idx) => (
                    <li key={idx} className="p-3 rounded-lg bg-slate-900/60 border border-slate-800/80 text-xs text-slate-300 flex items-start space-x-3">
                      <span className="w-5 h-5 rounded-full bg-slate-800 text-kali-cyan flex items-center justify-center font-mono text-[10px] shrink-0 mt-0.5">
                        {idx + 1}
                      </span>
                      <span>{step.replace(/^\d+\.\s*/, '')}</span>
                    </li>
                  ))}
                </ol>
              </div>

              <div>
                <h4 className="text-xs font-semibold text-slate-400 uppercase tracking-wider mb-2">
                  Required Kali Utilities
                </h4>
                <div className="flex flex-wrap gap-1.5">
                  {practical.tools_required.map((tool) => (
                    <span key={tool} className="px-2 py-1 rounded bg-slate-900 border border-slate-800 text-[11px] font-mono text-slate-300">
                      {tool}
                    </span>
                  ))}
                </div>
              </div>
            </div>
          )}
        </div>

        {/* Modal Footer */}
        <div className="p-6 border-t border-kali-border bg-slate-950/60 flex items-center justify-between">
          <div className="text-xs text-slate-400 font-mono">
            {isExecuting ? (
              <span className="text-kali-cyan flex items-center space-x-2">
                <span className="w-2 h-2 rounded-full bg-kali-cyan animate-ping inline-block"></span>
                <span>Executing in live Kali terminal...</span>
              </span>
            ) : (
              <span>Ready to launch in Kali shell</span>
            )}
          </div>

          <div className="flex items-center space-x-3">
            <button
              onClick={onClose}
              className="px-4 py-2 rounded-lg bg-slate-900 border border-slate-700 text-slate-300 hover:text-white text-xs font-medium transition"
            >
              Close
            </button>

            {isExecuting ? (
              <button
                onClick={handleStop}
                className="flex items-center space-x-2 px-5 py-2.5 rounded-lg bg-rose-600 text-white font-semibold text-xs hover:bg-rose-500 transition shadow-lg shadow-rose-600/20"
              >
                <Square className="w-3.5 h-3.5 fill-white" />
                <span>Stop Execution</span>
              </button>
            ) : (
              <button
                onClick={handleExecute}
                disabled={!confirmedSafety || loadingPlan}
                className="flex items-center space-x-2 px-6 py-2.5 rounded-lg bg-kali-cyan text-black font-bold text-xs hover:bg-kali-cyanHover disabled:opacity-50 disabled:cursor-not-allowed transition shadow-lg shadow-kali-cyan/25"
              >
                <Play className="w-4 h-4 fill-black" />
                <span>RUN ON KALI LINUX</span>
              </button>
            )}
          </div>
        </div>

      </div>
    </div>
  );
};
