import React, {useCallback, useRef, useState} from 'react';
import {ThemeProvider, ThemeToggle} from './theme.jsx';
import GraphMinimap from './GraphMinimap.jsx';
import LassoSelect from './LassoSelect.jsx';
import {computeLayout, applyPositionsToCy, listLayouts, LAYOUT_LABELS} from './layouts.js';

// GraphEnhancementToolbar: composes theme toggle, layout selector and
// lasso/minimap toggles around the graph canvas child element.
//
// Props:
//   cyRef          ref (or getter fn) holding the live cytoscape instance
//   nodes, edges   raw graph data (passed through to the child)
//   children       the graph canvas element (e.g. <CytoscapeRenderer/>); its
//                  props are spread with nodes/edges/onSelectNode
//   onSelectionChange  called with the array of nodes inside the lasso rect
export default function GraphEnhancementToolbar({cyRef, nodes = [], edges = [], children, onSelectionChange}) {
  const [lassoEnabled, setLassoEnabled] = useState(false);
  const [minimapVisible, setMinimapVisible] = useState(true);
  const [layout, setLayout] = useState('force');
  const [selection, setSelection] = useState([]);
  const lassoApi = useRef(null);

  const getCy = useCallback(() => (typeof cyRef === 'function' ? cyRef() : cyRef?.current), [cyRef]);

  const changeLayout = name => {
    setLayout(name);
    const cy = getCy();
    if (!cy) return;
    if (name === 'force' && cy.layout) {
      try {
        cy.layout({name: 'cose', padding: 34, animate: false, nodeOverlap: 28, idealEdgeLength: 100}).run();
        return;
      } catch {
        /* fall through to built-in implementation */
      }
    }
    applyPositionsToCy(cy, computeLayout(name, nodes, edges));
  };

  const toggle = (active, action, label) => (
    <button type="button" className={`enh-button ${active ? 'is-active' : ''}`} aria-pressed={active} onClick={action}>
      {label}
    </button>
  );

  return (
    <ThemeProvider>
      <div className="graph-enhancements">
        <div className="enh-toolbar" role="toolbar" aria-label="Graph enhancement controls">
          <ThemeToggle />
          <label className="enh-field">
            Layout
            <select aria-label="Graph layout algorithm" value={layout} onChange={event => changeLayout(event.target.value)}>
              {listLayouts().map(name => <option key={name} value={name}>{LAYOUT_LABELS[name] || name}</option>)}
            </select>
          </label>
          {toggle(lassoEnabled, () => setLassoEnabled(value => !value), 'Lasso select')}
          {toggle(minimapVisible, () => setMinimapVisible(value => !value), 'Minimap')}
          <button
            type="button"
            className="enh-button"
            disabled={selection.length < 2}
            onClick={() => {
              const group = lassoApi.current?.collapseSelection(selection);
              if (group) setSelection([]);
            }}
          >
            Collapse selection
          </button>
        </div>
        <LassoSelect
          apiRef={lassoApi}
          cyRef={getCy}
          nodes={nodes}
          edges={edges}
          enabled={lassoEnabled}
          onSelectionChange={selected => { setSelection(selected); onSelectionChange?.(selected); }}
        >
          {children}
        </LassoSelect>
        {minimapVisible && <GraphMinimap cyRef={getCy} />}
      </div>
    </ThemeProvider>
  );
}

