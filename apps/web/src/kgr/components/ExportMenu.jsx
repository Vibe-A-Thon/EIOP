import React, {useCallback, useState} from 'react';
import {Icon} from '../../icons.jsx';

const FORMATS = [
  {id: 'png', label: 'PNG Image', icon: 'focus', desc: 'Rasterized graph image at 2x resolution'},
  {id: 'svg', label: 'SVG Vector', icon: 'graph', desc: 'Scalable vector graphic'},
  {id: 'pdf', label: 'PDF Report', icon: 'database', desc: 'Graph image + node table + metrics summary'},
  {id: 'json-ld', label: 'JSON-LD', icon: 'database', desc: 'Linked Data with EOIP ontology @context'},
  {id: 'graphml', label: 'GraphML', icon: 'layers', desc: 'Standard graph interchange XML'},
  {id: 'csv', label: 'CSV', icon: 'check', desc: 'Nodes and edges as separate CSV files'},
  {id: 'clipboard', label: 'Clipboard', icon: 'check', desc: 'Copy selected node/edge as Markdown'},
];

function graphToJsonLd(graph) {
  return JSON.stringify({
    '@context': {'@vocab': 'urn:eoip:ontology:', 'nodes': '@graph'},
    nodes: (graph.nodes || []).map(n => ({
      '@id': n.id, '@type': n.label, ...n.properties,
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
  const [exporting, setExporting] = useState(false);

  const doExport = useCallback(async () => {
    setExporting(true);
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
        html += `<h2>Entities</h2><table><tr><th>ID</th><th>Label</th><th>Domain</th></tr>`;
        for (const n of nodes.slice(0, 200)) html += `<tr><td>${n.id}</td><td>${n.label}</td><td>${n.domain || ''}</td></tr>`;
        html += `</table><h2>Relationships</h2><table><tr><th>From</th><th>To</th><th>Type</th></tr>`;
        for (const e of edges.slice(0, 200)) html += `<tr><td>${e.from_id}</td><td>${e.to_id}</td><td>${e.type}</td></tr>`;
        html += `</table></body></html>`;
        const w = window.open('', '_blank');
        if (w) { w.document.write(html); w.document.close(); w.print(); }
      } else if (format === 'json-ld') {
        download(graphToJsonLd(graph), 'kgr-graph.jsonld', 'application/ld+json');
      } else if (format === 'graphml') {
        download(graphToGraphML(graph), 'kgr-graph.graphml', 'application/xml');
      } else if (format === 'csv') {
        const csv = graphToCsv(graph);
        download(csv.nodes, 'kgr-nodes.csv', 'text/csv');
        download(csv.edges, 'kgr-edges.csv', 'text/csv');
      } else if (format === 'clipboard') {
        const text = (graph.nodes || []).slice(0, 10).map(n => `- **${n.label}**: ${n.id}`).join('\n');
        try { await navigator.clipboard.writeText(text); } catch {}
      }
    } finally { setExporting(false); }
    if (onClose) onClose();
  }, [format, scope, graph, cyRef, onClose]);

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
    <button className="primary-button" onClick={doExport} disabled={exporting}>
      <Icon name="database" size={16}/>{exporting ? 'Exporting...' : 'Export'}
    </button>
  </div>;
}
