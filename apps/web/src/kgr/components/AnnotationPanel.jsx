import React from 'react';

export default function AnnotationPanel({nodeId}) {
  if (!nodeId) return null;

  let savedValue = '';
  try { savedValue = localStorage.getItem(`kgr-note-${nodeId}`) || ''; } catch {}

  return <div className="annotation-panel">
    <p className="subtle">Annotations are stored locally in your browser (max 500 characters).</p>
    <textarea
      placeholder="Add a note about this entity..."
      rows="4"
      maxLength={500}
      defaultValue={savedValue}
      onChange={e => {
        try {
          if (e.target.value) localStorage.setItem(`kgr-note-${nodeId}`, e.target.value);
          else localStorage.removeItem(`kgr-note-${nodeId}`);
        } catch {}
      }}
    />
    <small className="annotation-hint">Annotations are included in export reports when "Include annotations" is checked.</small>
  </div>;
}
