import React, {useCallback, useMemo, useState} from 'react';
import {Icon} from '../../icons.jsx';

const EVENT_ICONS = {
  vertex_upserted: 'database',
  edge_upserted: 'link',
  vertex_deleted: 'close',
  edge_deleted: 'close',
  ingestion_completed: 'check',
  validation_completed: 'shield',
};

const EVENT_COLORS = {
  vertex_upserted: '#10a981',
  edge_upserted: '#2589e8',
  vertex_deleted: '#ec6b76',
  edge_deleted: '#ec6b76',
  ingestion_completed: '#7054e8',
  validation_completed: '#df9d23',
};

function formatTime(ts) {
  if (!ts) return '';
  const d = new Date(ts);
  return d.toLocaleTimeString(undefined, {hour: '2-digit', minute: '2-digit', second: '2-digit'});
}

function eventSummary(event) {
  const data = event.data || {};
  if (event.type === 'vertex_upserted') return `${data.label || 'Entity'}: ${data.canonical_id || data.id || 'unknown'}`;
  if (event.type === 'edge_upserted') return `${data.label || 'Edge'}: ${data.out_cid || '?'} -> ${data.in_cid || '?'}`;
  if (event.type === 'vertex_deleted') return `Deleted: ${data.canonical_id || 'unknown'}`;
  if (event.type === 'edge_deleted') return `Removed edge: ${data.label || 'unknown'}`;
  if (event.type === 'ingestion_completed') return `Ingestion: ${data.source_system || 'complete'} (${data.count || 0} entities)`;
  if (event.type === 'validation_completed') return `Validation: ${data.status || 'complete'}`;
  return event.type;
}

export default function EventFeed({events, status, onPause, onResume, onClear, onNavigate, collapsed, onToggle}) {
  const [typeFilters, setTypeFilters] = useState({
    vertex_upserted: true, edge_upserted: true, vertex_deleted: true,
    edge_deleted: true, ingestion_completed: true, validation_completed: true,
  });
  const [isPaused, setIsPaused] = useState(false);

  const toggleFilter = useCallback((type) => {
    setTypeFilters(prev => ({...prev, [type]: !prev[type]}));
  }, []);

  const filteredEvents = useMemo(() => {
    return (events || []).filter(e => typeFilters[e.type] !== false).slice(-100);
  }, [events, typeFilters]);

  const statusColor = status === 'connected' ? '#10a981' : status === 'connecting' ? '#df9d23' : '#ec6b76';

  const handlePauseToggle = useCallback(() => {
    if (isPaused) {
      setIsPaused(false);
      if (onResume) onResume();
    } else {
      setIsPaused(true);
      if (onPause) onPause();
    }
  }, [isPaused, onPause, onResume]);

  if (collapsed) {
    return <button className="event-feed-toggle" onClick={onToggle} title="Show event feed">
      <Icon name="activity" size={14}/>
      <span className="event-feed-status-dot" style={{background: statusColor}}/>
      {events?.length > 0 && <span className="event-feed-badge">{events.length}</span>}
    </button>;
  }

  return <div className="kgr-event-feed panel">
    <div className="event-feed-header">
      <div className="event-feed-title">
        <span className="event-feed-status-dot" style={{background: statusColor}}/>
        <span className="eyebrow">LIVE EVENTS</span>
        <small>{status}</small>
      </div>
      <div className="event-feed-actions">
        <button onClick={handlePauseToggle} title={isPaused ? 'Resume' : 'Pause'} className="icon-button">
          <Icon name={isPaused ? 'chevron' : 'close'} size={12}/>{isPaused ? 'Resume' : 'Pause'}
        </button>
        <button onClick={onClear} title="Clear events" className="icon-button"><Icon name="close" size={12}/>Clear</button>
        <button onClick={onToggle} title="Collapse" className="icon-button"><Icon name="close" size={12}/></button>
      </div>
    </div>
    <div className="event-feed-filters">
      {Object.keys(EVENT_ICONS).map(type =>
        <label key={type} className={`event-filter-chip ${typeFilters[type] ? 'active' : ''}`}>
          <input type="checkbox" checked={typeFilters[type]} onChange={() => toggleFilter(type)}/>
          <Icon name={EVENT_ICONS[type]} size={11}/>{type.replace(/_/g, ' ')}
        </label>
      )}
    </div>
    <div className="event-feed-list">
      {filteredEvents.length === 0 && <div className="event-feed-empty"><Icon name="activity" size={16}/><span>No events yet</span></div>}
      {filteredEvents.map((e, i) => {
        const icon = EVENT_ICONS[e.type] || 'activity';
        const color = EVENT_COLORS[e.type] || '#94a3b8';
        return <div key={e.event_id || i} className="event-feed-item"
          onClick={() => onNavigate && onNavigate(e)}
          role="button" tabIndex={0}>
          <span className="event-icon" style={{color}}><Icon name={icon} size={14}/></span>
          <div className="event-info">
            <strong>{eventSummary(e)}</strong>
            <small>{formatTime(e.timestamp)}</small>
          </div>
        </div>;
      })}
    </div>
  </div>;
}
