import React, {useState} from 'react';
import {Icon} from '../icons.jsx';
import AdminDashboard from './AdminDashboard.jsx';
import UserManagement from './UserManagement.jsx';
import RbacPolicyEditor from './RbacPolicyEditor.jsx';

const TABS = [
  {id: 'dashboard', label: 'Live dashboard', icon: 'activity', hint: 'G2-ADMIN-001 · Real-time metrics, jobs, and health'},
  {id: 'users', label: 'Users & roles', icon: 'shield', hint: 'G2-ADMIN-002 · Provision users and manage role bindings'},
  {id: 'policies', label: 'Policies & decisions', icon: 'document', hint: 'G2-ADMIN-003 · Edit RBAC policy YAML and inspect decisions'},
];

export {AdminDashboard, UserManagement, RbacPolicyEditor};

// Composes the three G2-ADMIN panels behind tabs. Integration point: render
// <AdminSecurity api={api} run={run} busy={busy} /> alongside the existing
// Admin view (App.jsx owns wiring).
export default function AdminSecurity({api, run, busy}) {
  const [tab, setTab] = useState('dashboard');
  return <>
    <div className="admin-tabs" role="tablist" aria-label="Security administration panels">{TABS.map(item => <button key={item.id} role="tab" aria-selected={tab === item.id} className={tab === item.id ? 'active' : ''} onClick={() => setTab(item.id)} title={item.hint}><Icon name={item.icon}/>{item.label}</button>)}</div>
    <div className="admin-grid" key={tab}>
      {tab === 'dashboard' && <AdminDashboard api={api} run={run} busy={busy}/>}
      {tab === 'users' && <UserManagement api={api} run={run} busy={busy}/>}
      {tab === 'policies' && <RbacPolicyEditor api={api} run={run} busy={busy}/>}
    </div>
  </>;
}
