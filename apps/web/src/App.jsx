import React, {lazy, Suspense, useCallback, useEffect, useMemo, useRef, useState} from 'react';
import {palette} from './design-system/graph-palette.js';
import {Icon, Tip} from './icons.jsx';
import Connection from './app/shell/Connection.jsx';
import WorkspaceShell from './app/shell/WorkspaceShell.jsx';
import RouteBoundary from './app/shell/RouteBoundary.jsx';
import Appearance from './features/settings/Appearance.jsx';
import {destinationFor, destinations} from './app/navigation.ts';
import {createApiClient} from './shared/api/client.ts';
import GraphEnhancementToolbar from './kgr/enhancements/GraphEnhancementToolbar.jsx';
import './kgr/enhancements/enhancements.css';

const GraphCanvas = lazy(() => import('./GraphCanvas.jsx'));
const KGRExplorer = lazy(() => import('./kgr/KGRExplorer.jsx'));
const Studio = lazy(() => import('./studio/Studio.jsx'));
const AdminSecurityCenter = lazy(() => import('./admin/index.jsx'));
const CognitiveHub = lazy(() => import('./cognitive/CognitiveHub.jsx'));
const EngineDashboardsHub = lazy(() => import('./dashboards/EngineDashboardsHub.jsx'));

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


function GuidedDemo({api, run, busy}) {
  const [catalog, setCatalog] = useState(null);
  const [loadError, setLoadError] = useState('');
  const [outcomes, setOutcomes] = useState({});

  async function loadScenarios() {
    setLoadError('');
    try {
      const response = await api('/api/v1/demo/scenarios');
      if (!Array.isArray(response.scenarios)) {
        throw new Error('The scenario catalog response did not contain a scenarios list.');
      }
      setCatalog(response);
      setOutcomes({});
    } catch (exception) {
      setLoadError(exception.message || 'The scenario catalog could not be loaded.');
      setCatalog(null);
    }
  }

  useEffect(() => {
    loadScenarios();
  }, []);

  function executeScenario(scenario) {
    run(async () => {
      setOutcomes(current => ({...current, [scenario.id]: {status: 'RUNNING'}}));
      try {
        const expectedPath = scenario.expected_path;
        if (!Array.isArray(expectedPath) || expectedPath.length < 2) {
          throw new Error('This scenario does not declare a valid entrypoint-to-target path.');
        }
        const response = await api('/api/v1/path', {
          source_id: expectedPath[0],
          target_id: expectedPath[expectedPath.length - 1],
          max_depth: 8,
          ...(scenario.relationship_allowlist?.length ? {relationship_allowlist: scenario.relationship_allowlist} : {}),
        });
        setOutcomes(current => ({...current, [scenario.id]: {status: 'COMPLETE', response}}));
      } catch (exception) {
        setOutcomes(current => ({
          ...current,
          [scenario.id]: {status: 'ERROR', error: exception.message || 'Path request failed.'},
        }));
        throw exception;
      }
    });
  }

  return <section className="guided-demo">
    <div className="guided-demo-hero">
      <div><span className="eyebrow">NORTHSTAR COMMERCE · END-TO-END SCENARIOS</span>
        <h2>Follow the enterprise digital thread</h2>
        <p>Choose a journey to run its declared entrypoint-to-target path against the current authoritative graph. Results and API errors below come directly from the live service.</p>
      </div>
      <button className="secondary-button" onClick={() => run(loadScenarios)} disabled={busy}>Refresh scenario catalog</button>
    </div>
    {loadError && <div className="guided-demo-state error" role="alert"><strong>Scenario catalog unavailable</strong><span>{loadError}</span></div>}
    {!catalog && !loadError && <div className="guided-demo-state" role="status"><span className="spinner"/><span>Loading scenarios from the local API…</span></div>}
    {catalog && catalog.scenarios.length === 0 && <div className="guided-demo-state" role="status"><strong>No enterprise scenarios available</strong><span>The local API returned an empty scenario catalog.</span></div>}
    {catalog && catalog.scenarios.length > 0 && <>
      <div className="guided-demo-summary"><strong>{catalog.title}</strong><span>{catalog.scenarios.length} scenarios · dataset {catalog.dataset_id} v{catalog.version}</span><span>{catalog.description}</span></div>
      <div className="guided-demo-grid">{catalog.scenarios.map((scenario, index) => {
        const outcome = outcomes[scenario.id];
        const pathState = scenario.expected_path_state || [];
        return <article className="guided-scenario" key={scenario.id} data-testid={`scenario-${scenario.id}`}>
          <div className="guided-scenario-heading"><span className="guided-scenario-number">{String(index + 1).padStart(2, '0')}</span><StatusPill status={scenario.ready ? 'READY' : 'DATA MISSING'}/></div>
          <h3>{scenario.title}</h3>
          <p className="guided-scenario-audience">{scenario.audience}</p>
          <p>{scenario.story}</p>
          <div className="guided-capabilities">{(scenario.capabilities || []).map(capability => <span key={capability}>{capability}</span>)}</div>
          <details className="guided-path"><summary>Declared path · {scenario.expected_path?.length || 0} entities</summary>
            <ol>{(scenario.expected_path || []).map((entityId, pathIndex) => <li key={entityId}><StatusPill status={pathState[pathIndex]?.available ? 'AVAILABLE' : 'MISSING'}/><code title={entityId}>{entityId}</code></li>)}</ol>
          </details>
          <button className="primary-button guided-run" onClick={() => executeScenario(scenario)} disabled={busy || outcome?.status === 'RUNNING'}>Run declared path <Icon name="arrow" size={16}/></button>
          {outcome && <div className={`guided-outcome ${outcome.status.toLowerCase()}`} role="status" aria-label={`${scenario.title} result`}>
            {outcome.status === 'RUNNING' ? <><span className="spinner"/>Running live path query…</> :
              outcome.status === 'ERROR' ? <><strong>API error</strong><span>{outcome.error}</span></> :
                <><strong>{outcome.response.paths?.length ? 'Path returned' : 'No path returned'}</strong>
                  <pre>{JSON.stringify(outcome.response, null, 2)}</pre></>}
          </div>}
        </article>;
      })}</div>
    </>}
  </section>;
}

function GraphLegend({nodes}) {
  const types = [...new Set(nodes.map(node => node.label))];
  return types.length ? <div className="graph-legend" aria-label="Entity type legend">{types.map(type => <Tip text={`${type} entity`} key={type}><span><i style={{background: palette[type] || '#64748b'}}/>{type}</span></Tip>)}</div> : null;
}

