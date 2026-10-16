import React, {useCallback, useEffect, useRef, useState} from 'react';

const WIDTH = 176;
const HEIGHT = 124;

function readPositions(cy) {
  const positions = {};
  if (!cy) return positions;
  cy.nodes().forEach(node => {
    positions[node.id()] = node.position();
  });
  return positions;
}

function readViewport(cy) {
  if (!cy) return null;
  const extent = cy.extent();
  return {x1: extent.x1, y1: extent.y1, x2: extent.x2, y2: extent.y2};
}

// GraphMinimap: SVG overview of the full node set with a viewport rectangle.
// Click or drag to navigate the main graph (via the live cytoscape instance).
export default function GraphMinimap({cyRef, width = WIDTH, height = HEIGHT}) {
  const svgRef = useRef(null);
  const dragRef = useRef(false);
  const [frame, setFrame] = useState({positions: {}, viewport: null});

  const getCy = useCallback(() => (typeof cyRef === 'function' ? cyRef() : cyRef?.current), [cyRef]);

  useEffect(() => {
    const cy = getCy();
    if (!cy) return undefined;
    let raf = 0;
    const update = () => {
      cancelAnimationFrame(raf);
      raf = requestAnimationFrame(() => setFrame({positions: readPositions(cy), viewport: readViewport(cy)}));
    };
    update();
    cy.on('render pan zoom layoutstop', update);
    return () => {
      cancelAnimationFrame(raf);
      cy.removeListener('render pan zoom layoutstop', undefined, update);
    };
  }, [getCy]);

  const ids = Object.keys(frame.positions);
  const bounds = ids.length ? ids.reduce((acc, id) => {
    const p = frame.positions[id];
    return {
      minX: Math.min(acc.minX, p.x), maxX: Math.max(acc.maxX, p.x),
      minY: Math.min(acc.minY, p.y), maxY: Math.max(acc.maxY, p.y),
    };
  }, {minX: Infinity, maxX: -Infinity, minY: Infinity, maxY: -Infinity}) : null;

  const scale = bounds
    ? Math.min(width / Math.max(bounds.maxX - bounds.minX, 1), height / Math.max(bounds.maxY - bounds.minY, 1)) * 0.86
    : 1;
  const offsetX = bounds ? (width - (bounds.maxX - bounds.minX) * scale) / 2 - bounds.minX * scale : 0;
  const offsetY = bounds ? (height - (bounds.maxY - bounds.minY) * scale) / 2 - bounds.minY * scale : 0;
  const project = p => ({x: p.x * scale + offsetX, y: p.y * scale + offsetY});

  const navigate = event => {
    const cy = getCy();
    const rect = svgRef.current?.getBoundingClientRect();
    if (!cy || !rect) return;
    const x = ((event.clientX - rect.left) - offsetX) / scale;
    const y = ((event.clientY - rect.top) - offsetY) / scale;
    const zoom = cy.zoom();
    cy.pan({x: cy.width() / 2 - x * zoom, y: cy.height() / 2 - y * zoom});
  };

  const viewport = frame.viewport
    ? (() => {
        const a = project({x: frame.viewport.x1, y: frame.viewport.y1});
        const b = project({x: frame.viewport.x2, y: frame.viewport.y2});
        return {x: a.x, y: a.y, width: Math.max(b.x - a.x, 4), height: Math.max(b.y - a.y, 4)};
      })()
    : null;

  return (
    <svg
      ref={svgRef}
      className="graph-minimap"
      width={width}
      height={height}
      role="img"
      aria-label="Graph overview minimap"
      onMouseDown={event => { dragRef.current = true; navigate(event); }}
      onMouseMove={event => { if (dragRef.current) navigate(event); }}
      onMouseUp={() => { dragRef.current = false; }}
      onMouseLeave={() => { dragRef.current = false; }}
    >
      {ids.map(id => {
        const p = project(frame.positions[id]);
        return <circle key={id} cx={p.x} cy={p.y} r={2.6} className="graph-minimap-node" />;
      })}
      {viewport && <rect {...viewport} className="graph-minimap-viewport" />}
    </svg>
  );
}
