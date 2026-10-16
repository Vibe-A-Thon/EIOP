import React, {useMemo, useRef, useState} from 'react';
import {Icon} from '../icons.jsx';
import {downloadJson, loadArtifacts, uid} from './studio-utils.js';

const NODE_W = 190;
const NODE_H = 48;

function nodeCenter(node) {
  return {x: node.x + NODE_W / 2, y: node.y + NODE_H / 2};
}

function topologicalOrder(nodes, edges) {
  const ids = new Set(nodes.map(node => node.id));
  const indegree = new Map(nodes.map(node => [node.id, 0]));
  const outgoing = new Map(nodes.map(node => [node.id, []]));
  edges.forEach(edge => {
    if (!ids.has(edge.from) || !ids.has(edge.to)) return;
    indegree.set(edge.to, (indegree.get(edge.to) || 0) + 1);
    outgoing.get(edge.from)?.push(edge.to);
  });
  const queue = nodes.filter(node => (indegree.get(node.id) || 0) === 0).map(node => node.id);
  const order = [];
  while (queue.length) {
    const id = queue.shift();
    order.push(id);
    (outgoing.get(id) || []).forEach(next => {
      const remaining = (indegree.get(next) || 0) - 1;
      indegree.set(next, remaining);
      if (remaining === 0) queue.push(next);
    });
  }
  return order;
}

