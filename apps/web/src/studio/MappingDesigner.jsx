import React, {useEffect, useMemo, useState} from 'react';
import {Icon} from '../icons.jsx';
import {downloadJson, flattenJson, labelProperties, loadArtifacts, saveArtifacts, schemaLabels, schemaEdgeLabels, uid} from './studio-utils.js';

export default function MappingDesigner({api, run}) {
  const [schema, setSchema] = useState(null);
  const [schemaError, setSchemaError] = useState('');
  const [sampleText, setSampleText] = useState('');
  const [sample, setSample] = useState(null);
  const [parseError, setParseError] = useState('');
  const [mappingName, setMappingName] = useState('my-mapping');
  const [vertices, setVertices] = useState([]); // [{id, label, keyField, bindings: {prop: path}}]
  const [edges, setEdges] = useState([]); // [{id, type, fromLabel, toLabel, bindings}]
  const [saved, setSaved] = useState(() => loadArtifacts('eoip-studio-mappings'));

  useEffect(() => {
    if (!api) return;
    run(async () => {
      try {
        setSchema(await api('/api/v1/graph/schema'));
      } catch (exception) {
        setSchemaError(exception.message || 'Ontology schema could not be loaded.');
      }
    });
  }, [api]);

  const fields = useMemo(() => sample ? flattenJson(sample) : [], [sample]);
  const labels = schemaLabels(schema);
  const edgeTypes = schemaEdgeLabels(schema);

  function parseSample(text) {
    setParseError('');
    setSampleText(text);
    try {
      setSample(text.trim() ? JSON.parse(text) : null);
    } catch (exception) {
      setSample(null);
      setParseError(`Sample is not valid JSON: ${exception.message}`);
    }
  }

  function onFile(event) {
    const file = event.target.files?.[0];
    if (!file) return;
    const reader = new FileReader();
    reader.onload = () => parseSample(String(reader.result || ''));
    reader.readAsText(file);
    event.target.value = '';
  }

  function bind(vertexId, prop, path) {
    setVertices(list => list.map(vertex => vertex.id === vertexId
      ? {...vertex, bindings: {...vertex.bindings, [prop]: path}}
      : vertex));
  }

  function addVertex(label) {
    setVertices(list => [...list, {id: uid('vm'), label, keyField: '', bindings: {}}]);
  }

  function addEdge(type) {
    setEdges(list => [...list, {id: uid('em'), type, fromLabel: labels[0] || '', toLabel: labels[0] || '', bindings: {}}]);
  }

  const mapping = useMemo(() => ({
    format: 'eoip.field-mapping.v1',
    id: uid('mapping'),
    name: mappingName,
    sample_hint: sample && typeof sample === 'object' && !Array.isArray(sample) ? Object.keys(sample).slice(0, 12) : undefined,
    vertices: vertices.map(vertex => ({
      label: vertex.label,
      key_property: vertex.keyField || undefined,
      properties: Object.fromEntries(Object.entries(vertex.bindings).filter(([, path]) => path)),
    })),
    edges: edges.map(edge => ({
      type: edge.type,
      from_label: edge.fromLabel,
      to_label: edge.toLabel,
      properties: Object.fromEntries(Object.entries(edge.bindings).filter(([, path]) => path)),
    })),
  }), [mappingName, sample, vertices, edges]);

  const validation = useMemo(() => {
    const problems = [];
    if (!mappingName.trim()) problems.push('Mapping name is required.');
    if (!sample) problems.push('Load a sample JSON document to design against.');
    if (!vertices.length) problems.push('Add at least one vertex mapping.');
    vertices.forEach(vertex => {
      if (!Object.values(vertex.bindings).some(Boolean)) problems.push(`Vertex "${vertex.label}" has no bound properties.`);
    });
    return problems;
  }, [mappingName, sample, vertices]);

  function download() {
    downloadJson(`${mappingName.replace(/\W+/g, '-').toLowerCase() || 'mapping'}.json`, mapping);
  }

  function saveToLibrary() {
    if (validation.length) return;
    const next = [mapping, ...saved.filter(item => item.name !== mapping.name)].slice(0, 30);
    setSaved(next);
    saveArtifacts('eoip-studio-mappings', next);
  }

  return <div>
    {schemaError && <div className="studio-warn"><Icon name="warning" size={16}/><span>{schemaError} You can still design mappings; enter target labels manually.</span></div>}
    <div className="studio-grid">
      <section className="studio-panel" aria-label="Source fields">
        <h3><Icon name="document" size={15}/> 1. Sample document</h3>
        <div className="studio-field"><span>Paste JSON or upload a file</span>
          <textarea value={sampleText} onChange={event => parseSample(event.target.value)} placeholder='{"key": "REQ-1", "summary": "…"}' aria-label="Sample JSON document"/>
        </div>
        <div className="studio-row" style={{marginBottom: 10}}>
          <label className="ghost-button" style={{cursor: 'pointer'}}>
            <Icon name="upload" size={14}/> Upload file
            <input type="file" accept=".json,application/json" onChange={onFile} style={{display: 'none'}}/>
          </label>
        </div>
        {parseError && <div className="studio-error"><Icon name="warning" size={16}/><span>{parseError}</span></div>}
        <h3><Icon name="code" size={15}/> Source fields</h3>
        {fields.length === 0 && <div className="studio-empty"><strong>No fields detected</strong>Paste or upload a sample JSON document.</div>}
        <div className="studio-row">
          {fields.slice(0, 40).map(field => <span key={field.path} className="studio-chip" draggable
            onDragStart={event => event.dataTransfer.setData('text/field', field.path)}
            onClick={() => navigator.clipboard?.writeText(field.path).catch(() => {})}
            title={`${field.type} — drag onto a property slot`}>
            {field.path}
          </span>)}
        </div>
      </section>
      <section className="studio-panel" aria-label="Target mappings">
        <h3><Icon name="graph" size={15}/> 2. Target vertex / edge mappings</h3>
        <div className="studio-field"><span>Mapping name</span>
          <input type="text" value={mappingName} onChange={event => setMappingName(event.target.value)}/>
        </div>
        <div className="studio-row" style={{marginBottom: 10}}>
          <label className="select-control"><Icon name="layers" size={14}/>
            <select value="" onChange={event => event.target.value && addVertex(event.target.value)} aria-label="Add vertex mapping">
              <option value="">+ Vertex mapping…</option>
              {labels.map(label => <option key={label} value={label}>{label}</option>)}
              {!labels.length && <option value="Custom">Custom label</option>}
            </select>
          </label>
          <label className="select-control"><Icon name="link" size={14}/>
            <select value="" onChange={event => event.target.value && addEdge(event.target.value)} aria-label="Add edge mapping">
              <option value="">+ Edge mapping…</option>
              {(edgeTypes.length ? edgeTypes : ['RELATED_TO']).map(type => <option key={type} value={type}>{type}</option>)}
            </select>
          </label>
        </div>
        {vertices.length === 0 && edges.length === 0 && <div className="studio-empty"><strong>No mappings yet</strong>Choose a target vertex label or edge type, then drag source fields onto its property slots.</div>}
        {vertices.map(vertex => <div key={vertex.id} className="studio-panel" style={{padding: 12}}>
          <div className="studio-row" style={{justifyContent: 'space-between'}}>
            <strong><Icon name="layers" size={14}/> {vertex.label}</strong>
            <button type="button" className="icon-button" aria-label={`Remove ${vertex.label}`} onClick={() => setVertices(list => list.filter(item => item.id !== vertex.id))}><Icon name="close" size={14}/></button>
          </div>
          <div className="studio-field" style={{marginTop: 8}}><span>Key property (identity)</span>
            <select value={vertex.keyField} onChange={event => setVertices(list => list.map(item => item.id === vertex.id ? {...item, keyField: event.target.value} : item))}>
              <option value="">— none —</option>
              {labelProperties(schema, vertex.label).map(prop => <option key={prop} value={prop}>{prop}</option>)}
              {Object.keys(vertex.bindings).map(prop => <option key={prop} value={prop}>{prop}</option>)}
            </select>
          </div>
          {labelProperties(schema, vertex.label).map(prop => <div key={prop}
            className={`studio-slot ${vertex.bindings[prop] ? 'filled' : ''}`}
            onDragOver={event => { event.preventDefault(); event.currentTarget.classList.add('drop-target'); }}
            onDragLeave={event => event.currentTarget.classList.remove('drop-target')}
            onDrop={event => {
              event.preventDefault();
              event.currentTarget.classList.remove('drop-target');
              const path = event.dataTransfer.getData('text/field');
              if (path) bind(vertex.id, prop, path);
            }}>
            <span>{prop}</span>
            <select value={vertex.bindings[prop] || ''} onChange={event => bind(vertex.id, prop, event.target.value)} aria-label={`Source field for ${prop}`}>
              <option value="">— unbound —</option>
              {fields.map(field => <option key={field.path} value={field.path}>{field.path}</option>)}
            </select>
          </div>)}
          {!labelProperties(schema, vertex.label).length && <div className="studio-field"><span>Custom property name</span>
            <div className="studio-row">
              <input id={`custom-prop-${vertex.id}`} type="text" placeholder="property"/>
              <button type="button" className="ghost-button" onClick={() => {
                const input = document.getElementById(`custom-prop-${vertex.id}`);
                if (input.value.trim()) { bind(vertex.id, input.value.trim(), vertex.bindings[input.value.trim()] || ''); input.value = ''; }
              }}><Icon name="plus" size={13}/></button>
            </div>
          </div>}
        </div>)}
        {edges.map(edge => <div key={edge.id} className="studio-panel" style={{padding: 12}}>
          <div className="studio-row" style={{justifyContent: 'space-between'}}>
            <strong><Icon name="link" size={14}/> {edge.type}</strong>
            <button type="button" className="icon-button" aria-label={`Remove ${edge.type}`} onClick={() => setEdges(list => list.filter(item => item.id !== edge.id))}><Icon name="close" size={14}/></button>
          </div>
          <div className="studio-row" style={{marginTop: 8}}>
            <label className="select-control">
              <select value={edge.fromLabel} onChange={event => setEdges(list => list.map(item => item.id === edge.id ? {...item, fromLabel: event.target.value} : item))} aria-label="From vertex label">
                {labels.map(label => <option key={label} value={label}>{label}</option>)}
              </select>
            </label>
            <Icon name="arrow" size={14}/>
            <label className="select-control">
              <select value={edge.toLabel} onChange={event => setEdges(list => list.map(item => item.id === edge.id ? {...item, toLabel: event.target.value} : item))} aria-label="To vertex label">
                {labels.map(label => <option key={label} value={label}>{label}</option>)}
              </select>
            </label>
          </div>
        </div>)}
      </section>
    </div>
    <section className="studio-panel" style={{marginTop: 14}}>
      <h3><Icon name="document" size={15}/> Mapping JSON</h3>
      {validation.length > 0 && <div className="studio-warn"><Icon name="warning" size={16}/><div>{validation.map((problem, index) => <div key={index}>{problem}</div>)}</div></div>}
      <pre className="studio-json">{JSON.stringify(mapping, null, 2)}</pre>
      <div className="studio-row" style={{marginTop: 10}}>
        <button type="button" className="primary-button" onClick={download} disabled={validation.length > 0}><Icon name="upload" size={15}/> Download mapping</button>
        <button type="button" className="ghost-button" onClick={saveToLibrary} disabled={validation.length > 0}>Save to library</button>
      </div>
      {saved.length > 0 && <ul className="studio-list" style={{marginTop: 10}}>{saved.map(item => <li key={item.id}>
        <span><strong>{item.name}</strong> <span className="studio-latency">{item.vertices?.length || 0} vertices · {item.edges?.length || 0} edges</span></span>
        <button type="button" className="icon-button" aria-label={`Remove ${item.name}`} onClick={() => {
          const next = saved.filter(entry => entry.id !== item.id);
          setSaved(next);
          saveArtifacts('eoip-studio-mappings', next);
        }}><Icon name="close" size={14}/></button>
      </li>)}</ul>}
    </section>
  </div>;
}
