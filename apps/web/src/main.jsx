import React, {useEffect, useRef, useState} from 'react';
import {createRoot} from 'react-dom/client';
import cytoscape from 'cytoscape';
import './style.css';

function safeClass(name) {
  return String(name).toLowerCase().replace(/[^a-z0-9]/g, '');
}

function GraphCanvas({elements, selectedId, onSelect}) {
  const containerRef = useRef(null);
  const cyRef = useRef(null);

  useEffect(() => {
    const cy = cytoscape({
      container: containerRef.current,
      elements,
      minZoom: 0.2,
      maxZoom: 3,
      wheelSensitivity: 0.3,
      style: [
        {
          selector: 'node',
          style: {
            'background-color': '#9db3c2',
            'label': 'data(label)',
            'color': '#263e4e',
            'font-size': '11px',
            'text-valign': 'center',
            'text-halign': 'center',
            'width': '42px',
            'height': '42px',
            'border-width': 0,
            'border-color': '#0b766b',
            'text-wrap': 'wrap',
            'text-max-width': '80px',
          },
        },
        {
          selector: 'node.workitem',
          style: {'background-color': '#0b766b', 'color': '#fff'},
        },
        {
          selector: 'node.commit',
          style: {'background-color': '#2563eb'},
        },
        {
          selector: 'node.file',
          style: {'background-color': '#708392'},
        },
        {
          selector: 'node.codesymbol',
          style: {'background-color': '#16a34a'},
        },
        {
          selector: 'node:selected, node.selected',
          style: {
            'border-width': '4px',
            'border-color': '#0b766b',
            'border-opacity': 1,
          },
        },
        {
          selector: 'edge',
          style: {
            'width': 1.5,
            'line-color': '#698090',
            'target-arrow-color': '#698090',
            'target-arrow-shape': 'triangle',
            'curve-style': 'bezier',
            'label': 'data(label)',
            'font-size': '9px',
            'color': '#617586',
            'text-background-color': '#fff',
            'text-background-opacity': 0.85,
            'text-background-shape': 'roundrectangle',
            'text-background-padding': '2px',
          },
        },
      ],
    });

    cy.on('tap', 'node', event => {
      const node = event.target;
      onSelect({id: node.id(), label: node.data('originLabel'), properties: node.data('originProperties') || {}});
    });

    cyRef.current = cy;
    return () => {
      cy.destroy();
      cyRef.current = null;
    };
  }, []);

  useEffect(() => {
    const cy = cyRef.current;
    if (!cy) return;
    cy.elements().remove();
    if (elements.length) {
      cy.add(elements);
      try {
        cy.layout({name: 'cose', padding: 20, animate: false, componentSpacing: 80, nodeOverlap: 20}).run();
      } catch {
        cy.layout({name: 'grid', padding: 20}).run();
      }
      cy.fit(undefined, 25);
    }
  }, [elements]);

  useEffect(() => {
    const cy = cyRef.current;
    if (!cy) return;
    cy.nodes().removeClass('selected');
    if (selectedId) {
      const node = cy.getElementById(selectedId);
      if (node.length) {
        node.addClass('selected');
        node.select();
      }
    }
  }, [selectedId]);

  const relationshipTypes = [...new Set(elements.filter(element => element.data.source).map(element => element.data.label))];
  return <div ref={containerRef} className="graph-canvas" role="img" aria-label={`Knowledge graph. Relationship types: ${relationshipTypes.join(', ') || 'none'}.`}/>;
}

