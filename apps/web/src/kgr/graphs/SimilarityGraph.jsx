import React, {useCallback, useMemo, useState} from 'react';
import {Icon} from '../../icons.jsx';

function shortId(value, size = 22) {
  if (!value) return '—';
  return value.length > size ? `${value.slice(0, size - 1)}…` : value;
}

export default function SimilarityGraph({api, run, busy, graph, onHighlightPath}) {
  const [queryId, setQueryId] = useState('');
  const [algorithm, setAlgorithm] = useState('jaccard');
  const [results, setResults] = useState(null);
  const [pathResults, setPathResults] = useState(null);
  const [pathSource, setPathSource] = useState('');
  const [pathTarget, setPathTarget] = useState('');

  const nodeIds = useMemo(() => (graph.nodes || []).map(n => n.id), [graph]);

  const runSimilarity = useCallback(() => {
    if (!queryId.trim()) return;
    run(async () => {
      const result = await api('/api/v1/graph/similarity', {
        canonical_id: queryId.trim(), algorithm, limit: 20,
      });
      setResults(result);
    });
  }, [api, run, queryId, algorithm]);

  const runPaths = useCallback(() => {
    if (!pathSource.trim() || !pathTarget.trim()) return;
    run(async () => {
      const result = await api('/api/v1/graph/shortest-paths', {
        source_id: pathSource.trim(), target_id: pathTarget.trim(), max_paths: 5,
      });
      setPathResults(result);
    });
  }, [api, run, pathSource, pathTarget]);

  return <div className="kgr-similarity-view">
    <section className="panel">
      <div className="panel-heading"><div><span className="eyebrow">SIMILARITY SEARCH</span><h2>Find structurally similar nodes</h2></div></div>
      <div className="similarity-form">
        <div className="similarity-input-row">
          <input type="text" placeholder="Enter entity canonical ID..." value={queryId}
            onChange={e => setQueryId(e.target.value)} list="sim-node-list" aria-label="Entity ID"/>
          <datalist id="sim-node-list">{nodeIds.slice(0, 100).map(id => <option key={id} value={id}/>)}</datalist>
          <label className="select-control"><select value={algorithm} onChange={e => setAlgorithm(e.target.value)} aria-label="Algorithm">
            <option value="jaccard">Jaccard</option>
            <option value="adamic_adar">Adamic-Adar</option>
            <option value="common_neighbors">Common neighbors</option>
          </select></label>
          <button className="primary-button" disabled={busy || !queryId.trim()} onClick={runSimilarity}><Icon name="users" size={16}/>Search</button>
        </div>
      </div>
      {results && results.length > 0 ? <div className="similarity-results">
        {results.map((s, i) => <div key={s.canonical_id || i} className="similarity-result-row">
          <span className="similarity-rank">{i + 1}</span>
          <div className="similarity-info"><strong>{shortId(s.canonical_id, 36)}</strong><small>{s.common_neighbors ?? 0} common neighbors</small></div>
          <span className="similarity-score">{(s.score ?? 0).toFixed(4)}</span>
        </div>)}
      </div> : results ? <p className="subtle">No similar nodes found.</p> : null}
    </section>

    <section className="panel">
      <div className="panel-heading"><div><span className="eyebrow">SHORTEST PATHS</span><h2>Find all shortest paths between two entities</h2></div></div>
      <div className="similarity-form">
        <div className="similarity-input-row">
          <input type="text" placeholder="Source entity ID..." value={pathSource}
            onChange={e => setPathSource(e.target.value)} list="path-src-list" aria-label="Source ID"/>
          <datalist id="path-src-list">{nodeIds.slice(0, 100).map(id => <option key={id} value={id}/>)}</datalist>
          <span className="path-arrow-inline"><Icon name="chevron" size={14}/></span>
          <input type="text" placeholder="Target entity ID..." value={pathTarget}
            onChange={e => setPathTarget(e.target.value)} list="path-tgt-list" aria-label="Target ID"/>
          <datalist id="path-tgt-list">{nodeIds.slice(0, 100).map(id => <option key={id} value={id}/>)}</datalist>
          <button className="primary-button" disabled={busy || !pathSource.trim() || !pathTarget.trim()} onClick={runPaths}>
            <Icon name="link" size={16}/>Find paths</button>
        </div>
      </div>
      {pathResults && <>
        <p className="subtle">{pathResults.count} path{pathResults.count !== 1 ? 's' : ''} found</p>
        <div className="paths-list">{(pathResults.paths || []).map((path, i) =>
          <div key={i} className="path-row path-clickable" onClick={() => onHighlightPath && onHighlightPath(path)}>
            <span className="path-index">#{i + 1}</span>
            <div className="path-nodes">{path.map((nid, j) => <React.Fragment key={j}>
              {j > 0 && <span className="path-sep">&rarr;</span>}
              <span className="path-node" title={nid}>{shortId(nid, 18)}</span>
            </React.Fragment>)}</div>
            <span className="path-length">{path.length - 1} hop{path.length - 1 !== 1 ? 's' : ''}</span>
          </div>
        )}</div>
      </>}
    </section>
  </div>;
}
