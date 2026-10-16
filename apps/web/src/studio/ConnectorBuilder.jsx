import React, {useEffect, useMemo, useState} from 'react';
import {Icon, Tip} from '../icons.jsx';
import {downloadJson, loadArtifacts, saveArtifacts, uid} from './studio-utils.js';

const FALLBACK_SOURCES = [
  {id: 'jira', name: 'Jira', type: 'api'},
  {id: 'gitlab', name: 'GitLab', type: 'api'},
  {id: 'github', name: 'GitHub', type: 'api'},
  {id: 'confluence', name: 'Confluence', type: 'api'},
  {id: 'servicenow', name: 'ServiceNow', type: 'api'},
  {id: 'web', name: 'Web Crawler', type: 'crawler'},
  {id: 'local_code', name: 'Local Code', type: 'file'},
  {id: 'generic', name: 'Generic JSON', type: 'json'},
];

const AUTH_TYPES = ['none', 'token', 'basic', 'oauth2'];
const STEPS = ['Source', 'Connection', 'Auth', 'Scope'];

export default function ConnectorBuilder({api, run}) {
  const [step, setStep] = useState(0);
  const [sources, setSources] = useState(FALLBACK_SOURCES);
  const [catalogError, setCatalogError] = useState('');
  const [sourceId, setSourceId] = useState('jira');
  const [name, setName] = useState('');
  const [connection, setConnection] = useState([{key: 'base_url', value: ''}]);
  const [authType, setAuthType] = useState('token');
  const [authFields, setAuthFields] = useState([{key: 'token', value: '', secret: true}]);
  const [scope, setScope] = useState({projects: '', entities: 'requirement,issue', since: '', poll_interval_minutes: '60'});
  const [saved, setSaved] = useState(() => loadArtifacts('eoip-studio-connectors'));

  useEffect(() => {
    if (!api) return;
    run(async () => {
      try {
        const catalog = await api('/api/v1/connectors/catalog');
        if (catalog?.connectors?.length) setSources(catalog.connectors);
      } catch (exception) {
        setCatalogError(exception.message || 'Connector catalog unavailable; using built-in defaults.');
      }
    });
  }, [api]);

  const source = sources.find(item => item.id === sourceId);

  const manifest = useMemo(() => ({
    format: 'eoip.connector-manifest.v1',
    id: uid('connector'),
    name: name || `${source?.name || sourceId} connector`,
    source_type: source?.type || 'api',
    source: sourceId,
    connection: Object.fromEntries(connection.filter(row => row.key.trim()).map(row => [row.key.trim(), row.value])),
    auth: {
      type: authType,
      ...(authType === 'none' ? {} : {fields: Object.fromEntries(authFields.filter(row => row.key.trim()).map(row => [row.key.trim(), row.secret ? '<redacted>' : row.value]))}),
    },
    scope: Object.fromEntries(Object.entries(scope).filter(([, value]) => value !== '')),
  }), [name, source, sourceId, connection, authType, authFields, scope]);

  const validation = useMemo(() => {
    const problems = [];
    if (!manifest.name.trim()) problems.push('Name is required.');
    if (authType !== 'none' && !authFields.some(row => row.key.trim())) problems.push('At least one auth field is required for auth type "' + authType + '".');
    if (source?.type === 'api' && !connection.some(row => row.key.trim() === 'base_url' && row.value.trim())) problems.push('Connection parameter "base_url" is required for API sources.');
    if (!manifest.scope.entities) problems.push('Scope must list at least one entity type.');
    return problems;
  }, [manifest, authType, authFields, connection, source]);

  function kvEditor(rows, setRows, allowSecret = false) {
    return <div>
      {rows.map((row, index) => <div className="studio-kv" key={index}>
        <input type="text" value={row.key} placeholder="key" aria-label="Parameter key"
          onChange={event => setRows(list => list.map((item, i) => i === index ? {...item, key: event.target.value} : item))}/>
        <input type={row.secret ? 'password' : 'text'} value={row.value} placeholder={row.secret ? 'secret value' : 'value'} aria-label="Parameter value"
          onChange={event => setRows(list => list.map((item, i) => i === index ? {...item, value: event.target.value} : item))}/>
        <span className="studio-row">
          {allowSecret && <Tip text="Treat as secret"><button type="button" className={`ghost-button ${row.secret ? 'active' : ''}`} onClick={() => setRows(list => list.map((item, i) => i === index ? {...item, secret: !item.secret} : item))}><Icon name="shield" size={13}/></button></Tip>}
          <button type="button" className="icon-button" aria-label="Remove row" onClick={() => setRows(list => list.filter((_, i) => i !== index))}><Icon name="minus" size={13}/></button>
        </span>
      </div>)}
      <button type="button" className="ghost-button" onClick={() => setRows(list => [...list, {key: '', value: '', secret: false}])}><Icon name="plus" size={13}/> Add field</button>
    </div>;
  }

  function download() {
    downloadJson(`${manifest.name.replace(/\W+/g, '-').toLowerCase() || 'connector'}.manifest.json`, manifest);
  }

  function saveToLibrary() {
    if (validation.length) return;
    const next = [manifest, ...saved.filter(item => item.name !== manifest.name)].slice(0, 30);
    setSaved(next);
    saveArtifacts('eoip-studio-connectors', next);
  }

  return <div>
    {catalogError && <div className="studio-warn"><Icon name="info" size={16}/><span>{catalogError}</span></div>}
    <div className="studio-steps" aria-label="Wizard progress">
      {STEPS.map((label, index) => <span key={label} className={index === step ? 'active' : ''}>{index + 1}. {label}</span>)}
    </div>
    <div className="studio-grid">
      <section className="studio-panel">
        {step === 0 && <div>
          <h3><Icon name="database" size={15}/> Source type</h3>
          <div className="studio-field"><span>Connector</span>
            <select value={sourceId} onChange={event => setSourceId(event.target.value)}>
              {sources.map(item => <option key={item.id} value={item.id}>{item.name} ({item.type})</option>)}
            </select>
          </div>
          <div className="studio-field"><span>Manifest name</span>
            <input type="text" value={name} onChange={event => setName(event.target.value)} placeholder={`${source?.name || sourceId} connector`}/>
          </div>
        </div>}
        {step === 1 && <div>
          <h3><Icon name="settings" size={15}/> Connection parameters</h3>
          {kvEditor(connection, setConnection)}
        </div>}
        {step === 2 && <div>
          <h3><Icon name="shield" size={15}/> Authentication</h3>
          <div className="studio-field"><span>Auth type</span>
            <select value={authType} onChange={event => {
              setAuthType(event.target.value);
              setAuthFields(event.target.value === 'basic'
                ? [{key: 'username', value: '', secret: false}, {key: 'password', value: '', secret: true}]
                : event.target.value === 'oauth2'
                  ? [{key: 'client_id', value: '', secret: false}, {key: 'client_secret', value: '', secret: true}]
                  : [{key: 'token', value: '', secret: true}]);
            }}>
              {AUTH_TYPES.map(type => <option key={type} value={type}>{type}</option>)}
            </select>
          </div>
          {authType !== 'none' && kvEditor(authFields, setAuthFields, true)}
        </div>}
        {step === 3 && <div>
          <h3><Icon name="focus" size={15}/> Scope</h3>
          {Object.entries(scope).map(([key, value]) => <div className="studio-field" key={key}>
            <span>{key.replaceAll('_', ' ')}</span>
            <input type="text" value={value} onChange={event => setScope({...scope, [key]: event.target.value})}/>
          </div>)}
        </div>}
        <div className="studio-row" style={{marginTop: 12}}>
          <button type="button" className="ghost-button" onClick={() => setStep(step - 1)} disabled={step === 0}>Back</button>
          <button type="button" className="primary-button" onClick={() => setStep(step + 1)} disabled={step === STEPS.length - 1}>Next <Icon name="chevron" size={14}/></button>
        </div>
      </section>
      <section className="studio-panel">
        <h3><Icon name="document" size={15}/> Manifest preview</h3>
        {validation.length > 0 && <div className="studio-warn"><Icon name="warning" size={16}/><div>{validation.map((problem, index) => <div key={index}>{problem}</div>)}</div></div>}
        <pre className="studio-json">{JSON.stringify(manifest, null, 2)}</pre>
        <div className="studio-row" style={{marginTop: 10}}>
          <button type="button" className="primary-button" onClick={download} disabled={validation.length > 0}><Icon name="upload" size={15}/> Download manifest</button>
          <button type="button" className="ghost-button" onClick={saveToLibrary} disabled={validation.length > 0}>Save to library</button>
        </div>
        <p className="studio-hint">Saved manifests appear in the Pipeline Orchestrator as connector nodes. Secret values are redacted from the exported manifest.</p>
      </section>
    </div>
    <section className="studio-panel" style={{marginTop: 14}}>
      <h3><Icon name="database" size={15}/> Saved connectors</h3>
      {saved.length === 0 && <div className="studio-empty"><strong>No saved connectors</strong>Finish the wizard and choose "Save to library".</div>}
      <ul className="studio-list">{saved.map(item => <li key={item.id}>
        <span><strong>{item.name}</strong> <span className="studio-latency">{item.source}</span></span>
        <button type="button" className="icon-button" aria-label={`Remove ${item.name}`} onClick={() => {
          const next = saved.filter(entry => entry.id !== item.id);
          setSaved(next);
          saveArtifacts('eoip-studio-connectors', next);
        }}><Icon name="close" size={14}/></button>
      </li>)}</ul>
    </section>
  </div>;
}
