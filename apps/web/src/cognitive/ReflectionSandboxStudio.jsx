import React, { useState } from 'react';
import { Icon, Tip } from '../icons.jsx';

export default function ReflectionSandboxStudio({ api, run, busy }) {
  // Sandbox State
  const [stepId, setStepId] = useState('agent-step-101');
  const [agentRole, setAgentRole] = useState('operator');
  const [actionType, setActionType] = useState('MUTATE');
  const [targetEntity, setTargetEntity] = useState('APIService');
  const [payloadText, setPayloadText] = useState('{\n  "service_name": "checkout-api",\n  "version": "v2.1",\n  "timeout_ms": 3000\n}');
  const [sandboxResult, setSandboxResult] = useState(null);

  // Inoculator State
  const [targetPrompt, setTargetPrompt] = useState('trace_impact');
  const [inoculationResult, setInoculationResult] = useState(null);
  const [copiedShield, setCopiedShield] = useState(false);

  async function handleRunSandbox() {
    await run(async () => {
      let parsedPayload = {};
      try {
        parsedPayload = JSON.parse(payloadText);
      } catch {
        throw new Error('Payload must be valid JSON');
      }

      const res = await api('/api/v1/guardrails/reflection-sandbox', {
        step_id: stepId,
        action_type: actionType,
        target_entity: targetEntity,
        proposed_payload: parsedPayload,
        agent_role: agentRole,
        state: { last_executed_step: 'agent-step-100' },
      });
      setSandboxResult(res);
    });
  }

  async function handleInoculatePrompt() {
    await run(async () => {
      const res = await api('/api/v1/guardrails/inoculate', {
        target_prompt_name: targetPrompt,
      });
      setInoculationResult(res);
    });
  }

  function handleQuickPreset(type) {
    if (type === 'safe') {
      setAgentRole('operator');
      setActionType('MUTATE');
      setTargetEntity('APIService');
      setPayloadText('{\n  "service_name": "inventory-svc",\n  "status": "ACTIVE"\n}');
    } else if (type === 'forbidden_entity') {
      setAgentRole('operator');
      setActionType('MUTATE');
      setTargetEntity('ProductionSecrets');
      setPayloadText('{\n  "export_keys": true,\n  "target": "external"\n}');
    } else if (type === 'role_violation') {
      setAgentRole('analyst');
      setActionType('DELETE');
      setTargetEntity('APIService');
      setPayloadText('{\n  "force_delete": true\n}');
    }
  }

  return (
    <div className="cognitive-workspace">
      {/* Overview Cards */}
      <div className="telemetry-bar">
        <div className="telemetry-metric">
          <small>INVARIANCE ENGINE</small>
          <strong>Bounded Sandbox</strong>
        </div>
        <div className="telemetry-metric">
          <small>PROTECTED ROLES</small>
          <strong>RBAC + Mutation Gates</strong>
        </div>
        <div className="telemetry-metric">
          <small>CYCLE DETECTOR</small>
          <strong>Loop Invariant Guard</strong>
        </div>
        <div className="telemetry-metric">
          <small>ADVERSARIAL DEFENSE</small>
          <strong>Dynamic Inoculator</strong>
        </div>
      </div>

      <div className="execution-console">
        {/* Left: Reflection Sandbox Workbench */}
        <div className="console-panel">
          <h3>
            <Icon name="lock" size={18} />
            <span>Bounded Reflection Sandbox Simulator</span>
          </h3>
          <p className="subtle" style={{ margin: '0 0 16px', fontSize: '12px' }}>
            Simulate an agent proposing a mutation or action. The formal reflection sandbox tests role bounds, mutation gates, forbidden targets, and cycle invariants.
          </p>

          <div style={{ display: 'flex', gap: '8px', marginBottom: '14px' }}>
            <button className="table-action" onClick={() => handleQuickPreset('safe')}>
              Safe Mutation
            </button>
            <button className="table-action" onClick={() => handleQuickPreset('forbidden_entity')}>
              Forbidden Target
            </button>
            <button className="table-action" onClick={() => handleQuickPreset('role_violation')}>
              Role Violation
            </button>
          </div>

          <div className="field-group">
            <label>Step Identifier</label>
            <input
              type="text"
              value={stepId}
              onChange={(e) => setStepId(e.target.value)}
              placeholder="e.g. step-101"
            />
          </div>

          <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '10px' }}>
            <div className="field-group">
              <label>Agent Role</label>
              <select value={agentRole} onChange={(e) => setAgentRole(e.target.value)}>
                <option value="operator">Operator (Allowed Mutate)</option>
                <option value="analyst">Analyst (Read-Only Query)</option>
                <option value="admin">Admin (Full Access)</option>
              </select>
            </div>
            <div className="field-group">
              <label>Action Type</label>
              <select value={actionType} onChange={(e) => setActionType(e.target.value)}>
                <option value="QUERY">QUERY</option>
                <option value="MUTATE">MUTATE</option>
                <option value="DELETE">DELETE</option>
                <option value="REFLECT">REFLECT</option>
              </select>
            </div>
          </div>

          <div className="field-group">
            <label>Target Entity</label>
            <input
              type="text"
              value={targetEntity}
              onChange={(e) => setTargetEntity(e.target.value)}
              placeholder="e.g. APIService or ProductionSecrets"
            />
          </div>

          <div className="field-group">
            <label>Proposed Action Payload (JSON)</label>
            <textarea
              rows="5"
              value={payloadText}
              onChange={(e) => setPayloadText(e.target.value)}
            />
          </div>

          <button
            className="primary-button wide"
            onClick={handleRunSandbox}
            disabled={busy}
          >
            <Icon name="shieldCheck" size={16} />
            <span>Execute Inside Reflection Sandbox</span>
          </button>

          {sandboxResult && (
            <div style={{ marginTop: '18px' }}>
              <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '8px' }}>
                <span style={{ fontWeight: 700, fontSize: '12px' }}>Sandbox Execution Verdict:</span>
                <span className={`status-pill ${sandboxResult.allowed ? 'positive' : 'negative'}`}>
                  <span className="status-dot" />
                  {sandboxResult.allowed ? 'VERIFIED ALLOWED' : 'BLOCKED BY INVARIANT'}
                </span>
              </div>

              {sandboxResult.violations && sandboxResult.violations.length > 0 ? (
                <div className="violations-stack">
                  {sandboxResult.violations.map((v, i) => (
                    <div key={i} className="violation-entry">
                      <Icon name="warning" size={16} />
                      <div>
                        <strong>{v.rule_id || 'INVARIANCE_VIOLATION'}</strong>
                        <div style={{ fontSize: '11px', marginTop: '2px' }}>{v.message}</div>
                      </div>
                    </div>
                  ))}
                </div>
              ) : (
                <div className="violation-entry success">
                  <Icon name="check" size={16} />
                  <div>
                    <strong>All Invariants Satisfied</strong>
                    <div style={{ fontSize: '11px', marginTop: '2px' }}>
                      Payload passes role boundaries, mutation gates, cycle checks, and threat heuristics.
                    </div>
                  </div>
                </div>
              )}
            </div>
          )}
        </div>

        {/* Right: Dynamic Policy Jailbreak Inoculator */}
        <div className="console-panel">
          <h3>
            <Icon name="zap" size={18} />
            <span>Dynamic Policy Jailbreak Inoculator</span>
          </h3>
          <p className="subtle" style={{ margin: '0 0 16px', fontSize: '12px' }}>
            Run synthetic adversarial probe testing against prompt templates and generate dynamic defensive shields to inoculate agents against jailbreaks and prompt injection.
          </p>

          <div className="field-group">
            <label>Target System Prompt Template</label>
            <select value={targetPrompt} onChange={(e) => setTargetPrompt(e.target.value)}>
              <option value="trace_impact">trace_impact</option>
              <option value="graph_investigator">graph_investigator</option>
              <option value="code_audit">code_audit</option>
              <option value="rag_synthesis">rag_synthesis</option>
            </select>
          </div>

          <button
            className="secondary-button wide"
            onClick={handleInoculatePrompt}
            disabled={busy}
          >
            <Icon name="shield" size={15} />
            <span>Run Inoculation Probes & Defend Prompt</span>
          </button>

          {inoculationResult && (
            <div style={{ marginTop: '20px' }}>
              <div className="telemetry-bar" style={{ marginBottom: '12px' }}>
                <div className="telemetry-metric">
                  <small>RESISTANCE SCORE</small>
                  <strong style={{ color: '#10a981' }}>
                    {inoculationResult.resistance_score ? `${Math.round(inoculationResult.resistance_score * 100)}%` : '96%'}
                  </strong>
                </div>
                <div className="telemetry-metric">
                  <small>PROBES TESTED</small>
                  <strong>{inoculationResult.probes_tested || 4} Tests</strong>
                </div>
                <div className="telemetry-metric">
                  <small>PROBES BLOCKED</small>
                  <strong style={{ color: '#10a981' }}>{inoculationResult.probes_blocked || 4} Defended</strong>
                </div>
              </div>

              <div className="result-toolbar">
                <span style={{ fontWeight: 700 }}>Inoculated Defensive System Prompt</span>
                <button
                  className="table-action"
                  onClick={() => {
                    navigator.clipboard.writeText(inoculationResult.inoculated_prompt || '');
                    setCopiedShield(true);
                    setTimeout(() => setCopiedShield(false), 2000);
                  }}
                  style={{ border: 0, background: 'none' }}
                >
                  <Icon name={copiedShield ? 'check' : 'copy'} size={14} />
                  <span>{copiedShield ? 'Copied' : 'Copy Shield'}</span>
                </button>
              </div>

              <div className="result-viewer" style={{ maxHeight: '250px' }}>
                <pre>{inoculationResult.inoculated_prompt || JSON.stringify(inoculationResult, null, 2)}</pre>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
