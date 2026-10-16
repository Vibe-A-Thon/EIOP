import React, {useCallback, useMemo, useState} from 'react';
import {Icon} from '../../icons.jsx';

function shortId(value, size = 22) {
  if (!value) return '—';
  return value.length > size ? `${value.slice(0, size - 1)}…` : value;
}

export default function ImpactGraph({api, run, busy, graph, setGraph}) {
  const [centralityResults, setCentralityResults] = useState(null);
  const [anomalyResults, setAnomalyResults] = useState(null);
  const [clusterResults, setClusterResults] = useState(null);

  const runCentrality = useCallback(() => {
    const ids = (graph.nodes || []).slice(0, 50).map(n => n.id);
    if (!ids.length) return;
    run(async () => {
      const result = await api('/api/v1/graph/centrality/full', {
        canonical_ids: ids, algorithms: ['degree', 'betweenness', 'closeness', 'pagerank']
      });
      setCentralityResults(result);
    });
  }, [api, run, graph]);

  const runAnomalies = useCallback(() => {
    run(async () => {
      const result = await api('/api/v1/graph/anomalies', {algorithms: ['degree_zscore'], threshold: 2.0});
      setAnomalyResults(result);
    });
  }, [api, run]);

  const runClusters = useCallback(() => {
    run(async () => {
      const result = await api('/api/v1/graph/cluster', {algorithm: 'label_propagation', resolution: 1.0});
      setClusterResults(result);
    });
  }, [api, run]);

  const topCentral = useMemo(() => {
    if (!centralityResults) return [];
    return Object.entries(centralityResults)
      .map(([id, m]) => ({id, ...m}))
      .sort((a, b) => (b.page_rank || 0) - (a.page_rank || 0))
      .slice(0, 15);
  }, [centralityResults]);

  return <div className="kgr-impact-view">
    <div className="impact-actions-bar">
      <button className="primary-button" disabled={busy} onClick={runCentrality}><Icon name="activity" size={16}/>Compute centrality</button>
      <button className="primary-button" disabled={busy} onClick={runAnomalies}><Icon name="graph" size={16}/>Detect anomalies</button>
      <button className="primary-button" disabled={busy} onClick={runClusters}><Icon name="layers" size={16}/>Find communities</button>
    </div>

    {topCentral.length > 0 && <section className="panel">
      <div className="panel-heading"><div><span className="eyebrow">CENTRALITY LEADERS</span>
        <h2>Top {topCentral.length} by PageRank</h2></div></div>
      <div className="centrality-table">
        <div className="centrality-header"><span>Entity</span><span>Degree</span><span>Betweenness</span><span>Closeness</span><span>PageRank</span></div>
        {topCentral.map(c => <div key={c.id} className="centrality-row">
          <span className="centrality-id" title={c.id}>{shortId(c.canonical_id || c.id, 28)}</span>
          <span>{c.degree}</span>
          <span>{(c.betweenness || 0).toFixed(4)}</span>
          <span>{(c.closeness || 0).toFixed(4)}</span>
          <span className="centrality-pr">{(c.page_rank || 0).toFixed(4)}</span>
        </div>)}
      </div>
    </section>}

    {anomalyResults && <section className="panel">
      <div className="panel-heading"><div><span className="eyebrow">ANOMALIES</span>
        <h2>{anomalyResults.length} outlier{anomalyResults.length !== 1 ? 's' : ''} detected</h2></div></div>
      {anomalyResults.length ? <div className="anomaly-list">{anomalyResults.map((a, i) =>
        <div key={a.canonical_id || i} className="anomaly-row">
          <span className={`anomaly-type ${a.anomaly_type}`}>{a.anomaly_type}</span>
          <strong>{shortId(a.canonical_id, 28)}</strong>
          <span className="anomaly-score">z={a.score?.toFixed(2)}</span>
          <small>{a.details?.degree != null ? `degree: ${a.details.degree}` : ''}</small>
        </div>
      )}</div> : <p className="subtle">No anomalies found at this threshold.</p>}
    </section>}

    {clusterResults && <section className="panel">
      <div className="panel-heading"><div><span className="eyebrow">COMMUNITIES</span>
        <h2>{clusterResults.community_count} communities (modularity {(clusterResults.modularity || 0).toFixed(3)})</h2></div></div>
      <div className="cluster-grid">{(clusterResults.communities || []).slice(0, 20).map((c, i) =>
        <div key={i} className="cluster-card">
          <div className="cluster-header"><strong>Community {c.community_id ?? i}</strong><span className="badge">{c.size ?? c.members?.length ?? 0}</span></div>
          <div className="cluster-members">{(c.members || []).slice(0, 5).map(m =>
            <span key={m} className="cluster-member" title={m}>{shortId(m, 20)}</span>
          )}{(c.members || []).length > 5 && <span className="cluster-more">+{(c.members || []).length - 5} more</span>}</div>
        </div>
      )}</div>
    </section>}

    {!centralityResults && !anomalyResults && !clusterResults && <div className="empty-state">
      <span className="empty-icon"><Icon name="activity" size={22}/></span>
      <strong>Impact analysis</strong><p>Run centrality, anomaly detection, or community analysis using the buttons above.</p>
    </div>}
  </div>;
}
