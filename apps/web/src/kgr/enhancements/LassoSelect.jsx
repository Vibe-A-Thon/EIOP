import React, {useCallback, useEffect, useMemo, useRef, useState} from 'react';

let groupCounter = 0;

// LassoSelect: drag-a-rectangle multi-select over the graph plus group collapse.
// - Wraps a child element (the graph canvas) inside a relatively positioned shell.
// - When `enabled`, dragging draws a rectangle; on release all nodes whose
//   rendered position falls inside are reported via onSelectionChange.
// - collapseSelection() replaces the current selection with a single group node;
//   clicking a group node (or calling expandGroup) restores its members.
export default function LassoSelect({
  cyRef, nodes = [], edges = [], children,
  enabled = true, onSelectionChange, onCollapse, onExpand, apiRef,
}) {
  const shellRef = useRef(null);
  const [rect, setRect] = useState(null);
  const [groups, setGroups] = useState({});
  const dragStart = useRef(null);

  const getCy = useCallback(() => (typeof cyRef === 'function' ? cyRef() : cyRef?.current), [cyRef]);

  const memberIds = useMemo(() => {
    const set = new Set();
    for (const group of Object.values(groups)) for (const id of group.memberIds) set.add(id);
    return set;
  }, [groups]);

  // Derived graph: member nodes hidden, one group node per collapsed set.
  const {visibleNodes, visibleEdges} = useMemo(() => {
    const groupNodes = Object.values(groups).map(group => ({
      id: group.id,
      label: 'Group',
      properties: {
        name: group.name,
        member_count: group.memberIds.length,
      },
    }));
    const visibleNodes = [
      ...nodes.filter(node => !memberIds.has(node.id)),
      ...groupNodes,
    ];
    const visibleEdges = edges.filter(edge => !memberIds.has(edge.from_id) && !memberIds.has(edge.to_id));
    return {visibleNodes, visibleEdges};
  }, [nodes, edges, groups, memberIds]);

  const toLocal = event => {
    const bounds = shellRef.current?.getBoundingClientRect();
    return bounds ? {x: event.clientX - bounds.left, y: event.clientY - bounds.top} : null;
  };

  const onMouseDown = event => {
    if (!enabled || event.button !== 0) return;
    const point = toLocal(event);
    if (!point) return;
    dragStart.current = point;
    setRect({x: point.x, y: point.y, width: 0, height: 0});
  };

  const onMouseMove = event => {
    if (!dragStart.current) return;
    const point = toLocal(event);
    if (!point) return;
    setRect({
      x: Math.min(dragStart.current.x, point.x),
      y: Math.min(dragStart.current.y, point.y),
      width: Math.abs(point.x - dragStart.current.x),
      height: Math.abs(point.y - dragStart.current.y),
    });
  };

  const onMouseUp = () => {
    if (!dragStart.current) return;
    dragStart.current = null;
    const cy = getCy();
    const selectionRect = rect;
    setRect(null);
    if (!cy || !selectionRect || selectionRect.width < 4 || selectionRect.height < 4) {
      onSelectionChange?.([]);
      return;
    }
    const container = cy.container()?.getBoundingClientRect();
    if (!container) return;
    const selected = [];
    cy.nodes().forEach(node => {
      const rp = node.renderedPosition();
      const x = rp.x + container.left - (shellRef.current?.getBoundingClientRect().left || 0);
      const y = rp.y + container.top - (shellRef.current?.getBoundingClientRect().top || 0);
      if (x >= selectionRect.x && x <= selectionRect.x + selectionRect.width
        && y >= selectionRect.y && y <= selectionRect.y + selectionRect.height) {
        selected.push(node.data('node') || {id: node.id()});
      }
    });
    onSelectionChange?.(selected);
  };

  const collapseSelection = selectedNodes => {
    const members = (selectedNodes || []).filter(node => !groups[node.id]);
    if (members.length < 2) return null;
    groupCounter += 1;
    const groupId = `group:${groupCounter}`;
    const centroid = members.reduce((acc, node) => ({x: acc.x + (node.x || 0) / members.length, y: acc.y + (node.y || 0) / members.length}), {x: 0, y: 0});
    const group = {
      id: groupId,
      name: `Group ${groupCounter} (${members.length})`,
      memberIds: members.map(node => node.id),
      centroid,
    };
    setGroups(prev => ({...prev, [groupId]: group}));
    onCollapse?.(group);
    return group;
  };

  useEffect(() => {
    if (apiRef) apiRef.current = {collapseSelection};
  });

  const expandGroup = groupId => {
    const group = groups[groupId];
    if (!group) return;
    setGroups(prev => {
      const next = {...prev};
      delete next[groupId];
      return next;
    });
    onExpand?.(group);
  };

  const childProps = typeof children === 'function' ? null : children.props;
  const selectNode = node => {
    if (node && typeof node.id === 'string' && node.id.startsWith('group:')) {
      expandGroup(node.id);
      return;
    }
    childProps?.onSelectNode?.(node);
  };

  const child = typeof children === 'function'
    ? children({nodes: visibleNodes, edges: visibleEdges, onSelectNode: selectNode})
    : React.cloneElement(children, {
        nodes: visibleNodes,
        edges: visibleEdges,
        onSelectNode: selectNode,
      });

  return (
    <div
      ref={shellRef}
      className={`lasso-shell ${enabled ? 'lasso-enabled' : ''}`}
      onMouseDown={onMouseDown}
      onMouseMove={onMouseMove}
      onMouseUp={onMouseUp}
    >
      {child}
      {rect && <div className="lasso-rect" style={rect} aria-hidden="true" />}
    </div>
  );
}

export {LassoSelect};
