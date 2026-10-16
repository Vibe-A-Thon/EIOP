import React, {useCallback, useEffect, useMemo, useRef, useState} from 'react';
import GraphCanvas, {palette, getSemanticZoomLevel, applySemanticZoom, fisheyeDistort} from '../GraphCanvas.jsx';
import {Icon, Tip} from '../icons.jsx';
import CentralityRadar from './components/CentralityRadar.jsx';
import ContextMenu from './components/ContextMenu.jsx';
import ExplorationHistoryBar, {createHistory, pushState, undo, redo} from './components/ExplorationHistory.jsx';
import GraphBookmarks from './components/GraphBookmarks.jsx';
import GraphToolbar from './components/GraphToolbar.jsx';
import ExportMenu from './components/ExportMenu.jsx';
import TimelineScrubber from './components/TimelineScrubber.jsx';
import SigmaRenderer from './renderers/SigmaRenderer.jsx';
import VirtualEntityList from './components/VirtualEntityList.jsx';
import EventFeed from './components/EventFeed.jsx';
import GraphDiff from './components/GraphDiff.jsx';
import GraphHealth from './components/GraphHealth.jsx';
import EdgeInspector from './components/EdgeInspector.jsx';
import Minimap from './components/Minimap.jsx';
import useGraphEvents from './hooks/useGraphEvents.js';
import ComboNode, {applyComboNodes, groupByDomain, groupByType, groupByCommunity} from './components/ComboNode.jsx';
import CodePanel from './components/CodePanel.jsx';
import QueryBuilder from './components/QueryBuilder.jsx';
import GeoMap from './components/GeoMap.jsx';
import PRDashboard from './components/PRDashboard.jsx';
import StyleRules, {applyStyleRules} from './components/StyleRules.jsx';
import TableView from './components/TableView.jsx';
import Playbooks from './components/Playbooks.jsx';
import SurprisePanel from './components/SurprisePanel.jsx';
import AIExplorer from './components/AIExplorer.jsx';
import {generateInteractiveHTML} from './export/InteractiveExport.js';
import {generateGraphReport} from './export/GraphReport.js';
import MetadataGraphView from './graphs/MetadataGraph.jsx';
import OntologyGraphView from './graphs/OntologyGraph.jsx';
import ProvenanceGraphView from './graphs/ProvenanceGraph.jsx';
import ImpactGraphView from './graphs/ImpactGraph.jsx';
import SimilarityGraphView from './graphs/SimilarityGraph.jsx';
import RelationshipGraphView from './graphs/RelationshipGraph.jsx';

