import React, {useEffect, useState} from 'react';
import GraphCanvas, {palette} from './GraphCanvas.jsx';
import {Icon, Tip} from './icons.jsx';

const emptyGraph = {nodes: [], edges: [], paths: [], evidence: [], warnings: [], partial: false};
const lenses = [
  {id: 'graph', label: 'Graph', icon: 'graph', hint: 'Explore connected enterprise knowledge'},
  {id: 'impact', label: 'Impact', icon: 'activity', hint: 'Trace the blast radius of a change'},
  {id: 'evidence', label: 'Evidence', icon: 'shield', hint: 'Inspect provenance and GraphRAG context'},
];

function displayLabel(node) {
  return node?.properties?.issue_key || node?.properties?.display_name || node?.properties?.name || node?.properties?.qualified_name || node?.properties?.path || node?.label || 'Unknown entity';
}

function shortId(value, size = 22) {
  if (!value) return '—';
  return value.length > size ? `${value.slice(0, size - 1)}…` : value;
}

function formatTime(value) {
  if (!value) return 'Not available';
  const date = new Date(value);
  return Number.isNaN(date.getTime()) ? String(value) : date.toLocaleString();
}

function IconButton({label, icon, onClick, className = '', disabled = false}) {
  return <Tip text={label}><button type="button" className={`icon-button ${className}`} aria-label={label} onClick={onClick} disabled={disabled}><Icon name={icon}/></button></Tip>;
}

function StatusPill({status = 'UNKNOWN'}) {
  const normalized = String(status).toLowerCase();
  const positive = ['ready', 'running', 'succeeded', 'passed', 'ok', 'complete'].some(word => normalized.includes(word));
  const negative = ['failed', 'error', 'denied'].some(word => normalized.includes(word));
  return <span className={`status-pill ${positive ? 'positive' : negative ? 'negative' : 'neutral'}`}><span className="status-dot"/>{String(status).replaceAll('_', ' ')}</span>;
}

function EmptyState({icon = 'search', title, children}) {
  return <div className="empty-state"><span className="empty-icon"><Icon name={icon} size={22}/></span><strong>{title}</strong><p>{children}</p></div>;
}

function MetricCard({icon, eyebrow, value, caption, tone = 'violet', tooltip}) {
  return <Tip text={tooltip || caption} className="metric-tip"><article className={`metric-card tone-${tone}`} tabIndex="0">
    <span className="metric-icon"><Icon name={icon} size={20}/></span>
    <div><span className="eyebrow">{eyebrow}</span><strong>{value}</strong><small>{caption}</small></div>
  </article></Tip>;
}

function QualityRing({label, value, tone = 'violet'}) {
  const percentage = Math.max(0, Math.min(100, Math.round((value ?? 0) * 100)));
  return <Tip text={`${label}: ${percentage}% of checked graph facts`}><div className="quality-ring-card" tabIndex="0">
    <div className={`quality-ring ${tone}`} style={{'--score': `${percentage * 3.6}deg`}}><span>{percentage}%</span></div>
    <div><strong>{label}</strong><small>Latest validation run</small></div>
  </div></Tip>;
}

function Login({token, setToken, onSubmit, busy, health}) {
  return <div className="login-page">
    <section className="login-story">
      <span className="product-mark large"><span className="mark-core">E</span><span className="mark-orbit"/></span>
      <div className="kicker"><span/>ENTERPRISE KNOWLEDGE INTELLIGENCE</div>
      <h1>See how every decision<br/>connects to delivery.</h1>
      <p>Trace requirements, code, builds, evidence, and operational knowledge through one trusted, local-first graph.</p>
      <div className="login-feature-grid">
        <div><Icon name="graph"/><span><strong>Connected context</strong><small>Navigate typed relationships</small></span></div>
        <div><Icon name="shield"/><span><strong>Evidence first</strong><small>Explain every material link</small></span></div>
        <div><Icon name="database"/><span><strong>Local by design</strong><small>Your graph stays on premises</small></span></div>
      </div>
    </section>
    <section className="login-card" aria-labelledby="login-title">
      <div className="login-card-top"><span className={`health-orb ${health === 'ready' ? 'online' : ''}`}/><span>{health === 'ready' ? 'Local services are ready' : health === 'checking' ? 'Checking local services…' : 'Local service status unavailable'}</span></div>
      <div className="login-card-body">
        <span className="section-icon"><Icon name="link"/></span>
        <h2 id="login-title">Connect your workspace</h2>
        <p>Use the local API access token generated for this deployment.</p>
        <form onSubmit={onSubmit}>
          <label htmlFor="token">Access token <Tip text="Find EOIP_API_TOKEN in the generated deploy/.env file"><span className="help-dot">?</span></Tip></label>
          <div className="input-with-icon"><Icon name="shield" size={17}/><input id="token" type="password" autoComplete="current-password" value={token} onChange={event => setToken(event.target.value)} placeholder="Paste EOIP_API_TOKEN" required/></div>
          <button className="primary-button wide" disabled={busy} title="Authenticate with the local EOIP API">{busy ? <><span className="spinner small"/>Connecting…</> : <>Enter workspace <Icon name="arrow" size={17}/></>}</button>
        </form>
        <div className="local-note"><Icon name="shield" size={15}/><span>Your token is stored only in this browser tab and is never sent outside the local deployment.</span></div>
      </div>
    </section>
  </div>;
}

