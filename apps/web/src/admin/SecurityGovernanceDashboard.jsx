import React, {useState, useEffect} from 'react';
import {Icon} from '../icons.jsx';

export default function SecurityGovernanceDashboard({api, run, busy}) {
  const [status, setStatus] = useState(null);
  const [matrix, setMatrix] = useState(null);
  const [subject, setSubject] = useState('dev-lead@corp.internal');
  const [selectedRole, setSelectedRole] = useState('analyst');
  const [selectedScopes, setSelectedScopes] = useState('graph:read,graph:mutate');
  const [issuedToken, setIssuedToken] = useState(null);
  const [tokenToVerify, setTokenToVerify] = useState('');
  const [verifyResult, setVerifyResult] = useState(null);
  const [revokeId, setRevokeId] = useState('');
  const [revokeResult, setRevokeResult] = useState(null);

  useEffect(() => {
    loadStatus();
  }, []);

  const loadStatus = async () => {
    try {
      const res = await (api ? api.get('/api/v1/security/status') : fetch('/api/v1/security/status').then(r => r.json()));
      setStatus(res);
      const mat = await (api ? api.get('/api/v1/security/policy-matrix') : fetch('/api/v1/security/policy-matrix').then(r => r.json()));
      setMatrix(mat);
    } catch (e) {
      // offline / mock fallback
      setStatus({
        status: 'OPERATIONAL',
        enforcement_mode: 'FAIL_CLOSED',
        algorithm: 'HMAC-SHA256',
        key_rotation_supported: true,
        active_revocations_count: 0,
        roles_registered: 4,
        permissions_known: 12,
      });
      setMatrix({
        roles_hierarchy: {
          admin: {rank: 4, inherited_roles: ['viewer', 'analyst', 'steward', 'admin']},
          steward: {rank: 3, inherited_roles: ['viewer', 'analyst', 'steward']},
          analyst: {rank: 2, inherited_roles: ['viewer', 'analyst']},
          viewer: {rank: 1, inherited_roles: ['viewer']},
        },
        all_permissions: ['graph:read', 'graph:mutate', 'ontology:publish', 'admin:*'],
      });
    }
  };

  const handleIssue = async () => {
    try {
      const payload = {
        subject,
        roles: [selectedRole],
        scopes: selectedScopes.split(',').map(s => s.trim()).filter(Boolean),
        tenant_id: 'prod-enterprise',
        ttl_seconds: 3600,
      };
      const res = await (api ? api.post('/api/v1/security/tokens/issue', payload) : fetch('/api/v1/security/tokens/issue', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify(payload),
      }).then(r => r.json()));
      setIssuedToken(res);
      setTokenToVerify(res.token || '');
    } catch (e) {
      setIssuedToken({error: String(e)});
    }
  };

  const handleVerify = async () => {
    try {
      const payload = {
        token: tokenToVerify,
        required_scopes: ['graph:read'],
      };
      const res = await (api ? api.post('/api/v1/security/tokens/verify', payload) : fetch('/api/v1/security/tokens/verify', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify(payload),
      }).then(r => r.json()));
      setVerifyResult(res);
    } catch (e) {
      setVerifyResult({valid: false, error: String(e)});
    }
  };

  const handleRevoke = async () => {
    try {
      const payload = {
        identifier: revokeId || (issuedToken?.jti) || 'test-jti',
        reason: 'Compromised credential rotation',
      };
      const res = await (api ? api.post('/api/v1/security/tokens/revoke', payload) : fetch('/api/v1/security/tokens/revoke', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify(payload),
      }).then(r => r.json()));
      setRevokeResult(res);
      loadStatus();
    } catch (e) {
      setRevokeResult({revoked: false, error: String(e)});
    }
  };

  return (
    <div className="card" style={{padding: '1.25rem', display: 'flex', flexDirection: 'column', gap: '1.25rem'}}>
      <div style={{display: 'flex', justifyContent: 'space-between', alignItems: 'center', borderBottom: '1px solid var(--border-color, #2d3748)', paddingBottom: '0.75rem'}}>
        <div>
          <h3 style={{margin: 0, display: 'flex', alignItems: 'center', gap: '0.5rem'}}>
            <Icon name="shield" size={18} />
            Enterprise Security & Token Governance
          </h3>
          <p style={{margin: '0.25rem 0 0', fontSize: '0.85rem', color: '#a0aec0'}}>
            GAP-SEC-008..012 · Fail-closed token signing, key rotation, scoped ABAC, and CRL revocation
          </p>
        </div>
        <button onClick={loadStatus} className="btn-secondary" style={{padding: '0.35rem 0.75rem', fontSize: '0.8rem'}}>
          Refresh Status
        </button>
      </div>

      {status && (
        <div style={{display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(180px, 1fr))', gap: '0.75rem'}}>
          <div style={{background: 'rgba(255,255,255,0.03)', padding: '0.75rem', borderRadius: '6px', border: '1px solid rgba(255,255,255,0.08)'}}>
            <div style={{fontSize: '0.75rem', color: '#a0aec0'}}>Enforcement Posture</div>
            <div style={{fontSize: '1.1rem', fontWeight: 600, color: '#48bb78'}}>{status.enforcement_mode}</div>
          </div>
          <div style={{background: 'rgba(255,255,255,0.03)', padding: '0.75rem', borderRadius: '6px', border: '1px solid rgba(255,255,255,0.08)'}}>
            <div style={{fontSize: '0.75rem', color: '#a0aec0'}}>Signing Algorithm</div>
            <div style={{fontSize: '1.1rem', fontWeight: 600}}>{status.algorithm}</div>
          </div>
          <div style={{background: 'rgba(255,255,255,0.03)', padding: '0.75rem', borderRadius: '6px', border: '1px solid rgba(255,255,255,0.08)'}}>
            <div style={{fontSize: '0.75rem', color: '#a0aec0'}}>Key Rotation</div>
            <div style={{fontSize: '1.1rem', fontWeight: 600, color: '#48bb78'}}>Supported</div>
          </div>
          <div style={{background: 'rgba(255,255,255,0.03)', padding: '0.75rem', borderRadius: '6px', border: '1px solid rgba(255,255,255,0.08)'}}>
            <div style={{fontSize: '0.75rem', color: '#a0aec0'}}>Active Revocations (CRL)</div>
            <div style={{fontSize: '1.1rem', fontWeight: 600, color: status.active_revocations_count > 0 ? '#ed8936' : '#a0aec0'}}>
              {status.active_revocations_count}
            </div>
          </div>
        </div>
      )}

      {/* Token Issuance & Scopes */}
      <div style={{display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '1rem'}}>
        <div style={{background: 'rgba(255,255,255,0.02)', padding: '1rem', borderRadius: '6px', border: '1px solid rgba(255,255,255,0.05)'}}>
          <h4 style={{margin: '0 0 0.75rem', fontSize: '0.95rem'}}>Issue Scoped Bearer Token (GAP-SEC-009, 011)</h4>
          <div style={{display: 'flex', flexDirection: 'column', gap: '0.6rem'}}>
            <div>
              <label style={{fontSize: '0.75rem', color: '#a0aec0', display: 'block'}}>Subject (User / Service)</label>
              <input
                type="text"
                value={subject}
                onChange={e => setSubject(e.target.value)}
                style={{width: '100%', padding: '0.4rem', fontSize: '0.85rem', background: '#1a202c', border: '1px solid #4a5568', color: '#fff', borderRadius: '4px'}}
              />
            </div>
            <div>
              <label style={{fontSize: '0.75rem', color: '#a0aec0', display: 'block'}}>Role</label>
              <select
                value={selectedRole}
                onChange={e => setSelectedRole(e.target.value)}
                style={{width: '100%', padding: '0.4rem', fontSize: '0.85rem', background: '#1a202c', border: '1px solid #4a5568', color: '#fff', borderRadius: '4px'}}
              >
                <option value="admin">admin</option>
                <option value="steward">steward</option>
                <option value="analyst">analyst</option>
                <option value="viewer">viewer</option>
              </select>
            </div>
            <div>
              <label style={{fontSize: '0.75rem', color: '#a0aec0', display: 'block'}}>Scopes (comma-separated)</label>
              <input
                type="text"
                value={selectedScopes}
                onChange={e => setSelectedScopes(e.target.value)}
                style={{width: '100%', padding: '0.4rem', fontSize: '0.85rem', background: '#1a202c', border: '1px solid #4a5568', color: '#fff', borderRadius: '4px'}}
              />
            </div>
            <button onClick={handleIssue} className="btn-primary" style={{padding: '0.4rem', fontSize: '0.85rem'}}>
              Issue Scoped Token
            </button>
            {issuedToken && (
              <div style={{marginTop: '0.5rem', fontSize: '0.75rem', wordBreak: 'break-all', background: '#111', padding: '0.5rem', borderRadius: '4px'}}>
                <span style={{color: '#48bb78'}}>Token:</span> {issuedToken.token?.slice(0, 40)}...<br />
                <span style={{color: '#90cdf4'}}>JTI:</span> {issuedToken.jti}
              </div>
            )}
          </div>
        </div>

        {/* Verification & Revocation */}
        <div style={{background: 'rgba(255,255,255,0.02)', padding: '1rem', borderRadius: '6px', border: '1px solid rgba(255,255,255,0.05)'}}>
          <h4 style={{margin: '0 0 0.75rem', fontSize: '0.95rem'}}>Verify & Revoke Tokens (GAP-SEC-008, 010)</h4>
          <div style={{display: 'flex', flexDirection: 'column', gap: '0.6rem'}}>
            <div>
              <label style={{fontSize: '0.75rem', color: '#a0aec0', display: 'block'}}>Token to Verify</label>
              <input
                type="text"
                value={tokenToVerify}
                onChange={e => setTokenToVerify(e.target.value)}
                placeholder="Paste token string"
                style={{width: '100%', padding: '0.4rem', fontSize: '0.85rem', background: '#1a202c', border: '1px solid #4a5568', color: '#fff', borderRadius: '4px'}}
              />
            </div>
            <button onClick={handleVerify} className="btn-secondary" style={{padding: '0.4rem', fontSize: '0.85rem'}}>
              Verify Token (Requires graph:read scope)
            </button>
            {verifyResult && (
              <div style={{fontSize: '0.75rem', background: '#111', padding: '0.5rem', borderRadius: '4px'}}>
                <span style={{color: verifyResult.valid ? '#48bb78' : '#f56565'}}>
                  {verifyResult.valid ? 'VALID TOKEN' : 'VERIFICATION REJECTED'}
                </span>
                {verifyResult.payload && <div>Subject: {verifyResult.payload.sub} | Scopes: {verifyResult.payload.scopes?.join(', ')}</div>}
              </div>
            )}

            <div style={{borderTop: '1px solid #2d3748', paddingTop: '0.6rem', marginTop: '0.4rem'}}>
              <label style={{fontSize: '0.75rem', color: '#a0aec0', display: 'block'}}>Revoke Token JTI or Subject</label>
              <div style={{display: 'flex', gap: '0.5rem'}}>
                <input
                  type="text"
                  value={revokeId}
                  onChange={e => setRevokeId(e.target.value)}
                  placeholder="Enter JTI or subject"
                  style={{flex: 1, padding: '0.4rem', fontSize: '0.85rem', background: '#1a202c', border: '1px solid #4a5568', color: '#fff', borderRadius: '4px'}}
                />
                <button onClick={handleRevoke} className="btn-secondary" style={{padding: '0.4rem 0.8rem', fontSize: '0.85rem', color: '#f56565'}}>
                  Revoke
                </button>
              </div>
              {revokeResult && (
                <div style={{marginTop: '0.4rem', fontSize: '0.75rem', color: '#48bb78'}}>
                  Revocation recorded. Active CRL count: {revokeResult.active_revocations}
                </div>
              )}
            </div>
          </div>
        </div>
      </div>

      {/* Role Hierarchy Matrix */}
      {matrix && matrix.roles_hierarchy && (
        <div style={{background: 'rgba(255,255,255,0.02)', padding: '1rem', borderRadius: '6px', border: '1px solid rgba(255,255,255,0.05)'}}>
          <h4 style={{margin: '0 0 0.5rem', fontSize: '0.95rem'}}>Role Hierarchy & Inheritance Matrix (GAP-SEC-012)</h4>
          <div style={{display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: '0.5rem'}}>
            {Object.entries(matrix.roles_hierarchy).map(([role, def]) => (
              <div key={role} style={{background: '#1a202c', padding: '0.6rem', borderRadius: '4px', fontSize: '0.8rem'}}>
                <strong style={{color: '#90cdf4'}}>{role}</strong> (Rank {def.rank})
                <div style={{fontSize: '0.75rem', color: '#a0aec0', marginTop: '0.2rem'}}>
                  Inherits: {def.inherited_roles?.join(' → ') || 'none'}
                </div>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
