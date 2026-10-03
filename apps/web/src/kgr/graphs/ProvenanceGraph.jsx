import React from 'react';
import {Icon} from '../../icons.jsx';
import {palette} from '../../GraphCanvas.jsx';

function displayLabel(node) {
  return node?.properties?.issue_key || node?.properties?.display_name || node?.properties?.name || node?.properties?.qualified_name || node?.properties?.path || node?.label || 'Unknown';
}

export default function ProvenanceGraph({graph, onInspect, selected}) {
  const evidenceNodes = (graph.nodes || []).filter(n => ['Evidence', 'IngestionRun', 'ValidationRun'].includes(n.label));

  return <div className="kgr-provenance-view">
    <section className="panel">
      <div className="panel-heading">
        <div><span className="eyebrow">PROVENANCE CHAIN</span>
          <h2>Evidence & ingestion lineage</h2>
          <p>Entities are connected to their source evidence and ingestion runs.</p>
        </div>
        <span className="count-badge">{evidenceNodes.length} provenance entities</span>
      </div>
      {evidenceNodes.length ? <div className="provenance-list">{evidenceNodes.map(n =>
        <button key={n.id} onClick={() => onInspect(n)} className={selected?.id === n.id ? 'selected' : ''}>
          <span className="type-dot" style={{background: palette[n.label] || '#94a3b8'}}/>
          <span>
            <strong>{n.properties?.source_ref || n.properties?.run_kind || displayLabel(n)}</strong>
            <small>{n.label} · {n.properties?.method || n.properties?.run_status || ''}</small>
          </span>
          <Icon name="chevron" size={14}/>
        </button>
      )}</div> : <div className="empty-state">
        <span className="empty-icon"><Icon name="shield" size={22}/></span>
        <strong>No provenance entities</strong>
        <p>Search and expand entities to load their evidence chain.</p>
      </div>}
    </section>
  </div>;
}
