import React from 'react';
import GraphCanvas from '../../GraphCanvas.jsx';
import SigmaRenderer from '../renderers/SigmaRenderer.jsx';

const SIGMA_THRESHOLD = 5000;

export default function KnowledgeGraph({nodes, edges, paths, selectedId, selectedEdgeId, onSelectNode, onSelectEdge, onExpand, renderProgress, renderedCount, totalCount}) {
  const useSigma = nodes.length >= SIGMA_THRESHOLD;

  return <section className="panel graph-panel">
    <div className="panel-heading">
      <div><span className="eyebrow">KGR · KNOWLEDGE GRAPH</span><h2>Interactive entity-relationship map</h2></div>
      <span className="count-badge">{nodes.length}{nodes.length < totalCount ? `/${totalCount}` : ''} entities · {edges.length} relationships</span>
      {useSigma && <span className="renderer-badge">WebGL</span>}
    </div>
    {renderProgress && <div className="render-progress-bar"><div className="render-progress-fill" style={{width: `${(renderedCount / Math.max(totalCount, 1)) * 100}%`}}/><span>{renderProgress}</span></div>}
    {useSigma
      ? <SigmaRenderer nodes={nodes} edges={edges} selectedId={selectedId} onSelectNode={onSelectNode} onSelectEdge={onSelectEdge} onExpand={onExpand}/>
      : <GraphCanvas nodes={nodes} edges={edges} paths={paths || []} selectedId={selectedId} selectedEdgeId={selectedEdgeId} onSelectNode={onSelectNode} onSelectEdge={onSelectEdge} onExpand={onExpand}/>
    }
  </section>;
}
