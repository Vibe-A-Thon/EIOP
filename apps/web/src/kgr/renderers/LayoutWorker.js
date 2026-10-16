/**
 * Web Worker for non-blocking graph layout computation.
 * Supports ForceAtlas2, dagre (hierarchical), and cola (constraint-based).
 *
 * Message protocol:
 *   Inbound:  {type: 'start', nodes, edges, algorithm, options}
 *             {type: 'cancel'}
 *   Outbound: {type: 'progress', iteration, total}
 *             {type: 'positions', positions: {nodeId: {x, y}}}
 *             {type: 'error', message}
 */

let cancelled = false;

self.onmessage = function (event) {
  const {type, nodes, edges, algorithm, options} = event.data;

  if (type === 'cancel') {
    cancelled = true;
    return;
  }

  if (type !== 'start') return;
  cancelled = false;

  try {
    const positions = {};
    const opts = options || {};

    switch (algorithm) {
      case 'forceAtlas2':
        runForceAtlas2(nodes, edges, positions, opts);
        break;
      case 'dagre':
        runDagre(nodes, edges, positions, opts);
        break;
      case 'cola':
        runCola(nodes, edges, positions, opts);
        break;
      case 'orthogonal':
        runOrthogonal(nodes, edges, positions, opts);
        break;
      default:
        runForceAtlas2(nodes, edges, positions, opts);
    }

    if (!cancelled) {
      self.postMessage({type: 'positions', positions});
    }
  } catch (err) {
    self.postMessage({type: 'error', message: err.message || String(err)});
  }
};

function runForceAtlas2(nodes, edges, positions, opts) {
  const iterations = opts.iterations || 100;
  const gravity = opts.gravity || 1;
  const scalingRatio = opts.scalingRatio || 2;

  const state = {};
  for (const n of nodes) {
    state[n.id] = {x: Math.random() * 1000, y: Math.random() * 1000, vx: 0, vy: 0, mass: 1 + (n.degree || 0)};
  }

  const adj = {};
  for (const e of edges) {
    if (!adj[e.from_id]) adj[e.from_id] = [];
    if (!adj[e.to_id]) adj[e.to_id] = [];
    adj[e.from_id].push(e.to_id);
    adj[e.to_id].push(e.from_id);
  }

  const ids = Object.keys(state);
  const n = ids.length;

  for (let iter = 0; iter < iterations; iter++) {
    if (cancelled) return;

    if (iter % 10 === 0) {
      self.postMessage({type: 'progress', iteration: iter, total: iterations});
    }

    for (let i = 0; i < n; i++) {
      const a = state[ids[i]];
      a.vx = 0;
      a.vy = 0;
      a.vx -= a.x * gravity * 0.01;
      a.vy -= a.y * gravity * 0.01;

      for (let j = i + 1; j < n; j++) {
        const b = state[ids[j]];
        const dx = a.x - b.x, dy = a.y - b.y;
        const dist2 = dx * dx + dy * dy;
        const dist = Math.sqrt(dist2) || 0.01;
        const repulse = scalingRatio * a.mass * b.mass / dist;
        const fx = (dx / dist) * repulse, fy = (dy / dist) * repulse;
        a.vx += fx; a.vy += fy;
        b.vx -= fx; b.vy -= fy;
      }
    }

    for (const e of edges) {
      const a = state[e.from_id], b = state[e.to_id];
      if (!a || !b) continue;
      const dx = b.x - a.x, dy = b.y - a.y;
      const dist = Math.sqrt(dx * dx + dy * dy) || 0.01;
      const attract = dist / (a.mass * b.mass);
      a.vx += dx * attract; a.vy += dy * attract;
      b.vx -= dx * attract; b.vy -= dy * attract;
    }

    const temp = 10 * (1 - iter / iterations);
    for (const id of ids) {
      const s = state[id];
      const speed = Math.sqrt(s.vx * s.vx + s.vy * s.vy);
      if (speed > temp) {
        s.vx = (s.vx / speed) * temp;
        s.vy = (s.vy / speed) * temp;
      }
      s.x += s.vx;
      s.y += s.vy;
    }
  }

  for (const id of ids) {
    positions[id] = {x: state[id].x, y: state[id].y};
  }
}

