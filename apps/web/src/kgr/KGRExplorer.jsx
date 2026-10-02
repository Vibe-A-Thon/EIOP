import React, {useCallback, useEffect, useState} from 'react';
import GraphCanvas, {palette} from '../GraphCanvas.jsx';
import {Icon, Tip} from '../icons.jsx';

const graphTypes = [
  {id: 'knowledge', label: 'Knowledge', icon: 'graph', hint: 'Entity-centric knowledge graph with relationships and evidence'},
  {id: 'relationship', label: 'Relationships', icon: 'link', hint: 'Edge-centric analysis: which entity types connect via which relationships'},
  {id: 'metadata', label: 'Metadata', icon: 'database', hint: 'Schema topology: vertex labels, edge labels, property schemas, and indexes'},
  {id: 'ontology', label: 'Ontology', icon: 'layers', hint: 'Class hierarchy, domain decomposition, and ontology structure'},
  {id: 'temporal', label: 'Temporal', icon: 'clock', hint: 'Time-windowed views with temporal filtering'},
  {id: 'provenance', label: 'Provenance', icon: 'shield', hint: 'Evidence chains, ingestion lineage, and trust propagation'},
];

function GraphTypeSelector({active, onSelect}) {
  return <div className="kgr-type-bar" role="tablist" aria-label="Graph type selector">
    {graphTypes.map(t => <Tip text={t.hint} key={t.id}>
      <button role="tab" aria-selected={active === t.id} className={active === t.id ? 'active' : ''} onClick={() => onSelect(t.id)}>
        <Icon name={t.icon} size={15}/>{t.label}
      </button>
    </Tip>)}
  </div>;
}

function FilterBar({filters, onChange, schema}) {
  const labels = Object.keys(schema?.vertex_labels || {});
  const edgeTypes = Object.keys(schema?.edge_labels || {});
  const domains = schema?.domains || [];
  return <div className="kgr-filter-bar">
    <div className="kgr-filter-group">
      <label className="select-control" title="Filter by domain"><Icon name="layers" size={14}/>
        <select value={filters.domain} onChange={e => onChange({...filters, domain: e.target.value})} aria-label="Domain filter">
          <option value="ALL">All domains</option>
          {domains.map(d => <option key={d}>{d}</option>)}
        </select>
      </label>
      <label className="select-control" title="Filter by entity type"><Icon name="database" size={14}/>
        <select value={filters.label} onChange={e => onChange({...filters, label: e.target.value})} aria-label="Entity type filter">
          <option value="ALL">All types</option>
          {labels.map(l => <option key={l}>{l}</option>)}
        </select>
      </label>
      <label className="select-control" title="Filter by relationship"><Icon name="link" size={14}/>
        <select value={filters.edgeType} onChange={e => onChange({...filters, edgeType: e.target.value})} aria-label="Relationship filter">
          <option value="ALL">All relationships</option>
          {edgeTypes.map(e => <option key={e}>{e}</option>)}
        </select>
      </label>
      <label className="select-control" title="Filter by trust"><Icon name="shield" size={14}/>
        <select value={filters.trust} onChange={e => onChange({...filters, trust: e.target.value})} aria-label="Trust filter">
          <option value="ALL">All trust</option>
          <option value="DETERMINISTIC">Deterministic</option>
          <option value="INFERRED">Inferred</option>
        </select>
      </label>
    </div>
    <div className="kgr-filter-chips">
      {filters.domain !== 'ALL' && <span className="filter-chip" onClick={() => onChange({...filters, domain: 'ALL'})}>{filters.domain} <Icon name="close" size={11}/></span>}
      {filters.label !== 'ALL' && <span className="filter-chip" onClick={() => onChange({...filters, label: 'ALL'})}>{filters.label} <Icon name="close" size={11}/></span>}
      {filters.edgeType !== 'ALL' && <span className="filter-chip" onClick={() => onChange({...filters, edgeType: 'ALL'})}>{filters.edgeType} <Icon name="close" size={11}/></span>}
      {filters.trust !== 'ALL' && <span className="filter-chip" onClick={() => onChange({...filters, trust: 'ALL'})}>{filters.trust} <Icon name="close" size={11}/></span>}
    </div>
  </div>;
}

