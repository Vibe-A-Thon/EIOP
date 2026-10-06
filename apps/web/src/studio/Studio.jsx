import React, {useState} from 'react';
import {Icon, Tip} from '../icons.jsx';
import SchemaCanvas from './SchemaCanvas.jsx';
import QueryConsole from './QueryConsole.jsx';
import ConnectorBuilder from './ConnectorBuilder.jsx';
import MappingDesigner from './MappingDesigner.jsx';
import PipelineOrchestrator from './PipelineOrchestrator.jsx';
import './studio.css';

const TABS = [
  {id: 'schema', label: 'Schema Canvas', icon: 'layers', hint: 'GAP-STUDIO-002 — drag-and-drop ontology schema builder with JSON draft export'},
  {id: 'query', label: 'Query Console', icon: 'terminal', hint: 'GAP-STUDIO-003 — live EQL / guarded query console with history and latency'},
  {id: 'connector', label: 'Connector Builder', icon: 'database', hint: 'GAP-NOCODE-001 — no-code connector manifest wizard'},
  {id: 'mapping', label: 'Mapping Designer', icon: 'link', hint: 'GAP-NOCODE-002 — field-to-vertex/edge mapping designer'},
  {id: 'pipeline', label: 'Pipeline Orchestrator', icon: 'activity', hint: 'GAP-NOCODE-003 — visual DAG editor for ingestion pipelines'},
];

/**
 * Ontology Studio — composes the schema canvas, query console, and the
 * no-code builders behind a tab bar.
 *
 * Props:
 *   api  — async (path, body?, method?) => data, same signature as App.jsx's api helper
 *   run  — async action wrapper that surfaces errors through the app toast
 *   busy — global busy flag used to disable run buttons
 */
export default function Studio({api, run, busy}) {
  const [tab, setTab] = useState('schema');
  return <div>
    <div className="studio-tabs" role="tablist" aria-label="Ontology Studio">
      {TABS.map(item => <Tip key={item.id} text={item.hint}>
        <button type="button" role="tab" aria-selected={tab === item.id} className={tab === item.id ? 'active' : ''} onClick={() => setTab(item.id)}>
          <Icon name={item.icon} size={15}/>{item.label}
        </button>
      </Tip>)}
    </div>
    {tab === 'schema' && <SchemaCanvas api={api} run={run}/>}
    {tab === 'query' && <QueryConsole api={api} run={run} busy={busy}/>}
    {tab === 'connector' && <ConnectorBuilder api={api} run={run}/>}
    {tab === 'mapping' && <MappingDesigner api={api} run={run}/>}
    {tab === 'pipeline' && <PipelineOrchestrator/>}
  </div>;
}
