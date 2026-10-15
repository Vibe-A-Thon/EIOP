import React, {useEffect, useState} from 'react';
import {Icon} from '../../icons.jsx';

export default function CodePanel({filePath, api, highlightLines, onClose}) {
  const [content, setContent] = useState(null);
  const [language, setLanguage] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  useEffect(() => {
    setContent(null);
    if (!filePath || !api) return;
    let active = true;
    const controller = new AbortController();
    setLoading(true);
    setError(null);
    api(`/api/v1/files/${encodeURIComponent(filePath)}`, undefined, undefined, {signal: controller.signal})
      .then(data => {
        if (!active) return;
        setContent(typeof data === 'string' ? data : data.content || '');
        setLanguage(data.language || filePath.split('.').pop() || '');
        setLoading(false);
      })
      .catch(err => {
        if (!active || err.name === 'AbortError') return;
        setError(err.message);
        setLoading(false);
      });
    return () => {active = false; controller.abort();};
  }, [filePath, api]);

  const lines = (content || '').split('\n');
  const hlSet = new Set(highlightLines || []);

  return <section className="code-panel panel" aria-label="Code viewer">
    <div className="panel-heading">
      <div><span className="eyebrow">CODE VIEWER</span><h2>{filePath || 'No file selected'}</h2></div>
      <button className="icon-button" onClick={onClose} aria-label="Close code panel" title="Close code panel"><Icon name="close"/></button>
    </div>
    {loading && <div className="code-loading">Loading file...</div>}
    {error && <div className="code-error" role="alert">{error}</div>}
    {content != null && <div className="code-content">
      <pre className={`code-block language-${language}`}>{lines.map((line, i) =>
        <div key={i} className={`code-line ${hlSet.has(i + 1) ? 'code-highlight' : ''}`}>
          <span className="code-gutter">{i + 1}</span>
          <span className="code-text">{line}</span>
        </div>
      )}</pre>
    </div>}
    {!filePath && <div className="empty-state">
      <span className="empty-icon"><Icon name="database" size={22}/></span>
      <strong>Code viewer</strong><p>Select a File or CodeSymbol node to view its source code.</p>
    </div>}
  </section>;
}