function displayLabel(node) {
  return node?.properties?.issue_key || node?.properties?.display_name || node?.properties?.name || node?.properties?.qualified_name || node?.properties?.path || node?.label || 'Unknown';
}

function shortId(value, size = 22) {
  if (!value) return '—';
  return value.length > size ? `${value.slice(0, size - 1)}…` : value;
}

function NodeInspector({node, detail, metrics, blastRadius, onImpact, onBlastRadius, onLineage, onClose, busy}) {
  const [tab, setTab] = useState('overview');
  useEffect(() => setTab('overview'), [node?.id]);

  if (!node) return <section className="kgr-inspector panel">
    <div className="empty-state"><span className="empty-icon"><Icon name="focus" size={22}/></span>
      <strong>Select an entity</strong><p>Click a node on the graph to inspect its properties, relationships, impact, and evidence.</p>
    </div>
  </section>;

  const outgoing = detail?.outgoing || [];
  const incoming = detail?.incoming || [];
  const evidenceEdges = [...outgoing, ...incoming].filter(e => e.properties?.source_ref || e.properties?.evidence_key);
  const edgesByType = {};
  for (const e of [...outgoing, ...incoming]) {
    const t = e.label || e.type || 'UNKNOWN';
    edgesByType[t] = (edgesByType[t] || 0) + 1;
  }
  const m = metrics || {};
  const br = blastRadius;

  return <section className="kgr-inspector panel" aria-label="Entity inspector">
    <div className="inspector-heading">
      <span className="entity-symbol" style={{'--entity-color': palette[node.label] || '#64748b'}}>{displayLabel(node).slice(0, 1).toUpperCase()}</span>
      <div><span className="eyebrow">{node.label}</span><h2>{displayLabel(node)}</h2></div>
      <button className="icon-button" onClick={onClose} title="Close inspector" aria-label="Close inspector"><Icon name="close"/></button>
    </div>
    <code className="identity" title={node.id}>{node.id}</code>

    <div className="inspector-tabs" role="tablist">
      {['overview', 'relationships', 'impact', 'evidence', 'annotations'].map(t =>
        <button key={t} className={tab === t ? 'active' : ''} onClick={() => setTab(t)} role="tab">{t.charAt(0).toUpperCase() + t.slice(1)}
          {t === 'relationships' && <span>{outgoing.length + incoming.length}</span>}
          {t === 'evidence' && <span>{evidenceEdges.length}</span>}
        </button>
      )}
    </div>

    {tab === 'overview' && <>
      <div className="inspector-actions">
        <button disabled={busy} onClick={onImpact} title="Explore downstream impact"><Icon name="activity" size={16}/>Impact</button>
        <button disabled={busy} onClick={onBlastRadius} title="Compute blast radius"><Icon name="graph" size={16}/>Blast radius</button>
        <button disabled={busy} onClick={onLineage} title="Trace provenance"><Icon name="shield" size={16}/>Lineage</button>
      </div>
      <h3>Properties</h3>
      <dl className="property-list">
        {Object.entries(node.properties || {}).map(([k, v]) => <div key={k}><dt>{k.replaceAll('_', ' ')}</dt><dd>{String(v)}</dd></div>)}
      </dl>
    </>}

    {tab === 'relationships' && <>
      <div className="relationship-summary">
        <div><strong>{outgoing.length}</strong><small>outgoing</small></div>
        <div><strong>{incoming.length}</strong><small>incoming</small></div>
        <div><strong>{Object.keys(edgesByType).length}</strong><small>types</small></div>
      </div>
      <h3>By type</h3>
      <div className="relationship-bars">
        {Object.entries(edgesByType).sort((a, b) => b[1] - a[1]).map(([type, count]) =>
          <div key={type}><span>{type}</span><strong>{count}</strong></div>
        )}
      </div>
      <h3>Outgoing</h3>
      <div className="edge-list">{outgoing.length ? outgoing.map((e, i) =>
        <div key={e.eid || i} className="edge-item"><span className="badge">{e.label || e.type}</span><code>{shortId(e.target_id || '', 30)}</code></div>
      ) : <p className="subtle">No outgoing relationships</p>}</div>
      <h3>Incoming</h3>
      <div className="edge-list">{incoming.length ? incoming.map((e, i) =>
        <div key={e.eid || i} className="edge-item"><span className="badge">{e.label || e.type}</span><code>{shortId(e.source_id || '', 30)}</code></div>
      ) : <p className="subtle">No incoming relationships</p>}</div>
    </>}

    {tab === 'impact' && <>
      <div className="impact-summary">
        <div className="metric-card tone-coral"><span className="metric-icon"><Icon name="activity" size={20}/></span>
          <div><span className="eyebrow">BLAST RADIUS</span><strong>{br?.total_affected ?? '—'}</strong><small>{br?.risk || 'Not computed'}</small></div>
        </div>
        <div className="metric-card tone-violet"><span className="metric-icon"><Icon name="graph" size={20}/></span>
          <div><span className="eyebrow">DEGREE</span><strong>{m.degree ?? '—'}</strong><small>{m.in_degree ?? 0} in / {m.out_degree ?? 0} out</small></div>
        </div>
      </div>
      {br && <>
        <h3>Impact by depth</h3>
        <div className="depth-breakdown">
          {Object.entries(br.by_depth || {}).sort((a, b) => Number(a[0]) - Number(b[0])).map(([depth, count]) =>
            <div key={depth} className="depth-row">
              <span className="depth-label">{depth}-hop</span>
              <span className="depth-bar"><i style={{width: `${Math.min(100, (count / Math.max(br.total_affected, 1)) * 100)}%`}}/></span>
              <strong>{count}</strong>
            </div>
          )}
        </div>
        <h3>Affected entity types</h3>
        <div className="type-breakdown">
          {Object.entries(br.by_type || {}).sort((a, b) => b[1] - a[1]).map(([type, count]) =>
            <div key={type}><span className="type-dot" style={{background: palette[type] || '#94a3b8'}}/><span>{type}</span><strong>{count}</strong></div>
          )}
        </div>
      </>}
      {!br && <div className="inline-notice"><Icon name="info"/>Click "Blast radius" to compute downstream impact analysis.</div>}
      <button className="primary-button" disabled={busy} onClick={onBlastRadius}><Icon name="activity"/>Compute blast radius</button>
    </>}

    {tab === 'evidence' && <>
      <p className="subtle">Source references from relationships connected to this entity.</p>
      {evidenceEdges.length ? <div className="evidence-stack">{evidenceEdges.map((e, i) =>
        <div className="evidence-card" key={e.eid || i}><Icon name="shield"/><div>
          <strong>{e.label || e.type}</strong><small>{e.properties?.source_ref || e.properties?.evidence_key || 'No reference'}</small>
        </div></div>
      )}</div> : <div className="empty-state"><span className="empty-icon"><Icon name="shield" size={22}/></span>
        <strong>No evidence</strong><p>No source references found for this entity's relationships.</p>
      </div>}
    </>}

    {tab === 'annotations' && <div className="annotation-panel">
      <p className="subtle">Annotations are stored locally in your browser.</p>
      <textarea placeholder="Add a note about this entity..." rows="4" defaultValue={(() => {try {return localStorage.getItem(`kgr-note-${node.id}`) || '';} catch {return '';}})()}
        onChange={e => {try {if (e.target.value) localStorage.setItem(`kgr-note-${node.id}`, e.target.value); else localStorage.removeItem(`kgr-note-${node.id}`);} catch {}}}/>
    </div>}
  </section>;
}

