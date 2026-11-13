import React, { useState, useEffect } from 'react';
import { Sidebar } from './components/Sidebar';
import { Navbar } from './components/Navbar';
import { Dashboard } from './pages/Dashboard';
import { PracticalsList } from './pages/PracticalsList';
import { History } from './pages/History';
import { Settings } from './pages/Settings';
import { About } from './pages/About';
import { PracticalDetailModal } from './components/PracticalDetailModal';
import { LabRecordModal } from './components/LabRecordModal';
import { Practical, SystemStatus, HistoryRecord } from './types';
import { fetchSystemStatus, fetchAllPracticals, fetchHistory, startExecution } from './services/api';
import { wsClient } from './services/websocket';

export const App: React.FC = () => {
  const [currentTab, setCurrentTab] = useState<string>('dashboard');
  const [systemStatus, setSystemStatus] = useState<SystemStatus | null>(null);
  const [practicals, setPracticals] = useState<Practical[]>([]);
  const [history, setHistory] = useState<HistoryRecord[]>([]);

  // Modals
  const [selectedPractical, setSelectedPractical] = useState<Practical | null>(null);
  const [isDetailModalOpen, setIsDetailModalOpen] = useState<boolean>(false);
  const [selectedRecord, setSelectedRecord] = useState<HistoryRecord | null>(null);
  const [isRecordModalOpen, setIsRecordModalOpen] = useState<boolean>(false);

  // Execution tracking
  const [isExecuting, setIsExecuting] = useState<boolean>(false);
  const [currentStep, setCurrentStep] = useState<{ step_number: number; total_steps: number; command: string } | undefined>(undefined);
  const [terminalConnected, setTerminalConnected] = useState<boolean>(false);

  // Initial data loading
  useEffect(() => {
    loadData();
    const interval = setInterval(refreshStatus, 8000);
    return () => clearInterval(interval);
  }, []);

  const loadData = async () => {
    try {
      const [status, prs, hist] = await Promise.all([
        fetchSystemStatus(),
        fetchAllPracticals(),
        fetchHistory()
      ]);
      setSystemStatus(status);
      setPracticals(prs);
      setHistory(hist);
      setIsExecuting(status.is_executing);
    } catch (e) {
      console.warn('Initial load exception:', e);
    }
  };

  const refreshStatus = async () => {
    try {
      const status = await fetchSystemStatus();
      setSystemStatus(status);
      setIsExecuting(status.is_executing);
    } catch (e) {}
  };

  // Subscribe to live agent WebSocket events
  useEffect(() => {
    const unsubscribe = wsClient.subscribe((msg) => {
      if (msg.type === 'connection_status') {
        setTerminalConnected(msg.connected);
      } else if (msg.type === 'execution_started') {
        setIsExecuting(true);
      } else if (msg.type === 'step_start') {
        setCurrentStep({
          step_number: msg.step_number,
          total_steps: msg.total_steps,
          command: msg.command
        });
      } else if (msg.type === 'execution_completed') {
        setIsExecuting(false);
        setCurrentStep(undefined);
        // Refresh history
        fetchHistory().then((h) => {
          setHistory(h);
          if (msg.record) {
            setSelectedRecord(msg.record);
            setIsRecordModalOpen(true);
          }
        });
        refreshStatus();
      }
    });

    return () => unsubscribe();
  }, []);

  // Handlers
  const handleSelectPractical = (p: Practical) => {
    setSelectedPractical(p);
    setIsDetailModalOpen(true);
  };

  const handleQuickRun = async (p: Practical) => {
    // If practical requires custom inputs or is sensitive, open modal
    if (p.is_destructive || p.required_inputs.length > 2) {
      handleSelectPractical(p);
      return;
    }

    try {
      const defaultVals: Record<string, any> = {};
      p.required_inputs.forEach((inp) => {
        defaultVals[inp.key] = inp.default;
      });
      await startExecution(p.id, defaultVals);
      setIsExecuting(true);
      // Switch to dashboard so terminal is immediately in view!
      setCurrentTab('dashboard');
    } catch (err: any) {
      alert(`Error starting practical: ${err.message}`);
    }
  };

  const handleViewRecord = (rec: HistoryRecord) => {
    setSelectedRecord(rec);
    setIsRecordModalOpen(true);
  };

  return (
    <div className="flex h-screen bg-kali-bg text-slate-100 overflow-hidden font-sans">
      {/* Sidebar */}
      <Sidebar
        currentTab={currentTab}
        setCurrentTab={setCurrentTab}
        systemStatus={systemStatus}
      />

      {/* Main Content Area */}
      <div className="flex-1 flex flex-col h-screen overflow-hidden">
        {/* Navbar */}
        <Navbar
          currentTab={currentTab}
          systemStatus={systemStatus}
          terminalConnected={terminalConnected}
          onOpenQuickLaunch={() => setCurrentTab('practicals')}
        />

        {/* View Switcher */}
        {currentTab === 'dashboard' && (
          <Dashboard
            systemStatus={systemStatus}
            practicals={practicals}
            history={history}
            onSelectPractical={handleSelectPractical}
            onQuickRun={handleQuickRun}
            onViewRecord={handleViewRecord}
            onNavigateToPracticals={() => setCurrentTab('practicals')}
          />
        )}

        {currentTab === 'practicals' && (
          <PracticalsList
            practicals={practicals}
            onSelectPractical={handleSelectPractical}
            onQuickRun={handleQuickRun}
            isExecuting={isExecuting}
          />
        )}

        {currentTab === 'history' && (
          <History
            history={history}
            onViewRecord={handleViewRecord}
          />
        )}

        {currentTab === 'settings' && <Settings />}

        {currentTab === 'about' && <About />}
      </div>

      {/* Practical Detail & Execution Modal */}
      <PracticalDetailModal
        practical={selectedPractical}
        isOpen={isDetailModalOpen}
        onClose={() => setIsDetailModalOpen(false)}
        isExecuting={isExecuting}
        currentStep={currentStep}
        onExecutionStarted={() => {
          setIsDetailModalOpen(false);
          setCurrentTab('dashboard');
        }}
      />

      {/* Lab Record / Report Modal */}
      <LabRecordModal
        record={selectedRecord}
        isOpen={isRecordModalOpen}
        onClose={() => setIsRecordModalOpen(false)}
      />
    </div>
  );
};

export default App;
