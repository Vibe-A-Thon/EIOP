const $ = id => document.getElementById(id);
const ns = 'http://www.w3.org/2000/svg';

const colors = {
  BUSINESS: '#bd7c12',
  WORK: '#3478cb',
  CODE: '#28977d',
  CICD: '#8b62c5',
  TEST: '#617d26',
  DESIGN: '#bd5394',
  OPS: '#c56336',
  KNOWLEDGE: '#299bb3',
  IDENTITY: '#62748b',
  DECISION: '#a75c33',
  PROCESS: '#5665c0',
  META: '#7b828d',
  AGENT: '#9c4794',
  INTEGRATION: '#3e8595'
};

const metaLabels = new Set(['Evidence', 'IngestionRun', 'GraphDomain', 'ValidationRun']);

const backends = [
  {
    id: 'hugegraph',
    name: 'Apache HugeGraph / Hubble',
    models: ['Property graph'],
    native: ['Gremlin'],
    architecture: ['Distributed graph engine', 'External storage backends', 'Hubble administration'],
    status: 'Live in this Hubble container'
  },
  {
    id: 'neptune',
    name: 'Amazon Neptune',
    models: ['Property graph', 'W3C RDF triple store'],
    native: ['openCypher', 'Gremlin', 'SPARQL'],
    architecture: ['Managed service', 'Multi-model graph', 'Decoupled storage and compute'],
    status: 'Supported by EOIP backend config'
  },
  {
    id: 'neo4j',
    name: 'Neo4j / Aura',
    models: ['Property graph'],
    native: ['Cypher', 'OpenCypher'],
    architecture: ['Transactional graph', 'Clustered deployments'],
    status: 'Adapter-ready profile'
  },
  {
    id: 'janusgraph',
    name: 'JanusGraph',
    models: ['Property graph'],
    native: ['Gremlin'],
    architecture: ['Distributed graph engine', 'Cassandra/HBase/Bigtable backends', 'Search index integration'],
    status: 'Adapter-ready profile'
  },
  {
    id: 'rdf',
    name: 'RDF / OWL Triple Stores',
    models: ['Semantic Web RDF', 'OWL ontologies', 'SKOS vocabularies'],
    native: ['SPARQL', 'SHACL'],
    architecture: ['Triple store', 'Reasoning engine', 'Named graphs'],
    status: 'Portable export and validation profile'
  },
  {
    id: 'multimodel',
    name: 'Multi-model Graph Stores',
    models: ['Property graph', 'Document graph', 'RDF-compatible projections'],
    native: ['GQL', 'Gremlin', 'Cypher', 'SQL graph extensions'],
    architecture: ['Polyglot persistence', 'Federated query', 'External storage'],
    status: 'Capability matrix profile'
  }
];

const languages = [
  {id: 'gremlin', name: 'Gremlin', family: 'Traversal', executable: true},
  {id: 'opencypher', name: 'OpenCypher', family: 'Property graph pattern matching'},
  {id: 'cypher', name: 'Cypher', family: 'Property graph pattern matching'},
  {id: 'gql', name: 'GQL', family: 'ISO graph query language'},
  {id: 'sparql', name: 'SPARQL', family: 'RDF graph query'},
  {id: 'shacl', name: 'SHACL', family: 'RDF shape constraints'},
  {id: 'rdf', name: 'RDF / Turtle', family: 'Semantic graph serialization'},
  {id: 'owl', name: 'OWL', family: 'Ontology representation'},
  {id: 'skos', name: 'SKOS', family: 'Knowledge organization'},
  {id: 'eoql', name: 'EOQL', family: 'Enterprise object query'},
  {id: 'eql', name: 'EQL', family: 'EOIP graph query DSL'},
  {id: 'osql', name: 'OSQL', family: 'Ontology SQL'},
  {id: 'semantic', name: 'Semantic Prompts / NLQ', family: 'Natural language to governed query'}
];

