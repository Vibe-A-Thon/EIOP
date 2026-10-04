import React, {useCallback, useState} from 'react';
import {Icon} from '../../icons.jsx';
import {generateInteractiveHTML} from '../export/InteractiveExport.js';
import {generateGraphReport} from '../export/GraphReport.js';

const FORMATS = [
  {id: 'png', label: 'PNG Image', icon: 'focus', desc: 'Rasterized graph image at 2x resolution'},
  {id: 'svg', label: 'SVG Vector', icon: 'graph', desc: 'Scalable vector graphic'},
  {id: 'pdf', label: 'PDF Report', icon: 'database', desc: 'Graph image + node table + metrics summary'},
  {id: 'json-ld', label: 'JSON-LD', icon: 'database', desc: 'Linked Data with EOIP ontology @context'},
  {id: 'graphml', label: 'GraphML', icon: 'layers', desc: 'Standard graph interchange XML'},
  {id: 'gexf', label: 'GEXF', icon: 'layers', desc: 'Gephi-compatible graph exchange format'},
  {id: 'csv', label: 'CSV', icon: 'check', desc: 'Nodes and edges as separate CSV files'},
  {id: 'obsidian', label: 'Obsidian Vault', icon: 'database', desc: 'Entity-per-note with [[wikilinks]]'},
  {id: 'mermaid', label: 'Mermaid Diagram', icon: 'graph', desc: 'Mermaid graph syntax for Markdown'},
  {id: 'cypher', label: 'Cypher Script', icon: 'database', desc: 'Neo4j-compatible CREATE/MERGE statements'},
  {id: 'clipboard', label: 'Clipboard', icon: 'check', desc: 'Copy selected node/edge as Markdown'},
  {id: 'interactive', label: 'Interactive HTML', icon: 'graph', desc: 'Self-contained HTML with pan/zoom/search/filter'},
  {id: 'report', label: 'Graph Report', icon: 'activity', desc: '7-section Markdown analysis report'},
];

function getAnnotations() {
  const annotations = {};
  try {
    for (let i = 0; i < localStorage.length; i++) {
      const key = localStorage.key(i);
      if (key?.startsWith('kgr-note-')) {
        const id = key.replace('kgr-note-', '');
        annotations[id] = localStorage.getItem(key);
      }
    }
  } catch {}
  return annotations;
}

function graphToJsonLd(graph, annotations) {
  return JSON.stringify({
    '@context': {'@vocab': 'urn:eoip:ontology:', 'nodes': '@graph'},
    nodes: (graph.nodes || []).map(n => ({
      '@id': n.id, '@type': n.label, ...n.properties,
      ...(annotations[n.id] ? {annotation: annotations[n.id]} : {}),
    })),
    edges: (graph.edges || []).map(e => ({
      '@type': e.type, from: e.from_id, to: e.to_id, ...e.properties,
    })),
  }, null, 2);
}

function graphToGraphML(graph) {
  let xml = '<?xml version="1.0" encoding="UTF-8"?>\n<graphml xmlns="http://graphml.graphstudio.org">\n<graph edgedefault="directed">\n';
  for (const n of graph.nodes || []) {
    xml += `  <node id="${n.id}"><data key="label">${n.label}</data></node>\n`;
  }
  for (const e of graph.edges || []) {
    xml += `  <edge source="${e.from_id}" target="${e.to_id}"><data key="type">${e.type}</data></edge>\n`;
  }
  xml += '</graph>\n</graphml>';
  return xml;
}

function graphToGEXF(graph) {
  let xml = '<?xml version="1.0" encoding="UTF-8"?>\n<gexf xmlns="http://gexf.net/1.3" version="1.3">\n<graph defaultedgetype="directed">\n';
  xml += '  <attributes class="node"><attribute id="0" title="label" type="string"/><attribute id="1" title="domain" type="string"/></attributes>\n';
  xml += '  <nodes>\n';
  for (const n of graph.nodes || []) {
    xml += `    <node id="${n.id}" label="${n.properties?.name || n.label || n.id}"><attvalues><attvalue for="0" value="${n.label}"/><attvalue for="1" value="${n.domain || ''}"/></attvalues></node>\n`;
  }
  xml += '  </nodes>\n  <edges>\n';
  (graph.edges || []).forEach((e, i) => {
    xml += `    <edge id="${i}" source="${e.from_id}" target="${e.to_id}" label="${e.type}"/>\n`;
  });
  xml += '  </edges>\n</graph>\n</gexf>';
  return xml;
}

