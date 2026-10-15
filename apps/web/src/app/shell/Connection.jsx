import React, {useState} from 'react';
import {Icon} from '../../icons.jsx';

export default function Connection({token, setToken, onSubmit, busy, health}) {
  const [visible, setVisible] = useState(false);
  return <main className="connection-page">
    <div className="connection-brand"><Icon name="graph" size={28}/><strong>EOIP</strong></div>
    <section className="connection-form" aria-labelledby="connection-title">
      <h1 id="connection-title">Connect to EOIP</h1>
      <p className="connection-status"><span className={`health-orb ${health === 'ready' ? 'online' : ''}`}/>
        {health === 'ready' ? 'Local services are ready' : health === 'checking' ? 'Checking local services' : 'Service status unavailable'}
      </p>
      <form onSubmit={onSubmit}>
        <label htmlFor="token">Access token</label>
        <div className="connection-secret">
          <input id="token" type={visible ? 'text' : 'password'} value={token}
            autoComplete="off" spellCheck={false} required onChange={event => setToken(event.target.value)}
            aria-describedby="connection-note"/>
          <button type="button" className="icon-button" aria-label={visible ? 'Hide token' : 'Show token'}
            title={visible ? 'Hide token' : 'Show token'} onClick={() => setVisible(value => !value)}>
            <Icon name={visible ? 'eyeOff' : 'eye'}/>
          </button>
        </div>
        <p id="connection-note" className="subtle">Deployment access. Your token remains in memory until you disconnect or reload.</p>
        <button className="primary-button" disabled={busy || !token.trim()}>
          {busy ? <><Icon name="refresh" className="rotating"/>Connecting...</> : <>Connect<Icon name="arrow"/></>}
        </button>
      </form>
    </section>
  </main>;
}
