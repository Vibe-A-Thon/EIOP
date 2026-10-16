// Layout algorithm implementations for the graph explorer enhancements.
// All algorithms are pure: they take nodes/edges and return {id: {x, y}} positions.

const LAYOUTS = ['force', 'hierarchical', 'circular'];

export function listLayouts() {
  return [...LAYOUTS];
}

export const LAYOUT_LABELS = {
  force: 'Force directed',
  hierarchical: 'Hierarchical',
  circular: 'Circular',
};

function adjacency(nodes, edges) {
  const map = new Map(nodes.map(node => [node.id, []]));
  for (const edge of edges) {
    if (map.has(edge.from_id) && map.has(edge.to_id)) {
      map.get(edge.from_id).push(edge.to_id);
      map.get(edge.to_id).push(edge.from_id);
    }
  }
  return map;
}

function circular(nodes) {
  const positions = {};
  const n = Math.max(nodes.length, 1);
  const radius = Math.max(120, n * 22);
  nodes.forEach((node, index) => {
    const angle = (2 * Math.PI * index) / n - Math.PI / 2;
    positions[node.id] = {
      x: Math.round(radius * Math.cos(angle)),
      y: Math.round(radius * Math.sin(angle)),
    };
  });
  return positions;
}

function hierarchical(nodes, edges) {
  const adj = adjacency(nodes, edges);
  const depth = new Map();
  const queue = [];
  for (const node of nodes) {
    if (!edges.some(edge => edge.to_id === node.id)) {
      depth.set(node.id, 0);
      queue.push(node.id);
    }
  }
  if (!queue.length && nodes.length) {
    depth.set(nodes[0].id, 0);
    queue.push(nodes[0].id);
  }
  while (queue.length) {
    const id = queue.shift();
    for (const next of adj.get(id) || []) {
      if (!depth.has(next)) {
        depth.set(next, depth.get(id) + 1);
        queue.push(next);
      }
    }
  }
  for (const node of nodes) if (!depth.has(node.id)) depth.set(node.id, 0);
  const byDepth = new Map();
  for (const node of nodes) {
    const level = depth.get(node.id);
    if (!byDepth.has(level)) byDepth.set(level, []);
    byDepth.get(level).push(node.id);
  }
  const positions = {};
  const xGap = 190, yGap = 150;
  for (const [level, ids] of byDepth) {
    ids.forEach((id, index) => {
      positions[id] = {x: level * xGap, y: (index - (ids.length - 1) / 2) * yGap};
    });
  }
  return positions;
}

function force(nodes, edges, iterations = 240) {
  const n = nodes.length;
  const positions = {};
  nodes.forEach((node, index) => {
    const angle = (2 * Math.PI * index) / Math.max(n, 1);
    positions[node.id] = {x: 260 * Math.cos(angle), y: 260 * Math.sin(angle)};
  });
  const adj = adjacency(nodes, edges);
  const k = Math.max(140, Math.sqrt((600 * 500) / Math.max(n, 1)));
  const repulsion = 5200;
  const ids = nodes.map(node => node.id);
  for (let iter = 0; iter < iterations; iter++) {
    const disp = {};
    for (const id of ids) disp[id] = {x: 0, y: 0};
    for (let i = 0; i < ids.length; i++) {
      for (let j = i + 1; j < ids.length; j++) {
        const a = positions[ids[i]], b = positions[ids[j]];
        let dx = a.x - b.x, dy = a.y - b.y;
        let dist = Math.sqrt(dx * dx + dy * dy) || 0.01;
        const forceRep = repulsion / (dist * dist);
        dx = (dx / dist) * forceRep;
        dy = (dy / dist) * forceRep;
        disp[ids[i]].x += dx; disp[ids[i]].y += dy;
        disp[ids[j]].x -= dx; disp[ids[j]].y -= dy;
      }
    }
    for (const edge of edges) {
      if (!positions[edge.from_id] || !positions[edge.to_id]) continue;
      const a = positions[edge.from_id], b = positions[edge.to_id];
      const dx = b.x - a.x, dy = b.y - a.y;
      const dist = Math.sqrt(dx * dx + dy * dy) || 0.01;
      const forceAtt = (dist - k) * 0.06;
      const ux = (dx / dist) * forceAtt, uy = (dy / dist) * forceAtt;
      disp[edge.from_id].x += ux; disp[edge.from_id].y += uy;
      disp[edge.to_id].x -= ux; disp[edge.to_id].y -= uy;
    }
    const temp = 28 * (1 - iter / iterations) + 2;
    for (const id of ids) {
      const d = disp[id];
      const mag = Math.sqrt(d.x * d.x + d.y * d.y) || 0.01;
      positions[id] = {
        x: positions[id].x + (d.x / mag) * Math.min(mag, temp),
        y: positions[id].y + (d.y / mag) * Math.min(mag, temp),
      };
    }
  }
  return positions;
}

export function computeLayout(name, nodes, edges) {
  switch (name) {
    case 'circular': return circular(nodes);
    case 'hierarchical': return hierarchical(nodes, edges);
    case 'force':
    default: return force(nodes, edges);
  }
}

// Apply computed positions to a live cytoscape instance (nodes keyed by id).
export function applyPositionsToCy(cy, positions, animate = true) {
  if (!cy || !positions) return;
  cy.nodes().forEach(node => {
    const pos = positions[node.id()];
    if (pos) node.position({x: pos.x, y: pos.y});
  });
  if (animate && cy.animate) {
    cy.animate({fit: {eles: cy.elements(), padding: 38}}, {duration: 240});
  } else {
    cy.fit(undefined, 38);
  }
}
