import React, {useCallback, useState} from 'react';
import {Icon} from '../../icons.jsx';

const QUICK_ACTIONS = [
  {label: 'Explain this cluster', query: 'Explain the current community cluster — what entities does it contain and why are they grouped?'},
  {label: 'What would break?', query: 'If the selected entity were removed, what would break? Identify downstream impact and orphaned entities.'},
  {label: 'Find surprising connections', query: 'Find the most surprising or unexpected connections in the current graph view.'},
  {label: 'Summarize graph health', query: 'Give a health assessment of the current graph: completeness, evidence coverage, anomalies.'},
  {label: 'Root cause analysis', query: 'Trace upstream dependencies from the selected entity to identify potential root causes.'},
];

function formatResponse(result) {
  if (!result) return {text: 'No response available.', pattern: null, agent: null, confidence: null};
  return {
    text: result.answer || result.text || result.explanation || JSON.stringify(result),
    pattern: result.rag_pattern || result.pattern || null,
    agent: result.agent_type || result.agent || null,
    confidence: result.confidence != null ? result.confidence : null,
    highlights: result.highlight_ids || result.highlights || [],
    actions: result.actions || [],
  };
}

export default function AIExplorer({api, run, busy, selected, graph, onHighlight, onClose}) {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');

  const sendQuery = useCallback((query) => {
    if (!query.trim()) return;
    const userMsg = {role: 'user', text: query, ts: Date.now()};
    setMessages(m => [...m, userMsg]);
    setInput('');

    run(async () => {
      try {
        const result = await api('/api/v1/rag/query', {
          query,
          context: {
            selected_id: selected?.id,
            node_count: (graph?.nodes || []).length,
            edge_count: (graph?.edges || []).length,
          },
        });
        const formatted = formatResponse(result);
        setMessages(m => [...m, {role: 'assistant', ...formatted, ts: Date.now()}]);
        if (formatted.highlights?.length && onHighlight) {
          onHighlight(formatted.highlights);
        }
      } catch (err) {
        const fallbackResult = structuredFallback(query, graph, selected);
        setMessages(m => [...m, {role: 'assistant', ...fallbackResult, ts: Date.now()}]);
      }
    });
  }, [api, run, selected, graph, onHighlight]);

  const handleSubmit = (e) => {
    e.preventDefault();
    sendQuery(input);
  };

  return <div className="kgr-ai-explorer">
    <div className="ai-header">
      <h3 style={{margin: 0, fontSize: 14}}>AI Explorer</h3>
      <div style={{display: 'flex', gap: 4, alignItems: 'center'}}>
        {busy && <span style={{fontSize: 11, color: 'var(--muted)'}}>Thinking...</span>}
        <button className="icon-button" onClick={onClose}><Icon name="close"/></button>
      </div>
    </div>

    <div className="ai-quick-actions">
      {QUICK_ACTIONS.map((a, i) => <button key={i} onClick={() => sendQuery(a.query)}>{a.label}</button>)}
    </div>

    <div className="ai-messages">
      {messages.length === 0 && <div style={{textAlign: 'center', color: 'var(--muted)', padding: 20, fontSize: 12}}>
        Ask a question about the graph or use a quick action above.
      </div>}
      {messages.map((msg, i) => <div key={i} className={`ai-message ${msg.role}`}>
        <div>{msg.text}</div>
        {msg.pattern && <div style={{fontSize: 10, color: 'var(--muted)', marginTop: 4}}>RAG: {msg.pattern}</div>}
        {msg.agent && <div style={{fontSize: 10, color: 'var(--muted)'}}>Agent: {msg.agent}</div>}
        {msg.confidence != null && <div style={{fontSize: 10, color: 'var(--muted)'}}>Confidence: {(msg.confidence * 100).toFixed(0)}%</div>}
      </div>)}
    </div>

    <form className="ai-input" onSubmit={handleSubmit}>
      <input type="text" value={input} onChange={e => setInput(e.target.value)} placeholder="Ask about the graph..." disabled={busy}/>
      <button className="toolbar-button" type="submit" disabled={busy || !input.trim()}><Icon name="graph" size={14}/></button>
    </form>
  </div>;
}

function structuredFallback(query, graph, selected) {
  const nodes = graph?.nodes || [];
  const edges = graph?.edges || [];
  const q = query.toLowerCase();

  if (q.includes('health') || q.includes('summary')) {
    const orphaned = nodes.filter(n => !edges.some(e => e.to_id === n.id)).length;
    const evidenced = edges.filter(e => e.properties?.source_ref || e.properties?.evidence_key).length;
    return {
      text: `Graph has ${nodes.length} nodes and ${edges.length} edges. ${orphaned} orphaned entities. Evidence coverage: ${edges.length ? ((evidenced / edges.length) * 100).toFixed(0) : 0}%.`,
      pattern: 'structured_fallback', confidence: 0.8,
    };
  }

  if (q.includes('break') || q.includes('impact') || q.includes('remove')) {
    if (selected) {
      const affected = edges.filter(e => e.from_id === selected.id || e.to_id === selected.id).length;
      return {
        text: `Removing ${selected.properties?.name || selected.id} would affect ${affected} direct relationships. Use the What-If tab for full simulation.`,
        pattern: 'structured_fallback', confidence: 0.7,
      };
    }
    return {text: 'Select an entity first, then ask about its impact.', pattern: 'structured_fallback', confidence: 0.9};
  }

  if (q.includes('surprising') || q.includes('unexpected')) {
    return {text: `Use the Surprises panel to see statistically surprising connections and unexpected absences. ${edges.length} edges analyzed.`, pattern: 'structured_fallback', confidence: 0.7};
  }

  const labels = {};
  for (const n of nodes) labels[n.label] = (labels[n.label] || 0) + 1;
  const topTypes = Object.entries(labels).sort((a, b) => b[1] - a[1]).slice(0, 5);
  return {
    text: `Graph contains ${nodes.length} nodes across ${Object.keys(labels).length} types. Top types: ${topTypes.map(([l, c]) => `${l}(${c})`).join(', ')}. Try a more specific question or use the quick actions.`,
    pattern: 'structured_fallback', confidence: 0.5,
  };
}
