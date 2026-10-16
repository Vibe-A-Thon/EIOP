import React from 'react';
import {Icon} from '../../icons.jsx';

const MAX_HISTORY = 50;

export function createHistory() {
  return {past: [], future: [], current: null};
}

export function pushState(history, state) {
  const past = history.current ? [...history.past, history.current] : [...history.past];
  return {past: past.slice(-MAX_HISTORY), future: [], current: state};
}

export function undo(history) {
  if (history.past.length === 0) return history;
  const prev = history.past[history.past.length - 1];
  return {
    past: history.past.slice(0, -1),
    future: history.current ? [history.current, ...history.future] : history.future,
    current: prev,
  };
}

export function redo(history) {
  if (history.future.length === 0) return history;
  const next = history.future[0];
  return {
    past: history.current ? [...history.past, history.current] : history.past,
    future: history.future.slice(1),
    current: next,
  };
}

export default function ExplorationHistoryBar({history, onUndo, onRedo}) {
  const canUndo = history.past.length > 0;
  const canRedo = history.future.length > 0;

  return <div className="kgr-history-bar" role="toolbar" aria-label="Exploration history">
    <button onClick={onUndo} disabled={!canUndo} title="Undo (Ctrl+Z)" aria-label="Undo">
      <Icon name="chevron" size={14} style={{transform: 'rotate(180deg)'}}/> Undo
    </button>
    <span className="history-count">{history.past.length} step{history.past.length !== 1 ? 's' : ''}</span>
    <button onClick={onRedo} disabled={!canRedo} title="Redo (Ctrl+Shift+Z)" aria-label="Redo">
      Redo <Icon name="chevron" size={14}/>
    </button>
  </div>;
}
