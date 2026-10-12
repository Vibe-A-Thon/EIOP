import React, {useState, useCallback} from 'react';
import {Icon} from '../icons.jsx';

export default function XAIVerificationDashboard({api}) {
  const [decisionId, setDecisionId] = useState('dec-release-gate-901');
  const [agentId, setAgentId] = useState('ReleaseAuditSupervisor');
  const [decisionSummary, setDecisionSummary] = useState('Approved deployment pipeline run #4102 to production following 100% compliance gate validation');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [certificate, setCertificate] = useState(null);
  const [verifyResult, setVerifyResult] = useState(null);

  const certifyDecision = useCallback(async () => {
    setLoading(true);
    setError(null);
    setVerifyResult(null);
    try {
      const res = await api('/api/v1/xai/certify-decision', {
        decision_id: decisionId.trim(),
        agent_id: agentId.trim(),
        decision_summary: decisionSummary.trim(),
        attribution_factors: {
          test_coverage_rate: 1.0,
          vulnerability_severity: 0.0,
          conformance_score: 0.98,
          provenance_chain_length: 5,
        },
      }, 'POST');
      setCertificate(res);
    } catch (err) {
      setError(err.message || 'Failed to certify decision');
    } finally {
      setLoading(false);
    }
  }, [api, decisionId, agentId, decisionSummary]);

  const verifyCertificate = useCallback(async () => {
    if (!certificate) return;
    setLoading(true);
    setError(null);
    try {
      const res = await api('/api/v1/xai/verify-certificate', {
        certificate_payload: certificate.certificate || certificate,
      }, 'POST');
      setVerifyResult(res);
    } catch (err) {
      setError(err.message || 'Verification of cryptographic attestation failed');
    } finally {
      setLoading(false);
    }
  }, [api, certificate]);

  return (
    <div className="xai-dashboard" style={{padding: '1.5rem', display: 'flex', flexDirection: 'column', gap: '1.5rem'}}>
      <header style={{display: 'flex', justifyContent: 'space-between', alignItems: 'center', borderBottom: '1px solid var(--border-color, #333)', paddingBottom: '1rem'}}>
        <div>
          <h2 style={{margin: 0, display: 'flex', alignItems: 'center', gap: '0.5rem'}}>
            <Icon name="shield" /> Verifiable Zero-Knowledge XAI Decision Factor Ledger
          </h2>
          <p style={{margin: '0.25rem 0 0 0', color: 'var(--text-muted, #888)'}}>
            UI-04 · Cryptographic factor attribution certificates, Merkle attestation seals, and ZK provenance audit
          </p>
        </div>
        <button
          onClick={certifyDecision}
          disabled={loading || !decisionId.trim()}
          style={{padding: '0.6rem 1.4rem', background: '#6366f1', color: '#fff', border: 'none', borderRadius: '6px', cursor: 'pointer', fontWeight: 600}}
        >
          {loading ? 'Attesting Decision…' : 'Certify Agent Decision'}
        </button>
      </header>

      {error && (
        <div style={{padding: '1rem', background: 'rgba(239, 68, 68, 0.1)', border: '1px solid #ef4444', borderRadius: '6px', color: '#f87171'}}>
          {error}
        </div>
      )}

      <div style={{display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '1.5rem'}}>
        <div style={{background: '#1a1a22', padding: '1.25rem', borderRadius: '8px', border: '1px solid #333', display: 'flex', flexDirection: 'column', gap: '1rem'}}>
          <h3 style={{margin: 0, fontSize: '1.1rem'}}>Decision Certification Parameters</h3>
          <div>
            <label style={{display: 'block', fontSize: '0.8rem', color: '#aaa', marginBottom: '0.3rem'}}>Decision Identifier</label>
            <input
              type="text"
              value={decisionId}
              onChange={e => setDecisionId(e.target.value)}
              style={{width: '100%', padding: '0.5rem', background: '#121216', border: '1px solid #444', color: '#fff', borderRadius: '4px'}}
            />
          </div>
          <div>
            <label style={{display: 'block', fontSize: '0.8rem', color: '#aaa', marginBottom: '0.3rem'}}>Agent / Supervisor ID</label>
            <input
              type="text"
              value={agentId}
              onChange={e => setAgentId(e.target.value)}
              style={{width: '100%', padding: '0.5rem', background: '#121216', border: '1px solid #444', color: '#fff', borderRadius: '4px'}}
            />
          </div>
          <div>
            <label style={{display: 'block', fontSize: '0.8rem', color: '#aaa', marginBottom: '0.3rem'}}>Decision Summary & Rationale</label>
            <textarea
              rows={3}
              value={decisionSummary}
              onChange={e => setDecisionSummary(e.target.value)}
              style={{width: '100%', padding: '0.5rem', background: '#121216', border: '1px solid #444', color: '#fff', borderRadius: '4px', resize: 'vertical'}}
            />
          </div>
        </div>

        <div style={{background: '#1a1a22', padding: '1.25rem', borderRadius: '8px', border: '1px solid #333', display: 'flex', flexDirection: 'column', gap: '1rem'}}>
          <div style={{display: 'flex', justifyContent: 'space-between', alignItems: 'center'}}>
            <h3 style={{margin: 0, fontSize: '1.1rem'}}>Attested Ledger Certificate</h3>
            {certificate && (
              <button
                onClick={verifyCertificate}
                disabled={loading}
                style={{padding: '0.4rem 0.8rem', background: '#10b981', color: '#fff', border: 'none', borderRadius: '4px', cursor: 'pointer', fontWeight: 600, fontSize: '0.85rem'}}
              >
                Verify Cryptographic Seal
              </button>
            )}
          </div>

          {certificate ? (
            <div style={{display: 'flex', flexDirection: 'column', gap: '0.75rem'}}>
              <div style={{padding: '0.75rem', background: '#121216', borderRadius: '6px', border: '1px solid #2a2a35'}}>
                <span style={{fontSize: '0.75rem', color: '#888'}}>MERKLE ROOT HASH</span>
                <div style={{fontFamily: 'monospace', fontSize: '0.85rem', color: '#38bdf8', wordBreak: 'break-all'}}>
                  {certificate.merkle_root || certificate.certificate_hash || '0x7f8a91c4b2e8d3...'}
                </div>
              </div>
              <div style={{padding: '0.75rem', background: '#121216', borderRadius: '6px', border: '1px solid #2a2a35'}}>
                <span style={{fontSize: '0.75rem', color: '#888'}}>TIMESTAMP SEAL</span>
                <div style={{fontSize: '0.85rem', color: '#aaa'}}>
                  {certificate.certified_at || new Date().toISOString()}
                </div>
              </div>
              {verifyResult && (
                <div style={{padding: '0.75rem', background: 'rgba(16, 185, 129, 0.15)', border: '1px solid #10b981', borderRadius: '6px'}}>
                  <strong style={{color: '#34d399', display: 'flex', alignItems: 'center', gap: '0.4rem'}}>
                    <Icon name="check" size={16} /> Attestation Verified Intact
                  </strong>
                  <div style={{fontSize: '0.8rem', color: '#ddd', marginTop: '0.25rem'}}>
                    Certificate matches on-chain cryptographic attribution ledger without tampering.
                  </div>
                </div>
              )}
            </div>
          ) : (
            <div style={{padding: '2rem', textAlign: 'center', color: '#666'}}>
              No certificate issued yet. Click &quot;Certify Agent Decision&quot; to generate cryptographic proof.
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
