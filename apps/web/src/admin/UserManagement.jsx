import React, {useCallback, useEffect, useState} from 'react';
import {Icon} from '../icons.jsx';

function EmptyState({icon = 'search', title, children}) {
  return <div className="empty-state"><span className="empty-icon"><Icon name={icon} size={22}/></span><strong>{title}</strong><p>{children}</p></div>;
}

export default function UserManagement({api, run, busy}) {
  const [users, setUsers] = useState(null); // null = loading, [] = empty
  const [roles, setRoles] = useState([]);
  const [unavailable, setUnavailable] = useState(false);
  const [error, setError] = useState('');
  const [notice, setNotice] = useState('');
  const [draft, setDraft] = useState({user_id: '', roles: [], attributeKey: '', attributeValue: ''});

  const load = useCallback(async () => {
    setError('');
    setNotice('');
    try {
      const data = await api('/api/v1/authz/users');
      setUsers(Array.isArray(data?.users) ? data.users : []);
      setUnavailable(false);
    } catch (exception) {
      if (exception.message && exception.message.includes('404')) {
        setUnavailable(true);
        setUsers([]);
      } else {
        setError(exception.message || 'The user store could not be loaded.');
      }
    }
    try {
      const roleData = await api('/api/v1/authz/roles');
      setRoles(roleData?.roles || []);
    } catch {
      setRoles([]);
    }
  }, [api]);

  useEffect(() => {load();}, [load]);

  function toggleDraftRole(role) {
    setDraft(current => ({...current, roles: current.roles.includes(role) ? current.roles.filter(item => item !== role) : [...current.roles, role]}));
  }

  async function createUser(event) {
    event.preventDefault();
    const attributes = {};
    if (draft.attributeKey.trim()) attributes[draft.attributeKey.trim()] = draft.attributeValue;
    try {
      await api('/api/v1/authz/users', {user_id: draft.user_id.trim(), roles: draft.roles, attributes});
      setDraft({user_id: '', roles: [], attributeKey: '', attributeValue: ''});
      setNotice(`User created: ${draft.user_id.trim()}`);
      await load();
    } catch (exception) {
      setError(exception.message || 'The user could not be created.');
      setNotice('');
    }
  }

  async function assignRole(user, role) {
    const nextRoles = user.roles?.includes(role) ? user.roles.filter(item => item !== role) : [...(user.roles || []), role];
    try {
      await api('/api/v1/authz/users', {...user, user_id: user.user_id ?? user.id, roles: nextRoles});
      await load();
    } catch (exception) {
      setError(exception.message || 'The role assignment could not be saved.');
    }
  }

  function exportUsers() {
    const anchor = document.createElement('a');
    anchor.href = '/api/v1/authz/users/export';
    anchor.download = 'eoip-authz-users.json';
    anchor.click();
  }

  if (unavailable) {
    return <section className="panel span-3"><div className="panel-heading"><div><span className="eyebrow">ACCESS CONTROL</span><h2>User management</h2><p>Provision users and assign roles from the authorization user store.</p></div></div>
      <EmptyState icon="shield" title="The authz API is not available in this deployment">The <code>/api/v1/authz/users</code> endpoints returned 404. Enable the pass-2 authorization service to manage users from this panel.</EmptyState></section>;
  }

  return <>
    <section className="panel span-2"><div className="panel-heading"><div><span className="eyebrow">IDENTITY STORE</span><h2>Users</h2><p>Users and their role bindings, as reported by the authz service.</p></div><div className="panel-tools"><button className="secondary-button" onClick={() => run(load)} disabled={busy}><Icon name="refresh" size={15}/>Refresh</button><button className="secondary-button" onClick={exportUsers} title="Download the deterministic JSON export from /api/v1/authz/users/export"><Icon name="upload" size={15}/>Export</button><span className="count-badge">{users ? users.length : 0} users</span></div></div>
      {error && <div className="inline-notice warning" role="alert"><Icon name="warning"/>{error}</div>}
      {notice && <div className="inline-notice" role="status"><Icon name="check"/>{notice}</div>}
      {users === null && <div className="inline-notice" role="status"><span className="spinner"/>Loading users…</div>}
      {users !== null && !users.length && <EmptyState icon="shield" title="No users provisioned">Create the first user with the form on this panel; role bindings appear here immediately.</EmptyState>}
      {users !== null && users.length > 0 && <div className="table-wrap"><table><thead><tr><th>User</th><th>Roles</th><th>Attributes</th></tr></thead><tbody>{users.map(user => {
        const id = user.user_id ?? user.id;
        const bound = user.roles || [];
        return <tr key={id}><td><strong>{user.username || id}</strong><small style={{display: 'block'}} title={id}>{id}</small></td>
          <td>{bound.length ? bound.map(role => <span className="badge" key={role} style={{marginRight: 6}}>{role}</span>) : <span className="subtle">No roles</span>}
            <label className="select-control" style={{marginTop: 6}} title="Assign or remove a role for this user"><select value="" onChange={event => event.target.value && assignRole(user, event.target.value)} disabled={busy}><option value="">Assign role…</option>{roles.filter(role => (role.name || role) && !bound.includes(role.name || role)).map(role => {const name = role.name || role; return <option key={name} value={name}>{name}</option>;})}</select></label></td>
          <td>{user.attributes && Object.keys(user.attributes).length ? <code>{JSON.stringify(user.attributes)}</code> : <span className="subtle">—</span>}</td></tr>;
      })}</tbody></table></div>}</section>
    <section className="panel"><div className="panel-heading"><div><span className="eyebrow">PROVISIONING</span><h2>Create user</h2><p>New users are stored in the authz user store with their initial roles.</p></div></div>
      <form className="stack-form" onSubmit={createUser}>
        <label>User ID<input value={draft.user_id} onChange={event => setDraft(current => ({...current, user_id: event.target.value}))} placeholder="jane.doe" required/></label>
        <label>Roles<div>{roles.length ? roles.map(role => {const name = role.name || role; return <label className="toggle" key={name} style={{marginBottom: 6}}><input type="checkbox" checked={draft.roles.includes(name)} onChange={() => toggleDraftRole(name)}/><span/>{name}</label>;}) : <span className="subtle">No roles defined — the user will be created without roles.</span>}</div></label>
        <label>Attribute (optional)<div style={{display: 'flex', gap: 8}}><input value={draft.attributeKey} onChange={event => setDraft(current => ({...current, attributeKey: event.target.value}))} placeholder="department" style={{flex: 1}}/><input value={draft.attributeValue} onChange={event => setDraft(current => ({...current, attributeValue: event.target.value}))} placeholder="engineering" style={{flex: 1}}/></div></label>
        <button className="primary-button" disabled={busy || !draft.user_id.trim()}><Icon name="plus" size={16}/>Create user</button>
      </form></section>
  </>;
}
