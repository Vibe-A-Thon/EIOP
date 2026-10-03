import React, {useEffect, useState} from 'react';
import GraphCanvas, {palette} from './GraphCanvas.jsx';
import {Icon, Tip} from './icons.jsx';
import KGRExplorer from './kgr/KGRExplorer.jsx';

const emptyGraph = {nodes: [], edges: [], paths: [], evidence: [], warnings: [], partial: false};
const lenses = [
  {id: 'search', label: 'Search', icon: 'search', hint: 'Review and refine the current result set'},
  {id: 'graph', label: 'Graph', icon: 'graph', hint: 'Explore connected enterprise knowledge'},
  {id: 'impact', label: 'Impact', icon: 'activity', hint: 'Trace the blast radius of a change'},
  {id: 'evidence', label: 'Evidence', icon: 'shield', hint: 'Inspect provenance and GraphRAG context'},
  {id: 'architecture', label: 'Architecture', icon: 'layers', hint: 'Understand graph domains, types, and structural coverage'},
  {id: 'agent', label: 'Agents', icon: 'spark', hint: 'Run governed Deep Agents and inspect evidence-linked XAI'},
  {id: 'kgr', label: 'KGR', icon: 'graph', hint: 'Knowledge Graph Renderer — multi-graph explorer with blast radius, impact analysis, and node intelligence'},
];