function MetadataGraphView({schema}) {
  if (!schema) return <div className="empty-state"><span className="empty-icon"><Icon name="database" size={22}/></span><strong>Loading schema...</strong></div>;
  const labels = Object.entries(schema.vertex_labels || {});
  const edges = Object.entries(schema.edge_labels || {});
  return <div className="kgr-metadata-view">
    <section className="panel"><div className="panel-heading"><div><span className="eyebrow">VERTEX LABELS</span><h2>Entity types ({labels.length})</h2></div></div>
      <div className="schema-grid">{labels.map(([name, info]) =>
        <div key={name} className="schema-card" tabIndex="0">
          <div className="schema-card-header"><span className="type-dot" style={{background: palette[name] || '#94a3b8'}}/><strong>{name}</strong><span className="badge">{info.instance_count}</span></div>
          <small className="schema-domain">{info.domain}</small>
          <div className="schema-props"><strong>Required:</strong> {info.required_properties.join(', ')}</div>
          {info.optional_properties.length > 0 && <div className="schema-props"><strong>Optional:</strong> {info.optional_properties.join(', ')}</div>}
        </div>
      )}</div>
    </section>
    <section className="panel"><div className="panel-heading"><div><span className="eyebrow">EDGE LABELS</span><h2>Relationship types ({edges.length})</h2></div></div>
      <div className="schema-grid">{edges.map(([name, info]) =>
        <div key={name} className="schema-card" tabIndex="0">
          <div className="schema-card-header"><Icon name="link" size={14}/><strong>{name}</strong></div>
          <div className="schema-props"><strong>From:</strong> {info.source_labels.join(', ')}</div>
          <div className="schema-props"><strong>To:</strong> {info.target_labels.join(', ')}</div>
        </div>
      )}</div>
    </section>
  </div>;
}

