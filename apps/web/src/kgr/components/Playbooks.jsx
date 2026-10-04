import React, {useState} from 'react';
import {Icon} from '../../icons.jsx';

const builtInPlaybooks = [
  {
    id: 'impact-assessment',
    name: 'Impact Assessment',
    description: 'Assess the blast radius and risk of modifying an entity',
    steps: [
      {action: 'select', prompt: 'Select the entity to assess', type: 'user'},
      {action: 'blast-radius', label: 'Compute blast radius (4-hop)', type: 'auto'},
      {action: 'what-if', label: 'Simulate removal', type: 'auto'},
      {action: 'report', label: 'Generate impact report', type: 'auto'},
    ],
  },
  {
    id: 'root-cause',
    name: 'Root Cause Analysis',
    description: 'Trace upstream dependencies to find root causes',
    steps: [
      {action: 'select', prompt: 'Select the affected entity', type: 'user'},
      {action: 'reverse-impact', label: 'Trace upstream (6-hop)', type: 'auto'},
      {action: 'centrality', label: 'Compute betweenness centrality', type: 'auto'},
      {action: 'filter', label: 'Filter to inferred edges', type: 'auto'},
    ],
  },
  {
    id: 'community-health',
    name: 'Community Health Check',
    description: 'Audit a community cluster for orphans, stale entities, and anomalies',
    steps: [
      {action: 'detect-communities', label: 'Detect communities (Leiden)', type: 'auto'},
      {action: 'select-community', prompt: 'Select a community to audit', type: 'user'},
      {action: 'orphaned', label: 'Find orphaned entities', type: 'auto'},
      {action: 'stale', label: 'Find stale entities', type: 'auto'},
      {action: 'anomaly', label: 'Run anomaly detection', type: 'auto'},
    ],
  },
  {
    id: 'dependency-audit',
    name: 'Dependency Audit',
    description: 'Find critical dependencies and single points of failure',
    steps: [
      {action: 'centrality', label: 'Compute betweenness centrality', type: 'auto'},
      {action: 'filter', label: 'Filter to top-10% by centrality', type: 'auto'},
      {action: 'what-if', label: 'Simulate removal of top hub', type: 'auto'},
    ],
  },
];

function loadCustomPlaybooks() {
  try {
    const stored = localStorage.getItem('kgr-custom-playbooks');
    return stored ? JSON.parse(stored) : [];
  } catch { return []; }
}

function saveCustomPlaybooks(playbooks) {
  try { localStorage.setItem('kgr-custom-playbooks', JSON.stringify(playbooks)); } catch {}
}

export default function Playbooks({api, run, busy, selected, onAction, onClose}) {
  const [customPlaybooks] = useState(loadCustomPlaybooks);
  const [activePlaybook, setActivePlaybook] = useState(null);
  const [currentStep, setCurrentStep] = useState(0);
  const allPlaybooks = [...builtInPlaybooks, ...customPlaybooks];

  const startPlaybook = (pb) => {
    setActivePlaybook(pb);
    setCurrentStep(0);
  };

  const advanceStep = () => {
    if (!activePlaybook) return;
    if (currentStep < activePlaybook.steps.length - 1) {
      const step = activePlaybook.steps[currentStep + 1];
      if (step.type === 'auto' && onAction) {
        onAction(step.action, step);
      }
      setCurrentStep(s => s + 1);
    } else {
      setActivePlaybook(null);
      setCurrentStep(0);
    }
  };

  const exportPlaybooks = () => {
    try { navigator.clipboard.writeText(JSON.stringify(allPlaybooks, null, 2)); } catch {}
  };

  if (activePlaybook) {
    return <div className="kgr-playbook-panel">
      <div style={{display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 10}}>
        <h3 style={{margin: 0}}>{activePlaybook.name}</h3>
        <button className="icon-button" onClick={() => { setActivePlaybook(null); setCurrentStep(0); }}><Icon name="close"/></button>
      </div>
      <p style={{fontSize: 12, color: 'var(--muted)', marginBottom: 12}}>{activePlaybook.description}</p>
      <div className="playbook-runner">
        {activePlaybook.steps.map((step, i) => <div key={i} className={`step ${i < currentStep ? 'step-done' : i === currentStep ? 'step-active' : 'step-pending'}`}>
          <span>{i < currentStep ? '✓' : i === currentStep ? '▶' : '○'}</span>
          <span>{step.label || step.prompt || step.action}</span>
        </div>)}
      </div>
      <div style={{marginTop: 12, display: 'flex', gap: 8}}>
        {currentStep < activePlaybook.steps.length - 1
          ? <button className="primary-button" onClick={advanceStep} disabled={busy}>Next Step</button>
          : <button className="primary-button" onClick={advanceStep}>Complete</button>}
        <button className="toolbar-button" onClick={() => { setActivePlaybook(null); setCurrentStep(0); }}>Cancel</button>
      </div>
    </div>;
  }

  return <div className="kgr-playbook-panel">
    <div style={{display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 10}}>
      <h3 style={{margin: 0}}>Investigation Playbooks</h3>
      <div style={{display: 'flex', gap: 4}}>
        <button className="toolbar-button" onClick={exportPlaybooks} title="Export playbooks">Export</button>
        <button className="icon-button" onClick={onClose}><Icon name="close"/></button>
      </div>
    </div>
    <div className="kgr-playbook-list">
      {allPlaybooks.map(pb => <div key={pb.id} className="kgr-playbook-card" onClick={() => startPlaybook(pb)}>
        <h4>{pb.name}</h4>
        <p>{pb.description}</p>
        <small style={{color: 'var(--muted)'}}>{pb.steps.length} steps</small>
      </div>)}
    </div>
  </div>;
}

export {builtInPlaybooks};