const intents = [
  {id: 'overview', name: 'Graph overview'},
  {id: 'neighborhood', name: 'Seed neighborhood'},
  {id: 'lineage', name: 'Lineage and evidence'},
  {id: 'schema', name: 'Schema inventory'},
  {id: 'quality', name: 'Quality and constraints'},
  {id: 'migration', name: 'Migration preview'}
];

let connection;
let graphData = {vertices: [], edges: []};
let viewport = {x: 0, y: 0, width: 1000, height: 650};
let positions = new Map();
let activeView = 'graph';
let activeLens = 'schema';

const quote = value => JSON.stringify(value);
const logical = edge => String(edge.label || edge.type || 'RELATED_TO').split('__')[0];
const props = record => record?.properties || {};
const canonical = vertex => props(vertex).canonical_id || vertex.id;

function caption(vertex) {
  const p = props(vertex);
  for (const key of ['display_name', 'name', 'summary', 'api_name', 'mr_title', 'message',
    'qualified_name', 'branch_name', 'tag_name', 'incident_number', 'path', 'run_kind', 'evidence_key']) {
    if (p[key]) return String(p[key]);
  }
  return `${vertex.label || 'Vertex'}: ${String(canonical(vertex) || '').split(':').pop()}`;
}

function element(tag, attributes = {}, text) {
  const node = document.createElementNS(ns, tag);
  for (const [name, value] of Object.entries(attributes)) node.setAttribute(name, value);
  if (text !== undefined) node.textContent = text;
  return node;
}

function setStatus(text, error = false) {
  $('result-status').textContent = text;
  $('result-status').className = error ? 'status-error' : '';
}

async function hubbleJson(url, options = {}) {
  const response = await fetch(url, {...options, signal: AbortSignal.timeout(60000)});
  if (!response.ok) throw new Error(`Hubble HTTP ${response.status}`);
  const body = await response.json();
  if (body.status !== undefined && body.status !== 200) {
    throw new Error(`Hubble ${body.status}: ${body.message || 'Query rejected'}`);
  }
  return body.status === undefined ? body : body.data;
}

async function physicalId(cid) {
  const bytes = await crypto.subtle.digest('SHA-256', new TextEncoder().encode(cid));
  return 'eoip-' + [...new Uint8Array(bytes)].map(n => n.toString(16).padStart(2, '0')).join('');
}

function setupSelectors() {
  for (const backend of backends) $('backend').add(new Option(backend.name, backend.id));
  for (const language of languages) $('language').add(new Option(`${language.name} - ${language.family}`, language.id));
  for (const intent of intents) $('intent').add(new Option(intent.name, intent.id));
  $('backend').value = 'hugegraph';
  $('language').value = 'gremlin';
  $('intent').value = 'overview';
}

function activeBackend() {
  return backends.find(item => item.id === $('backend').value) || backends[0];
}

function activeLanguage() {
  return languages.find(item => item.id === $('language').value) || languages[0];
}

function chips(values) {
  return `<div class="chip-row">${values.map(value => `<span class="chip">${value}</span>`).join('')}</div>`;
}

function renderBackendCard() {
  const backend = activeBackend();
  $('backend-status').textContent = backend.name;
  $('backend-card').innerHTML = `
    <strong>${backend.name}</strong>
    <p>${backend.status}</p>
    ${chips([...backend.models, ...backend.native])}
  `;
  $('details').textContent = JSON.stringify(backend, null, 2);
  renderCompatibility();
  generateQuery();
}

