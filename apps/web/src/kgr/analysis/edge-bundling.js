/**
 * Force-Directed Edge Bundling (FDEB) — Holten & van Wijk algorithm.
 * Bundles nearby compatible edges into curves for visual declutter.
 */

function edgeMidpoint(e) {
  return {x: (e.x1 + e.x2) / 2, y: (e.y1 + e.y2) / 2};
}

function edgeLength(e) {
  const dx = e.x2 - e.x1, dy = e.y2 - e.y1;
  return Math.sqrt(dx * dx + dy * dy) || 0.001;
}

function edgeVector(e) {
  const len = edgeLength(e);
  return {x: (e.x2 - e.x1) / len, y: (e.y2 - e.y1) / len};
}

export function angleCompatibility(e1, e2) {
  const v1 = edgeVector(e1), v2 = edgeVector(e2);
  return Math.abs(v1.x * v2.x + v1.y * v2.y);
}

export function scaleCompatibility(e1, e2) {
  const l1 = edgeLength(e1), l2 = edgeLength(e2);
  const avg = (l1 + l2) / 2;
  return 2 / (avg / Math.min(l1, l2) + Math.max(l1, l2) / avg);
}

export function positionCompatibility(e1, e2) {
  const avg = (edgeLength(e1) + edgeLength(e2)) / 2;
  const m1 = edgeMidpoint(e1), m2 = edgeMidpoint(e2);
  const dx = m1.x - m2.x, dy = m1.y - m2.y;
  const dist = Math.sqrt(dx * dx + dy * dy);
  return avg / (avg + dist);
}

export function visibilityCompatibility(e1, e2) {
  const m1 = edgeMidpoint(e1), m2 = edgeMidpoint(e2);
  const dx1 = m2.x - e1.x1, dy1 = m2.y - e1.y1;
  const ex1 = e1.x2 - e1.x1, ey1 = e1.y2 - e1.y1;
  const len1sq = ex1 * ex1 + ey1 * ey1;
  const t1 = len1sq > 0 ? Math.max(0, Math.min(1, (dx1 * ex1 + dy1 * ey1) / len1sq)) : 0.5;
  const px1 = e1.x1 + t1 * ex1, py1 = e1.y1 + t1 * ey1;
  const d1 = Math.sqrt((m2.x - px1) ** 2 + (m2.y - py1) ** 2);

  const dx2 = m1.x - e2.x1, dy2 = m1.y - e2.y1;
  const ex2 = e2.x2 - e2.x1, ey2 = e2.y2 - e2.y1;
  const len2sq = ex2 * ex2 + ey2 * ey2;
  const t2 = len2sq > 0 ? Math.max(0, Math.min(1, (dx2 * ex2 + dy2 * ey2) / len2sq)) : 0.5;
  const px2 = e2.x1 + t2 * ex2, py2 = e2.y1 + t2 * ey2;
  const d2 = Math.sqrt((m1.x - px2) ** 2 + (m1.y - py2) ** 2);

  const avg = (edgeLength(e1) + edgeLength(e2)) / 2;
  return Math.max(0, 1 - 2 * Math.max(d1, d2) / avg);
}

export function edgeCompatibility(e1, e2) {
  return angleCompatibility(e1, e2) *
         scaleCompatibility(e1, e2) *
         positionCompatibility(e1, e2) *
         visibilityCompatibility(e1, e2);
}

export function forceDirectedEdgeBundling(edges, options = {}) {
  const {
    iterations = 6,
    subdivisions = 6,
    stepSize = 0.1,
    compatibilityThreshold = 0.6,
    maxEdges = 2000,
    strength = 1.0,
  } = options;

  if (!edges.length || edges.length > maxEdges) return edges.map(e => [{x: e.x1, y: e.y1}, {x: e.x2, y: e.y2}]);

  const compatCache = new Map();
  function getCompat(i, j) {
    const key = i < j ? `${i}:${j}` : `${j}:${i}`;
    if (compatCache.has(key)) return compatCache.get(key);
    const c = edgeCompatibility(edges[i], edges[j]);
    compatCache.set(key, c);
    return c;
  }

  let P = 1;
  const controlPoints = edges.map(e => [{x: e.x1, y: e.y1}, {x: e.x2, y: e.y2}]);

  for (let cycle = 0; cycle < iterations; cycle++) {
    P = Math.min(P * 2, subdivisions * 2);
    for (let ei = 0; ei < edges.length; ei++) {
      const oldPts = controlPoints[ei];
      const newPts = [{x: edges[ei].x1, y: edges[ei].y1}];
      for (let p = 1; p <= P; p++) {
        const t = p / (P + 1);
        const x = edges[ei].x1 + t * (edges[ei].x2 - edges[ei].x1);
        const y = edges[ei].y1 + t * (edges[ei].y2 - edges[ei].y1);
        if (oldPts.length > 2) {
          const oldIdx = Math.min(Math.floor(t * (oldPts.length - 1)), oldPts.length - 2);
          const ot = t * (oldPts.length - 1) - oldIdx;
          newPts.push({
            x: oldPts[oldIdx].x * (1 - ot) + oldPts[oldIdx + 1].x * ot,
            y: oldPts[oldIdx].y * (1 - ot) + oldPts[oldIdx + 1].y * ot,
          });
        } else {
          newPts.push({x, y});
        }
      }
      newPts.push({x: edges[ei].x2, y: edges[ei].y2});
      controlPoints[ei] = newPts;
    }

    const S = stepSize / (2 ** cycle);
    for (let iter = 0; iter < Math.max(1, Math.ceil(50 / (2 ** cycle))); iter++) {
      for (let ei = 0; ei < edges.length; ei++) {
        const pts = controlPoints[ei];
        const forces = pts.map(() => ({x: 0, y: 0}));
        for (let p = 1; p < pts.length - 1; p++) {
          forces[p].x += (pts[p - 1].x - pts[p].x) + (pts[p + 1].x - pts[p].x);
          forces[p].y += (pts[p - 1].y - pts[p].y) + (pts[p + 1].y - pts[p].y);
        }
        for (let ej = 0; ej < edges.length; ej++) {
          if (ei === ej) continue;
          const compat = getCompat(ei, ej);
          if (compat < compatibilityThreshold) continue;
          const otherPts = controlPoints[ej];
          for (let p = 1; p < pts.length - 1; p++) {
            const otherIdx = Math.min(Math.round(p * (otherPts.length - 1) / (pts.length - 1)), otherPts.length - 1);
            const dx = otherPts[otherIdx].x - pts[p].x;
            const dy = otherPts[otherIdx].y - pts[p].y;
            const dist = Math.sqrt(dx * dx + dy * dy) || 1;
            const f = compat * strength / dist;
            forces[p].x += dx * f;
            forces[p].y += dy * f;
          }
        }
        for (let p = 1; p < pts.length - 1; p++) {
          pts[p].x += S * forces[p].x;
          pts[p].y += S * forces[p].y;
        }
      }
    }
  }

  return controlPoints;
}
