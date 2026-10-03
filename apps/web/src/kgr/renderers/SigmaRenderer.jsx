import React, {useCallback, useEffect, useRef, useState} from 'react';
import Graph from 'graphology';
import Sigma from 'sigma';
import {palette} from '../../GraphCanvas.jsx';

function buildGraph(Graph, nodes, edges) {
  const g = new Graph();
  for (const n of nodes) {
    const color = palette[n.label] || '#64748b';
    const size = Math.max(3, Math.min(20, (n.degree || 1) * 1.5));
    g.addNode(n.id, {
      label: n.properties?.display_name || n.properties?.name || n.properties?.issue_key || n.label || n.id,
      x: Math.random() * 1000,
      y: Math.random() * 1000,
      size,
      color,
      nodeLabel: n.label,
      domain: n.domain,
    });
  }
  for (const e of edges) {
    const key = `${e.from_id}-${e.type}-${e.to_id}`;
    if (!g.hasNode(e.from_id) || !g.hasNode(e.to_id)) continue;
    try {
      g.addEdgeWithKey(key, e.from_id, e.to_id, {
        label: e.type,
        color: '#94a3b844',
        size: 1,
        type: 'arrow',
      });
    } catch (_) {}
  }
  return g;
}

function applyForceLayout(graph, iterations = 100) {
  const nodes = {};
  graph.forEachNode((id, attrs) => {
    nodes[id] = {x: attrs.x, y: attrs.y, vx: 0, vy: 0};
  });
  const ids = Object.keys(nodes);
  const k = Math.sqrt((1000 * 1000) / Math.max(ids.length, 1));
  for (let iter = 0; iter < iterations; iter++) {
    const temp = 100 * (1 - iter / iterations);
    for (let i = 0; i < ids.length; i++) {
      const a = nodes[ids[i]];
      for (let j = i + 1; j < ids.length; j++) {
        const b = nodes[ids[j]];
        const dx = a.x - b.x, dy = a.y - b.y;
        const dist = Math.max(Math.sqrt(dx * dx + dy * dy), 0.01);
        const repulse = (k * k) / dist;
        const fx = (dx / dist) * repulse, fy = (dy / dist) * repulse;
        a.vx += fx; a.vy += fy;
        b.vx -= fx; b.vy -= fy;
      }
    }
    graph.forEachEdge((_, attrs, src, tgt) => {
      const a = nodes[src], b = nodes[tgt];
      if (!a || !b) return;
      const dx = b.x - a.x, dy = b.y - a.y;
      const dist = Math.max(Math.sqrt(dx * dx + dy * dy), 0.01);
      const attract = (dist * dist) / k;
      const fx = (dx / dist) * attract, fy = (dy / dist) * attract;
      a.vx += fx * 0.1; a.vy += fy * 0.1;
      b.vx -= fx * 0.1; b.vy -= fy * 0.1;
    });
    for (const id of ids) {
      const n = nodes[id];
      const speed = Math.sqrt(n.vx * n.vx + n.vy * n.vy);
      if (speed > temp) {
        n.vx = (n.vx / speed) * temp;
        n.vy = (n.vy / speed) * temp;
      }
      n.x += n.vx; n.y += n.vy;
      n.vx *= 0.9; n.vy *= 0.9;
    }
  }
  for (const id of ids) {
    graph.setNodeAttribute(id, 'x', nodes[id].x);
    graph.setNodeAttribute(id, 'y', nodes[id].y);
  }
}

export default function SigmaRenderer({nodes, edges, selectedId, onSelectNode, onSelectEdge, onExpand, style}) {
  const containerRef = useRef(null);
  const sigmaRef = useRef(null);
  const graphRef = useRef(null);
  const [progress, setProgress] = useState(null);

  useEffect(() => {
    if (!containerRef.current) return;

    if (sigmaRef.current) {
      sigmaRef.current.kill();
      sigmaRef.current = null;
    }

    if (!nodes.length) return;

    setProgress(`Building graph: ${nodes.length} nodes...`);
    const g = buildGraph(Graph, nodes, edges);
    graphRef.current = g;

    setProgress(`Computing layout for ${nodes.length} nodes...`);
    const iterations = nodes.length > 10000 ? 30 : nodes.length > 5000 ? 50 : 80;
    applyForceLayout(g, iterations);

    setProgress(null);
    try {
      const renderer = new Sigma(g, containerRef.current, {
        renderEdgeLabels: nodes.length < 2000,
        labelRenderedSizeThreshold: nodes.length > 5000 ? 15 : 8,
        labelDensity: 0.07,
        labelGridCellSize: 60,
        minCameraRatio: 0.02,
        maxCameraRatio: 20,
        defaultEdgeType: 'arrow',
        enableEdgeClickEvents: true,
        enableEdgeHoverEvents: true,
      });

      renderer.on('clickNode', ({node}) => {
        const n = nodes.find(nd => nd.id === node);
        if (n && onSelectNode) onSelectNode(n);
      });

      renderer.on('doubleClickNode', ({node}) => {
        const n = nodes.find(nd => nd.id === node);
        if (n && onExpand) onExpand(n);
      });

      renderer.on('clickEdge', ({edge}) => {
        const e = edges.find(ed => `${ed.from_id}-${ed.type}-${ed.to_id}` === edge);
        if (e && onSelectEdge) onSelectEdge(e);
      });

      sigmaRef.current = renderer;
    } catch (err) {
      setProgress(`Renderer error: ${err.message}`);
    }

    return () => {
      if (sigmaRef.current) {
        sigmaRef.current.kill();
        sigmaRef.current = null;
      }
    };
  }, [nodes, edges]);

  useEffect(() => {
    if (!graphRef.current || !sigmaRef.current) return;
    graphRef.current.forEachNode((id, attrs) => {
      const isSelected = id === selectedId;
      graphRef.current.setNodeAttribute(id, 'highlighted', isSelected);
      if (isSelected) {
        graphRef.current.setNodeAttribute(id, 'color', '#f59e0b');
      } else {
        const n = nodes.find(nd => nd.id === id);
        graphRef.current.setNodeAttribute(id, 'color', palette[n?.label] || '#64748b');
      }
    });
    sigmaRef.current.refresh();
  }, [selectedId, nodes]);

  return <div className="sigma-container" style={{position: 'relative', width: '100%', height: '100%', ...style}}>
    <div ref={containerRef} style={{width: '100%', height: '100%', minHeight: 400}}/>
    {progress && <div className="sigma-progress" style={{
      position: 'absolute', top: 8, left: 8, padding: '6px 12px',
      background: 'var(--bg-surface, #1e293b)', borderRadius: 6, fontSize: 12,
      color: 'var(--text-secondary, #94a3b8)', zIndex: 10,
    }}>{progress}</div>}
    <div className="sigma-badge" style={{
      position: 'absolute', bottom: 8, right: 8, padding: '4px 10px',
      background: 'var(--bg-surface, #1e293b)', borderRadius: 4, fontSize: 11,
      color: 'var(--text-muted, #64748b)', zIndex: 10,
    }}>WebGL · {nodes.length} nodes · {edges.length} edges</div>
  </div>;
}

export {applyForceLayout, buildGraph};
