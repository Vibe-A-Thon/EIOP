import React, {useState, useEffect, useCallback} from 'react';
import {Icon} from '../icons.jsx';

export default function KnowledgeGovernanceAndSLOPanel({api}) {
  const [error, setError] = useState('');
  const [subTab, setSubTab] = useState('quality');
  const [slos, setSlos] = useState([]);
  const [debtScore, setDebtScore] = useState({});
  const [proposals, setProposals] = useState([]);
  const [workspaces, setWorkspaces] = useState([]);
  const [qualityStats, setQualityStats] = useState({});

  const fetchData = useCallback(async () => {
    try {
      setError('');
      const q = await api('/api/v1/graph/quality', undefined, 'GET');
      if (q && q.stats) setQualityStats(q.stats);
      const d = await api('/api/v1/knowledge-debt/summary', undefined, 'GET');
      if (d) setDebtScore(d);
      const p = await api('/api/v1/ontology/proposals', undefined, 'GET');
      if (p && p.proposals) setProposals(p.proposals);
      const w = await api('/api/v1/simulations', undefined, 'GET');
      if (w && w.workspaces) setWorkspaces(w.workspaces);
    } catch (exception) {
      setError(exception.message || 'The service is unavailable.');
    }
  }, [api]);

  useEffect(() => {
    fetchData();
  }, [fetchData]);

  return (
    <div className="gov-slo-panel card" style={{padding: '1.5rem', background: '#1c1c24', borderRadius: '8px', border: '1px solid #333'}}>
      {error && <p role="alert" className="resource-error">{error}</p>}
      <div style={{display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1.25rem'}}>
        <div>
          <h3 style={{margin: 0, display: 'flex', alignItems: 'center', gap: '0.5rem'}}>
            <Icon name="check" /> Governance, SLOs & Quality (G2-ADMIN-014..017, FR-ADMIN-002)
          </h3>
          <p style={{margin: '0.2rem 0 0 0', fontSize: '0.85rem', color: '#888'}}>
            SLO targets, knowledge debt quantification, ontology evolution proposals, and what-if simulation workspaces
          </p>
        </div>
        <div style={{display: 'flex', gap: '0.5rem', flexWrap: 'wrap'}}>
          <button
            onClick={() => setSubTab('quality')}
            style={{
              padding: '0.4rem 0.8rem',
              borderRadius: '4px',
              border: 'none',
              cursor: 'pointer',
              background: subTab === 'quality' ? '#6366f1' : '#282835',
              color: '#fff',
              fontSize: '0.8rem',
            }}
          >
            Graph Quality (FR-ADMIN-002)
          </button>
          <button
            onClick={() => setSubTab('slo')}
            style={{
              padding: '0.4rem 0.8rem',
              borderRadius: '4px',
              border: 'none',
              cursor: 'pointer',
              background: subTab === 'slo' ? '#10b981' : '#282835',
              color: '#fff',
              fontSize: '0.8rem',
            }}
          >
            SLO Management (G2-ADMIN-014)
          </button>
          <button
            onClick={() => setSubTab('debt')}
            style={{
              padding: '0.4rem 0.8rem',
              borderRadius: '4px',
              border: 'none',
              cursor: 'pointer',
              background: subTab === 'debt' ? '#f59e0b' : '#282835',
              color: '#fff',
              fontSize: '0.8rem',
            }}
          >
            Knowledge Debt (G2-ADMIN-015)
          </button>
          <button
            onClick={() => setSubTab('proposals')}
            style={{
              padding: '0.4rem 0.8rem',
              borderRadius: '4px',
              border: 'none',
              cursor: 'pointer',
              background: subTab === 'proposals' ? '#8b5cf6' : '#282835',
              color: '#fff',
              fontSize: '0.8rem',
            }}
          >
            Evolution Proposals (G2-ADMIN-016)
          </button>
          <button
            onClick={() => setSubTab('workspaces')}
            style={{
              padding: '0.4rem 0.8rem',
              borderRadius: '4px',
              border: 'none',
              cursor: 'pointer',
              background: subTab === 'workspaces' ? '#ec4899' : '#282835',
              color: '#fff',
              fontSize: '0.8rem',
            }}
          >
            Simulation Workspaces (G2-ADMIN-017)
          </button>
        </div>
      </div>

      {subTab === 'quality' && (
        <div style={{display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(220px, 1fr))', gap: '1rem'}}>
          <div style={{background: '#15151c', padding: '1rem', borderRadius: '6px', border: '1px solid #333', textAlign: 'center'}}>
            <span style={{fontSize: '0.8rem', color: '#888'}}>TOTAL VERTICES</span>
            <h3 style={{fontSize: '1.6rem', margin: '0.3rem 0', color: '#38bdf8'}}>{qualityStats.total_vertices?.toLocaleString()}</h3>
          </div>
          <div style={{background: '#15151c', padding: '1rem', borderRadius: '6px', border: '1px solid #333', textAlign: 'center'}}>
            <span style={{fontSize: '0.8rem', color: '#888'}}>TOTAL EDGES</span>
            <h3 style={{fontSize: '1.6rem', margin: '0.3rem 0', color: '#818cf8'}}>{qualityStats.total_edges?.toLocaleString()}</h3>
          </div>
          <div style={{background: '#15151c', padding: '1rem', borderRadius: '6px', border: '1px solid #333', textAlign: 'center'}}>
            <span style={{fontSize: '0.8rem', color: '#888'}}>VALIDATION CONFORMANCE</span>
            <h3 style={{fontSize: '1.6rem', margin: '0.3rem 0', color: '#34d399'}}>{qualityStats.validation_pass_rate}</h3>
          </div>
          <div style={{background: '#15151c', padding: '1rem', borderRadius: '6px', border: '1px solid #333', textAlign: 'center'}}>
            <span style={{fontSize: '0.8rem', color: '#888'}}>SCHEMA / BACKUP STATE</span>
            <h4 style={{fontSize: '1rem', margin: '0.6rem 0', color: '#ddd'}}>Schema v{qualityStats.schema_version} · Backup {qualityStats.backup_status}</h4>
          </div>
        </div>
      )}

      {subTab === 'slo' && (
        <div style={{display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(260px, 1fr))', gap: '1rem'}}>
          {slos.map(s => (
            <div key={s.name} style={{background: '#15151c', border: '1px solid #333', borderRadius: '6px', padding: '1rem'}}>
              <div style={{display: 'flex', justifyContent: 'space-between', alignItems: 'center'}}>
                <strong style={{color: '#fff', fontSize: '0.9rem'}}>{s.name}</strong>
                <span style={{padding: '0.15rem 0.4rem', borderRadius: '3px', background: 'rgba(16, 185, 129, 0.2)', color: '#34d399', fontSize: '0.75rem', fontWeight: 600}}>
                  {s.status}
                </span>
              </div>
              <div style={{marginTop: '0.75rem', display: 'flex', justifyContent: 'space-between', fontSize: '0.85rem', color: '#aaa'}}>
                <span>Current: <strong style={{color: '#34d399'}}>{s.current}</strong></span>
                <span>Target: <strong>{s.target}</strong></span>
              </div>
            </div>
          ))}
        </div>
      )}

      {subTab === 'debt' && (
        <div style={{display: 'grid', gridTemplateColumns: '1fr 2fr', gap: '1.5rem', alignItems: 'center'}}>
          <div style={{background: '#15151c', padding: '1.5rem', borderRadius: '6px', border: '1px solid #333', textAlign: 'center'}}>
            <span style={{fontSize: '0.85rem', color: '#888'}}>OVERALL KNOWLEDGE DEBT INDEX</span>
            <h2 style={{fontSize: '2.5rem', margin: '0.5rem 0', color: '#34d399'}}>{debtScore.score} / 100</h2>
            <span style={{color: '#34d399', fontWeight: 600}}>RATING: {debtScore.rating}</span>
          </div>
          <div style={{background: '#15151c', padding: '1.5rem', borderRadius: '6px', border: '1px solid #333', display: 'flex', flexDirection: 'column', gap: '0.75rem'}}>
            <div style={{display: 'flex', justifyContent: 'space-between', color: '#ccc', fontSize: '0.85rem'}}>
              <span>Orphaned Unlinked Vertices:</span>
              <strong style={{color: '#f59e0b'}}>{debtScore.orphaned_nodes}</strong>
            </div>
            <div style={{display: 'flex', justifyContent: 'space-between', color: '#ccc', fontSize: '0.85rem'}}>
              <span>Stale / Outdated Documentation Pages:</span>
              <strong style={{color: '#f59e0b'}}>{debtScore.stale_docs}</strong>
            </div>
            <div style={{display: 'flex', justifyContent: 'space-between', color: '#ccc', fontSize: '0.85rem'}}>
              <span>Untested Production Endpoints:</span>
              <strong style={{color: '#f59e0b'}}>{debtScore.missing_tests}</strong>
            </div>
          </div>
        </div>
      )}

      {subTab === 'proposals' && (
        <div style={{display: 'flex', flexDirection: 'column', gap: '0.75rem'}}>
          {proposals.map(p => (
            <div key={p.id} style={{background: '#15151c', border: '1px solid #333', borderRadius: '6px', padding: '1rem', display: 'flex', justifyContent: 'space-between', alignItems: 'center'}}>
              <div>
                <strong style={{color: '#fff'}}>{p.title}</strong>
                <div style={{fontSize: '0.8rem', color: '#666', marginTop: '0.2rem'}}>ID: {p.id} · Proposed by {p.author} at {p.submitted_at}</div>
              </div>
              <span style={{padding: '0.2rem 0.5rem', borderRadius: '4px', background: p.status === 'APPROVED' ? 'rgba(16, 185, 129, 0.2)' : 'rgba(139, 92, 246, 0.2)', color: p.status === 'APPROVED' ? '#34d399' : '#a78bfa', fontSize: '0.8rem', fontWeight: 600}}>
                {p.status}
              </span>
            </div>
          ))}
        </div>
      )}

      {subTab === 'workspaces' && (
        <div style={{display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(280px, 1fr))', gap: '1rem'}}>
          {workspaces.map(w => (
            <div key={w.id} style={{background: '#15151c', border: '1px solid #333', borderRadius: '6px', padding: '1rem'}}>
              <strong style={{color: '#fff', fontSize: '0.95rem'}}>{w.name}</strong>
              <div style={{fontSize: '0.8rem', color: '#888', margin: '0.4rem 0'}}>Workspace: <span style={{fontFamily: 'monospace', color: '#60a5fa'}}>{w.id}</span></div>
              <div style={{fontSize: '0.8rem', color: '#666'}}>Owner: {w.owner} · Active Scenario Forks: {w.forks_count}</div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
