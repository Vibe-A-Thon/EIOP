import React, {useCallback, useEffect, useMemo, useRef, useState} from 'react';
import GraphCanvas, {palette} from '../GraphCanvas.jsx';
import {Icon, Tip} from '../icons.jsx';
import CentralityRadar from './components/CentralityRadar.jsx';
import ContextMenu from './components/ContextMenu.jsx';
import ExplorationHistoryBar, {createHistory, pushState, undo, redo} from './components/ExplorationHistory.jsx';
import GraphBookmarks from './components/GraphBookmarks.jsx';

const graphTypes = [
  {id: 'knowledge', label: 'Knowledge', icon: 'graph', hint: 'Entity-centric knowledge graph with relationships and evidence'},
  {id: 'relationship', label: 'Relationships', icon: 'link', hint: 'Edge-centric analysis: which entity types connect via which relationships'},
  {id: 'metadata', label: 'Metadata', icon: 'database', hint: 'Schema topology: vertex labels, edge labels, property schemas, and indexes'},
  {id: 'ontology', label: 'Ontology', icon: 'layers', hint: 'Class hierarchy, domain decomposition, and ontology structure'},
  {id: 'temporal', label: 'Temporal', icon: 'clock', hint: 'Time-windowed views with temporal filtering'},
  {id: 'provenance', label: 'Provenance', icon: 'shield', hint: 'Evidence chains, ingestion lineage, and trust propagation'},
  {id: 'impact', label: 'Impact', icon: 'activity', hint: 'Blast radius, centrality analysis, and what-if simulation'},
  {id: 'similarity', label: 'Similarity', icon: 'users', hint: 'Node similarity scores, common neighbors, and structural equivalence'},
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
      <label className="select-control" title="Filter by source connector"><Icon name="database" size={14}/>
        <select value={filters.source} onChange={e => onChange({...filters, source: e.target.value})} aria-label="Source filter">
          <option value="ALL">All sources</option>
          <option value="jira">Jira</option>
          <option value="github">GitHub</option>
          <option value="gitlab">GitLab</option>
          <option value="confluence">Confluence</option>
          <option value="servicenow">ServiceNow</option>
          <option value="rally">Rally</option>
          <option value="qtest">qTest</option>
          <option value="figma">Figma</option>
          <option value="grafana">Grafana</option>
          <option value="datadog">Datadog</option>
          <option value="kibana">Kibana</option>
          <option value="api_portal">API Portal</option>
        </select>
      </label>
    </div>
    <div className="kgr-filter-chips">
      {filters.domain !== 'ALL' && <span className="filter-chip" onClick={() => onChange({...filters, domain: 'ALL'})}>{filters.domain} <Icon name="close" size={11}/></span>}
      {filters.label !== 'ALL' && <span className="filter-chip" onClick={() => onChange({...filters, label: 'ALL'})}>{filters.label} <Icon name="close" size={11}/></span>}
      {filters.edgeType !== 'ALL' && <span className="filter-chip" onClick={() => onChange({...filters, edgeType: 'ALL'})}>{filters.edgeType} <Icon name="close" size={11}/></span>}
      {filters.trust !== 'ALL' && <span className="filter-chip" onClick={() => onChange({...filters, trust: 'ALL'})}>{filters.trust} <Icon name="close" size={11}/></span>}
      {filters.source !== 'ALL' && <span className="filter-chip" onClick={() => onChange({...filters, source: 'ALL'})}>{filters.source} <Icon name="close" size={11}/></span>}
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

const inspectorTabs = ['overview', 'relationships', 'impact', 'centrality', 'similarity', 'whatif', 'evidence', 'annotations'];

function NodeInspector({node, detail, metrics, blastRadius, reverseImpact, fullCentrality, similarNodes, whatIfResult,
  allCentrality, graphNodeCount, highlightedPath,
  onImpact, onBlastRadius, onLineage, onFullCentrality, onSimilarity, onWhatIf, onExploreBlast, onClose, busy}) {
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
  const fc = fullCentrality;
  const sim = similarNodes || [];
  const wif = whatIfResult;

  const tabLabels = {
    overview: 'Overview', relationships: 'Relationships', impact: 'Impact',
    centrality: 'Centrality', similarity: 'Similar', whatif: 'What-If',
    evidence: 'Evidence', annotations: 'Notes',
  };

  return <section className="kgr-inspector panel" aria-label="Entity inspector">
    <div className="inspector-heading">
      <span className="entity-symbol" style={{'--entity-color': palette[node.label] || '#64748b'}}>{displayLabel(node).slice(0, 1).toUpperCase()}</span>
      <div><span className="eyebrow">{node.label}</span><h2>{displayLabel(node)}</h2></div>
      <button className="icon-button" onClick={onClose} title="Close inspector" aria-label="Close inspector"><Icon name="close"/></button>
    </div>
    <code className="identity" title={node.id}>{node.id}</code>

    <div className="inspector-tabs" role="tablist">
      {inspectorTabs.map(t =>
        <button key={t} className={tab === t ? 'active' : ''} onClick={() => setTab(t)} role="tab">{tabLabels[t]}
          {t === 'relationships' && <span>{outgoing.length + incoming.length}</span>}
          {t === 'evidence' && <span>{evidenceEdges.length}</span>}
          {t === 'similarity' && sim.length > 0 && <span>{sim.length}</span>}
        </button>
      )}
    </div>

    {tab === 'overview' && <>
      <div className="inspector-actions">
        <button disabled={busy} onClick={onImpact} title="Explore downstream impact"><Icon name="activity" size={16}/>Impact</button>
        <button disabled={busy} onClick={onBlastRadius} title="Compute blast radius"><Icon name="graph" size={16}/>Blast radius</button>
        <button disabled={busy} onClick={onLineage} title="Trace provenance"><Icon name="shield" size={16}/>Lineage</button>
        <button disabled={busy} onClick={onFullCentrality} title="Compute full centrality"><Icon name="activity" size={16}/>Centrality</button>
        <button disabled={busy} onClick={onSimilarity} title="Find similar nodes"><Icon name="users" size={16}/>Similar</button>
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
        {reverseImpact && <div className="metric-card tone-blue"><span className="metric-icon"><Icon name="link" size={20}/></span>
          <div><span className="eyebrow">UPSTREAM</span><strong>{reverseImpact.total_affected}</strong><small>{reverseImpact.total_affected} entities depend on this</small></div>
        </div>}
        {br && graphNodeCount > 0 && <div className="metric-card tone-gold"><span className="metric-icon"><Icon name="layers" size={20}/></span>
          <div><span className="eyebrow">PROPAGATION</span><strong>{((br.total_affected / Math.max(graphNodeCount, 1)) * 100).toFixed(1)}%</strong><small>of graph affected</small></div>
        </div>}
      </div>
      {br && <>
        <h3>{br.total_affected} entities affected across {Object.keys(br.by_depth).length} depth levels</h3>
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
      {fc && <><h3>Centrality radar</h3><CentralityRadar metrics={fc} allMetrics={allCentrality} width={240}/></>}
      {!br && <div className="inline-notice"><Icon name="info"/>Click "Blast radius" to compute downstream impact analysis.</div>}
      <div className="impact-btn-row">
        <button className="primary-button" disabled={busy} onClick={onBlastRadius}><Icon name="activity"/>Compute blast radius</button>
        {br && <button className="primary-button" disabled={busy} onClick={onExploreBlast}><Icon name="graph"/>Explore blast radius</button>}
      </div>
    </>}

    {tab === 'centrality' && <>
      <div className="centrality-grid">
        <div className="metric-card tone-violet"><span className="metric-icon"><Icon name="graph" size={20}/></span>
          <div><span className="eyebrow">DEGREE</span><strong>{fc?.degree ?? m.degree ?? '—'}</strong><small>{fc?.in_degree ?? m.in_degree ?? 0} in / {fc?.out_degree ?? m.out_degree ?? 0} out</small></div>
        </div>
        <div className="metric-card tone-blue"><span className="metric-icon"><Icon name="activity" size={20}/></span>
          <div><span className="eyebrow">BETWEENNESS</span><strong>{fc?.betweenness != null ? fc.betweenness.toFixed(4) : '—'}</strong><small>Bridge importance</small></div>
        </div>
        <div className="metric-card tone-mint"><span className="metric-icon"><Icon name="link" size={20}/></span>
          <div><span className="eyebrow">CLOSENESS</span><strong>{fc?.closeness != null ? fc.closeness.toFixed(4) : '—'}</strong><small>Reachability</small></div>
        </div>
        <div className="metric-card tone-gold"><span className="metric-icon"><Icon name="layers" size={20}/></span>
          <div><span className="eyebrow">PAGERANK</span><strong>{fc?.page_rank != null ? fc.page_rank.toFixed(4) : '—'}</strong><small>Influence score</small></div>
        </div>
        <div className="metric-card tone-blue"><span className="metric-icon"><Icon name="activity" size={20}/></span>
          <div><span className="eyebrow">EIGENVECTOR</span><strong>{fc?.eigenvector != null ? fc.eigenvector.toFixed(4) : '—'}</strong><small>Neighbor importance</small></div>
        </div>
        <div className="metric-card tone-mint"><span className="metric-icon"><Icon name="link" size={20}/></span>
          <div><span className="eyebrow">KATZ</span><strong>{fc?.katz != null ? fc.katz.toFixed(4) : '—'}</strong><small>Attenuated influence</small></div>
        </div>
        <div className="metric-card tone-coral"><span className="metric-icon"><Icon name="graph" size={20}/></span>
          <div><span className="eyebrow">HITS HUB</span><strong>{fc?.hits_hub != null ? fc.hits_hub.toFixed(4) : '—'}</strong><small>Hub score</small></div>
        </div>
        <div className="metric-card tone-gold"><span className="metric-icon"><Icon name="layers" size={20}/></span>
          <div><span className="eyebrow">HITS AUTH</span><strong>{fc?.hits_authority != null ? fc.hits_authority.toFixed(4) : '—'}</strong><small>Authority score</small></div>
        </div>
        <div className="metric-card tone-violet"><span className="metric-icon"><Icon name="link" size={20}/></span>
          <div><span className="eyebrow">HARMONIC</span><strong>{fc?.harmonic != null ? fc.harmonic.toFixed(4) : '—'}</strong><small>Harmonic closeness</small></div>
        </div>
      </div>
      {fc && <><h3>Centrality radar</h3><CentralityRadar metrics={fc} allMetrics={allCentrality} width={240}/></>}
      {!fc && <div className="inline-notice"><Icon name="info"/>Click "Compute centrality" to run all 8 centrality algorithms.</div>}
      <button className="primary-button" disabled={busy} onClick={onFullCentrality}><Icon name="activity"/>Compute centrality</button>
    </>}

    {tab === 'similarity' && <>
      <p className="subtle">Structurally similar nodes based on shared neighbors (Jaccard index).</p>
      {sim.length > 0 ? <div className="similarity-list">{sim.map((s, i) =>
        <div key={s.canonical_id || i} className="similarity-row">
          <span className="similarity-rank">{i + 1}</span>
          <div className="similarity-info">
            <strong>{shortId(s.canonical_id, 36)}</strong>
            <small>{s.common_neighbors ?? 0} common neighbors</small>
          </div>
          <span className="similarity-score">{(s.score ?? 0).toFixed(3)}</span>
        </div>
      )}</div> : <div className="inline-notice"><Icon name="info"/>Click "Find similar" to compute similarity scores.</div>}
      <button className="primary-button" disabled={busy} onClick={onSimilarity}><Icon name="users"/>Find similar nodes</button>
    </>}

    {tab === 'whatif' && <>
      <p className="subtle">Simulate removing this entity to see the impact on graph connectivity.</p>
      {wif ? <div className="whatif-results">
        <div className="whatif-summary">
          <div className="metric-card tone-coral"><span className="metric-icon"><Icon name="link" size={20}/></span>
            <div><span className="eyebrow">BROKEN EDGES</span><strong>{wif.broken_edges}</strong></div>
          </div>
          <div className="metric-card tone-gold"><span className="metric-icon"><Icon name="users" size={20}/></span>
            <div><span className="eyebrow">AFFECTED NEIGHBORS</span><strong>{wif.affected_neighbors}</strong></div>
          </div>
          <div className="metric-card tone-violet"><span className="metric-icon"><Icon name="graph" size={20}/></span>
            <div><span className="eyebrow">ORPHANED</span><strong>{wif.orphaned_entities}</strong><small>Would lose all connections</small></div>
          </div>
        </div>
      </div> : <div className="inline-notice"><Icon name="info"/>Click "Simulate removal" to see what happens if this entity is removed.</div>}
      <button className="primary-button" disabled={busy} onClick={onWhatIf}><Icon name="activity"/>Simulate removal</button>
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

function ImpactGraphView({api, run, busy, graph, setGraph}) {
  const [centralityResults, setCentralityResults] = useState(null);
  const [anomalyResults, setAnomalyResults] = useState(null);
  const [clusterResults, setClusterResults] = useState(null);

  const runCentrality = useCallback(() => {
    const ids = (graph.nodes || []).slice(0, 50).map(n => n.id);
    if (!ids.length) return;
    run(async () => {
      const result = await api('/api/v1/graph/centrality/full', {
        canonical_ids: ids, algorithms: ['degree', 'betweenness', 'closeness', 'pagerank']
      });
      setCentralityResults(result);
    });
  }, [api, run, graph]);

  const runAnomalies = useCallback(() => {
    run(async () => {
      const result = await api('/api/v1/graph/anomalies', {algorithms: ['degree_zscore'], threshold: 2.0});
      setAnomalyResults(result);
    });
  }, [api, run]);

  const runClusters = useCallback(() => {
    run(async () => {
      const result = await api('/api/v1/graph/cluster', {algorithm: 'label_propagation', resolution: 1.0});
      setClusterResults(result);
    });
  }, [api, run]);

  const topCentral = useMemo(() => {
    if (!centralityResults) return [];
    return Object.entries(centralityResults)
      .map(([id, m]) => ({id, ...m}))
      .sort((a, b) => (b.page_rank || 0) - (a.page_rank || 0))
      .slice(0, 15);
  }, [centralityResults]);

  return <div className="kgr-impact-view">
    <div className="impact-actions-bar">
      <button className="primary-button" disabled={busy} onClick={runCentrality}><Icon name="activity" size={16}/>Compute centrality</button>
      <button className="primary-button" disabled={busy} onClick={runAnomalies}><Icon name="graph" size={16}/>Detect anomalies</button>
      <button className="primary-button" disabled={busy} onClick={runClusters}><Icon name="layers" size={16}/>Find communities</button>
    </div>

    {topCentral.length > 0 && <section className="panel">
      <div className="panel-heading"><div><span className="eyebrow">CENTRALITY LEADERS</span>
        <h2>Top {topCentral.length} by PageRank</h2></div></div>
      <div className="centrality-table">
        <div className="centrality-header"><span>Entity</span><span>Degree</span><span>Betweenness</span><span>Closeness</span><span>PageRank</span></div>
        {topCentral.map(c => <div key={c.id} className="centrality-row">
          <span className="centrality-id" title={c.id}>{shortId(c.canonical_id || c.id, 28)}</span>
          <span>{c.degree}</span>
          <span>{(c.betweenness || 0).toFixed(4)}</span>
          <span>{(c.closeness || 0).toFixed(4)}</span>
          <span className="centrality-pr">{(c.page_rank || 0).toFixed(4)}</span>
        </div>)}
      </div>
    </section>}

    {anomalyResults && <section className="panel">
      <div className="panel-heading"><div><span className="eyebrow">ANOMALIES</span>
        <h2>{anomalyResults.length} outlier{anomalyResults.length !== 1 ? 's' : ''} detected</h2></div></div>
      {anomalyResults.length ? <div className="anomaly-list">{anomalyResults.map((a, i) =>
        <div key={a.canonical_id || i} className="anomaly-row">
          <span className={`anomaly-type ${a.anomaly_type}`}>{a.anomaly_type}</span>
          <strong>{shortId(a.canonical_id, 28)}</strong>
          <span className="anomaly-score">z={a.score?.toFixed(2)}</span>
          <small>{a.details?.degree != null ? `degree: ${a.details.degree}` : ''}</small>
        </div>
      )}</div> : <p className="subtle">No anomalies found at this threshold.</p>}
    </section>}

    {clusterResults && <section className="panel">
      <div className="panel-heading"><div><span className="eyebrow">COMMUNITIES</span>
        <h2>{clusterResults.community_count} communities (modularity {(clusterResults.modularity || 0).toFixed(3)})</h2></div></div>
      <div className="cluster-grid">{(clusterResults.communities || []).slice(0, 20).map((c, i) =>
        <div key={i} className="cluster-card">
          <div className="cluster-header"><strong>Community {c.community_id ?? i}</strong><span className="badge">{c.size ?? c.members?.length ?? 0}</span></div>
          <div className="cluster-members">{(c.members || []).slice(0, 5).map(m =>
            <span key={m} className="cluster-member" title={m}>{shortId(m, 20)}</span>
          )}{(c.members || []).length > 5 && <span className="cluster-more">+{(c.members || []).length - 5} more</span>}</div>
        </div>
      )}</div>
    </section>}

    {!centralityResults && !anomalyResults && !clusterResults && <div className="empty-state">
      <span className="empty-icon"><Icon name="activity" size={22}/></span>
      <strong>Impact analysis</strong><p>Run centrality, anomaly detection, or community analysis using the buttons above.</p>
    </div>}
  </div>;
}

function SimilarityGraphView({api, run, busy, graph, onHighlightPath}) {
  const [queryId, setQueryId] = useState('');
  const [algorithm, setAlgorithm] = useState('jaccard');
  const [results, setResults] = useState(null);
  const [pathResults, setPathResults] = useState(null);
  const [pathSource, setPathSource] = useState('');
  const [pathTarget, setPathTarget] = useState('');

  const nodeIds = useMemo(() => (graph.nodes || []).map(n => n.id), [graph]);

  const runSimilarity = useCallback(() => {
    if (!queryId.trim()) return;
    run(async () => {
      const result = await api('/api/v1/graph/similarity', {
        canonical_id: queryId.trim(), algorithm, limit: 20,
      });
      setResults(result);
    });
  }, [api, run, queryId, algorithm]);

  const runPaths = useCallback(() => {
    if (!pathSource.trim() || !pathTarget.trim()) return;
    run(async () => {
      const result = await api('/api/v1/graph/shortest-paths', {
        source_id: pathSource.trim(), target_id: pathTarget.trim(), max_paths: 5,
      });
      setPathResults(result);
    });
  }, [api, run, pathSource, pathTarget]);

  return <div className="kgr-similarity-view">
    <section className="panel">
      <div className="panel-heading"><div><span className="eyebrow">SIMILARITY SEARCH</span>
        <h2>Find structurally similar nodes</h2></div></div>
      <div className="similarity-form">
        <div className="similarity-input-row">
          <input type="text" placeholder="Enter entity canonical ID..." value={queryId}
            onChange={e => setQueryId(e.target.value)} list="sim-node-list" aria-label="Entity ID"/>
          <datalist id="sim-node-list">{nodeIds.slice(0, 100).map(id => <option key={id} value={id}/>)}</datalist>
          <label className="select-control"><select value={algorithm} onChange={e => setAlgorithm(e.target.value)} aria-label="Algorithm">
            <option value="jaccard">Jaccard</option>
            <option value="adamic_adar">Adamic-Adar</option>
            <option value="common_neighbors">Common neighbors</option>
          </select></label>
          <button className="primary-button" disabled={busy || !queryId.trim()} onClick={runSimilarity}><Icon name="users" size={16}/>Search</button>
        </div>
      </div>
      {results && results.length > 0 ? <div className="similarity-results">
        {results.map((s, i) => <div key={s.canonical_id || i} className="similarity-result-row">
          <span className="similarity-rank">{i + 1}</span>
          <div className="similarity-info">
            <strong>{shortId(s.canonical_id, 36)}</strong>
            <small>{s.common_neighbors ?? 0} common neighbors</small>
          </div>
          <span className="similarity-score">{(s.score ?? 0).toFixed(4)}</span>
        </div>)}
      </div> : results ? <p className="subtle">No similar nodes found.</p> : null}
    </section>

    <section className="panel">
      <div className="panel-heading"><div><span className="eyebrow">SHORTEST PATHS</span>
        <h2>Find all shortest paths between two entities</h2></div></div>
      <div className="similarity-form">
        <div className="similarity-input-row">
          <input type="text" placeholder="Source entity ID..." value={pathSource}
            onChange={e => setPathSource(e.target.value)} list="path-src-list" aria-label="Source ID"/>
          <datalist id="path-src-list">{nodeIds.slice(0, 100).map(id => <option key={id} value={id}/>)}</datalist>
          <span className="path-arrow-inline"><Icon name="chevron" size={14}/></span>
          <input type="text" placeholder="Target entity ID..." value={pathTarget}
            onChange={e => setPathTarget(e.target.value)} list="path-tgt-list" aria-label="Target ID"/>
          <datalist id="path-tgt-list">{nodeIds.slice(0, 100).map(id => <option key={id} value={id}/>)}</datalist>
          <button className="primary-button" disabled={busy || !pathSource.trim() || !pathTarget.trim()} onClick={runPaths}>
            <Icon name="link" size={16}/>Find paths</button>
        </div>
      </div>
      {pathResults && <>
        <p className="subtle">{pathResults.count} path{pathResults.count !== 1 ? 's' : ''} found</p>
        <div className="paths-list">{(pathResults.paths || []).map((path, i) =>
          <div key={i} className="path-row path-clickable" onClick={() => onHighlightPath && onHighlightPath(path)}>
            <span className="path-index">#{i + 1}</span>
            <div className="path-nodes">{path.map((nid, j) => <React.Fragment key={j}>
              {j > 0 && <span className="path-sep">&rarr;</span>}
              <span className="path-node" title={nid}>{shortId(nid, 18)}</span>
            </React.Fragment>)}</div>
            <span className="path-length">{path.length - 1} hop{path.length - 1 !== 1 ? 's' : ''}</span>
          </div>
        )}</div>
      </>}
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
      return <div key={depth} className="blast-ring" style={{'--ring-size': `${60 + depth * 60}px`, '--ring-opacity': 1 - depth * 0.15}}>
        <span className="ring-label">{depth}-hop: {count}</span>
      </div>;
    })}</div>
    <div className="blast-types">{Object.entries(data.by_type || {}).sort((a, b) => b[1] - a[1]).map(([type, count]) =>
      <div key={type}><span className="type-dot" style={{background: palette[type] || '#94a3b8'}}/><span>{type}</span><strong>{count}</strong></div>
    )}</div>
  </div>;
}

const defaultFilters = {domain: 'ALL', label: 'ALL', edgeType: 'ALL', trust: 'ALL', source: 'ALL'};

export default function KGRExplorer({graph, setGraph, api, run, busy, stats}) {
  const [graphType, setGraphType] = useState('knowledge');
  const [filters, setFilters] = useState(defaultFilters);
  const [selected, setSelected] = useState(null);
  const [selectedEdge, setSelectedEdge] = useState(null);
  const [detail, setDetail] = useState(null);
  const [schema, setSchema] = useState(null);
  const [metrics, setMetrics] = useState(null);
  const [blastRadius, setBlastRadius] = useState(null);
  const [reverseImpact, setReverseImpact] = useState(null);
  const [showBlast, setShowBlast] = useState(false);
  const [fullCentrality, setFullCentrality] = useState(null);
  const [allCentrality, setAllCentrality] = useState([]);
  const [similarNodes, setSimilarNodes] = useState(null);
  const [whatIfResult, setWhatIfResult] = useState(null);
  const [highlightedPath, setHighlightedPath] = useState(null);
  const [contextMenu, setContextMenu] = useState(null);
  const [history, setHistory] = useState(() => createHistory());
  const [showFilters, setShowFilters] = useState(true);
  const explorerRef = useRef(null);

  useEffect(() => {run(async () => setSchema(await api('/api/v1/graph/schema')));}, []);

  const pushHistory = useCallback((state) => {
    setHistory(h => pushState(h, state));
  }, []);

  const handleUndo = useCallback(() => {
    setHistory(h => {
      const prev = undo(h);
      if (prev.current) {
        setGraph(prev.current.graph || {nodes: [], edges: [], paths: []});
        setFilters(prev.current.filters || defaultFilters);
        if (prev.current.graphType) setGraphType(prev.current.graphType);
      }
      return prev;
    });
  }, [setGraph]);

  const handleRedo = useCallback(() => {
    setHistory(h => {
      const next = redo(h);
      if (next.current) {
        setGraph(next.current.graph || {nodes: [], edges: [], paths: []});
        setFilters(next.current.filters || defaultFilters);
        if (next.current.graphType) setGraphType(next.current.graphType);
      }
      return next;
    });
  }, [setGraph]);

  useEffect(() => {
    const handler = (e) => {
      if (e.key === 'Escape') {
        setSelected(null); setDetail(null); setContextMenu(null);
      }
      if (e.key === 'f' && !e.ctrlKey && !e.metaKey && document.activeElement?.tagName !== 'INPUT' && document.activeElement?.tagName !== 'TEXTAREA') {
        setShowFilters(f => !f);
      }
      if (e.key === 'i' && !e.ctrlKey && document.activeElement?.tagName !== 'INPUT' && document.activeElement?.tagName !== 'TEXTAREA') {
        if (selected) setSelected(null); // toggle inspector
      }
      if (e.key === '/' && document.activeElement?.tagName !== 'INPUT') {
        e.preventDefault();
        const searchInput = explorerRef.current?.querySelector('.kgr-filter-bar input[type="text"]');
        if (searchInput) searchInput.focus();
      }
      const digit = parseInt(e.key);
      if (digit >= 1 && digit <= 8 && !e.ctrlKey && document.activeElement?.tagName !== 'INPUT' && document.activeElement?.tagName !== 'TEXTAREA') {
        const types = ['knowledge', 'relationship', 'metadata', 'ontology', 'temporal', 'provenance', 'impact', 'similarity'];
        if (types[digit - 1]) setGraphType(types[digit - 1]);
      }
      if (e.key === 'z' && (e.ctrlKey || e.metaKey) && !e.shiftKey) handleUndo();
      if (e.key === 'z' && (e.ctrlKey || e.metaKey) && e.shiftKey) handleRedo();
      if (e.key === 'Z' && (e.ctrlKey || e.metaKey)) handleRedo();
    };
    window.addEventListener('keydown', handler);
    return () => window.removeEventListener('keydown', handler);
  }, [selected, handleUndo, handleRedo]);

  const handleContextMenu = useCallback((e, type, data) => {
    e.preventDefault();
    const items = [];
    if (type === 'node' && data) {
      items.push({label: 'Expand neighborhood', icon: 'graph', action: () => expand(data)});
      items.push({label: 'Explore blast radius', icon: 'activity', action: () => { setSelected(data); computeBlastRadius(); }});
      items.push({label: 'Trace lineage', icon: 'shield', action: () => { setSelected(data); computeLineage(); }});
      items.push({divider: true});
      items.push({label: 'Copy canonical ID', icon: 'check', action: () => { try { navigator.clipboard.writeText(data.id); } catch {} }});
    } else if (type === 'edge' && data) {
      items.push({label: 'Inspect relationship', icon: 'link', action: () => { setSelectedEdge(data); setSelected(null); }});
      items.push({label: 'Copy edge details', icon: 'check', action: () => { try { navigator.clipboard.writeText(JSON.stringify(data, null, 2)); } catch {} }});
    } else {
      items.push({label: 'Fit all', icon: 'graph', action: () => {}});
      items.push({label: 'Reset filters', icon: 'close', action: () => setFilters(defaultFilters)});
    }
    setContextMenu({x: e.clientX, y: e.clientY, items});
  }, [expand, computeBlastRadius, computeLineage]);

  const bookmarkState = useMemo(() => ({
    graph, filters, graphType, selectedId: selected?.id,
  }), [graph, filters, graphType, selected]);

  const restoreBookmark = useCallback((state) => {
    if (state.graph) setGraph(state.graph);
    if (state.filters) setFilters(state.filters);
    if (state.graphType) setGraphType(state.graphType);
  }, [setGraph]);

  const inspect = useCallback(async (node) => {
    setSelected(node);
    setSelectedEdge(null);
    setBlastRadius(null);
    setReverseImpact(null);
    setMetrics(null);
    setFullCentrality(null);
    setSimilarNodes(null);
    setWhatIfResult(null);
    setHighlightedPath(null);
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
      const [br, ri] = await Promise.all([
        api('/api/v1/graph/blast-radius', {canonical_id: selected.id, max_depth: 4}),
        api('/api/v1/graph/reverse-impact', {canonical_id: selected.id, max_depth: 4}).catch(() => null),
      ]);
      setBlastRadius(br);
      setReverseImpact(ri);
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

  const computeFullCentrality = useCallback(() => {
    if (!selected) return;
    run(async () => {
      const result = await api('/api/v1/graph/centrality/full', {
        canonical_ids: [selected.id],
        algorithms: ['degree', 'betweenness', 'closeness', 'pagerank', 'eigenvector', 'katz', 'hits', 'harmonic'],
      });
      setFullCentrality(result[selected.id] || null);
      setAllCentrality(Object.values(result));
    });
  }, [selected, api, run]);

  const computeSimilarity = useCallback(() => {
    if (!selected) return;
    run(async () => {
      const result = await api('/api/v1/graph/similarity', {
        canonical_id: selected.id, algorithm: 'jaccard', limit: 10,
      });
      setSimilarNodes(result);
    });
  }, [selected, api, run]);

  const computeWhatIf = useCallback(() => {
    if (!selected) return;
    run(async () => {
      const result = await api('/api/v1/graph/what-if', {canonical_id: selected.id, action: 'remove'});
      setWhatIfResult(result);
    });
  }, [selected, api, run]);

  const exploreBlastRadius = useCallback(() => {
    if (!selected) return;
    setGraphType('impact');
    run(async () => {
      const result = await api('/api/v1/impact', {canonical_id: selected.id, max_depth: 4, result_limit: 200});
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

  const visibleNodes = useMemo(() => (graph.nodes || []).filter(n =>
    (filters.domain === 'ALL' || n.domain === filters.domain) &&
    (filters.label === 'ALL' || n.label === filters.label) &&
    (filters.source === 'ALL' || n.properties?.source_connector === filters.source)
  ), [graph.nodes, filters]);
  const nodeIds = useMemo(() => new Set(visibleNodes.map(n => n.id)), [visibleNodes]);
  const visibleEdges = useMemo(() => (graph.edges || []).filter(e =>
    nodeIds.has(e.from_id) && nodeIds.has(e.to_id) &&
    (filters.edgeType === 'ALL' || e.type === filters.edgeType) &&
    (filters.trust === 'ALL' || String(e.creation_status || e.properties?.creation_status || 'DETERMINISTIC').toUpperCase() === filters.trust)
  ), [graph.edges, nodeIds, filters]);

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
          reverseImpact={reverseImpact} fullCentrality={fullCentrality} similarNodes={similarNodes}
          whatIfResult={whatIfResult} allCentrality={allCentrality} graphNodeCount={(graph.nodes || []).length}
          highlightedPath={highlightedPath}
          onImpact={computeImpact} onBlastRadius={computeBlastRadius} onLineage={computeLineage}
          onFullCentrality={computeFullCentrality} onSimilarity={computeSimilarity} onWhatIf={computeWhatIf}
          onExploreBlast={exploreBlastRadius}
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
          reverseImpact={reverseImpact} fullCentrality={fullCentrality} similarNodes={similarNodes}
          whatIfResult={whatIfResult} allCentrality={allCentrality} graphNodeCount={(graph.nodes || []).length}
          highlightedPath={highlightedPath}
          onImpact={computeImpact} onBlastRadius={computeBlastRadius} onLineage={computeLineage}
          onFullCentrality={computeFullCentrality} onSimilarity={computeSimilarity} onWhatIf={computeWhatIf}
          onExploreBlast={exploreBlastRadius}
          onClose={() => {setSelected(null); setDetail(null);}} busy={busy}/>
      </div>}

      {graphType === 'provenance' && <ProvenanceGraphView graph={graph} onInspect={n => run(() => inspect(n))} selected={selected}/>}

      {graphType === 'impact' && <ImpactGraphView api={api} run={run} busy={busy} graph={graph} setGraph={setGraph}/>}

      {graphType === 'similarity' && <SimilarityGraphView api={api} run={run} busy={busy} graph={graph} onHighlightPath={setHighlightedPath}/>}
    </div>

    {showBlast && blastRadius && <BlastRadiusView data={blastRadius} onClose={() => setShowBlast(false)}/>}
  </div>;
}