function Sidebar({mode, onNavigate, collapsed, onToggle, stats}) {
  const items = [
    {id: 'app', label: 'Knowledge explorer', icon: 'search', hint: 'Search, traverse, and explain the enterprise graph'},
    {id: 'admin', label: 'Administration', icon: 'settings', hint: 'Operate ingestion, quality, audit, and ontology services'},
  ];
  return <aside className={`sidebar ${collapsed ? 'collapsed' : ''}`}>
    <div className="brand-row"><span className="product-mark"><span className="mark-core">E</span><span className="mark-orbit"/></span><span className="brand-copy"><strong>EOIP</strong><small>Knowledge intelligence</small></span><IconButton label={collapsed ? 'Expand navigation' : 'Collapse navigation'} icon="menu" onClick={onToggle}/></div>
    <div className="nav-label">WORKSPACE</div>
    <nav aria-label="Primary navigation">{items.map(item => <Tip text={item.hint} key={item.id}><button className={mode === item.id ? 'active' : ''} onClick={() => onNavigate(item.id)} aria-current={mode === item.id ? 'page' : undefined}><Icon name={item.icon}/><span>{item.label}</span>{mode === item.id && <i/>}</button></Tip>)}</nav>
    <div className="sidebar-card"><span className="sidebar-card-icon"><Icon name="database"/></span><div><strong>HugeGraph</strong><small>{stats ? `${stats.vertices} entities indexed` : 'Authoritative graph'}</small></div><span className="live-dot"/></div>
    <div className="sidebar-footer"><div className="deployment"><span className="live-dot"/><span><strong>Local deployment</strong><small>No cloud dependency</small></span></div><span className="version">v0.1</span></div>
  </aside>;
}

function Topbar({mode, stats, onRefresh, onDisconnect, busy}) {
  return <header className="topbar"><div><span className="breadcrumb">WORKSPACE <Icon name="chevron" size={12}/> {mode === 'app' ? 'KNOWLEDGE EXPLORER' : 'ADMINISTRATION'}</span><h1>{mode === 'app' ? 'Enterprise knowledge explorer' : 'Operations control center'}</h1></div><div className="topbar-actions">
    <Tip text="Live status reported by the local worker"><div className="service-status"><span className="live-dot"/><span><small>SYSTEM STATUS</small><strong>{stats?.worker?.status || 'Connecting'}</strong></span></div></Tip>
    <IconButton label="Refresh live data" icon="refresh" onClick={onRefresh} disabled={busy}/>
    <Tip text="Open the local OpenAPI reference"><a className="icon-button" href="http://localhost:8000/docs" target="_blank" rel="noreferrer" aria-label="Open API documentation"><Icon name="code"/></a></Tip>
    <IconButton label="Disconnect this browser session" icon="logout" onClick={onDisconnect}/>
  </div></header>;
}

function GraphLegend({nodes}) {
  const types = [...new Set(nodes.map(node => node.label))];
  return types.length ? <div className="graph-legend" aria-label="Entity type legend">{types.map(type => <Tip text={`${type} entity`} key={type}><span><i style={{background: palette[type] || '#64748b'}}/>{type}</span></Tip>)}</div> : null;
}