function EntityInspector({selected, detail, selectedEdge, onImpact, onTrace, onLineage, busy}) {
  const [tab, setTab] = useState('overview');
  const [copiedId, setCopiedId] = useState(false);
  const [propFilter, setPropFilter] = useState('');

  useEffect(() => {
    setTab('overview');
    setPropFilter('');
  }, [selected?.id, selectedEdge?.id]);

  if (selectedEdge) return <section className="inspector panel" aria-label="Relationship inspector"><div className="inspector-heading"><span className="entity-symbol edge"><Icon name="link"/></span><div><span className="eyebrow">RELATIONSHIP</span><h2>{selectedEdge.type}</h2></div></div><div className="edge-route"><code title={selectedEdge.from_id}>{shortId(selectedEdge.from_id)}</code><span><Icon name="arrow" size={15}/></span><code title={selectedEdge.to_id}>{shortId(selectedEdge.to_id)}</code></div><h3>Why does this edge exist?</h3>{selectedEdge.properties?.source_ref || selectedEdge.properties?.evidence_key ? <div className="evidence-card"><Icon name="shield"/><div><strong>{selectedEdge.properties.source_ref || 'Graph evidence'}</strong><small>{selectedEdge.properties.evidence_key || 'Evidence key unavailable'}</small></div></div> : <p className="subtle">No direct evidence reference was returned for this relationship.</p>}<dl className="property-list">{Object.entries(selectedEdge.properties || {}).map(([key, value]) => <div key={key}><dt>{key.replaceAll('_', ' ')}</dt><dd>{String(value)}</dd></div>)}</dl></section>;
  if (!selected) return <section className="inspector panel"><EmptyState icon="focus" title="Select an entity">Choose a node on the map or an item in the result list to inspect its identity, properties, and evidence.</EmptyState></section>;
  
  const evidenceEdges = [...(detail?.outgoing || []), ...(detail?.incoming || [])].filter(edge => edge.properties?.source_ref || edge.properties?.evidence_key);
  const allProps = Object.entries(selected.properties || {});
  const filteredProps = propFilter ? allProps.filter(([k, v]) => k.toLowerCase().includes(propFilter.toLowerCase()) || String(v).toLowerCase().includes(propFilter.toLowerCase())) : allProps;

  return <section className="inspector panel" aria-label="Entity inspector">
    <div className="inspector-heading">
      <span className="entity-symbol" style={{'--entity-color': palette[selected.label] || '#64748b'}}>
        {displayLabel(selected).slice(0, 1).toUpperCase()}
      </span>
      <div>
        <span className="eyebrow">{selected.label}</span>
        <h2>{displayLabel(selected)}</h2>
      </div>
    </div>
    <div className="inspector-tabs" role="tablist">
      <button className={tab === 'overview' ? 'active' : ''} onClick={() => setTab('overview')} role="tab">Overview</button>
      <button className={tab === 'evidence' ? 'active' : ''} onClick={() => setTab('evidence')} role="tab">Evidence <span>{evidenceEdges.length}</span></button>
    </div>
    {tab === 'overview' ? <>
      <div className="identity-bar">
        <code className="identity" title={selected.id}>{selected.id}</code>
        <Tip text={copiedId ? "Copied ID!" : "Copy canonical ID"}>
          <button 
            type="button" 
            className="copy-chip-btn" 
            onClick={() => {
              navigator.clipboard.writeText(selected.id);
              setCopiedId(true);
              setTimeout(() => setCopiedId(false), 2000);
            }}
          >
            <Icon name={copiedId ? 'check' : 'copy'} size={13}/>
          </button>
        </Tip>
      </div>
      <div className="inspector-actions">
        <button disabled={busy} onClick={onImpact} title="Traverse bounded downstream impact"><Icon name="activity" size={16}/>Explore impact</button>
        <button className="secondary-button" disabled={busy} onClick={onTrace} title="Run the deterministic TraceImpact agent"><Icon name="spark" size={16}/>Run TraceImpact</button>
        <IconButton label="Trace provenance lineage" icon="shield" onClick={onLineage} disabled={busy}/>
      </div>
      <div style={{display: 'flex', justifyContent: 'space-between', alignItems: 'center', margin: '20px 0 8px'}}>
        <h3 style={{margin: 0}}>Entity properties ({filteredProps.length})</h3>
        {allProps.length > 4 && (
          <input 
            type="text" 
            placeholder="Filter props…" 
            value={propFilter} 
            onChange={e => setPropFilter(e.target.value)} 
            className="prop-filter-box"
          />
        )}
      </div>
      <dl className="property-list">
        {filteredProps.map(([key, value]) => (
          <div key={key}>
            <dt>{key.replaceAll('_', ' ')}</dt>
            <dd>{String(value)}</dd>
          </div>
        ))}
      </dl>
    </> : <>
      <p className="subtle">Source references returned for relationships connected to this entity.</p>
      {evidenceEdges.length ? (
        <div className="evidence-stack">
          {evidenceEdges.map((edge, index) => (
            <div className="evidence-card" key={edge.eid || edge.id || index}>
              <Icon name="shield"/>
              <div>
                <strong>{edge.label || edge.type}</strong>
                <small>{edge.properties?.source_ref || edge.properties?.evidence_key}</small>
              </div>
            </div>
          ))}
        </div>
      ) : (
        <EmptyState icon="shield" title="No direct evidence returned">Try the Evidence lens to retrieve a broader lineage chain.</EmptyState>
      )}
    </>}
  </section>;
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
  const cyRef = useRef(null);
  const [domain, setDomain] = useState('ALL');
  const [relationship, setRelationship] = useState('ALL');
  const [trust, setTrust] = useState('ALL');
  const domains = ['ALL', ...new Set((graph.nodes || []).map(node => node.domain).filter(Boolean))];
  const relationships = ['ALL', ...new Set((graph.edges || []).map(edge => edge.type).filter(Boolean))];
  const visibleNodes = domain === 'ALL' ? graph.nodes || [] : (graph.nodes || []).filter(node => node.domain === domain);
  const ids = new Set(visibleNodes.map(node => node.id));
  const visibleEdges = (graph.edges || []).filter(edge => ids.has(edge.from_id) && ids.has(edge.to_id) && (relationship === 'ALL' || edge.type === relationship) && (trust === 'ALL' || String(edge.creation_status || edge.properties?.creation_status || 'DETERMINISTIC').toUpperCase() === trust));
  return <div className="explorer-grid"><section className="panel graph-panel"><div className="panel-heading"><div><span className="eyebrow">LIVE SUBGRAPH</span><h2>Relationship map</h2><p>Explore typed, evidence-aware connections. Results stay bounded for browser safety.</p></div><div className="panel-tools"><label className="select-control" title="Show entities from one graph domain"><Icon name="filter" size={15}/><select aria-label="Filter graph by domain" value={domain} onChange={event => setDomain(event.target.value)}>{domains.map(item => <option key={item}>{item}</option>)}</select></label><label className="select-control" title="Show one relationship class"><Icon name="link" size={15}/><select aria-label="Filter graph by relationship" value={relationship} onChange={event => setRelationship(event.target.value)}>{relationships.map(item => <option key={item}>{item}</option>)}</select></label><label className="select-control" title="Filter deterministic or inferred relationships"><Icon name="shield" size={15}/><select aria-label="Filter graph by trust status" value={trust} onChange={event => setTrust(event.target.value)}><option value="ALL">All trust</option><option value="DETERMINISTIC">Deterministic</option><option value="INFERRED">Inferred</option></select></label><span className="count-badge">{visibleNodes.length} entities</span></div></div>{(graph.warnings || []).length > 0 && <div className="inline-notice warning"><Icon name="warning"/>{graph.warnings.join(' ')}</div>}{graph.partial && <div className="inline-notice"><Icon name="info"/>This is a bounded result. Expand a specific entity to retrieve more context.</div>}<GraphEnhancementToolbar cyRef={cyRef} nodes={visibleNodes} edges={visibleEdges}><GraphCanvas cyRef={cyRef} nodes={visibleNodes} edges={visibleEdges} paths={graph.paths || []} selectedId={selected?.id} selectedEdgeId={selectedEdge?.id} onSelectNode={onInspect} onSelectEdge={onInspectEdge} onExpand={onExpand}/></GraphEnhancementToolbar><GraphLegend nodes={visibleNodes}/><div className="edge-key"><span><i className="deterministic"/>Deterministic</span><span><i className="inferred"/>Inferred</span><span><i className="path"/>Highlighted path</span><span><Icon name="shield" size={12}/>Thicker links include evidence</span></div><div className="entity-strip"><div className="entity-strip-title"><strong>Entities in view</strong><small>Select an item to inspect it</small></div><div className="entity-list">{visibleNodes.map(node => <button key={node.id} disabled={busy} onClick={() => onInspect(node)} className={selected?.id === node.id ? 'selected' : ''} title={`Inspect ${displayLabel(node)}`}><span className="type-dot" style={{background: palette[node.label] || '#64748b'}}/><span><strong>{displayLabel(node)}</strong><small>{node.label}</small></span><Icon name="chevron" size={14}/></button>)}</div></div></section><EntityInspector selected={selected} detail={detail} selectedEdge={selectedEdge} onImpact={onImpact} onTrace={onTrace} onLineage={onLineage} busy={busy}/></div>;
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

function Explorer({stats, graph, setGraph, selected, setSelected, detail, setDetail, selectedEdge, setSelectedEdge, lens, setLens, api, run, busy, token}) {
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
    <section className="hero-search">
      <div className="hero-copy">
        <h2>Explore knowledge</h2>
      </div>
      
      <form onSubmit={executeSearch} className="global-search">
        <Icon name="search" size={21}/>
        <input 
          id="global-search-input"
          aria-label="Search knowledge graph" 
          value={query} 
          onChange={event => setQuery(event.target.value)} 
          placeholder="Search entities and relationships"
          required
        />
        {query && (
          <button 
            type="button" 
            className="input-clear-btn" 
            onClick={() => setQuery('')} 
            title="Clear search input"
          >
            <Icon name="close" size={14}/>
          </button>
        )}
        <button disabled={busy} title="Search the persisted knowledge graph">Search graph <span>↵</span></button>
      </form>
      <div className="search-suggestions">
        <span>Suggested:</span>
        {['EOIP-1', 'Order', 'Payment', 'Service', 'Authentication'].map(item => (
          <button 
            key={item} 
            type="button" 
            onClick={() => {
              setQuery(item);
              run(async () => {
                setGraph(await api(`/api/v1/search?q=${encodeURIComponent(item)}`));
                setSelected(null); setSelectedEdge(null); setTrace(null);
              });
            }}
          >
            {item}
          </button>
        ))}
      </div>

      <form onSubmit={askNaturalLanguage} className="global-search nl-search" style={{marginTop: 12}}>
        <Icon name="spark" size={21}/>
        <input 
          aria-label="Ask the knowledge graph" 
          value={nlQuestion} 
          onChange={event => setNlQuestion(event.target.value)} 
          placeholder="Ask in plain language — e.g. what implements EOIP-1, what is impacted by a symbol…" 
          required
        />
        {nlQuestion && (
          <button 
            type="button" 
            className="input-clear-btn" 
            onClick={() => setNlQuestion('')} 
            title="Clear question input"
          >
            <Icon name="close" size={14}/>
          </button>
        )}
        <button disabled={busy} title="Interpret the question as a bounded, policy-checked QueryPlan">Ask graph <span>↵</span></button>
      </form>
      <div className="search-suggestions" style={{marginTop: 8}}>
        <span>Ask:</span>
        {['What implements EOIP-1?', 'What is impacted by payment-svc?', 'Explain checkout dependencies'].map(item => (
          <button 
            key={item} 
            type="button" 
            onClick={() => {
              setNlQuestion(item);
              run(async () => {
                const response = await api('/api/v1/query/nl', {question: item});
                setNlResult(response);
                if (response.result) {
                  setGraph(response.result);
                  setSelected(null); setSelectedEdge(null); setTrace(null);
                }
              });
            }}
          >
            {item}
          </button>
        ))}
      </div>

      {nlResult && <div className="inline-notice nl-interpretation" role="status">
        <Icon name={nlResult.interpretation?.plan ? 'check' : 'info'}/>
        {nlResult.interpretation?.plan ? <span>Interpreted as <strong>{nlResult.interpretation.plan.intent}</strong> plan{nlResult.interpretation.explanation ? ` — ${nlResult.interpretation.explanation}` : ''}{nlResult.result ? ` · ${nlResult.result.nodes?.length || 0} entities returned` : ''}</span> : <span>{nlResult.interpretation?.clarification || 'The question could not be mapped to a bounded query plan.'}</span>}
      </div>}
    </section>
    <div className="metrics-grid"><MetricCard icon="database" eyebrow="ENTITIES" value={stats?.vertices ?? '—'} caption="Persisted canonical facts" tone="violet" tooltip="Canonical entities currently stored in HugeGraph"/><MetricCard icon="graph" eyebrow="RELATIONSHIPS" value={stats?.edges ?? '—'} caption="Typed semantic links" tone="blue" tooltip="Typed relationships currently stored in HugeGraph"/><MetricCard icon="layers" eyebrow="ENTITY TYPES" value={stats ? Object.values(stats.labels || {}).filter(value => value > 0).length : '—'} caption={`${Object.keys(stats?.labels || {}).length || 0} types available`} tone="mint" tooltip="Ontology entity types represented by at least one stored entity"/><MetricCard icon="activity" eyebrow="WORKER" value={stats?.worker?.status || 'Starting'} caption={stats?.worker?.updated_at ? `Updated ${formatTime(stats.worker.updated_at)}` : 'Background ingestion service'} tone="coral" tooltip="Current background ingestion worker state"/></div>
    <div className="lens-bar" role="tablist" aria-label="Explorer lenses"><div>{lenses.map(item => <Tip text={item.hint} key={item.id}><button role="tab" aria-selected={lens === item.id} className={lens === item.id ? 'active' : ''} onClick={() => setLens(item.id)}><Icon name={item.icon}/>{item.label}</button></Tip>)}<Tip text="Browse every documented experience lens and its implementation state"><button onClick={() => setLibraryOpen(true)}><Icon name="plus"/>All lenses</button></Tip></div><span className="context-actions"><span className="context-chip"><Icon name="focus" size={14}/>{selected ? displayLabel(selected) : 'No entity selected'}</span><IconButton label="Export the current local lens context" icon="upload" onClick={exportContext}/></span></div>
    {lens === 'search' && <SearchView graph={graph} selected={selected} onInspect={node => run(() => inspect(node))}/>}
    {lens === 'graph' && <GraphView graph={graph} selected={selected} detail={detail} selectedEdge={selectedEdge} onInspect={node => run(() => inspect(node))} onInspectEdge={edge => {setSelectedEdge(edge); setSelected(null);}} onExpand={expand} onImpact={impact} onTrace={traceImpact} onLineage={traceLineage} busy={busy}/>} 
    {lens === 'impact' && <ImpactView source={source} setSource={setSource} target={target} setTarget={setTarget} selected={selected} graph={graph} trace={trace} onPath={findPath} onImpact={impact} onTrace={traceImpact} busy={busy}/>} 
    {lens === 'evidence' && <EvidenceView source={source} setSource={setSource} selected={selected} lineage={lineage} rag={rag} question={question} setQuestion={setQuestion} onLineage={traceLineage} onRag={retrieve} onInspect={node => run(() => inspect(node))} busy={busy}/>} 
    {lens === 'architecture' && <ArchitectureView stats={stats} graph={graph}/>}
    {lens === 'agent' && <AgentView agents={agents} selectedAgent={selectedAgent} setSelectedAgent={setSelectedAgent} goal={agentGoal} setGoal={setAgentGoal} selected={selected} result={agentResult} onRun={runAgent} busy={busy} synthesize={agentSynthesize} setSynthesize={setAgentSynthesize}/>}
    {lens === 'kgr' && <KGRExplorer graph={graph} setGraph={setGraph} api={api} run={run} busy={busy} stats={stats} apiBase={window.location.origin} token={token}/>}
    <LensLibrary open={libraryOpen} onClose={() => setLibraryOpen(false)} onSelect={openCatalogLens}/>
  </>;
}

function ConnectorCard({icon, name, description, status = 'Available', children, tone}) {
  return <article className={`connector-card ${tone || ''}`}><div className="connector-top"><span className="connector-icon"><Icon name={icon}/></span><StatusPill status={status}/></div><h3>{name}</h3><p>{description}</p>{children}</article>;
}

function JobsTable({jobs, jobSummary, onCancel, onReadmit}) {
  if (!jobs.length) return <EmptyState icon="clock" title="No ingestion jobs yet">Load the demo or import a source to create the first durable job.</EmptyState>;
  return <div className="table-wrap"><table><thead><tr><th>Source</th><th>Status</th><th>Created</th><th>Result</th>{onCancel && <th>Action</th>}</tr></thead><tbody>{jobs.map(job => <tr key={job.job_id}><td><div className="table-primary"><span className="service-icon mini"><Icon name={job.kind === 'DEMO' ? 'spark' : 'upload'} size={15}/></span><span><strong>{job.kind.replaceAll('_', ' ')}</strong><small title={job.job_id}>{shortId(job.job_id, 18)}</small></span></div></td><td><StatusPill status={job.status}/></td><td>{formatTime(job.created_at)}</td><td>{job.status === 'HELD' ? 'Recovery hold: review possible side effects before re-admission' : job.error || (job.result ? jobSummary(job) : job.status === 'CANCELLED' ? 'Cancelled before execution' : 'Waiting for worker')}</td>{onCancel && <td>{['PENDING', 'HELD'].includes(job.status) ? <><button className="table-action" onClick={() => onCancel(job.job_id)}>Cancel</button>{job.status === 'HELD' && onReadmit && <button className="table-action" onClick={() => onReadmit(job.job_id)}>Readmit</button>}</> : <span className="subtle">—</span>}</td>}</tr>)}</tbody></table></div>;
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
    const replayable = Boolean(item.event_id);
    return <tr key={item.event_id || index}>
      <td><strong>{item.source_system || 'Unknown source'}</strong><small>{item.error_category || item.stage || 'Unknown category'}</small></td>
      <td>{item.error || item.error_message || 'Rejected record'}</td>
      <td><code title={item.event_id || ''}>{shortId(item.source_record_id || item.event_id || '', 24)}</code></td>
      <td><code title={item.payload_hash || ''}>{shortId(item.payload_hash || '', 20)}</code></td>
      <td>{replayable && item.event_id ? <button className="table-action" onClick={() => onReplay(item.event_id)} disabled={busy}>Replay</button> : <span className="subtle">Not supported</span>}</td>
    </tr>;
  })}</tbody></table></div>;
}

