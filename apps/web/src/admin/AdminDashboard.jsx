import React, {useCallback, useEffect, useRef, useState} from 'react';
import {Icon, Tip} from '../icons.jsx';

const POLL_MS = 5000;

function parseLabels(rest) {
  const labels = {};
  const re = /(\w+)="((?:[^"\\]|\\.)*)"/g;
  let match;
  while ((match = re.exec(rest))) labels[match[1]] = match[2];
  return labels;
}

// Parse the Prometheus text exposition into {counters, histograms} summaries.
export function parsePrometheus(text) {
  const counters = {}; // key: `${method} ${path}` -> {statuses: {status: count}, total}
  const latency = {count: 0, sum: 0, buckets: []}; // buckets: {le, count}
  const byPath = {};
  for (const rawLine of String(text || '').split(/\r?\n/)) {
    const line = rawLine.trim();
    if (!line || line.startsWith('#')) continue;
    const open = line.indexOf('{');
    const name = open === -1 ? line.split(/\s+/)[0] : line.slice(0, open);
    const value = Number(line.slice(line.lastIndexOf('}') + 1).trim());
    if (!Number.isFinite(value)) continue;
    if (name === 'http_requests_total') {
      const labels = parseLabels(line.slice(open + 1, line.lastIndexOf('}')));
      const key = `${labels.method || '?'} ${labels.path || 'unknown'}`;
      counters[key] = counters[key] || {method: labels.method, path: labels.path, statuses: {}, total: 0};
      counters[key].statuses[labels.status || '?'] = (counters[key].statuses[labels.status || '?'] || 0) + value;
      counters[key].total += value;
    } else if (name === 'http_request_duration_seconds_bucket') {
      const labels = parseLabels(line.slice(open + 1, line.lastIndexOf('}')));
      const le = Number(labels.le);
      if (Number.isFinite(le)) {
        latency.buckets.push({le, count: value});
        const pathKey = `${labels.method || '?'} ${labels.path || 'unknown'}`;
        byPath[pathKey] = byPath[pathKey] || {buckets: [], count: 0};
        byPath[pathKey].buckets.push({le, count: value});
      }
    } else if (name === 'http_request_duration_seconds_sum') {
      latency.sum += value;
    } else if (name === 'http_request_duration_seconds_count') {
      latency.count += value;
    }
  }
  latency.buckets.sort((a, b) => a.le - b.le);
  return {counters, latency, byPath};
}

// Smallest bucket whose cumulative count reaches ratio of total observations.
export function histogramQuantile(buckets, ratio, totalCount) {
  if (!buckets.length || !totalCount) return null;
  for (const bucket of buckets) {
    if (bucket.count >= ratio * totalCount) return bucket.le;
  }
  return buckets[buckets.length - 1].le;
}

function Pill({status = 'UNKNOWN'}) {
  const normalized = String(status).toLowerCase();
  const positive = ['ready', 'running', 'succeeded', 'passed', 'ok', 'complete', '2'].some(word => normalized.includes(word));
  const negative = ['failed', 'error', 'denied', '5', 'unavailable'].some(word => normalized.includes(word));
  return <span className={`status-pill ${positive ? 'positive' : negative ? 'negative' : 'neutral'}`}><span className="status-dot"/>{String(status).replaceAll('_', ' ')}</span>;
}

function EmptyState({icon = 'activity', title, children}) {
  return <div className="empty-state"><span className="empty-icon"><Icon name={icon} size={22}/></span><strong>{title}</strong><p>{children}</p></div>;
}

