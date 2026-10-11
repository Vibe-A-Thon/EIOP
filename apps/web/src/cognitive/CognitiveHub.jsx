import React, { useState } from 'react';
import { Icon, Tip } from '../icons.jsx';
import DisciplineMatrix from './DisciplineMatrix.jsx';
import ReflectionSandboxStudio from './ReflectionSandboxStudio.jsx';
import ContextSlicingStudio from './ContextSlicingStudio.jsx';
import SentinelDistillationStudio from './SentinelDistillationStudio.jsx';
import McpAttestationStudio from './McpAttestationStudio.jsx';
import TokenEconomicsStudio from './TokenEconomicsStudio.jsx';
import './cognitive.css';

const tabs = [
  { id: 'matrix', label: '15 Engineering Disciplines', icon: 'cpu', hint: 'Inspect and execute the 15 core engineering disciplines' },
  { id: 'sandbox', label: 'Reflection Sandbox & Inoculator', icon: 'lock', hint: 'Bounded invariance sandbox and active adversarial prompt shields' },
  { id: 'context', label: 'Attention Slicer & Bitemporal', icon: 'layers', hint: 'Attention-weighted graph pruning and side-by-side temporal state diffs' },
  { id: 'sentinel', label: 'Graph Repair & Distillation', icon: 'radar', hint: 'Self-healing graph topology sentinel and few-shot prompt distiller' },
  { id: 'mcp', label: 'External MCP & Attestation', icon: 'key', hint: 'Connect external MCP servers and verify HMAC-SHA256 tool signatures' },
  { id: 'economics', label: 'Token Economics & Latency', icon: 'chart', hint: 'Model multi-model compute spend, latency, and cache efficiency' },
];

export default function CognitiveHub({ api, run, busy, stats }) {
  const [activeTab, setActiveTab] = useState('matrix');

  return (
    <div className="cognitive-hub">
      {/* Hero Header */}
      <div className="cognitive-hero">
        <div className="cognitive-hero-title">
          <span className="cognitive-hero-badge">
            <Icon name="spark" size={14} />
            <span>COGNITIVE INTELLIGENCE & ENGINEERING PLATFORM</span>
          </span>
          <h2>
            <span>Autonomous Intelligence & Multi-Paradigm Engine</span>
          </h2>
          <p>
            Enterprise command center unifying all 15 core disciplines with advanced cognitive capabilities: bounded reflection sandboxes, dynamic jailbreak inoculation, attention-weighted graph slicing, self-healing topology repair, and cryptographically attested MCP tool execution.
          </p>
        </div>

        <div className="cognitive-hero-actions">
          <div className="telemetry-metric" style={{ background: '#ffffff', minWidth: '150px' }}>
            <small>DISCIPLINES COMPLETE</small>
            <strong style={{ color: '#10a981' }}>15 / 15 (100%)</strong>
          </div>
          <div className="telemetry-metric" style={{ background: '#ffffff', minWidth: '150px' }}>
            <small>SECURITY GATES</small>
            <strong style={{ color: '#7054e8' }}>ACTIVE & BOUNDED</strong>
          </div>
        </div>
      </div>

      {/* Tabs Navigation */}
      <nav className="cognitive-nav" aria-label="Cognitive modules navigation">
        {tabs.map((tab) => (
          <Tip text={tab.hint} key={tab.id}>
            <button
              className={`cognitive-nav-btn ${activeTab === tab.id ? 'active' : ''}`}
              onClick={() => setActiveTab(tab.id)}
            >
              <Icon name={tab.icon} size={16} />
              <span>{tab.label}</span>
            </button>
          </Tip>
        ))}
      </nav>

      {/* Dynamic Tab Body */}
      <main>
        {activeTab === 'matrix' && <DisciplineMatrix api={api} run={run} busy={busy} />}
        {activeTab === 'sandbox' && <ReflectionSandboxStudio api={api} run={run} busy={busy} />}
        {activeTab === 'context' && <ContextSlicingStudio api={api} run={run} busy={busy} />}
        {activeTab === 'sentinel' && <SentinelDistillationStudio api={api} run={run} busy={busy} />}
        {activeTab === 'mcp' && <McpAttestationStudio api={api} run={run} busy={busy} />}
        {activeTab === 'economics' && <TokenEconomicsStudio />}
      </main>
    </div>
  );
}
