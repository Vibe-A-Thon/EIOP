const assert = require('node:assert/strict');
const http = require('node:http');
const {test} = require('node:test');
const {callTool} = require('../mcp-client');

test('MCP authenticates the handshake, lists tools and calls the approved tool', async () => {
  const methods = [];
  const server = http.createServer(async (request, response) => {
    let text = '';
    for await (const chunk of request) text += chunk;
    const body = JSON.parse(text);
    methods.push(body.method);
    if (request.headers.authorization !== 'Bearer fixture-token') {
      response.writeHead(401).end('{}');
      return;
    }
    if (body.method === 'notifications/initialized') { response.writeHead(202).end(); return; }
    response.setHeader('Content-Type', 'application/json');
    const result = body.method === 'initialize'
      ? {protocolVersion: '2024-11-05', capabilities: {tools: {}}, serverInfo: {name: 'fixture'}}
      : body.method === 'tools/list' ? {tools: [{name: 'search'}]}
      : {content: [{type: 'text', text: '{"nodes":[{"id":"fixture"}]}'}]};
    response.end(JSON.stringify({jsonrpc: '2.0', id: body.id, result}));
  });
  await new Promise(resolve => server.listen(0, '127.0.0.1', resolve));
  const url = `http://127.0.0.1:${server.address().port}/mcp`;
  try {
    const result = await callTool(url, 'fixture-token', 'search', {q: 'PAY-202'});
    assert.equal(result.tool, 'search');
    assert.deepEqual(methods, ['initialize', 'notifications/initialized', 'tools/list', 'tools/call']);
    await assert.rejects(callTool(url, 'wrong', 'search', {}), /HTTP 401/);
    await assert.rejects(callTool(url, 'fixture-token', 'impact', {}), /unavailable/);
    const before = methods.length;
    await assert.rejects(callTool(url, 'fixture-token', 'run_agent', {}), /read-only/);
    assert.equal(methods.length, before, 'Rejected tools must never reach the network.');
  } finally {
    await new Promise(resolve => server.close(resolve));
  }
});

test('MCP rejects tool errors and malformed JSON-RPC envelopes', async () => {
  let invalid = false;
  const server = http.createServer(async (request, response) => {
    let text = '';
    for await (const chunk of request) text += chunk;
    const body = JSON.parse(text);
    if (body.method === 'notifications/initialized') { response.writeHead(202).end(); return; }
    const result = body.method === 'initialize'
      ? {protocolVersion: '2024-11-05', capabilities: {tools: {}}}
      : body.method === 'tools/list' ? {tools: [{name: 'search'}]}
      : {isError: true, content: []};
    response.end(JSON.stringify({jsonrpc: '2.0', id: invalid ? 999 : body.id, result}));
  });
  await new Promise(resolve => server.listen(0, '127.0.0.1', resolve));
  try {
    const url = `http://127.0.0.1:${server.address().port}/mcp`;
    await assert.rejects(callTool(url, 'fixture', 'search', {}), /reported an error/);
    invalid = true;
    await assert.rejects(callTool(url, 'fixture', 'search', {}), /invalid JSON-RPC/);
  } finally {
    await new Promise(resolve => server.close(resolve));
  }
});