function graphToObsidian(graph) {
  const files = [];
  for (const n of graph.nodes || []) {
    const props = n.properties || {};
    let md = '---\n';
    md += `canonical_id: "${n.id}"\n`;
    md += `type: "${n.label}"\n`;
    if (n.domain) md += `domain: "${n.domain}"\n`;
    for (const [k, v] of Object.entries(props)) {
      if (typeof v === 'string') md += `${k}: "${v}"\n`;
      else md += `${k}: ${JSON.stringify(v)}\n`;
    }
    md += '---\n\n';
    md += `# ${props.name || props.display_name || n.label || n.id}\n\n`;
    const outgoing = (graph.edges || []).filter(e => e.from_id === n.id);
    const incoming = (graph.edges || []).filter(e => e.to_id === n.id);
    if (outgoing.length) {
      md += '## Outgoing\n';
      for (const e of outgoing) md += `- ${e.type} → [[${e.to_id}]]\n`;
      md += '\n';
    }
    if (incoming.length) {
      md += '## Incoming\n';
      for (const e of incoming) md += `- ${e.type} ← [[${e.from_id}]]\n`;
    }
    const folder = (n.domain || 'OTHER') + '/' + (n.label || 'Entity');
    files.push({path: `${folder}/${(props.name || n.id).replace(/[/\\:*?"<>|]/g, '_')}.md`, content: md});
  }
  return files;
}

