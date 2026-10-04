const http = require('node:http');
const https = require('node:https');

const READ_ONLY_TOOLS = new Set(['search', 'entity', 'path', 'impact', 'lineage', 'neighbors', 'document', 'code_symbol', 'jira_issue', 'evidence', 'query']);

function requestJson(url, token, body, notification = false, extraHeaders = {}) {
  const endpoint = new URL(url);
  if (!['http:', 'https:'].includes(endpoint.protocol)) throw new Error('MCP URL must use HTTP or HTTPS.');
  const payload = JSON.stringify(body);
  return new Promise((resolve, reject) => {
    const request = (endpoint.protocol === 'https:' ? https : http).request(endpoint, {
      method: 'POST',
      headers: {Authorization: `Bearer ${token}`, Accept: 'application/json, text/event-stream',
        'Content-Type': 'application/json', 'Content-Length': Buffer.byteLength(payload), ...extraHeaders},
      timeout: 60000,
    }, response => {
      let data = '';
      response.on('error', reject);
      response.on('data', chunk => {
        data += chunk;
        if (Buffer.byteLength(data) > 4000000) request.destroy(new Error('MCP response exceeded 4 MB.'));
      });
      response.on('end', () => {
        if (response.statusCode < 200 || response.statusCode >= 300) {
          reject(new Error(`MCP request failed with HTTP ${response.statusCode}.`));
          return;
        }
        if (notification) { resolve(undefined); return; }
        try {
          const message = JSON.parse(data);
          if (message.jsonrpc !== '2.0' || message.id !== body.id) throw new Error('MCP returned an invalid JSON-RPC response.');
          if (message.error) throw new Error(`MCP protocol error ${message.error.code}.`);
          if (!Object.hasOwn(message, 'result')) throw new Error('MCP response has no result.');
          resolve(message.result);
        } catch (error) { reject(error); }
      });
    });
    request.on('error', reject);
    request.on('timeout', () => request.destroy(new Error('MCP request timed out.')));
    request.end(payload);
  });
}

async function callTool(url, token, name, args) {
  if (!READ_ONLY_TOOLS.has(name)) throw new Error('Only approved read-only MCP tools can be called.');
  const initialized = await requestJson(url, token, {
    jsonrpc: '2.0', id: 1, method: 'initialize',
    params: {protocolVersion: '2024-11-05', capabilities: {}, clientInfo: {name: 'eoip-context', version: '0.1.0'}},
  });
  if (!initialized.protocolVersion || !initialized.capabilities?.tools) throw new Error('MCP server does not advertise tools.');
  const headers = {'MCP-Protocol-Version': initialized.protocolVersion};
  await requestJson(url, token, {jsonrpc: '2.0', method: 'notifications/initialized'}, true, headers);
  const catalog = await requestJson(url, token, {jsonrpc: '2.0', id: 2, method: 'tools/list'}, false, headers);
  if (!Array.isArray(catalog.tools) || !catalog.tools.some(tool => tool.name === name)) throw new Error(`MCP tool "${name}" is unavailable.`);
  const result = await requestJson(url, token, {
    jsonrpc: '2.0', id: 3, method: 'tools/call', params: {name, arguments: args},
  }, false, headers);
  if (result.isError) throw new Error(`MCP tool "${name}" reported an error.`);
  if (!Array.isArray(result.content)) throw new Error('MCP tool returned invalid content.');
  return {server: initialized.serverInfo, protocolVersion: initialized.protocolVersion,
    tools: catalog.tools.map(tool => tool.name), tool: name, result};
}

module.exports = {callTool};
