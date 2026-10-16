import React, {useCallback, useEffect, useState} from 'react';
import {Icon} from '../icons.jsx';
import {policyDocument} from '../shared/api/policies.ts';

function EmptyState({icon = 'document', title, children}) {
  return <div className="empty-state"><span className="empty-icon"><Icon name={icon} size={22}/></span><strong>{title}</strong><p>{children}</p></div>;
}

function Pill({status}) {
  const normalized = String(status || '').toLowerCase();
  const positive = normalized.includes('allow') || normalized.includes('true');
  const negative = normalized.includes('deny') || normalized.includes('false');
  return <span className={`status-pill ${positive ? 'positive' : negative ? 'negative' : 'neutral'}`}><span className="status-dot"/>{String(status ?? 'UNKNOWN')}</span>;
}

function decisionStatus(decision) {
  if (decision.decision) return decision.decision;
  if (decision.effect) return decision.effect;
  if (decision.allowed === true || decision.allow === true) return 'ALLOW';
  if (decision.allowed === false || decision.allow === false) return 'DENY';
  return 'UNKNOWN';
}

export default function RbacPolicyEditor({api, run, busy}) {
  const [policies, setPolicies] = useState(null);
  const [yaml, setYaml] = useState('');
  const [originalYaml, setOriginalYaml] = useState('');
  const [decisions, setDecisions] = useState(null);
  const [unavailable, setUnavailable] = useState(false);
  const [error, setError] = useState('');
  const [saving, setSaving] = useState(false);
  const [saveResult, setSaveResult] = useState(null);

  const load = useCallback(async () => {
    setError('');
    try {
      const [policyData, decisionData] = await Promise.all([
        api('/api/v1/authz/policies'),
        api('/api/v1/authz/decisions').catch(() => null),
      ]);
      const statements = policyData?.policies || [];
      setPolicies(statements);
      const rendered = policyDocument(statements);
      setYaml(rendered);
      setOriginalYaml(rendered);
      setSaveResult(null);
      setDecisions(decisionData ? (decisionData.decisions || []) : []);
      setUnavailable(false);
    } catch (exception) {
      if (exception.message && exception.message.includes('404')) {
        setUnavailable(true);
        setPolicies([]);
      } else {
        setError(exception.message || 'Policies could not be loaded.');
      }
    }
  }, [api]);

  useEffect(() => {load();}, [load]);


  async function save() {
    setSaving(true);
    setError('');
    setSaveResult(null);
    try {
      const result = await api('/api/v1/authz/policies/reload?replace_existing=true', yaml, 'POST', {contentType: 'application/yaml'});
      setOriginalYaml(yaml);
      await load();
      setSaveResult({ok: true, loaded: result.loaded ?? null});
    } catch (exception) {
      setSaveResult({ok: false});
      setError(exception.message || 'The policy reload failed.');
    } finally {
      setSaving(false);
    }
  }

  const dirty = yaml !== originalYaml;

  if (unavailable) {
    return <section className="panel span-3"><div className="panel-heading"><div><span className="eyebrow">POLICY AS CODE</span><h2>RBAC policy editor</h2><p>Edit the loaded authorization policy set as YAML and validate it on save.</p></div></div>
      <EmptyState icon="shield" title="The authz API is not available in this deployment">The <code>/api/v1/authz/policies</code> endpoints returned 404. Enable the pass-2 authorization service to edit policies from this panel.</EmptyState></section>;
  }

  return <>
    <section className="panel span-2"><div className="panel-heading"><div><span className="eyebrow">POLICY AS CODE</span><h2>RBAC policy editor</h2><p>Edit the loaded authorization policy set as YAML. Saving reloads and validates it through <code>/api/v1/authz/policies/reload</code>.</p></div><div className="panel-tools"><button className="secondary-button" onClick={() => run(load)} disabled={busy || saving}><Icon name="refresh" size={15}/>Reload</button>{dirty && <span className="count-badge">Unsaved changes</span>}</div></div>
      {error && <div className="inline-notice warning" role="alert"><Icon name="warning"/>{error}</div>}
      {saveResult?.ok && <div className="inline-notice" role="status"><Icon name="check"/>Policy set reloaded{saveResult.loaded != null ? ` — ${saveResult.loaded} statement(s) loaded` : ''}.</div>}
      {policies === null && <div className="inline-notice" role="status"><span className="spinner"/>Loading policies…</div>}
      {policies !== null && <>
        <label htmlFor="policy-yaml" className="eyebrow">POLICY YAML · {policies.length} statement(s) loaded</label>
        <textarea id="policy-yaml" value={yaml} onChange={event => {setYaml(event.target.value); setSaveResult(null);}} spellCheck="false"
          style={{width: '100%', minHeight: 320, fontFamily: 'ui-monospace, SFMono-Regular, Consolas, monospace', fontSize: 12.5, lineHeight: 1.55, background: 'rgba(148, 163, 184, 0.06)', border: '1px solid rgba(148, 163, 184, 0.25)', borderRadius: 10, padding: '10px 12px', color: 'inherit', resize: 'vertical'}}/>
        <div className="pipeline-actions" style={{marginTop: 10}}>
          <button className="primary-button" onClick={save} disabled={saving || busy || !dirty}>{saving ? <><span className="spinner small"/>Validating…</> : <><Icon name="check" size={16}/>Save & reload policies</>}</button>
          <button className="secondary-button" onClick={() => {setYaml(originalYaml); setSaveResult(null); setError('');}} disabled={saving || !dirty}>Discard changes</button>
        </div></>}
    </section>
    <section className="panel"><div className="panel-heading"><div><span className="eyebrow">ENFORCEMENT TRAIL</span><h2>Authorization decisions</h2><p>Read-only audit of recent allow / deny decisions returned by the authz service.</p></div><span className="count-badge">{decisions ? decisions.length : 0} entries</span></div>
      {decisions === null && <div className="inline-notice" role="status"><span className="spinner"/>Loading decisions…</div>}
      {decisions !== null && !decisions.length && <EmptyState icon="check" title="No decisions recorded">Authorization decisions appear here once the policy enforcer evaluates requests.</EmptyState>}
      {decisions !== null && decisions.length > 0 && <div className="table-wrap"><table><thead><tr><th>Time</th><th>User</th><th>Action</th><th>Decision</th></tr></thead><tbody>{decisions.slice(-25).reverse().map((decision, index) => {
        const time = decision.timestamp || decision.ts;
        return <tr key={decision.decision_id || index}><td>{time ? new Date(time).toLocaleString() : '—'}</td><td><strong>{decision.user_id ?? decision.subject ?? '—'}</strong></td><td>{decision.action ?? '—'}</td><td><Pill status={decisionStatus(decision)}/></td></tr>;
      })}</tbody></table></div>}</section>
  </>;
}
