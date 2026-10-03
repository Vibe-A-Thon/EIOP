import React, {useCallback, useEffect, useState} from 'react';
import {Icon} from '../../icons.jsx';

function escapeHtml(str) {
  return str.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
}

export default function CodePanel({filePath, apiBase, highlightLines, onSymbolClick, onClose}) {
  const [content, setContent] = useState(null);
  const [language, setLanguage] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  useEffect(() => {
    if (!filePath || !apiBase) return;
    setLoading(true);
    setError(null);
    fetch(`${apiBase}/api/v1/files/${encodeURIComponent(filePath)}`)
      .then(r => {
        if (!r.ok) throw new Error(`Failed to load file: ${r.status}`);
        return r.json();
      })
      .then(data => {
        setContent(data.content || '');
        setLanguage(data.language || filePath.split('.').pop() || '');
        setLoading(false);
      })
      .catch(err => {
        setError(err.message);
        setLoading(false);
      });
  }, [filePath, apiBase]);

  const lines = (content || '').split('\n');
  const hlSet = new Set(highlightLines || []);

  return <section className="code-panel panel" aria-label="Code viewer">
    <div className="panel-heading">
      <div><span className="eyebrow">CODE VIEWER</span><h2>{filePath || 'No file selected'}</h2></div>
      <button className="icon-button" onClick={onClose} title="Close code panel"><Icon name="close"/></button>
    </div>
    {loading && <div className="code-loading">Loading file...</div>}
    {error && <div className="code-error">{error}</div>}
    {content != null && <div className="code-content">
      <pre className={`code-block language-${language}`}>{lines.map((line, i) =>
        <div key={i} className={`code-line ${hlSet.has(i + 1) ? 'code-highlight' : ''}`}>
          <span className="code-gutter">{i + 1}</span>
          <span className="code-text" dangerouslySetInnerHTML={{__html: escapeHtml(line)}}/>
        </div>
      )}</pre>
    </div>}
    {!filePath && <div className="empty-state">
      <span className="empty-icon"><Icon name="database" size={22}/></span>
      <strong>Code viewer</strong><p>Select a File or CodeSymbol node to view its source code.</p>
    </div>}
  </section>;
}
