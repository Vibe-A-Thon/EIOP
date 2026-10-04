import React, {useEffect, useMemo, useRef, useState} from 'react';
import {Icon, Tip} from './icons.jsx';

const palette = {
  WorkItem: '#7c5cff', Project: '#9a7dff', Person: '#ef6e91', Repository: '#0ea5e9',
  Branch: '#38bdf8', Commit: '#2563eb', File: '#64748b', CodeSymbol: '#10b981',
  Dependency: '#f59e0b', MergeRequest: '#8b5cf6', PipelineRun: '#f97316',
  Document: '#14b8a6', DocumentSection: '#2dd4bf', Evidence: '#eab308',
  IngestionRun: '#94a3b8', ValidationRun: '#22c55e', ValidationFinding: '#ef4444',
};

const safeClass = name => String(name).toLowerCase().replace(/[^a-z0-9]/g, '');

export function getSemanticZoomLevel(zoom) {
  if (zoom < 0.3) return 'cluster';
  if (zoom < 0.8) return 'entity';
  return 'detail';
}

export function applySemanticZoom(cy, level) {
  if (!cy) return;
  cy.nodes().removeClass('sz-cluster sz-entity sz-detail');
  cy.nodes().addClass(`sz-${level}`);
  cy.edges().removeClass('sz-cluster sz-entity sz-detail');
  cy.edges().addClass(`sz-${level}`);
}

export function fisheyeDistort(positions, focusX, focusY, radius = 200, distortion = 2) {
  const result = {};
  for (const [id, pos] of Object.entries(positions)) {
    const dx = pos.x - focusX, dy = pos.y - focusY;
    const dist = Math.sqrt(dx * dx + dy * dy);
    if (dist > radius || dist === 0) {
      result[id] = {...pos};
    } else {
      const normalised = dist / radius;
      const scale = distortion * (1 - normalised * normalised) + 1;
      result[id] = {x: focusX + dx * scale, y: focusY + dy * scale};
    }
  }
  return result;
}

