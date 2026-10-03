import React, {useCallback, useEffect, useMemo, useState} from 'react';
import {Icon} from '../../icons.jsx';

export default function PRDashboard({api, run, busy, onClose}) {
  const [prData, setPrData] = useState(null);
  const [loading, setLoading] = useState(false);

  const refresh = useCallback(() => {
    setLoading(true);
    run(async () => {
      const result = await api('/api/v1/graph/pr-impact');
      setPrData(result);
      setLoading(false);
    });
  }, [api, run]);

  useEffect(() => { refresh(); }, []);

  const prs = prData?.pull_requests || [];
  const conflicts = prData?.conflicts || [];

  const riskClass = (risk) => risk === 'HIGH' ? 'negative' : risk === 'MEDIUM' ? 'neutral' : 'positive';

  return <div className="pr-dashboard panel" role="dialog" aria-label="PR impact dashboard">
    <div className="panel-heading">
      <div><span className="eyebrow">PR / CHANGE IMPACT</span><h2>Pull request conflict detection</h2></div>
      <div className="panel-heading-right">
        <button className="primary-button" onClick={refresh} disabled={busy || loading}>
          <Icon name="activity" size={16}/>{loading ? 'Loading...' : 'Refresh'}
        </button>
        {onClose && <button className="icon-button" onClick={onClose}><Icon name="close"/></button>}
      </div>
    </div>

    {prs.length > 0 && <section>
      <h3>Open pull requests ({prs.length})</h3>
      <div className="pr-table">
        <div className="pr-header-row">
          <span>Title</span><span>Author</span><span>Communities</span><span>Entities</span>
        </div>
        {prs.map((pr, i) => <div key={pr.mr_id || i} className="pr-row">
          <strong className="pr-title">{pr.title || `PR #${pr.mr_id}`}</strong>
          <span className="pr-author">{pr.author || '—'}</span>
          <span className="pr-communities">{(pr.communities_touched || []).length}</span>
          <span className="pr-entities">{pr.entities_modified || 0}</span>
        </div>)}
      </div>
    </section>}

    {conflicts.length > 0 && <section>
      <h3>Potential conflicts ({conflicts.length})</h3>
      <div className="conflict-matrix">
        {conflicts.map((c, i) => <div key={i} className={`conflict-cell ${riskClass(c.risk)}`}>
          <div className="conflict-header">
            <span className={`risk-badge ${riskClass(c.risk)}`}>{c.risk}</span>
            <strong>{c.overlap_pct != null ? `${(c.overlap_pct * 100).toFixed(0)}% overlap` : 'Overlap detected'}</strong>
          </div>
          <small>PR {c.mr_a} ↔ PR {c.mr_b}</small>
          {c.overlap_communities?.length > 0 && <div className="conflict-communities">
            {c.overlap_communities.map((comm, j) => <span key={j} className="badge">{comm}</span>)}
          </div>}
        </div>)}
      </div>
    </section>}

    {!prData && !loading && <div className="empty-state">
      <span className="empty-icon"><Icon name="activity" size={22}/></span>
      <strong>PR impact analysis</strong>
      <p>Analyzes open pull requests for community overlap and conflict risk.</p>
    </div>}

    {prData && prs.length === 0 && <div className="empty-state">
      <span className="empty-icon"><Icon name="check" size={22}/></span>
      <strong>No open pull requests</strong>
      <p>No open PRs/MRs found for conflict analysis.</p>
    </div>}
  </div>;
}
