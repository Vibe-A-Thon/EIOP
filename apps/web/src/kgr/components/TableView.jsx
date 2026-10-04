import React, {useMemo, useState} from 'react';
import {Icon} from '../../icons.jsx';
import {palette} from '../../GraphCanvas.jsx';

export default function TableView({nodes = [], edges = [], onSelect, selectedId, onClose}) {
  const [sortCol, setSortCol] = useState('label');
  const [sortDir, setSortDir] = useState('asc');
  const [filterText, setFilterText] = useState('');
  const [tab, setTab] = useState('entities');
  const [expandedRow, setExpandedRow] = useState(null);

  const handleSort = (col) => {
    if (sortCol === col) setSortDir(d => d === 'asc' ? 'desc' : 'asc');
    else { setSortCol(col); setSortDir('asc'); }
  };

  const degrees = useMemo(() => {
    const d = {};
    for (const n of nodes) d[n.id] = {in: 0, out: 0};
    for (const e of edges) {
      if (d[e.from_id]) d[e.from_id].out++;
      if (d[e.to_id]) d[e.to_id].in++;
    }
    return d;
  }, [nodes, edges]);

  const filteredNodes = useMemo(() => {
    const search = filterText.toLowerCase();
    let result = nodes.filter(n => {
      if (!search) return true;
      const name = n.properties?.name || n.properties?.qualified_name || n.id;
      return name.toLowerCase().includes(search) || n.label.toLowerCase().includes(search) || (n.domain || '').toLowerCase().includes(search);
    });
    result.sort((a, b) => {
      let va, vb;
      if (sortCol === 'label') { va = a.label; vb = b.label; }
      else if (sortCol === 'name') { va = a.properties?.name || a.id; vb = b.properties?.name || b.id; }
      else if (sortCol === 'domain') { va = a.domain || ''; vb = b.domain || ''; }
      else if (sortCol === 'degree') { va = (degrees[a.id]?.in || 0) + (degrees[a.id]?.out || 0); vb = (degrees[b.id]?.in || 0) + (degrees[b.id]?.out || 0); }
      else if (sortCol === 'inDeg') { va = degrees[a.id]?.in || 0; vb = degrees[b.id]?.in || 0; }
      else if (sortCol === 'outDeg') { va = degrees[a.id]?.out || 0; vb = degrees[b.id]?.out || 0; }
      else { va = a.id; vb = b.id; }
      if (typeof va === 'number' && typeof vb === 'number') return sortDir === 'asc' ? va - vb : vb - va;
      return sortDir === 'asc' ? String(va).localeCompare(String(vb)) : String(vb).localeCompare(String(va));
    });
    return result;
  }, [nodes, filterText, sortCol, sortDir, degrees]);

  const nodeEdges = useMemo(() => {
    if (!expandedRow) return [];
    return edges.filter(e => e.from_id === expandedRow || e.to_id === expandedRow);
  }, [edges, expandedRow]);

  const sortIcon = (col) => sortCol === col ? (sortDir === 'asc' ? ' ▲' : ' ▼') : '';

  return <div className="kgr-table-view" role="region" aria-label="Graph table view">
    <div style={{display: 'flex', justifyContent: 'space-between', alignItems: 'center', padding: '8px 0', gap: 8}}>
      <div style={{display: 'flex', gap: 4}}>
        <button className={`toolbar-button${tab === 'entities' ? ' is-active' : ''}`} onClick={() => setTab('entities')}>Entities</button>
        <button className={`toolbar-button${tab === 'relationships' ? ' is-active' : ''}`} onClick={() => setTab('relationships')}>Relationships</button>
      </div>
      <input type="text" placeholder="Filter..." value={filterText} onChange={e => setFilterText(e.target.value)}
        style={{padding: '4px 8px', fontSize: 12, border: '1px solid var(--line)', borderRadius: 4, background: 'var(--bg)', color: 'var(--fg)'}}/>
      <button className="icon-button" onClick={onClose}><Icon name="close"/></button>
    </div>

    {tab === 'entities' && <table role="grid" aria-label="Entity table">
      <thead>
        <tr>
          <th onClick={() => handleSort('name')} aria-sort={sortCol === 'name' ? sortDir + 'ending' : 'none'}>Name{sortIcon('name')}</th>
          <th onClick={() => handleSort('label')}>Type{sortIcon('label')}</th>
          <th onClick={() => handleSort('domain')}>Domain{sortIcon('domain')}</th>
          <th onClick={() => handleSort('degree')}>Degree{sortIcon('degree')}</th>
          <th onClick={() => handleSort('inDeg')}>In{sortIcon('inDeg')}</th>
          <th onClick={() => handleSort('outDeg')}>Out{sortIcon('outDeg')}</th>
        </tr>
      </thead>
      <tbody>
        {filteredNodes.slice(0, 500).map(n => <React.Fragment key={n.id}>
          <tr className={n.id === selectedId ? 'selected' : ''}
            onClick={() => { onSelect?.(n); setExpandedRow(expandedRow === n.id ? null : n.id); }}
            tabIndex={0} onKeyDown={e => { if (e.key === 'Enter') onSelect?.(n); }}>
            <td><span className="type-dot" style={{background: palette[n.label] || '#64748b'}}/>{(n.properties?.name || n.properties?.qualified_name || n.id).slice(0, 40)}</td>
            <td>{n.label}</td>
            <td>{n.domain || '—'}</td>
            <td>{(degrees[n.id]?.in || 0) + (degrees[n.id]?.out || 0)}</td>
            <td>{degrees[n.id]?.in || 0}</td>
            <td>{degrees[n.id]?.out || 0}</td>
          </tr>
          {expandedRow === n.id && nodeEdges.length > 0 && <tr>
            <td colSpan={6} style={{padding: '4px 20px', fontSize: 11, background: 'var(--bg)'}}>
              {nodeEdges.slice(0, 20).map((e, i) => <div key={e.id || i} style={{padding: '2px 0'}}>
                <strong>{e.type}</strong> → {e.from_id === n.id ? e.to_id : e.from_id}
                {e.creation_status && <span style={{marginLeft: 6, fontSize: 10, color: 'var(--muted)'}}>({e.creation_status})</span>}
              </div>)}
              {nodeEdges.length > 20 && <div style={{color: 'var(--muted)'}}>+{nodeEdges.length - 20} more</div>}
            </td>
          </tr>}
        </React.Fragment>)}
      </tbody>
    </table>}

    {tab === 'relationships' && <table role="grid" aria-label="Relationship table">
      <thead>
        <tr>
          <th>Type</th><th>Source</th><th>Target</th><th>Status</th>
        </tr>
      </thead>
      <tbody>
        {edges.slice(0, 500).map((e, i) => <tr key={e.id || i}>
          <td><strong>{e.type}</strong></td>
          <td>{(e.from_id || '').slice(0, 30)}</td>
          <td>{(e.to_id || '').slice(0, 30)}</td>
          <td>{e.creation_status || '—'}</td>
        </tr>)}
      </tbody>
    </table>}
  </div>;
}
