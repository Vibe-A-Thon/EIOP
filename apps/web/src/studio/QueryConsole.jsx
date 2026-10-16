import React, {useEffect, useState} from 'react';
import {Icon} from '../icons.jsx';

const HISTORY_KEY = 'eoip-studio-query-history';
const LANGUAGES = [
  {id: 'eql', label: 'EQL', hint: 'EOIP Query Language via POST /api/v1/query/eql'},
  {id: 'eoql', label: 'EOQL', hint: 'POST /api/v1/query/language'},
  {id: 'osql', label: 'OSQL', hint: 'POST /api/v1/query/language'},
  {id: 'semantic', label: 'Semantic QL', hint: 'POST /api/v1/query/language'},
];

function loadHistory() {
  try {
    const parsed = JSON.parse(sessionStorage.getItem(HISTORY_KEY) || '[]');
    return Array.isArray(parsed) ? parsed : [];
  } catch {
    return [];
  }
}

function collectWarnings(data) {
  if (!data || typeof data !== 'object') return [];
  const warnings = [];
  for (const key of ['warnings', 'safety', 'guards', 'notices']) {
    const value = data[key];
    if (Array.isArray(value)) warnings.push(...value.map(String));
  }
  if (data.truncated || data.partial) warnings.push('Result was truncated or partially fulfilled by the engine.');
  if (data.max_results_exceeded) warnings.push('Result exceeded the maximum result size and was cut off.');
  return [...new Set(warnings)];
}

export default function QueryConsole({api, run, busy}) {
  const [language, setLanguage] = useState('eql');
  const [query, setQuery] = useState('MATCH (n:Requirement) RETURN n LIMIT 10');
  const [result, setResult] = useState(null);
  const [latency, setLatency] = useState(null);
  const [error, setError] = useState('');
  const [warnings, setWarnings] = useState([]);
  const [history, setHistory] = useState(loadHistory);

  useEffect(() => {sessionStorage.setItem(HISTORY_KEY, JSON.stringify(history.slice(0, 50)));}, [history]);

  function execute() {
    if (!query.trim() || !api) return;
    run(async () => {
      const started = performance.now();
      setError('');
      try {
        const data = language === 'eql'
          ? await api('/api/v1/query/eql', {query})
          : await api('/api/v1/query/language', {language, query});
        setResult(data);
        setWarnings(collectWarnings(data));
        setLatency(Math.round(performance.now() - started));
        setHistory(list => [{id: `${Date.now()}`, language, query, latency_ms: Math.round(performance.now() - started), at: new Date().toISOString()}, ...list.filter(item => item.query !== query)].slice(0, 50));
      } catch (exception) {
        setResult(null);
        setWarnings([]);
        setLatency(Math.round(performance.now() - started));
        setError(exception.message || 'Query failed.');
      }
    });
  }

  return <div>
    <section className="studio-panel">
      <h3><Icon name="terminal" size={15}/> Query</h3>
      <div className="studio-row" style={{marginBottom: 10}}>
        {LANGUAGES.map(item => <button key={item.id} type="button"
          className={language === item.id ? 'primary-button' : 'ghost-button'}
          title={item.hint}
          onClick={() => setLanguage(item.id)}>
          {item.label}
        </button>)}
      </div>
      <div className="studio-field">
        <span>{language.toUpperCase()} statement</span>
        <textarea value={query} onChange={event => setQuery(event.target.value)}
          onKeyDown={event => { if (event.key === 'Enter' && (event.ctrlKey || event.metaKey)) execute(); }}
          placeholder={language === 'eql' ? 'MATCH (n:Requirement) RETURN n LIMIT 10' : 'Enter query…'}
          aria-label="Query statement"/>
      </div>
      <div className="studio-row">
        <button type="button" className="primary-button" onClick={execute} disabled={busy || !query.trim() || !api}>
          {busy ? <span className="spinner small"/> : <Icon name="arrow" size={15}/>} Run query
        </button>
        <span className="studio-hint" style={{margin: 0}}>Ctrl+Enter to run. Guarded execution — destructive statements are rejected by the API.</span>
      </div>
    </section>
    {error && <div className="studio-error" role="alert"><Icon name="warning" size={16}/><span>{error}</span></div>}
    {warnings.map((warning, index) => <div key={index} className="studio-warn"><Icon name="shield" size={16}/><span>{warning}</span></div>)}
    <div className="studio-grid">
      <section className="studio-panel" aria-label="Query history">
        <h3><Icon name="clock" size={15}/> History</h3>
        {history.length === 0 && <div className="studio-empty"><strong>No queries yet</strong>Run a query to build session history.</div>}
        <ul className="studio-list">
          {history.slice(0, 15).map(item => <li key={item.id}>
            <button type="button" className="studio-chip" title={`${item.language}: ${item.query}`}
              onClick={() => { setLanguage(item.language); setQuery(item.query); }}>
              {item.query.length > 42 ? `${item.query.slice(0, 41)}…` : item.query}
            </button>
            <span className="studio-latency">{item.latency_ms} ms</span>
          </li>)}
        </ul>
        {history.length > 0 && <button type="button" className="ghost-button" style={{marginTop: 8}} onClick={() => setHistory([])}>Clear history</button>}
      </section>
      <section className="studio-panel" aria-label="Query result">
        <h3><Icon name="document" size={15}/> Result {latency !== null && <span className="studio-latency">· {latency} ms</span>}</h3>
        {result === null && !error && <div className="studio-empty"><strong>No result</strong>Run a query to see JSON output here.</div>}
        <pre className="studio-json">{result !== null ? JSON.stringify(result, null, 2) : ''}</pre>
      </section>
    </div>
  </div>;
}
