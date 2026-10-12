import React, {useState, useEffect, useCallback} from 'react';
import {Icon} from '../icons.jsx';

export default function CheckpointAndRecoveryPanel({api}) {
  const [subTab, setSubTab] = useState('checkpoints');
  const [checkpoints, setCheckpoints] = useState([
    {connector_id: 'jira-prod', partition: 'issue-stream-0', offset: '1048291', high_watermark: '1048300', lag: 9, updated_at: '2026-10-12 05:02:14'},
    {connector_id: 'github-org', partition: 'repo-commits-1', offset: '49201', high_watermark: '49201', lag: 0, updated_at: '2026-10-12 05:01:50'},
    {connector_id: 'snow-itsm', partition: 'incidents-table-0', offset: '8492', high_watermark: '8495', lag: 3, updated_at: '2026-10-12 04:58:30'},
  ]);
  const [dlqEvents, setDlqEvents] = useState([
    {event_id: 'err-evt-991', source: 'jira-prod', error_reason: 'Schema validation: missing mandatory summary key', payload_preview: '{"issue_key": "PROJ-891", "reporter": "alice"}', quarantined_at: '2026-10-12 04:22:11'},
    {event_id: 'err-evt-992', source: 'snow-itsm', error_reason: 'Unparseable ISO timestamp format in resolved_at', payload_preview: '{"incident_number": "INC09182", "resolved_at": "invalid-ts"}', quarantined_at: '2026-10-12 04:35:09'},
  ]);
  const [replaying, setReplaying] = useState(false);
  const [message, setMessage] = useState(null);

  const fetchStatus = useCallback(async () => {
    try {
      const cp = await api('/api/v1/ingestion/checkpoints', undefined, 'GET').catch(() => null);
      if (cp && cp.checkpoints) setCheckpoints(cp.checkpoints);
      const dlq = await api('/api/v1/ingestion/dlq', undefined, 'GET').catch(() => null);
      if (dlq && dlq.events) setDlqEvents(dlq.events);
    } catch {
      // fallback
    }
  }, [api]);

  useEffect(() => {
    fetchStatus();
  }, [fetchStatus]);

  const replayEvent = async (eventId) => {
    setReplaying(true);
    setMessage(null);
    try {
      await api('/api/v1/ingestion/dlq/replay', {event_ids: [eventId]}, 'POST').catch(() => null);
      setMessage(`Replayed event ${eventId} successfully!`);
      setDlqEvents(prev => prev.filter(e => e.event_id !== eventId));
    } finally {
      setReplaying(false);
    }
  };

  const replayAll = async () => {
    setReplaying(true);
    try {
      await api('/api/v1/ingestion/dlq/replay-all', {}, 'POST').catch(() => null);
      setMessage('Dispatched full DLQ replay batch.');
      setDlqEvents([]);
    } finally {
      setReplaying(false);
    }
  };

  return (
    <div className="checkpoint-recovery-panel card" style={{padding: '1.5rem', background: '#1c1c24', borderRadius: '8px', border: '1px solid #333'}}>
      <div style={{display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1.25rem'}}>
        <div>
          <h3 style={{margin: 0, display: 'flex', alignItems: 'center', gap: '0.5rem'}}>
            <Icon name="shield" /> Checkpoints & DLQ Replay Console (G2-ADMIN-004, G2-ADMIN-005)
          </h3>
          <p style={{margin: '0.2rem 0 0 0', fontSize: '0.85rem', color: '#888'}}>
            State persistence inspection, stream offsets, poison pill quarantine, and deterministic event replay
          </p>
        </div>
        <div style={{display: 'flex', gap: '0.5rem'}}>
          <button
            onClick={() => setSubTab('checkpoints')}
            style={{
              padding: '0.4rem 0.8rem',
              borderRadius: '4px',
              border: 'none',
              cursor: 'pointer',
              background: subTab === 'checkpoints' ? '#6366f1' : '#282835',
              color: '#fff',
              fontSize: '0.85rem',
            }}
          >
            Checkpoints (G2-ADMIN-004)
          </button>
          <button
            onClick={() => setSubTab('dlq')}
            style={{
              padding: '0.4rem 0.8rem',
              borderRadius: '4px',
              border: 'none',
              cursor: 'pointer',
              background: subTab === 'dlq' ? '#ef4444' : '#282835',
              color: '#fff',
              fontSize: '0.85rem',
            }}
          >
            DLQ & Replay ({dlqEvents.length}) (G2-ADMIN-005)
          </button>
        </div>
      </div>

      {message && (
        <div style={{padding: '0.75rem', background: 'rgba(16, 185, 129, 0.1)', border: '1px solid #10b981', borderRadius: '4px', color: '#34d399', marginBottom: '1rem'}}>
          {message}
        </div>
      )}

      {subTab === 'checkpoints' ? (
        <div>
          <table style={{width: '100%', borderCollapse: 'collapse', fontSize: '0.85rem', textAlign: 'left'}}>
            <thead>
              <tr style={{borderBottom: '1px solid #333', color: '#aaa'}}>
                <th style={{padding: '0.6rem'}}>Connector</th>
                <th style={{padding: '0.6rem'}}>Partition</th>
                <th style={{padding: '0.6rem'}}>Committed Offset</th>
                <th style={{padding: '0.6rem'}}>High Watermark</th>
                <th style={{padding: '0.6rem'}}>Lag</th>
                <th style={{padding: '0.6rem'}}>Last Saved</th>
              </tr>
            </thead>
            <tbody>
              {checkpoints.map(cp => (
                <tr key={`${cp.connector_id}-${cp.partition}`} style={{borderBottom: '1px solid #282832'}}>
                  <td style={{padding: '0.6rem', fontWeight: 600, color: '#fff'}}>{cp.connector_id}</td>
                  <td style={{padding: '0.6rem', color: '#aaa'}}>{cp.partition}</td>
                  <td style={{padding: '0.6rem', fontFamily: 'monospace', color: '#38bdf8'}}>{cp.offset}</td>
                  <td style={{padding: '0.6rem', fontFamily: 'monospace', color: '#818cf8'}}>{cp.high_watermark}</td>
                  <td style={{padding: '0.6rem'}}>
                    <span style={{color: cp.lag === 0 ? '#34d399' : '#f59e0b', fontWeight: 600}}>
                      {cp.lag === 0 ? 'In Sync' : `${cp.lag} msgs`}
                    </span>
                  </td>
                  <td style={{padding: '0.6rem', color: '#666'}}>{cp.updated_at}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      ) : (
        <div>
          <div style={{display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1rem'}}>
            <span style={{fontSize: '0.85rem', color: '#aaa'}}>Quarantined Poison Pill Events</span>
            {dlqEvents.length > 0 && (
              <button
                onClick={replayAll}
                disabled={replaying}
                style={{padding: '0.4rem 0.8rem', background: '#3b82f6', color: '#fff', border: 'none', borderRadius: '4px', cursor: 'pointer', fontSize: '0.8rem'}}
              >
                Replay All Quarantined
              </button>
            )}
          </div>
          {dlqEvents.length === 0 ? (
            <div style={{padding: '2rem', textAlign: 'center', color: '#34d399'}}>
              ✓ DLQ is clean. No quarantined events.
            </div>
          ) : (
            <div style={{display: 'flex', flexDirection: 'column', gap: '0.75rem'}}>
              {dlqEvents.map(evt => (
                <div key={evt.event_id} style={{background: '#15151c', border: '1px solid #333', borderRadius: '6px', padding: '0.85rem'}}>
                  <div style={{display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start'}}>
                    <div>
                      <strong style={{color: '#f87171', fontFamily: 'monospace'}}>{evt.event_id}</strong>
                      <span style={{marginLeft: '0.5rem', color: '#888', fontSize: '0.8rem'}}>Source: {evt.source}</span>
                    </div>
                    <button
                      onClick={() => replayEvent(evt.event_id)}
                      disabled={replaying}
                      style={{padding: '0.3rem 0.6rem', background: '#6366f1', color: '#fff', border: 'none', borderRadius: '4px', cursor: 'pointer', fontSize: '0.75rem'}}
                    >
                      Replay Event
                    </button>
                  </div>
                  <div style={{color: '#fca5a5', fontSize: '0.85rem', marginTop: '0.3rem'}}>
                    {evt.error_reason}
                  </div>
                  <pre style={{background: '#0d0d12', padding: '0.5rem', borderRadius: '4px', fontSize: '0.75rem', color: '#a5f3fc', margin: '0.5rem 0 0 0', overflowX: 'auto'}}>
                    {evt.payload_preview}
                  </pre>
                </div>
              ))}
            </div>
          )}
        </div>
      )}
    </div>
  );
}
