import React, {useState} from 'react';
import {Icon} from '../icons.jsx';
import CausalBlastRadiusDashboard from './CausalBlastRadiusDashboard.jsx';
import MultiParadigmQueryDashboard from './MultiParadigmQueryDashboard.jsx';
import DomainPackDashboard from './DomainPackDashboard.jsx';
import XAIVerificationDashboard from './XAIVerificationDashboard.jsx';

const DASHBOARD_TABS = [
  {id: 'causal', label: 'Causal Blast Radius', icon: 'activity', req: 'UI-01'},
  {id: 'multiparadigm', label: 'Multi-Paradigm Query', icon: 'spark', req: 'UI-02'},
  {id: 'domainpacks', label: 'Domain Packs', icon: 'layers', req: 'UI-03'},
  {id: 'xai', label: 'XAI Verification', icon: 'shield', req: 'UI-04'},
];

export {
  CausalBlastRadiusDashboard,
  MultiParadigmQueryDashboard,
  DomainPackDashboard,
  XAIVerificationDashboard,
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
            }}
          >
            <Icon name={tab.icon} size={15} />
            <span>{tab.label}</span>
            <small style={{opacity: 0.7, fontSize: '0.7rem'}}>({tab.req})</small>
          </button>
        ))}
      </div>

      <div className="hub-content" style={{flex: 1, overflowY: 'auto'}}>
        {activeTab === 'causal' && <CausalBlastRadiusDashboard api={api} />}
        {activeTab === 'multiparadigm' && <MultiParadigmQueryDashboard api={api} />}
        {activeTab === 'domainpacks' && <DomainPackDashboard api={api} />}
        {activeTab === 'xai' && <XAIVerificationDashboard api={api} />}
      </div>
    </div>
  );
}
