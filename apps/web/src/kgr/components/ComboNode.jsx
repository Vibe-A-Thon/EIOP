import React, {useCallback, useMemo, useState} from 'react';
import {Icon} from '../../icons.jsx';

export function groupByDomain(elements) {
  const groups = {};
  for (const n of elements) {
    const d = n.domain || 'OTHER';
    if (!groups[d]) groups[d] = {id: `combo:domain:${d}`, name: d, memberIds: []};
    groups[d].memberIds.push(n.id);
  }
  return Object.values(groups).filter(g => g.memberIds.length > 1);
}

export function groupByType(elements) {
  const groups = {};
  for (const n of elements) {
    const t = n.label || 'Unknown';
    if (!groups[t]) groups[t] = {id: `combo:type:${t}`, name: t, memberIds: []};
    groups[t].memberIds.push(n.id);
  }
  return Object.values(groups).filter(g => g.memberIds.length > 1);
}

export function groupByCommunity(elements, communities) {
  if (!communities?.length) return [];
  return communities.map(c => ({
    id: `combo:community:${c.community_id ?? c.id}`,
    name: c.auto_label || `Community ${c.community_id ?? c.id}`,
    memberIds: c.members || [],
  })).filter(g => g.memberIds.length > 1);
}

export function createCustomGroup(selectedIds, name) {
  return {id: `combo:custom:${Date.now()}`, name, memberIds: [...selectedIds]};
}

export function applyComboNodes(nodes, edges, groups) {
  if (!groups?.length) return {nodes, edges};
  const memberToGroup = {};
  for (const g of groups) {
    for (const mid of g.memberIds) memberToGroup[mid] = g.id;
  }

  const comboNodes = groups.map(g => ({
    id: g.id, label: 'ComboNode', domain: g.name,
    properties: {name: g.name, member_count: g.memberIds.length, display_name: g.name},
    isCombo: true, memberIds: g.memberIds,
  }));

  const remainingNodes = nodes.filter(n => !memberToGroup[n.id]);
  const superEdges = {};
  const remainingEdges = [];
  for (const e of edges) {
    const fromGroup = memberToGroup[e.from_id];
    const toGroup = memberToGroup[e.to_id];
    if (fromGroup && toGroup && fromGroup === toGroup) continue;
    const srcId = fromGroup || e.from_id;
    const tgtId = toGroup || e.to_id;
    const key = `${srcId}|${tgtId}|${e.type}`;
    if (fromGroup || toGroup) {
      if (!superEdges[key]) superEdges[key] = {from_id: srcId, to_id: tgtId, type: e.type, id: key, count: 0, isSuperEdge: true};
      superEdges[key].count++;
    } else {
      remainingEdges.push(e);
    }
  }
  return {
    nodes: [...remainingNodes, ...comboNodes],
    edges: [...remainingEdges, ...Object.values(superEdges)],
  };
}

export default function ComboNode({groups, onToggleExpand, onRemoveGroup}) {
  if (!groups?.length) return null;
  return <div className="combo-controls">
    <div className="combo-header"><Icon name="layers" size={14}/><span>Node Groups ({groups.length})</span></div>
    {groups.map(g => <div key={g.id} className="combo-group-row">
      <strong>{g.name}</strong>
      <span className="combo-badge">{g.memberIds.length}</span>
      <button className="icon-button" onClick={() => onToggleExpand && onToggleExpand(g.id)} title="Toggle expand"><Icon name="graph" size={12}/></button>
      <button className="icon-button" onClick={() => onRemoveGroup && onRemoveGroup(g.id)} title="Remove group"><Icon name="close" size={12}/></button>
    </div>)}
  </div>;
}
