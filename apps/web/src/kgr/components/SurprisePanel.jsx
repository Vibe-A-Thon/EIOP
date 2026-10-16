import React from 'react';
import {Icon} from '../../icons.jsx';

export default function SurprisePanel({data, onHighlight, onClose}) {
  if (!data) return <div className="kgr-surprise-panel panel">
    <div style={{display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 10}}>
      <h3 style={{margin: 0}}>Surprising Connections</h3>
      <button className="icon-button" onClick={onClose}><Icon name="close"/></button>
    </div>
    <div className="empty-state"><span className="empty-icon"><Icon name="activity" size={22}/></span>
      <strong>Loading...</strong><p>Computing surprise analysis.</p>
    </div>
  </div>;

  const {surprising_edges = [], unexpected_absences = [], counts = {}} = data;

  return <div className="kgr-surprise-panel panel">
    <div style={{display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 10}}>
      <h3 style={{margin: 0}}>Surprising Connections</h3>
      <button className="icon-button" onClick={onClose}><Icon name="close"/></button>
    </div>

    <div style={{marginBottom: 12}}>
      <span className="eyebrow">SURPRISING EDGES</span>
      <span style={{marginLeft: 6, fontSize: 12, color: 'var(--muted)'}}>({counts.surprising_edges || 0})</span>
    </div>
    {surprising_edges.map((s, i) => <div key={i} className="kgr-surprise-row" onClick={() => onHighlight?.('edge', s)}>
      <span className="kgr-surprise-sparkle">✦</span>
      <div style={{flex: 1, minWidth: 0}}>
        <div style={{fontSize: 12, fontWeight: 600}}>{s.edge_label || 'edge'}</div>
        <div style={{fontSize: 11, color: 'var(--muted)', overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap'}}>
          {(s.source_label || '?')} → {(s.target_label || '?')}
        </div>
        <div style={{fontSize: 10, color: 'var(--muted)'}}>{s.explanation}</div>
      </div>
      <span className="kgr-surprise-score">{s.score?.toFixed?.(1) || '—'}</span>
    </div>)}

    {surprising_edges.length === 0 && <p style={{fontSize: 12, color: 'var(--muted)'}}>No surprising edges found.</p>}

    <div style={{marginTop: 16, marginBottom: 12}}>
      <span className="eyebrow">UNEXPECTED ABSENCES</span>
      <span style={{marginLeft: 6, fontSize: 12, color: 'var(--muted)'}}>({counts.unexpected_absences || 0})</span>
    </div>
    {unexpected_absences.map((s, i) => <div key={i} className="kgr-surprise-row" onClick={() => onHighlight?.('absence', s)}>
      <span className="kgr-surprise-sparkle" style={{color: '#ef4444'}}>◇</span>
      <div style={{flex: 1, minWidth: 0}}>
        <div style={{fontSize: 12, fontWeight: 600}}>Missing connection</div>
        <div style={{fontSize: 11, color: 'var(--muted)', overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap'}}>
          {(s.source_label || '?')}: {s.source_id?.slice(0, 25)} ↔ {(s.target_label || '?')}: {s.target_id?.slice(0, 25)}
        </div>
        <div style={{fontSize: 10, color: 'var(--muted)'}}>{s.explanation}</div>
      </div>
      <span className="kgr-surprise-score">{s.score?.toFixed?.(1) || '—'}</span>
    </div>)}

    {unexpected_absences.length === 0 && <p style={{fontSize: 12, color: 'var(--muted)'}}>No unexpected absences found.</p>}
  </div>;
}
