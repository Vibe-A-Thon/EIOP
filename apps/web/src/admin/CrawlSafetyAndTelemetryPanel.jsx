import React, {useState} from 'react';
import {Icon} from '../icons.jsx';

export default function CrawlSafetyAndTelemetryPanel({api}) {
  const [subTab, setSubTab] = useState('mapping_preview');
  const [allowlistUrls, setAllowlistUrls] = useState('https://jira.corp.internal/*\nhttps://gitlab.corp.internal/*\nhttps://wiki.corp.internal/*');
  const [maxContentSizeMb, setMaxContentSizeMb] = useState(10);
  const [maxCrawlDepth, setMaxCrawlDepth] = useState(4);
  const [ssrfEnforced, setSsrfEnforced] = useState(true);
  const [otelAggWindow, setOtelAggWindow] = useState(60);
  const [sampleRate, setSampleRate] = useState(100);

  return (
    <div className="crawl-telemetry-panel card" style={{padding: '1.5rem', background: '#1c1c24', borderRadius: '8px', border: '1px solid #333'}}>
      <div style={{display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1.25rem'}}>
        <div>
          <h3 style={{margin: 0, display: 'flex', alignItems: 'center', gap: '0.5rem'}}>
            <Icon name="shield" /> Mapping Preview, Crawl Safety & Telemetry (G2-ADMIN-011, 012, 013)
          </h3>
          <p style={{margin: '0.2rem 0 0 0', fontSize: '0.85rem', color: '#888'}}>
            Source-to-ontology preview, strict target allowlists, SSRF guardrails, and OpenTelemetry semantic extraction
          </p>
        </div>
        <div style={{display: 'flex', gap: '0.5rem'}}>
          <button
            onClick={() => setSubTab('mapping_preview')}
            style={{
              padding: '0.4rem 0.8rem',
              borderRadius: '4px',
              border: 'none',
              cursor: 'pointer',
              background: subTab === 'mapping_preview' ? '#6366f1' : '#282835',
              color: '#fff',
              fontSize: '0.85rem',
            }}
          >
            Mapping Preview (G2-ADMIN-011)
          </button>
          <button
            onClick={() => setSubTab('safety')}
            style={{
              padding: '0.4rem 0.8rem',
              borderRadius: '4px',
              border: 'none',
              cursor: 'pointer',
              background: subTab === 'safety' ? '#10b981' : '#282835',
              color: '#fff',
              fontSize: '0.85rem',
            }}
          >
            Crawl Safety & SSRF (G2-ADMIN-012)
          </button>
          <button
            onClick={() => setSubTab('telemetry')}
            style={{
              padding: '0.4rem 0.8rem',
              borderRadius: '4px',
              border: 'none',
              cursor: 'pointer',
              background: subTab === 'telemetry' ? '#f59e0b' : '#282835',
              color: '#fff',
              fontSize: '0.85rem',
            }}
          >
            Telemetry Extraction (G2-ADMIN-013)
          </button>
        </div>
      </div>

      {subTab === 'mapping_preview' && (
        <div style={{display: 'flex', flexDirection: 'column', gap: '1rem'}}>
          <div style={{display: 'grid', gridTemplateColumns: '1fr 60px 1fr', gap: '1rem', alignItems: 'center'}}>
            <div style={{background: '#15151c', border: '1px solid #333', borderRadius: '6px', padding: '1rem'}}>
              <h4 style={{margin: '0 0 0.5rem 0', color: '#60a5fa'}}>Source Event: Jira Payload</h4>
              <pre style={{margin: 0, fontSize: '0.75rem', color: '#a5f3fc', background: '#0e0e14', padding: '0.75rem', borderRadius: '4px', overflowX: 'auto'}}>
{`{
  "id": "10492",
  "key": "CORE-104",
  "fields": {
    "summary": "Fix authentication timeout",
    "status": {"name": "In Progress"},
    "assignee": {"displayName": "Alice Smith"}
  }
}`}
              </pre>
            </div>
            <div style={{textAlign: 'center', fontSize: '1.5rem', color: '#6366f1'}}>➔</div>
            <div style={{background: '#15151c', border: '1px solid #333', borderRadius: '6px', padding: '1rem'}}>
              <h4 style={{margin: '0 0 0.5rem 0', color: '#34d399'}}>Ontology Entity: WorkItem</h4>
              <pre style={{margin: 0, fontSize: '0.75rem', color: '#86efac', background: '#0e0e14', padding: '0.75rem', borderRadius: '4px', overflowX: 'auto'}}>
{`{
  "label": "WorkItem",
  "canonical_id": "CORE-104",
  "properties": {
    "issue_key": "CORE-104",
    "summary": "Fix authentication timeout",
    "status": "In Progress"
  },
  "edges": [
    {"label": "ASSIGNED_TO", "target": "Person:Alice Smith"}
  ]
}`}
              </pre>
            </div>
          </div>
        </div>
      )}

      {subTab === 'safety' && (
        <div style={{display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '1.5rem'}}>
          <div style={{background: '#15151c', padding: '1rem', borderRadius: '6px', border: '1px solid #333'}}>
            <h4 style={{margin: '0 0 0.5rem 0'}}>Strict Target Allowlist</h4>
            <p style={{fontSize: '0.8rem', color: '#aaa', margin: '0 0 0.5rem 0'}}>Crawlers are blocked from accessing any destination outside explicit allowlist.</p>
            <textarea
              rows={5}
              value={allowlistUrls}
              onChange={e => setAllowlistUrls(e.target.value)}
              style={{width: '100%', padding: '0.5rem', background: '#0e0e14', border: '1px solid #444', color: '#fff', borderRadius: '4px', fontFamily: 'monospace', fontSize: '0.8rem'}}
            />
          </div>
          <div style={{background: '#15151c', padding: '1rem', borderRadius: '6px', border: '1px solid #333', display: 'flex', flexDirection: 'column', gap: '0.8rem'}}>
            <h4 style={{margin: '0 0 0.5rem 0'}}>SSRF & Scope Protection Rules</h4>
            <label style={{display: 'flex', alignItems: 'center', gap: '0.5rem', fontSize: '0.85rem', color: '#ddd'}}>
              <input type="checkbox" checked={ssrfEnforced} onChange={e => setSsrfEnforced(e.target.checked)} />
              Enforce Anti-SSRF (Block 127.0.0.1, 169.254.169.254, RFC1918)
            </label>
            <div>
              <label style={{display: 'block', fontSize: '0.8rem', color: '#aaa'}}>Max Document Download Size: {maxContentSizeMb} MB</label>
              <input type="range" min="1" max="50" value={maxContentSizeMb} onChange={e => setMaxContentSizeMb(parseInt(e.target.value, 10))} style={{width: '100%'}} />
            </div>
            <div>
              <label style={{display: 'block', fontSize: '0.8rem', color: '#aaa'}}>Max Crawl Graph Depth: {maxCrawlDepth} hops</label>
              <input type="range" min="1" max="10" value={maxCrawlDepth} onChange={e => setMaxCrawlDepth(parseInt(e.target.value, 10))} style={{width: '100%'}} />
            </div>
          </div>
        </div>
      )}

      {subTab === 'telemetry' && (
        <div style={{display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '1.5rem'}}>
          <div style={{background: '#15151c', padding: '1rem', borderRadius: '6px', border: '1px solid #333'}}>
            <h4 style={{margin: '0 0 0.5rem 0'}}>Semantic Observation Windows</h4>
            <p style={{fontSize: '0.8rem', color: '#aaa'}}>Store bounded semantic relationships rather than unlimited raw metrics.</p>
            <div style={{marginTop: '1rem'}}>
              <label style={{display: 'block', fontSize: '0.8rem', color: '#aaa'}}>Aggregation Window: <strong>{otelAggWindow}s</strong></label>
              <input type="range" min="10" max="300" step="10" value={otelAggWindow} onChange={e => setOtelAggWindow(parseInt(e.target.value, 10))} style={{width: '100%'}} />
            </div>
            <div style={{marginTop: '1rem'}}>
              <label style={{display: 'block', fontSize: '0.8rem', color: '#aaa'}}>Trace Sample Rate: <strong>{sampleRate}%</strong></label>
              <input type="range" min="1" max="100" value={sampleRate} onChange={e => setSampleRate(parseInt(e.target.value, 10))} style={{width: '100%'}} />
            </div>
          </div>
          <div style={{background: '#15151c', padding: '1rem', borderRadius: '6px', border: '1px solid #333'}}>
            <h4 style={{margin: '0 0 0.5rem 0'}}>Edge Expiration Policy</h4>
            <p style={{fontSize: '0.8rem', color: '#aaa'}}>Runtime communication edges automatically decay and expire when not re-observed within 24 hours.</p>
            <div style={{padding: '0.75rem', background: '#0e0e14', borderRadius: '4px', fontSize: '0.8rem', color: '#34d399', border: '1px solid #2a2a35'}}>
              ✓ Automatic TTL decay enabled for CALLS, SENDS_TO, and QUERIES runtime edges.
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
