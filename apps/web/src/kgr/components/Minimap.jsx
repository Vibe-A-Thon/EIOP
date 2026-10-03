import React, {useCallback, useMemo, useRef} from 'react';

const WIDTH = 200;
const HEIGHT = 150;
const PADDING = 8;

export default function Minimap({nodes, viewport, onNavigate, selectedId}) {
  const svgRef = useRef(null);

  const bounds = useMemo(() => {
    if (!nodes || nodes.length === 0) return {minX: 0, minY: 0, maxX: 100, maxY: 100};
    let minX = Infinity, minY = Infinity, maxX = -Infinity, maxY = -Infinity;
    for (const n of nodes) {
      const x = n.position?.x ?? n.x ?? 0;
      const y = n.position?.y ?? n.y ?? 0;
      if (x < minX) minX = x;
      if (y < minY) minY = y;
      if (x > maxX) maxX = x;
      if (y > maxY) maxY = y;
    }
    const dx = maxX - minX || 100;
    const dy = maxY - minY || 100;
    return {minX: minX - dx * 0.05, minY: minY - dy * 0.05, maxX: maxX + dx * 0.05, maxY: maxY + dy * 0.05};
  }, [nodes]);

  const scale = useMemo(() => {
    const w = bounds.maxX - bounds.minX || 1;
    const h = bounds.maxY - bounds.minY || 1;
    return Math.min((WIDTH - PADDING * 2) / w, (HEIGHT - PADDING * 2) / h);
  }, [bounds]);

  const toMinimap = useCallback((x, y) => ({
    mx: PADDING + (x - bounds.minX) * scale,
    my: PADDING + (y - bounds.minY) * scale,
  }), [bounds, scale]);

  const handleClick = useCallback((e) => {
    if (!svgRef.current || !onNavigate) return;
    const rect = svgRef.current.getBoundingClientRect();
    const mx = e.clientX - rect.left;
    const my = e.clientY - rect.top;
    const x = bounds.minX + (mx - PADDING) / scale;
    const y = bounds.minY + (my - PADDING) / scale;
    onNavigate({x, y});
  }, [bounds, scale, onNavigate]);

  const vp = viewport || {};
  const vpRect = useMemo(() => {
    if (!vp.x1 && !vp.x2) return null;
    const tl = toMinimap(vp.x1 || 0, vp.y1 || 0);
    const br = toMinimap(vp.x2 || 100, vp.y2 || 100);
    return {x: tl.mx, y: tl.my, w: br.mx - tl.mx, h: br.my - tl.my};
  }, [vp, toMinimap]);

  return <div className="kgr-minimap" role="img" aria-label="Graph minimap">
    <svg ref={svgRef} width={WIDTH} height={HEIGHT} onClick={handleClick} style={{cursor: 'crosshair'}}>
      <rect x={0} y={0} width={WIDTH} height={HEIGHT} fill="var(--surface-bg, #1e293b)" rx={4}/>
      {(nodes || []).map(n => {
        const {mx, my} = toMinimap(n.position?.x ?? n.x ?? 0, n.position?.y ?? n.y ?? 0);
        return <circle key={n.id} cx={mx} cy={my} r={n.id === selectedId ? 3 : 1.5}
          fill={n.id === selectedId ? '#3b82f6' : '#94a3b8'} opacity={0.8}/>;
      })}
      {vpRect && <rect x={vpRect.x} y={vpRect.y} width={Math.max(vpRect.w, 4)} height={Math.max(vpRect.h, 4)}
        fill="none" stroke="#3b82f6" strokeWidth={1.5} rx={2} opacity={0.7}/>}
    </svg>
  </div>;
}