function renderCompatibility() {
  const backend = activeBackend();
  const language = activeLanguage();
  const native = backend.native.some(item => item.toLowerCase() === language.name.toLowerCase());
  const executable = language.executable && backend.id === 'hugegraph';
  const items = [
    ['Native match', native ? 'This language is native for the selected backend.' : 'Use EOIP translation, export, or an adapter-specific compiler.'],
    ['Live execution', executable ? 'Can run through the current Hubble Gremlin connection.' : 'Preview only in Hubble; run through the matching backend adapter/API.'],
    ['Representations', 'Property graph, relationship table, RDF-like triples, and raw JSON are available from one result set.'],
    ['Migration stance', 'Canonical IDs, edge keys, evidence references, and ontology labels are preserved across backend changes.']
  ];
  $('compatibility').replaceChildren();
  for (const [title, body] of items) {
    const item = document.createElement('div');
    item.className = 'compat-item';
    item.innerHTML = `<strong>${title}</strong><span>${body}</span>`;
    $('compatibility').append(item);
  }
  $('query-heading').textContent = `${language.name} for ${backend.name}`;
  $('execute').disabled = !executable;
}

function queryFor(language, intent, seed, limit) {
  const cid = seed || 'urn:eoip:demo:workitem:PAY-101';
  const escaped = cid.replaceAll('"', '\\"');
  const gremlinSeed = seed ? `g.V(${quote('PENDING_PHYSICAL_ID')})` : 'g.V()';
  const templates = {
    gremlin: {
      overview: `g.V().limit(${limit})`,
      neighborhood: `${gremlinSeed}.bothE().dedup().limit(${limit})`,
      lineage: `${gremlinSeed}.repeat(bothE().otherV().simplePath()).times(3).path().limit(${Math.min(limit, 40)})`,
      schema: `g.V().label().groupCount()`,
      quality: `g.V().hasNot('canonical_id').limit(${limit})`,
      migration: `g.V().project('id','label','canonical_id','domain').by(id()).by(label()).by('canonical_id').by('graph_domain').limit(${limit})`
    },
    opencypher: {
      overview: `MATCH (n) RETURN n LIMIT ${limit}`,
      neighborhood: `MATCH (n {canonical_id: "${escaped}"})-[r]-(m) RETURN n, r, m LIMIT ${limit}`,
      lineage: `MATCH p=(n {canonical_id: "${escaped}"})-[*1..3]-(m) RETURN p LIMIT ${Math.min(limit, 40)}`,
      schema: 'MATCH (n) RETURN labels(n) AS labels, count(*) AS count',
      quality: `MATCH (n) WHERE n.canonical_id IS NULL RETURN n LIMIT ${limit}`,
      migration: `MATCH (n) RETURN labels(n), n.canonical_id, n.graph_domain LIMIT ${limit}`
    },
    cypher: {
      overview: `MATCH (n) RETURN n LIMIT ${limit}`,
      neighborhood: `MATCH (n {canonical_id: "${escaped}"})-[r]-(m) RETURN n, r, m LIMIT ${limit}`,
      lineage: `MATCH p=(n {canonical_id: "${escaped}"})-[*1..3]-(m) RETURN p LIMIT ${Math.min(limit, 40)}`,
      schema: 'CALL db.labels() YIELD label RETURN label',
      quality: `MATCH (n) WHERE n.canonical_id IS NULL RETURN n LIMIT ${limit}`,
      migration: `MATCH (n) RETURN labels(n), properties(n) LIMIT ${limit}`
    },
    gql: {
      overview: `MATCH (n) RETURN n LIMIT ${limit}`,
      neighborhood: `MATCH (n {canonical_id: "${escaped}"})-[r]-(m) RETURN n, r, m LIMIT ${limit}`,
      lineage: `MATCH p = (n {canonical_id: "${escaped}"})-[*1..3]-(m) RETURN p LIMIT ${Math.min(limit, 40)}`,
      schema: 'MATCH (n) RETURN labels(n), count(n)',
      quality: `MATCH (n) WHERE n.canonical_id IS NULL RETURN n LIMIT ${limit}`,
      migration: `MATCH (n) RETURN n.canonical_id, labels(n), properties(n) LIMIT ${limit}`
    },
    sparql: {
      overview: `SELECT ?s ?p ?o WHERE { ?s ?p ?o } LIMIT ${limit}`,
      neighborhood: `SELECT ?p ?o WHERE { <${cid}> ?p ?o } LIMIT ${limit}`,
      lineage: `SELECT ?mid ?p ?o WHERE { <${cid}> ?p ?mid . ?mid ?p ?o } LIMIT ${Math.min(limit, 40)}`,
      schema: 'SELECT ?class (COUNT(?s) AS ?count) WHERE { ?s a ?class } GROUP BY ?class',
      quality: `SELECT ?s WHERE { ?s ?p ?o FILTER NOT EXISTS { ?s <urn:eoip:ontology:canonical_id> ?id } } LIMIT ${limit}`,
      migration: `CONSTRUCT { ?s ?p ?o } WHERE { ?s ?p ?o } LIMIT ${limit}`
    },
    shacl: {
      overview: 'eoip:EntityShape a sh:NodeShape ;\n  sh:property [ sh:path eoip:canonical_id ; sh:minCount 1 ] .',
      neighborhood: 'eoip:RelationshipShape a sh:NodeShape ;\n  sh:property [ sh:path eoip:evidence_ref ; sh:minCount 0 ] .',
      lineage: 'eoip:LineageShape a sh:NodeShape ;\n  sh:property [ sh:path eoip:source_ref ; sh:minCount 1 ] .',
      schema: 'eoip:OntologyShape a sh:NodeShape ;\n  sh:targetClass owl:Class .',
      quality: 'eoip:QualityGateShape a sh:NodeShape ;\n  sh:property [ sh:path eoip:canonical_id ; sh:minCount 1 ; sh:maxCount 1 ] .',
      migration: 'eoip:MigrationShape a sh:NodeShape ;\n  sh:property [ sh:path eoip:edge_key ; sh:minCount 1 ] .'
    },
    rdf: {
      overview: `CONSTRUCT { ?s ?p ?o } WHERE { ?s ?p ?o } LIMIT ${limit}`,
      neighborhood: `<${cid}> ?predicate ?object .`,
      lineage: `<${cid}> eoip:hasLineagePath ?path .`,
      schema: 'eoip:WorkItem rdf:type rdfs:Class .\neoip:IMPLEMENTS rdf:type rdf:Property .',
      quality: '[] eoip:qualityFinding "Missing canonical identity" .',
      migration: '[] eoip:migrationTarget "property-graph-and-rdf" .'
    },
    owl: {
      overview: 'Ontology: <urn:eoip:ontology>\nClass: eoip:WorkItem\nObjectProperty: eoip:IMPLEMENTS',
      neighborhood: `Individual: <${cid}>\n  Facts: eoip:relatedTo ?entity`,
      lineage: `ObjectProperty: eoip:dependsOn\n  Characteristics: Transitive`,
      schema: 'Class: eoip:Evidence\nClass: eoip:GraphDomain',
      quality: 'DataProperty: eoip:canonical_id\n  Characteristics: Functional',
      migration: 'AnnotationProperty: eoip:targetBackend'
    },
    skos: {
      overview: 'eoip:EnterpriseConceptScheme a skos:ConceptScheme .',
      neighborhood: `<${cid}> skos:related ?concept .`,
      lineage: '<urn:eoip:concept:lineage> skos:broader <urn:eoip:concept:governance> .',
      schema: '?concept skos:prefLabel ?label ; skos:inScheme eoip:EnterpriseConceptScheme .',
      quality: '?concept skos:prefLabel ?label FILTER(lang(?label) = "")',
      migration: '?concept skos:exactMatch ?targetConcept .'
    },
    eoql: {
      overview: `SELECT * FROM WorkItem LIMIT ${limit}`,
      neighborhood: `TRAVERSE FROM ${cid} DEPTH 2`,
      lineage: `TRAVERSE FROM ${cid} VIA EVIDENCED_BY DEPTH 3`,
      schema: 'AGGREGATE WorkItem BY status',
      quality: `SELECT canonical_id, summary FROM WorkItem WHERE status != done LIMIT ${limit}`,
      migration: `SELECT canonical_id, graph_domain, entity_type FROM WorkItem LIMIT ${limit}`
    },
    eql: {
      overview: `SEARCH * LABEL WorkItem LIMIT ${limit}`,
      neighborhood: `NEIGHBORS ${cid} DEPTH 2 LIMIT ${limit}`,
      lineage: `LINEAGE ${cid} DEPTH 4`,
      schema: 'DOMAINS',
      quality: `SEARCH missing evidence LIMIT ${limit}`,
      migration: `SEARCH graph_domain LIMIT ${limit}`
    },
    osql: {
      overview: 'LIST TYPES',
      neighborhood: `DESCRIBE WorkItem`,
      lineage: 'LIST RELATIONSHIPS',
      schema: 'SCHEMA FOR WorkItem',
      quality: `INSTANCES OF WorkItem LIMIT ${limit}`,
      migration: 'LIST DOMAINS'
    },
    semantic: {
      overview: 'Show the enterprise work graph with evidence and domain boundaries.',
      neighborhood: `Explain what is related to ${cid} and why those relationships exist.`,
      lineage: `Trace lineage and evidence for ${cid}.`,
      schema: 'Describe graph schema, ontology classes, query languages, and backend compatibility.',
      quality: 'Find missing identities, stale evidence, orphaned nodes, and low-confidence facts.',
      migration: 'Plan migration across HugeGraph, Neptune, Neo4j, RDF, and multi-model backends.'
    }
  };
  return (templates[language] || templates.gremlin)[intent] || templates[language].overview;
}

