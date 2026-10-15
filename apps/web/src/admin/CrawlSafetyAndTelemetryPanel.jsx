import React, {useCallback, useEffect, useState} from 'react';
import {Icon} from '../icons.jsx';

export default function CrawlSafetyAndTelemetryPanel({api}) {
  const [sources, setSources] = useState([]);
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const load = useCallback(async () => {
    setLoading(true); setError('');
    try {
      const data = await api('/api/v1/sources');
      if (!Array.isArray(data)) throw new Error('Source registry returned an unsupported response.');
      setSources(data.filter(source => ['web', 'crawler'].includes(source.source_type)));
    } catch (exception) {setSources([]); setError(exception.message || 'Crawl sources could not be loaded.');}
    finally {setLoading(false);}
  }, [api]);
  useEffect(() => {load();}, [load]);
  return <section className="panel" aria-labelledby="crawl-sources-title">
    <div className="panel-heading"><h2 id="crawl-sources-title">Crawl sources</h2>
      <button className="secondary-button" onClick={load} disabled={loading}><Icon name="refresh"/>Refresh sources</button></div>
    {loading && <p role="status">Loading crawl sources...</p>}
    {error && <p role="alert" className="resource-error">{error}</p>}
    {!loading && !error && !sources.length && <p>No crawl sources are registered.</p>}
    {!!sources.length && <div className="table-wrap"><table><thead><tr><th>Source</th><th>Health</th><th>Enabled</th></tr></thead>
      <tbody>{sources.map(source => <tr key={source.source_id}><td>{source.name || source.source_id}</td><td>{source.health || 'Unknown'}</td><td>{source.enabled ? 'Yes' : 'No'}</td></tr>)}</tbody></table></div>}
    <p className="inline-notice" role="status">Crawl policy and telemetry settings are unavailable here. No policy changes have been applied.</p>
  </section>;
}