function OntologyGraphView({schema}) {
  if (!schema) return <div className="empty-state"><span className="empty-icon"><Icon name="layers" size={22}/></span><strong>Loading ontology...</strong></div>;
  const domains = schema.domains || [];
  const labels = schema.vertex_labels || {};
  const domainGroups = {};
  for (const [name, info] of Object.entries(labels)) {
    const d = info.domain;
    if (!domainGroups[d]) domainGroups[d] = [];
    domainGroups[d].push({name, ...info});
  }
  return <div className="kgr-ontology-view">
    <section className="panel"><div className="panel-heading"><div><span className="eyebrow">ONTOLOGY</span>
      <h2>Enterprise ontology v{schema.ontology_version}</h2><p>Schema v{schema.schema_version} · {domains.length} domains · {Object.keys(labels).length} entity types</p>
    </div></div>
      <div className="ontology-domain-grid">{domains.map(d =>
        <div key={d} className="ontology-domain-card">
          <h3><Icon name="layers" size={16}/> {d}</h3>
          <div className="ontology-types">{(domainGroups[d] || []).map(t =>
            <div key={t.name} className="ontology-type-row">
              <span className="type-dot" style={{background: palette[t.name] || '#94a3b8'}}/><strong>{t.name}</strong>
              <span className="badge">{t.instance_count}</span>
              <small>{t.required_properties.length} required</small>
            </div>
          )}</div>
        </div>
      )}</div>
    </section>
    <section className="panel"><div className="panel-heading"><div><span className="eyebrow">INDEXES</span><h2>Index coverage</h2></div></div>
      <div className="index-list">{(schema.indexes || []).map(idx =>
        <div key={idx.name} className="index-row"><Icon name="check" size={14}/><strong>{idx.name}</strong>
          <span className="badge">{idx.type}</span><small>{idx.label || 'global'} · {idx.fields.join(', ')}</small>
        </div>
      )}</div>
    </section>
  </div>;
}

function ProvenanceGraphView({graph, onInspect, selected}) {
  const evidenceNodes = (graph.nodes || []).filter(n => ['Evidence', 'IngestionRun', 'ValidationRun'].includes(n.label));
  const otherNodes = (graph.nodes || []).filter(n => !['Evidence', 'IngestionRun', 'ValidationRun'].includes(n.label));
  return <div className="kgr-provenance-view">
    <section className="panel"><div className="panel-heading"><div><span className="eyebrow">PROVENANCE CHAIN</span>
      <h2>Evidence & ingestion lineage</h2><p>Entities are connected to their source evidence and ingestion runs.</p>
    </div><span className="count-badge">{evidenceNodes.length} provenance entities</span></div>
      {evidenceNodes.length ? <div className="provenance-list">{evidenceNodes.map(n =>
        <button key={n.id} onClick={() => onInspect(n)} className={selected?.id === n.id ? 'selected' : ''}>
          <span className="type-dot" style={{background: palette[n.label] || '#94a3b8'}}/><span>
            <strong>{n.properties?.source_ref || n.properties?.run_kind || displayLabel(n)}</strong>
            <small>{n.label} · {n.properties?.method || n.properties?.run_status || ''}</small>
          </span><Icon name="chevron" size={14}/>
        </button>
      )}</div> : <div className="empty-state"><span className="empty-icon"><Icon name="shield" size={22}/></span>
        <strong>No provenance entities</strong><p>Search and expand entities to load their evidence chain.</p>
      </div>}
    </section>
  </div>;
}