function generateQuery() {
  const language = $('language').value;
  const intent = $('intent').value;
  const seed = $('seed').value.trim();
  const limit = Number($('limit').value || 80);
  $('query').value = queryFor(language, intent, seed, limit);
  const executable = language === 'gremlin' && $('backend').value === 'hugegraph';
  $('query-note').textContent = executable
    ? 'This Gremlin query can be executed through the current Hubble connection. Seed queries are converted to HugeGraph physical ids at runtime.'
    : 'This is a portable query or semantic artifact preview. Execute it through the matching EOIP backend adapter or target graph database.';
  renderCompatibility();
}

async function executeHubbleQuery() {
  if (!connection) return setStatus('No Hubble connection', true);
  if ($('language').value !== 'gremlin' || $('backend').value !== 'hugegraph') {
    return setStatus('Preview only for this target', true);
  }
  $('execute').disabled = true;
  setStatus('Running Hubble query...');
  try {
    const limit = Number($('limit').value || 80);
    const seed = $('seed').value.trim();
    const useSeed = seed && ($('intent').value !== 'overview' || $('edges-only').checked);
    let vertexQuery;
    let edgeQuery;
    if (useSeed) {
      const id = await physicalId(seed);
      const start = `g.V(${quote(id)})`;
      vertexQuery = start;
      edgeQuery = `${start}.bothE().dedup().limit(${limit})`;
    } else {
      vertexQuery = `g.V().limit(${limit})`;
      edgeQuery = `g.E().limit(${limit})`;
    }
    $('query').value = edgeQuery;
    const execute = content => hubbleJson(`/api/v1.2/graph-connections/${connection}/gremlin-query`, {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({content})
    });
    const [vertices, edges] = await Promise.all([execute(vertexQuery), execute(edgeQuery)]);
    const graphVertices = [...(vertices.graph_view?.vertices || []), ...(edges.graph_view?.vertices || [])];
    const graphEdges = edges.graph_view?.edges || [];
    graphData = {
      vertices: [...new Map(graphVertices.map(vertex => [vertex.id, vertex])).values()],
      edges: graphEdges
    };
    setStatus(`${graphData.vertices.length} vertices / ${graphData.edges.length} relationships`);
    renderAll();
  } catch (error) {
    setStatus(error.message, true);
  } finally {
    $('execute').disabled = false;
  }
}