function SourceRegistryTable({sources, onLoad, onOperation, onDiscover, onToggle, onDelete, busy}) {
  if (!sources) return <EmptyState icon="database" title="Source registry is not loaded">Load registered sources to operate baseline, sync, discovery, reconciliation and replay flows.</EmptyState>;
  if (!sources.length) return <EmptyState icon="database" title="No registered sources">Create a governed source from the connector catalog to begin acquisition.</EmptyState>;
  return <div className="table-wrap"><table><thead><tr><th>Source</th><th>Health</th><th>Modes</th><th>Checkpoint</th><th>Operations</th></tr></thead><tbody>{sources.map(source => {
    const caps = source.capabilities || {};
    return <tr key={source.source_id}>
      <td><div className="table-primary"><span className="service-icon mini"><Icon name="database" size={15}/></span><span><strong>{source.name || source.source_id}</strong><small>{source.source_id} · {source.source_type}</small></span></div></td>
      <td><StatusPill status={source.enabled ? (source.health || 'UNKNOWN') : 'DISABLED'}/></td>
      <td>{(source.acquisition_modes || []).join(', ') || 'baseline'}</td>
      <td><code title={source.checkpoint || ''}>{shortId(source.checkpoint || source.last_incremental_run || source.last_successful_baseline || '', 22)}</code></td>
      <td><div className="table-actions">
        {caps.discovery && <button className="table-action" onClick={() => onDiscover(source.source_id)} disabled={busy}>Discover</button>}
        {caps.baseline && <button className="table-action" onClick={() => onOperation(source.source_id, 'baseline')} disabled={busy}>Baseline</button>}
        <button className="table-action" onClick={() => onOperation(source.source_id, 'dry-run')} disabled={busy}>Dry run</button>
        {caps.polling && <button className="table-action" onClick={() => onOperation(source.source_id, 'sync')} disabled={busy}>Sync</button>}
        {caps.reconciliation && <button className="table-action" onClick={() => onOperation(source.source_id, 'reconcile')} disabled={busy}>Reconcile</button>}
        {caps.replay && <button className="table-action" onClick={() => onOperation(source.source_id, 'replay')} disabled={busy}>Replay</button>}
        <button className="table-action" onClick={() => onToggle(source)} disabled={busy}>{source.enabled ? 'Disable' : 'Enable'}</button>
        <button className="table-action danger" onClick={() => onDelete(source.source_id)} disabled={busy}>Delete</button>
      </div></td>
    </tr>;
  })}</tbody></table><div className="table-footer"><button className="secondary-button" onClick={onLoad} disabled={busy}><Icon name="refresh"/>Refresh registry</button></div></div>;
}