function App() {
  const [token, setToken] = useState(sessionStorage.getItem('eoip-token') || '');
  const [authenticated, setAuthenticated] = useState(false);
  const [mode, setMode] = useState(location.pathname.startsWith('/admin') ? 'admin' : 'app');
  const [query, setQuery] = useState('EOIP-1');
  const [graph, setGraph] = useState({nodes: [], edges: []});
  const [selected, setSelected] = useState(null);
  const [detail, setDetail] = useState(null);
  const [stats, setStats] = useState(null);
  const [jobs, setJobs] = useState([]);
  const [validation, setValidation] = useState(null);
  const [trace, setTrace] = useState(null);
  const [source, setSource] = useState('urn:eoip:work:item:jira:EOIP-1');
  const [target, setTarget] = useState('');
  const [error, setError] = useState('');
  const [busy, setBusy] = useState(false);
  const [upload, setUpload] = useState(null);

  async function api(path, body) {
    const response = await fetch(path, {method: body === undefined ? 'GET' : 'POST', headers: {'Authorization': `Bearer ${token}`, ...(body !== undefined ? {'Content-Type': 'application/json'} : {})}, ...(body !== undefined ? {body: JSON.stringify(body)} : {})});
    const data = await response.json();
    if (!response.ok) throw new Error(typeof data.detail === 'string' ? data.detail : `Request failed (${response.status})`);
    return data;
  }
  async function run(action) {
    setBusy(true); setError('');
    try { await action(); } catch (e) { setError(e.message); } finally { setBusy(false); }
  }
  async function refresh() { const [s, j] = await Promise.all([api('/api/v1/admin/stats'), api('/api/v1/admin/jobs')]); setStats(s); setJobs(j); }
  async function login(e) { e.preventDefault(); await run(async () => { await refresh(); sessionStorage.setItem('eoip-token', token); setAuthenticated(true); setGraph(await api('/api/v1/search?q=EOIP-1')); }); }
  useEffect(() => { if (!authenticated) return; const timer = setInterval(() => { refresh().catch(e => setError(e.message)); }, 10000); return () => clearInterval(timer); }, [authenticated, token]);
  async function inspect(node) { setSelected(node); setTarget(node.id); setDetail(await api(`/api/v1/entities/${encodeURIComponent(node.id)}`)); }
  function navigation(value) { setMode(value); history.pushState({}, '', `/${value}`); }
  const nodes = graph.nodes || [];
  const jobSummary = job => { const r = job.result; return job.kind === 'DEMO' ? `${r.jira?.records_accepted || 0} Jira records · ${r.git?.files || 0} files · ${r.git?.symbols || 0} symbols` : `${r.records_accepted || 0} accepted · ${r.records_rejected || 0} rejected`; };
  const label = n => n.properties?.issue_key || n.properties?.name || n.properties?.qualified_name || n.properties?.path || n.label;

  const cyElements = [
    ...nodes.map(n => ({
      data: {
        id: n.id,
        label: label(n).slice(0, 34),
        originLabel: n.label,
        originProperties: n.properties,
      },
      classes: safeClass(n.label),
    })),
    ...(graph.edges || []).map(e => ({
      data: {
        id: e.id,
        source: e.from_id,
        target: e.to_id,
        label: e.type,
      },
    })),
  ];

  return <div className="layout">
    <aside><div className="brand"><span className="brand-icon">E</span> EOIP</div><div className="small muted">ENTERPRISE INTELLIGENCE</div><nav><button className={mode === 'app' ? 'active' : ''} onClick={() => navigation('app')}>◉ Knowledge explorer</button><button className={mode === 'admin' ? 'active' : ''} onClick={() => navigation('admin')}>▦ Administration</button></nav><div className="aside-bottom"><span className="dot"/> Local Docker deployment<br/><span className="muted">Evidence from your persisted graph</span></div></aside>
    <main><header><div><div className="small muted">WORKSPACE / {mode === 'app' ? 'EXPLORER' : 'ADMINISTRATION'}</div><h1>{mode === 'app' ? 'Connect requirements to code.' : 'Your knowledge graph, in operation.'}</h1><p className="muted">{mode === 'app' ? 'Search, trace relationships, and inspect the evidence behind every connection.' : 'Ingest sources and inspect live graph counts, job results, and validation findings.'}</p></div><a href="http://localhost:8000/docs" target="_blank" rel="noreferrer">API docs ↗</a></header>
    {error && <div role="alert" className="error">{error}</div>}
    {!authenticated ? <section className="panel login"><h2>Connect to your local system</h2><p>Enter the EOIP_API_TOKEN from <code>eoip/deploy/.env</code>.</p><form onSubmit={login}><label htmlFor="token">Access token</label><input id="token" type="password" autoComplete="off" value={token} onChange={e => setToken(e.target.value)} required/><button disabled={busy}>Connect</button></form></section> : <>
      <div className="metrics"><div><span className="muted">ENTITIES</span><strong>{stats?.vertices ?? '—'}</strong></div><div><span className="muted">RELATIONSHIPS</span><strong>{stats?.edges ?? '—'}</strong></div><div><span className="muted">GRAPH STORAGE</span><strong>HugeGraph</strong></div><div><span className="muted">WORKER</span><strong>{stats?.worker?.status || 'starting'}</strong></div></div>
      {mode === 'app' ? <>
        <form className="search" onSubmit={e => {e.preventDefault(); run(async () => {setGraph(await api(`/api/v1/search?q=${encodeURIComponent(query)}`)); setSelected(null); setTrace(null);});}}><input aria-label="Search knowledge graph" value={query} onChange={e => setQuery(e.target.value)} placeholder="Issue key, symbol, commit, or path…" required/><button disabled={busy}>Search graph</button></form>
        <div className="explorer"><section className="panel"><div className="panel-top"><h2>Relationship map</h2><span className="badge">{nodes.length} entities</span></div>
          <GraphCanvas elements={cyElements} selectedId={selected?.id} onSelect={node => run(() => inspect(node))}/>
          {graph.partial && <p className="muted">Results are bounded. Some connected entities are outside the current limits.</p>}<div className="entity-list">{nodes.map(n => <button key={n.id} onClick={() => run(() => inspect(n))}><span className="badge">{n.label}</span> {label(n)}</button>)}</div></section>
          <section className="panel detail"><h2>{selected ? label(selected) : 'Inspect an entity'}</h2>{selected ? <><span className="badge">{selected.label}</span><code className="identity">{selected.id}</code><button disabled={busy} onClick={() => run(async () => {setGraph(await api('/api/v1/impact', {canonical_id: selected.id, max_depth: 4}));})}>Explore impact</button><button className="secondary" disabled={busy} onClick={() => run(async () => setTrace(await api('/api/v1/agents/trace-impact', {canonical_id: selected.id})))}>Run TraceImpact</button><h3>Properties</h3><dl>{Object.entries(selected.properties || {}).map(([k, v]) => <div key={k}><dt>{k.replaceAll('_', ' ')}</dt><dd>{String(v)}</dd></div>)}</dl><h3>Source evidence</h3>{(detail?.outgoing || []).filter(e => e.properties?.source_ref).map(e => <p className="evidence" key={e.eid}><strong>{e.label}</strong><br/>{e.properties.source_ref}<br/><span className="muted">{e.properties.evidence_key}</span></p>)}</> : <p className="muted">Select an entity on the map or in the result list to see its properties and source references.</p>}</section></div>
        <section className="panel"><h2>Trace a requirement to implementation</h2><form className="trace-form" onSubmit={e => {e.preventDefault(); run(async () => setGraph(await api('/api/v1/path', {source_id: source, target_id: target})));}}><label>From canonical ID<input value={source} onChange={e => setSource(e.target.value)} required/></label><label>To canonical ID<input value={target} onChange={e => setTarget(e.target.value)} required placeholder="Select a code symbol above"/></label><button disabled={busy}>Find path</button></form></section>
        {trace && <section className="panel"><h2>TraceImpact result</h2><p>{trace.summary}</p><p className="muted">Deterministic graph traversal · {trace.evidence_refs.length} source references</p>{trace.evidence_refs.map(ref => <p className="evidence" key={ref}>{ref}</p>)}</section>}
      </> : <>
        <section className="panel"><div className="panel-top"><h2>Source ingestion</h2><button className="secondary" disabled={busy} onClick={() => run(refresh)}>Refresh counts</button></div><p className="muted">Demo ingestion captures source events, parses a Git repository, and writes evidence to HugeGraph.</p><div className="actions"><button disabled={busy} onClick={() => run(async () => {await api('/api/v1/admin/demo', {}); await refresh();})}>Load / replay demo</button><label className="file-label">Jira JSON<input type="file" accept="application/json,.json" onChange={e => setUpload(e.target.files?.[0])}/></label><button disabled={busy || !upload} onClick={() => run(async () => {if (upload.size > 3_000_000) throw new Error('Select a JSON file smaller than 3 MB'); await api('/api/v1/admin/ingestion/jira', {document: JSON.parse(await upload.text())}); await refresh();})}>Import Jira file</button></div></section>
        <section className="panel"><h2>Ingestion jobs</h2><table><thead><tr><th>Source</th><th>Status</th><th>Created</th><th>Details</th></tr></thead><tbody>{jobs.map(j => <tr key={j.job_id}><td>{j.kind}</td><td><span className="badge">{j.status}</span></td><td>{new Date(j.created_at).toLocaleString()}</td><td>{j.error || (j.result ? jobSummary(j) : 'Waiting for worker')}</td></tr>)}</tbody></table></section>
        <section className="panel"><div className="panel-top"><h2>Graph validation</h2><button disabled={busy} onClick={() => run(async () => setValidation(await api('/api/v1/admin/validation', {})))}>Run validation</button></div>{validation && <><p>{validation.valid ? 'No findings in the checked graph.' : `${validation.findings.length} findings`} Checked {validation.vertices_checked} entities and {validation.edges_checked} relationships.</p><pre>{JSON.stringify(validation.findings, null, 2)}</pre></>}</section>
        <section className="panel"><h2>Entity inventory</h2><div className="inventory">{Object.entries(stats?.labels || {}).map(([key, value]) => <div key={key}><span>{key}</span><strong>{value}</strong></div>)}</div></section>
      </>}
      <footer><span>EOIP · Local enterprise intelligence</span><button className="text-button" onClick={() => {sessionStorage.removeItem('eoip-token'); setToken(''); setAuthenticated(false);}}>Disconnect</button></footer>
    </>}
    </main></div>;
}

createRoot(document.getElementById('root')).render(<App/>);