function graphForDisplay() {
  const vertices = graphData.vertices.filter(vertex => $('metadata').checked || !metaLabels.has(vertex.label));
  const allowed = new Set(vertices.map(vertex => vertex.id));
  const edges = graphData.edges.filter(edge => allowed.has(edge.source) && allowed.has(edge.target));
  return {vertices, edges};
}

function renderGraph() {
  const svg = $('graph');
  svg.replaceChildren();
  const {vertices, edges} = graphForDisplay();
  const byId = new Map(vertices.map(vertex => [vertex.id, vertex]));
  if (!vertices.length) {
    const empty = element('text', {x: 40, y: 60}, 'Run a live Hubble query to display a graph.');
    svg.append(empty);
    return;
  }

  const defs = element('defs');
  const marker = element('marker', {id: 'idl-arrow', viewBox: '0 0 10 10', refX: 9, refY: 5,
    markerWidth: 7, markerHeight: 7, orient: 'auto-start-reverse'});
  marker.append(element('path', {d: 'M 0 0 L 10 5 L 0 10 z', fill: '#53657b'}));
  defs.append(marker);
  svg.append(defs);

  const layers = new Map();
  const seed = vertices.find(vertex => canonical(vertex) === $('seed').value.trim()) || vertices[0];
  layers.set(seed.id, 0);
  for (let pass = 0; pass < vertices.length; pass++) {
    let changed = false;
    for (const edge of edges) {
      if (layers.has(edge.source) && !layers.has(edge.target)) {
        layers.set(edge.target, layers.get(edge.source) + 1);
        changed = true;
      } else if (layers.has(edge.target) && !layers.has(edge.source)) {
        layers.set(edge.source, layers.get(edge.target) + 1);
        changed = true;
      }
    }
    if (!changed) break;
  }

  const rows = new Map();
  positions = new Map();
  for (const vertex of vertices) {
    const layer = layers.get(vertex.id) ?? 0;
    const row = rows.get(layer) || 0;
    rows.set(layer, row + 1);
    positions.set(vertex.id, {x: 160 + layer * 320, y: 90 + row * 118});
  }
  const width = Math.max(900, ...[...positions.values()].map(point => point.x + 180));
  const height = Math.max(620, ...[...positions.values()].map(point => point.y + 90));
  viewport = {x: 0, y: 0, width, height};
  svg.setAttribute('viewBox', `${viewport.x} ${viewport.y} ${viewport.width} ${viewport.height}`);

  const edgeDrawings = [];
  const pairCounts = new Map();
  for (const edge of edges) {
    const key = [edge.source, edge.target].sort().join('|');
    const lane = pairCounts.get(key) || 0;
    pairCounts.set(key, lane + 1);
    const group = element('g', {class: 'edge', tabindex: 0, role: 'button'});
    const path = element('path', {stroke: '#53657b', 'marker-end': 'url(#idl-arrow)'});
    const label = element('text', {'text-anchor': 'middle'}, logical(edge).replaceAll('_', ' ').toLowerCase());
    group.append(path, label);
    const inspect = () => inspectRecord({kind: 'relationship', relationship: logical(edge), ...edge});
    group.addEventListener('click', inspect);
    group.addEventListener('keydown', event => { if (event.key === 'Enter') inspect(); });
    svg.append(group);
    edgeDrawings.push({edge, path, label, lane});
  }

  const nodeGroups = new Map();
  for (const vertex of vertices) {
    const domain = props(vertex).graph_domain || 'INTEGRATION';
    const color = colors[domain] || colors.INTEGRATION;
    const group = element('g', {class: 'node', tabindex: 0, role: 'button', 'aria-label': caption(vertex)});
    group.append(element('rect', {x: -128, y: -34, width: 256, height: 78, rx: 8, fill: '#fbfdff', stroke: color, 'stroke-width': 3}));
    group.append(element('rect', {x: -128, y: -34, width: 8, height: 78, rx: 3, fill: color}));
    const name = caption(vertex);
    group.append(element('title', {}, `${name}\n${vertex.label}\n${canonical(vertex)}`));
    group.append(element('text', {x: -110, y: -10}, name.length > 31 ? name.slice(0, 30) + '...' : name));
    group.append(element('text', {x: -110, y: 12}, vertex.label || 'Vertex'));
    group.append(element('text', {x: -110, y: 33}, domain));
    const inspect = () => inspectRecord({kind: 'vertex', display_name: name, ...vertex});
    group.addEventListener('click', inspect);
    group.addEventListener('keydown', event => { if (event.key === 'Enter') inspect(); });
    group.addEventListener('pointerdown', event => {
      group.setPointerCapture(event.pointerId);
      const move = ev => {
        const point = new DOMPoint(ev.clientX, ev.clientY).matrixTransform(svg.getScreenCTM().inverse());
        positions.set(vertex.id, {x: point.x, y: point.y});
        redraw();
      };
      group.addEventListener('pointermove', move);
      group.addEventListener('pointerup', () => group.removeEventListener('pointermove', move), {once: true});
    });
    svg.append(group);
    nodeGroups.set(vertex.id, group);
  }

  function redraw() {
    for (const [id, group] of nodeGroups) {
      const point = positions.get(id);
      group.setAttribute('transform', `translate(${point.x},${point.y})`);
    }
    for (const {edge, path, label, lane} of edgeDrawings) {
      const a = positions.get(edge.source);
      const b = positions.get(edge.target);
      if (!a || !b) continue;
      const angle = Math.atan2(b.y - a.y, b.x - a.x);
      const start = {x: a.x + Math.cos(angle) * 132, y: a.y + Math.sin(angle) * 42};
      const end = {x: b.x - Math.cos(angle) * 138, y: b.y - Math.sin(angle) * 46};
      const bend = 22 + lane * 28;
      const mid = {x: (start.x + end.x) / 2 - Math.sin(angle) * bend,
        y: (start.y + end.y) / 2 + Math.cos(angle) * bend};
      path.setAttribute('d', `M ${start.x} ${start.y} Q ${mid.x} ${mid.y} ${end.x} ${end.y}`);
      label.setAttribute('x', (start.x + 2 * mid.x + end.x) / 4);
      label.setAttribute('y', (start.y + 2 * mid.y + end.y) / 4 - 5);
    }
  }
  redraw();
}

