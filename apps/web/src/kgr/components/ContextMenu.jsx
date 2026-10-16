import React, {useCallback, useEffect, useRef} from 'react';
import {Icon} from '../../icons.jsx';

export default function ContextMenu({x, y, items, onClose}) {
  const ref = useRef(null);

  useEffect(() => {
    const handler = (e) => {
      if (ref.current && !ref.current.contains(e.target)) onClose();
    };
    document.addEventListener('mousedown', handler);
    document.addEventListener('keydown', (e) => { if (e.key === 'Escape') onClose(); });
    return () => {
      document.removeEventListener('mousedown', handler);
    };
  }, [onClose]);

  if (!items || items.length === 0) return null;

  const style = {position: 'fixed', left: x, top: y, zIndex: 9999};

  return <div className="kgr-context-menu" style={style} ref={ref} role="menu">
    {items.map((item, i) => item.divider
      ? <hr key={i} className="context-divider"/>
      : <button key={i} role="menuitem" className="context-item" onClick={() => { item.action(); onClose(); }}
          disabled={item.disabled}>
          {item.icon && <Icon name={item.icon} size={14}/>}
          <span>{item.label}</span>
          {item.shortcut && <kbd>{item.shortcut}</kbd>}
        </button>
    )}
  </div>;
}