function EntityInspector({selected, detail, selectedEdge, onImpact, onTrace, onLineage, busy}) {
  const [tab, setTab] = useState('overview');
  useEffect(() => setTab('overview'), [selected?.id, selectedEdge?.id]);
  if (selectedEdge) return <section className="inspector panel" aria-label="Relationship inspector"><div className="inspector-heading"><span className="entity-symbol edge"><Icon name="link"/></span><div><span className="eyebrow">RELATIONSHIP</span><h2>{selectedEdge.type}</h2></div></div><div className="edge-route"><code title={selectedEdge.from_id}>{shortId(selectedEdge.from_id)}</code><span><Icon name="arrow" size={15}/></span><code title={selectedEdge.to_id}>{shortId(selectedEdge.to_id)}</code></div><h3>Why does this edge exist?</h3>{selectedEdge.properties?.source_ref || selectedEdge.properties?.evidence_key ? <div className="evidence-card"><Icon name="shield"/><div><strong>{selectedEdge.properties.source_ref || 'Graph evidence'}</strong><small>{selectedEdge.properties.evidence_key || 'Evidence key unavailable'}</small></div></div> : <p className="subtle">No direct evidence reference was returned for this relationship.</p>}<dl className="property-list">{Object.entries(selectedEdge.properties || {}).map(([key, value]) => <div key={key}><dt>{key.replaceAll('_', ' ')}</dt><dd>{String(value)}</dd></div>)}</dl></section>;
  if (!selected) return <section className="inspector panel"><EmptyState icon="focus" title="Select an entity">Choose a node on the map or an item in the result list to inspect its identity, properties, and evidence.</EmptyState></section>;
  const evidenceEdges = [...(detail?.outgoing || []), ...(detail?.incoming || [])].filter(edge => edge.properties?.source_ref || edge.properties?.evidence_key);
  return <section className="inspector panel" aria-label="Entity inspector"><div className="inspector-heading"><span className="entity-symbol" style={{'--entity-color': palette[selected.label] || '#64748b'}}>{displayLabel(selected).slice(0, 1).toUpperCase()}</span><div><span className="eyebrow">{selected.label}</span><h2>{displayLabel(selected)}</h2></div></div><div className="inspector-tabs" role="tablist"><button className={tab === 'overview' ? 'active' : ''} onClick={() => setTab('overview')} role="tab">Overview</button><button className={tab === 'evidence' ? 'active' : ''} onClick={() => setTab('evidence')} role="tab">Evidence <span>{evidenceEdges.length}</span></button></div>{tab === 'overview' ? <><code className="identity" title={selected.id}>{selected.id}</code><div className="inspector-actions"><button disabled={busy} onClick={onImpact} title="Traverse bounded downstream impact"><Icon name="activity" size={16}/>Explore impact</button><button className="secondary-button" disabled={busy} onClick={onTrace} title="Run the deterministic TraceImpact agent"><Icon name="spark" size={16}/>Run TraceImpact</button><IconButton label="Trace provenance lineage" icon="shield" onClick={onLineage} disabled={busy}/></div><h3>Entity properties</h3><dl className="property-list">{Object.entries(selected.properties || {}).map(([key, value]) => <div key={key}><dt>{key.replaceAll('_', ' ')}</dt><dd>{String(value)}</dd></div>)}</dl></> : <><p className="subtle">Source references returned for relationships connected to this entity.</p>{evidenceEdges.length ? <div className="evidence-stack">{evidenceEdges.map((edge, index) => <div className="evidence-card" key={edge.eid || edge.id || index}><Icon name="shield"/><div><strong>{edge.label || edge.type}</strong><small>{edge.properties?.source_ref || edge.properties?.evidence_key}</small></div></div>)}</div> : <EmptyState icon="shield" title="No direct evidence returned">Try the Evidence lens to retrieve a broader lineage chain.</EmptyState>}</>}</section>;
}

function GraphView({graph, selected, detail, selectedEdge, onInspect, onInspectEdge, onExpand, onImpact, onTrace, onLineage, busy}) {
  const [domain, setDomain] = useState('ALL');
  const domains = ['ALL', ...new Set((graph.nodes || []).map(node => node.domain).filter(Boolean))];
  const visibleNodes = domain === 'ALL' ? graph.nodes || [] : (graph.nodes || []).filter(node => node.domain === domain);
  const ids = new Set(visibleNodes.map(node => node.id));
  const visibleEdges = (graph.edges || []).filter(edge => ids.has(edge.from_id) && ids.has(edge.to_id));
  return <div className="explorer-grid"><section className="panel graph-panel"><div className="panel-heading"><div><span className="eyebrow">LIVE SUBGRAPH</span><h2>Relationship map</h2><p>Explore typed, evidence-aware connections. Results stay bounded for browser safety.</p></div><div className="panel-tools"><label className="select-control"><Icon name="filter" size={15}/><select aria-label="Filter graph by domain" value={domain} onChange={event => setDomain(event.target.value)}>{domains.map(item => <option key={item}>{item}</option>)}</select></label><span className="count-badge">{visibleNodes.length} entities</span></div></div>{(graph.warnings || []).length > 0 && <div className="inline-notice warning"><Icon name="warning"/>{graph.warnings.join(' ')}</div>}{graph.partial && <div className="inline-notice"><Icon name="info"/>This is a bounded result. Expand a specific entity to retrieve more context.</div>}<GraphCanvas nodes={visibleNodes} edges={visibleEdges} selectedId={selected?.id} selectedEdgeId={selectedEdge?.id} onSelectNode={onInspect} onSelectEdge={onInspectEdge} onExpand={onExpand}/><GraphLegend nodes={visibleNodes}/><div className="entity-strip"><div className="entity-strip-title"><strong>Entities in view</strong><small>Select an item to inspect it</small></div><div className="entity-list">{visibleNodes.map(node => <button key={node.id} onClick={() => onInspect(node)} className={selected?.id === node.id ? 'selected' : ''} title={`Inspect ${displayLabel(node)}`}><span className="type-dot" style={{background: palette[node.label] || '#64748b'}}/><span><strong>{displayLabel(node)}</strong><small>{node.label}</small></span><Icon name="chevron" size={14}/></button>)}</div></div></section><EntityInspector selected={selected} detail={detail} selectedEdge={selectedEdge} onImpact={onImpact} onTrace={onTrace} onLineage={onLineage} busy={busy}/></div>;
}

// Additional lens, administration, and application composition components follow below.
