import React, {useCallback, useEffect, useMemo, useState} from 'react';
import {Icon, Tip} from '../icons.jsx';
import {downloadJson, uid} from './studio-utils.js';

const KNOWN_TYPES = [
  'jira','gitlab','github','confluence','servicenow','datadog','grafana',
  'kibana','kubernetes','jenkins','elasticsearch','postgresql','mongodb',
  'redis','kafka','aws','azure','gcp','slack','pagerduty','terraform',
  'vault','snyk','splunk','newrelic','circleci','argocd','sonarqube',
  'artifactory','bitbucket','docker_registry','okta','ldap','custom',
];

const AUTH_TYPES = ['none','api_key','bearer_token','basic_auth','oauth2','certificate','aws_iam','service_account'];
const INGESTION_MODES = ['scheduled','event_driven','manual','streaming'];
const STATUS_COLORS = {
  PENDING: '#6b7280', ONBOARDING: '#f59e0b', CONNECTED: '#3b82f6',
  ACTIVE: '#10b981', PAUSED: '#8b5cf6', ERROR: '#ef4444', DISCONNECTED: '#9ca3af',
};

export default function SystemRegistry({api, run, busy}) {
  const [systems, setSystems] = useState([]);
  const [loading, setLoading] = useState(false);
  const [view, setView] = useState('list'); // list | register | detail | schema
  const [selected, setSelected] = useState(null);
  const [knownTypes, setKnownTypes] = useState(null);
  const [schemaResult, setSchemaResult] = useState(null);

  // Registration form
  const [form, setForm] = useState({
    system_type: 'jira', name: '', base_url: '', api_version: '',
    auth_type: 'api_key', credentials: {}, entity_types: '',
    ingestion_mode: 'scheduled', poll_interval_minutes: 60,
    batch_size: 500, tags: '', auto_onboard: true,
  });

  const [sampleData, setSampleData] = useState('');

  const fetchSystems = useCallback(async () => {
    if (!api) return;
    setLoading(true);
    try {
      const res = await api('/api/v1/systems/');
      setSystems(res?.systems || []);
    } catch { setSystems([]); }
    setLoading(false);
  }, [api]);

  useEffect(() => { fetchSystems(); }, [fetchSystems]);

  useEffect(() => {
    if (!api || knownTypes) return;
    (async () => {
      try {
        const res = await api('/api/v1/systems/known-types');
        if (res?.known_types) setKnownTypes(res.known_types);
      } catch {}
    })();
  }, [api, knownTypes]);

  const handleRegister = async () => {
    const body = {
      ...form,
      entity_types: form.entity_types ? form.entity_types.split(',').map(s => s.trim()) : [],
      tags: form.tags ? form.tags.split(',').map(s => s.trim()) : [],
    };
    try {
      const res = await api('/api/v1/systems/register', body, 'POST');
      await fetchSystems();
      setSelected(res);
      setView('detail');
    } catch (e) {
      alert('Registration failed: ' + (e.message || e));
    }
  };

  const handleTestConnection = async (systemId) => {
    try {
      const res = await api(`/api/v1/systems/${systemId}/test-connection`, {}, 'POST');
      alert(res?.connected ? 'Connection successful' : 'Connection failed');
    } catch (e) {
      alert('Connection test error: ' + (e.message || e));
    }
  };

  const handleOnboard = async (systemId) => {
    let data = null;
    if (sampleData.trim()) {
      try { data = JSON.parse(sampleData); } catch { alert('Invalid JSON sample data'); return; }
    }
    try {
      const res = await api(`/api/v1/systems/${systemId}/onboard`, {sample_data: data}, 'POST');
      setSelected(res);
      setView('detail');
      await fetchSystems();
    } catch (e) {
      alert('Onboarding failed: ' + (e.message || e));
    }
  };

  const handleGenerateSchema = async (systemId) => {
    let data;
    try { data = JSON.parse(sampleData); } catch { alert('Paste valid JSON sample data first'); return; }
    try {
      const res = await api(`/api/v1/systems/${systemId}/generate-schema`, {sample_data: data}, 'POST');
      setSchemaResult(res);
      setView('schema');
    } catch (e) {
      alert('Schema generation failed: ' + (e.message || e));
    }
  };

  const handleRemove = async (systemId) => {
    if (!confirm('Remove this system from the registry?')) return;
    try {
      await api(`/api/v1/systems/${systemId}`, {}, 'DELETE');
      setView('list');
      await fetchSystems();
    } catch (e) {
      alert('Removal failed: ' + (e.message || e));
    }
  };

  // ── List View ─────────────────────────────────────────
  if (view === 'list') return (
    <div className="sr-panel">
      <div className="sr-header">
        <h3><Icon name="server" size={18}/> Connected Systems</h3>
        <div className="sr-actions">
          <button onClick={fetchSystems} disabled={loading}>
            <Icon name="refresh-cw" size={14}/> Refresh
          </button>
          <button className="primary" onClick={() => { setForm({...form}); setView('register'); }}>
            <Icon name="plus" size={14}/> Register System
          </button>
        </div>
      </div>
      {loading && <p className="sr-loading">Loading systems…</p>}
      {!loading && systems.length === 0 && <p className="sr-empty">No systems connected yet. Click "Register System" to begin.</p>}
      <div className="sr-grid">
        {systems.map(s => (
          <div key={s.system_id} className="sr-card" onClick={() => { setSelected(s); setView('detail'); }}>
            <div className="sr-card-header">
              <span className="sr-type-badge">{s.system_type}</span>
              <span className="sr-status" style={{background: STATUS_COLORS[s.status] || '#6b7280'}}>{s.status}</span>
            </div>
            <div className="sr-card-name">{s.name}</div>
            <div className="sr-card-category">{s.category}</div>
            {s.tags?.length > 0 && <div className="sr-tags">{s.tags.map(t => <span key={t} className="sr-tag">{t}</span>)}</div>}
          </div>
        ))}
      </div>
    </div>
  );

  // ── Register View ─────────────────────────────────────
  if (view === 'register') return (
    <div className="sr-panel">
      <div className="sr-header">
        <h3><Icon name="plus-circle" size={18}/> Register New System</h3>
        <button onClick={() => setView('list')}><Icon name="arrow-left" size={14}/> Back</button>
      </div>
      <div className="sr-form">
        <div className="sr-field">
          <label>System Type</label>
          <select value={form.system_type} onChange={e => setForm({...form, system_type: e.target.value})}>
            {KNOWN_TYPES.map(t => <option key={t} value={t}>{t}</option>)}
          </select>
        </div>
        <div className="sr-field">
          <label>Display Name</label>
          <input value={form.name} onChange={e => setForm({...form, name: e.target.value})} placeholder="e.g. Production Jira"/>
        </div>
        <div className="sr-field">
          <label>Base URL</label>
          <input value={form.base_url} onChange={e => setForm({...form, base_url: e.target.value})} placeholder="https://your-instance.example.com"/>
        </div>
        <div className="sr-field">
          <label>API Version</label>
          <input value={form.api_version} onChange={e => setForm({...form, api_version: e.target.value})} placeholder="v2"/>
        </div>
        <div className="sr-row">
          <div className="sr-field">
            <label>Auth Type</label>
            <select value={form.auth_type} onChange={e => setForm({...form, auth_type: e.target.value})}>
              {AUTH_TYPES.map(t => <option key={t} value={t}>{t}</option>)}
            </select>
          </div>
          <div className="sr-field">
            <label>Ingestion Mode</label>
            <select value={form.ingestion_mode} onChange={e => setForm({...form, ingestion_mode: e.target.value})}>
              {INGESTION_MODES.map(m => <option key={m} value={m}>{m}</option>)}
            </select>
          </div>
        </div>
        <div className="sr-row">
          <div className="sr-field">
            <label>Poll Interval (min)</label>
            <input type="number" value={form.poll_interval_minutes} onChange={e => setForm({...form, poll_interval_minutes: +e.target.value})}/>
          </div>
          <div className="sr-field">
            <label>Batch Size</label>
            <input type="number" value={form.batch_size} onChange={e => setForm({...form, batch_size: +e.target.value})}/>
          </div>
        </div>
        <div className="sr-field">
          <label>Entity Types (comma-separated)</label>
          <input value={form.entity_types} onChange={e => setForm({...form, entity_types: e.target.value})} placeholder="issue,project,user"/>
        </div>
        <div className="sr-field">
          <label>Tags (comma-separated)</label>
          <input value={form.tags} onChange={e => setForm({...form, tags: e.target.value})} placeholder="production,team-alpha"/>
        </div>
        <div className="sr-field">
          <label>Sample Data (JSON, optional)</label>
          <textarea rows={6} value={sampleData} onChange={e => setSampleData(e.target.value)} placeholder='[{"id":1,"name":"..."}]'/>
        </div>
        <div className="sr-field-check">
          <label><input type="checkbox" checked={form.auto_onboard} onChange={e => setForm({...form, auto_onboard: e.target.checked})}/> Auto-onboard after registration</label>
        </div>
        <div className="sr-buttons">
          <button onClick={() => setView('list')}>Cancel</button>
          <button className="primary" onClick={handleRegister} disabled={!form.name || !form.base_url}>
            <Icon name="check" size={14}/> Register &amp; Connect
          </button>
        </div>
      </div>
    </div>
  );

  // ── Detail View ───────────────────────────────────────
  if (view === 'detail' && selected) return (
    <div className="sr-panel">
      <div className="sr-header">
        <h3><Icon name="server" size={18}/> {selected.name || selected.system_id}</h3>
        <button onClick={() => setView('list')}><Icon name="arrow-left" size={14}/> Back</button>
      </div>
      <div className="sr-detail">
        <div className="sr-detail-grid">
          <div><strong>System ID</strong><span>{selected.system_id}</span></div>
          <div><strong>Type</strong><span>{selected.system_type}</span></div>
          <div><strong>Status</strong><span className="sr-status" style={{background: STATUS_COLORS[selected.status] || '#6b7280'}}>{selected.status}</span></div>
          <div><strong>Category</strong><span>{selected.category}</span></div>
          {selected.onboarding && <>
            <div><strong>Onboarding</strong><span>{selected.onboarding.success ? 'Completed' : 'Failed'}</span></div>
            <div><strong>Duration</strong><span>{selected.onboarding.total_duration_ms}ms</span></div>
          </>}
        </div>
        {selected.onboarding?.phases && (
          <div className="sr-phases">
            <h4>Onboarding Phases</h4>
            {selected.onboarding.phases.map((p, i) => (
              <div key={i} className={`sr-phase ${p.success ? 'ok' : 'fail'}`}>
                <span className="sr-phase-name">{p.phase}</span>
                <span className="sr-phase-msg">{p.message}</span>
                <span className="sr-phase-time">{p.duration_ms}ms</span>
              </div>
            ))}
          </div>
        )}
        <div className="sr-field">
          <label>Sample Data for Schema / Re-onboard</label>
          <textarea rows={4} value={sampleData} onChange={e => setSampleData(e.target.value)} placeholder="Paste JSON data here"/>
        </div>
        <div className="sr-buttons">
          <button onClick={() => handleTestConnection(selected.system_id)}><Icon name="zap" size={14}/> Test Connection</button>
          <button onClick={() => handleOnboard(selected.system_id)}><Icon name="play" size={14}/> Re-onboard</button>
          <button onClick={() => handleGenerateSchema(selected.system_id)}><Icon name="layers" size={14}/> Generate Schema</button>
          <button className="danger" onClick={() => handleRemove(selected.system_id)}><Icon name="trash-2" size={14}/> Remove</button>
        </div>
      </div>
    </div>
  );

  // ── Schema View ───────────────────────────────────────
  if (view === 'schema' && schemaResult) return (
    <div className="sr-panel">
      <div className="sr-header">
        <h3><Icon name="layers" size={18}/> Generated Schema</h3>
        <div className="sr-actions">
          <button onClick={() => setView('detail')}><Icon name="arrow-left" size={14}/> Back</button>
          <button onClick={() => downloadJson(schemaResult, 'schema.json')}><Icon name="download" size={14}/> Export</button>
        </div>
      </div>
      <div className="sr-schema">
        <div className="sr-schema-stats">
          <div><strong>Entities</strong><span>{schemaResult.entities}</span></div>
          <div><strong>Relationships</strong><span>{schemaResult.relationships}</span></div>
          <div><strong>Validation Rules</strong><span>{schemaResult.validation_rules?.length || 0}</span></div>
          <div><strong>Golden Queries</strong><span>{schemaResult.golden_queries?.length || 0}</span></div>
        </div>
        <details open>
          <summary>GraphQL SDL</summary>
          <pre className="sr-code">{schemaResult.graphql_sdl}</pre>
        </details>
        <details>
          <summary>JSON Schema</summary>
          <pre className="sr-code">{JSON.stringify(schemaResult.json_schema, null, 2)}</pre>
        </details>
        <details>
          <summary>Field Mappings</summary>
          <pre className="sr-code">{JSON.stringify(schemaResult.field_mappings, null, 2)}</pre>
        </details>
        <details>
          <summary>Golden Queries</summary>
          <ul>{(schemaResult.golden_queries || []).map((q, i) => <li key={i}><code>{q}</code></li>)}</ul>
        </details>
        <details>
          <summary>Validation Rules</summary>
          <pre className="sr-code">{JSON.stringify(schemaResult.validation_rules, null, 2)}</pre>
        </details>
      </div>
    </div>
  );

  return <div className="sr-panel"><p>Loading…</p></div>;
}
