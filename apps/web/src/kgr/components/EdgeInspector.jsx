import React from 'react';
import {Icon} from '../../icons.jsx';
import {palette} from '../../GraphCanvas.jsx';

function shortId(value, size = 22) {
  if (!value) return '—';
  return value.length > size ? `${value.slice(0, size - 1)}…` : value;
}

export default function EdgeInspector({edge, sourceNode, targetNode, onClose, onNavigate}) {
  if (!edge) return null;

  const props = edge.properties || {};
  const status = (edge.creation_status || props.creation_status || 'DETERMINISTIC').toUpperCase();
  const statusColor = status === 'DETERMINISTIC' ? '#22c55e' : status === 'INFERRED' ? '#f59e0b' : status === 'AMBIGUOUS' ? '#f97316' : status === 'MANUAL' ? '#3b82f6' : '#94a3b8';

  const parallelCount = edge._parallelCount || 0;

  return <section className="kgr-edge-inspector panel" aria-label="Edge inspector">
    <div className="inspector-heading">
      <span className="entity-symbol" style={{'--entity-color': '#64748b'}}><Icon name="link" size={16}/></span>
      <div><span className="eyebrow">RELATIONSHIP</span><h2>{edge.type || edge.label || 'Unknown'}</h2></div>
      <button className="icon-button" onClick={onClose} title="Close" aria-label="Close"><Icon name="close"/></button>
    </div>

    <div className="edge-endpoints">
      <button className="edge-endpoint-card" onClick={() => sourceNode && onNavigate && onNavigate(sourceNode)}>
        <span className="type-dot" style={{background: palette[sourceNode?.label] || '#94a3b8'}}/>
        <div>
          <span className="eyebrow">SOURCE</span>
          <strong>{shortId(edge.from_id || sourceNode?.id, 30)}</strong>
          <small>{sourceNode?.label || ''}</small>
        </div>
        <Icon name="chevron" size={14}/>
      </button>
      <span className="edge-direction-arrow"><Icon name="chevron" size={18}/></span>
      <button className="edge-endpoint-card" onClick={() => targetNode && onNavigate && onNavigate(targetNode)}>
        <span className="type-dot" style={{background: palette[targetNode?.label] || '#94a3b8'}}/>
        <div>
          <span className="eyebrow">TARGET</span>
          <strong>{shortId(edge.to_id || targetNode?.id, 30)}</strong>
          <small>{targetNode?.label || ''}</small>
        </div>
        <Icon name="chevron" size={14}/>
      </button>
    </div>

    <div className="edge-status-row">
      <span className="edge-status-badge" style={{background: statusColor}}>{status}</span>
      {parallelCount > 1 && <span className="badge">{parallelCount} parallel edges</span>}
    </div>

    {(props.source_ref || props.evidence_key || props.method) && <div className="edge-evidence-section">
      <h3><Icon name="shield" size={14}/> Evidence</h3>
      <dl className="property-list">
        {props.source_ref && <div><dt>Source ref</dt><dd>{props.source_ref}</dd></div>}
        {props.evidence_key && <div><dt>Evidence key</dt><dd>{props.evidence_key}</dd></div>}
        {props.method && <div><dt>Method</dt><dd>{props.method}</dd></div>}
      </dl>
    </div>}

    <h3>Properties</h3>
    <dl className="property-list">
      {Object.entries(props).filter(([k]) => !['source_ref', 'evidence_key', 'method', 'creation_status'].includes(k)).map(([k, v]) =>
        <div key={k}><dt>{k.replaceAll('_', ' ')}</dt><dd>{String(v)}</dd></div>
      )}
    </dl>

    <div className="edge-raw-section">
      <button className="secondary-button" onClick={() => { try { navigator.clipboard.writeText(JSON.stringify(edge, null, 2)); } catch {} }}>
        <Icon name="check" size={14}/> Copy edge JSON
      </button>
    </div>
  </section>;
}
