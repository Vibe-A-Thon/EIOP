import React, {useCallback, useEffect, useId, useMemo, useRef, useState} from 'react';
import {Icon} from '../../icons.jsx';

const ITEM_HEIGHT = 44;
const OVERSCAN = 5;

export default function VirtualEntityList({nodes, selectedId, onSelect, onExpand, palette: colorPalette}) {
  const containerRef = useRef(null);
  const [scrollTop, setScrollTop] = useState(0);
  const [filterText, setFilterText] = useState('');
  const [sortBy, setSortBy] = useState('label');
  const [activeIndex, setActiveIndex] = useState(0);
  const listId = useId();

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

  useEffect(() => {
    setScrollTop(0); setActiveIndex(0);
    if (containerRef.current) containerRef.current.scrollTop = 0;
  }, [filterText, sortBy]);

  const totalHeight = filtered.length * ITEM_HEIGHT;
  const containerHeight = containerRef.current?.clientHeight || 400;
  const startIdx = Math.max(0, Math.floor(scrollTop / ITEM_HEIGHT) - OVERSCAN);
  const endIdx = Math.min(filtered.length, Math.ceil((scrollTop + containerHeight) / ITEM_HEIGHT) + OVERSCAN);
  const visibleItems = filtered.slice(startIdx, endIdx);

  const handleScroll = useCallback((e) => {
    setScrollTop(e.target.scrollTop);
  }, []);

  function handleKeyDown(event) {
    const index = Math.min(activeIndex, Math.max(0, filtered.length - 1));
    if (event.key === 'Enter' || event.key === ' ') {
      event.preventDefault();
      if (filtered[index]) {
        if (event.key === 'Enter' && onExpand) onExpand(filtered[index]);
        else onSelect?.(filtered[index]);
      }
      return;
    }
    const next = event.key === 'ArrowDown' ? Math.min(index + 1, filtered.length - 1)
      : event.key === 'ArrowUp' ? Math.max(0, index - 1)
      : event.key === 'Home' ? 0 : event.key === 'End' ? filtered.length - 1 : null;
    if (next === null || next < 0) return;
    event.preventDefault(); setActiveIndex(next);
    const viewport = containerRef.current;
    if (viewport) {
      const top = next * ITEM_HEIGHT;
      if (top < viewport.scrollTop) viewport.scrollTop = top;
      else if (top + ITEM_HEIGHT > viewport.scrollTop + viewport.clientHeight) viewport.scrollTop = top + ITEM_HEIGHT - viewport.clientHeight;
      setScrollTop(viewport.scrollTop);
    }
  }

  const displayName = (n) => n.properties?.display_name || n.properties?.name || n.properties?.issue_key || n.label || n.id || 'Unknown';
  const shortId = (v) => v && v.length > 24 ? v.slice(0, 23) + '…' : v;

  return <div className="virtual-entity-list">
    <div className="vel-header">
      <span className="vel-count" id={`${listId}-count`} role="status">{filtered.length} entities</span>
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
      role="listbox" aria-label="Entity results" tabIndex={0} onKeyDown={handleKeyDown}
      aria-describedby={`${listId}-count`}
      aria-activedescendant={filtered.length ? `${listId}-${Math.min(activeIndex, filtered.length - 1)}` : undefined}
      style={{overflowY: 'auto', height: 400, maxHeight: '60vh', position: 'relative'}}>
      <div style={{height: totalHeight, position: 'relative'}}>
        {visibleItems.map((n, i) => {
          const idx = startIdx + i;
          const isSelected = n.id === selectedId;
          const color = colorPalette?.[n.label] || '#64748b';
          return <div key={n.id} id={`${listId}-${idx}`} className={`vel-item ${isSelected ? 'selected' : ''} ${activeIndex === idx ? 'keyboard-active' : ''}`}
            style={{position: 'absolute', top: idx * ITEM_HEIGHT, height: ITEM_HEIGHT, left: 0, right: 0}}
            onClick={() => {setActiveIndex(idx); onSelect?.(n); containerRef.current?.focus({preventScroll: true});}}
            onDoubleClick={() => onExpand && onExpand(n)}
            role="option" aria-selected={isSelected} aria-posinset={idx + 1} aria-setsize={filtered.length}>
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