function BlastRadiusView({data, onClose}) {
  if (!data) return null;
  const maxDepth = Math.max(...Object.keys(data.by_depth || {}).map(Number), 0);
  const riskClass = data.risk === 'HIGH' ? 'negative' : data.risk === 'MEDIUM' ? 'neutral' : 'positive';
  return <div className="kgr-blast-overlay">
    <div className="blast-header">
      <div><span className="eyebrow">BLAST RADIUS</span><h2>{data.total_affected} affected entities</h2></div>
      <span className={`status-pill ${riskClass}`}><span className="status-dot"/>{data.risk} RISK</span>
      <button className="icon-button" onClick={onClose}><Icon name="close"/></button>
    </div>
    <div className="blast-rings">{[...Array(maxDepth)].map((_, i) => {
      const depth = i + 1;
      const count = data.by_depth?.[depth] || 0;
      const pct = count / Math.max(data.total_affected, 1);
      return <div key={depth} className="blast-ring" style={{'--ring-size': `${60 + depth * 60}px`, '--ring-opacity': 1 - depth * 0.15}}>
        <span className="ring-label">{depth}-hop: {count}</span>
      </div>;
    })}</div>
    <div className="blast-types">{Object.entries(data.by_type || {}).sort((a, b) => b[1] - a[1]).map(([type, count]) =>
      <div key={type}><span className="type-dot" style={{background: palette[type] || '#94a3b8'}}/><span>{type}</span><strong>{count}</strong></div>
    )}</div>
  </div>;
}

const defaultFilters = {domain: 'ALL', label: 'ALL', edgeType: 'ALL', trust: 'ALL'};

