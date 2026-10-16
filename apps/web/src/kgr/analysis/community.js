/**
 * Client-side community detection for small graphs (<1K nodes).
 * Simplified Louvain operating on a {nodes, edges} graph object.
 */

function buildUndirected(graph) {
  const adj = {};
  for (const n of graph.nodes || []) adj[n.id] = new Set();
  for (const e of graph.edges || []) {
    if (adj[e.from_id]) adj[e.from_id].add(e.to_id);
    if (adj[e.to_id]) adj[e.to_id].add(e.from_id);
  }
  return adj;
}

export function detectCommunities(graph, {algorithm = 'louvain', resolution = 1.0, maxIterations = 20} = {}) {
  const adj = buildUndirected(graph);
  const nodes = Object.keys(adj);
  if (nodes.length === 0) return {communities: {}, count: 0};

  const comm = {};
  nodes.forEach((n, i) => comm[n] = i);

  let totalEdges = 0;
  for (const n of nodes) totalEdges += adj[n].size;
  totalEdges /= 2;

  if (totalEdges === 0) return {communities: comm, count: nodes.length};

  const m2 = 2 * totalEdges;
  const deg = {};
  for (const n of nodes) deg[n] = adj[n].size;

  for (let iter = 0; iter < maxIterations; iter++) {
    let moved = false;
    const order = [...nodes].sort(() => Math.random() - 0.5);

    for (const node of order) {
      const cur = comm[node];
      const ki = deg[node];
      const nbrEdges = {};
      for (const nbr of adj[node]) {
        const c = comm[nbr];
        nbrEdges[c] = (nbrEdges[c] || 0) + 1;
      }
      const commDeg = {};
      for (const n of nodes) commDeg[comm[n]] = (commDeg[comm[n]] || 0) + deg[n];
      const ownEdges = nbrEdges[cur] || 0;
      const sigmaOwn = commDeg[cur] - ki;

      let bestDelta = 0, bestComm = cur;
      for (const [c, kiC] of Object.entries(nbrEdges)) {
        const cNum = Number(c);
        if (cNum === cur) continue;
        const sigmaC = commDeg[cNum] || 0;
        const delta = (kiC - ownEdges) / totalEdges - resolution * ki * (sigmaC - sigmaOwn) / (m2 * totalEdges);
        if (delta > bestDelta) { bestDelta = delta; bestComm = cNum; }
      }
      if (bestComm !== cur) { comm[node] = bestComm; moved = true; }
    }
    if (!moved) break;
  }

  const remap = {};
  let nextId = 0;
  for (const n of nodes) {
    if (!(comm[n] in remap)) remap[comm[n]] = nextId++;
    comm[n] = remap[comm[n]];
  }

  return {communities: comm, count: nextId};
}

export function computeConvexHulls(positions, communities) {
  const groups = {};
  for (const [nodeId, commId] of Object.entries(communities)) {
    if (!groups[commId]) groups[commId] = [];
    const pos = positions[nodeId];
    if (pos) groups[commId].push(pos);
  }
  return groups;
}