const lensCatalog = [
  ['Search', 'search', 'available'], ['Graph', 'graph', 'available'], ['Evidence', 'shield', 'available'],
  ['Impact', 'activity', 'available'], ['Architecture', 'layers', 'available'], ['Requirement', 'link', 'available'],
  ['Trust', 'shield', 'available'], ['Ontology', 'layers', 'available'], ['Agent', 'spark', 'available'],
  ['Knowledge Health', 'activity', 'available'], ['API', 'code', 'available'], ['Security', 'shield', 'available'],
  ['Timeline', 'clock', 'planned'], ['Change', 'refresh', 'planned'], ['Runtime', 'activity', 'planned'],
  ['Release', 'upload', 'planned'], ['Process', 'graph', 'planned'], ['Simulation', 'spark', 'planned'],
  ['Decision', 'document', 'planned'], ['Test', 'check', 'planned'],
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
  // FR-VALID-003: unknown denominators render as N/A, never a false 0%.
  const na = value === null || value === undefined;
  const percentage = na ? null : Math.max(0, Math.min(100, Math.round(value * 100)));
  return <Tip text={na ? `${label}: not available for the checked graph` : `${label}: ${percentage}% of checked graph facts`}><div className="quality-ring-card" tabIndex="0">
    <div className={`quality-ring ${tone}${na ? ' na' : ''}`} style={percentage === null ? undefined : {'--score': `${percentage * 3.6}deg`}}><span>{na ? 'N/A' : `${percentage}%`}</span></div>
    <div><strong>{label}</strong><small>{na ? 'Not available for this run' : 'Latest validation run'}</small></div>
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
          <button className="primary-button wide" disabled={busy} title="Authenticate with the local EOIP API">{busy ? <><span className="spinner small"/>Connecting…</> : <>Connect <Icon name="arrow" size={17}/></>}</button>
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
    <Tip text="Open the local OpenAPI reference"><a className="icon-button" href="/docs" target="_blank" rel="noreferrer" aria-label="Open API documentation"><Icon name="code"/></a></Tip>
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

function SearchView({graph, selected, onInspect}) {
  const groups = Object.entries((graph.nodes || []).reduce((result, node) => {
    const key = node.domain || 'OTHER';
    result[key] = [...(result[key] || []), node];
    return result;
  }, {}));
  return <section className="panel search-results-panel"><div className="panel-heading"><div><span className="eyebrow">SEARCH LENS</span><h2>Results by knowledge domain</h2><p>Every result preserves its canonical graph identity for use in the other lenses.</p></div><span className="count-badge">{graph.nodes?.length || 0} matches</span></div>{groups.length ? <div className="search-domain-grid">{groups.map(([domain, nodes]) => <section key={domain} className="search-domain"><header><span>{domain}</span><strong>{nodes.length}</strong></header>{nodes.map(node => <button key={node.id} className={selected?.id === node.id ? 'selected' : ''} onClick={() => onInspect(node)} title={`Inspect ${displayLabel(node)} and preserve it as the shared lens context`}><span className="entity-symbol small" style={{'--entity-color': palette[node.label] || '#64748b'}}>{displayLabel(node).slice(0, 1).toUpperCase()}</span><span><strong>{displayLabel(node)}</strong><small>{node.label} · {shortId(node.id, 34)}</small></span><Icon name="chevron" size={15}/></button>)}</section>)}</div> : <EmptyState icon="search" title="No matching entities">Use the search field above to query issue keys, symbols, commits, files, or documents.</EmptyState>}</section>;
}

function ArchitectureView({stats, graph}) {
  const domains = Object.entries((graph.nodes || []).reduce((result, node) => {
    const key = node.domain || 'OTHER';
    result[key] = (result[key] || 0) + 1;
    return result;
  }, {}));
  const relationships = Object.entries((graph.edges || []).reduce((result, edge) => {
    result[edge.type] = (result[edge.type] || 0) + 1;
    return result;
  }, {})).sort((a, b) => b[1] - a[1]);
  return <div className="architecture-grid"><section className="panel span-2"><div className="panel-heading"><div><span className="eyebrow">ARCHITECTURE LENS</span><h2>Current semantic structure</h2><p>A live projection of domains and relationship classes in the bounded result.</p></div><span className="section-icon violet"><Icon name="layers"/></span></div><div className="domain-map">{domains.map(([domain, count], index) => <Tip text={`${count} visible entities in the ${domain} graph domain`} key={domain}><article className={`domain-card domain-${index % 5}`} tabIndex="0"><span><Icon name={index % 2 ? 'code' : 'database'}/></span><strong>{domain}</strong><small>{count} visible entities</small></article></Tip>)}</div>{!domains.length && <EmptyState icon="layers" title="No architecture context">Search for an entity to populate this bounded domain projection.</EmptyState>}</section><section className="panel"><div className="panel-heading"><div><span className="eyebrow">ONTOLOGY BASELINE</span><h2>Semantic contract</h2></div></div><dl className="architecture-facts"><div><dt>Ontology</dt><dd>{stats?.schema?.ontology_version || 'Unavailable'}</dd></div><div><dt>Graph schema</dt><dd>{stats?.schema?.schema_version || 'Unavailable'}</dd></div><div><dt>Entity types</dt><dd>{Object.keys(stats?.labels || {}).length}</dd></div><div><dt>Storage</dt><dd>{stats?.backend || 'Unavailable'}</dd></div></dl></section><section className="panel span-3"><div className="panel-heading"><div><span className="eyebrow">RELATIONSHIP MODEL</span><h2>Visible semantic links</h2><p>Counts are derived only from the current query result.</p></div></div><div className="relationship-bars">{relationships.map(([type, count]) => <Tip text={`${count} visible ${type} relationship${count === 1 ? '' : 's'}`} key={type}><div tabIndex="0"><span>{type}</span><i><b style={{width: `${Math.max(8, count / Math.max(...relationships.map(item => item[1])) * 100)}%`}}/></i><strong>{count}</strong></div></Tip>)}</div>{!relationships.length && <EmptyState icon="graph" title="No visible relationships">Select or expand a result to load connected architecture context.</EmptyState>}</section></div>;
}

function LensLibrary({open, onClose, onSelect}) {
  useEffect(() => {
    if (!open) return undefined;
    const closeOnEscape = event => event.key === 'Escape' && onClose();
    addEventListener('keydown', closeOnEscape);
    return () => removeEventListener('keydown', closeOnEscape);
  }, [open, onClose]);
  if (!open) return null;
  return <div className="lens-library-backdrop" role="presentation" onMouseDown={event => event.target === event.currentTarget && onClose()}><section className="lens-library" role="dialog" aria-modal="true" aria-labelledby="lens-library-title"><header><div><span className="eyebrow">LENSORYX FRAMEWORK</span><h2 id="lens-library-title">Experience lens library</h2><p>Available lenses are backed by current APIs. Planned lenses remain disabled until their temporal or simulation services exist.</p></div><IconButton label="Close lens library" icon="close" onClick={onClose}/></header><div className="lens-catalog">{lensCatalog.map(([name, icon, state]) => <Tip text={state === 'available' ? `${name} uses current graph and operational APIs` : `${name} requires a later roadmap backend and is not represented with fake data`} key={name}><button disabled={state !== 'available'} onClick={() => onSelect(name.toLowerCase())} title={state === 'available' ? `Open ${name} lens` : `${name} lens is planned`}><span className={`catalog-icon ${state}`}><Icon name={icon}/></span><span><strong>{name}</strong><small>{state === 'available' ? 'API-backed' : 'Backend planned'}</small></span><StatusPill status={state}/></button></Tip>)}</div></section></div>;
}

function GraphView({graph, selected, detail, selectedEdge, onInspect, onInspectEdge, onExpand, onImpact, onTrace, onLineage, busy}) {
  const [domain, setDomain] = useState('ALL');
  const [relationship, setRelationship] = useState('ALL');
  const [trust, setTrust] = useState('ALL');
  const domains = ['ALL', ...new Set((graph.nodes || []).map(node => node.domain).filter(Boolean))];
  const relationships = ['ALL', ...new Set((graph.edges || []).map(edge => edge.type).filter(Boolean))];
  const visibleNodes = domain === 'ALL' ? graph.nodes || [] : (graph.nodes || []).filter(node => node.domain === domain);
  const ids = new Set(visibleNodes.map(node => node.id));
  const visibleEdges = (graph.edges || []).filter(edge => ids.has(edge.from_id) && ids.has(edge.to_id) && (relationship === 'ALL' || edge.type === relationship) && (trust === 'ALL' || String(edge.creation_status || edge.properties?.creation_status || 'DETERMINISTIC').toUpperCase() === trust));
  return <div className="explorer-grid"><section className="panel graph-panel"><div className="panel-heading"><div><span className="eyebrow">LIVE SUBGRAPH</span><h2>Relationship map</h2><p>Explore typed, evidence-aware connections. Results stay bounded for browser safety.</p></div><div className="panel-tools"><label className="select-control" title="Show entities from one graph domain"><Icon name="filter" size={15}/><select aria-label="Filter graph by domain" value={domain} onChange={event => setDomain(event.target.value)}>{domains.map(item => <option key={item}>{item}</option>)}</select></label><label className="select-control" title="Show one relationship class"><Icon name="link" size={15}/><select aria-label="Filter graph by relationship" value={relationship} onChange={event => setRelationship(event.target.value)}>{relationships.map(item => <option key={item}>{item}</option>)}</select></label><label className="select-control" title="Filter deterministic or inferred relationships"><Icon name="shield" size={15}/><select aria-label="Filter graph by trust status" value={trust} onChange={event => setTrust(event.target.value)}><option value="ALL">All trust</option><option value="DETERMINISTIC">Deterministic</option><option value="INFERRED">Inferred</option></select></label><span className="count-badge">{visibleNodes.length} entities</span></div></div>{(graph.warnings || []).length > 0 && <div className="inline-notice warning"><Icon name="warning"/>{graph.warnings.join(' ')}</div>}{graph.partial && <div className="inline-notice"><Icon name="info"/>This is a bounded result. Expand a specific entity to retrieve more context.</div>}<GraphCanvas nodes={visibleNodes} edges={visibleEdges} paths={graph.paths || []} selectedId={selected?.id} selectedEdgeId={selectedEdge?.id} onSelectNode={onInspect} onSelectEdge={onInspectEdge} onExpand={onExpand}/><GraphLegend nodes={visibleNodes}/><div className="edge-key"><span><i className="deterministic"/>Deterministic</span><span><i className="inferred"/>Inferred</span><span><i className="path"/>Highlighted path</span><span><Icon name="shield" size={12}/>Thicker links include evidence</span></div><div className="entity-strip"><div className="entity-strip-title"><strong>Entities in view</strong><small>Select an item to inspect it</small></div><div className="entity-list">{visibleNodes.map(node => <button key={node.id} disabled={busy} onClick={() => onInspect(node)} className={selected?.id === node.id ? 'selected' : ''} title={`Inspect ${displayLabel(node)}`}><span className="type-dot" style={{background: palette[node.label] || '#64748b'}}/><span><strong>{displayLabel(node)}</strong><small>{node.label}</small></span><Icon name="chevron" size={14}/></button>)}</div></div></section><EntityInspector selected={selected} detail={detail} selectedEdge={selectedEdge} onImpact={onImpact} onTrace={onTrace} onLineage={onLineage} busy={busy}/></div>;
}

function ImpactView({source, setSource, target, setTarget, selected, graph, trace, onPath, onImpact, onTrace, busy}) {
  return <div className="lens-layout">
    <section className="panel action-panel"><div className="panel-heading"><div><span className="eyebrow">BOUNDED TRAVERSAL</span><h2>Change impact studio</h2><p>Trace downstream dependencies or find the evidence path between two canonical entities.</p></div><span className="section-icon coral"><Icon name="activity"/></span></div><div className="selection-callout"><span className="entity-symbol small" style={{'--entity-color': palette[selected?.label] || '#64748b'}}>{selected ? displayLabel(selected).slice(0, 1) : '?'}</span><div><small>CURRENT ANCHOR</small><strong>{selected ? displayLabel(selected) : 'Select an entity in the Graph lens'}</strong><code>{selected?.id || 'No canonical ID selected'}</code></div></div><button className="primary-button" disabled={busy || !selected} onClick={onImpact} title="Find entities affected within four graph hops"><Icon name="activity"/>Explore impact</button><button className="secondary-button" disabled={busy || !selected} onClick={onTrace} title="Run the read-only deterministic agent"><Icon name="spark"/>Run TraceImpact</button></section>
    <section className="panel"><div className="panel-heading"><div><span className="eyebrow">PATH FINDER</span><h2>Trace requirement to implementation</h2><p>Use exact canonical identifiers to find an ordered, policy-bounded path.</p></div></div><form className="path-form" onSubmit={onPath}><label>From canonical ID<input value={source} onChange={event => setSource(event.target.value)} required/></label><span className="path-arrow"><Icon name="arrow"/></span><label>To canonical ID<input value={target} onChange={event => setTarget(event.target.value)} required placeholder="Select a code symbol in Graph"/></label><button className="primary-button" disabled={busy} title="Find the shortest permitted graph path">Find path</button></form>{graph.paths?.length > 0 && <div className="path-result"><Icon name="check"/><div><strong>{graph.paths.length} evidence path{graph.paths.length === 1 ? '' : 's'} found</strong><small>{graph.nodes?.length || 0} entities · {graph.edges?.length || 0} relationships</small></div></div>}</section>
    {graph.meta?.impact_rationale && Object.keys(graph.meta.impact_rationale).length > 0 && <section className="panel"><div className="panel-heading"><div><span className="eyebrow">PER-NODE RATIONALE</span><h2>Why each entity is included</h2><p>Path depth, edge classes, and evidence for every impacted entity.</p></div><span className="count-badge">{Object.keys(graph.meta.impact_rationale).length} items</span></div><div className="rationale-list">{Object.entries(graph.meta.impact_rationale).map(([cid, reason]) => <div className="evidence-card" key={cid}><Icon name="activity"/><div><strong>{shortId(cid, 42)}</strong><small>{reason}</small></div></div>)}</div></section>}
    {trace && <section className="panel trace-result"><div className="panel-heading"><div><span className="eyebrow">DETERMINISTIC AGENT</span><h2>TraceImpact result</h2></div><StatusPill status={trace.partial ? 'PARTIAL' : 'COMPLETE'}/></div><p className="trace-summary">{trace.summary}</p><div className="trace-meta"><span><Icon name="graph"/>Bounded graph traversal</span><span><Icon name="shield"/>{trace.evidence_refs?.length || 0} source references</span></div><div className="evidence-stack">{(trace.evidence_refs || []).map(ref => <div className="evidence-card" key={ref}><Icon name="document"/><div><strong>Source evidence</strong><small>{ref}</small></div></div>)}</div></section>}
  </div>;
}

function EvidenceView({source, setSource, selected, lineage, rag, question, setQuestion, onLineage, onRag, onInspect, busy}) {
  return <div className="lens-layout two-column">
    <section className="panel"><div className="panel-heading"><div><span className="eyebrow">PROVENANCE</span><h2>Lineage explorer</h2><p>Trace where an entity came from and inspect the connected evidence chain.</p></div><span className="section-icon gold"><Icon name="shield"/></span></div><form className="stack-form" onSubmit={onLineage}><label>Entity canonical ID<input value={source} onChange={event => setSource(event.target.value)} required/></label><button className="primary-button" disabled={busy}>Trace lineage</button></form>{lineage ? <><div className="result-summary"><strong>{lineage.nodes?.length || 0}</strong><span>entities in lineage chain</span><small>{lineage.edges?.length || 0} relationships</small></div><div className="lineage-list">{(lineage.nodes || []).map(node => <button key={node.id} onClick={() => onInspect(node)} title={`Inspect ${displayLabel(node)}`}><span className="type-dot" style={{background: palette[node.label] || '#64748b'}}/><span><strong>{displayLabel(node)}</strong><small>{node.label}</small></span><Icon name="chevron" size={14}/></button>)}</div></> : <EmptyState icon="shield" title="No lineage loaded">Select an entity and trace lineage to view its provenance chain.</EmptyState>}</section>
    <section className="panel"><div className="panel-heading"><div><span className="eyebrow">LOCAL GRAPHRAG</span><h2>Ask with evidence</h2><p>Retrieve grounded context from the graph. Generation remains optional.</p></div><span className="section-icon mint"><Icon name="spark"/></span></div><form className="stack-form" onSubmit={onRag}><label>Question<textarea value={question} onChange={event => setQuestion(event.target.value)} rows="3" placeholder="Explain this entity and the evidence behind it" required/></label><button className="primary-button" disabled={busy || !selected}><Icon name="spark"/>Retrieve trusted context</button></form>{!selected && <div className="inline-notice"><Icon name="info"/>Select an entity in the Graph lens before retrieving context.</div>}{rag && <div className="rag-result"><div className="rag-header"><StatusPill status={rag.strategy || 'RETRIEVED'}/><span>{rag.contexts?.length || 0} contexts · {rag.evidence_refs?.length || 0} citations</span></div>{rag.answer && <p className="rag-answer">{rag.answer}</p>}<div className="evidence-stack">{(rag.contexts || []).map((context, index) => <article className="context-card" key={`${context.ref}-${index}`}><div><span className="badge">{context.kind}</span><code>{shortId(context.ref, 42)}</code></div><p>{context.text}</p>{context.citations?.length > 0 && <small>{context.citations.join(' · ')}</small>}</article>)}</div></div>}</section>
  </div>;
}

function AgentView({agents, selectedAgent, setSelectedAgent, goal, setGoal, selected, result, onRun, busy, synthesize, setSynthesize}) {
  const contract = agents.find(item => item.agent_id === selectedAgent);
  const explanation = result?.explanation;
  return <div className="agent-workbench">
    <section className="panel agent-catalog"><div className="panel-heading"><div><span className="eyebrow">GOVERNED CATALOG</span><h2>Deep Agents</h2><p>Every agent is capability-scoped, budgeted, audited, and read-only or proposal-only.</p></div><span className="count-badge">{agents.length} agents</span></div><div className="agent-list">{agents.map(agent => <button key={agent.agent_id} className={selectedAgent === agent.agent_id ? 'selected' : ''} onClick={() => setSelectedAgent(agent.agent_id)}><span className="section-icon violet"><Icon name="spark"/></span><span><strong>{agent.agent_id}</strong><small>{agent.agent_type} · {agent.risk_level} · {agent.human_control.replaceAll('_', ' ')}</small></span><Icon name="chevron" size={14}/></button>)}</div></section>
    <section className="panel agent-runner"><div className="panel-heading"><div><span className="eyebrow">BOUNDED EXECUTION</span><h2>{contract?.agent_id || 'Select an agent'}</h2><p>{contract?.purpose || 'Choose a governed specialist from the catalog.'}</p></div>{contract && <StatusPill status={contract.enabled ? 'READY' : 'DISABLED'}/>}</div>{contract && <><div className="agent-policy"><span><strong>{contract.budgets.max_steps}</strong> max steps</span><span><strong>{contract.budgets.max_seconds}s</strong> deadline</span><span><strong>{contract.allowed_tools.length}</strong> tools</span></div><form className="stack-form" onSubmit={onRun}><label>Goal<textarea rows="4" value={goal} onChange={event => setGoal(event.target.value)} required maxLength="4096"/></label>{selectedAgent === 'GraphInvestigator' && <label className="toggle"><input type="checkbox" checked={synthesize} onChange={event => setSynthesize(event.target.checked)}/><span/>Use the configured local model for evidence-grounded synthesis</label>}<div className="selection-callout"><Icon name="focus"/><div><small>GRAPH CONTEXT</small><strong>{selected ? displayLabel(selected) : 'No selected entity'}</strong><code>{selected?.id || 'Agent will use goal-only context'}</code></div></div><button className="primary-button" disabled={busy || !contract.enabled}><Icon name="spark"/>Run governed agent</button></form></>}
    {result && <div className="agent-result"><div className="panel-heading"><div><span className="eyebrow">EXPLAINABLE RESULT</span><h2>Decision and evidence</h2></div><StatusPill status={result.status}/></div><p className="trace-summary">{result.summary}</p><div className="agent-policy"><span><strong>{Math.round((explanation?.confidence || 0) * 100)}%</strong> confidence</span><span><strong>{result.evidence_refs?.length || 0}</strong> evidence refs</span><span><strong>{result.tool_calls?.length || 0}</strong> tool calls</span></div>{explanation?.uncertainty?.length > 0 && <div className="inline-notice warning"><Icon name="warning"/>{explanation.uncertainty.join(' ')}</div>}<div className="xai-grid"><div><h3>Evidence</h3><div className="evidence-stack">{(result.evidence_refs || []).slice(0, 20).map(ref => <div className="evidence-card" key={ref}><Icon name="shield"/><div><strong>Observed reference</strong><small>{ref}</small></div></div>)}</div></div><div><h3>Policy decisions</h3><div className="evidence-stack">{(explanation?.rule_decisions || []).map(rule => <div className="evidence-card" key={rule.rule_id}><Icon name="check"/><div><strong>{rule.rule_id} · {rule.outcome}</strong><small>{rule.summary}</small></div></div>)}</div></div></div>{result.proposals?.length > 0 && <div className="inline-notice"><Icon name="info"/>{result.proposals.length} inert change proposal(s) await explicit human approval. Approval does not automatically apply a mutation.</div>}</div>}
    </section>
  </div>;
}

function Explorer({stats, graph, setGraph, selected, setSelected, detail, setDetail, selectedEdge, setSelectedEdge, lens, setLens, api, run, busy}) {
  const [query, setQuery] = useState('');
  const [nlQuestion, setNlQuestion] = useState('');
  const [nlResult, setNlResult] = useState(null);
  const [source, setSource] = useState('');
  const [target, setTarget] = useState('');
  const [trace, setTrace] = useState(null);
  const [lineage, setLineage] = useState(null);
  const [rag, setRag] = useState(null);
  const [question, setQuestion] = useState('Explain the implementation and its evidence');
  const [libraryOpen, setLibraryOpen] = useState(false);
  const [agents, setAgents] = useState([]);
  const [selectedAgent, setSelectedAgent] = useState('TraceImpact');
  const [agentGoal, setAgentGoal] = useState('Explain the impact, supporting evidence, and uncertainty');
  const [agentResult, setAgentResult] = useState(null);
  const [agentSynthesize, setAgentSynthesize] = useState(false);

  useEffect(() => {
    if (lens === 'agent' && !agents.length) {
      run(async () => {const response = await api('/api/v1/agents'); setAgents(response.agents || []);});
    }
  }, [lens]);

  async function inspect(node) {
    setSelected(node); setSelectedEdge(null); setTarget(node.id); setSource(node.id);
    setDetail(await api(`/api/v1/entities/${encodeURIComponent(node.id)}`));
  }
  const executeSearch = event => {event?.preventDefault(); run(async () => {setGraph(await api(`/api/v1/search?q=${encodeURIComponent(query)}`)); setSelected(null); setSelectedEdge(null); setTrace(null);});};
  const askNaturalLanguage = event => {event.preventDefault(); run(async () => {const response = await api('/api/v1/query/nl', {question: nlQuestion}); setNlResult(response); if (response.result) {setGraph(response.result); setSelected(null); setSelectedEdge(null); setTrace(null);}});};
  const impact = () => run(async () => {const result = await api('/api/v1/impact', {canonical_id: selected.id, max_depth: 4}); setGraph(result); setLens('impact');});
  const traceImpact = () => run(async () => {setTrace(await api('/api/v1/agents/trace-impact', {canonical_id: selected.id})); setLens('impact');});
  const traceLineage = event => {event?.preventDefault(); run(async () => {setLineage(await api('/api/v1/lineage', {canonical_id: selected?.id || source, max_depth: 4})); setLens('evidence');});};
  const findPath = event => {event.preventDefault(); run(async () => {setGraph(await api('/api/v1/path', {source_id: source, target_id: target})); setLens('graph');});};
  const expand = node => run(async () => {setGraph(await api('/api/v1/neighborhood', {canonical_id: node.id, max_depth: 1, result_limit: 75})); await inspect(node);});
  const retrieve = event => {event.preventDefault(); run(async () => setRag(await api('/api/v1/rag', {canonical_id: selected.id, question, synthesize: false})));};
  const runAgent = event => {event.preventDefault(); run(async () => setAgentResult(await api(`/api/v1/agents/${encodeURIComponent(selectedAgent)}/runs`, {goal: agentGoal, context_refs: selected ? [selected.id] : [], dry_run: false, synthesize: agentSynthesize})));};
  function exportContext() {
    const context = {version: 1, lens, query, rootEntities: selected ? [selected.id] : [], domains: [...new Set((graph.nodes || []).map(node => node.domain).filter(Boolean))], result: {nodes: graph.nodes?.length || 0, edges: graph.edges?.length || 0}, exportedAt: new Date().toISOString()};
    const url = URL.createObjectURL(new Blob([JSON.stringify(context, null, 2)], {type: 'application/json'}));
    const anchor = document.createElement('a'); anchor.href = url; anchor.download = 'eoip-knowledge-context.json'; anchor.click(); URL.revokeObjectURL(url);
  }
  function openCatalogLens(name) {
    const routes = {requirement: 'impact', trust: 'evidence', ontology: 'architecture', agent: 'agent', 'knowledge health': 'architecture', api: 'architecture', security: 'evidence'};
    setLens(routes[name] || name); setLibraryOpen(false);
  }

  return <>
    <section className="hero-search"><div className="hero-copy"><span className="eyebrow"><i/>CONNECTED ENTERPRISE CONTEXT</span><h2>What do you want to understand?</h2><p>Find an issue, commit, symbol, file, person, or document—then follow the relationships that explain it.</p></div><form onSubmit={executeSearch} className="global-search"><Icon name="search" size={21}/><input aria-label="Search knowledge graph" value={query} onChange={event => setQuery(event.target.value)} placeholder="Search by issue key, symbol, commit, or path…" required/><button disabled={busy} title="Search the persisted knowledge graph">Search graph <span>↵</span></button></form><form onSubmit={askNaturalLanguage} className="global-search nl-search"><Icon name="spark" size={21}/><input aria-label="Ask the knowledge graph" value={nlQuestion} onChange={event => setNlQuestion(event.target.value)} placeholder="Ask in plain language — e.g. what implements EOIP-1, what is impacted by a symbol…" required/><button disabled={busy} title="Interpret the question as a bounded, policy-checked QueryPlan">Ask graph <span>↵</span></button></form>{nlResult && <div className="inline-notice nl-interpretation" role="status"><Icon name={nlResult.interpretation?.plan ? 'check' : 'info'}/>{nlResult.interpretation?.plan ? <span>Interpreted as <strong>{nlResult.interpretation.plan.intent}</strong> plan{nlResult.interpretation.explanation ? ` — ${nlResult.interpretation.explanation}` : ''}{nlResult.result ? ` · ${nlResult.result.nodes?.length || 0} entities returned` : ''}</span> : <span>{nlResult.interpretation?.clarification || 'The question could not be mapped to a bounded query plan.'}</span>}</div>}</section>
    <div className="metrics-grid"><MetricCard icon="database" eyebrow="ENTITIES" value={stats?.vertices ?? '—'} caption="Persisted canonical facts" tone="violet" tooltip="Canonical entities currently stored in HugeGraph"/><MetricCard icon="graph" eyebrow="RELATIONSHIPS" value={stats?.edges ?? '—'} caption="Typed semantic links" tone="blue" tooltip="Typed relationships currently stored in HugeGraph"/><MetricCard icon="layers" eyebrow="ENTITY TYPES" value={stats ? Object.values(stats.labels || {}).filter(value => value > 0).length : '—'} caption={`${Object.keys(stats?.labels || {}).length || 0} types available`} tone="mint" tooltip="Ontology entity types represented by at least one stored entity"/><MetricCard icon="activity" eyebrow="WORKER" value={stats?.worker?.status || 'Starting'} caption={stats?.worker?.updated_at ? `Updated ${formatTime(stats.worker.updated_at)}` : 'Background ingestion service'} tone="coral" tooltip="Current background ingestion worker state"/></div>
    <div className="lens-bar" role="tablist" aria-label="Explorer lenses"><div>{lenses.map(item => <Tip text={item.hint} key={item.id}><button role="tab" aria-selected={lens === item.id} className={lens === item.id ? 'active' : ''} onClick={() => setLens(item.id)}><Icon name={item.icon}/>{item.label}</button></Tip>)}<Tip text="Browse every documented experience lens and its implementation state"><button onClick={() => setLibraryOpen(true)}><Icon name="plus"/>All lenses</button></Tip></div><span className="context-actions"><span className="context-chip"><Icon name="focus" size={14}/>{selected ? displayLabel(selected) : 'No entity selected'}</span><IconButton label="Export the current local lens context" icon="upload" onClick={exportContext}/></span></div>
    {lens === 'search' && <SearchView graph={graph} selected={selected} onInspect={node => run(() => inspect(node))}/>}
    {lens === 'graph' && <GraphView graph={graph} selected={selected} detail={detail} selectedEdge={selectedEdge} onInspect={node => run(() => inspect(node))} onInspectEdge={edge => {setSelectedEdge(edge); setSelected(null);}} onExpand={expand} onImpact={impact} onTrace={traceImpact} onLineage={traceLineage} busy={busy}/>} 
    {lens === 'impact' && <ImpactView source={source} setSource={setSource} target={target} setTarget={setTarget} selected={selected} graph={graph} trace={trace} onPath={findPath} onImpact={impact} onTrace={traceImpact} busy={busy}/>} 
    {lens === 'evidence' && <EvidenceView source={source} setSource={setSource} selected={selected} lineage={lineage} rag={rag} question={question} setQuestion={setQuestion} onLineage={traceLineage} onRag={retrieve} onInspect={node => run(() => inspect(node))} busy={busy}/>} 
    {lens === 'architecture' && <ArchitectureView stats={stats} graph={graph}/>}
    {lens === 'agent' && <AgentView agents={agents} selectedAgent={selectedAgent} setSelectedAgent={setSelectedAgent} goal={agentGoal} setGoal={setAgentGoal} selected={selected} result={agentResult} onRun={runAgent} busy={busy} synthesize={agentSynthesize} setSynthesize={setAgentSynthesize}/>}
    {lens === 'kgr' && <KGRExplorer graph={graph} setGraph={setGraph} api={api} run={run} busy={busy} stats={stats}/>}
    <LensLibrary open={libraryOpen} onClose={() => setLibraryOpen(false)} onSelect={openCatalogLens}/>
  </>;
}

function ConnectorCard({icon, name, description, status = 'Available', children, tone}) {
  return <article className={`connector-card ${tone || ''}`}><div className="connector-top"><span className="connector-icon"><Icon name={icon}/></span><StatusPill status={status}/></div><h3>{name}</h3><p>{description}</p>{children}</article>;
}

function JobsTable({jobs, jobSummary, onCancel}) {
  if (!jobs.length) return <EmptyState icon="clock" title="No ingestion jobs yet">Load the demo or import a source to create the first durable job.</EmptyState>;
  return <div className="table-wrap"><table><thead><tr><th>Source</th><th>Status</th><th>Created</th><th>Result</th>{onCancel && <th>Action</th>}</tr></thead><tbody>{jobs.map(job => <tr key={job.job_id}><td><div className="table-primary"><span className="service-icon mini"><Icon name={job.kind === 'DEMO' ? 'spark' : 'upload'} size={15}/></span><span><strong>{job.kind.replaceAll('_', ' ')}</strong><small title={job.job_id}>{shortId(job.job_id, 18)}</small></span></div></td><td><StatusPill status={job.status}/></td><td>{formatTime(job.created_at)}</td><td>{job.error || (job.result ? jobSummary(job) : job.status === 'CANCELLED' ? 'Cancelled before execution' : 'Waiting for worker')}</td>{onCancel && <td>{job.status === 'PENDING' ? <button className="table-action" onClick={() => onCancel(job.job_id)}>Cancel</button> : <span className="subtle">—</span>}</td>}</tr>)}</tbody></table></div>;
}

function FindingsTable({findings}) {
  if (!findings.length) return null;
  return <div className="table-wrap"><table><thead><tr><th>Severity</th><th>Rule</th><th>Affected fact</th><th>Detail</th></tr></thead><tbody>{findings.map((finding, index) => <tr key={`${finding.rule}-${index}`}><td><StatusPill status={finding.severity}/></td><td>{finding.rule}</td><td><code>{shortId(finding.canonical_id || finding.edge_id || '', 26)}</code></td><td>{finding.detail}</td></tr>)}</tbody></table></div>;
}

function AuditTable({items}) {
  if (!items.length) return <EmptyState icon="check" title="No audit events returned">The current audit store contains no readable events.</EmptyState>;
  return <div className="table-wrap"><table><thead><tr><th>Time</th><th>Operation</th><th>Actor</th><th>Outcome</th><th>Summary</th></tr></thead><tbody>{items.map((event, index) => <tr key={event.audit_id || index}><td>{formatTime(event.timestamp)}</td><td>{event.event_type}</td><td>{event.actor}</td><td><StatusPill status={event.outcome}/></td><td>{event.safe_summary || '—'}</td></tr>)}</tbody></table></div>;
}

function DeadLetterTable({items, onReplay, busy}) {
  if (!items.length) return <EmptyState icon="check" title="Dead-letter queue is clear">No rejected records were returned by the API.</EmptyState>;
  return <div className="table-wrap"><table><thead><tr><th>Source</th><th>Failure</th><th>Record</th><th>Payload hash</th><th>Recovery</th></tr></thead><tbody>{items.map((item, index) => {
    const replayable = ['jira', 'gitlab'].includes(item.source_system);
    return <tr key={item.event_id || index}>
      <td><strong>{item.source_system || 'Unknown source'}</strong><small>{item.error_category || item.stage || 'Unknown category'}</small></td>
      <td>{item.error || item.error_message || 'Rejected record'}</td>
      <td><code title={item.event_id || ''}>{shortId(item.source_record_id || item.event_id || '', 24)}</code></td>
      <td><code title={item.payload_hash || ''}>{shortId(item.payload_hash || '', 20)}</code></td>
      <td>{replayable && item.event_id ? <button className="table-action" onClick={() => onReplay(item.event_id)} disabled={busy}>Replay</button> : <span className="subtle">Not supported</span>}</td>
    </tr>;
  })}</tbody></table></div>;
}

function AdminOntology({schema}) {
  if (!schema) return <EmptyState icon="layers" title="Ontology schema is not loaded">Load the authoritative graph schema to inspect entity types, relationship constraints, and indexes.</EmptyState>;
  const labels = Object.entries(schema.vertex_labels || {});
  const edges = Object.entries(schema.edge_labels || {});
  return <div className="kgr-ontology-view">
    <div className="ontology-summary"><span className="section-icon violet"><Icon name="layers"/></span><strong>Ontology {schema.ontology_version}</strong><small>Schema {schema.schema_version} · {(schema.domains || []).length} domains · {labels.length} entity types · {edges.length} relationship types</small></div>
    <section><div className="panel-heading"><div><span className="eyebrow">ENTITY TYPES</span><h3>Vertex labels ({labels.length})</h3></div></div><div className="schema-grid">{labels.map(([name, info]) =>
      <article key={name} className="schema-card"><div className="schema-card-header"><span className="type-dot" style={{background: palette[name] || '#94a3b8'}}/><strong>{name}</strong><span className="badge">{info.instance_count} instances</span></div><small className="schema-domain">{info.domain}</small><div className="schema-props"><strong>Required:</strong> {(info.required_properties || []).join(', ') || 'None'}</div>{(info.optional_properties || []).length > 0 && <div className="schema-props"><strong>Optional:</strong> {info.optional_properties.join(', ')}</div>}</article>
    )}</div></section>
    <section><div className="panel-heading"><div><span className="eyebrow">RELATIONSHIP TYPES</span><h3>Edge labels ({edges.length})</h3></div></div><div className="schema-grid">{edges.map(([name, info]) =>
      <article key={name} className="schema-card"><div className="schema-card-header"><Icon name="link" size={14}/><strong>{name}</strong></div><div className="schema-props"><strong>From:</strong> {(info.source_labels || []).join(', ')}</div><div className="schema-props"><strong>To:</strong> {(info.target_labels || []).join(', ')}</div>{(info.properties || []).length > 0 && <div className="schema-props"><strong>Properties:</strong> {info.properties.join(', ')}</div>}</article>
    )}</div></section>
    <section><div className="panel-heading"><div><span className="eyebrow">INDEXES</span><h3>Index coverage ({(schema.indexes || []).length})</h3></div></div><div className="index-list">{(schema.indexes || []).map(index =>
      <div key={index.name} className="index-row"><Icon name="check" size={14}/><strong>{index.name}</strong><span className="badge">{index.type}</span><small>{index.label || 'global'} · {(index.fields || []).join(', ')}</small></div>
    )}</div></section>
  </div>;
}

function Admin({stats, system, jobs, api, run, refresh, busy}) {
  const [validation, setValidation] = useState(null);
  const [upload, setUpload] = useState(null);
  const [gitlabUpload, setGitlabUpload] = useState(null);
  const [audit, setAudit] = useState(null);
  const [dlq, setDlq] = useState(null);
  const [ontology, setOntology] = useState(null);
  const [ontologySchema, setOntologySchema] = useState(null);
  const [section, setSection] = useState('overview');
  const [checkpoint, setCheckpoint] = useState('');
  const [dryRun, setDryRun] = useState(true);
  const finishedJobs = jobs.filter(job => ['SUCCEEDED', 'PARTIAL', 'FAILED', 'CANCELLED'].includes(job.status));
  const successRate = finishedJobs.length ? Math.round(finishedJobs.filter(job => job.status === 'SUCCEEDED').length / finishedJobs.length * 100) : null;
  const jobSummary = job => {const result = job.result || {}; return job.kind === 'DEMO' ? `${result.jira?.records_accepted || 0} Jira · ${result.git?.files || 0} files · ${result.git?.symbols || 0} symbols` : `${result.records_accepted || 0} accepted · ${result.records_rejected || 0} rejected`;};
  async function importFile(file, endpoint) {if (!file) return; if (file.size > 3_000_000) throw new Error('Select a JSON file smaller than 3 MB'); await api(endpoint, {document: JSON.parse(await file.text())}); await refresh();}
  const submitSync = source => run(async () => {await api(`/api/v1/admin/ingestion/${source}`, {checkpoint: checkpoint || null, watermark: null, dry_run: dryRun}); await refresh();});
  const cancelJob = jobId => run(async () => {await api(`/api/v1/admin/jobs/${encodeURIComponent(jobId)}/cancel`, {}); await refresh();});
  const replayDlq = eventId => run(async () => {await api(`/api/v1/admin/dlq/${encodeURIComponent(eventId)}/replay`, {}); setDlq(await api('/api/v1/admin/dlq?limit=25')); await refresh();});
  return <>
    <div className="admin-summary"><div><span className="eyebrow"><i/>OPERATIONS OVERVIEW</span><h2>Keep enterprise knowledge trustworthy.</h2><p>Monitor source ingestion, graph quality, ontology state, and auditable platform activity from one control plane.</p></div><div className="admin-summary-actions"><button className="secondary-button" onClick={() => run(async () => {setValidation(await api('/api/v1/admin/validation', {})); setSection('quality');})} disabled={busy} title="Validate current graph facts and open quality results"><Icon name="shield"/>Run validation</button><button className="primary-button" onClick={() => run(async () => {await api('/api/v1/admin/demo', {}); await refresh();})} disabled={busy} title="Queue an idempotent demo ingestion run"><Icon name="spark"/>Load / replay demo</button></div></div>
    <div className="metrics-grid admin-metrics"><MetricCard icon="database" eyebrow="GRAPH ENTITIES" value={stats?.vertices ?? '—'} caption="Authoritative HugeGraph" tone="violet"/><MetricCard icon="graph" eyebrow="RELATIONSHIPS" value={stats?.edges ?? '—'} caption="Across all graph domains" tone="blue"/><MetricCard icon="activity" eyebrow="JOB SUCCESS" value={successRate === null ? '—' : `${successRate}%`} caption={`${finishedJobs.length} completed runs`} tone="mint" tooltip="Success rate calculated from completed jobs returned by the API"/><MetricCard icon="shield" eyebrow="SCHEMA" value={stats?.schema?.schema_version || '—'} caption={`Ontology ${stats?.schema?.ontology_version || 'unavailable'}`} tone="gold"/></div>
    <div className="admin-tabs" role="tablist">{[['overview', 'Overview', 'layers'], ['sources', 'Sources & jobs', 'upload'], ['quality', 'Quality & ontology', 'shield'], ['operations', 'Audit & recovery', 'terminal']].map(([id, label, icon]) => <button key={id} role="tab" aria-selected={section === id} className={section === id ? 'active' : ''} onClick={() => setSection(id)} title={`Open ${label}`}><Icon name={icon}/>{label}</button>)}</div>
    {section === 'overview' && <div className="admin-grid">
      <section className="panel span-2"><div className="panel-heading"><div><span className="eyebrow">RECENT ACTIVITY</span><h2>Ingestion jobs</h2><p>Durable worker jobs and their latest reported state.</p></div><button className="secondary-button" onClick={() => run(refresh)} disabled={busy}><Icon name="refresh"/>Refresh jobs</button></div><JobsTable jobs={jobs} jobSummary={jobSummary}/></section>
      <section className="panel"><div className="panel-heading"><div><span className="eyebrow">PLATFORM</span><h2>Service health</h2></div></div><div className="service-list"><div><span className="service-icon violet"><Icon name="database"/></span><span><strong>HugeGraph</strong><small>Authoritative graph store</small></span><StatusPill status={system?.graph?.status || (stats ? 'READY' : 'CHECKING')}/></div><div><span className="service-icon mint"><Icon name="activity"/></span><span><strong>Ingestion worker</strong><small>Background job processor</small></span><StatusPill status={stats?.worker?.status || 'STARTING'}/></div><div><span className="service-icon blue"><Icon name="shield"/></span><span><strong>Schema bootstrap</strong><small>Idempotent ontology schema</small></span><StatusPill status={stats?.schema ? 'READY' : 'CHECKING'}/></div><div><span className="service-icon coral"><Icon name="spark"/></span><span><strong>Local model</strong><small>{system?.model?.name || 'Optional deterministic fallback active'}</small></span><StatusPill status={system?.model?.status || 'CHECKING'}/></div><div><span className="service-icon gold"><Icon name="upload"/></span><span><strong>Backup state</strong><small>{system?.backup?.latest ? `${system.backup.latest.vertices} entities · ${formatTime(system.backup.latest.created_at)}` : 'No checksummed snapshot found'}</small></span><StatusPill status={system?.backup?.status || 'CHECKING'}/></div></div></section>
      <section className="panel span-3"><div className="panel-heading"><div><span className="eyebrow">ENTITY DISTRIBUTION</span><h2>Graph inventory</h2><p>Live counts by ontology label; zero-count types are intentionally visible.</p></div><span className="count-badge">{Object.keys(stats?.labels || {}).length} types</span></div><div className="inventory-grid">{Object.entries(stats?.labels || {}).map(([key, value]) => <Tip text={`${value} ${key} entities persisted`} key={key}><div className={value ? '' : 'zero'} tabIndex="0"><span className="type-dot" style={{background: palette[key] || '#94a3b8'}}/><span>{key}</span><strong>{value}</strong></div></Tip>)}</div></section>
    </div>}
    {section === 'sources' && <div className="admin-section">
      <div className="connector-grid"><ConnectorCard icon="spark" name="Demo dataset" description="Synthetic Jira, Git, code, pipeline, and documentation evidence." status="Ready" tone="violet"><button onClick={() => run(async () => {await api('/api/v1/admin/demo', {}); await refresh();})} disabled={busy}>Load dataset <Icon name="arrow"/></button></ConnectorCard><ConnectorCard icon="upload" name="Jira JSON" description="Import a configurable Jira export with record-level validation." status="File import" tone="blue"><label className="file-picker"><input type="file" accept="application/json,.json" onChange={event => setUpload(event.target.files?.[0] || null)}/><Icon name="document"/><span>{upload?.name || 'Choose JSON file'}</span></label><button onClick={() => run(() => importFile(upload, '/api/v1/admin/ingestion/jira'))} disabled={busy || !upload}>Import Jira <Icon name="arrow"/></button></ConnectorCard><ConnectorCard icon="code" name="GitLab metadata" description="Import merge request and pipeline metadata from JSON." status="File import" tone="coral"><label className="file-picker"><input type="file" accept="application/json,.json" onChange={event => setGitlabUpload(event.target.files?.[0] || null)}/><Icon name="document"/><span>{gitlabUpload?.name || 'Choose JSON file'}</span></label><button onClick={() => run(() => importFile(gitlabUpload, '/api/v1/admin/ingestion/gitlab'))} disabled={busy || !gitlabUpload}>Import GitLab <Icon name="arrow"/></button></ConnectorCard><ConnectorCard icon="document" name="Confluence" description="Queue incremental Data Center content synchronization." status="Configured externally" tone="mint"><button onClick={() => submitSync('confluence')} disabled={busy}>Queue dry run <Icon name="arrow"/></button></ConnectorCard><ConnectorCard icon="settings" name="ServiceNow" description="Queue incremental knowledge article synchronization." status="Configured externally" tone="gold"><button onClick={() => submitSync('servicenow')} disabled={busy}>Queue dry run <Icon name="arrow"/></button></ConnectorCard><ConnectorCard icon="layers" name="Rally" description="Import epics, features, and user stories from Rally/Broadcom." status="Configured externally" tone="violet"><button onClick={() => submitSync('rally')} disabled={busy}>Queue dry run <Icon name="arrow"/></button></ConnectorCard><ConnectorCard icon="activity" name="Grafana" description="Sync dashboards, alert rules, and data sources from Grafana." status="Configured externally" tone="mint"><button onClick={() => submitSync('grafana')} disabled={busy}>Queue dry run <Icon name="arrow"/></button></ConnectorCard><ConnectorCard icon="activity" name="Datadog" description="Sync dashboards and monitors from Datadog." status="Configured externally" tone="coral"><button onClick={() => submitSync('datadog')} disabled={busy}>Queue dry run <Icon name="arrow"/></button></ConnectorCard><ConnectorCard icon="terminal" name="Kibana" description="Import dashboards, saved searches, and index patterns from Kibana." status="Configured externally" tone="blue"><button onClick={() => submitSync('kibana')} disabled={busy}>Queue dry run <Icon name="arrow"/></button></ConnectorCard><ConnectorCard icon="shield" name="qTest" description="Import test cases, suites, cycles, and runs from qTest." status="Configured externally" tone="gold"><button onClick={() => submitSync('qtest')} disabled={busy}>Queue dry run <Icon name="arrow"/></button></ConnectorCard><ConnectorCard icon="focus" name="Figma" description="Import design files, pages, and components from Figma." status="Configured externally" tone="violet"><button onClick={() => submitSync('figma')} disabled={busy}>Queue dry run <Icon name="arrow"/></button></ConnectorCard><ConnectorCard icon="link" name="API Portal" description="Sync API services, endpoints, and Swagger connections." status="Configured externally" tone="blue"><button onClick={() => submitSync('api_portal')} disabled={busy}>Queue dry run <Icon name="arrow"/></button></ConnectorCard><ConnectorCard icon="code" name="GitHub" description="Import repositories, commits, and pull requests from GitHub." status="Configured externally" tone="coral"><button onClick={() => submitSync('github')} disabled={busy}>Queue dry run <Icon name="arrow"/></button></ConnectorCard></div>
      <section className="panel sync-options"><div><h2>Incremental sync options</h2><p>Applies to Confluence and ServiceNow jobs. Credentials remain in worker configuration.</p></div><label>Checkpoint<input value={checkpoint} onChange={event => setCheckpoint(event.target.value)} placeholder="Optional ISO-8601 checkpoint"/></label><label className="toggle"><input type="checkbox" checked={dryRun} onChange={event => setDryRun(event.target.checked)}/><span/>Dry run only</label></section>
      <section className="panel"><div className="panel-heading"><div><span className="eyebrow">DURABLE QUEUE</span><h2>Ingestion jobs</h2></div><button className="secondary-button" onClick={() => run(refresh)} disabled={busy}><Icon name="refresh"/>Refresh counts</button></div><JobsTable jobs={jobs} jobSummary={jobSummary} onCancel={cancelJob}/></section>
    </div>}
    {section === 'quality' && <div className="admin-grid">
      <section className="panel span-2"><div className="panel-heading"><div><span className="eyebrow">GRAPH VALIDATION</span><h2>Knowledge quality</h2><p>Metrics are computed from persisted entities, relationships, and findings.</p></div><button className="primary-button" onClick={() => run(async () => setValidation(await api('/api/v1/admin/validation', {})))} disabled={busy}><Icon name="shield"/>Run validation</button></div>{validation ? <><div className={`validation-banner ${validation.valid ? 'success' : 'danger'}`}><Icon name={validation.valid ? 'check' : 'warning'}/><div><strong>{validation.valid ? 'No findings in the checked graph.' : `${validation.findings.length} findings require review.`}</strong><small>Checked {validation.vertices_checked} entities and {validation.edges_checked} relationships · {formatTime(validation.finished_at)}</small></div></div><div className="quality-grid"><QualityRing label="Evidence coverage" value={validation.quality?.evidence_coverage} tone="violet"/><QualityRing label="Provenance coverage" value={validation.quality?.provenance_coverage} tone="mint"/><QualityRing label="Schema compliance" value={validation.quality?.schema_compliance} tone="blue"/><QualityRing label="Completeness" value={validation.quality?.completeness} tone="gold"/><QualityRing label="Freshness" value={validation.quality?.freshness} tone="coral"/><QualityRing label="Orphan rate" value={validation.quality?.orphan_rate} tone="coral"/><QualityRing label="Duplicate rate" value={validation.quality?.duplicate_rate} tone="coral"/><div className="finding-count"><strong>{validation.quality?.error_count || 0}</strong><span>Errors</span><small>{validation.quality?.warning_count || 0} warnings</small></div></div><FindingsTable findings={validation.findings || []}/></> : <EmptyState icon="shield" title="Validation has not run in this session">Run validation to compute current quality coverage and inspect first-class findings.</EmptyState>}</section>
      <section className="panel"><div className="panel-heading"><div><span className="eyebrow">SEMANTIC MODEL</span><h2>Ontology schema</h2></div></div><div className="ontology-summary"><span className="section-icon violet"><Icon name="layers"/></span><strong>Ontology {stats?.schema?.ontology_version || '—'}</strong><small>Schema {stats?.schema?.schema_version || '—'}</small></div><dl className="compact-list"><div><dt>Vertex labels</dt><dd>{Object.keys(stats?.labels || {}).length}</dd></div><div><dt>Storage backend</dt><dd>{stats?.backend || '—'}</dd></div><div><dt>Initialization</dt><dd><StatusPill status={stats?.schema ? 'READY' : 'UNKNOWN'}/></dd></div></dl><button className="secondary-button wide" onClick={() => run(async () => setOntologySchema(await api('/api/v1/graph/schema')))} disabled={busy}><Icon name="layers"/>Load ontology schema</button>{ontologySchema && <AdminOntology schema={ontologySchema}/>}<button className="secondary-button wide" onClick={() => run(async () => setOntology(await api('/api/v1/ontology/export?limit=1')))} disabled={busy}><Icon name="code"/>Inspect JSON-LD context</button>{ontology && <pre className="code-panel">{JSON.stringify(ontology['@context'] || {}, null, 2)}</pre>}</section>
    </div>}
    {section === 'operations' && <div className="admin-grid">
      <section className="panel span-2"><div className="panel-heading"><div><span className="eyebrow">AUDIT TRAIL</span><h2>Security-relevant activity</h2><p>Safe summaries only; secrets and payload content are excluded.</p></div><button className="secondary-button" onClick={() => run(async () => setAudit(await api('/api/v1/admin/audit?limit=50')))} disabled={busy}><Icon name="refresh"/>Load audit events</button></div>{audit ? <AuditTable items={audit}/> : <EmptyState icon="terminal" title="Audit events are not loaded">Load the latest events to inspect operations, outcomes, actors, and correlation-safe summaries.</EmptyState>}</section>
      <section className="panel span-3"><div className="panel-heading"><div><span className="eyebrow">RECOVERY</span><h2>Dead-letter queue</h2><p>Inspect rejection context and payload identity without exposing captured payloads.</p></div><button className="secondary-button" onClick={() => run(async () => setDlq(await api('/api/v1/admin/dlq?limit=25')))} disabled={busy}>Load DLQ</button></div>{dlq ? <DeadLetterTable items={dlq} onReplay={replayDlq} busy={busy}/> : <EmptyState icon="warning" title="DLQ is not loaded">Load the queue to inspect rejected records and their recovery actions.</EmptyState>}</section>
    </div>}
  </>;
}

export default function App() {
  const [token, setToken] = useState(sessionStorage.getItem('eoip-token') || '');
  const [authenticated, setAuthenticated] = useState(false);
  const [mode, setMode] = useState(location.pathname.startsWith('/admin') ? 'admin' : 'app');
  const [lens, setLens] = useState('graph');
  const [collapsed, setCollapsed] = useState(false);
  const [stats, setStats] = useState(null);
  const [system, setSystem] = useState(null);
  const [jobs, setJobs] = useState([]);
  const [graph, setGraph] = useState(emptyGraph);
  const [selected, setSelected] = useState(null);
  const [selectedEdge, setSelectedEdge] = useState(null);
  const [detail, setDetail] = useState(null);
  const [error, setError] = useState('');
  const [errorMeta, setErrorMeta] = useState('');
  const [busy, setBusy] = useState(false);
  const [health, setHealth] = useState('checking');

  async function api(path, body) {
    const response = await fetch(path, {method: body === undefined ? 'GET' : 'POST', headers: {'Authorization': `Bearer ${token}`, ...(body !== undefined ? {'Content-Type': 'application/json'} : {})}, ...(body !== undefined ? {body: JSON.stringify(body)} : {})});
    const contentType = response.headers.get('content-type') || '';
    const data = contentType.includes('json') ? await response.json() : await response.text();
    if (!response.ok) {
      const message = typeof data?.detail === 'string' ? data.detail : typeof data === 'string' && data ? data : `Request failed (${response.status})`;
      const exception = new Error(message);
      exception.correlationId = response.headers.get('X-Correlation-ID');
      throw exception;
    }
    return data;
  }
  async function run(action) {
    setBusy(true); setError(''); setErrorMeta('');
    try {await action();} catch (exception) {setError(exception.message || 'The operation could not be completed.'); setErrorMeta(exception.correlationId ? `Correlation ID: ${exception.correlationId}` : 'Check that the local API and graph services are available.');} finally {setBusy(false);}
  }
  async function refresh() {const [nextStats, nextSystem, nextJobs] = await Promise.all([api('/api/v1/admin/stats'), api('/api/v1/admin/system'), api('/api/v1/admin/jobs')]); setStats(nextStats); setSystem(nextSystem); setJobs(nextJobs);}
  async function login(event) {event.preventDefault(); await run(async () => {await refresh(); sessionStorage.setItem('eoip-token', token); setAuthenticated(true);});}
  function disconnect() {sessionStorage.removeItem('eoip-token'); setToken(''); setAuthenticated(false); setStats(null); setSystem(null); setGraph(emptyGraph); setSelected(null);}
  function navigate(value) {setMode(value); history.pushState({}, '', `/${value}`);}

  useEffect(() => {fetch('/health/ready').then(response => setHealth(response.ok ? 'ready' : 'unavailable')).catch(() => setHealth('unavailable'));}, []);
  useEffect(() => {if (!authenticated) return; const timer = setInterval(() => refresh().catch(() => {}), 15000); return () => clearInterval(timer);}, [authenticated, token]);
  useEffect(() => {const onPop = () => setMode(location.pathname.startsWith('/admin') ? 'admin' : 'app'); addEventListener('popstate', onPop); return () => removeEventListener('popstate', onPop);}, []);

  if (!authenticated) return <><Login token={token} setToken={setToken} onSubmit={login} busy={busy} health={health}/>{error && <div className="toast error-toast" role="alert"><span className="toast-icon"><Icon name="warning"/></span><div><strong>{error}</strong><small>{errorMeta}</small></div><IconButton label="Dismiss error" icon="close" onClick={() => setError('')}/></div>}</>;
  return <div className={`app-shell ${collapsed ? 'nav-collapsed' : ''}`}><Sidebar mode={mode} onNavigate={navigate} collapsed={collapsed} onToggle={() => setCollapsed(value => !value)} stats={stats}/><div className="workspace"><Topbar mode={mode} stats={stats} onRefresh={() => run(refresh)} onDisconnect={disconnect} busy={busy}/><main>{mode === 'app' ? <Explorer stats={stats} graph={graph} setGraph={setGraph} selected={selected} setSelected={setSelected} detail={detail} setDetail={setDetail} selectedEdge={selectedEdge} setSelectedEdge={setSelectedEdge} lens={lens} setLens={setLens} api={api} run={run} busy={busy}/> : <Admin stats={stats} system={system} jobs={jobs} api={api} run={run} refresh={refresh} busy={busy}/>}</main><footer><span>EOIP · Evidence-backed enterprise intelligence</span><span>Local-first · Read-only graph experience · Policy bounded</span></footer></div>{busy && <div className="busy-bar" aria-label="Operation in progress"><span/></div>}{error && <div className="toast error-toast" role="alert"><span className="toast-icon"><Icon name="warning"/></span><div><strong>{error}</strong><small>{errorMeta}</small></div><IconButton label="Dismiss error" icon="close" onClick={() => setError('')}/></div>}</div>;
}
