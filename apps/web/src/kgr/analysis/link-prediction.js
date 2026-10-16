/**
 * Client-side link prediction for small graphs (< 500 nodes).
 * Predicts missing edges based on structural similarity.
 */

import {buildAdjacency} from './similarity.js';

export function predictLinks(nodes, edges, nodeId, algorithm = 'common_neighbors', limit = 10) {
  const adj = buildAdjacency(nodes, edges);
  const nbrs = adj[nodeId];
  if (!nbrs || nbrs.size === 0) return [];

  const predictions = [];
  for (const [otherId, otherNbrs] of Object.entries(adj)) {
    if (otherId === nodeId || nbrs.has(otherId)) continue;

    let common = 0;
    for (const n of nbrs) if (otherNbrs.has(n)) common++;
    if (common === 0) continue;

    let score;
    if (algorithm === 'jaccard') {
      const union = nbrs.size + otherNbrs.size - common;
      score = union > 0 ? common / union : 0;
    } else if (algorithm === 'adamic_adar') {
      score = 0;
      for (const n of nbrs) {
        if (otherNbrs.has(n)) {
          const deg = (adj[n] || new Set()).size;
          if (deg > 1) score += 1.0 / Math.log(deg);
        }
      }
    } else {
      score = common;
    }

    if (score > 0) {
      predictions.push({source_id: nodeId, target_id: otherId, score, algorithm});
    }
  }

  predictions.sort((a, b) => b.score - a.score);
  return predictions.slice(0, limit);
}
