import React, {useState, useEffect, useCallback} from 'react';
import {Icon} from '../icons.jsx';

export default function SchemaDriftAndFreshnessPanel({api}) {
  const [error, setError] = useState('');
  const [subTab, setSubTab] = useState('drift');
  const [driftFindings, setDriftFindings] = useState([]);
  const [sourceFreshness, setSourceFreshness] = useState([]);

  const fetchDrift = useCallback(async () => {
    try {
      setError('');
      const d = await api('/api/v1/ontology/drift', undefined, 'GET');
      if (d && d.findings) setDriftFindings(d.findings);
      const f = await api('/api/v1/sources/freshness', undefined, 'GET');
      if (f && f.sources) setSourceFreshness(f.sources);
    } catch (exception) {
      setError(exception.message || 'The service is unavailable.');
    }
  }, [api]);

  useEffect(() => {
    fetchDrift();
  }, [fetchDrift]);

  return (
    <div className="drift-freshness-panel card" style={{padding: '1.5rem', background: '#1c1c24', borderRadius: '8px', border: '1px solid #333'}}>
      {error && <p role="alert" className="resource-error">{error}</p>}
      <div style={{display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1.25rem'}}>
        <div>
          <h3 style={{margin: 0, display: 'flex', alignItems: 'center', gap: '0.5rem'}}>
            <Icon name="activity" /> Schema Drift & Source Freshness (G2-ADMIN-006, G2-ADMIN-007)
          </h3>
          <p style={{margin: '0.2rem 0 0 0', fontSize: '0.85rem', color: '#888'}}>
            Track schema drift across upstream SaaS sources and live data freshness against SLA targets
          </p>
        </div>
        <div style={{display: 'flex', gap: '0.5rem'}}>
          <button
            onClick={() => setSubTab('drift')}
            style={{
              padding: '0.4rem 0.8rem',
              borderRadius: '4px',
              border: 'none',
              cursor: 'pointer',
              background: subTab === 'drift' ? '#6366f1' : '#282835',
              color: '#fff',
              fontSize: '0.85rem',
            }}
          >
            Schema Drift Console (G2-ADMIN-006)
          </button>
          <button
            onClick={() => setSubTab('freshness')}
            style={{
              padding: '0.4rem 0.8rem',
              borderRadius: '4px',
              border: 'none',
              cursor: 'pointer',
              background: subTab === 'freshness' ? '#10b981' : '#282835',
              color: '#fff',
              fontSize: '0.85rem',
            }}
          >
            Freshness / Lag Dashboard (G2-ADMIN-007)
          </button>
        </div>
      </div>

      {subTab === 'drift' ? (
        <div>
          <table style={{width: '100%', borderCollapse: 'collapse', fontSize: '0.85rem', textAlign: 'left'}}>
            <thead>
              <tr style={{borderBottom: '1px solid #333', color: '#aaa'}}>
                <th style={{padding: '0.6rem'}}>Source</th>
                <th style={{padding: '0.6rem'}}>Detected Field</th>
                <th style={{padding: '0.6rem'}}>Inferred Type</th>
                <th style={{padding: '0.6rem'}}>Suggested Mapping</th>
                <th style={{padding: '0.6rem'}}>Status</th>
                <th style={{padding: '0.6rem'}}>Detected At</th>
              </tr>
            </thead>
            <tbody>
              {driftFindings.map((df, i) => (
                <tr key={i} style={{borderBottom: '1px solid #282832'}}>
                  <td style={{padding: '0.6rem', color: '#fff'}}>{df.source}</td>
                  <td style={{padding: '0.6rem', fontFamily: 'monospace', color: '#f59e0b'}}>{df.field_name}</td>
                  <td style={{padding: '0.6rem', color: '#888'}}>{df.detected_type}</td>
                  <td style={{padding: '0.6rem', color: '#60a5fa'}}>{df.suggested_mapping}</td>
                  <td style={{padding: '0.6rem'}}>
                    <span style={{
                      padding: '0.15rem 0.4rem',
                      borderRadius: '3px',
                      background: df.status === 'MAPPED' ? 'rgba(16, 185, 129, 0.2)' : 'rgba(245, 158, 11, 0.2)',
                      color: df.status === 'MAPPED' ? '#34d399' : '#fbbf24',
                      fontSize: '0.75rem',
                      fontWeight: 600,
                    }}>
                      {df.status}
                    </span>
                  </td>
                  <td style={{padding: '0.6rem', color: '#666'}}>{df.detected_at}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      ) : (
        <div>
          <div style={{display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(260px, 1fr))', gap: '1rem'}}>
            {sourceFreshness.map(sf => (
              <div key={sf.connector} style={{background: '#15151c', border: sf.status === 'FRESH' ? '1px solid #333' : '1px solid #ef4444', borderRadius: '6px', padding: '1rem'}}>
                <div style={{display: 'flex', justifyContent: 'space-between', alignItems: 'center'}}>
                  <strong style={{color: '#fff'}}>{sf.source_name}</strong>
                  <span style={{
                    fontSize: '0.75rem',
                    padding: '0.2rem 0.4rem',
                    borderRadius: '3px',
                    background: sf.status === 'FRESH' ? 'rgba(16, 185, 129, 0.2)' : 'rgba(239, 68, 68, 0.2)',
                    color: sf.status === 'FRESH' ? '#34d399' : '#f87171',
                    fontWeight: 600,
                  }}>
                    {sf.status}
                  </span>
                </div>
                <div style={{marginTop: '0.75rem', fontSize: '0.85rem', color: '#aaa', display: 'flex', flexDirection: 'column', gap: '0.3rem'}}>
                  <div>Last Sync: <strong style={{color: '#ddd'}}>{sf.last_synced}</strong></div>
                  <div>Current Lag: <strong style={{color: sf.status === 'FRESH' ? '#34d399' : '#f87171'}}>{sf.lag_seconds}s</strong> (Target: &lt;{sf.sla_target})</div>
                  <div>Connector ID: <span style={{fontFamily: 'monospace', color: '#666'}}>{sf.connector}</span></div>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