function SourceOnboarding({catalog, draft, setDraft, onSubmit, busy}) {
  const connectors = catalog || [];
  const selected = connectors.find(connector => connector.id === draft.sourceType);
  function choose(type) {
    const connector = connectors.find(item => item.id === type);
    const mappedType = type === 'local_code' ? 'local_files' : type;
    setDraft(current => ({
      ...current,
      sourceType: mappedType,
      name: current.name || connector?.name || mappedType,
      sourceId: current.sourceId || `${mappedType}-prod`,
    }));
  }
  return <section className="panel span-3"><div className="panel-heading"><div><span className="eyebrow">SOURCE ONBOARDING</span><h2>Registry and discovery</h2><p>Create non-secret source entries, then run discovery or dry-run acquisition from the registry.</p></div></div>
    <div className="connector-catalog-strip">{connectors.map(connector => <button key={connector.id} type="button" className={draft.sourceType === connector.id || draft.sourceType === 'local_files' && connector.id === 'local_code' ? 'active' : ''} onClick={() => choose(connector.id)}><Icon name={connector.type === 'crawler' ? 'search' : connector.type === 'file' ? 'document' : 'link'} size={14}/><span>{connector.name}</span><small>{(connector.capabilities || []).join(', ')}</small></button>)}</div>
    <form className="source-form" onSubmit={event => {event.preventDefault(); onSubmit();}}>
      <label>Source ID<input value={draft.sourceId} onChange={event => setDraft(current => ({...current, sourceId: event.target.value}))} placeholder="jira-prod" required/></label>
      <label>Source type<select value={draft.sourceType} onChange={event => setDraft(current => ({...current, sourceType: event.target.value}))}>
        {['jira', 'gitlab', 'github', 'confluence', 'servicenow', 'rally', 'grafana', 'datadog', 'kibana', 'qtest', 'figma', 'api_portal', 'web', 'local_files'].map(type => <option key={type} value={type}>{type}</option>)}
      </select></label>
      <label>Name<input value={draft.name} onChange={event => setDraft(current => ({...current, name: event.target.value}))} placeholder={selected?.name || 'Production source'} required/></label>
      <label>Base URL<input value={draft.baseUrl} onChange={event => setDraft(current => ({...current, baseUrl: event.target.value}))} placeholder="https://example.local"/></label>
      <label>Token secret ref<input value={draft.secretRef} onChange={event => setDraft(current => ({...current, secretRef: event.target.value}))} placeholder="env://JIRA_TOKEN"/></label>
      <button className="primary-button" type="submit" disabled={busy}><Icon name="plus"/>Create source</button>
    </form>
  </section>;
}

function LiveOpsPanel({api, run, busy}) {
  const [preflight, setPreflight] = useState(null);
  const [metrics, setMetrics] = useState('');
  const load = () => run(async () => {
    const [p, m] = await Promise.all([api('/api/v1/ops/preflight'), fetch('/metrics').then(r => r.text())]);
    setPreflight(p); setMetrics(m);
  });
  useEffect(() => {load();}, []);
  return <div className="admin-grid">
    <section className="panel span-2"><div className="panel-heading"><div><span className="eyebrow">REAL-TIME OPERATIONS</span><h2>Preflight and metrics</h2></div><button className="secondary-button" onClick={load} disabled={busy}><Icon name="refresh"/>Refresh</button></div>
      {preflight ? <div className="preflight-grid">{(preflight.checks || []).map(check => <article key={check.name} className={`preflight-card ${check.status}`}><StatusPill status={check.status}/><strong>{check.name}</strong><small>{check.detail}</small></article>)}</div> : <EmptyState icon="activity" title="Operations data not loaded">Refresh to read current preflight checks.</EmptyState>}
    </section>
    <section className="panel"><div className="panel-heading"><div><span className="eyebrow">PROMETHEUS</span><h2>Metrics sample</h2></div></div><pre className="processing-log">{metrics.split('\n').filter(line => line && !line.startsWith('#')).slice(0, 28).join('\n') || 'No metrics returned yet.'}</pre></section>
  </div>;
}

