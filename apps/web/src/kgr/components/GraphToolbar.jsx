import React, {useState} from 'react';
import {Icon} from '../../icons.jsx';

const LAYOUTS = [
  {id: 'cose', label: 'Force-directed (COSE)', group: 'Force'},
  {id: 'dagre', label: 'Hierarchical (Dagre)', group: 'Hierarchical'},
  {id: 'breadthfirst', label: 'Breadthfirst', group: 'Hierarchical'},
  {id: 'circle', label: 'Circle', group: 'Geometric'},
  {id: 'grid', label: 'Grid', group: 'Geometric'},
  {id: 'concentric', label: 'Concentric', group: 'Geometric'},
  {id: 'radial', label: 'Radial', group: 'Geometric'},
  {id: 'cola', label: 'Constraint (Cola)', group: 'Force'},
  {id: 'euler', label: 'Euler (physics)', group: 'Force'},
  {id: 'spread', label: 'Spread', group: 'Geometric'},
  {id: 'timeline', label: 'Timeline', group: 'Temporal'},
  {id: 'clustered', label: 'Clustered', group: 'Force'},
  {id: 'orthogonal', label: 'Orthogonal', group: 'Architecture'},
];

const SIZE_MODES = [
  {id: 'uniform', label: 'Uniform'},
  {id: 'degree', label: 'By degree'},
  {id: 'centrality', label: 'By centrality'},
  {id: 'property', label: 'By property value'},
];

const COLOR_BLIND_MODES = [
  {id: 'default', label: 'Default'},
  {id: 'deuteranopia', label: 'Deuteranopia (red-green)'},
  {id: 'tritanopia', label: 'Tritanopia (blue-yellow)'},
  {id: 'high-contrast', label: 'High contrast'},
];

export default function GraphToolbar({layout, onLayoutChange, sizeMode, onSizeModeChange, onFitAll, onToggleMinimap, onToggleFilters, onToggleEntityList, onExport,
  fisheyeEnabled, onToggleFisheye, colorBlindMode, onColorBlindChange, onToggleTableView, onToggleDeepLink, multiSelectionCount, onTogglePlaybooks, onToggleStyleRules, onToggleAIExplorer, onToggleSurprises,
  selectionMode, onSelectionModeChange, comboMode, onComboModeChange}) {
  const [showSettings, setShowSettings] = useState(false);

  return <div className="kgr-graph-toolbar" role="toolbar" aria-label="Graph toolbar">
    <div className="toolbar-group">
      <label className="select-control toolbar-select" title="Layout algorithm">
        <Icon name="layers" size={14}/>
        <select value={layout || 'cose'} onChange={e => onLayoutChange && onLayoutChange(e.target.value)} aria-label="Layout">
          {LAYOUTS.map(l => <option key={l.id} value={l.id}>{l.label}</option>)}
        </select>
      </label>
    </div>

    <div className="toolbar-group">
      <button className="toolbar-button" onClick={onFitAll} title="Fit all nodes (Space)"><Icon name="graph" size={14}/> Fit</button>
      <button className="toolbar-button" onClick={onToggleMinimap} title="Toggle minimap (M)"><Icon name="focus" size={14}/> Map</button>
      <button className="toolbar-button" onClick={onToggleFilters} title="Toggle filters (F)"><Icon name="layers" size={14}/> Filter</button>
      <button className="toolbar-button" onClick={onToggleEntityList} title="Toggle entity list"><Icon name="database" size={14}/> List</button>
    </div>

    <div className="toolbar-group">
      <button className={`toolbar-button${selectionMode ? ' is-active' : ''}`} onClick={() => onSelectionModeChange && onSelectionModeChange(selectionMode ? null : 'box')} title="Toggle box/lasso selection"><Icon name="focus" size={14}/> Select</button>
      <label className="select-control toolbar-select" title="Collapse repeated nodes into combo groups">
        <Icon name="layers" size={14}/>
        <select value={comboMode || 'none'} onChange={e => onComboModeChange && onComboModeChange(e.target.value === 'none' ? null : e.target.value)} aria-label="Combo grouping">
          <option value="none">No groups</option>
          <option value="domain">Group by domain</option>
          <option value="type">Group by type</option>
          <option value="community">Group by community</option>
        </select>
      </label>
      <button className={`toolbar-button${fisheyeEnabled ? ' is-active' : ''}`} onClick={onToggleFisheye} title="Toggle fisheye distortion (Shift+F)"><Icon name="focus" size={14}/> Fisheye</button>
      <button className="toolbar-button" onClick={onToggleTableView} title="Toggle table view (T)"><Icon name="database" size={14}/> Table</button>
      <button className="toolbar-button" onClick={onToggleDeepLink} title="Copy link to this view"><Icon name="link" size={14}/> Share</button>
      {multiSelectionCount > 0 && <span className="selection-count-badge">{multiSelectionCount} selected</span>}
    </div>

    <div className="toolbar-group">
      <button className="toolbar-button" onClick={onToggleSurprises} title="Surprising connections"><Icon name="activity" size={14}/> Surprises</button>
      <button className="toolbar-button" onClick={onTogglePlaybooks} title="Investigation playbooks"><Icon name="layers" size={14}/> Playbooks</button>
      <button className="toolbar-button" onClick={onToggleStyleRules} title="Conditional styling rules"><Icon name="settings" size={14}/> Rules</button>
      <button className="toolbar-button" onClick={onToggleAIExplorer} title="AI Explorer (A)"><Icon name="graph" size={14}/> AI</button>
    </div>

    <div className="toolbar-group">
      <button className="toolbar-button" onClick={onExport} title="Export graph"><Icon name="check" size={14}/> Export</button>
      <button className="toolbar-button" onClick={() => setShowSettings(s => !s)} title="Settings"><Icon name="settings" size={14}/></button>
    </div>

    {showSettings && <div className="toolbar-settings-panel">
      <h4>Node sizing</h4>
      <div className="toolbar-radio-group">
        {SIZE_MODES.map(m => <label key={m.id}>
          <input type="radio" name="sizeMode" value={m.id} checked={(sizeMode || 'uniform') === m.id}
            onChange={() => onSizeModeChange && onSizeModeChange(m.id)}/> {m.label}
        </label>)}
      </div>
      <h4>Accessibility</h4>
      <div className="toolbar-radio-group">
        {COLOR_BLIND_MODES.map(m => <label key={m.id}>
          <input type="radio" name="colorBlind" value={m.id} checked={(colorBlindMode || 'default') === m.id}
            onChange={() => onColorBlindChange && onColorBlindChange(m.id)}/> {m.label}
        </label>)}
      </div>
    </div>}
  </div>;
}
