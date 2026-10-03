import React, {useCallback, useEffect, useState} from 'react';
import {Icon} from '../../icons.jsx';

function HealthWidget({title, value, unit, status, description, icon}) {
  const statusClass = status === 'good' ? 'positive' : status === 'warning' ? 'neutral' : status === 'critical' ? 'negative' : '';
  return <div className={`health-widget ${statusClass}`}>
    <div className="health-widget-header">
      <Icon name={icon || 'check'} size={18}/>
      <span className="eyebrow">{title}</span>
    </div>
    <div className="health-widget-value">
      <strong>{value != null ? value : '—'}</strong>
      {unit && <span className="health-unit">{unit}</span>}
    </div>
    <div className={`status-pill ${statusClass}`}><span className="status-dot"/>{status || 'unknown'}</div>
    {description && <small className="health-desc">{description}</small>}
  </div>;
}

function ProgressWidget({title, value, max, icon}) {
  const pct = max > 0 ? (value / max) * 100 : 0;
  const status = pct > 80 ? 'good' : pct > 50 ? 'warning' : 'critical';
  const statusClass = status === 'good' ? 'positive' : status === 'warning' ? 'neutral' : 'negative';
  return <div className={`health-widget ${statusClass}`}>
    <div className="health-widget-header"><Icon name={icon || 'check'} size={18}/><span className="eyebrow">{title}</span></div>
    <div className="health-progress-bar"><div className="health-progress-fill" style={{width: `${pct}%`}}/></div>
    <div className="health-widget-value"><strong>{pct.toFixed(1)}%</strong></div>
  </div>;
}

