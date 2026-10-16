import React, { useState } from 'react';
import { Icon, Tip } from '../icons.jsx';

const disciplines = [
  {
    id: 'loop',
    name: 'Loop Engineering',
    category: 'Agentic Control',
    icon: 'refresh',
    tone: 'violet',
    endpoint: '/api/v1/graph-loop/execute',
    method: 'POST',
    desc: 'Bounded execution primitives with invariant checking, convergence criteria, and cycle prevention.',
    defaultBody: { mode: 'GRAPH_OVER_LOOP', query: 'service_dependencies', seed_ids: ['order-svc', 'payment-svc'], max_iterations: 5 },
  },
  {
    id: 'graph',
    name: 'Graph Engineering',
    category: 'Knowledge Structure',
    icon: 'graph',
    tone: 'blue',
    endpoint: '/api/v1/graph/schema',
    method: 'GET',
    desc: 'Typed multi-relational property graph topologies, semantic traversal paths, and ontology schema contracts.',
    defaultBody: null,
  },
  {
    id: 'harness',
    name: 'Harness Engineering',
    category: 'Execution Pipeline',
    icon: 'cpu',
    tone: 'teal',
    endpoint: '/api/v1/demo/scenarios',
    method: 'GET',
    desc: 'Deterministic test harness, DAG stage execution, topological sort, and live pipeline telemetry.',
    defaultBody: null,
  },
  {
    id: 'memory',
    name: 'Memory Engineering',
    category: 'Cognitive Memory',
    icon: 'database',
    tone: 'amber',
    endpoint: '/api/v1/memory/recall',
    method: 'POST',
    desc: 'Tiered memory retrieval (working, episodic, semantic) with semantic decay, salience, and deduplication.',
    defaultBody: { query: 'checkout deployment transaction', tier: 'WORKING', limit: 5 },
  },
  {
    id: 'context',
    name: 'Context Engineering',
    category: 'Context Synthesis',
    icon: 'layers',
    tone: 'violet',
    endpoint: '/api/v1/context/slice-graph',
    method: 'POST',
    desc: 'Token budgeting, priority ranking, SHA-256 deduplication, and compressed markdown slate generation.',
    defaultBody: { query: 'payment gateway failover', seed_ids: ['checkout-api'], attention_threshold: 0.15 },
  },
  {
    id: 'prompt',
    name: 'Prompt Engineering',
    category: 'System Directives',
    icon: 'spark',
    tone: 'rose',
    endpoint: '/api/v1/eval/distill-prompts',
    method: 'POST',
    desc: 'Template compilation, few-shot exemplar injection, defense hardening, and dynamic variable binding.',
    defaultBody: { target_prompt_name: 'trace_impact', benchmark_name: 'standard_core_suite' },
  },
  {
    id: 'graph-over-loop',
    name: 'Graph-over-Loop Engineering',
    category: 'Composite Control',
    icon: 'gitBranch',
    tone: 'blue',
    endpoint: '/api/v1/graph-loop/execute',
    method: 'POST',
    desc: 'Topological DAG traversal where each graph vertex invokes a bounded deterministic execution loop.',
    defaultBody: { mode: 'GRAPH_OVER_LOOP', query: 'impact_trace', seed_ids: ['inventory-db'], max_iterations: 4 },
  },
  {
    id: 'loop-over-graph',
    name: 'Loop-over-Graph Engineering',
    category: 'Composite Control',
    icon: 'radar',
    tone: 'teal',
    endpoint: '/api/v1/graph-loop/execute',
    method: 'POST',
    desc: 'Iterative convergence algorithms (PageRank, Bellman-Ford, community discovery) across full graphs.',
    defaultBody: { mode: 'LOOP_OVER_GRAPH', query: 'pagerank_centrality', seed_ids: ['auth-svc', 'api-gw'], max_iterations: 6, convergence_threshold: 0.005 },
  },
  {
    id: 'eval',
    name: 'Evaluation & Benchmarking',
    category: 'Quality Assurance',
    icon: 'shieldCheck',
    tone: 'teal',
    endpoint: '/api/v1/eval/suite/run',
    method: 'POST',
    desc: 'Automated golden regression suites, multi-judge consensus, semantic faithfulness, and pass/fail quality gates.',
    defaultBody: { benchmark_name: 'standard_core_suite' },
  },
  {
    id: 'state',
    name: 'State & Persistence Engineering',
    category: 'Storage & History',
    icon: 'clock',
    tone: 'amber',
    endpoint: '/api/v1/context/bitemporal-slate',
    method: 'POST',
    desc: 'Event-sourced state stores, time-travel point-in-time state reconstruction, and historical diffing.',
    defaultBody: { stream: 'deployment_stream_01', past_timestamp: 1710000000.0, present_timestamp: 1710003600.0 },
  },
  {
    id: 'tools',
    name: 'Tool & API Contracts (MCP)',
    category: 'Interoperability',
    icon: 'code',
    tone: 'blue',
    endpoint: '/api/v1/tools/list',
    method: 'GET',
    desc: 'Strict JSON Schema input/output definitions, runtime validation gates, and MCP 2024-11-05 protocol compliance.',
    defaultBody: null,
  },
  {
    id: 'security',
    name: 'Security & Red-Teaming',
    category: 'Cyber Resilience',
    icon: 'shield',
    tone: 'rose',
    endpoint: '/api/v1/guardrails/reflection-sandbox',
    method: 'POST',
    desc: 'Autonomous reflection sandboxing, role isolation, prompt injection inoculation, and payload screening.',
    defaultBody: { step_id: 'step-sec-01', action_type: 'MUTATE', target_entity: 'ServiceConfig', proposed_payload: { role: 'operator', timeout: 30 }, agent_role: 'operator' },
  },
  {
    id: 'economics',
    name: 'Cost & Latency Optimization',
    category: 'Economics & Scale',
    icon: 'chart',
    tone: 'teal',
    endpoint: '/api/v1/tools/stats',
    method: 'GET',
    desc: 'Token economics, semantic prompt caching, TTFT / inter-token latency modeling, and compute tier routing.',
    defaultBody: null,
  },
  {
    id: 'feature',
    name: 'Feature Engineering',
    category: 'Machine Learning',
    icon: 'sliders',
    tone: 'violet',
    endpoint: '/api/v1/context/slice-graph',
    method: 'POST',
    desc: 'Graph structural embeddings, centrality metrics, topological node features, and vector representations.',
    defaultBody: { query: 'cluster_features', seed_ids: ['api-gw'], attention_threshold: 0.1 },
  },
  {
    id: 'spec',
    name: 'Spec Engineering',
    category: 'Formal Contracts',
    icon: 'document',
    tone: 'blue',
    endpoint: '/api/v1/graph/schema',
    method: 'GET',
    desc: 'Formal semantic invariants, schema conformance verification, and machine-verifiable operational specs.',
    defaultBody: null,
  },
];