function runDagre(nodes, edges, positions, opts) {
  const rankSep = opts.rankSep || 80;
  const nodeSep = opts.nodeSep || 40;

  const adj = {};
  const inDeg = {};
  for (const n of nodes) {
    adj[n.id] = [];
    inDeg[n.id] = 0;
  }
  for (const e of edges) {
    if (adj[e.from_id]) adj[e.from_id].push(e.to_id);
    if (e.to_id in inDeg) inDeg[e.to_id] = (inDeg[e.to_id] || 0) + 1;
  }

  // Topological layering via Kahn's algorithm
  const rank = {};
  const queue = [];
  for (const n of nodes) {
    if (!inDeg[n.id]) queue.push(n.id);
  }
  let qi = 0;
  while (qi < queue.length) {
    const id = queue[qi++];
    rank[id] = rank[id] || 0;
    for (const tgt of adj[id] || []) {
      rank[tgt] = Math.max(rank[tgt] || 0, (rank[id] || 0) + 1);
      inDeg[tgt]--;
      if (inDeg[tgt] <= 0) queue.push(tgt);
    }
  }
  // Handle cycles
  for (const n of nodes) {
    if (!(n.id in rank)) rank[n.id] = 0;
  }

  const byRank = {};
  for (const n of nodes) {
    const r = rank[n.id] || 0;
    if (!byRank[r]) byRank[r] = [];
    byRank[r].push(n.id);
  }

  const maxRank = Math.max(...Object.keys(byRank).map(Number), 0);
  self.postMessage({type: 'progress', iteration: 50, total: 100});

  for (let r = 0; r <= maxRank; r++) {
    const row = byRank[r] || [];
    const totalWidth = row.length * nodeSep;
    row.forEach((id, i) => {
      positions[id] = {
        x: (i - row.length / 2) * nodeSep + totalWidth / 2,
        y: r * rankSep,
      };
    });
  }
}

function runCola(nodes, edges, positions, opts) {
  const iterations = opts.iterations || 60;

  const state = {};
  for (const n of nodes) {
    state[n.id] = {x: Math.random() * 800, y: Math.random() * 800};
  }

  const idealLength = opts.idealLength || 100;

  for (let iter = 0; iter < iterations; iter++) {
    if (cancelled) return;
    if (iter % 10 === 0) {
      self.postMessage({type: 'progress', iteration: iter, total: iterations});
    }

    for (const e of edges) {
      const a = state[e.from_id], b = state[e.to_id];
      if (!a || !b) continue;
      const dx = b.x - a.x, dy = b.y - a.y;
      const dist = Math.sqrt(dx * dx + dy * dy) || 0.01;
      const diff = (dist - idealLength) / dist * 0.5;
      const mx = dx * diff * 0.1, my = dy * diff * 0.1;
      a.x += mx; a.y += my;
      b.x -= mx; b.y -= my;
    }

    const ids = Object.keys(state);
    for (let i = 0; i < ids.length; i++) {
      for (let j = i + 1; j < ids.length; j++) {
        const a = state[ids[i]], b = state[ids[j]];
        const dx = b.x - a.x, dy = b.y - a.y;
        const dist = Math.sqrt(dx * dx + dy * dy) || 0.01;
        if (dist < idealLength * 0.5) {
          const push = (idealLength * 0.5 - dist) / dist * 0.05;
          a.x -= dx * push; a.y -= dy * push;
          b.x += dx * push; b.y += dy * push;
        }
      }
    }
  }

  for (const id of Object.keys(state)) {
    positions[id] = {x: state[id].x, y: state[id].y};
  }
}

function runOrthogonal(nodes, edges, positions, opts) {
  const spacing = opts.gridSpacing || 140;

  const adj = {};
  const incoming = {};
  const outgoing = {};
  for (const n of nodes) {
    adj[n.id] = [];
    incoming[n.id] = 0;
    outgoing[n.id] = 0;
  }
  for (const e of edges) {
    if (adj[e.from_id]) adj[e.from_id].push(e.to_id);
    if (e.to_id in incoming) incoming[e.to_id]++;
    if (e.from_id in outgoing) outgoing[e.from_id]++;
  }

  const rank = {};
  const queue = [];
  for (const n of nodes) {
    if (!incoming[n.id]) queue.push(n.id);
  }
  const visited = new Set();
  let qi = 0;
  while (qi < queue.length) {
    const id = queue[qi++];
    if (visited.has(id)) continue;
    visited.add(id);
    rank[id] = rank[id] || 0;
    for (const tgt of adj[id] || []) {
      rank[tgt] = Math.max(rank[tgt] || 0, (rank[id] || 0) + 1);
      if (!visited.has(tgt)) queue.push(tgt);
    }
  }
  for (const n of nodes) {
    if (!(n.id in rank)) rank[n.id] = 0;
  }

  const byRank = {};
  for (const n of nodes) {
    const r = rank[n.id] || 0;
    if (!byRank[r]) byRank[r] = [];
    byRank[r].push(n);
  }

  const maxRank = Math.max(...Object.keys(byRank).map(Number), 0);
  self.postMessage({type: 'progress', iteration: 50, total: 100});

  for (let r = 0; r <= maxRank; r++) {
    const row = byRank[r] || [];
    row.sort((a, b) => (outgoing[b.id] || 0) - (outgoing[a.id] || 0) || String(a.id).localeCompare(String(b.id)));
    const totalWidth = row.length * spacing;
    row.forEach((node, i) => {
      positions[node.id] = {
        x: (i - row.length / 2) * spacing + totalWidth / 2,
        y: r * spacing,
      };
    });
  }
}
