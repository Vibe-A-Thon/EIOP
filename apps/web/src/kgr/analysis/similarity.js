/**
 * Client-side similarity algorithms for small graphs (< 500 nodes).
 * Server fallback for larger graphs via /api/v1/graph/similarity.
 */

export function buildAdjacency(nodes, edges) {
  const adj = {};
  for (const n of nodes) adj[n.id] = new Set();
  for (const e of edges) {
    if (adj[e.from_id]) adj[e.from_id].add(e.to_id);
    if (adj[e.to_id]) adj[e.to_id].add(e.from_id);
  }
  return adj;
}

export function jaccardSimilarity(adj, nodeId, limit = 10) {
  const nbrs = adj[nodeId];
  if (!nbrs || nbrs.size === 0) return [];
  const results = [];
  for (const [otherId, otherNbrs] of Object.entries(adj)) {
    if (otherId === nodeId || otherNbrs.size === 0) continue;
    let intersection = 0;
    for (const n of nbrs) if (otherNbrs.has(n)) intersection++;
    if (intersection === 0) continue;
    const union = nbrs.size + otherNbrs.size - intersection;
    results.push({canonical_id: otherId, score: intersection / union, common_neighbors: intersection});
  }
  results.sort((a, b) => b.score - a.score);
  return results.slice(0, limit);
}

export function adamicAdar(adj, nodeId, limit = 10) {
  const nbrs = adj[nodeId];
  if (!nbrs || nbrs.size === 0) return [];
  const results = [];
  for (const [otherId, otherNbrs] of Object.entries(adj)) {
    if (otherId === nodeId || otherNbrs.size === 0) continue;
    let score = 0;
    let common = 0;
    for (const n of nbrs) {
      if (otherNbrs.has(n)) {
        common++;
        const deg = (adj[n] || new Set()).size;
        if (deg > 1) score += 1.0 / Math.log(deg);
      }
    }
    if (score > 0) results.push({canonical_id: otherId, score, common_neighbors: common});
  }
  results.sort((a, b) => b.score - a.score);
  return results.slice(0, limit);
}

export function commonNeighbors(adj, nodeId, limit = 10) {
  const nbrs = adj[nodeId];
  if (!nbrs || nbrs.size === 0) return [];
  const results = [];
  for (const [otherId, otherNbrs] of Object.entries(adj)) {
    if (otherId === nodeId || otherNbrs.size === 0) continue;
    let common = 0;
    for (const n of nbrs) if (otherNbrs.has(n)) common++;
    if (common > 0) results.push({canonical_id: otherId, score: common, common_neighbors: common});
  }
  results.sort((a, b) => b.score - a.score);
  return results.slice(0, limit);
}