function renderTable() {
  const {vertices, edges} = graphForDisplay();
  const byId = new Map(vertices.map(vertex => [vertex.id, vertex]));
  $('relations').replaceChildren();
  for (const edge of edges) {
    const row = document.createElement('tr');
    const source = byId.get(edge.source);
    const target = byId.get(edge.target);
    const values = [
      source ? caption(source) : edge.source,
      logical(edge),
      target ? caption(target) : edge.target,
      props(edge).creation_status || props(edge).trust_state || 'recorded'
    ];
    for (const value of values) {
      const cell = document.createElement('td');
      cell.textContent = value;
      row.append(cell);
    }
    $('relations').append(row);
  }
}

function renderRdf() {
  const {vertices, edges} = graphForDisplay();
  const byId = new Map(vertices.map(vertex => [vertex.id, vertex]));
  const lines = [
    '@prefix eoip: <urn:eoip:ontology:> .',
    '@prefix data: <urn:eoip:data:> .',
    ''
  ];
  for (const vertex of vertices) {
    const id = String(canonical(vertex) || vertex.id).replace(/[^A-Za-z0-9_-]/g, '_');
    lines.push(`data:${id} a eoip:${vertex.label || 'Vertex'} ;`);
    lines.push(`  eoip:canonical_id ${quote(canonical(vertex) || vertex.id)} .`);
  }
  for (const edge of edges) {
    const source = byId.get(edge.source);
    const target = byId.get(edge.target);
    if (!source || !target) continue;
    const sid = String(canonical(source)).replace(/[^A-Za-z0-9_-]/g, '_');
    const tid = String(canonical(target)).replace(/[^A-Za-z0-9_-]/g, '_');
    lines.push(`data:${sid} eoip:${logical(edge)} data:${tid} .`);
  }
  $('rdf-view').textContent = lines.join('\n');
}

