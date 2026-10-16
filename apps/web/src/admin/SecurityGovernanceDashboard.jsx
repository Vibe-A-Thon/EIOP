import React, {useCallback, useEffect, useRef, useState} from 'react';
import {Icon} from '../icons.jsx';

export default function SecurityGovernanceDashboard({api}) {
  const [status, setStatus] = useState(null);
  const [matrix, setMatrix] = useState(null);
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const [pending, setPending] = useState(false);
  const [subject, setSubject] = useState('');
  const [tenant, setTenant] = useState('');
  const [role, setRole] = useState('viewer');
  const [scopes, setScopes] = useState('graph:read');
  const [issued, setIssued] = useState(null);
  const [verifyToken, setVerifyToken] = useState('');
  const [verified, setVerified] = useState(null);
  const [revokeId, setRevokeId] = useState('');
  const [revokeReason, setRevokeReason] = useState('');
  const [revoked, setRevoked] = useState(null);
  const [confirmed, setConfirmed] = useState(false);
  const mutation = useRef(false);
  const alive = useRef(true);
  useEffect(() => {alive.current = true; return () => {alive.current = false;};}, []);

  const load = useCallback(async () => {
    setLoading(true); setError(''); setStatus(null); setMatrix(null);
    try {
      const [posture, policies] = await Promise.all([api('/api/v1/security/status'), api('/api/v1/security/policy-matrix')]);
      if (!posture || typeof posture.enforcement_mode !== 'string' || !policies?.roles_hierarchy) {
        throw new Error('Security status is unavailable: the service returned an unsupported response.');
      }
      if (alive.current) {setStatus(posture); setMatrix(policies);}
    } catch (exception) {
      if (alive.current && exception.name !== 'AbortError') setError(exception.message || 'Security status is unavailable.');
    } finally {if (alive.current) setLoading(false);}
  }, [api]);
  useEffect(() => {load();}, [load]);

  async function submit(event, action) {
    event.preventDefault();
    if (mutation.current) return;
    mutation.current = true; setPending(true); setError('');
    try {await action();}
    catch (exception) {if (alive.current && exception.name !== 'AbortError') setError(exception.message || 'The operation failed.');}
    finally {mutation.current = false; if (alive.current) setPending(false);}
  }

  return <section className="security-workspace" aria-labelledby="security-title">
    <div className="panel-heading"><h2 id="security-title"><Icon name="shield"/> Enterprise Security &amp; Token Governance</h2>
      <button className="secondary-button" onClick={load} disabled={loading || pending}><Icon name="refresh"/>Refresh status</button></div>
    {loading && <p role="status">Loading security status...</p>}
    {error && <p className="resource-error" role="alert">{error}</p>}
    {status && <dl className="security-posture">
      <div><dt>Enforcement posture</dt><dd>{status.enforcement_mode}</dd></div>
      <div><dt>Signing algorithm</dt><dd>{status.algorithm || 'Unknown'}</dd></div>
      <div><dt>Key rotation</dt><dd>{status.key_rotation_supported === true ? 'Supported' : status.key_rotation_supported === false ? 'Not supported' : 'Unknown'}</dd></div>
      <div><dt>Active revocations</dt><dd>{status.active_revocations_count ?? 'Unknown'}</dd></div>
    </dl>}
    <div className="security-forms">
      <form onSubmit={event => submit(event, async () => {
        setIssued(null);
        const result = await api('/api/v1/security/tokens/issue', {subject: subject.trim(), tenant_id: tenant.trim(),
          roles: [role], scopes: scopes.split(',').map(value => value.trim()).filter(Boolean), ttl_seconds: 3600});
        if (!result?.token || !result.jti) throw new Error('The token service did not confirm issuance.');
        if (alive.current) {setIssued(result); setVerifyToken(result.token); setRevokeId(result.jti);}
      })}>
        <h3>Issue scoped token</h3>
        <label>Subject<input required value={subject} onChange={event => setSubject(event.target.value)}/></label>
        <label>Tenant ID<input required value={tenant} onChange={event => setTenant(event.target.value)}/></label>
        <label>Role<select value={role} onChange={event => setRole(event.target.value)}>
          {Object.keys(matrix?.roles_hierarchy || {viewer: {}}).map(name => <option key={name}>{name}</option>)}
        </select></label>
        <label>Scopes<input required value={scopes} onChange={event => setScopes(event.target.value)}/></label>
        <button className="primary-button" disabled={pending || !matrix}><Icon name="key"/>Issue scoped token</button>
        {issued && <><label>Issued token<input type="password" readOnly value={issued.token} autoComplete="off"/></label><output role="status">Issued token: {issued.jti}</output></>}
      </form>
      <div>
        <form onSubmit={event => submit(event, async () => {
          setVerified(null);
          const result = await api('/api/v1/security/tokens/verify', {token: verifyToken, required_scopes: ['graph:read']});
          if (typeof result?.valid !== 'boolean') throw new Error('The token service did not confirm verification.');
          if (alive.current) setVerified(result);
        })}>
          <h3>Verify token</h3>
          <label>Token to verify<input type="password" required autoComplete="off" value={verifyToken} onChange={event => setVerifyToken(event.target.value)}/></label>
          <button className="secondary-button" disabled={pending}><Icon name="shieldCheck"/>Verify token</button>
          {verified && <output role="status">{verified.valid ? 'Valid token' : 'Verification rejected'}</output>}
        </form>
        <form style={{marginTop: 24}} onSubmit={event => submit(event, async () => {
          setRevoked(null);
          const result = await api('/api/v1/security/tokens/revoke', {identifier: revokeId.trim(), reason: revokeReason.trim()});
          if (result?.revoked !== true) throw new Error('The token service did not confirm revocation.');
          if (alive.current) {setRevoked(result); setConfirmed(false); await load();}
        })}>
          <h3>Revoke token</h3>
          <label>Token identifier<input required value={revokeId} onChange={event => {setRevokeId(event.target.value); setConfirmed(false);}}/></label>
          <label>Reason<input required value={revokeReason} onChange={event => setRevokeReason(event.target.value)}/></label>
          <label className="motion-choice"><input type="checkbox" checked={confirmed} onChange={event => setConfirmed(event.target.checked)}/>Confirm revocation</label>
          <button className="secondary-button" disabled={pending || !confirmed}><Icon name="lock"/>Revoke</button>
          {revoked && <output role="status">Revocation recorded. Active revocations: {revoked.active_revocations ?? 'Unknown'}</output>}
        </form>
      </div>
    </div>
    {matrix && <div className="table-wrap" style={{marginTop: 24}}><table><caption>Role hierarchy and inheritance</caption>
      <thead><tr><th>Role</th><th>Rank</th><th>Inherits</th></tr></thead><tbody>
        {Object.entries(matrix.roles_hierarchy).map(([name, definition]) => <tr key={name}><td>{name}</td><td>{definition.rank}</td><td>{definition.inherited_roles?.join(', ') || 'None'}</td></tr>)}
      </tbody></table></div>}
  </section>;
}