function graphToMermaid(graph) {
  let md = '```mermaid\ngraph TD\n';
  const domains = {};
  for (const n of graph.nodes || []) {
    const d = n.domain || 'OTHER';
    if (!domains[d]) domains[d] = [];
    domains[d].push(n);
  }
  for (const [d, nodes] of Object.entries(domains)) {
    md += `  subgraph ${d}\n`;
    for (const n of nodes) {
      const name = (n.properties?.name || n.label || n.id).replace(/"/g, "'");
      md += `    ${n.id.replace(/[^a-zA-Z0-9_]/g, '_')}["${name}"]\n`;
    }
    md += '  end\n';
  }
  for (const e of (graph.edges || []).slice(0, 200)) {
    const src = e.from_id.replace(/[^a-zA-Z0-9_]/g, '_');
    const tgt = e.to_id.replace(/[^a-zA-Z0-9_]/g, '_');
    md += `  ${src} -->|${e.type}| ${tgt}\n`;
  }
  md += '```\n';
  return md;
}

function graphToCypher(graph) {
  let cypher = '// Generated by KGR — EOIP Knowledge Graph Renderer\n\n';
  for (const n of graph.nodes || []) {
    const props = {...(n.properties || {}), canonical_id: n.id};
    const propsStr = Object.entries(props).map(([k, v]) => `${k}: ${JSON.stringify(v)}`).join(', ');
    cypher += `MERGE (n:${n.label} {canonical_id: "${n.id}"}) SET n += {${propsStr}};\n`;
  }
  cypher += '\n';
  for (const e of graph.edges || []) {
    cypher += `MATCH (a {canonical_id: "${e.from_id}"}), (b {canonical_id: "${e.to_id}"}) MERGE (a)-[:${e.type}]->(b);\n`;
  }
  return cypher;
}

function graphToCsv(graph) {
  let nodes = 'id,label,domain\n';
  for (const n of graph.nodes || []) nodes += `"${n.id}","${n.label}","${n.domain || ''}"\n`;
  let edges = 'from_id,to_id,type\n';
  for (const e of graph.edges || []) edges += `"${e.from_id}","${e.to_id}","${e.type}"\n`;
  return {nodes, edges};
}

function download(content, filename, type = 'text/plain') {
  const blob = new Blob([content], {type});
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url; a.download = filename; a.click();
  URL.revokeObjectURL(url);
}

export default function ExportMenu({graph, cyRef, onClose}) {
  const [format, setFormat] = useState('json-ld');
  const [scope, setScope] = useState('visible');
  const [includeAnnotations, setIncludeAnnotations] = useState(true);
  const [exporting, setExporting] = useState(false);

  const doExport = useCallback(async () => {
    setExporting(true);
    const annotations = includeAnnotations ? getAnnotations() : {};
    try {
      if (format === 'png' && cyRef?.current) {
        const blob = await cyRef.current.png({output: 'blob', scale: 2, full: true});
        download(blob, 'kgr-graph.png', 'image/png');
      } else if (format === 'svg' && cyRef?.current) {
        download(cyRef.current.svg({full: true}), 'kgr-graph.svg', 'image/svg+xml');
      } else if (format === 'pdf') {
        const nodes = graph.nodes || [];
        const edges = graph.edges || [];
        let html = `<html><head><title>KGR Graph Report</title><style>body{font-family:sans-serif;padding:20px}table{border-collapse:collapse;width:100%;margin:12px 0}th,td{border:1px solid #ddd;padding:6px 10px;text-align:left}th{background:#f0f0f0}h1,h2{margin:8px 0}</style></head><body>`;
        html += `<h1>KGR Graph Report</h1><p>${nodes.length} entities, ${edges.length} relationships</p>`;
        html += `<h2>Entities</h2><table><tr><th>ID</th><th>Label</th><th>Domain</th>${includeAnnotations ? '<th>Annotation</th>' : ''}</tr>`;
        for (const n of nodes.slice(0, 200)) html += `<tr><td>${n.id}</td><td>${n.label}</td><td>${n.domain || ''}</td>${includeAnnotations ? `<td>${annotations[n.id] || ''}</td>` : ''}</tr>`;
        html += `</table><h2>Relationships</h2><table><tr><th>From</th><th>To</th><th>Type</th></tr>`;
        for (const e of edges.slice(0, 200)) html += `<tr><td>${e.from_id}</td><td>${e.to_id}</td><td>${e.type}</td></tr>`;
        html += `</table></body></html>`;
        const w = window.open('', '_blank');
        if (w) { w.document.write(html); w.document.close(); w.print(); }
      } else if (format === 'json-ld') {
        download(graphToJsonLd(graph, annotations), 'kgr-graph.jsonld', 'application/ld+json');
      } else if (format === 'graphml') {
        download(graphToGraphML(graph), 'kgr-graph.graphml', 'application/xml');
      } else if (format === 'gexf') {
        download(graphToGEXF(graph), 'kgr-graph.gexf', 'application/xml');
      } else if (format === 'csv') {
        const csv = graphToCsv(graph);
        download(csv.nodes, 'kgr-nodes.csv', 'text/csv');
        download(csv.edges, 'kgr-edges.csv', 'text/csv');
      } else if (format === 'obsidian') {
        const files = graphToObsidian(graph);
        const content = files.map(f => `=== ${f.path} ===\n${f.content}`).join('\n\n');
        download(content, 'kgr-obsidian-vault.md', 'text/markdown');
      } else if (format === 'mermaid') {
        download(graphToMermaid(graph), 'kgr-mermaid.md', 'text/markdown');
      } else if (format === 'cypher') {
        download(graphToCypher(graph), 'kgr-graph.cypher', 'text/plain');
      } else if (format === 'clipboard') {
        const text = (graph.nodes || []).slice(0, 10).map(n => `- **${n.label}**: ${n.id}`).join('\n');
        try { await navigator.clipboard.writeText(text); } catch {}
      } else if (format === 'interactive') {
        const html = generateInteractiveHTML(graph.nodes || [], graph.edges || [], {title: 'KGR Interactive Export', annotations});
        download(html, 'kgr-interactive.html', 'text/html');
      } else if (format === 'report') {
        const md = generateGraphReport(graph.nodes || [], graph.edges || [], {title: 'KGR Graph Report', annotations});
        download(md, 'kgr-graph-report.md', 'text/markdown');
      }
    } finally { setExporting(false); }
    if (onClose) onClose();
  }, [format, scope, graph, cyRef, onClose, includeAnnotations]);

  return <div className="kgr-export-menu panel">
    <div className="panel-heading"><div><span className="eyebrow">EXPORT</span><h2>Export graph data</h2></div>
      {onClose && <button className="icon-button" onClick={onClose}><Icon name="close"/></button>}
    </div>
    <div className="export-formats">{FORMATS.map(f =>
      <label key={f.id} className={`export-format-option ${format === f.id ? 'selected' : ''}`}>
        <input type="radio" name="format" value={f.id} checked={format === f.id} onChange={() => setFormat(f.id)}/>
        <Icon name={f.icon} size={16}/><div><strong>{f.label}</strong><small>{f.desc}</small></div>
      </label>
    )}</div>
    <div className="export-scope">
      <label><input type="radio" name="scope" value="visible" checked={scope === 'visible'} onChange={() => setScope('visible')}/> Visible graph</label>
      <label><input type="radio" name="scope" value="full" checked={scope === 'full'} onChange={() => setScope('full')}/> Full graph</label>
    </div>
    <div className="export-options">
      <label><input type="checkbox" checked={includeAnnotations} onChange={e => setIncludeAnnotations(e.target.checked)}/> Include annotations</label>
    </div>
    <button className="primary-button" onClick={doExport} disabled={exporting}>
      <Icon name="database" size={16}/>{exporting ? 'Exporting...' : 'Export'}
    </button>
  </div>;
}
