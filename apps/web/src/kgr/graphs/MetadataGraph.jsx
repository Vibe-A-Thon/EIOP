import React from 'react';
import {Icon} from '../../icons.jsx';
import {palette} from '../../GraphCanvas.jsx';

export default function MetadataGraph({schema}) {
  if (!schema) return <div className="empty-state"><span className="empty-icon"><Icon name="database" size={22}/></span><strong>Loading schema...</strong></div>;

  const labels = Object.entries(schema.vertex_labels || {});
  const edges = Object.entries(schema.edge_labels || {});

  return <div className="kgr-metadata-view">
    <section className="panel">
      <div className="panel-heading"><div><span className="eyebrow">VERTEX LABELS</span><h2>Entity types ({labels.length})</h2></div></div>
      <div className="schema-grid">{labels.map(([name, info]) =>
        <div key={name} className="schema-card" tabIndex="0">
          <div className="schema-card-header"><span className="type-dot" style={{background: palette[name] || '#94a3b8'}}/><strong>{name}</strong><span className="badge">{info.instance_count}</span></div>
          <small className="schema-domain">{info.domain}</small>
          <div className="schema-props"><strong>Required:</strong> {info.required_properties.join(', ')}</div>
          {info.optional_properties.length > 0 && <div className="schema-props"><strong>Optional:</strong> {info.optional_properties.join(', ')}</div>}
        </div>
      )}</div>
    </section>
    <section className="panel">
      <div className="panel-heading"><div><span className="eyebrow">EDGE LABELS</span><h2>Relationship types ({edges.length})</h2></div></div>
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
