import React, {useMemo} from 'react';

const AXES = [
  {key: 'degree', label: 'Degree', tip: 'Total connections (in + out)'},
  {key: 'betweenness', label: 'Betweenness', tip: 'How often this node sits on shortest paths between others'},
  {key: 'closeness', label: 'Closeness', tip: 'Average distance to all reachable nodes'},
  {key: 'page_rank', label: 'PageRank', tip: 'Influence: importance propagated from neighbors'},
  {key: 'eigenvector', label: 'Eigenvector', tip: 'Importance based on connectivity to other important nodes'},
];

const CX = 140, CY = 140, R = 100, RINGS = 4;

function polarPoint(index, total, value) {
  const angle = (2 * Math.PI * index) / total - Math.PI / 2;
  return {x: CX + R * value * Math.cos(angle), y: CY + R * value * Math.sin(angle)};
}

function radarPolygon(values, count) {
  return values.map((v, i) => {
    const pt = polarPoint(i, count, v);
    return `${pt.x},${pt.y}`;
  }).join(' ');
}

function normalizeMetrics(metrics, allMetrics) {
  if (!metrics) return AXES.map(() => 0);
  return AXES.map(({key}) => {
    const raw = metrics[key] ?? 0;
    if (!allMetrics || allMetrics.length === 0) return Math.min(raw, 1);
    const vals = allMetrics.map(m => m[key] ?? 0).filter(v => v > 0);
    if (vals.length === 0) return 0;
    const max = Math.max(...vals);
    return max > 0 ? raw / max : 0;
  });
}

export default function CentralityRadar({metrics, comparisonMetrics, allMetrics, width}) {
  const scale = Math.min((width || 280) / 280, 1.4);
  const primary = useMemo(() => normalizeMetrics(metrics, allMetrics), [metrics, allMetrics]);
  const comparison = useMemo(() => comparisonMetrics ? normalizeMetrics(comparisonMetrics, allMetrics) : null,
    [comparisonMetrics, allMetrics]);
  const axisCount = AXES.length;

  return <svg viewBox="0 0 280 280" width={280 * scale} height={280 * scale} className="centrality-radar"
    role="img" aria-label="Centrality radar chart">
    {[...Array(RINGS)].map((_, ring) => {
      const r = (ring + 1) / RINGS;
      const pts = AXES.map((_, i) => polarPoint(i, axisCount, r));
      return <polygon key={ring} points={pts.map(p => `${p.x},${p.y}`).join(' ')}
        fill="none" stroke="var(--radar-ring)" strokeWidth="0.5" opacity={0.4}/>;
    })}

    {AXES.map((axis, i) => {
      const end = polarPoint(i, axisCount, 1.0);
      const labelPt = polarPoint(i, axisCount, 1.18);
      return <g key={axis.key}>
        <line x1={CX} y1={CY} x2={end.x} y2={end.y} stroke="var(--radar-axis)" strokeWidth="0.5" opacity={0.5}/>
        <text x={labelPt.x} y={labelPt.y} textAnchor="middle" dominantBaseline="central"
          fontSize="9" fill="var(--radar-label)" fontWeight="500">
          <title>{axis.tip}</title>
          {axis.label}
        </text>
      </g>;
    })}

    {comparison && <polygon points={radarPolygon(comparison, axisCount)}
      fill="var(--radar-comparison-fill)" stroke="var(--radar-comparison-stroke)" strokeWidth="1.5" opacity={0.6}/>}

    <polygon points={radarPolygon(primary, axisCount)}
      fill="var(--radar-primary-fill)" stroke="var(--radar-primary-stroke)" strokeWidth="2"/>

    {primary.map((v, i) => {
      const pt = polarPoint(i, axisCount, v);
      return <circle key={i} cx={pt.x} cy={pt.y} r="3.5"
        fill="var(--radar-primary-stroke)" stroke="var(--bg)" strokeWidth="1.5">
        <title>{AXES[i].label}: {(metrics?.[AXES[i].key] ?? 0).toFixed(4)}</title>
      </circle>;
    })}

    {comparison && comparison.map((v, i) => {
      const pt = polarPoint(i, axisCount, v);
      return <circle key={i} cx={pt.x} cy={pt.y} r="2.5"
        fill="var(--radar-comparison-stroke)" stroke="var(--bg)" strokeWidth="1">
        <title>{AXES[i].label}: {(comparisonMetrics?.[AXES[i].key] ?? 0).toFixed(4)}</title>
      </circle>;
    })}
  </svg>;
}
