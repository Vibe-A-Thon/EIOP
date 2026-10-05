const $ = id => document.getElementById(id);
const ns = 'http://www.w3.org/2000/svg';
const colors = {
  BUSINESS: '#bd7c12', WORK: '#3478cb', CODE: '#28977d', CICD: '#8b62c5',
  TEST: '#617d26', DESIGN: '#bd5394', OPS: '#c56336', KNOWLEDGE: '#299bb3',
  IDENTITY: '#62748b', DECISION: '#a75c33', PROCESS: '#5665c0', META: '#7b828d',
  AGENT: '#9c4794', INTEGRATION: '#3e8595'
};
const metaLabels = new Set(['Evidence', 'IngestionRun', 'GraphDomain', 'ValidationRun']);
let pack, connection, returned, query, positions, viewport, activeScenario;
let loading = false;
let touring = false;
const caption = vertex => {
  const p = vertex.properties;
  for (const key of ['display_name', 'name', 'summary', 'api_name', 'mr_title', 'message',
    'qualified_name', 'branch_name', 'tag_name', 'incident_number', 'path', 'run_kind', 'evidence_key']) {
    if (p[key]) return String(p[key]);
  }
  return `${vertex.label}: ${(p.canonical_id || vertex.id).split(':').pop()}`;
};
const logical = edge => edge.label.split('__')[0];
const quote = value => JSON.stringify(value);
function element(tag, attributes = {}, text) {
  const node = document.createElementNS(ns, tag);
  for (const [name, value] of Object.entries(attributes)) node.setAttribute(name, value);
  if (text !== undefined) node.textContent = text;
  return node;
}
async function json(url, options = {}) {
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
function showDetails(record) {
  $('details').textContent = JSON.stringify(record, null, 2);
}
function render() {
  const svg = $('graph');
  svg.replaceChildren();
  const nodes = returned.vertices.filter(v => $('metadata').checked || !metaLabels.has(v.label));
  const byId = new Map(nodes.map(v => [v.id, v]));
  const edges = returned.edges.filter(e => byId.has(e.source) && byId.has(e.target));
  const domains = [...new Set(nodes.map(v => v.properties.graph_domain || 'INTEGRATION'))].sort();
  $('legend').replaceChildren();
  for (const domain of domains) {
    const badge = document.createElement('span');
    badge.className = 'badge'; badge.style.borderColor = colors[domain] || colors.META;
    badge.textContent = domain; $('legend').append(badge);
  }
  const layers = new Map();
  const seed = nodes.find(v => v.properties.canonical_id === activeScenario?.entrypoint) || nodes[0];
  if (seed) layers.set(seed.id, 0);
  for (let pass = 0; pass < nodes.length; pass++) {
    let changed = false;
    for (const e of edges) {
      if (layers.has(e.source) && !layers.has(e.target)) {
        layers.set(e.target, layers.get(e.source) + 1); changed = true;
      } else if (layers.has(e.target) && !layers.has(e.source)) {
        layers.set(e.source, layers.get(e.target) + 1); changed = true;
      }
    }
    if (!changed) break;
  }
  const rows = new Map(); positions = new Map();
  for (const v of nodes) {
    const layer = layers.get(v.id) ?? 0;
    const row = rows.get(layer) || 0; rows.set(layer, row + 1);
    positions.set(v.id, {x: 160 + layer * 340, y: 90 + row * 125});
  }
  const width = Math.max(700, ...[...positions.values()].map(p => p.x + 180));
  const height = Math.max(400, ...[...positions.values()].map(p => p.y + 90));
  viewport = {x: 0, y: 0, width, height};
  const defs = element('defs');
  const marker = element('marker', {id: 'arrow', viewBox: '0 0 10 10', refX: 9, refY: 5,
    markerWidth: 7, markerHeight: 7, orient: 'auto-start-reverse'});
  marker.append(element('path', {d: 'M 0 0 L 10 5 L 0 10 z', fill: '#425570'}));
  defs.append(marker); svg.append(defs);
  const drawings = [];
  const pairCounts = new Map();
  for (const e of edges) {
    const key = [e.source, e.target].sort().join('|');
    const lane = pairCounts.get(key) || 0; pairCounts.set(key, lane + 1);
    const group = element('g', {class: 'edge', tabindex: 0, role: 'button',
      'aria-label': `${caption(byId.get(e.source))} ${logical(e)} ${caption(byId.get(e.target))}`});
    const path = element('path', {stroke: '#425570', 'marker-end': 'url(#arrow)'});
    const label = element('text', {'text-anchor': 'middle'}, logical(e).replaceAll('_', ' ').toLowerCase());
    group.append(path, label);
    const inspect = () => showDetails({relationship: logical(e), source: caption(byId.get(e.source)),
      target: caption(byId.get(e.target)), ...e});
    group.addEventListener('click', inspect);
    group.addEventListener('keydown', event => { if (event.key === 'Enter') inspect(); });
    svg.append(group); drawings.push({e, path, label, lane});
  }
  const nodeGroups = new Map();
  for (const v of nodes) {
    const group = element('g', {class: 'node', tabindex: 0, role: 'button', 'aria-label': caption(v)});
    const color = colors[v.properties.graph_domain] || colors.INTEGRATION;
    group.append(element('rect', {x: -135, y: -35, width: 270, height: 82, rx: 10,
      fill: '#f8fbff', stroke: color, 'stroke-width': 3}));
    group.append(element('rect', {x: -135, y: -35, width: 8, height: 82, rx: 3, fill: color}));
    const name = caption(v);
    group.append(element('title', {}, `${name}\n${v.label}\n${v.properties.canonical_id}`));
    group.append(element('text', {x: -116, y: -10}, name.length > 33 ? name.slice(0, 32) + '...' : name));
    group.append(element('text', {x: -116, y: 12}, name.length > 33 ? name.slice(32, 65) : v.label));
    group.append(element('text', {x: -116, y: 34}, `${v.properties.graph_domain || 'INTEGRATION'} / ${v.label}`));
    group.addEventListener('click', () => showDetails({display_name: name, ...v}));
    group.addEventListener('keydown', event => { if (event.key === 'Enter') showDetails(v); });
    group.addEventListener('pointerdown', event => {
      group.setPointerCapture(event.pointerId);
      const move = ev => {
        const point = new DOMPoint(ev.clientX, ev.clientY).matrixTransform(svg.getScreenCTM().inverse());
        positions.set(v.id, {x: point.x, y: point.y}); redraw();
      };
      group.addEventListener('pointermove', move);
      group.addEventListener('pointerup', () => group.removeEventListener('pointermove', move), {once: true});
    });
    svg.append(group); nodeGroups.set(v.id, group);
  }
  function redraw() {
    svg.setAttribute('viewBox', `${viewport.x} ${viewport.y} ${viewport.width} ${viewport.height}`);
    for (const [id, group] of nodeGroups) {
      const p = positions.get(id); group.setAttribute('transform', `translate(${p.x},${p.y})`);
    }
    for (const {e, path, label, lane} of drawings) {
      const a = positions.get(e.source), b = positions.get(e.target);
      const angle = Math.atan2(b.y - a.y, b.x - a.x);
      const start = {x: a.x + Math.cos(angle) * 140, y: a.y + Math.sin(angle) * 45};
      const end = {x: b.x - Math.cos(angle) * 145, y: b.y - Math.sin(angle) * 50};
      const bend = 22 + lane * 30;
      const mid = {x: (start.x + end.x) / 2 - Math.sin(angle) * bend,
        y: (start.y + end.y) / 2 + Math.cos(angle) * bend};
      path.setAttribute('d', `M ${start.x} ${start.y} Q ${mid.x} ${mid.y} ${end.x} ${end.y}`);
      label.setAttribute('x', (start.x + 2 * mid.x + end.x) / 4);
      label.setAttribute('y', (start.y + 2 * mid.y + end.y) / 4 - 5);
    }
  }
  redraw();
  $('zoom-in').onclick = () => { viewport.width *= .8; viewport.height *= .8; redraw(); };
  $('zoom-out').onclick = () => { viewport.width /= .8; viewport.height /= .8; redraw(); };
  $('fit').onclick = () => { viewport = {x: 0, y: 0, width, height}; redraw(); };
  $('relations').replaceChildren();
  for (const e of edges) {
    const row = document.createElement('tr');
    for (const text of [caption(byId.get(e.source)), logical(e), caption(byId.get(e.target))]) {
      const cell = document.createElement('td'); cell.textContent = text; row.append(cell);
    }
    $('relations').append(row);
  }
  $('status').textContent = `${nodes.length} named vertices / ${edges.length} directed relationships displayed. ` +
    `${returned.vertices.length - nodes.length} provenance nodes hidden. Query limit: 120 relationships.`;
}
async function explore(cids, scenario) {
  if (loading) return;
  loading = true; $('explore').disabled = true; $('scenario').disabled = true;
  $('status').className = ''; $('status').textContent = 'Reading the real Hubble graph...';
  $('graph').replaceChildren(); $('relations').replaceChildren(); $('legend').replaceChildren();
  $('details').textContent = 'Select a node or relationship.';
  try {
    activeScenario = scenario;
    $('story').textContent = scenario?.story || 'One-hop relationships around the selected named entity.';
    const ids = await Promise.all(cids.map(physicalId));
    const start = `g.V(${ids.map(quote).join(',')})`;
    query = `${start}.bothE().dedup().limit(120)`;
    $('query').textContent = `Nodes: ${start}\nRelationships: ${query}`;
    const execute = content => json(`/api/v1.2/graph-connections/${connection}/gremlin-query`,
      {method: 'POST', headers: {'Content-Type': 'application/json'}, body: JSON.stringify({content})});
    const [vertices, relationships] = await Promise.all([execute(start), execute(query)]);
    const found = vertices.graph_view.vertices || [];
    if (found.length !== ids.length) throw new Error('Scenario data is incomplete. Run the additive demo-data loader.');
    const unique = new Map([...found, ...(relationships.graph_view.vertices || [])].map(v => [v.id, v]));
    returned = {vertices: [...unique.values()], edges: relationships.graph_view.edges || []};
    render();
  } catch (error) {
    returned = null; $('status').className = 'error'; $('status').textContent = error.message;
  } finally {
    loading = false; $('explore').disabled = false; $('scenario').disabled = false;
  }
}
function entities() {
  const search = $('search').value.toLowerCase();
  $('entity').replaceChildren();
  for (const v of pack.vertices.filter(v => caption(v).toLowerCase().includes(search))) {
    $('entity').add(new Option(`${caption(v)} (${v.label})`, v.properties.canonical_id));
  }
}
$('metadata').onchange = () => { if (returned) render(); };
$('search').oninput = () => { if (pack) entities(); };
$('explore').onclick = () => { if ($('entity').value) explore([$('entity').value]); };
$('scenario').onchange = () => {
  const scenario = pack.scenarios.find(s => s.id === $('scenario').value);
  explore([...new Set(scenario.expected_path)], scenario);
};
$('copy').onclick = async () => {
  try { if (query) { await navigator.clipboard.writeText(query); $('status').textContent = 'Relationship query copied. Paste into native Hubble and execute.'; } }
  catch (error) { $('status').textContent = `Clipboard failed: ${error.message}. Select and copy the query text manually.`; }
};
$('export').onclick = () => {
  if (!returned) return;
  const url = URL.createObjectURL(new Blob([JSON.stringify(returned, null, 2)], {type: 'application/json'}));
  const a = document.createElement('a'); a.href = url; a.download = 'eoip-hubble-graph.json'; a.click();
  URL.revokeObjectURL(url);
};
async function tour() {
  if (loading || touring) return;
  touring = true; $('tour').disabled = true; $('stop-tour').disabled = false;
  for (const scenario of pack.scenarios) {
    if (!touring) break;
    $('scenario').value = scenario.id;
    await explore([...new Set(scenario.expected_path)], scenario);
    if (!returned) break;
    await new Promise(resolve => setTimeout(resolve, 15000));
  }
  touring = false; $('tour').disabled = false; $('stop-tour').disabled = true;
}
$('tour').onclick = tour;
$('stop-tour').onclick = () => { touring = false; $('stop-tour').disabled = true; };
try {
  pack = await json('/enterprise-scenarios.json');
  const connections = await json('/api/v1.2/graph-connections?page_size=100');
  const requested = new URLSearchParams(location.search).get('connection');
  const matches = connections.records.filter(c => requested ? String(c.id) === requested :
    c.host === 'hugegraph-server' && c.graph === 'hugegraph');
  if (matches.length !== 1) throw new Error('Select exactly one local graph with ?connection=<connection number>.');
  connection = matches[0].id;
  $('native').href = `/graph-management/${connection}/data-analyze`;
  for (const s of pack.scenarios) $('scenario').add(new Option(s.title, s.id));
  entities();
  const scenario = pack.scenarios[0];
  await explore([...new Set(scenario.expected_path)], scenario);
  if (returned && new URLSearchParams(location.search).get('tour') === '1') tour();
} catch (error) {
  $('status').className = 'error'; $('status').textContent = error.message;
}
