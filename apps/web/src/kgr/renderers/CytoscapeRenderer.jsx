import React from 'react';
import GraphCanvas, {palette} from '../../GraphCanvas.jsx';

export {palette};

export default function CytoscapeRenderer({
  nodes, edges, paths, selectedId, selectedEdgeId, onSelectNode, onSelectEdge,
  onExpand, onContextMenu, layout, onLayoutChange,
}) {
  return <GraphCanvas
    nodes={nodes}
    edges={edges}
    paths={paths || []}
    selectedId={selectedId}
    selectedEdgeId={selectedEdgeId}
    onSelectNode={onSelectNode}
    onSelectEdge={onSelectEdge}
    onExpand={onExpand}
    onContextMenu={onContextMenu}
    layout={layout}
    onLayoutChange={onLayoutChange}
  />;
}
