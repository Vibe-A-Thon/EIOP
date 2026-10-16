interface GraphNode {
  id: string;
  label?: string;
  domain?: string;
  properties?: Record<string, unknown>;
}
interface GraphEdge {
  id?: string;
  from_id: string;
  to_id: string;
  type: string;
  properties?: Record<string, unknown>;
}
export interface ExportGraph {nodes?: GraphNode[]; edges?: GraphEdge[];}

function append(doc: XMLDocument, parent: Element, name: string, attributes: Record<string, unknown> = {}, text?: string) {
  const element = doc.createElementNS(parent.namespaceURI, name);
  for (const [key, value] of Object.entries(attributes)) element.setAttribute(key, String(value ?? ''));
  if (text !== undefined) element.textContent = text;
  parent.append(element);
  return element;
}

export function graphToGraphML(graph: ExportGraph): string {
  const doc = document.implementation.createDocument('http://graphml.graphdrawing.org/xmlns', 'graphml');
  const root = doc.documentElement;
  for (const [id, target, name] of [['n-label', 'node', 'label'], ['n-domain', 'node', 'domain'],
    ['n-properties', 'node', 'properties'], ['e-type', 'edge', 'type'], ['e-properties', 'edge', 'properties']]) {
    append(doc, root, 'key', {id, for: target, 'attr.name': name, 'attr.type': 'string'});
  }
  const body = append(doc, root, 'graph', {id: 'loaded-graph', edgedefault: 'directed'});
  for (const node of graph.nodes || []) {
    const entry = append(doc, body, 'node', {id: node.id});
    append(doc, entry, 'data', {key: 'n-label'}, node.label || '');
    append(doc, entry, 'data', {key: 'n-domain'}, node.domain || '');
    append(doc, entry, 'data', {key: 'n-properties'}, JSON.stringify(node.properties || {}));
  }
  for (const [index, edge] of (graph.edges || []).entries()) {
    const entry = append(doc, body, 'edge', {id: edge.id ?? `edge-${index}`, source: edge.from_id, target: edge.to_id});
    append(doc, entry, 'data', {key: 'e-type'}, edge.type);
    append(doc, entry, 'data', {key: 'e-properties'}, JSON.stringify(edge.properties || {}));
  }
  return '<?xml version="1.0" encoding="UTF-8"?>\n' + new XMLSerializer().serializeToString(doc);
}

export function graphToGEXF(graph: ExportGraph): string {
  const doc = document.implementation.createDocument('http://gexf.net/1.3', 'gexf');
  const root = doc.documentElement;
  root.setAttribute('version', '1.3');
  const body = append(doc, root, 'graph', {defaultedgetype: 'directed', mode: 'static'});
  for (const target of ['node', 'edge']) {
    const attributes = append(doc, body, 'attributes', {class: target});
    for (const name of target === 'node' ? ['label', 'domain', 'properties'] : ['type', 'properties']) {
      append(doc, attributes, 'attribute', {id: name, title: name, type: 'string'});
    }
  }
  const nodes = append(doc, body, 'nodes');
  for (const node of graph.nodes || []) {
    const entry = append(doc, nodes, 'node', {id: node.id, label: node.properties?.name || node.label || node.id});
    const values = append(doc, entry, 'attvalues');
    for (const [key, value] of Object.entries({label: node.label || '', domain: node.domain || '', properties: JSON.stringify(node.properties || {})})) {
      append(doc, values, 'attvalue', {for: key, value});
    }
  }
  const edges = append(doc, body, 'edges');
  for (const [index, edge] of (graph.edges || []).entries()) {
    const entry = append(doc, edges, 'edge', {id: edge.id ?? `edge-${index}`, source: edge.from_id, target: edge.to_id, label: edge.type});
    const values = append(doc, entry, 'attvalues');
    append(doc, values, 'attvalue', {for: 'type', value: edge.type});
    append(doc, values, 'attvalue', {for: 'properties', value: JSON.stringify(edge.properties || {})});
  }
  return '<?xml version="1.0" encoding="UTF-8"?>\n' + new XMLSerializer().serializeToString(doc);
}

export function graphToCsv(graph: ExportGraph): {nodes: string; edges: string} {
  const cell = (value: unknown) => '"' + String(value ?? '').replaceAll('"', '""') + '"';
  const row = (values: unknown[]) => values.map(cell).join(',') + '\r\n';
  return {
    nodes: row(['id', 'label', 'domain', 'properties']) + (graph.nodes || []).map(node => row([node.id, node.label, node.domain, JSON.stringify(node.properties || {})])).join(''),
    edges: row(['id', 'from_id', 'to_id', 'type', 'properties']) + (graph.edges || []).map((edge, index) => row([edge.id ?? `edge-${index}`, edge.from_id, edge.to_id, edge.type, JSON.stringify(edge.properties || {})])).join(''),
  };
}

export function graphPrintDocument(graph: ExportGraph): string {
  const doc = document.implementation.createHTMLDocument('EOIP graph');
  const heading = doc.createElement('h1');
  heading.textContent = 'EOIP graph'; doc.body.append(heading);
  const summary = doc.createElement('p');
  summary.textContent = `${graph.nodes?.length || 0} entities, ${graph.edges?.length || 0} relationships`; doc.body.append(summary);
  function table(title: string, headers: string[], records: unknown[][]) {
    const label = doc.createElement('h2'); label.textContent = title; doc.body.append(label);
    const element = doc.createElement('table');
    const head = element.createTHead().insertRow();
    for (const name of headers) {const cell = doc.createElement('th'); cell.textContent = name; head.append(cell);}
    const body = element.createTBody();
    for (const record of records) {
      const row = body.insertRow();
      for (const value of record) row.insertCell().textContent = String(value ?? '');
    }
    doc.body.append(element);
  }
  table('Entities', ['ID', 'Type', 'Domain'], (graph.nodes || []).map(node => [node.id, node.label, node.domain]));
  table('Relationships', ['ID', 'From', 'To', 'Type'], (graph.edges || []).map((edge, index) => [edge.id ?? index, edge.from_id, edge.to_id, edge.type]));
  return '<!doctype html>\n' + doc.documentElement.outerHTML;
}
