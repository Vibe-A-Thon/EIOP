import React from 'react';
import {Icon} from '../../icons.jsx';

function shortId(value, size = 22) {
  if (!value) return '—';
  return value.length > size ? `${value.slice(0, size - 1)}…` : value;
}

export default function SimilarityPanel({similarNodes, onSearch, busy}) {
  const sim = similarNodes || [];

  return <div className="kgr-similarity-panel">
    <p className="subtle">Structurally similar nodes based on shared neighbors (Jaccard index).</p>
    {sim.length > 0 ? <div className="similarity-list">{sim.map((s, i) =>
      <div key={s.canonical_id || i} className="similarity-row">
        <span className="similarity-rank">{i + 1}</span>
        <div className="similarity-info">
          <strong>{shortId(s.canonical_id, 36)}</strong>
          <small>{s.common_neighbors ?? 0} common neighbors</small>
        </div>
        <span className="similarity-score">{(s.score ?? 0).toFixed(3)}</span>
      </div>
    )}</div> : <div className="inline-notice"><Icon name="info"/>Click "Find similar" to compute similarity scores.</div>}
    <button className="primary-button" disabled={busy} onClick={onSearch}><Icon name="users"/>Find similar nodes</button>
  </div>;
}
