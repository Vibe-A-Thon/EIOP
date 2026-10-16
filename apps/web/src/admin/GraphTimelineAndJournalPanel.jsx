import React, {useState, useEffect, useCallback} from 'react';
import {Icon} from '../icons.jsx';

export default function GraphTimelineAndJournalPanel({api}) {
  const [error, setError] = useState('');
  const [subTab, setSubTab] = useState('timeline');
  const [versions, setVersions] = useState([]);
  const [journalEntries, setJournalEntries] = useState([]);
  const [consumers, setConsumers] = useState([]);

  const fetchData = useCallback(async () => {
    try {
      setError('');
      const v = await api('/api/v1/graph/versions', undefined, 'GET');
      if (v && v.versions) setVersions(v.versions);
      const j = await api('/api/v1/journal/entries', undefined, 'GET');
      if (j && j.entries) setJournalEntries(j.entries);
      const c = await api('/api/v1/events/consumers', undefined, 'GET');
      if (c && c.consumers) setConsumers(c.consumers);
    } catch (exception) {
      setError(exception.message || 'The service is unavailable.');
    }
  }, [api]);

  useEffect(() => {
    fetchData();
  }, [fetchData]);

  return (
    <div className="timeline-journal-panel card" style={{padding: '1.5rem', background: '#1c1c24', borderRadius: '8px', border: '1px solid #333'}}>
      {error && <p role="alert" className="resource-error">{error}</p>}
      <div style={{display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1.25rem'}}>
        <div>
          <h3 style={{margin: 0, display: 'flex', alignItems: 'center', gap: '0.5rem'}}>
            <Icon name="clock" /> Timeline, Change Journal & Event Consumers (G2-ADMIN-008, 009, 010)
          </h3>
          <p style={{margin: '0.2rem 0 0 0', fontSize: '0.85rem', color: '#888'}}>
            Immutable graph revisions, bitemporal facts journal, and asynchronous event consumer health
          </p>
        </div>
        <div style={{display: 'flex', gap: '0.5rem'}}>
          <button
            onClick={() => setSubTab('timeline')}
            style={{
              padding: '0.4rem 0.8rem',
              borderRadius: '4px',
              border: 'none',
              cursor: 'pointer',
              background: subTab === 'timeline' ? '#6366f1' : '#282835',
              color: '#fff',
              fontSize: '0.85rem',
            }}
          >
            Version Timeline (G2-ADMIN-008)
          </button>
          <button
            onClick={() => setSubTab('journal')}
            style={{
              padding: '0.4rem 0.8rem',
              borderRadius: '4px',
              border: 'none',
              cursor: 'pointer',
              background: subTab === 'journal' ? '#10b981' : '#282835',
              color: '#fff',
              fontSize: '0.85rem',
            }}
          >
            Change Journal (G2-ADMIN-009)
          </button>
          <button
            onClick={() => setSubTab('consumers')}
            style={{
              padding: '0.4rem 0.8rem',
              borderRadius: '4px',
              border: 'none',
              cursor: 'pointer',
              background: subTab === 'consumers' ? '#f59e0b' : '#282835',
              color: '#fff',
              fontSize: '0.85rem',
            }}
          >
            Consumer Health (G2-ADMIN-010)
          </button>
        </div>
      </div>

      {subTab === 'timeline' && (
        <div style={{display: 'flex', flexDirection: 'column', gap: '1rem'}}>
          {versions.map(ver => (
            <div key={ver.version} style={{background: '#15151c', border: '1px solid #333', borderRadius: '6px', padding: '1rem'}}>
              <div style={{display: 'flex', justifyContent: 'space-between', alignItems: 'center'}}>
                <div>
                  <strong style={{color: '#60a5fa', fontSize: '1.1rem'}}>{ver.version}</strong>
                  <span style={{marginLeft: '0.6rem', padding: '0.15rem 0.4rem', borderRadius: '3px', background: '#252535', color: '#aaa', fontSize: '0.75rem'}}>
                    {ver.tag}
                  </span>
                </div>
                <span style={{fontSize: '0.8rem', color: '#666'}}>{ver.committed_at} by {ver.author}</span>
              </div>
              <p style={{margin: '0.5rem 0 0.75rem 0', fontSize: '0.85rem', color: '#ddd'}}>{ver.summary}</p>
              <div style={{fontSize: '0.8rem', color: '#888', display: 'flex', gap: '1.5rem'}}>
                <span>Vertices: <strong style={{color: '#34d399'}}>{ver.entities.toLocaleString()}</strong></span>
                <span>Edges: <strong style={{color: '#38bdf8'}}>{ver.edges.toLocaleString()}</strong></span>
              </div>
            </div>
          ))}
        </div>
      )}

      {subTab === 'journal' && (
        <table style={{width: '100%', borderCollapse: 'collapse', fontSize: '0.85rem', textAlign: 'left'}}>
          <thead>
            <tr style={{borderBottom: '1px solid #333', color: '#aaa'}}>
              <th style={{padding: '0.6rem'}}>Event ID</th>
              <th style={{padding: '0.6rem'}}>Action</th>
              <th style={{padding: '0.6rem'}}>Subject Entity</th>
              <th style={{padding: '0.6rem'}}>Type</th>
              <th style={{padding: '0.6rem'}}>Valid From</th>
              <th style={{padding: '0.6rem'}}>Source Evidence</th>
              <th style={{padding: '0.6rem'}}>Confidence</th>
            </tr>
          </thead>
          <tbody>
            {journalEntries.map(e => (
              <tr key={e.event_id} style={{borderBottom: '1px solid #282832'}}>
                <td style={{padding: '0.6rem', fontFamily: 'monospace', color: '#818cf8'}}>{e.event_id}</td>
                <td style={{padding: '0.6rem'}}>
                  <span style={{
                    fontSize: '0.75rem',
                    padding: '0.15rem 0.4rem',
                    borderRadius: '3px',
                    background: e.change_kind.includes('CREATED') || e.change_kind.includes('ASSERTED') ? 'rgba(16, 185, 129, 0.2)' : 'rgba(239, 68, 68, 0.2)',
                    color: e.change_kind.includes('CREATED') || e.change_kind.includes('ASSERTED') ? '#34d399' : '#f87171',
                  }}>
                    {e.change_kind}
                  </span>
                </td>
                <td style={{padding: '0.6rem', color: '#fff'}}>{e.entity_id}</td>
                <td style={{padding: '0.6rem', color: '#aaa'}}>{e.entity_label}</td>
                <td style={{padding: '0.6rem', color: '#666'}}>{e.bitemporal_valid_from}</td>
                <td style={{padding: '0.6rem', color: '#60a5fa'}}>{e.assertion_source}</td>
                <td style={{padding: '0.6rem', color: '#34d399'}}>{((e.confidence || 1.0) * 100).toFixed(0)}%</td>
              </tr>
            ))}
          </tbody>
        </table>
      )}

      {subTab === 'consumers' && (
        <div style={{display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(280px, 1fr))', gap: '1rem'}}>
          {consumers.map(c => (
            <div key={c.group_id} style={{background: '#15151c', border: '1px solid #333', borderRadius: '6px', padding: '1rem'}}>
              <div style={{display: 'flex', justifyContent: 'space-between', alignItems: 'center'}}>
                <strong style={{color: '#fff'}}>{c.group_id}</strong>
                <span style={{
                  fontSize: '0.75rem',
                  padding: '0.15rem 0.4rem',
                  borderRadius: '3px',
                  background: c.status === 'HEALTHY' ? 'rgba(16, 185, 129, 0.2)' : 'rgba(245, 158, 11, 0.2)',
                  color: c.status === 'HEALTHY' ? '#34d399' : '#fbbf24',
                  fontWeight: 600,
                }}>
                  {c.status}
                </span>
              </div>
              <div style={{marginTop: '0.75rem', fontSize: '0.85rem', color: '#aaa', display: 'flex', flexDirection: 'column', gap: '0.3rem'}}>
                <div>Consumer Partitions: <strong style={{color: '#ddd'}}>{c.partition_count}</strong></div>
                <div>Consumer Lag: <strong style={{color: c.total_lag === 0 ? '#34d399' : '#f59e0b'}}>{c.total_lag}</strong></div>
                <div>Processing Rate: <strong style={{color: '#38bdf8'}}>{c.rate_eps} events/sec</strong></div>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