export default function PipelineOrchestrator() {
  const connectors = loadArtifacts('eoip-studio-connectors');
  const mappings = loadArtifacts('eoip-studio-mappings');
  const [name, setName] = useState('my-pipeline');
  const [nodes, setNodes] = useState([]);
  const [edges, setEdges] = useState([]);
  const [pending, setPending] = useState(null);
  const dragRef = useRef(null);
  const svgRef = useRef(null);

  const library = useMemo(() => ([
    ...connectors.map(item => ({kind: 'connector', ref: item.name, detail: item.source, icon: 'database'})),
    ...mappings.map(item => ({kind: 'mapping', ref: item.name, detail: `${item.vertices?.length || 0} vertices`, icon: 'layers'})),
  ]), [connectors, mappings]);

  function svgPoint(event) {
    const rect = svgRef.current.getBoundingClientRect();
    return {x: event.clientX - rect.left, y: event.clientY - rect.top};
  }

  function addNode(entry, at) {
    const position = at || {x: 60 + (nodes.length % 4) * 60, y: 60 + nodes.length * 30};
    setNodes(list => [...list, {id: uid('step'), kind: entry.kind, ref: entry.ref, detail: entry.detail, x: position.x, y: position.y}]);
  }

  function onDrop(event) {
    event.preventDefault();
    const index = event.dataTransfer.getData('text/library-index');
    if (index !== '') addNode(library[Number(index)], svgPoint(event));
  }

  function onNodePointerDown(event, node) {
    event.stopPropagation();
    const point = svgPoint(event);
    dragRef.current = {id: node.id, dx: point.x - node.x, dy: point.y - node.y};
  }

  function onPortPointerDown(event, node) {
    event.stopPropagation();
    const c = nodeCenter(node);
    setPending({fromId: node.id, x: c.x, y: c.y});
  }

  function onPointerMove(event) {
    if (pending) {
      const point = svgPoint(event);
      setPending({...pending, x: point.x, y: point.y});
      return;
    }
    const drag = dragRef.current;
    if (!drag) return;
    const point = svgPoint(event);
    setNodes(list => list.map(node => node.id === drag.id ? {...node, x: point.x - drag.dx, y: point.y - drag.dy} : node));
  }

  function onPointerUp(event) {
    if (pending) {
      const point = svgPoint(event);
      const target = nodes.find(node => node.id !== pending.fromId && Math.hypot(nodeCenter(node).x - point.x, nodeCenter(node).y - point.y) < NODE_W);
      if (target && !edges.some(edge => edge.from === pending.fromId && edge.to === target.id)) {
        setEdges(list => [...list, {id: uid('edge'), from: pending.fromId, to: target.id}]);
      }
      setPending(null);
    }
    dragRef.current = null;
  }

  function removeNode(id) {
    setNodes(list => list.filter(node => node.id !== id));
    setEdges(list => list.filter(edge => edge.from !== id && edge.to !== id));
  }

  const order = useMemo(() => topologicalOrder(nodes, edges), [nodes, edges]);
  const cyclic = order.length !== nodes.length && nodes.length > 0;
  const orderedNodes = order.map(id => nodes.find(node => node.id === id)).filter(Boolean);

  const pipeline = {
    format: 'eoip.pipeline.v1',
    id: uid('pipeline'),
    name,
    steps: orderedNodes.map((node, index) => ({
      order: index + 1,
      kind: node.kind,
      ref: node.ref,
      depends_on: edges.filter(edge => edge.to === node.id).map(edge => orderedNodes.findIndex(item => item.id === edge.from) + 1).filter(value => value > 0),
    })),
  };

  return <div>
    <div className="studio-toolbar">
      <label className="studio-field" style={{marginBottom: 0, minWidth: 220}}><span>Pipeline name</span>
        <input type="text" value={name} onChange={event => setName(event.target.value)}/>
      </label>
      <button type="button" className="primary-button" onClick={() => downloadJson(`${name.replace(/\W+/g, '-').toLowerCase() || 'pipeline'}.json`, pipeline)} disabled={!nodes.length || cyclic}>
        <Icon name="upload" size={15}/> Export pipeline JSON
      </button>
      <span className="studio-latency">{nodes.length} steps · {edges.length} links {cyclic && '· cycle detected'}</span>
    </div>
    <div className="studio-grid">
      <section className="studio-panel" aria-label="Step library">
        <h3><Icon name="database" size={15}/> Step library</h3>
        {library.length === 0 && <div className="studio-empty"><strong>Library is empty</strong>Save a connector in Connector Builder or a mapping in Mapping Designer to use it as a pipeline step.</div>}
        {library.map((entry, index) => <div key={`${entry.kind}-${entry.ref}`} className="studio-palette-item" draggable
          onDragStart={event => event.dataTransfer.setData('text/library-index', String(index))}
          onDoubleClick={() => addNode(entry)} title="Drag onto the canvas or double-click">
          <span><Icon name={entry.icon} size={13}/> {entry.ref}</span><small>{entry.kind}</small>
        </div>)}
        <button type="button" className="ghost-button" style={{marginTop: 8}} onClick={() => addNode({kind: 'validation', ref: 'schema-validation', detail: 'Validate against ontology schema', icon: 'check'})}>
          <Icon name="plus" size={13}/> Add validation step
        </button>
        <p className="studio-hint">Connect steps from output port (bottom of node) to the next node. A linear run order is derived topologically; cycles block export.</p>
      </section>
      <section aria-label="Pipeline canvas">
        <svg ref={svgRef} className="studio-canvas" role="application" aria-label="Pipeline DAG canvas"
          onDragOver={event => event.preventDefault()}
          onDrop={onDrop}
          onPointerMove={onPointerMove}
          onPointerUp={onPointerUp}
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
            return <g key={edge.id}>
              <line x1={a.x} y1={a.y} x2={b.x} y2={b.y} className="studio-edge-line"
                onClick={() => setEdges(list => list.filter(item => item.id !== edge.id))} style={{cursor: 'pointer'}}>
                <title>Click to remove link</title>
              </line>
            </g>;
          })}
          {pending && (() => {
            const from = nodes.find(node => node.id === pending.fromId);
            const a = from ? nodeCenter(from) : pending;
            return <line x1={a.x} y1={a.y} x2={pending.x} y2={pending.y} className="studio-edge-line pending"/>;
          })()}
          {nodes.map((node, index) => <g key={node.id} transform={`translate(${node.x}, ${node.y})`} onPointerDown={event => onNodePointerDown(event, node)}>
            <rect width={NODE_W} height={NODE_H} rx="9" className="studio-node-rect"/>
            <text x={10} y={19} className="studio-node-text"><tspan fontWeight="700">{index + 1}. {node.ref.slice(0, 20)}</tspan></text>
            <text x={10} y={34} className="studio-edge-label">{node.kind} · {node.detail?.slice(0, 26) || ''}</text>
            <circle cx={NODE_W - 12} cy={12} r="7" className="studio-port" style={{cursor: 'pointer'}}
              onPointerDown={event => { event.stopPropagation(); removeNode(node.id); }}>
              <title>Click to remove step</title>
            </circle>
            <text x={NODE_W - 12} y={15.5} textAnchor="middle" style={{fontSize: 9, fill: 'var(--accent, #5b4bce)', pointerEvents: 'none'}}>×</text>
            <circle cx={NODE_W / 2} cy={NODE_H} r="5" className="studio-port" onPointerDown={event => onPortPointerDown(event, node)}/>
          </g>)}
          {nodes.length === 0 && <text x="50%" y="50%" textAnchor="middle" className="studio-edge-label">Drag connectors, mappings, or validations here to compose the pipeline</text>}
        </svg>
        {cyclic && <div className="studio-error" style={{marginTop: 10}}><Icon name="warning" size={16}/><span>The pipeline graph has a cycle — remove a link before exporting.</span></div>}
      </section>
    </div>
    <section className="studio-panel" style={{marginTop: 14}}>
      <h3><Icon name="activity" size={15}/> Run order</h3>
      {orderedNodes.length === 0 && <div className="studio-empty"><strong>No steps</strong>Compose the DAG to see the topological run order.</div>}
      <ol className="studio-list" style={{listStyle: 'decimal', paddingLeft: 22}}>
        {orderedNodes.map(node => <li key={node.id}><span><strong>{node.ref}</strong> <span className="studio-latency">{node.kind}</span></span></li>)}
      </ol>
      <pre className="studio-json" style={{marginTop: 10}}>{JSON.stringify(pipeline, null, 2)}</pre>
    </section>
  </div>;
}
