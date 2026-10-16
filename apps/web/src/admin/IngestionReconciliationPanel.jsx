import React, {useState, useEffect, useCallback} from 'react';
import {Icon} from '../icons.jsx';

export default function IngestionReconciliationPanel({api}) {
  const [runs, setRuns] = useState([]);
  const [loading, setLoading] = useState(false);
  const [filterType, setFilterType] = useState('ALL');
  const [error, setError] = useState('');

  const fetchRuns = useCallback(async () => {
    setLoading(true);
    setError('');
    try {
      const data = await api('/api/v1/ingestion/runs', undefined, 'GET');
      const items = Array.isArray(data) ? data : data?.runs;
      if (!Array.isArray(items)) throw new Error('Ingestion runs returned an unsupported response.');
      setRuns(items);
    } catch (exception) {
      setRuns([]);
      setError(exception.message || 'Ingestion runs are unavailable.');
    } finally {
      setLoading(false);
    }
  }, [api]);

  useEffect(() => {
    fetchRuns();
  }, [fetchRuns]);

  const triggerRun = async (mode) => {
    setLoading(true);
    setError('');
    try {
      await api('/api/v1/ingestion/trigger', {mode}, 'POST');
      await fetchRuns();
    } catch (exception) {
      setError(exception.message || 'The ingestion run could not be started.');
    } finally {
      setLoading(false);
    }
  };

  const filtered = filterType === 'ALL' ? runs : runs.filter(r => r.mode === filterType);

  return (
    <div className="ingestion-panel card" style={{padding: '1.5rem', background: '#1c1c24', borderRadius: '8px', border: '1px solid #333'}}>
      {error && <p role="alert" className="resource-error">{error}</p>}
      <div style={{display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1rem'}}>
        <div>
          <h3 style={{margin: 0, display: 'flex', alignItems: 'center', gap: '0.5rem'}}>
            <Icon name="refresh" /> Baseline / Incremental / Reconciliation Status (G2-ADMIN-003, FR-ADMIN-001)
          </h3>
          <p style={{margin: '0.2rem 0 0 0', fontSize: '0.85rem', color: '#888'}}>
            Monitor extraction pipelines, reconciliation passes, and dry-run/replay verification
          </p>
        </div>
        <div style={{display: 'flex', gap: '0.5rem'}}>
          <button onClick={() => triggerRun('INCREMENTAL')} disabled={loading} style={{padding: '0.4rem 0.8rem', background: '#6366f1', color: '#fff', border: 'none', borderRadius: '4px', cursor: 'pointer', fontSize: '0.85rem'}}>
            + Run Incremental
          </button>
          <button onClick={() => triggerRun('RECONCILIATION')} disabled={loading} style={{padding: '0.4rem 0.8rem', background: '#10b981', color: '#fff', border: 'none', borderRadius: '4px', cursor: 'pointer', fontSize: '0.85rem'}}>
            + Trigger Reconciliation
          </button>
        </div>
      </div>

      <div style={{display: 'flex', gap: '0.5rem', marginBottom: '1rem'}}>
        {['ALL', 'BASELINE', 'INCREMENTAL', 'RECONCILIATION'].map(f => (
          <button
            key={f}
            onClick={() => setFilterType(f)}
            style={{
              padding: '0.3rem 0.7rem',
              borderRadius: '4px',
              border: '1px solid #444',
              background: filterType === f ? '#333' : 'transparent',
              color: filterType === f ? '#fff' : '#aaa',
              cursor: 'pointer',
              fontSize: '0.8rem',
            }}
          >
            {f}
          </button>
        ))}
      </div>

      <table style={{width: '100%', borderCollapse: 'collapse', fontSize: '0.85rem', textAlign: 'left'}}>
        <thead>
          <tr style={{borderBottom: '1px solid #333', color: '#aaa'}}>
            <th style={{padding: '0.6rem'}}>Run ID</th>
            <th style={{padding: '0.6rem'}}>Mode</th>
            <th style={{padding: '0.6rem'}}>Source</th>
            <th style={{padding: '0.6rem'}}>Status</th>
            <th style={{padding: '0.6rem'}}>Entities</th>
            <th style={{padding: '0.6rem'}}>Errors</th>
            <th style={{padding: '0.6rem'}}>Duration</th>
            <th style={{padding: '0.6rem'}}>Time</th>
          </tr>
        </thead>
        <tbody>
          {filtered.map(r => (
            <tr key={r.run_id} style={{borderBottom: '1px solid #282832'}}>
              <td style={{padding: '0.6rem', fontFamily: 'monospace', color: '#38bdf8'}}>{r.run_id}</td>
              <td style={{padding: '0.6rem'}}><span style={{padding: '0.15rem 0.4rem', borderRadius: '3px', background: '#262635', color: '#ddd', fontSize: '0.75rem'}}>{r.mode}</span></td>
              <td style={{padding: '0.6rem', color: '#fff'}}>{r.source}</td>
              <td style={{padding: '0.6rem'}}>
                <span style={{color: r.status === 'COMPLETED' ? '#34d399' : r.status === 'RUNNING' ? '#60a5fa' : '#f87171', fontWeight: 600}}>
                  {r.status}
                </span>
              </td>
              <td style={{padding: '0.6rem'}}>{r.entities_ingested}</td>
              <td style={{padding: '0.6rem', color: r.errors > 0 ? '#f87171' : '#aaa'}}>{r.errors}</td>
              <td style={{padding: '0.6rem', color: '#888'}}>{r.duration}</td>
              <td style={{padding: '0.6rem', color: '#666'}}>{r.timestamp}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
