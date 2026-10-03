/**
 * Client-side centrality algorithms for small graphs (<500 nodes).
 * Operates on a {nodes: [...], edges: [...]} graph object.
 */

function buildAdjacency(graph) {
  const outAdj = {};
  const inAdj = {};
  for (const n of graph.nodes || []) {
    outAdj[n.id] = [];
    inAdj[n.id] = [];
  }
  for (const e of graph.edges || []) {
    if (outAdj[e.from_id]) outAdj[e.from_id].push(e.to_id);
    if (inAdj[e.to_id]) inAdj[e.to_id].push(e.from_id);
  }
  return {outAdj, inAdj};
}

export function degreeCentrality(graph) {
  const {outAdj, inAdj} = buildAdjacency(graph);
  const result = {};
  for (const n of graph.nodes || []) {
    result[n.id] = {
      degree: (outAdj[n.id]?.length || 0) + (inAdj[n.id]?.length || 0),
      in_degree: inAdj[n.id]?.length || 0,
      out_degree: outAdj[n.id]?.length || 0,
    };
  }
  return result;
}

export function betweennessCentrality(graph) {
  const {outAdj} = buildAdjacency(graph);
  const nodes = (graph.nodes || []).map(n => n.id);
  const cb = {};
  for (const n of nodes) cb[n] = 0;

  for (const s of nodes) {
    const stack = [];
    const pred = {};
    const sigma = {};
    const dist = {};
    for (const n of nodes) { pred[n] = []; sigma[n] = 0; dist[n] = -1; }
    sigma[s] = 1; dist[s] = 0;
    const queue = [s];
    let qi = 0;
    while (qi < queue.length) {
      const v = queue[qi++];
      stack.push(v);
      for (const w of outAdj[v] || []) {
        if (dist[w] < 0) { dist[w] = dist[v] + 1; queue.push(w); }
        if (dist[w] === dist[v] + 1) { sigma[w] += sigma[v]; pred[w].push(v); }
      }
    }
    const delta = {};
    for (const n of nodes) delta[n] = 0;
    while (stack.length) {
      const w = stack.pop();
      for (const v of pred[w]) {
        delta[v] += (sigma[v] / Math.max(sigma[w], 1)) * (1 + delta[w]);
      }
      if (w !== s) cb[w] += delta[w];
    }
  }

  const n = nodes.length;
  const norm = Math.max((n - 1) * (n - 2), 1);
  for (const k of nodes) cb[k] /= norm;
  return cb;
}

export function closenessCentrality(graph) {
  const {outAdj} = buildAdjacency(graph);
  const nodes = (graph.nodes || []).map(n => n.id);
  const result = {};
  for (const s of nodes) {
    const dist = {[s]: 0};
    const queue = [s];
    let qi = 0;
    while (qi < queue.length) {
      const v = queue[qi++];
      for (const w of outAdj[v] || []) {
        if (!(w in dist)) { dist[w] = dist[v] + 1; queue.push(w); }
      }
    }
    const totalDist = Object.values(dist).reduce((a, b) => a + b, 0);
    const reachable = Object.keys(dist).length - 1;
    result[s] = reachable > 0 ? reachable / Math.max(totalDist, 1) : 0;
  }
  return result;
}

export function pageRank(graph, {damping = 0.85, iterations = 20} = {}) {
  const {outAdj} = buildAdjacency(graph);
  const nodes = (graph.nodes || []).map(n => n.id);
  const n = nodes.length;
  if (n === 0) return {};
  let pr = {};
  for (const node of nodes) pr[node] = 1.0 / n;
  const outDeg = {};
  for (const node of nodes) outDeg[node] = (outAdj[node] || []).length;

  for (let iter = 0; iter < iterations; iter++) {
    const newPr = {};
    for (const node of nodes) {
      let rank = (1 - damping) / n;
      for (const other of nodes) {
        if ((outAdj[other] || []).includes(node)) {
          rank += damping * pr[other] / Math.max(outDeg[other], 1);
        }
      }
      newPr[node] = rank;
    }
    pr = newPr;
  }
  return pr;
}

export function graphDensity(graph) {
  const n = (graph.nodes || []).length;
  const e = (graph.edges || []).length;
  return n > 1 ? e / (n * (n - 1)) : 0;
}

export function connectedComponents(graph) {
  const {outAdj, inAdj} = buildAdjacency(graph);
  const nodes = (graph.nodes || []).map(n => n.id);
  const visited = new Set();
  const components = [];
  for (const start of nodes) {
    if (visited.has(start)) continue;
    const component = [];
    const queue = [start];
    visited.add(start);
    while (queue.length) {
      const v = queue.shift();
      component.push(v);
      for (const nbr of [...(outAdj[v] || []), ...(inAdj[v] || [])]) {
        if (!visited.has(nbr)) { visited.add(nbr); queue.push(nbr); }
      }
    }
    components.push(component);
  }
  return components;
}

export function degreeDistribution(graph) {
  const {outAdj, inAdj} = buildAdjacency(graph);
  const hist = {};
  for (const n of graph.nodes || []) {
    const deg = (outAdj[n.id]?.length || 0) + (inAdj[n.id]?.length || 0);
    hist[deg] = (hist[deg] || 0) + 1;
  }
  return hist;
}

export function clusteringCoefficient(graph) {
  const {outAdj, inAdj} = buildAdjacency(graph);
  const result = {};
  for (const n of graph.nodes || []) {
    const neighbors = new Set([...(outAdj[n.id] || []), ...(inAdj[n.id] || [])]);
    const k = neighbors.size;
    if (k < 2) { result[n.id] = 0; continue; }
    let links = 0;
    const nbArr = [...neighbors];
    for (let i = 0; i < nbArr.length; i++) {
      for (let j = i + 1; j < nbArr.length; j++) {
        if ((outAdj[nbArr[i]] || []).includes(nbArr[j]) || (outAdj[nbArr[j]] || []).includes(nbArr[i])) {
          links++;
        }
      }
    }
    result[n.id] = (2 * links) / (k * (k - 1));
  }
  return result;
}
