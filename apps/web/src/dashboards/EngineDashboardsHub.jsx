import React, {useState} from 'react';
import {Icon} from '../icons.jsx';
import CausalBlastRadiusDashboard from './CausalBlastRadiusDashboard.jsx';
import MultiParadigmQueryDashboard from './MultiParadigmQueryDashboard.jsx';
import DomainPackDashboard from './DomainPackDashboard.jsx';
import XAIVerificationDashboard from './XAIVerificationDashboard.jsx';
import TimelineLens from './TimelineLens.jsx';
import ChangeLens from './ChangeLens.jsx';
import RuntimeLens from './RuntimeLens.jsx';
import ReleaseLens from './ReleaseLens.jsx';
import ProcessLens from './ProcessLens.jsx';
import SimulationLens from './SimulationLens.jsx';
import SearchAnalyticsDashboard from './SearchAnalyticsDashboard.jsx';

const DASHBOARD_TABS = [
  {id: 'causal', label: 'Causal Blast Radius', icon: 'activity', req: 'UI-01'},
  {id: 'multiparadigm', label: 'Multi-Paradigm Query', icon: 'spark', req: 'UI-02'},
  {id: 'domainpacks', label: 'Domain Packs', icon: 'layers', req: 'UI-03'},
  {id: 'xai', label: 'XAI Verification', icon: 'shield', req: 'UI-04'},
  {id: 'timeline', label: 'Timeline Lens', icon: 'activity', req: 'UI-007'},
  {id: 'change', label: 'Change Lens', icon: 'layers', req: 'UI-007'},
  {id: 'runtime', label: 'Runtime Lens', icon: 'spark', req: 'UI-007'},
  {id: 'release', label: 'Release Lens', icon: 'shield', req: 'UI-007'},
  {id: 'process', label: 'Process Lens', icon: 'activity', req: 'UI-007'},
  {id: 'simulation', label: 'Simulation Lens', icon: 'spark', req: 'UI-007'},
  {id: 'search_analytics', label: 'Search Analytics', icon: 'layers', req: 'UI-008'},
];

export {
  CausalBlastRadiusDashboard,
  MultiParadigmQueryDashboard,
  DomainPackDashboard,
  XAIVerificationDashboard,
  TimelineLens,
  ChangeLens,
  RuntimeLens,
  ReleaseLens,
  ProcessLens,
  SimulationLens,
  SearchAnalyticsDashboard,
};

export default function EngineDashboardsHub({api}) {
  const [activeTab, setActiveTab] = useState('causal');

  return (
    <div className="engine-dashboards-hub" style={{display: 'flex', flexDirection: 'column', height: '100%'}}>
      <div
        className="hub-tab-bar"
        style={{
          display: 'flex',
          gap: '0.5rem',
          padding: '0.75rem 1.5rem',
          background: 'var(--surface-bg, #18181f)',
          borderBottom: '1px solid var(--border-color, #2d2d38)',
          overflowX: 'auto',
        }}
      >
        {DASHBOARD_TABS.map(tab => (
          <button
            key={tab.id}
            onClick={() => setActiveTab(tab.id)}
            style={{
              padding: '0.5rem 1rem',
              borderRadius: '6px',
              border: 'none',
              cursor: 'pointer',
              background: activeTab === tab.id ? 'var(--accent-color, #6366f1)' : '#262630',
              color: '#fff',
              fontWeight: activeTab === tab.id ? 600 : 400,
              display: 'flex',
              alignItems: 'center',
              gap: '0.4rem',
              fontSize: '0.85rem',
              whiteSpace: 'nowrap',
            }}
          >
            <Icon name={tab.icon} size={15} />
            <span>{tab.label}</span>
            <small style={{opacity: 0.7, fontSize: '0.7rem'}}>({tab.req})</small>
          </button>
        ))}
      </div>

      <div className="hub-content" style={{flex: 1, overflowY: 'auto', padding: '16px'}}>
        {activeTab === 'causal' && <CausalBlastRadiusDashboard api={api} />}
        {activeTab === 'multiparadigm' && <MultiParadigmQueryDashboard api={api} />}
        {activeTab === 'domainpacks' && <DomainPackDashboard api={api} />}
        {activeTab === 'xai' && <XAIVerificationDashboard api={api} />}
        {activeTab === 'timeline' && <TimelineLens api={api} />}
        {activeTab === 'change' && <ChangeLens api={api} />}
        {activeTab === 'runtime' && <RuntimeLens api={api} />}
        {activeTab === 'release' && <ReleaseLens api={api} />}
        {activeTab === 'process' && <ProcessLens api={api} />}
        {activeTab === 'simulation' && <SimulationLens api={api} />}
        {activeTab === 'search_analytics' && <SearchAnalyticsDashboard api={api} />}
      </div>
    </div>
  );
}