const graphTypes = [
  {id: 'knowledge', label: 'Knowledge', icon: 'graph', hint: 'Entity-centric knowledge graph with relationships and evidence'},
  {id: 'relationship', label: 'Relationships', icon: 'link', hint: 'Edge-centric analysis: which entity types connect via which relationships'},
  {id: 'metadata', label: 'Metadata', icon: 'database', hint: 'Schema topology: vertex labels, edge labels, property schemas, and indexes'},
  {id: 'ontology', label: 'Ontology', icon: 'layers', hint: 'Class hierarchy, domain decomposition, and ontology structure'},
  {id: 'temporal', label: 'Temporal', icon: 'clock', hint: 'Time-windowed views with temporal filtering'},
  {id: 'provenance', label: 'Provenance', icon: 'shield', hint: 'Evidence chains, ingestion lineage, and trust propagation'},
  {id: 'impact', label: 'Impact', icon: 'activity', hint: 'Blast radius, centrality analysis, and what-if simulation'},
  {id: 'similarity', label: 'Similarity', icon: 'users', hint: 'Node similarity scores, common neighbors, and structural equivalence'},
  {id: 'diff', label: 'Diff', icon: 'activity', hint: 'Compare graph snapshots and visualize structural changes'},
  {id: 'health', label: 'Health', icon: 'check', hint: 'Graph health dashboard: completeness, connectivity, anomalies'},
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
  const hasActiveFilters = filters.domain !== 'ALL' || filters.label !== 'ALL' || filters.edgeType !== 'ALL' || filters.trust !== 'ALL' || filters.source !== 'ALL' || filters.evidence !== 'ALL' || filters.searchText || filters.minDegree > 0 || (filters.temporal && (filters.temporal.from || filters.temporal.to)) || (filters.community && filters.community !== 'ALL');
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
          <option value="AMBIGUOUS">Ambiguous</option>
          <option value="MANUAL">Manual</option>
        </select>
      </label>
      <label className="select-control" title="Filter by evidence"><Icon name="shield" size={14}/>
        <select value={filters.evidence} onChange={e => onChange({...filters, evidence: e.target.value})} aria-label="Evidence filter">
          <option value="ALL">All evidence</option>
          <option value="EVIDENCED">Evidenced only</option>
          <option value="UNEVIDENCED">Unevidenced only</option>
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
      <label className="filter-range" title="Min degree threshold">
        <Icon name="graph" size={14}/>
        <input type="number" min="0" max="100" value={filters.minDegree || 0} placeholder="Min degree"
          onChange={e => onChange({...filters, minDegree: parseInt(e.target.value) || 0})} aria-label="Min degree"/>
      </label>
      <label className="filter-date" title="Temporal filter (from)">
        <Icon name="clock" size={14}/>
        <input type="date" value={(filters.temporal || {}).from || ''}
          onChange={e => onChange({...filters, temporal: {...(filters.temporal || {}), from: e.target.value}})} aria-label="From date"/>
      </label>
      <label className="filter-date" title="Temporal filter (to)">
        <input type="date" value={(filters.temporal || {}).to || ''}
          onChange={e => onChange({...filters, temporal: {...(filters.temporal || {}), to: e.target.value}})} aria-label="To date"/>
      </label>
      <label className="select-control" title="Filter by community"><Icon name="users" size={14}/>
        <select value={filters.community || 'ALL'} onChange={e => onChange({...filters, community: e.target.value})} aria-label="Community filter">
          <option value="ALL">All communities</option>
        </select>
      </label>
      <label className="filter-search" title="Search within visible nodes">
        <Icon name="focus" size={14}/>
        <input type="text" placeholder="Search nodes..." value={filters.searchText || ''}
          onChange={e => onChange({...filters, searchText: e.target.value})} aria-label="Search within view"/>
      </label>
      {hasActiveFilters && <button className="filter-reset" onClick={() => onChange(defaultFilters)} title="Reset all filters">
        <Icon name="close" size={12}/>Reset
      </button>}
    </div>
    <div className="kgr-filter-chips">
      {filters.domain !== 'ALL' && <span className="filter-chip" onClick={() => onChange({...filters, domain: 'ALL'})}>{filters.domain} <Icon name="close" size={11}/></span>}
      {filters.label !== 'ALL' && <span className="filter-chip" onClick={() => onChange({...filters, label: 'ALL'})}>{filters.label} <Icon name="close" size={11}/></span>}
      {filters.edgeType !== 'ALL' && <span className="filter-chip" onClick={() => onChange({...filters, edgeType: 'ALL'})}>{filters.edgeType} <Icon name="close" size={11}/></span>}
      {filters.trust !== 'ALL' && <span className="filter-chip" onClick={() => onChange({...filters, trust: 'ALL'})}>{filters.trust} <Icon name="close" size={11}/></span>}
      {filters.evidence !== 'ALL' && <span className="filter-chip" onClick={() => onChange({...filters, evidence: 'ALL'})}>{filters.evidence} <Icon name="close" size={11}/></span>}
      {filters.source !== 'ALL' && <span className="filter-chip" onClick={() => onChange({...filters, source: 'ALL'})}>{filters.source} <Icon name="close" size={11}/></span>}
      {(filters.minDegree || 0) > 0 && <span className="filter-chip" onClick={() => onChange({...filters, minDegree: 0})}>degree≥{filters.minDegree} <Icon name="close" size={11}/></span>}
      {filters.searchText && <span className="filter-chip" onClick={() => onChange({...filters, searchText: ''})}>"{filters.searchText}" <Icon name="close" size={11}/></span>}
      {filters.temporal?.from && <span className="filter-chip" onClick={() => onChange({...filters, temporal: {...filters.temporal, from: ''}})}>from {filters.temporal.from} <Icon name="close" size={11}/></span>}
      {filters.temporal?.to && <span className="filter-chip" onClick={() => onChange({...filters, temporal: {...filters.temporal, to: ''}})}>to {filters.temporal.to} <Icon name="close" size={11}/></span>}
      {filters.community && filters.community !== 'ALL' && <span className="filter-chip" onClick={() => onChange({...filters, community: 'ALL'})}>community {filters.community} <Icon name="close" size={11}/></span>}
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

const defaultFilters = {domain: 'ALL', label: 'ALL', edgeType: 'ALL', trust: 'ALL', evidence: 'ALL', source: 'ALL', minDegree: 0, searchText: '', temporal: {from: '', to: ''}, community: 'ALL'};

export default function KGRExplorer({graph, setGraph, api, run, busy, stats, apiBase}) {
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
  const [renderProgress, setRenderProgress] = useState(null);
  const [renderedCount, setRenderedCount] = useState(0);
  const [showEntityList, setShowEntityList] = useState(false);
  const [structureAnalysis, setStructureAnalysis] = useState(null);
  const [eventFeedCollapsed, setEventFeedCollapsed] = useState(true);
  const [layout, setLayout] = useState('cose');
  const [sizeMode, setSizeMode] = useState('uniform');
  const [showMinimap, setShowMinimap] = useState(true);
  const [showExport, setShowExport] = useState(false);
  const [timelineRange, setTimelineRange] = useState(null);
  const [comboMode, setComboMode] = useState(null);
  const [showCodePanel, setShowCodePanel] = useState(false);
  const [codeFile, setCodeFile] = useState(null);
  const [showQueryBuilder, setShowQueryBuilder] = useState(false);
  const [showGeoMode, setShowGeoMode] = useState(false);
  const [showPRDashboard, setShowPRDashboard] = useState(false);
  const [viewport, setViewport] = useState(null);
  const [communities, setCommunities] = useState(null);
  const [orphanedCount, setOrphanedCount] = useState(null);
  const [fisheyeEnabled, setFisheyeEnabled] = useState(false);
  const [semanticZoom, setSemanticZoom] = useState('detail');
  const [colorBlindMode, setColorBlindMode] = useState('default');
  const [hubExclusionPct, setHubExclusionPct] = useState(0);
  const [showStyleRules, setShowStyleRules] = useState(false);
  const [lassoMode, setLassoMode] = useState(null);
  const [multiSelection, setMultiSelection] = useState([]);
  const [showTableView, setShowTableView] = useState(false);
  const [showPlaybooks, setShowPlaybooks] = useState(false);
  const [showSurprises, setShowSurprises] = useState(false);
  const [surpriseData, setSurpriseData] = useState(null);
  const [showAIExplorer, setShowAIExplorer] = useState(false);
  const [deepLinkState, setDeepLinkState] = useState(null);
  const explorerRef = useRef(null);
  const cyRef = useRef(null);

  const {events: graphEvents, status: wsStatus, pause: pauseEvents, resume: resumeEvents, clear: clearEvents} = useGraphEvents(apiBase);

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
      if (digit >= 1 && digit <= 9 && !e.ctrlKey && document.activeElement?.tagName !== 'INPUT' && document.activeElement?.tagName !== 'TEXTAREA') {
        const types = ['knowledge', 'relationship', 'metadata', 'ontology', 'temporal', 'provenance', 'impact', 'similarity', 'diff', 'health'];
        if (types[digit - 1]) setGraphType(types[digit - 1]);
      }
      if (e.key === '0' && !e.ctrlKey && document.activeElement?.tagName !== 'INPUT' && document.activeElement?.tagName !== 'TEXTAREA') {
        setGraphType('health');
      }
      if (e.key === 'z' && (e.ctrlKey || e.metaKey) && !e.shiftKey) handleUndo();
      if (e.key === 'z' && (e.ctrlKey || e.metaKey) && e.shiftKey) handleRedo();
      if (e.key === 'Z' && (e.ctrlKey || e.metaKey)) handleRedo();
      if (e.key === 'm' && !e.ctrlKey && document.activeElement?.tagName !== 'INPUT' && document.activeElement?.tagName !== 'TEXTAREA') {
        setShowMinimap(v => !v);
      }
      if (e.key === 'c' && !e.ctrlKey && document.activeElement?.tagName !== 'INPUT' && document.activeElement?.tagName !== 'TEXTAREA') {
        setShowCodePanel(v => !v);
      }
      if (e.key === 'q' && !e.ctrlKey && document.activeElement?.tagName !== 'INPUT' && document.activeElement?.tagName !== 'TEXTAREA') {
        setShowQueryBuilder(v => !v);
      }
      if (e.key === 'g' && !e.ctrlKey && !e.shiftKey && document.activeElement?.tagName !== 'INPUT' && document.activeElement?.tagName !== 'TEXTAREA') {
        setComboMode(prev => prev ? null : 'domain');
      }
      if (e.key === 'F' && e.shiftKey && document.activeElement?.tagName !== 'INPUT' && document.activeElement?.tagName !== 'TEXTAREA') {
        setFisheyeEnabled(v => !v);
      }
      if (e.key === 't' && !e.ctrlKey && document.activeElement?.tagName !== 'INPUT' && document.activeElement?.tagName !== 'TEXTAREA') {
        setShowTableView(v => !v);
      }
      if (e.key === 'a' && !e.ctrlKey && document.activeElement?.tagName !== 'INPUT' && document.activeElement?.tagName !== 'TEXTAREA') {
        setShowAIExplorer(v => !v);
      }
    };
    window.addEventListener('keydown', handler);
    return () => window.removeEventListener('keydown', handler);
  }, [selected, handleUndo, handleRedo]);

  useEffect(() => {
    document.documentElement.setAttribute('data-palette', colorBlindMode);
    return () => document.documentElement.removeAttribute('data-palette');
  }, [colorBlindMode]);

  useEffect(() => {
    if (!deepLinkState) {
      try {
        const hash = window.location.hash.slice(1);
        if (hash) {
          const state = JSON.parse(atob(hash));
          if (state.graphType) setGraphType(state.graphType);
          if (state.filters) setFilters(state.filters);
          if (state.layout) setLayout(state.layout);
          setDeepLinkState(state);
        }
      } catch {}
    }
  }, []);

  const bookmarkState = useMemo(() => ({
    graph, filters, graphType, selectedId: selected?.id,
  }), [graph, filters, graphType, selected]);

  const restoreBookmark = useCallback((state) => {
    if (state.graph) setGraph(state.graph);
    if (state.filters) setFilters(state.filters);
    if (state.graphType) setGraphType(state.graphType);
  }, [setGraph]);

  const inspect = useCallback(async (node) => {
    if (node?.isCombo) {
      setSelected(node);
      setSelectedEdge(null);
      setDetail({
        outgoing: [],
        incoming: [],
        combo_members: node.memberIds || [],
      });
      return;
    }
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

  const computeStructureAnalysis = useCallback(() => {
    run(async () => {
      const [kcore, components, degDist] = await Promise.all([
        api('/api/v1/graph/k-core', {min_k: 1}).catch(() => null),
        api('/api/v1/graph/components', {limit: 20}).catch(() => null),
        api('/api/v1/graph/degree-distribution').catch(() => null),
      ]);
      setStructureAnalysis({kcore, components, degDist});
    });
  }, [api, run]);

  const SIGMA_THRESHOLD = 5000;
  const PROGRESSIVE_THRESHOLD = 1000;
  const BATCH_SIZE = 100;

  const visibleNodes = useMemo(() => {
    const search = (filters.searchText || '').toLowerCase();
    return (graph.nodes || []).filter(n => {
      if (filters.domain !== 'ALL' && n.domain !== filters.domain) return false;
      if (filters.label !== 'ALL' && n.label !== filters.label) return false;
      if (filters.source !== 'ALL' && n.properties?.source_connector !== filters.source) return false;
      if (search && !displayLabel(n).toLowerCase().includes(search) && !(n.id || '').toLowerCase().includes(search)) return false;
      return true;
    });
  }, [graph.nodes, filters]);
  const progressiveNodes = useMemo(() => {
    if (visibleNodes.length <= PROGRESSIVE_THRESHOLD) return visibleNodes;
    const sorted = [...visibleNodes].sort((a, b) => (b.degree || 0) - (a.degree || 0));
    return sorted;
  }, [visibleNodes]);

  useEffect(() => {
    if (visibleNodes.length <= PROGRESSIVE_THRESHOLD) {
      setRenderedCount(visibleNodes.length);
      setRenderProgress(null);
      return;
    }
    setRenderedCount(200);
    setRenderProgress(`Rendering 200/${visibleNodes.length} nodes...`);
    let frame;
    let count = 200;
    const step = () => {
      count = Math.min(count + BATCH_SIZE, progressiveNodes.length);
      setRenderedCount(count);
      if (count < progressiveNodes.length) {
        setRenderProgress(`Rendering ${count}/${progressiveNodes.length} nodes...`);
        frame = requestAnimationFrame(step);
      } else {
        setRenderProgress(null);
      }
    };
    frame = requestAnimationFrame(step);
    return () => cancelAnimationFrame(frame);
  }, [visibleNodes.length, progressiveNodes.length]);

  const displayedNodes = useMemo(() => progressiveNodes.slice(0, renderedCount), [progressiveNodes, renderedCount]);
  const nodeIds = useMemo(() => new Set(displayedNodes.map(n => n.id)), [displayedNodes]);
  const visibleEdges = useMemo(() => (graph.edges || []).filter(e =>
    nodeIds.has(e.from_id) && nodeIds.has(e.to_id) &&
    (filters.edgeType === 'ALL' || e.type === filters.edgeType) &&
    (filters.trust === 'ALL' || String(e.creation_status || e.properties?.creation_status || 'DETERMINISTIC').toUpperCase() === filters.trust)
  ), [graph.edges, nodeIds, filters]);
  const comboGroups = useMemo(() => {
    if (comboMode === 'domain') return groupByDomain(displayedNodes);
    if (comboMode === 'type') return groupByType(displayedNodes);
    if (comboMode === 'community') return groupByCommunity(displayedNodes, communities);
    return [];
  }, [comboMode, displayedNodes, communities]);
  const renderedGraph = useMemo(
    () => applyComboNodes(displayedNodes, visibleEdges, comboGroups),
    [displayedNodes, visibleEdges, comboGroups],
  );
  const renderedNodes = renderedGraph.nodes;
  const renderedEdges = renderedGraph.edges;
  const selectGraphNode = useCallback((node) => run(() => inspect(node)), [run, inspect]);

  return <div className="kgr-explorer" ref={explorerRef}>
    <GraphTypeSelector active={graphType} onSelect={setGraphType}/>
    <ExplorationHistoryBar history={history} onUndo={handleUndo} onRedo={handleRedo}/>
    {showFilters && <FilterBar filters={filters} onChange={setFilters} schema={schema}/>}
    <GraphBookmarks currentState={bookmarkState} onRestore={restoreBookmark}/>

    <div className="kgr-content">
      {graphType === 'knowledge' && <div className="explorer-grid">
        <section className="panel graph-panel">
          <div className="panel-heading"><div><span className="eyebrow">KGR · KNOWLEDGE GRAPH</span><h2>Interactive entity-relationship map</h2></div>
            <div className="panel-heading-right">
              <span className="count-badge">{displayedNodes.length}{displayedNodes.length < visibleNodes.length ? `/${visibleNodes.length}` : ''} entities · {visibleEdges.length} relationships</span>
              {visibleNodes.length >= SIGMA_THRESHOLD && <span className="renderer-badge">WebGL</span>}
              {wsStatus === 'connected' && <span className="ws-status-badge connected" title="WebSocket connected">●</span>}
              {wsStatus === 'connecting' && <span className="ws-status-badge connecting" title="Connecting...">◌</span>}
            </div>
          </div>
          <GraphToolbar layout={layout} onLayoutChange={setLayout} sizeMode={sizeMode} onSizeModeChange={setSizeMode}
            onFitAll={() => cyRef.current?.fit()} onToggleMinimap={() => setShowMinimap(v => !v)}
            onToggleFilters={() => setShowFilters(v => !v)} onToggleEntityList={() => setShowEntityList(v => !v)}
            onExport={() => setShowExport(v => !v)}
            fisheyeEnabled={fisheyeEnabled} onToggleFisheye={() => setFisheyeEnabled(v => !v)}
            colorBlindMode={colorBlindMode} onColorBlindChange={setColorBlindMode}
            onToggleTableView={() => setShowTableView(v => !v)}
            onToggleDeepLink={() => {
              try {
                const state = btoa(JSON.stringify({graphType, filters, layout, selected: selected?.id, zoom: viewport?.zoom, pan: viewport?.pan}));
                navigator.clipboard.writeText(`${window.location.origin}${window.location.pathname}#${state}`);
              } catch {}
            }}
            multiSelectionCount={multiSelection.length}
            selectionMode={lassoMode}
            onSelectionModeChange={setLassoMode}
            comboMode={comboMode}
            onComboModeChange={setComboMode}
            onTogglePlaybooks={() => setShowPlaybooks(v => !v)}
            onToggleStyleRules={() => setShowStyleRules(v => !v)}
            onToggleAIExplorer={() => setShowAIExplorer(v => !v)}
            onToggleSurprises={() => {
              setShowSurprises(v => !v);
              if (!surpriseData) run(async () => {
                const data = await api('/api/v1/graph/surprises', {limit: 20}).catch(() => null);
                setSurpriseData(data);
              });
            }}/>
          {renderProgress && <div className="render-progress-bar"><div className="render-progress-fill" style={{width: `${(renderedCount / Math.max(visibleNodes.length, 1)) * 100}%`}}/><span>{renderProgress}</span></div>}
          {comboGroups.length > 0 && <ComboNode groups={comboGroups} onToggleExpand={() => setComboMode(null)} onRemoveGroup={() => setComboMode(null)}/>}
          {lassoMode && <div className="selection-mode-banner"><Icon name="focus" size={13}/><span>Drag on the canvas to select multiple entities.</span>{multiSelection.length > 0 && <strong>{multiSelection.length} selected</strong>}</div>}
          {showGeoMode
            ? <GeoMap elements={renderedNodes} edges={renderedEdges} onSelect={selectGraphNode}/>
            : visibleNodes.length >= SIGMA_THRESHOLD
              ? <SigmaRenderer nodes={renderedNodes} edges={renderedEdges}
                  selectedId={selected?.id} onSelectNode={selectGraphNode}
                  onSelectEdge={e => {setSelectedEdge(e); setSelected(null);}} onExpand={expand}
                  onViewportChange={setViewport} layout={layout}/>
              : <GraphCanvas nodes={renderedNodes} edges={renderedEdges} paths={graph.paths || []}
                  selectedId={selected?.id} selectedEdgeId={selectedEdge?.id}
                  onSelectNode={selectGraphNode} onSelectEdge={e => {setSelectedEdge(e); setSelected(null);}}
                  onExpand={expand} cyRef={cyRef} layout={layout} onLayoutChange={setLayout} onViewportChange={setViewport}
                  selectionMode={lassoMode} onSelectionChange={nodes => setMultiSelection(nodes.map(node => node.id))}/>
          }
        </section>
        {showCodePanel && <CodePanel filePath={codeFile} api={api}
          onSymbolClick={id => { const node = (graph.nodes || []).find(n => n.id === id); if (node) run(() => inspect(node)); }}
          onClose={() => setShowCodePanel(false)}/>}
        {showEntityList && <VirtualEntityList nodes={visibleNodes} selectedId={selected?.id}
          onSelect={n => run(() => inspect(n))} onExpand={expand} palette={palette}/>}
        <NodeInspector node={selected} detail={detail} metrics={metrics} blastRadius={blastRadius}
          reverseImpact={reverseImpact} fullCentrality={fullCentrality} similarNodes={similarNodes}
          whatIfResult={whatIfResult} allCentrality={allCentrality} graphNodeCount={(graph.nodes || []).length}
          highlightedPath={highlightedPath}
          onImpact={computeImpact} onBlastRadius={computeBlastRadius} onLineage={computeLineage}
          onFullCentrality={computeFullCentrality} onSimilarity={computeSimilarity} onWhatIf={computeWhatIf}
          onExploreBlast={exploreBlastRadius}
          onClose={() => {setSelected(null); setDetail(null);}} busy={busy}/>
      </div>}

      {graphType === 'relationship' && <RelationshipGraphView edges={graph.edges}/>}

      {graphType === 'metadata' && <MetadataGraphView schema={schema}/>}
      {graphType === 'ontology' && <OntologyGraphView schema={schema}/>}

      {graphType === 'temporal' && <div className="explorer-grid">
        <section className="panel graph-panel">
          <div className="panel-heading"><div><span className="eyebrow">KGR · TEMPORAL VIEW</span><h2>Time-filtered graph</h2></div></div>
          {visibleNodes.length >= SIGMA_THRESHOLD
            ? <SigmaRenderer nodes={displayedNodes} edges={visibleEdges}
                selectedId={selected?.id} onSelectNode={n => run(() => inspect(n))} onExpand={expand}
                onViewportChange={setViewport} layout={layout}/>
            : <GraphCanvas nodes={displayedNodes} edges={visibleEdges} paths={graph.paths || []}
                selectedId={selected?.id} onSelectNode={n => run(() => inspect(n))} onExpand={expand}
                cyRef={cyRef} layout={layout} onLayoutChange={setLayout} onViewportChange={setViewport}/>
          }
          <TimelineScrubber nodes={graph.nodes || []} range={timelineRange} onRangeChange={setTimelineRange}/>
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

      {graphType === 'impact' && <>
        <ImpactGraphView api={api} run={run} busy={busy} graph={graph} setGraph={setGraph}/>
        {structureAnalysis && <div className="kgr-structure-analysis">
          {structureAnalysis.components && <section className="panel">
            <div className="panel-heading"><div><span className="eyebrow">COMPONENTS</span>
              <h2>{structureAnalysis.components.total_components} connected components</h2></div></div>
            <div className="cluster-grid">{(structureAnalysis.components.components || []).slice(0, 10).map(c =>
              <div key={c.id} className="cluster-card">
                <div className="cluster-header"><strong>Component {c.id}</strong><span className="badge">{c.size}</span></div>
                <div className="cluster-members">{(c.members || []).slice(0, 3).map(m =>
                  <span key={m} className="cluster-member" title={m}>{shortId(m, 20)}</span>
                )}{c.members?.length > 3 && <span className="cluster-more">+{c.members.length - 3}</span>}</div>
              </div>
            )}</div>
          </section>}
          {structureAnalysis.degDist && <section className="panel">
            <div className="panel-heading"><div><span className="eyebrow">DEGREE DISTRIBUTION</span>
              <h2>{structureAnalysis.degDist.total_nodes} nodes</h2></div></div>
            <div className="degree-histogram">{Object.entries(structureAnalysis.degDist.distribution || {}).slice(0, 20).map(([deg, cnt]) =>
              <div key={deg} className="degree-bar-row">
                <span className="degree-label">deg {deg}</span>
                <span className="degree-bar"><i style={{width: `${Math.min(100, (cnt / Math.max(...Object.values(structureAnalysis.degDist.distribution))) * 100)}%`}}/></span>
                <strong>{cnt}</strong>
              </div>
            )}</div>
          </section>}
          {structureAnalysis.kcore && <section className="panel">
            <div className="panel-heading"><div><span className="eyebrow">K-CORE</span>
              <h2>Max k-core: {structureAnalysis.kcore.max_k}</h2></div></div>
            <div className="kcore-summary">{Object.entries(structureAnalysis.kcore.cores || {}).sort((a, b) => Number(b[0]) - Number(a[0])).slice(0, 8).map(([k, members]) =>
              <div key={k} className="kcore-row">
                <span className="badge">{k}-core</span><strong>{members.length} nodes</strong>
              </div>
            )}</div>
          </section>}
        </div>}
      </>}

      {graphType === 'similarity' && <SimilarityGraphView api={api} run={run} busy={busy} graph={graph} onHighlightPath={setHighlightedPath}/>}

      {graphType === 'diff' && <GraphDiff api={api} run={run} busy={busy}/>}
      {graphType === 'health' && <GraphHealth api={api} run={run} busy={busy}/>}
    </div>

    {selectedEdge && !selected && <EdgeInspector edge={selectedEdge}
      sourceNode={(graph.nodes || []).find(n => n.id === selectedEdge.from_id)}
      targetNode={(graph.nodes || []).find(n => n.id === selectedEdge.to_id)}
      onClose={() => setSelectedEdge(null)}
      onNavigate={n => { if (n) { setSelectedEdge(null); inspect(n); }}}/>}
    {showMinimap && <Minimap nodes={displayedNodes} selectedId={selected?.id} viewport={viewport}
      onNavigate={pos => { if (cyRef.current) cyRef.current.center(); }}/>}
    {showBlast && blastRadius && <BlastRadiusView data={blastRadius} onClose={() => setShowBlast(false)}/>}
    {showExport && <ExportMenu graph={{nodes: displayedNodes, edges: visibleEdges}} cyRef={cyRef}
      onClose={() => setShowExport(false)}/>}
    {showQueryBuilder && <QueryBuilder schema={schema} onExecute={(plan) => {
      run(async () => { const result = await api('/api/v1/query', plan); setGraph(result); });
      setShowQueryBuilder(false);
    }} onClose={() => setShowQueryBuilder(false)}/>}
    {showPRDashboard && <PRDashboard api={api} run={run} busy={busy} onClose={() => setShowPRDashboard(false)}/>}
    {showTableView && <TableView nodes={displayedNodes} edges={visibleEdges} selectedId={selected?.id}
      onSelect={n => run(() => inspect(n))} onClose={() => setShowTableView(false)}/>}
    {showStyleRules && <StyleRules onApply={() => {}} onClose={() => setShowStyleRules(false)}/>}
    {showPlaybooks && <Playbooks api={api} run={run} busy={busy} selected={selected}
      onAction={(action) => {
        if (action === 'blast-radius' && selected) computeBlastRadius();
        if (action === 'what-if' && selected) computeWhatIf();
        if (action === 'centrality' && selected) computeFullCentrality();
        if (action === 'reverse-impact' && selected) computeImpact();
      }}
      onClose={() => setShowPlaybooks(false)}/>}
    {showSurprises && <SurprisePanel data={surpriseData} onClose={() => setShowSurprises(false)}
      onHighlight={(type, item) => {
        if (type === 'edge' && item.source_id) {
          const node = (graph.nodes || []).find(n => n.id === item.source_id);
          if (node) run(() => inspect(node));
        }
      }}/>}
    {showAIExplorer && <AIExplorer api={api} run={run} busy={busy} selected={selected} graph={graph}
      onHighlight={(ids) => {
        if (ids?.length) {
          const node = (graph.nodes || []).find(n => ids.includes(n.id));
          if (node) run(() => inspect(node));
        }
      }}
      onClose={() => setShowAIExplorer(false)}/>}
    {fisheyeEnabled && <div className="fisheye-indicator"><Icon name="focus" size={12}/> Fisheye active (Shift+F)</div>}
    {contextMenu && <ContextMenu x={contextMenu.x} y={contextMenu.y} items={contextMenu.items} onClose={() => setContextMenu(null)}/>}
    <EventFeed events={graphEvents} status={wsStatus}
      onPause={pauseEvents} onResume={resumeEvents} onClear={clearEvents}
      onNavigate={(e) => {
        if (e.data?.canonical_id) {
          const node = (graph.nodes || []).find(n => n.id === e.data.canonical_id);
          if (node) run(() => inspect(node));
        }
      }}
      collapsed={eventFeedCollapsed} onToggle={() => setEventFeedCollapsed(v => !v)}/>
  </div>;
}
