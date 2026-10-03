import React, {useCallback, useState} from 'react';
import {Icon} from '../../icons.jsx';

function PatternNode({node, onUpdate, onRemove}) {
  return <div className="qb-node">
    <div className="qb-node-header">
      <strong>{node.label || 'Entity'}</strong>
      <button className="icon-button" onClick={onRemove} title="Remove"><Icon name="close" size={12}/></button>
    </div>
    <input type="text" placeholder="Entity type" value={node.label || ''} className="qb-node-type"
      onChange={e => onUpdate({...node, label: e.target.value})} aria-label="Entity type"/>
    {(node.filters || []).map((f, i) =>
      <div key={i} className="qb-filter">
        <input type="text" placeholder="Property" value={f.key || ''} className="qb-filter-key"
          onChange={e => {const nf = [...node.filters]; nf[i] = {...f, key: e.target.value}; onUpdate({...node, filters: nf});}}/>
        <select value={f.operator || '='} className="qb-filter-op"
          onChange={e => {const nf = [...node.filters]; nf[i] = {...f, operator: e.target.value}; onUpdate({...node, filters: nf});}}>
          <option value="=">=</option><option value="!=">!=</option>
          <option value=">">{'>'}</option><option value="<">{'<'}</option>
          <option value="contains">contains</option><option value="regex">regex</option>
        </select>
        <input type="text" placeholder="Value" value={f.value || ''} className="qb-filter-value"
          onChange={e => {const nf = [...node.filters]; nf[i] = {...f, value: e.target.value}; onUpdate({...node, filters: nf});}}/>
      </div>
    )}
    <button className="secondary-button qb-add-filter" onClick={() => onUpdate({...node, filters: [...(node.filters || []), {key: '', operator: '=', value: ''}]})}>
      + Filter
    </button>
  </div>;
}

function visualPatternToQueryPlan(patternNodes, patternEdges, options) {
  const anchors = patternNodes.filter(n => n.label).map(n => n.label);
  const filters = [];
  for (const n of patternNodes) {
    for (const f of n.filters || []) {
      if (f.key && f.value) filters.push({field: f.key, operator: f.operator || '=', value: f.value});
    }
  }
  return {
    intent: 'SEARCH', anchors, filters,
    max_depth: options.maxDepth || 4,
    result_limit: options.resultLimit || 100,
    evidence_mode: 'NONE',
  };
}

export default function QueryBuilder({schema, onExecute, onClose}) {
  const [nodes, setNodes] = useState([{id: 1, label: '', filters: []}]);
  const [edges, setEdges] = useState([]);
  const [maxDepth, setMaxDepth] = useState(4);
  const [resultLimit, setResultLimit] = useState(100);
  const [savedQueries, setSavedQueries] = useState(() => {
    try { return JSON.parse(localStorage.getItem('kgr-saved-queries') || '[]'); } catch { return []; }
  });

  const vertexLabels = Object.keys(schema?.vertex_labels || {});
  const edgeLabels = Object.keys(schema?.edge_labels || {});
  let nextId = Math.max(...nodes.map(n => n.id), 0) + 1;

  const addNode = () => setNodes(prev => [...prev, {id: nextId++, label: '', filters: []}]);
  const updateNode = (id, data) => setNodes(prev => prev.map(n => n.id === id ? data : n));
  const removeNode = (id) => setNodes(prev => prev.filter(n => n.id !== id));

  const addEdge = () => {
    if (nodes.length < 2) return;
    setEdges(prev => [...prev, {from: nodes[0].id, to: nodes[nodes.length - 1].id, type: ''}]);
  };

  const executeQuery = useCallback(() => {
    const plan = visualPatternToQueryPlan(nodes, edges, {maxDepth, resultLimit});
    if (onExecute) onExecute(plan);
  }, [nodes, edges, maxDepth, resultLimit, onExecute]);

  const saveQuery = useCallback(() => {
    const name = prompt('Query name:');
    if (!name) return;
    const saved = [...savedQueries, {name, nodes, edges, maxDepth, resultLimit}];
    setSavedQueries(saved);
    try { localStorage.setItem('kgr-saved-queries', JSON.stringify(saved)); } catch {}
  }, [nodes, edges, maxDepth, resultLimit, savedQueries]);

  const loadQuery = useCallback((q) => {
    setNodes(q.nodes); setEdges(q.edges || []);
    setMaxDepth(q.maxDepth || 4); setResultLimit(q.resultLimit || 100);
  }, []);

  return <div className="query-builder panel" role="dialog" aria-label="Visual query builder">
    <div className="panel-heading">
      <div><span className="eyebrow">VISUAL QUERY BUILDER</span><h2>Build queries without code</h2></div>
      <button className="icon-button" onClick={onClose}><Icon name="close"/></button>
    </div>

    <div className="qb-palette">
      <span className="eyebrow">ENTITY TYPES</span>
      <div className="qb-palette-chips">
        {vertexLabels.slice(0, 20).map(l => <button key={l} className="qb-palette-chip"
          onClick={() => setNodes(prev => [...prev, {id: nextId++, label: l, filters: []}])}>{l}</button>)}
      </div>
    </div>

    <div className="qb-canvas">
      {nodes.map(n => <PatternNode key={n.id} node={n}
        onUpdate={data => updateNode(n.id, data)} onRemove={() => removeNode(n.id)}/>)}
      <button className="secondary-button" onClick={addNode}><Icon name="graph" size={14}/> Add entity</button>
      {nodes.length >= 2 && <button className="secondary-button" onClick={addEdge}><Icon name="link" size={14}/> Add edge</button>}
    </div>

    {edges.length > 0 && <div className="qb-edges">
      <span className="eyebrow">EDGES</span>
      {edges.map((e, i) => <div key={i} className="qb-edge">
        <span>Node {e.from}</span><Icon name="chevron" size={14}/>
        <select value={e.type} onChange={ev => {const ne = [...edges]; ne[i] = {...e, type: ev.target.value}; setEdges(ne);}}>
          <option value="">Any type</option>
          {edgeLabels.map(l => <option key={l} value={l}>{l}</option>)}
        </select>
        <span>Node {e.to}</span>
      </div>)}
    </div>}

    <div className="qb-options">
      <label>Max depth: <input type="number" min="1" max="8" value={maxDepth} onChange={e => setMaxDepth(Number(e.target.value))}/></label>
      <label>Result limit: <input type="number" min="1" max="500" value={resultLimit} onChange={e => setResultLimit(Number(e.target.value))}/></label>
    </div>

    <div className="qb-actions">
      <button className="primary-button" onClick={executeQuery}><Icon name="graph" size={16}/>Run query</button>
      <button className="secondary-button" onClick={saveQuery}><Icon name="check" size={14}/>Save</button>
      <button className="secondary-button" onClick={() => {setNodes([{id: 1, label: '', filters: []}]); setEdges([]);}}>Clear</button>
    </div>

    {savedQueries.length > 0 && <div className="qb-saved">
      <span className="eyebrow">SAVED QUERIES</span>
      {savedQueries.map((q, i) => <button key={i} className="qb-saved-item" onClick={() => loadQuery(q)}>
        <Icon name="database" size={14}/>{q.name}
      </button>)}
    </div>}
  </div>;
}
