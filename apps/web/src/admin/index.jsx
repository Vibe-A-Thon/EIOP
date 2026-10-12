import React, {useState} from 'react';
import {Icon} from '../icons.jsx';
import AdminDashboard from './AdminDashboard.jsx';
import UserManagement from './UserManagement.jsx';
import RbacPolicyEditor from './RbacPolicyEditor.jsx';
import ConnectorSetupWizard from './ConnectorSetupWizard.jsx';
import IngestionReconciliationPanel from './IngestionReconciliationPanel.jsx';
import CheckpointAndRecoveryPanel from './CheckpointAndRecoveryPanel.jsx';
import SchemaDriftAndFreshnessPanel from './SchemaDriftAndFreshnessPanel.jsx';
import GraphTimelineAndJournalPanel from './GraphTimelineAndJournalPanel.jsx';
import CrawlSafetyAndTelemetryPanel from './CrawlSafetyAndTelemetryPanel.jsx';
import KnowledgeGovernanceAndSLOPanel from './KnowledgeGovernanceAndSLOPanel.jsx';
import SecurityGovernanceDashboard from './SecurityGovernanceDashboard.jsx';

const TABS = [
  {id: 'dashboard', label: 'Live Dashboard', icon: 'activity', hint: 'G2-ADMIN-001 · Real-time metrics, jobs, and health'},
  {id: 'wizard', label: 'Connector Wizard', icon: 'link', hint: 'G2-ADMIN-002, FR-ADMIN-001 · Connector setup & live extraction'},
  {id: 'ingestion', label: 'Ingestion & Reconciliation', icon: 'refresh', hint: 'G2-ADMIN-003, FR-ADMIN-001 · Baseline/reconciliation status'},
  {id: 'checkpoints', label: 'Checkpoints & DLQ', icon: 'shield', hint: 'G2-ADMIN-004, G2-ADMIN-005 · Offset viewer & DLQ replay'},
  {id: 'drift', label: 'Drift & Freshness', icon: 'activity', hint: 'G2-ADMIN-006, G2-ADMIN-007 · Schema drift & lag monitor'},
  {id: 'timeline', label: 'Timeline & Journal', icon: 'clock', hint: 'G2-ADMIN-008, 009, 010 · Graph revisions & Change Journal'},
  {id: 'safety', label: 'Crawl Safety & Telemetry', icon: 'shield', hint: 'G2-ADMIN-011, 012, 013 · Scope safety & OTel extraction'},
  {id: 'governance', label: 'Quality, SLOs & Debt', icon: 'check', hint: 'G2-ADMIN-014..017, FR-ADMIN-002 · Governance, SLOs, debt & workspaces'},
  {id: 'token-gov', label: 'Token Governance & CRL', icon: 'shield', hint: 'GAP-SEC-008..012 · Scoped tokens, key rotation & revocation list'},
  {id: 'users', label: 'Users & Roles', icon: 'users', hint: 'Security · Provision users and manage role bindings'},
  {id: 'policies', label: 'Policies & RBAC', icon: 'document', hint: 'Security · Edit RBAC policy YAML and inspect decisions'},
];

export {
  AdminDashboard,
  UserManagement,
  RbacPolicyEditor,
  ConnectorSetupWizard,
  IngestionReconciliationPanel,
  CheckpointAndRecoveryPanel,
  SchemaDriftAndFreshnessPanel,
  GraphTimelineAndJournalPanel,
  CrawlSafetyAndTelemetryPanel,
  KnowledgeGovernanceAndSLOPanel,
  SecurityGovernanceDashboard,
};

export default function AdminSecurityCenter({api, run, busy}) {
  const [tab, setTab] = useState('dashboard');

  return (
    <div className="admin-security-center" style={{display: 'flex', flexDirection: 'column', gap: '1rem'}}>
      <div className="admin-tabs" role="tablist" aria-label="Security and Operations Administration Panels" style={{display: 'flex', flexWrap: 'wrap', gap: '0.4rem'}}>
        {TABS.map(item => (
          <button
            key={item.id}
            role="tab"
            aria-selected={tab === item.id}
            className={tab === item.id ? 'active' : ''}
            onClick={() => setTab(item.id)}
            title={item.hint}
            style={{display: 'flex', alignItems: 'center', gap: '0.4rem', padding: '0.45rem 0.85rem', fontSize: '0.85rem'}}
          >
            <Icon name={item.icon} size={14} />
            {item.label}
          </button>
        ))}
      </div>

      <div className="admin-content-area" key={tab}>
        {tab === 'dashboard' && <AdminDashboard api={api} run={run} busy={busy} />}
        {tab === 'wizard' && <ConnectorSetupWizard api={api} onComplete={() => setTab('ingestion')} />}
        {tab === 'ingestion' && <IngestionReconciliationPanel api={api} />}
        {tab === 'checkpoints' && <CheckpointAndRecoveryPanel api={api} />}
        {tab === 'drift' && <SchemaDriftAndFreshnessPanel api={api} />}
        {tab === 'timeline' && <GraphTimelineAndJournalPanel api={api} />}
        {tab === 'safety' && <CrawlSafetyAndTelemetryPanel api={api} />}
        {tab === 'governance' && <KnowledgeGovernanceAndSLOPanel api={api} />}
        {tab === 'token-gov' && <SecurityGovernanceDashboard api={api} run={run} busy={busy} />}
        {tab === 'users' && <UserManagement api={api} run={run} busy={busy} />}
        {tab === 'policies' && <RbacPolicyEditor api={api} run={run} busy={busy} />}
      </div>
    </div>
  );
}