export default function GraphCanvas({
  nodes = [], edges = [], paths = [], selectedId, selectedEdgeId,
  onSelectNode, onSelectEdge, onExpand, layout: requestedLayout, onLayoutChange,
  semanticZoomLevel, fisheye,
}) {
  const containerRef = useRef(null);
  const cyRef = useRef(null);
  const [ready, setReady] = useState(false);
  const [showLabels, setShowLabels] = useState(true);
  const [localLayout, setLocalLayout] = useState('cose');
  const layout = requestedLayout || localLayout;
  const changeLayout = value => {
    if (onLayoutChange) onLayoutChange(value);
    else setLocalLayout(value);
  };

  const elements = useMemo(() => [
    ...nodes.map(node => ({
      data: {
        id: node.id,
        label: (node.properties?.issue_key || node.properties?.name || node.properties?.qualified_name || node.properties?.path || node.label).slice(0, 34),
        entityLabel: node.label,
        color: palette[node.label] || '#64748b',
        node,
      },
      classes: safeClass(node.label),
    })),
    ...edges.map(edge => ({
      data: {id: edge.id, source: edge.from_id, target: edge.to_id, label: edge.type, edge},
      classes: [
        edge.creation_status?.toLowerCase() === 'inferred' ? 'inferred' : '',
        edge.properties?.source_ref || edge.properties?.evidence_key ? 'evidenced' : '',
        paths.some(path => path.edge_ids?.includes(edge.id)) ? 'path-edge' : '',
      ].filter(Boolean).join(' '),
    })),
  ], [nodes, edges, paths]);

  useEffect(() => {
    let cancelled = false;
    let instance;
    import('cytoscape').then(({default: cytoscape}) => {
      if (cancelled || !containerRef.current) return;
      instance = cytoscape({
        container: containerRef.current,
        elements: [],
        minZoom: 0.18,
        maxZoom: 3.5,
        wheelSensitivity: 0.24,
        boxSelectionEnabled: false,
        style: [
          {selector: 'node', style: {
            'background-color': 'data(color)', 'label': 'data(label)', 'color': '#24324a',
            'font-family': 'Inter, Segoe UI, sans-serif', 'font-size': '10px', 'font-weight': 600,
            'text-valign': 'bottom', 'text-margin-y': 8, 'text-wrap': 'ellipsis', 'text-max-width': '100px',
            'width': 38, 'height': 38, 'border-width': 5, 'border-color': '#ffffff',
            'shadow-blur': 10, 'shadow-color': '#334155', 'shadow-opacity': .14, 'shadow-offset-y': 3,
          }},
          {selector: 'node:selected, node.selected', style: {
            'border-width': 5, 'border-color': '#a78bfa', 'width': 48, 'height': 48,
            'shadow-blur': 16, 'shadow-color': '#7c3aed', 'shadow-opacity': .35,
          }},
          {selector: 'edge', style: {
            'width': 1.6, 'line-color': '#b8c2d1', 'target-arrow-color': '#94a3b8',
            'target-arrow-shape': 'triangle', 'arrow-scale': .7, 'curve-style': 'bezier',
            'label': 'data(label)', 'font-family': 'Inter, Segoe UI, sans-serif', 'font-size': '8px',
            'font-weight': 600, 'color': '#64748b', 'text-background-color': '#fff',
            'text-background-opacity': .88, 'text-background-shape': 'roundrectangle',
            'text-background-padding': '3px', 'text-rotation': 'autorotate',
          }},
          {selector: 'edge:selected, edge.selected', style: {
            'width': 3, 'line-color': '#7c5cff', 'target-arrow-color': '#7c5cff', 'color': '#5b3fd6',
          }},
          {selector: 'edge.inferred', style: {'line-style': 'dashed', 'line-color': '#f59e0b', 'target-arrow-color': '#f59e0b'}},
          {selector: 'edge.evidenced', style: {'width': 2.2}},
          {selector: 'edge.path-edge', style: {'width': 4, 'line-color': '#7c5cff', 'target-arrow-color': '#7c5cff', 'z-index': 10}},
          {selector: 'edge.orthogonal-edge', style: {
            'curve-style': 'taxi', 'taxi-direction': 'auto', 'taxi-turn': '50%',
            'taxi-turn-min-distance': '18px',
          }},
          {selector: '.labels-off', style: {'label': ''}},
          {selector: '.semantic-compact', style: {'label': ''}},
          {selector: 'node.sz-cluster', style: {'label': '', 'opacity': 0.35, 'width': 18, 'height': 18, 'border-width': 2, 'transition-property': 'opacity, width, height', 'transition-duration': '200ms'}},
          {selector: 'node.sz-cluster[?isHub]', style: {'opacity': 1, 'width': 44, 'height': 44}},
          {selector: 'node.sz-entity', style: {'text-max-width': '60px', 'transition-property': 'opacity, width, height', 'transition-duration': '200ms'}},
          {selector: 'edge.sz-cluster', style: {'label': '', 'opacity': 0.15}},
          {selector: 'edge.sz-entity', style: {'label': ''}},
          {selector: 'edge.sz-detail', style: {}},
          {selector: 'node.fisheye-focus', style: {'border-color': '#f59e0b', 'border-width': 3}},
        ],
      });
      instance.on('tap', 'node', event => onSelectNode?.(event.target.data('node')));
      instance.on('tap', 'edge', event => onSelectEdge?.(event.target.data('edge')));
      instance.on('dbltap', 'node', event => onExpand?.(event.target.data('node')));
      instance.on('zoom', () => {
        instance.nodes().toggleClass('semantic-compact', instance.zoom() < .52);
        const level = getSemanticZoomLevel(instance.zoom());
        applySemanticZoom(instance, level);
      });
      cyRef.current = instance;
      setReady(true);
    });
    return () => {
      cancelled = true;
      instance?.destroy();
      if (cyRef.current === instance) cyRef.current = null;
    };
  }, []);

  useEffect(() => {
    const cy = cyRef.current;
    if (!cy || !ready) return;
    cy.elements().remove();
    if (!elements.length) return;
    cy.add(elements);
    cy.edges().toggleClass('orthogonal-edge', layout === 'orthogonal');
    const layoutName = layout === 'orthogonal' ? 'grid' : layout;
    try {
      cy.layout({name: layoutName, padding: 34, animate: false, componentSpacing: 100, nodeOverlap: 28, idealEdgeLength: 100}).run();
    } catch {
      cy.layout({name: 'grid', padding: 34}).run();
    }
    cy.fit(undefined, 38);
  }, [elements, layout, ready]);

  useEffect(() => {
    const cy = cyRef.current;
    if (!cy) return;
    cy.elements().removeClass('selected');
    const id = selectedEdgeId || selectedId;
    if (id) cy.getElementById(id).addClass('selected').select();
  }, [selectedId, selectedEdgeId]);

  useEffect(() => {
    const cy = cyRef.current;
    if (!cy) return;
    cy.elements().toggleClass('labels-off', !showLabels);
  }, [showLabels, elements]);

  const control = (text, icon, action, active = false) => <Tip text={text}><button type="button" className={`canvas-button ${active ? 'is-active' : ''}`} onClick={action} aria-label={text}><Icon name={icon} size={16}/></button></Tip>;
  const relationshipTypes = [...new Set(edges.map(edge => edge.type))];

  return <div className="canvas-shell">
    <div className="canvas-toolbar" aria-label="Graph controls">
      {control('Zoom in', 'plus', () => cyRef.current?.zoom({level: Math.min(3.5, (cyRef.current?.zoom() || 1) * 1.2), renderedPosition: {x: 350, y: 220}}))}
      {control('Zoom out', 'minus', () => cyRef.current?.zoom({level: Math.max(.18, (cyRef.current?.zoom() || 1) / 1.2), renderedPosition: {x: 350, y: 220}}))}
      {control('Fit all entities in view', 'focus', () => cyRef.current?.fit(undefined, 38))}
      {control(showLabels ? 'Hide graph labels' : 'Show graph labels', 'eye', () => setShowLabels(value => !value), showLabels)}
      <Tip text="Switch graph layout"><select aria-label="Graph layout" value={layout} onChange={event => changeLayout(event.target.value)}><option value="cose">Organic</option><option value="breadthfirst">Hierarchy</option><option value="circle">Circle</option><option value="grid">Grid</option><option value="orthogonal">Orthogonal</option></select></Tip>
    </div>
    {!ready && <div className="canvas-loading"><span className="spinner"/>Preparing relationship map…</div>}
    {ready && elements.length === 0 && <div className="empty-state canvas-empty"><span className="empty-icon"><Icon name="graph" size={24}/></span><strong>No relationships to display</strong><p>Search for an entity to build a bounded graph view.</p></div>}
    <div ref={containerRef} className="graph-canvas" role="img" aria-label={`Knowledge graph. Relationship types: ${relationshipTypes.join(', ') || 'none'}. Double-click an entity to expand its neighborhood.`}/>
    <div className="canvas-hint"><span><Icon name="info" size={14}/> Select to inspect</span><span>Double-click to expand</span></div>
  </div>;
}

export {palette};
