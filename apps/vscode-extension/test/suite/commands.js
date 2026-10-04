const assert = require('node:assert/strict');
const vscode = require('vscode');

async function run({symbol, jira, inputs, requests, document}) {
  const registered = await vscode.commands.getCommands();
  for (const contribution of require('../../package.json').contributes.commands) {
    assert.ok(registered.includes(contribution.command), `${contribution.command} must be registered in the host`);
  }
  inputs.push('target');
  await vscode.commands.executeCommand('eoip.search');
  const entity = JSON.parse(vscode.window.activeTextEditor.document.getText());
  assert.equal(entity.id, symbol.id);
  await vscode.commands.executeCommand('eoip.impact');
  assert.ok(JSON.parse(vscode.window.activeTextEditor.document.getText()).nodes.some(node => node.id === jira.id));
  inputs.push(symbol.id);
  await vscode.commands.executeCommand('eoip.lineage');
  assert.ok(JSON.parse(vscode.window.activeTextEditor.document.getText()).evidence.length > 0);
  inputs.push(symbol.id, 'Explain target');
  await vscode.commands.executeCommand('eoip.retrieval');
  const retrieval = JSON.parse(vscode.window.activeTextEditor.document.getText());
  assert.equal(retrieval.canonical_id, symbol.id);
  assert.ok(retrieval.evidence.length > 0);
  const request = requests.find(item => item.url === '/api/v1/rag');
  assert.deepEqual(request.body, {canonical_id: symbol.id, question: 'Explain target', synthesize: false});
  assert.ok(requests.every(item => item.method === 'GET' ||
    ['/api/v1/impact', '/api/v1/lineage', '/api/v1/path', '/api/v1/rag', '/api/v1/query/nl', '/mcp'].includes(item.url)));
  await vscode.window.showTextDocument(document);
  assert.equal(document.isDirty, false);
}

module.exports = {run};