export default function DisciplineMatrix({ api, run, busy }) {
  const [selectedDiscipline, setSelectedDiscipline] = useState(disciplines[0]);
  const [requestPayload, setRequestPayload] = useState(JSON.stringify(disciplines[0].defaultBody, null, 2));
  const [responseResult, setResponseResult] = useState(null);
  const [execDuration, setExecDuration] = useState(null);
  const [copied, setCopied] = useState(false);

  function handleSelect(discipline) {
    setSelectedDiscipline(discipline);
    setRequestPayload(discipline.defaultBody ? JSON.stringify(discipline.defaultBody, null, 2) : '');
    setResponseResult(null);
    setExecDuration(null);
  }

  async function handleExecute() {
    await run(async () => {
      const startTime = performance.now();
      let bodyData = undefined;
      if (selectedDiscipline.method === 'POST') {
        try {
          bodyData = requestPayload ? JSON.parse(requestPayload) : {};
        } catch {
          throw new Error('Invalid JSON payload in execution configuration');
        }
      }
      const data = await api(selectedDiscipline.endpoint, bodyData, selectedDiscipline.method);
      const endTime = performance.now();
      setExecDuration(Math.round(endTime - startTime));
      setResponseResult(data);
    });
  }

  function handleCopy() {
    if (!responseResult) return;
    navigator.clipboard.writeText(JSON.stringify(responseResult, null, 2));
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  }

  return (
    <div className="cognitive-workspace">
      {/* 15 Disciplines Matrix Cards */}
      <div className="disciplines-grid">
        {disciplines.map((d) => {
          const isSelected = selectedDiscipline.id === d.id;
          return (
            <div
              key={d.id}
              className={`discipline-card ${isSelected ? 'selected' : ''}`}
              onClick={() => handleSelect(d)}
            >
              <div className="discipline-header">
                <span className={`discipline-icon-badge ${d.tone}`}>
                  <Icon name={d.icon} size={20} />
                </span>
                <span className="discipline-badge success">
                  <Icon name="check" size={12} /> 100% COMPLETE
                </span>
              </div>
              <h4 className="discipline-title">{d.name}</h4>
              <p className="discipline-desc">{d.desc}</p>
              <div className="discipline-footer">
                <span className="subtle">{d.category}</span>
                <code>{d.method} {d.endpoint.split('/').pop()}</code>
              </div>
            </div>
          );
        })}
      </div>

      {/* Interactive Execution Console */}
      <div className="execution-console">
        <div className="console-panel">
          <h3>
            <Icon name="play" size={17} />
            <span>Execute & Test: {selectedDiscipline.name}</span>
          </h3>
          <p className="subtle" style={{ margin: '0 0 16px', fontSize: '12px' }}>
            Trigger a live execution directly against the authoritative platform engine via <code>{selectedDiscipline.endpoint}</code>.
          </p>

          <div className="field-group">
            <label>Endpoint & Protocol</label>
            <input
              type="text"
              readOnly
              value={`${selectedDiscipline.method} ${selectedDiscipline.endpoint}`}
              style={{ background: '#f1f5f9' }}
            />
          </div>

          {selectedDiscipline.method === 'POST' && (
            <div className="field-group">
              <label>Request JSON Payload</label>
              <textarea
                rows="7"
                value={requestPayload}
                onChange={(e) => setRequestPayload(e.target.value)}
                placeholder="Enter JSON request payload"
              />
            </div>
          )}

          <div className="console-actions">
            <button
              className="primary-button wide"
              onClick={handleExecute}
              disabled={busy}
            >
              <Icon name="play" size={15} />
              <span>Execute {selectedDiscipline.name}</span>
            </button>
          </div>
        </div>

        <div className="console-panel">
          <div className="result-toolbar">
            <span style={{ fontWeight: 700, color: '#334155' }}>
              Execution Telemetry & Output
            </span>
            {execDuration !== null && (
              <span className="discipline-badge success">
                <Icon name="clock" size={12} /> {execDuration}ms
              </span>
            )}
            {responseResult && (
              <button
                className="table-action"
                onClick={handleCopy}
                style={{ marginLeft: 'auto', border: 0, background: 'none' }}
              >
                <Icon name={copied ? 'check' : 'copy'} size={14} />
                <span>{copied ? 'Copied' : 'Copy JSON'}</span>
              </button>
            )}
          </div>

          {responseResult ? (
            <div className="result-viewer">
              <pre>{JSON.stringify(responseResult, null, 2)}</pre>
            </div>
          ) : (
            <div className="empty-state" style={{ minHeight: '260px' }}>
              <span className="empty-icon"><Icon name="terminal" size={24} /></span>
              <strong>Ready for Execution</strong>
              <p>Configure parameters on the left and click execute to view live telemetry and data response.</p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
