const assert = require('node:assert/strict');
const fs = require('node:fs/promises');
const http = require('node:http');
const os = require('node:os');
const path = require('node:path');
const vscode = require('vscode');

async function run() {
  const journeys = [];
  const requests = [];
  const root = await fs.mkdtemp(path.join(os.tmpdir(), 'eoip-vscode-test-'));
  const configuration = vscode.workspace.getConfiguration('eoip');
  const oldRoot = configuration.get('repositoryRoot');
  const oldApiUrl = configuration.get('apiUrl');
  const originalShowInputBox = vscode.window.showInputBox;
  const originalShowQuickPick = vscode.window.showQuickPick;
  let server;
  try {
    const sourcePath = path.join(root, 'src', 'sample.py');
    await fs.mkdir(path.dirname(sourcePath), {recursive: true});
    await fs.writeFile(sourcePath, 'def target():\n    return 1\n', 'utf8');
    const canonicalSourcePath = await fs.realpath(sourcePath);
    const symbol = {
      id: 'urn:eoip:code:demo:src/sample.py#target',
      label: 'CodeSymbol',
      properties: {
        name: 'target',
        qualified_name: 'sample.target',
        path: 'src/sample.py',
        start_line: 1,
        end_line: 2,
        start_column: 0,
        end_column: 12,
      },
    };
    const jira = {
      id: 'urn:eoip:work:item:jira:EOIP-1',
      label: 'WorkItem',
      properties: {issue_key: 'EOIP-1', summary: 'Trace the demo function'},
    };
    const commit = {
      id: 'urn:eoip:code:commit:demo:abc123',
      label: 'Commit',
      properties: {commit_sha: 'abc123', summary: 'Add target function'},
    };
    const dependency = {
      id: 'urn:eoip:code:dependency:python:requests',
      label: 'Dependency',
      properties: {name: 'requests'},
    };
    const documentSection = {
      id: 'urn:eoip:document:demo:target',
      label: 'DocumentSection',
      properties: {name: 'Target design', path: 'docs/design.md'},
    };
    const evidenceNode = {
      id: 'urn:eoip:evidence:demo:target',
      label: 'Evidence',
      properties: {evidence_key: 'target-source', source_ref: 'src/sample.py'},
    };
    const impact = {
      query_id: 'test-impact',
      nodes: [symbol, jira, commit, dependency, documentSection],
      edges: [
        {id: 'e-jira', type: 'IMPLEMENTS', from_id: jira.id, to_id: symbol.id},
        {id: 'e-commit', type: 'MODIFIES', from_id: commit.id, to_id: symbol.id},
        {id: 'e-dependency', type: 'DEPENDS_ON', from_id: symbol.id, to_id: dependency.id},
        {id: 'e-document', type: 'DOCUMENTS', from_id: documentSection.id, to_id: symbol.id},
      ],
      paths: [
        {path_id: 'p-jira', node_ids: [symbol.id, jira.id], edge_ids: ['e-jira']},
        {path_id: 'p-commit', node_ids: [symbol.id, commit.id], edge_ids: ['e-commit']},
        {path_id: 'p-dependency', node_ids: [symbol.id, dependency.id], edge_ids: ['e-dependency']},
        {path_id: 'p-document', node_ids: [symbol.id, documentSection.id], edge_ids: ['e-document']},
      ],
      evidence: [{edge_id: 'e-commit', evidence_key: 'commit-proof', source_ref: 'abc123', source_system: 'git'}],
      partial: false,
      warnings: [],
    };
    const lineage = {
      query_id: 'test-lineage',
      nodes: [symbol, evidenceNode],
      edges: [{id: 'e-evidence', type: 'EVIDENCED_BY', from_id: symbol.id, to_id: evidenceNode.id}],
      paths: [{path_id: 'p-evidence', node_ids: [symbol.id, evidenceNode.id], edge_ids: ['e-evidence']}],
      evidence: [{edge_id: 'e-evidence', evidence_key: 'target-source', source_ref: 'src/sample.py', source_system: 'git'}],
      partial: false,
      warnings: [],
    };
    const trace = {
      query_id: 'test-path',
      nodes: [jira, symbol],
      edges: [{id: 'e-trace', type: 'IMPLEMENTS', from_id: jira.id, to_id: symbol.id}],
      paths: [{path_id: 'p-trace', node_ids: [jira.id, symbol.id], edge_ids: ['e-trace']}],
      evidence: [{edge_id: 'e-trace', evidence_key: 'trace-proof', source_ref: 'src/sample.py'}],
      partial: false,
      warnings: [],
    };
    server = http.createServer(async (request, response) => {
      let body = '';
      for await (const chunk of request) body += chunk;
      requests.push({url: request.url, method: request.method, body: body ? JSON.parse(body) : undefined});
      response.setHeader('Content-Type', 'application/json');
      if (request.headers.authorization !== 'Bearer test-token') {
        response.writeHead(401).end(JSON.stringify({detail: 'Unauthorized'}));
        return;
      }
      if (request.url.startsWith('/api/v1/search')) {
        const query = new URL(request.url, 'http://localhost').searchParams.get('q');
        response.end(JSON.stringify({
          query_id: 'test-search',
          nodes: query === 'EOIP-1' ? [jira] : [symbol],
          edges: [],
          paths: [],
          evidence: [],
          partial: false,
          warnings: [],
        }));
      } else if (request.url.startsWith('/api/v1/entities/')) {
        response.end(JSON.stringify(symbol));
      } else if (request.url === '/health/ready') {
        response.end(JSON.stringify({status: 'ready'}));
      } else if (request.url === '/api/v1/rag') {
        response.end(JSON.stringify({canonical_id: JSON.parse(body).canonical_id, evidence: lineage.evidence}));
      } else if (request.url === '/api/v1/impact') {
        response.end(JSON.stringify(impact));
      } else if (request.url === '/api/v1/lineage') {
        response.end(JSON.stringify(lineage));
      } else if (request.url === '/api/v1/path') {
        response.end(JSON.stringify(trace));
      } else {
        response.writeHead(404).end(JSON.stringify({detail: 'Not found'}));
      }
    });
    await new Promise(resolve => server.listen(0, '127.0.0.1', resolve));
    const apiUrl = `http://127.0.0.1:${server.address().port}`;
    await configuration.update('apiUrl', apiUrl, vscode.ConfigurationTarget.Global);
    await configuration.update(
      'repositoryRoot',
      root,
      vscode.ConfigurationTarget.Global,
    );
    const inputs = ['test-token', 'EOIP-1'];
    vscode.window.showInputBox = async () => inputs.shift();
    vscode.window.showQuickPick = async items => items[0];
    const document = await vscode.workspace.openTextDocument(vscode.Uri.file(sourcePath));
    const originalText = document.getText();
    await vscode.window.showTextDocument(document);

    const result = await vscode.commands.executeCommand('eoip.openSource', {
      id: symbol.id,
      label: symbol.label,
      properties: {
        path: 'src/sample.py',
        start_line: 2,
        end_line: 2,
        start_column: 4,
        end_column: 12,
      },
    });
    assert.equal(result.ok, true, 'source navigation should succeed');
    assert.equal(
      path.normalize(vscode.window.activeTextEditor.document.uri.fsPath).toLocaleLowerCase(),
      path.normalize(canonicalSourcePath).toLocaleLowerCase(),
    );
    assert.equal(vscode.window.activeTextEditor.selection.start.line, 1);
    assert.equal(vscode.window.activeTextEditor.selection.start.character, 4);
    assert.equal(vscode.window.activeTextEditor.selection.end.line, 1);
    assert.equal(vscode.window.activeTextEditor.selection.end.character, 12);

    await vscode.commands.executeCommand('eoip.setToken');
    vscode.window.activeTextEditor.selection = new vscode.Selection(
      new vscode.Position(0, 5),
      new vscode.Position(0, 5),
    );
    const context = await vscode.commands.executeCommand('eoip.context');
    assert.equal(context.ok, true, `active symbol context should be retrieved (${context.code}: ${context.message})`);
    assert.equal(context.node.id, symbol.id);
    assert.equal(context.relatedCount, 5, 'Jira, commit, dependency, document, and evidence nodes should be presented');
    assert.equal(context.evidenceCount, 2, 'graph evidence should be presented');

    await vscode.commands.executeCommand('eoip.path');
    const traceDocument = vscode.window.activeTextEditor.document;
    const traceResult = JSON.parse(traceDocument.getText());
    assert.equal(traceResult.source.id, jira.id);
    assert.equal(traceResult.target.id, symbol.id);
    assert.equal(traceResult.path.paths[0].node_ids.length, 2);
    assert.ok(traceResult.impact.nodes.some(node => node.id === dependency.id));

    const fixture = {symbol, jira, inputs, requests, document};
    for (const name of ['commands', 'symbols', 'refusals']) {
      await require(`./${name}`).run(fixture);
      journeys.push(name);
    }
    await vscode.window.showTextDocument(document);
    await new Promise((resolve, reject) => server.close(error => error ? reject(error) : resolve()));
    server = undefined;
    const offline = await vscode.commands.executeCommand('eoip.context');
    assert.equal(offline.ok, false, 'context should report when the API is offline');
    assert.equal(offline.code, 'EOIP_OFFLINE');
    assert.equal(document.getText(), originalText, 'the extension must not modify source files');

    const unsafe = await vscode.commands.executeCommand('eoip.openSource', {
      properties: {path: '../outside.py', start_line: 1, end_line: 1},
    });
    assert.equal(unsafe.ok, false, 'source navigation must reject traversal paths');
    assert.equal(unsafe.code, 'EOIP_UNSAFE_SOURCE_PATH');
    journeys.push('context-path-navigation-offline');
    if (process.env.EOIP_EXTENSION_RECEIPT) {
      await fs.writeFile(process.env.EOIP_EXTENSION_RECEIPT, JSON.stringify({
        status: 'PASS', passed: journeys.length, failed: 0, journeys,
        vscode: vscode.version,
        scope: 'Real VS Code host; local HTTP contract fixture; prompt input/selection automated.',
        exclusions: ['Live HugeGraph/API integration', 'Manual prompt interaction', 'Visual TreeView layout'],
      }, null, 2));
    }
    console.log('VS Code extension-host acceptance passed: graph context, Jira path and impact, exact range, and source path safety.');
  } finally {
    vscode.window.showInputBox = originalShowInputBox;
    vscode.window.showQuickPick = originalShowQuickPick;
    if (server) {
      await new Promise((resolve, reject) => server.close(error => error ? reject(error) : resolve()));
    }
    await vscode.commands.executeCommand('workbench.action.closeAllEditors');
    await configuration.update('apiUrl', oldApiUrl, vscode.ConfigurationTarget.Global);
    await vscode.workspace.getConfiguration('eoip').update(
      'repositoryRoot',
      oldRoot,
      vscode.ConfigurationTarget.Global,
    );
    let lastError;
    for (let attempt = 0; attempt < 10; attempt += 1) {
      try {
        await fs.rm(root, {recursive: true, force: true});
        lastError = undefined;
        break;
      } catch (error) {
        if (!['EBUSY', 'EPERM'].includes(error.code)) throw error;
        lastError = error;
        await new Promise(resolve => setTimeout(resolve, 100));
      }
    }
    if (lastError) throw lastError;
  }
}

module.exports = {run};
