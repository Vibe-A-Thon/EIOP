import React from 'react';
import {Icon} from '../../icons.jsx';
import {palette} from '../../GraphCanvas.jsx';

export default function OntologyGraph({schema}) {
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
    <section className="panel">
      <div className="panel-heading"><div><span className="eyebrow">ONTOLOGY</span>
        <h2>Enterprise ontology v{schema.ontology_version}</h2>
        <p>Schema v{schema.schema_version} · {domains.length} domains · {Object.keys(labels).length} entity types</p>
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
    <section className="panel">
      <div className="panel-heading"><div><span className="eyebrow">INDEXES</span><h2>Index coverage</h2></div></div>
      <div className="index-list">{(schema.indexes || []).map(idx =>
        <div key={idx.name} className="index-row"><Icon name="check" size={14}/><strong>{idx.name}</strong>
          <span className="badge">{idx.type}</span><small>{idx.label || 'global'} · {idx.fields.join(', ')}</small>
        </div>
      )}</div>
    </section>
  </div>;
}
