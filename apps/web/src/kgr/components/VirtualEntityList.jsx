import React, {useCallback, useMemo, useRef, useState} from 'react';
import {Icon} from '../../icons.jsx';

const ITEM_HEIGHT = 44;
const OVERSCAN = 5;

export default function VirtualEntityList({nodes, selectedId, onSelect, onExpand, palette: colorPalette}) {
  const containerRef = useRef(null);
  const [scrollTop, setScrollTop] = useState(0);
  const [filterText, setFilterText] = useState('');
  const [sortBy, setSortBy] = useState('label');

  const filtered = useMemo(() => {
    let list = nodes || [];
    if (filterText) {
      const q = filterText.toLowerCase();
      list = list.filter(n => {
        const name = n.properties?.display_name || n.properties?.name || n.properties?.issue_key || n.label || n.id || '';
        return name.toLowerCase().includes(q) || (n.id || '').toLowerCase().includes(q);
      });
    }
    if (sortBy === 'degree') {
      list = [...list].sort((a, b) => (b.degree || 0) - (a.degree || 0));
    } else if (sortBy === 'type') {
      list = [...list].sort((a, b) => (a.label || '').localeCompare(b.label || ''));
    } else {
      list = [...list].sort((a, b) => {
        const aName = a.properties?.display_name || a.properties?.name || a.label || a.id || '';
        const bName = b.properties?.display_name || b.properties?.name || b.label || b.id || '';
        return aName.localeCompare(bName);
      });
    }
    return list;
  }, [nodes, filterText, sortBy]);

  const totalHeight = filtered.length * ITEM_HEIGHT;
  const containerHeight = containerRef.current?.clientHeight || 400;
  const startIdx = Math.max(0, Math.floor(scrollTop / ITEM_HEIGHT) - OVERSCAN);
  const endIdx = Math.min(filtered.length, Math.ceil((scrollTop + containerHeight) / ITEM_HEIGHT) + OVERSCAN);
  const visibleItems = filtered.slice(startIdx, endIdx);

  const handleScroll = useCallback((e) => {
    setScrollTop(e.target.scrollTop);
  }, []);

  const displayName = (n) => n.properties?.display_name || n.properties?.name || n.properties?.issue_key || n.label || n.id || 'Unknown';
  const shortId = (v) => v && v.length > 24 ? v.slice(0, 23) + '…' : v;

  return <div className="virtual-entity-list">
    <div className="vel-header">
      <span className="vel-count">{filtered.length} entities</span>
      <div className="vel-controls">
        <input type="text" placeholder="Filter..." value={filterText} onChange={e => setFilterText(e.target.value)}
          className="vel-filter" aria-label="Filter entities"/>
        <select value={sortBy} onChange={e => setSortBy(e.target.value)} className="vel-sort" aria-label="Sort by">
          <option value="label">Name</option>
          <option value="degree">Degree</option>
          <option value="type">Type</option>
        </select>
      </div>
    </div>
    <div className="vel-viewport" ref={containerRef} onScroll={handleScroll}
      style={{overflowY: 'auto', height: '100%', position: 'relative'}}>
      <div style={{height: totalHeight, position: 'relative'}}>
        {visibleItems.map((n, i) => {
          const idx = startIdx + i;
          const isSelected = n.id === selectedId;
          const color = colorPalette?.[n.label] || '#64748b';
          return <div key={n.id} className={`vel-item ${isSelected ? 'selected' : ''}`}
            style={{position: 'absolute', top: idx * ITEM_HEIGHT, height: ITEM_HEIGHT, left: 0, right: 0}}
            onClick={() => onSelect && onSelect(n)}
            onDoubleClick={() => onExpand && onExpand(n)}
            role="option" aria-selected={isSelected}>
            <span className="vel-dot" style={{background: color}}/>
            <div className="vel-info">
              <strong>{displayName(n)}</strong>
              <small>{n.label} {shortId(n.id)}</small>
            </div>
            {n.degree != null && <span className="vel-degree">{n.degree}</span>}
          </div>;
        })}
      </div>
    </div>
  </div>;
}
