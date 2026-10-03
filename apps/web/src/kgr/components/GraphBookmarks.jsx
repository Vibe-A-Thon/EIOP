import React, {useCallback, useEffect, useState} from 'react';
import {Icon} from '../../icons.jsx';

const STORAGE_KEY = 'kgr-bookmarks';
const MAX_BOOKMARKS = 20;

function loadBookmarks() {
  try { return JSON.parse(localStorage.getItem(STORAGE_KEY) || '[]'); } catch { return []; }
}

function saveBookmarks(bm) {
  try { localStorage.setItem(STORAGE_KEY, JSON.stringify(bm)); } catch {}
}

export default function GraphBookmarks({currentState, onRestore}) {
  const [bookmarks, setBookmarks] = useState(() => loadBookmarks());
  const [showSave, setShowSave] = useState(false);
  const [name, setName] = useState('');

  useEffect(() => { saveBookmarks(bookmarks); }, [bookmarks]);

  const addBookmark = useCallback(() => {
    if (!name.trim() || !currentState) return;
    const bm = {name: name.trim(), state: currentState, created: new Date().toISOString()};
    setBookmarks(prev => [bm, ...prev].slice(0, MAX_BOOKMARKS));
    setName('');
    setShowSave(false);
  }, [name, currentState]);

  const removeBookmark = useCallback((index) => {
    setBookmarks(prev => prev.filter((_, i) => i !== index));
  }, []);

  const exportBookmarks = useCallback(() => {
    const blob = new Blob([JSON.stringify(bookmarks, null, 2)], {type: 'application/json'});
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url; a.download = 'kgr-bookmarks.json'; a.click();
    URL.revokeObjectURL(url);
  }, [bookmarks]);

  const importBookmarks = useCallback((e) => {
    const file = e.target.files?.[0];
    if (!file) return;
    const reader = new FileReader();
    reader.onload = () => {
      try {
        const imported = JSON.parse(reader.result);
        if (Array.isArray(imported)) setBookmarks(prev => [...imported, ...prev].slice(0, MAX_BOOKMARKS));
      } catch {}
    };
    reader.readAsText(file);
  }, []);

  return <div className="kgr-bookmarks">
    <div className="bookmarks-bar">
      {bookmarks.map((bm, i) =>
        <button key={i} className="bookmark-chip" onClick={() => onRestore(bm.state)} title={bm.name}>
          <Icon name="layers" size={12}/>{bm.name}
          <span className="bookmark-remove" onClick={(e) => { e.stopPropagation(); removeBookmark(i); }}>&times;</span>
        </button>
      )}
      <button className="bookmark-add" onClick={() => setShowSave(!showSave)} title="Save bookmark">
        <Icon name="check" size={12}/> Save
      </button>
      {bookmarks.length > 0 && <button className="bookmark-export" onClick={exportBookmarks} title="Export bookmarks">
        <Icon name="database" size={12}/>
      </button>}
    </div>
    {showSave && <div className="bookmark-save-form">
      <input type="text" placeholder="Bookmark name..." value={name} onChange={e => setName(e.target.value)}
        onKeyDown={e => { if (e.key === 'Enter') addBookmark(); }} autoFocus aria-label="Bookmark name"/>
      <button onClick={addBookmark} disabled={!name.trim()}>Save</button>
      <button onClick={() => setShowSave(false)}>Cancel</button>
    </div>}
  </div>;
}
