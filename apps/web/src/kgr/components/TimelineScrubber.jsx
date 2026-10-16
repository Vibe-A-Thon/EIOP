import React, {useCallback, useEffect, useMemo, useRef, useState} from 'react';
import {Icon} from '../../icons.jsx';

function bucketByTime(nodes, bucketSize = 'day') {
  const buckets = {};
  for (const n of nodes) {
    const ts = n.properties?.created_at || n.properties?.modified_at;
    if (!ts) continue;
    const d = new Date(ts);
    let key;
    if (bucketSize === 'month') key = `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, '0')}`;
    else if (bucketSize === 'week') {
      const start = new Date(d); start.setDate(d.getDate() - d.getDay());
      key = start.toISOString().slice(0, 10);
    } else key = d.toISOString().slice(0, 10);
    buckets[key] = (buckets[key] || 0) + 1;
  }
  return buckets;
}

export default function TimelineScrubber({nodes, range, onRangeChange}) {
  const [playing, setPlaying] = useState(false);
  const [speed, setSpeed] = useState(1);
  const intervalRef = useRef(null);

  const timestamps = useMemo(() => {
    const ts = [];
    for (const n of nodes || []) {
      const t = n.properties?.created_at || n.properties?.modified_at;
      if (t) ts.push(new Date(t).getTime());
    }
    ts.sort((a, b) => a - b);
    return ts;
  }, [nodes]);

  const minTs = timestamps[0] || Date.now() - 86400000 * 365;
  const maxTs = timestamps[timestamps.length - 1] || Date.now();
  const from = range?.from || minTs;
  const to = range?.to || maxTs;

  const buckets = useMemo(() => {
    const span = maxTs - minTs;
    const size = span > 86400000 * 365 ? 'month' : span > 86400000 * 30 ? 'week' : 'day';
    return bucketByTime(nodes || [], size);
  }, [nodes, minTs, maxTs]);

  const maxBucket = Math.max(...Object.values(buckets), 1);
  const sortedKeys = Object.keys(buckets).sort();

  useEffect(() => {
    if (!playing) { clearInterval(intervalRef.current); return; }
    const step = (maxTs - minTs) / 50;
    intervalRef.current = setInterval(() => {
      onRangeChange(prev => {
        const newTo = Math.min((prev?.to || from) + step * speed, maxTs);
        if (newTo >= maxTs) { setPlaying(false); return {from: prev?.from || minTs, to: maxTs}; }
        return {from: prev?.from || minTs, to: newTo};
      });
    }, 200);
    return () => clearInterval(intervalRef.current);
  }, [playing, speed, from, minTs, maxTs, onRangeChange]);

  const pct = (v) => ((v - minTs) / Math.max(maxTs - minTs, 1)) * 100;

  return <div className="kgr-timeline" role="region" aria-label="Timeline scrubber">
    <div className="timeline-controls">
      <button onClick={() => setPlaying(!playing)} title={playing ? 'Pause' : 'Play'}>
        <Icon name={playing ? 'close' : 'chevron'} size={14}/>{playing ? 'Pause' : 'Play'}
      </button>
      <select value={speed} onChange={e => setSpeed(Number(e.target.value))} aria-label="Playback speed">
        <option value={1}>1x</option><option value={2}>2x</option><option value={5}>5x</option><option value={10}>10x</option>
      </select>
      <span className="timeline-date">{new Date(from).toLocaleDateString()} — {new Date(to).toLocaleDateString()}</span>
    </div>
    <div className="timeline-track">
      <div className="timeline-histogram">
        {sortedKeys.map(k => <div key={k} className="timeline-bar" style={{height: `${(buckets[k] / maxBucket) * 100}%`}} title={`${k}: ${buckets[k]}`}/>)}
      </div>
      <div className="timeline-selection" style={{left: `${pct(from)}%`, width: `${pct(to) - pct(from)}%`}}/>
      <input type="range" className="timeline-handle timeline-from" min={minTs} max={maxTs} value={from}
        onChange={e => onRangeChange({from: Number(e.target.value), to})} aria-label="Start date"/>
      <input type="range" className="timeline-handle timeline-to" min={minTs} max={maxTs} value={to}
        onChange={e => onRangeChange({from, to: Number(e.target.value)})} aria-label="End date"/>
    </div>
  </div>;
}
