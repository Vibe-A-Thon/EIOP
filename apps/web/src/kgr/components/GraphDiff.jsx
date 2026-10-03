import React, {useCallback, useMemo, useState} from 'react';
import {Icon} from '../../icons.jsx';

function classifyChanges(diffData) {
  const added = [], removed = [], modified = [], unchanged = [];
  for (const node of diffData?.added_vertices || []) {
    added.push({type: 'vertex', action: 'added', id: node.canonical_id || node.id, label: node.label, data: node});
  }
  for (const node of diffData?.removed_vertices || []) {
    removed.push({type: 'vertex', action: 'removed', id: node.canonical_id || node.id, label: node.label, data: node});
  }
  for (const node of diffData?.modified_vertices || []) {
    modified.push({type: 'vertex', action: 'modified', id: node.canonical_id || node.id, label: node.label, data: node});
  }
  for (const edge of diffData?.added_edges || []) {
    added.push({type: 'edge', action: 'added', id: edge.eid || `${edge.out_cid}-${edge.in_cid}`, label: edge.label, data: edge});
  }
  for (const edge of diffData?.removed_edges || []) {
    removed.push({type: 'edge', action: 'removed', id: edge.eid || `${edge.out_cid}-${edge.in_cid}`, label: edge.label, data: edge});
  }
  return {added, removed, modified, unchanged, total: added.length + removed.length + modified.length};
}

export default function GraphDiff({api, run, busy}) {
  const [fromTs, setFromTs] = useState('');
  const [toTs, setToTs] = useState('');
  const [diffData, setDiffData] = useState(null);
  const [viewMode, setViewMode] = useState('overlay');
  const [filterAction, setFilterAction] = useState('all');

  const loadDiff = useCallback(() => {
    if (!fromTs || !toTs) return;
    run(async () => {
      const result = await api(`/api/v1/graph/diff?from=${encodeURIComponent(fromTs)}&to=${encodeURIComponent(toTs)}`);
      setDiffData(result);
    });
  }, [api, run, fromTs, toTs]);

  const changes = useMemo(() => diffData ? classifyChanges(diffData) : null, [diffData]);

  const filteredChanges = useMemo(() => {
    if (!changes) return [];
    const all = [...changes.added, ...changes.removed, ...changes.modified];
    if (filterAction === 'all') return all;
    return all.filter(c => c.action === filterAction);
  }, [changes, filterAction]);

  return <div className="kgr-graph-diff">
    <section className="panel">
      <div className="panel-heading"><div><span className="eyebrow">GRAPH DIFF</span>
        <h2>Compare graph snapshots</h2></div></div>
      <div className="diff-inputs">
        <label>From: <input type="text" placeholder="ISO timestamp (e.g. 2026-10-01T00:00:00)" value={fromTs}
          onChange={e => setFromTs(e.target.value)} aria-label="From timestamp"/></label>
        <label>To: <input type="text" placeholder="ISO timestamp (e.g. 2026-10-03T00:00:00)" value={toTs}
          onChange={e => setToTs(e.target.value)} aria-label="To timestamp"/></label>
        <button className="primary-button" disabled={busy || !fromTs || !toTs} onClick={loadDiff}>
          <Icon name="graph" size={16}/>Compare</button>
      </div>
      <div className="diff-mode-toggle">
        <button className={viewMode === 'overlay' ? 'active' : ''} onClick={() => setViewMode('overlay')}>Overlay</button>
        <button className={viewMode === 'side-by-side' ? 'active' : ''} onClick={() => setViewMode('side-by-side')}>Side-by-side</button>
      </div>
    </section>

    {changes && <section className="panel">
      <div className="panel-heading"><div><span className="eyebrow">CHANGES</span>
        <h2>{changes.total} changes detected</h2></div></div>
      <div className="diff-summary">
        <div className="diff-stat diff-added"><Icon name="check" size={16}/><strong>{changes.added.length}</strong><span>Added</span></div>
        <div className="diff-stat diff-removed"><Icon name="close" size={16}/><strong>{changes.removed.length}</strong><span>Removed</span></div>
        <div className="diff-stat diff-modified"><Icon name="activity" size={16}/><strong>{changes.modified.length}</strong><span>Modified</span></div>
      </div>
      <div className="diff-filter-row">
        {['all', 'added', 'removed', 'modified'].map(f =>
          <button key={f} className={filterAction === f ? 'active' : ''} onClick={() => setFilterAction(f)}>{f}</button>
        )}
      </div>
      <div className="diff-change-list">
        {filteredChanges.map((c, i) =>
          <div key={c.id || i} className={`diff-change-item diff-${c.action}`}>
            <span className={`diff-badge diff-badge-${c.action}`}>
              {c.action === 'added' ? '+' : c.action === 'removed' ? '−' : '~'}
            </span>
            <span className="diff-type">{c.type}</span>
            <strong>{c.label}</strong>
            <code>{c.id?.length > 30 ? c.id.slice(0, 29) + '…' : c.id}</code>
          </div>
        )}
        {filteredChanges.length === 0 && <p className="subtle">No changes match the current filter.</p>}
      </div>
    </section>}

    {!diffData && <div className="empty-state">
      <span className="empty-icon"><Icon name="graph" size={22}/></span>
      <strong>Graph comparison</strong><p>Enter two timestamps to compare graph state and see structural changes.</p>
    </div>}
  </div>;
}