function renderJson() {
  $('json-view').textContent = JSON.stringify({
    lens: activeLens,
    backend: activeBackend(),
    language: activeLanguage(),
    graph: graphForDisplay()
  }, null, 2);
}

function renderView() {
  for (const pane of document.querySelectorAll('[data-view-pane]')) {
    pane.classList.toggle('active', pane.dataset.viewPane === activeView);
  }
  for (const button of document.querySelectorAll('[data-view]')) {
    button.classList.toggle('active', button.dataset.view === activeView);
  }
  $('view-status').textContent = activeView.toUpperCase();
}

function renderAll() {
  renderGraph();
  renderTable();
  renderRdf();
  renderJson();
  renderView();
}

function inspectRecord(record) {
  $('details').textContent = JSON.stringify(record, null, 2);
}

async function copyQuery() {
  try {
    await navigator.clipboard.writeText($('query').value);
    setStatus('Query copied');
  } catch (error) {
    setStatus(`Clipboard failed: ${error.message}`, true);
  }
}

function exportJson() {
  const payload = JSON.stringify({backend: activeBackend(), language: activeLanguage(), graph: graphForDisplay()}, null, 2);
  const url = URL.createObjectURL(new Blob([payload], {type: 'application/json'}));
  const a = document.createElement('a');
  a.href = url;
  a.download = 'graph-idl-result.json';
  a.click();
  URL.revokeObjectURL(url);
}

