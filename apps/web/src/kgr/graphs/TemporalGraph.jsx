import React from 'react';
import {Icon} from '../../icons.jsx';
import GraphCanvas from '../../GraphCanvas.jsx';
import SigmaRenderer from '../renderers/SigmaRenderer.jsx';
import TimelineScrubber from '../components/TimelineScrubber.jsx';

const SIGMA_THRESHOLD = 5000;

export default function TemporalGraph({nodes, edges, paths, selectedId, onSelectNode, onExpand, timeRange, onTimeRangeChange}) {
  const useSigma = nodes.length >= SIGMA_THRESHOLD;

  return <div className="explorer-grid">
    <section className="panel graph-panel">
      <div className="panel-heading"><div><span className="eyebrow">KGR · TEMPORAL VIEW</span><h2>Time-filtered graph</h2></div></div>
      {useSigma
        ? <SigmaRenderer nodes={nodes} edges={edges} selectedId={selectedId} onSelectNode={onSelectNode} onExpand={onExpand}/>
        : <GraphCanvas nodes={nodes} edges={edges} paths={paths || []} selectedId={selectedId} onSelectNode={onSelectNode} onExpand={onExpand}/>
      }
      {onTimeRangeChange && <TimelineScrubber nodes={nodes} range={timeRange} onRangeChange={onTimeRangeChange}/>}
    </section>
  </div>;
}