export default function AdminDashboard({api, run, busy}) {
  const [metrics, setMetrics] = useState(null);
  const [stats, setStats] = useState(null);
  const [jobs, setJobs] = useState([]);
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(true);
  const [auto, setAuto] = useState(true);
  const [updatedAt, setUpdatedAt] = useState(null);
  const timer = useRef(null);

  const load = useCallback(async () => {
    setError('');
    try {
      const [metricsText, nextStats, nextJobs] = await Promise.all([
        api('/metrics', undefined, 'GET').catch(exception => {
          if (exception.message && exception.message.includes('404')) return null;
          throw exception;
        }),
        api('/api/v1/admin/stats').catch(() => null),
        api('/api/v1/admin/jobs').catch(() => []),
      ]);
      setMetrics(metricsText ? parsePrometheus(metricsText) : null);
      setStats(nextStats);
      setJobs(Array.isArray(nextJobs) ? nextJobs : nextJobs?.jobs || []);
      setUpdatedAt(new Date());
    } catch (exception) {
      setError(exception.message || 'Live metrics could not be loaded.');
    } finally {
      setLoading(false);
    }
  }, [api]);

  useEffect(() => {
    load();
    return () => clearInterval(timer.current);
  }, [load]);

  useEffect(() => {
    clearInterval(timer.current);
    if (auto) timer.current = setInterval(() => load().catch(() => {}), POLL_MS);
    return () => clearInterval(timer.current);
  }, [auto, load]);

  const counterRows = Object.values(metrics?.counters || {}).sort((a, b) => b.total - a.total).slice(0, 15);
  const totalRequests = counterRows.reduce((sum, row) => sum + row.total, 0);
  const p50 = metrics ? histogramQuantile(metrics.latency.buckets, 0.5, metrics.latency.count) : null;
  const p95 = metrics ? histogramQuantile(metrics.latency.buckets, 0.95, metrics.latency.count) : null;
  const errorCount = counterRows.reduce((sum, row) => sum + Object.entries(row.statuses).filter(([status]) => status.startsWith('5') || status.startsWith('4')).reduce((inner, [, count]) => inner + count, 0), 0);
  const activeJobs = jobs.filter(job => ['PENDING', 'RUNNING', 'HELD'].includes(job.status));
  const workerStatus = stats?.worker?.status || 'UNAVAILABLE';
  const healthOk = workerStatus === 'RUNNING' || workerStatus === 'READY' || workerStatus === 'IDLE';

  const fmtMs = seconds => seconds === null || seconds === undefined ? '—' : seconds < 1 ? `${Math.round(seconds * 1000)} ms` : `${seconds.toFixed(2)} s`;

  return <>
    <section className="panel span-3">
      <div className="panel-heading"><div><span className="eyebrow">LIVE OBSERVABILITY</span><h2>Real-time platform metrics</h2><p>Polls <code>/metrics</code> and <code>/api/v1/admin/stats</code> every 5 seconds while auto-refresh is on.</p></div>
        <div className="panel-tools">
          <span className="context-chip"><Icon name="clock" size={14}/>{updatedAt ? `Updated ${updatedAt.toLocaleTimeString()}` : 'Not loaded yet'}</span>
          <button className="secondary-button" onClick={() => run(load)} disabled={busy}><Icon name="refresh" size={15}/>Refresh</button>
          <label className="toggle" title="Toggle automatic 5 second polling"><input type="checkbox" checked={auto} onChange={event => setAuto(event.target.checked)}/><span/>Auto-refresh</label>
        </div></div>
      {error && <div className="inline-notice warning" role="alert"><Icon name="warning"/>{error} — the last successful snapshot is shown where available.</div>}
      {loading && <div className="inline-notice" role="status"><span className="spinner"/>Loading live metrics…</div>}
      {!loading && !metrics && !stats && !error && <EmptyState icon="activity" title="No live metrics returned">The Prometheus endpoint and admin stats did not return data for this deployment.</EmptyState>}
      {metrics && <div className="metrics-grid">
        <article className="metric-card tone-violet" tabIndex="0"><span className="metric-icon"><Icon name="activity" size={20}/></span><div><span className="eyebrow">HTTP REQUESTS</span><strong>{totalRequests.toLocaleString()}</strong><small>Across {counterRows.length} tracked routes</small></div></article>
        <article className="metric-card tone-blue" tabIndex="0"><span className="metric-icon"><Icon name="clock" size={20}/></span><div><span className="eyebrow">p95 LATENCY</span><strong>{fmtMs(p95)}</strong><small>p50 {fmtMs(p50)} · from histogram buckets</small></div></article>
        <article className={`metric-card ${errorCount ? 'tone-coral' : 'tone-mint'}`} tabIndex="0"><span className="metric-icon"><Icon name={errorCount ? 'warning' : 'check'} size={20}/></span><div><span className="eyebrow">ERROR RESPONSES</span><strong>{errorCount.toLocaleString()}</strong><small>4xx / 5xx responses observed</small></div></article>
        <article className={`metric-card ${healthOk ? 'tone-mint' : 'tone-coral'}`} tabIndex="0"><span className="metric-icon"><Icon name="shield" size={20}/></span><div><span className="eyebrow">HEALTH</span><strong>{workerStatus}</strong><small>Ingestion worker · {activeJobs.length} active job{activeJobs.length === 1 ? '' : 's'}</small></div></article>
      </div>}
    </section>
    {metrics && <section className="panel span-2"><div className="panel-heading"><div><span className="eyebrow">REQUEST COUNTERS</span><h2>Top routes</h2><p>Counters grouped by method, path, and response status.</p></div><span className="count-badge">{totalRequests.toLocaleString()} requests</span></div>
      {counterRows.length ? <div className="table-wrap"><table><thead><tr><th>Route</th><th>Statuses</th><th>Total</th></tr></thead><tbody>{counterRows.map(row => <tr key={`${row.method} ${row.path}`}><td><code>{row.method} {row.path}</code></td><td>{Object.entries(row.statuses).map(([status, count]) => <Tip text={`${count} response(s)`} key={status}><span className="badge" style={{marginRight: 6}}>{status} · {count}</span></Tip>)}</td><td><strong>{row.total}</strong></td></tr>)}</tbody></table></div> : <EmptyState icon="activity" title="No request counters yet">Counters appear after the API serves its first tracked request.</EmptyState>}</section>}
    <section className="panel"><div className="panel-heading"><div><span className="eyebrow">JOB STATUS</span><h2>Worker jobs</h2></div><span className="count-badge">{jobs.length} total</span></div>
      {jobs.length ? <div className="table-wrap"><table><thead><tr><th>Kind</th><th>Status</th><th>Created</th></tr></thead><tbody>{jobs.slice(0, 12).map(job => <tr key={job.job_id}><td><strong>{String(job.kind || 'JOB').replaceAll('_', ' ')}</strong><small style={{display: 'block'}} title={job.job_id}>{job.job_id}</small></td><td><Pill status={job.status}/></td><td>{job.created_at ? new Date(job.created_at).toLocaleString() : '—'}</td></tr>)}</tbody></table></div> : <EmptyState icon="clock" title="No ingestion jobs yet">Jobs appear once a demo load or source import is queued.</EmptyState>}</section>
  </>;
}