function bindEvents() {
  $('backend').onchange = renderBackendCard;
  $('language').onchange = generateQuery;
  $('intent').onchange = generateQuery;
  $('seed').oninput = generateQuery;
  $('limit').oninput = generateQuery;
  $('generate').onclick = generateQuery;
  $('execute').onclick = executeHubbleQuery;
  $('copy').onclick = copyQuery;
  $('export').onclick = exportJson;
  $('metadata').onchange = renderAll;
  $('edges-only').onchange = generateQuery;
  for (const button of document.querySelectorAll('[data-view]')) {
    button.onclick = () => {
      activeView = button.dataset.view;
      renderView();
    };
  }
  for (const button of document.querySelectorAll('[data-lens]')) {
    button.onclick = () => {
      activeLens = button.dataset.lens;
      for (const candidate of document.querySelectorAll('[data-lens]')) {
        candidate.classList.toggle('active', candidate === button);
      }
      generateQuery();
      renderJson();
    };
  }
}

async function initConnection() {
  try {
    const connections = await hubbleJson('/api/v1.2/graph-connections?page_size=100');
    const requested = new URLSearchParams(location.search).get('connection');
    const matches = connections.records.filter(item => requested
      ? String(item.id) === requested
      : item.host === 'hugegraph-server' && item.graph === 'hugegraph');
    if (matches.length !== 1) throw new Error('Select exactly one Hubble graph with ?connection=<connection number>.');
    connection = matches[0].id;
    $('connection-status').textContent = `${matches[0].host}/${matches[0].graph}`;
    $('native').href = `/graph-management/${connection}/data-analyze`;
    await executeHubbleQuery();
  } catch (error) {
    $('connection-status').textContent = error.message;
    $('connection-status').className = 'status-error';
    renderAll();
  }
}

setupSelectors();
bindEvents();
renderBackendCard();
renderAll();
await initConnection();
