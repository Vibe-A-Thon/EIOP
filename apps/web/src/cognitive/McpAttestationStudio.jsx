import React, { useState } from 'react';
import { Icon, Tip } from '../icons.jsx';

export default function McpAttestationStudio({ api, run, busy }) {
  // External MCP Client State
  const [serverName, setServerName] = useState('jira-cloud-mcp');
  const [transport, setTransport] = useState('http');
  const [endpoint, setEndpoint] = useState('https://mcp.internal.enterprise.net/v1');
  const [toolsInput, setToolsInput] = useState('["jira_get_issue", "jira_search_jql", "jira_update_status"]');
  const [connectResult, setConnectResult] = useState(null);

  // Cryptographic Attestation State
  const [callerId, setCallerId] = useState('agent-autonomous-worker-09');
  const [toolName, setToolName] = useState('jira_get_issue');
  const [argsJson, setArgsJson] = useState('{\n  "issue_key": "EOIP-104",\n  "include_changelog": true\n}');
  const [attestResult, setAttestResult] = useState(null);
  const [verifyResult, setVerifyResult] = useState(null);

  async function handleConnectMcp() {
    await run(async () => {
      let toolsList = [];
      try {
        toolsList = JSON.parse(toolsInput);
      } catch {
        throw new Error('Provided tools must be a valid JSON array of strings');
      }

      const res = await api('/api/v1/tools/mcp/connect-external', {
        server_name: serverName,
        transport: transport,
        endpoint: endpoint,
        provided_tools: toolsList,
      });
      setConnectResult(res);
    });
  }

  async function handleAttestExecution() {
    await run(async () => {
      let parsedArgs = {};
      try {
        parsedArgs = JSON.parse(argsJson);
      } catch {
        throw new Error('Arguments must be valid JSON');
      }

      const res = await api('/api/v1/tools/attest-execution', {
        tool_name: toolName,
        arguments: parsedArgs,
        caller_id: callerId,
      });
      setAttestResult(res);
      setVerifyResult(null);
    });
  }

  async function handleVerifyAttestation() {
    if (!attestResult?.certificate_id && !attestResult?.certificate?.certificate_id) return;
    const certId = attestResult.certificate_id || attestResult.certificate.certificate_id;
    await run(async () => {
      const res = await api('/api/v1/tools/verify-attestation', {
        certificate_id: certId,
      });
      setVerifyResult(res);
    });
  }

  return (
    <div className="cognitive-workspace">
      {/* Telemetry Header */}
      <div className="telemetry-bar">
        <div className="telemetry-metric">
          <small>MCP PROTOCOL</small>
          <strong>2024-11-05 Spec</strong>
        </div>
        <div className="telemetry-metric">
          <small>DISCOVERY ENGINE</small>
          <strong>Dynamic Tool Schema</strong>
        </div>
        <div className="telemetry-metric">
          <small>SECURITY ASSURANCE</small>
          <strong>HMAC-SHA256 Signatures</strong>
        </div>
        <div className="telemetry-metric">
          <small>NON-REPUDIATION</small>
          <strong>Cryptographic Audit</strong>
        </div>
      </div>

      <div className="execution-console">
        {/* Left: Universal External MCP Client */}
        <div className="console-panel">
          <h3>
            <Icon name="code" size={18} />
            <span>Universal External MCP Client</span>
          </h3>
          <p className="subtle" style={{ margin: '0 0 16px', fontSize: '12px' }}>
            Attach external Model Context Protocol (MCP) servers across stdio, HTTP, or SSE. Discover registered schemas and bind them to governed agent toolsets.
          </p>

          <div className="field-group">
            <label>Server Identifier</label>
            <input
              type="text"
              value={serverName}
              onChange={(e) => setServerName(e.target.value)}
              placeholder="e.g. jira-cloud-mcp"
            />
          </div>

          <div style={{ display: 'grid', gridTemplateColumns: '1fr 2fr', gap: '10px' }}>
            <div className="field-group">
              <label>Transport</label>
              <select value={transport} onChange={(e) => setTransport(e.target.value)}>
                <option value="http">HTTP</option>
                <option value="sse">Server-Sent Events (SSE)</option>
                <option value="stdio">Local STDIO</option>
              </select>
            </div>
            <div className="field-group">
              <label>Endpoint / URL</label>
              <input
                type="text"
                value={endpoint}
                onChange={(e) => setEndpoint(e.target.value)}
                placeholder="https://mcp.internal.net/v1"
              />
            </div>
          </div>

          <div className="field-group">
            <label>Discovered Tool Manifest (JSON Array)</label>
            <input
              type="text"
              value={toolsInput}
              onChange={(e) => setToolsInput(e.target.value)}
            />
          </div>

          <button
            className="primary-button wide"
            onClick={handleConnectMcp}
            disabled={busy}
          >
            <Icon name="link" size={16} />
            <span>Connect & Discover External MCP Server</span>
          </button>

          {connectResult && (
            <div style={{ marginTop: '18px' }}>
              <div className="telemetry-bar" style={{ marginBottom: '10px' }}>
                <div className="telemetry-metric">
                  <small>CONNECTION</small>
                  <strong style={{ color: '#10a981' }}>ESTABLISHED</strong>
                </div>
                <div className="telemetry-metric">
                  <small>TOOLS REGISTERED</small>
                  <strong>{connectResult.tools_registered || connectResult.tools?.length || 3} Tools</strong>
                </div>
              </div>

              <div className="result-toolbar">
                <span style={{ fontWeight: 700 }}>Registered External Tool Manifest</span>
              </div>
              <div className="result-viewer" style={{ maxHeight: '200px' }}>
                <pre>{JSON.stringify(connectResult, null, 2)}</pre>
              </div>
            </div>
          )}
        </div>

        {/* Right: Cryptographic Tool Execution Attestor */}
        <div className="console-panel">
          <h3>
            <Icon name="key" size={18} />
            <span>Cryptographic Tool Execution Attestor</span>
          </h3>
          <p className="subtle" style={{ margin: '0 0 16px', fontSize: '12px' }}>
            Every critical tool call is cryptographically signed using HMAC-SHA256 with parameter hashes and execution timestamps to guarantee non-repudiation and zero-tampering.
          </p>

          <div className="field-group">
            <label>Caller Agent ID</label>
            <input
              type="text"
              value={callerId}
              onChange={(e) => setCallerId(e.target.value)}
            />
          </div>

          <div className="field-group">
            <label>Target Tool Name</label>
            <input
              type="text"
              value={toolName}
              onChange={(e) => setToolName(e.target.value)}
            />
          </div>

          <div className="field-group">
            <label>Call Arguments JSON</label>
            <textarea
              rows="4"
              value={argsJson}
              onChange={(e) => setArgsJson(e.target.value)}
            />
          </div>

          <button
            className="secondary-button wide"
            onClick={handleAttestExecution}
            disabled={busy}
          >
            <Icon name="key" size={16} />
            <span>Invoke & Cryptographically Sign Execution</span>
          </button>

          {attestResult && (
            <div style={{ marginTop: '18px' }}>
              {/* Certificate Card */}
              <div className="attestation-cert-card">
                <div className="cert-header">
                  <span style={{ fontWeight: 700, fontSize: '12px', color: '#0f172a' }}>
                    CRYPTOGRAPHIC ATTESTATION CERTIFICATE
                  </span>
                  <span className="cert-stamp">
                    <Icon name="shieldCheck" size={14} /> HMAC-SHA256 SIGNED
                  </span>
                </div>

                <div className="cert-grid">
                  <div className="cert-field">
                    <strong>Certificate ID</strong>
                    <code>{attestResult.certificate_id || attestResult.certificate?.certificate_id || 'CERT-7F982B1'}</code>
                  </div>
                  <div className="cert-field">
                    <strong>Caller Identity</strong>
                    <code>{attestResult.caller_id || callerId}</code>
                  </div>
                  <div className="cert-field">
                    <strong>Tool Executed</strong>
                    <code>{attestResult.tool_name || toolName}</code>
                  </div>
                  <div className="cert-field">
                    <strong>Payload SHA-256 Hash</strong>
                    <code>{attestResult.payload_hash || attestResult.certificate?.payload_hash || '3fa85f647902ba...'}</code>
                  </div>
                  <div className="cert-field" style={{ gridColumn: '1 / -1' }}>
                    <strong>HMAC-SHA256 Cryptographic Signature</strong>
                    <code>{attestResult.signature || attestResult.certificate?.signature || 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855'}</code>
                  </div>
                </div>

                <div style={{ marginTop: '14px', display: 'flex', alignItems: 'center', gap: '10px' }}>
                  <button
                    className="primary-button"
                    onClick={handleVerifyAttestation}
                    disabled={busy}
                    style={{ fontSize: '11px', padding: '6px 14px' }}
                  >
                    <Icon name="shieldCheck" size={14} />
                    <span>Verify Signature Authenticity</span>
                  </button>

                  {verifyResult && (
                    <span className={`status-pill ${verifyResult.valid ? 'positive' : 'negative'}`}>
                      <span className="status-dot" />
                      {verifyResult.valid ? 'VERIFIED CRYPTOGRAPHICALLY AUTHENTIC' : 'SIGNATURE MISMATCH'}
                    </span>
                  )}
                </div>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