export default function KGRExplorer({graph, setGraph, api, run, busy, stats}) {
  const [graphType, setGraphType] = useState('knowledge');
  const [filters, setFilters] = useState(defaultFilters);
  const [selected, setSelected] = useState(null);
  const [selectedEdge, setSelectedEdge] = useState(null);
  const [detail, setDetail] = useState(null);
  const [schema, setSchema] = useState(null);
  const [metrics, setMetrics] = useState(null);
  const [blastRadius, setBlastRadius] = useState(null);
  const [showBlast, setShowBlast] = useState(false);

  useEffect(() => {run(async () => setSchema(await api('/api/v1/graph/schema')));}, []);

  const inspect = useCallback(async (node) => {
    setSelected(node);
    setSelectedEdge(null);
    setBlastRadius(null);
    setMetrics(null);
    const [d, m] = await Promise.all([
      api(`/api/v1/entities/${encodeURIComponent(node.id)}`),
      api('/api/v1/graph/metrics', {canonical_ids: [node.id]}).catch(() => ({})),
    ]);
    setDetail(d);
    setMetrics(m[node.id] || null);
  }, [api]);

  const computeBlastRadius = useCallback(() => {
    if (!selected) return;
    run(async () => {
      const result = await api('/api/v1/graph/blast-radius', {canonical_id: selected.id, max_depth: 4});
      setBlastRadius(result);
      setShowBlast(true);
    });
  }, [selected, api, run]);

  const computeImpact = useCallback(() => {
    if (!selected) return;
    run(async () => {
      const result = await api('/api/v1/impact', {canonical_id: selected.id, max_depth: 4});
      setGraph(result);
    });
  }, [selected, api, run, setGraph]);

  const computeLineage = useCallback(() => {
    if (!selected) return;
    run(async () => {
      const result = await api('/api/v1/lineage', {canonical_id: selected.id, max_depth: 4});
      setGraph(result);
    });
  }, [selected, api, run, setGraph]);

  const expand = useCallback((node) => {
    run(async () => {
      const result = await api('/api/v1/neighborhood', {canonical_id: node.id, max_depth: 1, result_limit: 75});
      setGraph(result);
      await inspect(node);
    });
  }, [api, run, setGraph, inspect]);

  const visibleNodes = (graph.nodes || []).filter(n =>
    (filters.domain === 'ALL' || n.domain === filters.domain) &&
    (filters.label === 'ALL' || n.label === filters.label)
  );
  const nodeIds = new Set(visibleNodes.map(n => n.id));
  const visibleEdges = (graph.edges || []).filter(e =>
    nodeIds.has(e.from_id) && nodeIds.has(e.to_id) &&
    (filters.edgeType === 'ALL' || e.type === filters.edgeType) &&
    (filters.trust === 'ALL' || String(e.creation_status || e.properties?.creation_status || 'DETERMINISTIC').toUpperCase() === filters.trust)
  );

  return <div className="kgr-explorer">
    <GraphTypeSelector active={graphType} onSelect={setGraphType}/>
    <FilterBar filters={filters} onChange={setFilters} schema={schema}/>

    <div className="kgr-content">
      {graphType === 'knowledge' && <div className="explorer-grid">
        <section className="panel graph-panel">
          <div className="panel-heading"><div><span className="eyebrow">KGR · KNOWLEDGE GRAPH</span><h2>Interactive entity-relationship map</h2></div>
            <span className="count-badge">{visibleNodes.length} entities · {visibleEdges.length} relationships</span>
          </div>
          <GraphCanvas nodes={visibleNodes} edges={visibleEdges} paths={graph.paths || []}
            selectedId={selected?.id} selectedEdgeId={selectedEdge?.id}
            onSelectNode={n => run(() => inspect(n))} onSelectEdge={e => {setSelectedEdge(e); setSelected(null);}}
            onExpand={expand}/>
        </section>
        <NodeInspector node={selected} detail={detail} metrics={metrics} blastRadius={blastRadius}
          onImpact={computeImpact} onBlastRadius={computeBlastRadius} onLineage={computeLineage}
          onClose={() => {setSelected(null); setDetail(null);}} busy={busy}/>
      </div>}

      {graphType === 'relationship' && <div className="kgr-relationship-view">
        <section className="panel"><div className="panel-heading"><div><span className="eyebrow">KGR · RELATIONSHIP ANALYSIS</span>
          <h2>Edge-centric view</h2><p>Relationship types as nodes, connected when they share entity endpoints.</p></div></div>
          <div className="relationship-bars">{Object.entries((graph.edges || []).reduce((acc, e) => {
            acc[e.type] = (acc[e.type] || 0) + 1; return acc;
          }, {})).sort((a, b) => b[1] - a[1]).map(([type, count]) =>
            <Tip text={`${count} ${type} relationships in view`} key={type}><div tabIndex="0">
              <span>{type}</span><i><b style={{width: `${Math.max(8, count / Math.max(...Object.values((graph.edges || []).reduce((a, e) => {a[e.type] = (a[e.type] || 0) + 1; return a;}, {}))) * 100)}%`}}/></i><strong>{count}</strong>
            </div></Tip>
          )}</div>
        </section>
      </div>}

      {graphType === 'metadata' && <MetadataGraphView schema={schema}/>}
      {graphType === 'ontology' && <OntologyGraphView schema={schema}/>}

      {graphType === 'temporal' && <div className="explorer-grid">
        <section className="panel graph-panel">
          <div className="panel-heading"><div><span className="eyebrow">KGR · TEMPORAL VIEW</span><h2>Time-filtered graph</h2></div></div>
          <GraphCanvas nodes={visibleNodes} edges={visibleEdges} paths={graph.paths || []}
            selectedId={selected?.id} onSelectNode={n => run(() => inspect(n))} onExpand={expand}/>
        </section>
        <NodeInspector node={selected} detail={detail} metrics={metrics} blastRadius={blastRadius}
          onImpact={computeImpact} onBlastRadius={computeBlastRadius} onLineage={computeLineage}
          onClose={() => {setSelected(null); setDetail(null);}} busy={busy}/>
      </div>}

      {graphType === 'provenance' && <ProvenanceGraphView graph={graph} onInspect={n => run(() => inspect(n))} selected={selected}/>}
    </div>

    {showBlast && blastRadius && <BlastRadiusView data={blastRadius} onClose={() => setShowBlast(false)}/>}
  </div>;
}
