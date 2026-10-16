const assert = require('node:assert/strict');
const vscode = require('vscode');

async function run({inputs, document}) {
  inputs.push('invalid-token', 'target');
  await vscode.commands.executeCommand('eoip.setToken');
  const rejected = await vscode.commands.executeCommand('eoip.search');
  assert.equal(rejected.ok, false);
  assert.equal(rejected.code, 'EOIP_HTTP_401');
  const nlq = await vscode.commands.executeCommand('eoip.nlq', 'What is the impact of EOIP-1?');
  assert.equal(nlq.code, 'EOIP_HTTP_401');
  const mcp = await vscode.commands.executeCommand('eoip.mcp', {tool: 'search', arguments: {q: 'EOIP-1'}});
  assert.equal(mcp.ok, false);
  assert.match(mcp.message, /HTTP 401/);
  inputs.push('test-token');
  await vscode.commands.executeCommand('eoip.setToken');
  const unsafe = await vscode.commands.executeCommand('eoip.openSource', {
    properties: {path: '../outside.py'},
  });
  assert.equal(unsafe.code, 'EOIP_UNSAFE_SOURCE_PATH');
  await vscode.window.showTextDocument(document);
  assert.equal(document.getText(), 'def target():\n    return 1\n');
  assert.equal(document.isDirty, false);
}

module.exports = {run};