export default function GraphHealth({api, run, busy}) {
  const [stats, setStats] = useState(null);
  const [anomalyCount, setAnomalyCount] = useState(null);
  const [components, setComponents] = useState(null);
  const [orphaned, setOrphaned] = useState(null);
  const [stale, setStale] = useState(null);
  const [loading, setLoading] = useState(false);

  const refresh = useCallback(() => {
    setLoading(true);
    run(async () => {
      const [s, a, c, o, st] = await Promise.all([
        api('/api/v1/graph/statistics').catch(() => null),
        api('/api/v1/graph/anomalies', {algorithms: ['degree_zscore'], threshold: 2.0}).catch(() => []),
        api('/api/v1/graph/components', {limit: 5}).catch(() => null),
        api('/api/v1/graph/orphaned').catch(() => null),
        api('/api/v1/graph/stale?threshold_hours=168').catch(() => null),
      ]);
      setStats(s);
      setAnomalyCount(Array.isArray(a) ? a.length : 0);
      setComponents(c);
      setOrphaned(o);
      setStale(st);
      setLoading(false);
    });
  }, [api, run]);

  useEffect(() => { refresh(); }, []);

  const vertexCount = stats?.vertex_count || 0;
  const edgeCount = stats?.edge_count || 0;
  const density = stats?.density || 0;
  const componentCount = components?.total_components || 0;
  const orphanedCount = orphaned?.count || 0;
  const staleCount = stale?.count || 0;

  return <div className="kgr-graph-health">
    <section className="panel">
      <div className="panel-heading"><div><span className="eyebrow">GRAPH HEALTH DASHBOARD</span>
        <h2>System health & quality metrics</h2></div>
        <button className="primary-button" onClick={refresh} disabled={busy || loading}>
          <Icon name="activity" size={16}/>{loading ? 'Loading...' : 'Refresh'}
        </button>
      </div>
    </section>

    <div className="health-grid">
      <HealthWidget title="VERTICES" value={vertexCount} icon="database"
        status={vertexCount > 0 ? 'good' : 'critical'}
        description={`${stats?.vertex_label_count || 0} entity types`}/>
      <HealthWidget title="EDGES" value={edgeCount} icon="link"
        status={edgeCount > 0 ? 'good' : 'critical'}
        description={`${stats?.edge_label_count || 0} relationship types`}/>
      <HealthWidget title="DENSITY" value={(density * 100).toFixed(4)} unit="%" icon="graph"
        status={density > 0.01 ? 'good' : density > 0 ? 'warning' : 'critical'}
        description="Graph connectivity vs theoretical max"/>
      <HealthWidget title="COMPONENTS" value={componentCount} icon="layers"
        status={componentCount === 1 ? 'good' : componentCount <= 3 ? 'warning' : 'critical'}
        description={componentCount === 1 ? 'Fully connected' : `${componentCount} disconnected subgraphs`}/>
      <HealthWidget title="ANOMALIES" value={anomalyCount} icon="activity"
        status={anomalyCount === 0 ? 'good' : anomalyCount <= 3 ? 'warning' : 'critical'}
        description={anomalyCount === 0 ? 'No outliers detected' : `${anomalyCount} degree z-score outliers`}/>
      <HealthWidget title="AVG DEGREE" value={vertexCount > 0 ? ((edgeCount * 2) / vertexCount).toFixed(1) : '—'} icon="graph"
        status={vertexCount > 0 && (edgeCount * 2 / vertexCount) >= 2 ? 'good' : 'warning'}
        description="Average connections per entity"/>
      <HealthWidget title="ORPHANED" value={orphanedCount} icon="focus"
        status={orphanedCount === 0 ? 'good' : orphanedCount <= 5 ? 'warning' : 'critical'}
        description={orphanedCount === 0 ? 'No unreferenced entities' : `${orphanedCount} entities with zero incoming edges`}/>
      <HealthWidget title="STALE" value={staleCount} icon="clock"
        status={staleCount === 0 ? 'good' : staleCount <= 10 ? 'warning' : 'critical'}
        description={staleCount === 0 ? 'All entities recently updated' : `${staleCount} entities not updated in 7+ days`}/>
      {vertexCount > 0 && <ProgressWidget title="CONNECTIVITY" value={vertexCount - orphanedCount} max={vertexCount} icon="graph"/>}
    </div>

    {orphaned && orphaned.orphaned?.length > 0 && <section className="panel">
      <div className="panel-heading"><div><span className="eyebrow">ORPHANED ENTITIES</span>
        <h2>{orphanedCount} unreferenced entities</h2>
        <p>Entities with zero incoming edges — potential dead code or missing relationships.</p>
      </div></div>
      <div className="health-entity-list">{orphaned.orphaned.slice(0, 20).map((o, i) =>
        <div key={o.canonical_id || i} className="health-entity-row">
          <span className="type-dot" style={{background: '#ec6b76'}}/><strong>{o.canonical_id}</strong>
          <span className="badge">{o.details?.label}</span>
          <small>out-degree: {o.details?.out_degree || 0}</small>
        </div>
      )}{orphanedCount > 20 && <div className="health-entity-more">+{orphanedCount - 20} more orphaned entities</div>}</div>
    </section>}

    {stale && stale.stale?.length > 0 && <section className="panel">
      <div className="panel-heading"><div><span className="eyebrow">STALE ENTITIES</span>
        <h2>{staleCount} stale entities</h2>
        <p>Entities not updated within the last 7 days — may need re-ingestion.</p>
      </div></div>
      <div className="health-entity-list">{stale.stale.slice(0, 20).map((s, i) =>
        <div key={s.canonical_id || i} className="health-entity-row">
          <span className="type-dot" style={{background: '#df9d23'}}/><strong>{s.canonical_id}</strong>
          <span className="badge">{s.details?.label}</span>
          <small>last seen: {s.details?.last_seen || 'unknown'}</small>
        </div>
      )}{staleCount > 20 && <div className="health-entity-more">+{staleCount - 20} more stale entities</div>}</div>
    </section>}

    {!stats && !loading && <div className="empty-state">
      <span className="empty-icon"><Icon name="activity" size={22}/></span>
      <strong>Health dashboard</strong><p>Click Refresh to compute graph health metrics.</p>
    </div>}
  </div>;
}