function DiscoveryResult({result}) {
  if (!result) return null;
  const items = result.items || result.resources || result.entities || [];
  return <section className="panel span-3"><div className="panel-heading"><div><span className="eyebrow">DISCOVERY RESULT</span><h2>{result.source_id || result.source || 'Source discovery'}</h2><p>Preview returned by the connector without materializing graph changes.</p></div><StatusPill status={result.status || 'COMPLETE'}/></div>
    <pre className="code-panel">{JSON.stringify({...result, items: items.slice ? items.slice(0, 20) : items}, null, 2)}</pre>
  </section>;
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
  const [sources, setSources] = useState(null);
  const [connectorCatalog, setConnectorCatalog] = useState(null);
  const [sourceDiscovery, setSourceDiscovery] = useState(null);
  const [sourceDraft, setSourceDraft] = useState({sourceId: '', sourceType: 'jira', name: '', baseUrl: '', secretRef: ''});
  const [ontology, setOntology] = useState(null);
  const [ontologySchema, setOntologySchema] = useState(null);
  const [federation, setFederation] = useState(null);
  const [section, setSection] = useState('overview');
  const [checkpoint, setCheckpoint] = useState('');
  const [dryRun, setDryRun] = useState(true);
  const [jsonFiles, setJsonFiles] = useState([]);
  const [ingestionResult, setIngestionResult] = useState(null);
  const [convertResult, setConvertResult] = useState(null);
  const [availableFormats, setAvailableFormats] = useState(null);
  const [selectedFormat, setSelectedFormat] = useState('rdf');
  const [ingestionLog, setIngestionLog] = useState([]);
  const [dragOver, setDragOver] = useState(false);
  const finishedJobs = jobs.filter(job => ['SUCCEEDED', 'PARTIAL', 'FAILED', 'CANCELLED'].includes(job.status));
  const successRate = finishedJobs.length ? Math.round(finishedJobs.filter(job => job.status === 'SUCCEEDED').length / finishedJobs.length * 100) : null;
  const jobSummary = job => {const result = job.result || {}; return job.kind === 'DEMO' ? `${result.jira?.records_accepted || 0} Jira · ${result.git?.files || 0} files · ${result.git?.symbols || 0} symbols` : `${result.records_accepted || 0} accepted · ${result.records_rejected || 0} rejected`;};
  async function importFile(file, endpoint) {if (!file) return; if (file.size > 3_000_000) throw new Error('Select a JSON file smaller than 3 MB'); await api(endpoint, {document: JSON.parse(await file.text())}); await refresh();}
  const submitSync = source => run(async () => {await api(`/api/v1/admin/ingestion/${source}`, {checkpoint: checkpoint || null, watermark: null, dry_run: dryRun}); await refresh();});
  const loadSourceControl = () => run(async () => {
    const [nextSources, catalog] = await Promise.all([api('/api/v1/sources'), api('/api/v1/connectors/catalog')]);
    setSources(nextSources);
    setConnectorCatalog(catalog.connectors || []);
  });
  const createRegistrySource = () => run(async () => {
    const catalogItem = (connectorCatalog || []).find(item => item.id === sourceDraft.sourceType || (sourceDraft.sourceType === 'local_files' && item.id === 'local_code'));
    const modes = catalogItem?.capabilities || ['baseline'];
    const capabilities = {
      baseline: modes.includes('baseline'),
      polling: modes.includes('poll'),
      webhooks: modes.includes('webhook'),
      discovery: true,
      reconciliation: modes.includes('reconcile'),
      replay: modes.includes('replay'),
    };
    const payload = {
      source_id: sourceDraft.sourceId,
      source_type: sourceDraft.sourceType,
      name: sourceDraft.name || sourceDraft.sourceId,
      base_url: sourceDraft.baseUrl || null,
      capabilities,
      secret_refs: sourceDraft.secretRef ? {token: sourceDraft.secretRef} : {},
    };
    await api('/api/v1/sources', payload);
    setSourceDraft({sourceId: '', sourceType: 'jira', name: '', baseUrl: '', secretRef: ''});
    const nextSources = await api('/api/v1/sources');
    setSources(nextSources);
  });
  const sourceOperation = (sourceId, operation) => run(async () => {
    const body = operation === 'dry-run' ? {checkpoint: checkpoint || null, dry_run: true} : {checkpoint: checkpoint || null, dry_run: dryRun};
    await api(`/api/v1/sources/${encodeURIComponent(sourceId)}/${operation}`, body);
    await refresh();
  });
  const discoverSource = sourceId => run(async () => setSourceDiscovery(await api(`/api/v1/sources/${encodeURIComponent(sourceId)}/discover`, {})));
  const toggleSource = source => run(async () => {
    await api(`/api/v1/sources/${encodeURIComponent(source.source_id)}`, {enabled: !source.enabled}, 'PATCH');
    setSources(await api('/api/v1/sources'));
  });
  const deleteSource = sourceId => {
    if (window.confirm(`Delete source ${sourceId}?`)) {
      run(async () => {
        await api(`/api/v1/sources/${encodeURIComponent(sourceId)}`, undefined, 'DELETE');
        setSources(await api('/api/v1/sources'));
      });
    }
  };
  const cancelJob = jobId => run(async () => {await api(`/api/v1/admin/jobs/${encodeURIComponent(jobId)}/cancel`, {}); await refresh();});
  const readmitJob = jobId => {
    if (window.confirm('Re-admit this recovered job? Execution may repeat side effects from before the backup.')) {
      run(async () => {await api(`/api/v1/admin/jobs/${encodeURIComponent(jobId)}/readmit`, {}); await refresh();});
    }
  };
  const replayDlq = eventId => run(async () => {await api(`/api/v1/admin/dlq/${encodeURIComponent(eventId)}/replay`, {}); setDlq(await api('/api/v1/admin/dlq?limit=25')); await refresh();});
  return <>
    <div className="admin-summary"><div><span className="eyebrow"><i/>OPERATIONS OVERVIEW</span><h2>Keep enterprise knowledge trustworthy.</h2><p>Monitor source ingestion, graph quality, ontology state, and auditable platform activity from one control plane.</p></div><div className="admin-summary-actions"><button className="secondary-button" onClick={() => run(async () => {setValidation(await api('/api/v1/admin/validation', {})); setSection('quality');})} disabled={busy} title="Validate current graph facts and open quality results"><Icon name="shield"/>Run validation</button><button className="primary-button" onClick={() => run(async () => {await api('/api/v1/admin/demo', {}); await refresh();})} disabled={busy} title="Queue an idempotent demo ingestion run"><Icon name="spark"/>Load / replay demo</button></div></div>
    <div className="metrics-grid admin-metrics"><MetricCard icon="database" eyebrow="GRAPH ENTITIES" value={stats?.vertices ?? '—'} caption="Authoritative graph store" tone="violet"/><MetricCard icon="graph" eyebrow="RELATIONSHIPS" value={stats?.edges ?? '—'} caption="Across all graph domains" tone="blue"/><MetricCard icon="activity" eyebrow="JOB SUCCESS" value={successRate === null ? '—' : `${successRate}%`} caption={`${finishedJobs.length} completed runs`} tone="mint" tooltip="Success rate calculated from completed jobs returned by the API"/><MetricCard icon="shield" eyebrow="SCHEMA" value={stats?.schema?.schema_version || '—'} caption={`Ontology ${stats?.schema?.ontology_version || 'unavailable'}`} tone="gold"/></div>
    <div className="admin-tabs" role="tablist">{[['overview', 'Overview', 'layers'], ['sources', 'Sources & jobs', 'upload'], ['ingestion', 'JSON Ingestion & Convert', 'database'], ['quality', 'Quality & ontology', 'shield'], ['security', 'Users & policy', 'shield'], ['liveops', 'Live operations', 'activity'], ['operations', 'Audit & recovery', 'terminal']].map(([id, label, icon]) => <button key={id} role="tab" aria-selected={section === id} className={section === id ? 'active' : ''} onClick={() => setSection(id)} title={`Open ${label}`}><Icon name={icon}/>{label}</button>)}</div>
    {section === 'overview' && <div className="admin-grid">
      <section className="panel span-2"><div className="panel-heading"><div><span className="eyebrow">RECENT ACTIVITY</span><h2>Ingestion jobs</h2><p>Durable worker jobs and their latest reported state.</p></div><button className="secondary-button" onClick={() => run(refresh)} disabled={busy}><Icon name="refresh"/>Refresh jobs</button></div><JobsTable jobs={jobs} jobSummary={jobSummary}/></section>
      <section className="panel"><div className="panel-heading"><div><span className="eyebrow">PLATFORM</span><h2>Service health</h2></div></div><div className="service-list"><div><span className="service-icon violet"><Icon name="database"/></span><span><strong>HugeGraph</strong><small>Authoritative graph store</small></span><StatusPill status={system?.graph?.status || (stats ? 'READY' : 'CHECKING')}/></div><div><span className="service-icon mint"><Icon name="activity"/></span><span><strong>Ingestion worker</strong><small>Background job processor</small></span><StatusPill status={stats?.worker?.status || 'STARTING'}/></div><div><span className="service-icon blue"><Icon name="shield"/></span><span><strong>Schema bootstrap</strong><small>Idempotent ontology schema</small></span><StatusPill status={stats?.schema ? 'READY' : 'CHECKING'}/></div><div><span className="service-icon coral"><Icon name="spark"/></span><span><strong>Local model</strong><small>{system?.model?.name || 'Optional deterministic fallback active'}</small></span><StatusPill status={system?.model?.status || 'CHECKING'}/></div><div><span className="service-icon gold"><Icon name="upload"/></span><span><strong>Backup state</strong><small>{system?.backup?.latest ? `${system.backup.latest.vertices} entities · ${formatTime(system.backup.latest.created_at)}` : 'No checksummed snapshot found'}</small></span><StatusPill status={system?.backup?.status || 'CHECKING'}/></div></div></section>
      <section className="panel span-3"><div className="panel-heading"><div><span className="eyebrow">ENTITY DISTRIBUTION</span><h2>Graph inventory</h2><p>Live counts by ontology label; zero-count types are intentionally visible.</p></div><span className="count-badge">{Object.keys(stats?.labels || {}).length} types</span></div><div className="inventory-grid">{Object.entries(stats?.labels || {}).map(([key, value]) => <Tip text={`${value} ${key} entities persisted`} key={key}><div className={value ? '' : 'zero'} tabIndex="0"><span className="type-dot" style={{background: palette[key] || '#94a3b8'}}/><span>{key}</span><strong>{value}</strong></div></Tip>)}</div></section>
    </div>}
    {section === 'sources' && <div className="admin-section">
      <div className="connector-grid"><ConnectorCard icon="spark" name="Demo dataset" description="Synthetic Jira, Git, code, pipeline, and documentation evidence." status="Ready" tone="violet"><button onClick={() => run(async () => {await api('/api/v1/admin/demo', {}); await refresh();})} disabled={busy}>Load dataset <Icon name="arrow"/></button></ConnectorCard><ConnectorCard icon="upload" name="Jira JSON" description="Import a configurable Jira export with record-level validation." status="File import" tone="blue"><label className="file-picker"><input type="file" accept="application/json,.json" onChange={event => setUpload(event.target.files?.[0] || null)}/><Icon name="document"/><span>{upload?.name || 'Choose JSON file'}</span></label><button onClick={() => run(() => importFile(upload, '/api/v1/admin/ingestion/jira'))} disabled={busy || !upload}>Import Jira <Icon name="arrow"/></button></ConnectorCard><ConnectorCard icon="code" name="GitLab metadata" description="Import merge request and pipeline metadata from JSON." status="File import" tone="coral"><label className="file-picker"><input type="file" accept="application/json,.json" onChange={event => setGitlabUpload(event.target.files?.[0] || null)}/><Icon name="document"/><span>{gitlabUpload?.name || 'Choose JSON file'}</span></label><button onClick={() => run(() => importFile(gitlabUpload, '/api/v1/admin/ingestion/gitlab'))} disabled={busy || !gitlabUpload}>Import GitLab <Icon name="arrow"/></button></ConnectorCard><ConnectorCard icon="document" name="Confluence" description="Queue incremental Data Center content synchronization." status="Configured externally" tone="mint"><button onClick={() => submitSync('confluence')} disabled={busy}>Queue dry run <Icon name="arrow"/></button></ConnectorCard><ConnectorCard icon="settings" name="ServiceNow" description="Queue incremental knowledge article synchronization." status="Configured externally" tone="gold"><button onClick={() => submitSync('servicenow')} disabled={busy}>Queue dry run <Icon name="arrow"/></button></ConnectorCard><ConnectorCard icon="layers" name="Rally" description="Import epics, features, and user stories from Rally/Broadcom." status="Configured externally" tone="violet"><button onClick={() => submitSync('rally')} disabled={busy}>Queue dry run <Icon name="arrow"/></button></ConnectorCard><ConnectorCard icon="activity" name="Grafana" description="Sync dashboards, alert rules, and data sources from Grafana." status="Configured externally" tone="mint"><button onClick={() => submitSync('grafana')} disabled={busy}>Queue dry run <Icon name="arrow"/></button></ConnectorCard><ConnectorCard icon="activity" name="Datadog" description="Sync dashboards and monitors from Datadog." status="Configured externally" tone="coral"><button onClick={() => submitSync('datadog')} disabled={busy}>Queue dry run <Icon name="arrow"/></button></ConnectorCard><ConnectorCard icon="terminal" name="Kibana" description="Import dashboards, saved searches, and index patterns from Kibana." status="Configured externally" tone="blue"><button onClick={() => submitSync('kibana')} disabled={busy}>Queue dry run <Icon name="arrow"/></button></ConnectorCard><ConnectorCard icon="shield" name="qTest" description="Import test cases, suites, cycles, and runs from qTest." status="Configured externally" tone="gold"><button onClick={() => submitSync('qtest')} disabled={busy}>Queue dry run <Icon name="arrow"/></button></ConnectorCard><ConnectorCard icon="focus" name="Figma" description="Import design files, pages, and components from Figma." status="Configured externally" tone="violet"><button onClick={() => submitSync('figma')} disabled={busy}>Queue dry run <Icon name="arrow"/></button></ConnectorCard><ConnectorCard icon="link" name="API Portal" description="Sync API services, endpoints, and Swagger connections." status="Configured externally" tone="blue"><button onClick={() => submitSync('api_portal')} disabled={busy}>Queue dry run <Icon name="arrow"/></button></ConnectorCard><ConnectorCard icon="code" name="GitHub" description="Import repositories, commits, and pull requests from GitHub." status="Configured externally" tone="coral"><button onClick={() => submitSync('github')} disabled={busy}>Queue dry run <Icon name="arrow"/></button></ConnectorCard></div>
      <section className="panel sync-options"><div><h2>Incremental sync options</h2><p>Applies to Confluence and ServiceNow jobs. Credentials remain in worker configuration.</p></div><label>Checkpoint<input value={checkpoint} onChange={event => setCheckpoint(event.target.value)} placeholder="Optional ISO-8601 checkpoint"/></label><label className="toggle"><input type="checkbox" checked={dryRun} onChange={event => setDryRun(event.target.checked)}/><span/>Dry run only</label></section>
      <SourceOnboarding catalog={connectorCatalog} draft={sourceDraft} setDraft={setSourceDraft} onSubmit={createRegistrySource} busy={busy}/>
      <Studio api={api} run={run} busy={busy}/>
      <section className="panel span-3"><div className="panel-heading"><div><span className="eyebrow">SOURCE REGISTRY</span><h2>Registered sources</h2><p>Operate baseline, discovery, dry run, sync, reconciliation and replay from the durable registry.</p></div><button className="secondary-button" onClick={loadSourceControl} disabled={busy}><Icon name="refresh"/>Load source control</button></div><SourceRegistryTable sources={sources} onLoad={loadSourceControl} onOperation={sourceOperation} onDiscover={discoverSource} onToggle={toggleSource} onDelete={deleteSource} busy={busy}/></section>
      <DiscoveryResult result={sourceDiscovery}/>
      <section className="panel"><div className="panel-heading"><div><span className="eyebrow">DURABLE QUEUE</span><h2>Ingestion jobs</h2></div><button className="secondary-button" onClick={() => run(refresh)} disabled={busy}><Icon name="refresh"/>Refresh counts</button></div><JobsTable jobs={jobs} jobSummary={jobSummary} onCancel={cancelJob} onReadmit={readmitJob}/></section>
    </div>}
    {section === 'ingestion' && <div className="admin-section admin-ingestion-panel">
      <section className="panel span-3">
        <div className="panel-heading"><div><span className="eyebrow">JSON INGESTION PIPELINE</span>
          <h2>Ingest JSON data into the knowledge graph</h2>
          <p>Upload JSON files to process entities, build relationships, metadata graphs, and convert to RDF, RDFS, OWL, Gremlin, Cypher, GQL, and SPARQL formats.</p>
        </div></div>

        <div className={`file-drop-zone ${dragOver ? 'dragover' : ''}`}
          onDragOver={e => { e.preventDefault(); setDragOver(true); }}
          onDragLeave={() => setDragOver(false)}
          onDrop={e => {
            e.preventDefault(); setDragOver(false);
            const files = Array.from(e.dataTransfer.files).filter(f => f.name.endsWith('.json'));
            setJsonFiles(prev => [...prev, ...files]);
          }}
          onClick={() => document.getElementById('json-file-input')?.click()}>
          <input id="json-file-input" type="file" accept="application/json,.json" multiple
            onChange={e => setJsonFiles(prev => [...prev, ...Array.from(e.target.files || [])])}/>
          <span className="section-icon violet"><Icon name="upload"/></span>
          <strong>Drop JSON files here or click to browse</strong>
          <small>Supports entity arrays, nested documents, and NormalizedEntity envelopes</small>
        </div>

        {jsonFiles.length > 0 && <div style={{marginTop: 12}}>
          <h3>{jsonFiles.length} file{jsonFiles.length !== 1 ? 's' : ''} selected</h3>
          <div className="ingestion-pipeline-grid">
            {jsonFiles.map((f, i) => <div key={`${f.name}-${i}`} className="pipeline-card">
              <div className="pipeline-card-header">
                <span className="section-icon blue"><Icon name="document"/></span>
                <div><h3>{f.name}</h3><p>{(f.size / 1024).toFixed(1)} KB</p></div>
              </div>
              <button className="table-action" onClick={() => setJsonFiles(prev => prev.filter((_, j) => j !== i))}>Remove</button>
            </div>)}
          </div>
          <div className="pipeline-actions" style={{marginTop: 12}}>
            <button className="primary-button" disabled={busy} onClick={() => run(async () => {
              setIngestionLog([]);
              let totalEntities = 0, totalRels = 0, allErrors = [];
              for (const file of jsonFiles) {
                const text = await file.text();
                const data = JSON.parse(text);
                setIngestionLog(prev => [...prev, {ts: new Date().toISOString().slice(11, 19), level: 'info', msg: `Processing ${file.name}...`}]);
                const result = await api('/api/v1/admin/ingestion/json', {data, source_label: file.name, pipeline_id: 'manual_gui'});
                totalEntities += result.entities_created || 0;
                totalRels += result.relationships_created || 0;
                if (result.errors?.length) allErrors.push(...result.errors);
                setIngestionLog(prev => [...prev, {ts: new Date().toISOString().slice(11, 19), level: result.error_count ? 'err' : 'ok', msg: `${file.name}: ${result.entities_created} entities, ${result.relationships_created} relationships${result.error_count ? `, ${result.error_count} errors` : ''}`}]);
              }
              setIngestionResult({entities_created: totalEntities, relationships_created: totalRels, error_count: allErrors.length, errors: allErrors.slice(0, 20)});
              setIngestionLog(prev => [...prev, {ts: new Date().toISOString().slice(11, 19), level: 'ok', msg: `All files processed: ${totalEntities} entities, ${totalRels} relationships created`}]);
              await refresh();
            })}><Icon name="database" size={16}/>Process & Build Graphs</button>
            <button className="primary-button" disabled={busy} onClick={() => run(async () => {
              setIngestionLog([]);
              for (const file of jsonFiles) {
                const text = await file.text();
                const data = JSON.parse(text);
                setIngestionLog(prev => [...prev, {ts: new Date().toISOString().slice(11, 19), level: 'info', msg: `Processing & converting ${file.name}...`}]);
                const result = await api('/api/v1/admin/ingestion/process-and-convert', {data, source_label: file.name, pipeline_id: 'manual_gui'});
                setIngestionResult(result.ingestion);
                setConvertResult(result.formats);
                setIngestionLog(prev => [...prev, {ts: new Date().toISOString().slice(11, 19), level: 'ok', msg: `${file.name}: ${result.ingestion?.entities_created || 0} entities, ${Object.keys(result.formats || {}).length} formats generated`}]);
              }
              await refresh();
            })}><Icon name="layers" size={16}/>Process, Build & Convert All Formats</button>
            <button className="secondary-button" onClick={() => { setJsonFiles([]); setIngestionResult(null); setConvertResult(null); setIngestionLog([]); }}>
              <Icon name="close" size={16}/>Clear all
            </button>
          </div>
        </div>}
      </section>

      {ingestionLog.length > 0 && <section className="panel">
        <div className="panel-heading"><div><span className="eyebrow">PROCESSING LOG</span><h2>Pipeline activity</h2></div></div>
        <div className="processing-log">{ingestionLog.map((entry, i) =>
          <div key={i} className="log-entry"><span className="log-ts">{entry.ts}</span><span className={`log-${entry.level}`}>[{entry.level.toUpperCase()}]</span><span>{entry.msg}</span></div>
        )}</div>
      </section>}

      {ingestionResult && <section className="panel">
        <div className="panel-heading"><div><span className="eyebrow">INGESTION RESULT</span><h2>Graph building summary</h2></div></div>
        <div className="metrics-grid">
          <MetricCard icon="database" eyebrow="ENTITIES CREATED" value={ingestionResult.entities_created} caption="Vertices added to graph" tone="violet"/>
          <MetricCard icon="graph" eyebrow="RELATIONSHIPS" value={ingestionResult.relationships_created} caption="Edges established" tone="blue"/>
          <MetricCard icon="activity" eyebrow="ERRORS" value={ingestionResult.error_count || 0} caption={ingestionResult.error_count ? 'Review errors below' : 'No errors'} tone={ingestionResult.error_count ? 'coral' : 'mint'}/>
          <MetricCard icon="layers" eyebrow="METADATA" value={ingestionResult.metadata_vertices || 1} caption="Ingestion run records" tone="gold"/>
        </div>
        {ingestionResult.errors?.length > 0 && <div style={{marginTop: 12}}>
          <h3>Errors ({ingestionResult.errors.length})</h3>
          <div className="table-wrap"><table><thead><tr><th>Entity</th><th>Type</th><th>Error</th></tr></thead>
            <tbody>{ingestionResult.errors.slice(0, 20).map((err, i) => <tr key={i}>
              <td><code>{err.canonical_id || err.relationship || '—'}</code></td>
              <td>{err.entity_type || err.relationship || '—'}</td>
              <td>{err.error}</td>
            </tr>)}</tbody>
          </table></div>
        </div>}
      </section>}

      <section className="panel">
        <div className="panel-heading"><div><span className="eyebrow">FORMAT CONVERSION</span>
          <h2>Convert graph to standard formats</h2>
          <p>Export the current knowledge graph in industry-standard formats.</p>
        </div>
        <button className="secondary-button" disabled={busy} onClick={() => run(async () => {
          const result = await api('/api/v1/graph/formats');
          setAvailableFormats(result.formats);
        })}><Icon name="refresh" size={16}/>Load formats</button></div>
        <div className="format-output-grid">
          {[
            {id: 'rdf', label: 'RDF (Turtle)', icon: 'R', color: '#7054e8', desc: 'W3C RDF in Turtle syntax'},
            {id: 'rdf_xml', label: 'RDF/XML', icon: 'X', color: '#2589e8', desc: 'W3C RDF in XML format'},
            {id: 'rdfs', label: 'RDFS Schema', icon: 'S', color: '#10a981', desc: 'RDFS class definitions'},
            {id: 'owl', label: 'OWL Ontology', icon: 'O', color: '#df9d23', desc: 'OWL ontology export'},
            {id: 'gremlin', label: 'Gremlin', icon: 'G', color: '#ec6b76', desc: 'TinkerPop traversal script'},
            {id: 'cypher', label: 'Cypher', icon: 'C', color: '#7054e8', desc: 'Neo4j MERGE statements'},
            {id: 'gql', label: 'GQL', icon: 'Q', color: '#2589e8', desc: 'ISO GQL INSERT statements'},
            {id: 'sparql', label: 'SPARQL', icon: 'S', color: '#10a981', desc: 'SPARQL INSERT DATA'},
          ].map(fmt => <div key={fmt.id} className={`format-output-card ${selectedFormat === fmt.id ? 'selected' : ''}`}
            onClick={() => setSelectedFormat(fmt.id)}>
            <span className="format-icon" style={{background: fmt.color, color: '#fff'}}>{fmt.icon}</span>
            <div><strong>{fmt.label}</strong><small>{fmt.desc}</small></div>
          </div>)}
        </div>
        <div className="pipeline-actions" style={{marginTop: 12}}>
          <button className="primary-button" disabled={busy} onClick={() => run(async () => {
            const result = await api('/api/v1/graph/convert', {format_id: selectedFormat, limit: 10000});
            setConvertResult({[selectedFormat]: result});
          })}><Icon name="database" size={16}/>Convert to {selectedFormat.toUpperCase()}</button>
          <button className="primary-button" disabled={busy} onClick={() => run(async () => {
            const allFormats = {};
            for (const fmtId of ['rdf', 'rdf_xml', 'rdfs', 'owl', 'gremlin', 'cypher', 'gql', 'sparql']) {
              setIngestionLog(prev => [...prev, {ts: new Date().toISOString().slice(11, 19), level: 'info', msg: `Converting to ${fmtId}...`}]);
              const result = await api('/api/v1/graph/convert', {format_id: fmtId, limit: 10000});
              allFormats[fmtId] = result;
            }
            setConvertResult(allFormats);
            setIngestionLog(prev => [...prev, {ts: new Date().toISOString().slice(11, 19), level: 'ok', msg: `All 8 formats generated successfully`}]);
          })}><Icon name="layers" size={16}/>Convert All Formats</button>
        </div>
      </section>

      {convertResult && <section className="panel">
        <div className="panel-heading"><div><span className="eyebrow">GENERATED OUTPUT</span>
          <h2>Format conversion results</h2></div></div>
        <div className="format-output-grid">
          {Object.entries(convertResult).map(([fmtId, data]) => <div key={fmtId} className="format-output-card"
            onClick={() => {
              if (data.content) {
                const blob = new Blob([data.content], {type: 'text/plain'});
                const url = URL.createObjectURL(blob);
                const a = document.createElement('a'); a.href = url;
                a.download = `eoip-graph${data.extension || `.${fmtId}`}`;
                a.click(); URL.revokeObjectURL(url);
              }
            }}>
            <span className="format-icon" style={{background: data.error ? '#ec6b76' : '#10a981', color: '#fff'}}>
              {data.error ? '!' : '✓'}
            </span>
            <div>
              <strong>{data.label || fmtId.toUpperCase()}</strong>
              <small>{data.error || `${(data.content_length || data.content?.length || 0).toLocaleString()} chars — click to download`}</small>
            </div>
          </div>)}
        </div>
        {convertResult[selectedFormat]?.content && <details style={{marginTop: 12}}>
          <summary style={{cursor: 'pointer', fontWeight: 600}}>Preview: {selectedFormat.toUpperCase()}</summary>
          <pre className="processing-log" style={{maxHeight: 300, overflow: 'auto', whiteSpace: 'pre-wrap'}}>{convertResult[selectedFormat].content.slice(0, 5000)}{convertResult[selectedFormat].content.length > 5000 ? '\n\n... (truncated)' : ''}</pre>
        </details>}
      </section>}
    </div>}
    {section === 'quality' && <div className="admin-grid">
      <section className="panel span-2"><div className="panel-heading"><div><span className="eyebrow">GRAPH VALIDATION</span><h2>Knowledge quality</h2><p>Metrics are computed from persisted entities, relationships, and findings.</p></div><button className="primary-button" onClick={() => run(async () => setValidation(await api('/api/v1/admin/validation', {})))} disabled={busy}><Icon name="shield"/>Run validation</button></div>{validation ? <><div className={`validation-banner ${validation.valid ? 'success' : 'danger'}`}><Icon name={validation.valid ? 'check' : 'warning'}/><div><strong>{validation.valid ? 'No findings in the checked graph.' : `${validation.findings.length} findings require review.`}</strong><small>Checked {validation.vertices_checked} entities and {validation.edges_checked} relationships · {formatTime(validation.finished_at)}</small></div></div><div className="quality-grid"><QualityRing label="Evidence coverage" value={validation.quality?.evidence_coverage} tone="violet"/><QualityRing label="Provenance coverage" value={validation.quality?.provenance_coverage} tone="mint"/><QualityRing label="Schema compliance" value={validation.quality?.schema_compliance} tone="blue"/><QualityRing label="Completeness" value={validation.quality?.completeness} tone="gold"/><QualityRing label="Freshness" value={validation.quality?.freshness} tone="coral"/><QualityRing label="Orphan rate" value={validation.quality?.orphan_rate} tone="coral"/><QualityRing label="Duplicate rate" value={validation.quality?.duplicate_rate} tone="coral"/><div className="finding-count"><strong>{validation.quality?.error_count || 0}</strong><span>Errors</span><small>{validation.quality?.warning_count || 0} warnings</small></div></div><FindingsTable findings={validation.findings || []}/></> : <EmptyState icon="shield" title="Validation has not run in this session">Run validation to compute current quality coverage and inspect first-class findings.</EmptyState>}</section>
      <section className="panel"><div className="panel-heading"><div><span className="eyebrow">SEMANTIC MODEL</span><h2>Ontology schema</h2></div></div><div className="ontology-summary"><span className="section-icon violet"><Icon name="layers"/></span><strong>Ontology {stats?.schema?.ontology_version || '—'}</strong><small>Schema {stats?.schema?.schema_version || '—'}</small></div><dl className="compact-list"><div><dt>Vertex labels</dt><dd>{Object.keys(stats?.labels || {}).length}</dd></div><div><dt>Storage backend</dt><dd>{stats?.backend || '—'}</dd></div><div><dt>Initialization</dt><dd><StatusPill status={stats?.schema ? 'READY' : 'UNKNOWN'}/></dd></div></dl><button className="secondary-button wide" onClick={() => run(async () => setOntologySchema(await api('/api/v1/graph/schema')))} disabled={busy}><Icon name="layers"/>Load ontology schema</button>{ontologySchema && <AdminOntology schema={ontologySchema}/>}<button className="secondary-button wide" onClick={() => run(async () => setOntology(await api('/api/v1/ontology/export?limit=1')))} disabled={busy}><Icon name="code"/>Inspect JSON-LD context</button>{ontology && <pre className="code-panel">{JSON.stringify(ontology['@context'] || {}, null, 2)}</pre>}</section>
      <section className="panel"><div className="panel-heading"><div><span className="eyebrow">FEDERATION</span><h2>Semantic sources</h2></div></div><button className="secondary-button wide" onClick={() => run(async () => {
        const sourceData = await api('/api/v1/federation/sources');
        const queryData = await api('/api/v1/federation/query', {entity_types: ['WorkItem'], projection: ['canonical_id', 'issue_key', 'summary']});
        setFederation({sources: sourceData.sources || [], query: queryData});
      })} disabled={busy}><Icon name="database"/>Load federation plan</button>{federation ? <><dl className="compact-list"><div><dt>Sources</dt><dd>{federation.sources.length}</dd></div><div><dt>Rows</dt><dd>{federation.query?.row_count || 0}</dd></div><div><dt>Degraded</dt><dd>{(federation.query?.plan?.degraded_sources || []).length}</dd></div></dl><div className="table-wrap"><table><thead><tr><th>Source</th><th>Adapter</th><th>Mode</th><th>Entity types</th></tr></thead><tbody>{federation.sources.map(source => <tr key={source.source_id}><td><code>{source.source_id}</code></td><td>{source.adapter_kind || 'generic'}</td><td>{source.mode}</td><td>{(source.entity_types || []).slice(0, 4).join(', ')}{(source.entity_types || []).length > 4 ? '…' : ''}</td></tr>)}</tbody></table></div><pre className="code-panel">{JSON.stringify(federation.query?.plan || {}, null, 2)}</pre></> : <EmptyState icon="database" title="Federation plan is not loaded">Load the current source registry and routing plan.</EmptyState>}</section>
    </div>}
    {section === 'security' && <AdminSecurityCenter api={api} run={run} busy={busy}/>}
    {section === 'liveops' && <LiveOpsPanel api={api} run={run} busy={busy}/>}
    {section === 'operations' && <div className="admin-grid">
      <section className="panel span-2"><div className="panel-heading"><div><span className="eyebrow">AUDIT TRAIL</span><h2>Security-relevant activity</h2><p>Safe summaries only; secrets and payload content are excluded.</p></div><button className="secondary-button" onClick={() => run(async () => setAudit(await api('/api/v1/admin/audit?limit=50')))} disabled={busy}><Icon name="refresh"/>Load audit events</button></div>{audit ? <AuditTable items={audit}/> : <EmptyState icon="terminal" title="Audit events are not loaded">Load the latest events to inspect operations, outcomes, actors, and correlation-safe summaries.</EmptyState>}</section>
      <section className="panel span-3"><div className="panel-heading"><div><span className="eyebrow">RECOVERY</span><h2>Dead-letter queue</h2><p>Inspect rejection context and payload identity without exposing captured payloads.</p></div><button className="secondary-button" onClick={() => run(async () => setDlq(await api('/api/v1/admin/dlq?limit=25')))} disabled={busy}>Load DLQ</button></div>{dlq ? <DeadLetterTable items={dlq} onReplay={replayDlq} busy={busy}/> : <EmptyState icon="warning" title="DLQ is not loaded">Load the queue to inspect rejected records and their recovery actions.</EmptyState>}</section>
    </div>}
  </>;
}

