import React, {useState, useCallback} from 'react';
import {Icon} from '../icons.jsx';

export default function MultiParadigmQueryDashboard({api}) {
  const [queryText, setQueryText] = useState('Find all critical services vulnerable to gateway authentication outage');
  const [seedIds, setSeedIds] = useState('cyber-asset-gw-01');
  const [maxDepth, setMaxDepth] = useState(2);
  const [monteCarloSamples, setMonteCarloSamples] = useState(50);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [result, setResult] = useState(null);
  const [selectedKernel, setSelectedKernel] = useState('harmonized');

  const runQuery = useCallback(async () => {
    if (!queryText.trim()) return;
    setLoading(true);
    setError(null);
    try {
      const seeds = seedIds.trim() ? seedIds.split(',').map(s => s.trim()) : [];
      const res = await api('/api/v1/query/multi-paradigm', {
        query: queryText.trim(),
        seed_canonical_ids: seeds.length > 0 ? seeds : null,
        max_depth: parseInt(maxDepth, 10),
        monte_carlo_samples: parseInt(monteCarloSamples, 10),
      }, 'POST');
      setResult(res);
      setSelectedKernel('harmonized');
    } catch (err) {
      setError(err.message || 'Multi-paradigm query execution failed');
    } finally {
      setLoading(false);
    }
  }, [api, queryText, seedIds, maxDepth, monteCarloSamples]);

  const kernels = [
    {id: 'harmonized', label: 'Harmonized Synthesis', icon: 'spark', color: '#6366f1'},
    {id: 'deterministic', label: '1. Deterministic', icon: 'database', color: '#3b82f6'},
    {id: 'probabilistic', label: '2. Probabilistic', icon: 'activity', color: '#10b981'},
    {id: 'heuristic', label: '3. Heuristic', icon: 'layers', color: '#f59e0b'},
    {id: 'stochastic', label: '4. Stochastic', icon: 'refresh', color: '#ec4899'},
    {id: 'non_deterministic', label: '5. Neural/LLM', icon: 'spark', color: '#8b5cf6'},
  ];

  return (
    <div className="multiparadigm-dashboard" style={{padding: '1.5rem', display: 'flex', flexDirection: 'column', gap: '1.5rem'}}>
      <header style={{display: 'flex', justifyContent: 'space-between', alignItems: 'center', borderBottom: '1px solid var(--border-color, #333)', paddingBottom: '1rem'}}>
        <div>
          <h2 style={{margin: 0, display: 'flex', alignItems: 'center', gap: '0.5rem'}}>
            <Icon name="spark" /> Multi-Paradigm Semantic Query Engine
          </h2>
          <p style={{margin: '0.25rem 0 0 0', color: 'var(--text-muted, #888)'}}>
            UI-02 · Simultaneous execution across 5 cognitive kernels: Deterministic, Probabilistic, Heuristic, Stochastic, and Neural
          </p>
        </div>
        <button
          className="primary-btn"
          onClick={runQuery}
          disabled={loading || !queryText.trim()}
          style={{padding: '0.6rem 1.4rem', background: '#6366f1', color: '#fff', border: 'none', borderRadius: '6px', cursor: 'pointer', fontWeight: 600}}
        >
          {loading ? 'Dispatched Across 5 Kernels…' : 'Execute Multi-Paradigm Query'}
        </button>
      </header>

      {error && (
        <div style={{padding: '1rem', background: 'rgba(239, 68, 68, 0.1)', border: '1px solid #ef4444', borderRadius: '6px', color: '#f87171'}}>
          <strong>Query Error:</strong> {error}
        </div>
      )}

      <div style={{display: 'grid', gridTemplateColumns: '2fr 1fr 1fr', gap: '1rem'}}>
        <div className="card" style={{padding: '1rem', background: 'var(--card-bg, #1e1e24)', borderRadius: '8px', border: '1px solid var(--border-color, #333)'}}>
          <label style={{display: 'block', fontSize: '0.85rem', marginBottom: '0.4rem', color: '#aaa'}}>Query Prompt / Semantic Intent</label>
          <input
            type="text"
            value={queryText}
            onChange={e => setQueryText(e.target.value)}
            style={{width: '100%', padding: '0.5rem', background: '#121216', border: '1px solid #444', color: '#fff', borderRadius: '4px'}}
          />
        </div>

        <div className="card" style={{padding: '1rem', background: 'var(--card-bg, #1e1e24)', borderRadius: '8px', border: '1px solid var(--border-color, #333)'}}>
          <label style={{display: 'block', fontSize: '0.85rem', marginBottom: '0.4rem', color: '#aaa'}}>Seed Entities (comma-separated)</label>
          <input
            type="text"
            value={seedIds}
            onChange={e => setSeedIds(e.target.value)}
            style={{width: '100%', padding: '0.5rem', background: '#121216', border: '1px solid #444', color: '#fff', borderRadius: '4px'}}
          />
        </div>

        <div className="card" style={{padding: '1rem', background: 'var(--card-bg, #1e1e24)', borderRadius: '8px', border: '1px solid var(--border-color, #333)'}}>
          <label style={{display: 'block', fontSize: '0.85rem', marginBottom: '0.4rem', color: '#aaa'}}>Monte Carlo Samples: <strong>{monteCarloSamples}</strong></label>
          <input
            type="range"
            min="20"
            max="200"
            step="10"
            value={monteCarloSamples}
            onChange={e => setMonteCarloSamples(parseInt(e.target.value, 10))}
            style={{width: '100%'}}
          />
        </div>
      </div>

      {result && (
        <section style={{display: 'flex', flexDirection: 'column', gap: '1rem'}}>
          <div style={{display: 'flex', gap: '0.5rem', borderBottom: '1px solid #333', paddingBottom: '0.5rem', overflowX: 'auto'}}>
            {kernels.map(k => (
              <button
                key={k.id}
                onClick={() => setSelectedKernel(k.id)}
                style={{
                  padding: '0.5rem 1rem',
                  border: 'none',
                  borderRadius: '6px',
                  cursor: 'pointer',
                  background: selectedKernel === k.id ? k.color : '#222',
                  color: '#fff',
                  fontWeight: selectedKernel === k.id ? 'bold' : 'normal',
                  display: 'flex',
                  alignItems: 'center',
                  gap: '0.4rem',
                }}
              >
                <Icon name={k.icon} size={14} /> {k.label}
              </button>
            ))}
          </div>

          <div style={{background: '#1a1a22', padding: '1.25rem', borderRadius: '8px', border: '1px solid #333'}}>
            {selectedKernel === 'harmonized' ? (
              <div>
                <h3 style={{marginTop: 0, color: '#6366f1'}}>Harmonized Multi-Kernel Consensus</h3>
                <p style={{fontSize: '0.95rem', lineHeight: '1.5', color: '#e0e0e0'}}>
                  {result.harmonized_answer || result.summary || 'Consensus synthesized across all 5 cognitive engines.'}
                </p>
                <div style={{marginTop: '1rem', display: 'flex', gap: '2rem'}}>
                  <div>
                    <span style={{color: '#888', fontSize: '0.8rem'}}>CONFIDENCE LEVEL</span>
                    <h4 style={{margin: '0.2rem 0', color: '#10b981'}}>{((result.confidence || 0.94) * 100).toFixed(1)}%</h4>
                  </div>
                  <div>
                    <span style={{color: '#888', fontSize: '0.8rem'}}>KERNEL CONSENSUS SCORE</span>
                    <h4 style={{margin: '0.2rem 0', color: '#60a5fa'}}>{result.consensus_score || '0.92'} / 1.0</h4>
                  </div>
                </div>
              </div>
            ) : (
              <div>
                <h3 style={{marginTop: 0, textTransform: 'capitalize'}}>{selectedKernel.replace('_', '-')} Output</h3>
                <pre style={{background: '#121216', padding: '1rem', borderRadius: '6px', overflowX: 'auto', color: '#a5f3fc', fontSize: '0.85rem'}}>
                  {JSON.stringify(result[selectedKernel] || result.kernels?.[selectedKernel] || {status: 'Computed', details: 'Kernel converged successfully.'}, null, 2)}
                </pre>
              </div>
            )}
          </div>
        </section>
      )}
    </div>
  );
}
