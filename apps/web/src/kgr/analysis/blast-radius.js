/**
 * Client-side blast radius for small graphs (<500 nodes).
 */

export function clientBlastRadius(graph, nodeId, maxDepth = 4) {
  const outAdj = {};
  for (const n of graph.nodes || []) outAdj[n.id] = [];
  for (const e of graph.edges || []) {
    if (outAdj[e.from_id]) outAdj[e.from_id].push(e.to_id);
  }

  const nodeLabels = {};
  for (const n of graph.nodes || []) nodeLabels[n.id] = n.label || 'Unknown';

  const visited = new Set([nodeId]);
  const queue = [{id: nodeId, depth: 0}];
  const byDepth = {};
  const byType = {};
  const affected = [];

  while (queue.length) {
    const {id, depth} = queue.shift();
    if (depth >= maxDepth) continue;
    for (const nbr of outAdj[id] || []) {
      if (visited.has(nbr)) continue;
      visited.add(nbr);
      const d = depth + 1;
      byDepth[d] = (byDepth[d] || 0) + 1;
      const label = nodeLabels[nbr] || 'Unknown';
      byType[label] = (byType[label] || 0) + 1;
      affected.push(nbr);
      queue.push({id: nbr, depth: d});
    }
  }

  const total = affected.length;
  const totalGraph = (graph.nodes || []).length;
  const pct = totalGraph > 0 ? (total / totalGraph) * 100 : 0;
  const risk = pct > 20 ? 'HIGH' : pct > 5 ? 'MEDIUM' : 'LOW';

  return {target_id: nodeId, total_affected: total, by_depth: byDepth, by_type: byType, risk, affected_ids: affected};
}
