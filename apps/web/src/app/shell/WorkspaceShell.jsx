import React, {useEffect, useRef, useState} from 'react';
import {Icon, Tip} from '../../icons.jsx';
import {destinations} from '../navigation.ts';

function Tool({label, icon, onClick, disabled}) {
  return <Tip text={label}><button className="icon-button" type="button" aria-label={label}
    title={label} onClick={onClick} disabled={disabled}><Icon name={icon}/></button></Tip>;
}

export default function WorkspaceShell({mode, onNavigate, onRefresh, onDisconnect, busy, children}) {
  const [paletteOpen, setPaletteOpen] = useState(false);
  const [search, setSearch] = useState('');
  const dialogRef = useRef(null);
  const titleRef = useRef(null);
  const routeChosen = useRef(false);
  const current = destinations.find(item => item.id === mode);
  useEffect(() => {
    document.title = `${current?.title || 'Page not found'} | EOIP`;
    titleRef.current?.focus({preventScroll: true});
  }, [mode]);
  useEffect(() => {
    const keydown = event => {
      if ((event.metaKey || event.ctrlKey) && event.key.toLowerCase() === 'k') {
        event.preventDefault();
        setPaletteOpen(value => !value);
      }
    };
    window.addEventListener('keydown', keydown);
    return () => window.removeEventListener('keydown', keydown);
  }, []);
  useEffect(() => {
    if (paletteOpen) dialogRef.current?.showModal();
    else dialogRef.current?.close();
  }, [paletteOpen]);
  function choose(id) {routeChosen.current = true; setPaletteOpen(false); setSearch(''); onNavigate(id);}
  return <div className="atlas-shell">
    <a className="skip-link" href="#workspace-content">Skip to content</a>
    <aside className="atlas-rail">
      <a className="atlas-mark" href="/app" aria-label="EOIP home" onClick={event => {event.preventDefault(); onNavigate('app');}}><Icon name="graph" size={25}/></a>
      <nav aria-label="Primary navigation">{destinations.map(item => <Tip key={item.id} text={item.label}>
        <a href={item.path} className={item.id === mode ? 'active' : ''} aria-label={item.label}
          aria-current={item.id === mode ? 'page' : undefined} title={item.label}
          onClick={event => {if (!event.metaKey && !event.ctrlKey && !event.shiftKey && event.button === 0) {event.preventDefault(); onNavigate(item.id);}}}>
          <Icon name={item.icon} size={20}/><span className="sr-only">{item.label}</span>
        </a></Tip>)}</nav>
    </aside>
    <div className="atlas-workspace">
      <header className="atlas-topbar">
        <div className="atlas-heading"><span>EOIP</span><h1 ref={titleRef} tabIndex={-1}>{current?.title || 'Page not found'}</h1></div>
        <div className="atlas-tools">
          <span className="atlas-context" title="Deployment access; tenant/workspace grants are not available in this login flow">Deployment access</span>
          <Tool label="Open command palette" icon="search" onClick={() => setPaletteOpen(true)}/>
          <Tool label="Refresh live data" icon="refresh" onClick={onRefresh} disabled={busy}/>
          <Tool label="Disconnect this browser session" icon="logout" onClick={onDisconnect}/>
        </div>
      </header>
      <main id="workspace-content" className="atlas-content" tabIndex={-1} aria-busy={busy}>{children}</main>
    </div>
    <dialog ref={dialogRef} className="command-dialog" aria-labelledby="command-title"
      onCancel={() => setPaletteOpen(false)} onClose={() => {
        setPaletteOpen(false);
        if (routeChosen.current) {
          routeChosen.current = false;
          requestAnimationFrame(() => titleRef.current?.focus({preventScroll: true}));
        }
      }}
      onClick={event => {if (event.target === dialogRef.current) setPaletteOpen(false);}}>
      <div className="command-heading"><h2 id="command-title">Go to</h2><Tool label="Close command palette" icon="close" onClick={() => setPaletteOpen(false)}/></div>
      <label className="sr-only" htmlFor="command-search">Find a screen</label>
      <input id="command-search" autoFocus placeholder="Find a screen" value={search} onChange={event => setSearch(event.target.value)}/>
      <nav aria-label="Screen results">{destinations.filter(item => item.label.toLowerCase().includes(search.toLowerCase())).map(item =>
        <button key={item.id} type="button" onClick={() => choose(item.id)}><Icon name={item.icon}/><span>{item.label}</span><Icon name="arrow"/></button>)}
        {!destinations.some(item => item.label.toLowerCase().includes(search.toLowerCase())) && <p role="status">No screens found.</p>}
      </nav>
    </dialog>
  </div>;
}
