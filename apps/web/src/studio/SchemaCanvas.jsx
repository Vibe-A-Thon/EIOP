import React, {useEffect, useRef, useState} from 'react';
import {Icon} from '../icons.jsx';
import {downloadJson, schemaEdgeLabels, schemaLabels, uid} from './studio-utils.js';

const NODE_W = 150;
const NODE_H = 44;

function nodeCenter(node) {
  return {x: node.x + NODE_W / 2, y: node.y + NODE_H / 2};
}

export default function SchemaCanvas({api, run}) {
  const [schema, setSchema] = useState(null);
  const [schemaError, setSchemaError] = useState('');
  const [nodes, setNodes] = useState([]);
  const [edges, setEdges] = useState([]);
  const [selected, setSelected] = useState(null);
  const [pending, setPending] = useState(null); // {fromId, x, y}
  const [edgeType, setEdgeType] = useState('RELATED_TO');
  const dragRef = useRef(null);
  const svgRef = useRef(null);

  useEffect(() => {
    if (!api) return;
    run(async () => {
      try {
        setSchema(await api('/api/v1/graph/schema'));
      } catch (exception) {
        setSchemaError(exception.message || 'Schema could not be loaded.');
      }
    });
  }, [api]);

  useEffect(() => {
    const labels = schemaEdgeLabels(schema);
    if (labels.length && !labels.includes(edgeType)) setEdgeType(labels[0]);
  }, [schema]);

  const labels = schemaLabels(schema);

  function svgPoint(event) {
    const rect = svgRef.current.getBoundingClientRect();
    return {x: event.clientX - rect.left, y: event.clientY - rect.top};
  }

  function addNode(label, at) {
    const position = at || {x: 60 + (nodes.length % 5) * 40, y: 60 + nodes.length * 24};
    setNodes(list => [...list, {id: uid('class'), label, x: position.x, y: position.y}]);
  }

  function onPaletteDrop(event) {
    event.preventDefault();
    const label = event.dataTransfer.getData('text/label');
    if (label) addNode(label, svgPoint(event));
  }

  function onNodePointerDown(event, node) {
    event.stopPropagation();
    const point = svgPoint(event);
    dragRef.current = {kind: 'move', id: node.id, dx: point.x - node.x, dy: point.y - node.y};
    setSelected({kind: 'node', id: node.id});
    event.target.setPointerCapture?.(event.pointerId);
  }

  function onPortPointerDown(event, node) {
    event.stopPropagation();
    const c = nodeCenter(node);
    setPending({fromId: node.id, x: c.x, y: c.y});
  }

  function onSvgPointerMove(event) {
    if (pending) {
      const point = svgPoint(event);
      setPending({...pending, x: point.x, y: point.y});
      return;
    }
    const drag = dragRef.current;
    if (!drag) return;
    const point = svgPoint(event);
    if (drag.kind === 'move') {
      setNodes(list => list.map(node => node.id === drag.id ? {...node, x: point.x - drag.dx, y: point.y - drag.dy} : node));
    }
  }

  function onSvgPointerUp(event) {
    if (pending) {
      const point = svgPoint(event);
      const target = nodes.find(node => {
        if (node.id === pending.fromId) return false;
        const c = nodeCenter(node);
        return Math.hypot(c.x - point.x, c.y - point.y) < NODE_W;
      });
      if (target) {
        setEdges(list => [...list, {id: uid('rel'), from: pending.fromId, to: target.id, type: edgeType}]);
      }
      setPending(null);
    }
    dragRef.current = null;
  }

  function removeSelected() {
    if (!selected) return;
    if (selected.kind === 'node') {
      setNodes(list => list.filter(node => node.id !== selected.id));
      setEdges(list => list.filter(edge => edge.from !== selected.id && edge.to !== selected.id));
    } else {
      setEdges(list => list.filter(edge => edge.id !== selected.id));
    }
    setSelected(null);
  }

  const draft = {
    format: 'eoip.ontology-schema-draft.v1',
    classes: nodes.map(node => ({name: node.label, canvas: {x: Math.round(node.x), y: Math.round(node.y)}})),
    relationships: edges.map(edge => ({
      from: nodes.find(node => node.id === edge.from)?.label,
      to: nodes.find(node => node.id === edge.to)?.label,
      type: edge.type,
    })),
  };

  return <div>
    <div className="studio-toolbar">
      <button type="button" className="primary-button" onClick={() => downloadJson('ontology-schema-draft.json', draft)} disabled={!nodes.length}>
        <Icon name="upload" size={15}/> Export draft JSON
      </button>
      <button type="button" className="ghost-button" onClick={removeSelected} disabled={!selected}>Remove selected</button>
      <label className="select-control"><Icon name="link" size={14}/>
        <select value={edgeType} onChange={event => setEdgeType(event.target.value)} aria-label="Relationship type for new edges">
          {(schemaEdgeLabels(schema).length ? schemaEdgeLabels(schema) : ['RELATED_TO']).map(label => <option key={label} value={label}>{label}</option>)}
        </select>
      </label>
      <span className="studio-latency">{nodes.length} classes · {edges.length} relationships</span>
    </div>
    {schemaError && <div className="studio-error"><Icon name="warning" size={16}/><span>{schemaError} Add classes manually below; the canvas works without a live schema.</span></div>}
    <div className="studio-grid">
      <section className="studio-panel" aria-label="Class palette">
        <h3><Icon name="layers" size={15}/> Class palette</h3>
        {labels.length === 0 && !schemaError && <div className="studio-empty"><strong>No schema loaded</strong>Waiting for /api/v1/graph/schema…</div>}
        {labels.length === 0 && schemaError && <div className="studio-field"><span>Custom class name</span>
          <div className="studio-row">
            <input id="studio-custom-class" type="text" placeholder="e.g. Requirement"/>
            <button type="button" className="ghost-button" onClick={() => {
              const input = document.getElementById('studio-custom-class');
              if (input.value.trim()) { addNode(input.value.trim()); input.value = ''; }
            }}><Icon name="plus" size={14}/> Add</button>
          </div>
        </div>}
        {labels.map(label => <div key={label} className="studio-palette-item" draggable
          onDragStart={event => event.dataTransfer.setData('text/label', label)}
          onDoubleClick={() => addNode(label)} title="Drag onto the canvas or double-click to place">
          <span>{label}</span><small><Icon name="graph" size={13}/></small>
        </div>)}
        <p className="studio-hint">Drag a class onto the canvas. Drag node → port to draw a relationship. Double-click places at a default position.</p>
      </section>
      <section aria-label="Schema canvas">
        <svg ref={svgRef} className="studio-canvas" role="application" aria-label="Ontology schema canvas"
          onDragOver={event => event.preventDefault()}
          onDrop={onPaletteDrop}
          onPointerMove={onSvgPointerMove}
          onPointerUp={onSvgPointerUp}
          onPointerLeave={() => { dragRef.current = null; setPending(null); }}>
          <defs>
            <marker id="studio-arrow" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto">
              <path d="M0,0 L8,4 L0,8" fill="none" stroke="var(--accent, #5b4bce)" strokeWidth="1.4"/>
            </marker>
          </defs>
          {edges.map(edge => {
            const from = nodes.find(node => node.id === edge.from);
            const to = nodes.find(node => node.id === edge.to);
            if (!from || !to) return null;
            const a = nodeCenter(from);
            const b = nodeCenter(to);
            const mid = {x: (a.x + b.x) / 2, y: (a.y + b.y) / 2};
            return <g key={edge.id} onClick={() => setSelected({kind: 'edge', id: edge.id})} style={{cursor: 'pointer'}}>
              <line x1={a.x} y1={a.y} x2={b.x} y2={b.y} className="studio-edge-line" strokeWidth={selected?.kind === 'edge' && selected.id === edge.id ? 3 : 1.6}/>
              <text x={mid.x} y={mid.y - 4} textAnchor="middle" className="studio-edge-label">{edge.type}</text>
            </g>;
          })}
          {pending && (() => {
            const from = nodes.find(node => node.id === pending.fromId);
            const a = from ? nodeCenter(from) : pending;
            return <line x1={a.x} y1={a.y} x2={pending.x} y2={pending.y} className="studio-edge-line pending"/>;
          })()}
          {nodes.map(node => <g key={node.id} transform={`translate(${node.x}, ${node.y})`}
            onPointerDown={event => onNodePointerDown(event, node)}>
            <rect width={NODE_W} height={NODE_H} rx="9"
              className={`studio-node-rect ${selected?.kind === 'node' && selected.id === node.id ? 'selected' : ''}`}/>
            <text x={NODE_W / 2} y={NODE_H / 2 + 4} textAnchor="middle" className="studio-node-text">{node.label}</text>
            <circle cx={NODE_W / 2} cy={NODE_H} r="5" className="studio-port"
              onPointerDown={event => onPortPointerDown(event, node)}/>
          </g>)}
          {nodes.length === 0 && <text x="50%" y="50%" textAnchor="middle" className="studio-edge-label">Drop classes here to start drafting the ontology schema</text>}
        </svg>
      </section>
    </div>
    <section className="studio-panel" style={{marginTop: 14}}>
      <h3><Icon name="document" size={15}/> Draft preview</h3>
      <pre className="studio-json">{JSON.stringify(draft, null, 2)}</pre>
      <p className="studio-hint">Export only — no backend write endpoint exists for schema drafts. Save the JSON and promote it via config/ontology.</p>
    </section>
  </div>;
}