export default function App() {
  const [token, setToken] = useState('');
  const [authenticated, setAuthenticated] = useState(false);
  const [mode, setMode] = useState(() => destinationFor(location.pathname)?.id || 'not-found');
  const [theme, setTheme] = useState('light');
  const [reducedMotion, setReducedMotion] = useState(false);
  const [lens, setLens] = useState('graph');
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
  const operations = useRef(0);

  // useCallback is required: child components (Studio, admin panels) hold
  // `api`/`run` in effect dependency arrays. Recreating these closures on
  // every render would re-fire those effects on each state change and starve
  // the UI (observed as an infinite schema-reload loop clearing error toasts).
  const api = useMemo(() => createApiClient(token), [token]);
  useEffect(() => () => api.dispose(), [api]);
  useEffect(() => {
    // Remove the obsolete credential without reading it back into the application.
    try {sessionStorage.removeItem('eoip-token');} catch { /* storage may be unavailable */ }
  }, []);
  useEffect(() => {
    document.documentElement.dataset.theme = theme;
    document.documentElement.dataset.motion = reducedMotion ? 'reduce' : 'system';
  }, [theme, reducedMotion]);
  const run = useCallback(async action => {
    operations.current += 1;
    setBusy(true); setError(''); setErrorMeta('');
    try {await action();} catch (exception) {
      if (exception.name !== 'AbortError') {
        setError(exception.message || 'The operation could not be completed.');
        setErrorMeta(exception.correlationId ? `Correlation ID: ${exception.correlationId}` : 'Check that the local API and graph services are available.');
      }
    } finally {operations.current -= 1; setBusy(operations.current > 0);}
  }, []);
  const refresh = useCallback(async () => {
    const [nextStats, nextSystem, nextJobs] = await Promise.all([api('/api/v1/admin/stats'), api('/api/v1/admin/system'), api('/api/v1/admin/jobs')]);
    setStats(nextStats); setSystem(nextSystem); setJobs(nextJobs);
  }, [api]);
  async function login(event) {event.preventDefault(); await run(async () => {await refresh(); setAuthenticated(true);});}
  function disconnect() {
    api.dispose(); setToken(''); setAuthenticated(false); setStats(null); setSystem(null);
    setJobs([]); setGraph(emptyGraph); setSelected(null); setSelectedEdge(null); setDetail(null);
    setLens('graph'); setError(''); setErrorMeta(''); setTheme('light'); setReducedMotion(false);
  }
  function navigate(value) {
    const destination = destinations.find(item => item.id === value);
    if (!destination) return;
    setMode(value); history.pushState({}, '', destination.path);
  }

  useEffect(() => {
    const controller = new AbortController();
    fetch('/health/ready', {signal: controller.signal}).then(async response => {
      const data = response.headers.get('content-type')?.includes('json') ? await response.json() : null;
      setHealth(response.ok && data?.status === 'ready' ? 'ready' : 'unavailable');
    }).catch(error => {if (error.name !== 'AbortError') setHealth('unavailable');});
    return () => controller.abort();
  }, []);
  useEffect(() => {if (!authenticated) return; const timer = setInterval(() => {if (!document.hidden) refresh().catch(() => {});}, 15000); return () => clearInterval(timer);}, [authenticated, refresh]);
  useEffect(() => {const onPop = () => setMode(destinationFor(location.pathname)?.id || 'not-found'); addEventListener('popstate', onPop); return () => removeEventListener('popstate', onPop);}, []);

  const alert = error && <div className="toast error-toast" role="alert"><span className="toast-icon"><Icon name="warning"/></span><div><strong>{error}</strong><small>{errorMeta}</small></div><IconButton label="Dismiss error" icon="close" onClick={() => setError('')}/></div>;
  if (!authenticated) return <><Connection token={token} setToken={setToken} onSubmit={login} busy={busy} health={health}/>{alert}</>;
  return <>
    <WorkspaceShell mode={mode} onNavigate={navigate} onRefresh={() => run(refresh)} onDisconnect={disconnect} busy={busy}>
      <RouteBoundary key={mode}><Suspense fallback={<div className="route-loading" role="status">Loading workspace...</div>}>
        {mode === 'app' ? <Explorer stats={stats} graph={graph} setGraph={setGraph} selected={selected} setSelected={setSelected} detail={detail} setDetail={setDetail} selectedEdge={selectedEdge} setSelectedEdge={setSelectedEdge} lens={lens} setLens={setLens} api={api} run={run} busy={busy} token={token}/>
          : mode === 'cognitive' ? <CognitiveHub api={api} run={run} busy={busy} stats={stats}/>
          : mode === 'dashboards' ? <EngineDashboardsHub api={api}/>
          : mode === 'demo' ? <GuidedDemo api={api} run={run} busy={busy}/>
          : mode === 'studio' ? <Studio api={api} run={run} busy={busy}/>
          : mode === 'admin' ? <Admin stats={stats} system={system} jobs={jobs} api={api} run={run} refresh={refresh} busy={busy}/>
          : mode === 'settings' ? <Appearance theme={theme} setTheme={setTheme} reducedMotion={reducedMotion} setReducedMotion={setReducedMotion}/>
          : <section className="empty-state"><h2>Page not found</h2><button className="secondary-button" onClick={() => navigate('app')}>Open knowledge explorer</button></section>}
      </Suspense></RouteBoundary>
    </WorkspaceShell>
    {busy && <div className="busy-bar" aria-label="Operation in progress"><span/></div>}{alert}
  </>;
}
