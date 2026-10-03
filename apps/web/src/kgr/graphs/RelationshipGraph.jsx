import React, {useMemo} from 'react';
import {Icon, Tip} from '../../icons.jsx';

export default function RelationshipGraph({edges}) {
  const edgeCounts = useMemo(() => {
    const counts = {};
    for (const e of (edges || [])) counts[e.type] = (counts[e.type] || 0) + 1;
    return Object.entries(counts).sort((a, b) => b[1] - a[1]);
  }, [edges]);

  const maxCount = edgeCounts.length > 0 ? edgeCounts[0][1] : 1;

  return <div className="kgr-relationship-view">
    <section className="panel">
      <div className="panel-heading">
        <div><span className="eyebrow">KGR · RELATIONSHIP ANALYSIS</span>
          <h2>Edge-centric view</h2>
          <p>Relationship types as nodes, connected when they share entity endpoints.</p>
        </div>
      </div>
      <div className="relationship-bars">
        {edgeCounts.map(([type, count]) =>
          <Tip text={`${count} ${type} relationships in view`} key={type}>
            <div tabIndex="0">
              <span>{type}</span>
              <i><b style={{width: `${Math.max(8, (count / maxCount) * 100)}%`}}/></i>
              <strong>{count}</strong>
            </div>
          </Tip>
        )}
      </div>
    </section>
  </div>;
}
