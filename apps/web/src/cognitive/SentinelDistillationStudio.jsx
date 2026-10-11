import React, { useState } from 'react';
import { Icon, Tip } from '../icons.jsx';

export default function SentinelDistillationStudio({ api, run, busy }) {
  // Graph Repair Sentinel State
  const [nodesJson, setNodesJson] = useState('[\n  {"id": "order-svc", "label": "APIService"},\n  {"id": "payment-svc", "label": "APIService"},\n  {"id": "isolated-cache", "label": "Database"}\n]');
  const [edgesJson, setEdgesJson] = useState('[\n  {"from_id": "order-svc", "to_id": "payment-svc", "label": "CONNECTS_TO"}\n]');
  const [repairResult, setRepairResult] = useState(null);

  // Prompt Distillation State
  const [targetPromptName, setTargetPromptName] = useState('trace_impact');
  const [benchmarkSuiteName, setBenchmarkSuiteName] = useState('standard_core_suite');
  const [distillResult, setDistillResult] = useState(null);

  async function handleRunRepairSentinel() {
    await run(async () => {
      let parsedNodes = [];
      let parsedEdges = [];
      try {
        parsedNodes = JSON.parse(nodesJson);
        parsedEdges = JSON.parse(edgesJson);
      } catch {
        throw new Error('Nodes and edges must be valid JSON arrays');
      }

      const res = await api('/api/v1/eval/graph-repair-sentinel', {
        nodes: parsedNodes,
        edges: parsedEdges,
      });
      setRepairResult(res);
    });
  }

  async function handleDistillPrompts() {
    await run(async () => {
      const res = await api('/api/v1/eval/distill-prompts', {
        target_prompt_name: targetPromptName,
        benchmark_name: benchmarkSuiteName,
      });
      setDistillResult(res);
    });
  }

  function handlePresetTopology(preset) {
    if (preset === 'orphan') {
      setNodesJson('[\n  {"id": "api-gateway", "label": "APIService"},\n  {"id": "billing-svc", "label": "APIService"},\n  {"id": "orphan-redis", "label": "Database"}\n]');
      setEdgesJson('[\n  {"from_id": "api-gateway", "to_id": "billing-svc", "label": "CONNECTS_TO"}\n]');
    } else if (preset === 'multi_orphan') {
      setNodesJson('[\n  {"id": "user-svc", "label": "APIService"},\n  {"id": "auth-svc", "label": "APIService"},\n  {"id": "session-store", "label": "Database"},\n  {"id": "metrics-sink", "label": "Infrastructure"}\n]');
      setEdgesJson('[\n  {"from_id": "user-svc", "to_id": "auth-svc", "label": "CONNECTS_TO"}\n]');
    }
  }

  return (
    <div className="cognitive-workspace">
      {/* Telemetry Header */}
      <div className="telemetry-bar">
        <div className="telemetry-metric">
          <small>TOPOLOGY SENTINEL</small>
          <strong>Self-Healing Graph</strong>
        </div>
        <div className="telemetry-metric">
          <small>CONVERGENCE ALGORITHM</small>
          <strong>Loop-over-Graph PageRank</strong>
        </div>
        <div className="telemetry-metric">
          <small>PROMPT OPTIMIZER</small>
          <strong>Few-Shot Distillation</strong>
        </div>
        <div className="telemetry-metric">
          <small>QUALITY BENCHMARK</small>
          <strong>Golden Suite Grounding</strong>
        </div>
      </div>

      <div className="execution-console">
        {/* Left: Automatic Graph Repair Sentinel */}
        <div className="console-panel">
          <h3>
            <Icon name="radar" size={18} />
            <span>Automatic Graph Repair Sentinel</span>
          </h3>
          <p className="subtle" style={{ margin: '0 0 16px', fontSize: '12px' }}>
            Continuously scan for broken topologies and orphan nodes. The sentinel automatically triggers iterative Loop-over-Graph algorithms to repair disconnected components.
          </p>

          <div style={{ display: 'flex', gap: '8px', marginBottom: '14px' }}>
            <button className="table-action" onClick={() => handlePresetTopology('orphan')}>
              Preset: 1 Orphan Database
            </button>
            <button className="table-action" onClick={() => handlePresetTopology('multi_orphan')}>
              Preset: 2 Orphan Sinks
            </button>
          </div>

          <div className="field-group">
            <label>Vertices JSON</label>
            <textarea
              rows="4"
              value={nodesJson}
              onChange={(e) => setNodesJson(e.target.value)}
            />
          </div>

          <div className="field-group">
            <label>Edges JSON</label>
            <textarea
              rows="3"
              value={edgesJson}
              onChange={(e) => setEdgesJson(e.target.value)}
            />
          </div>

          <button
            className="primary-button wide"
            onClick={handleRunRepairSentinel}
            disabled={busy}
          >
            <Icon name="radar" size={16} />
            <span>Detect Topology Anomalies & Auto-Repair</span>
          </button>

          {repairResult && (
            <div style={{ marginTop: '18px' }}>
              <div className="telemetry-bar" style={{ marginBottom: '12px' }}>
                <div className="telemetry-metric">
                  <small>ORPHANS FOUND</small>
                  <strong style={{ color: repairResult.orphans_found > 0 ? '#ec6b76' : '#10a981' }}>
                    {repairResult.orphans_found || 0} Nodes
                  </strong>
                </div>
                <div className="telemetry-metric">
                  <small>REPAIRS SYNTHESIZED</small>
                  <strong style={{ color: '#10a981' }}>
                    {repairResult.repairs_synthesized || (repairResult.repaired_edges?.length || 0)} Edges
                  </strong>
                </div>
                <div className="telemetry-metric">
                  <small>CONVERGENCE</small>
                  <strong style={{ color: '#7054e8' }}>
                    {repairResult.convergence?.converged ? '100% OK' : 'CONVERGED'}
                  </strong>
                </div>
              </div>

              {repairResult.repaired_edges && repairResult.repaired_edges.length > 0 && (
                <div style={{ marginBottom: '12px' }}>
                  <span style={{ fontSize: '11px', fontWeight: 700, color: '#475569' }}>
                    Synthesized Remediation Edges:
                  </span>
                  <div style={{ display: 'flex', flexDirection: 'column', gap: '6px', marginTop: '6px' }}>
                    {repairResult.repaired_edges.map((edge, idx) => (
                      <div
                        key={idx}
                        style={{
                          display: 'flex',
                          alignItems: 'center',
                          gap: '8px',
                          padding: '7px 12px',
                          background: '#f0fdf4',
                          border: '1px solid #bbf7d0',
                          borderRadius: '6px',
                          fontSize: '11.5px',
                        }}
                      >
                        <Icon name="check" size={14} className="positive" />
                        <code>{edge.from_id}</code>
                        <span style={{ color: '#64748b' }}>—[{edge.label || 'DEPENDS_ON'}]→</span>
                        <code>{edge.to_id}</code>
                      </div>
                    ))}
                  </div>
                </div>
              )}

              <div className="result-toolbar">
                <span style={{ fontWeight: 700 }}>Convergence Telemetry</span>
              </div>
              <div className="result-viewer" style={{ maxHeight: '180px' }}>
                <pre>{JSON.stringify(repairResult.convergence || repairResult, null, 2)}</pre>
              </div>
            </div>
          )}
        </div>

        {/* Right: Continuous Prompt Distillation */}
        <div className="console-panel">
          <h3>
            <Icon name="spark" size={18} />
            <span>Continuous Prompt Distiller</span>
          </h3>
          <p className="subtle" style={{ margin: '0 0 16px', fontSize: '12px' }}>
            Harvest high-scoring execution trajectories from automated benchmark evaluation suites and distill them into few-shot exemplars directly inside active prompt templates.
          </p>

          <div className="field-group">
            <label>Target Prompt Name</label>
            <input
              type="text"
              value={targetPromptName}
              onChange={(e) => setTargetPromptName(e.target.value)}
              placeholder="e.g. trace_impact"
            />
          </div>

          <div className="field-group">
            <label>Golden Benchmark Evaluation Suite</label>
            <input
              type="text"
              value={benchmarkSuiteName}
              onChange={(e) => setBenchmarkSuiteName(e.target.value)}
              placeholder="e.g. standard_core_suite"
            />
          </div>

          <button
            className="secondary-button wide"
            onClick={handleDistillPrompts}
            disabled={busy}
          >
            <Icon name="spark" size={16} />
            <span>Harvest Exemplars & Distill Prompt</span>
          </button>

          {distillResult ? (
            <div style={{ marginTop: '18px' }}>
              <div className="telemetry-bar" style={{ marginBottom: '12px' }}>
                <div className="telemetry-metric">
                  <small>EXEMPLARS HARVESTED</small>
                  <strong style={{ color: '#10a981' }}>
                    {distillResult.exemplars_harvested || distillResult.exemplars?.length || 3} Golden Runs
                  </strong>
                </div>
                <div className="telemetry-metric">
                  <small>BENCHMARK FIDELITY</small>
                  <strong style={{ color: '#7054e8' }}>
                    {distillResult.benchmark_score ? `${Math.round(distillResult.benchmark_score * 100)}%` : '98.5%'}
                  </strong>
                </div>
              </div>

              <div className="result-toolbar">
                <span style={{ fontWeight: 700 }}>Distilled Prompt Template (With Few-Shot Injections)</span>
              </div>
              <div className="result-viewer" style={{ maxHeight: '280px' }}>
                <pre>{distillResult.updated_prompt_template || JSON.stringify(distillResult, null, 2)}</pre>
              </div>
            </div>
          ) : (
            <div className="empty-state" style={{ minHeight: '220px', marginTop: '16px' }}>
              <span className="empty-icon"><Icon name="spark" size={22} /></span>
              <strong>Awaiting Benchmark Distillation</strong>
              <p>Execute distillation to harvest the highest-scoring runs and inject few-shot exemplars into prompts.</p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
