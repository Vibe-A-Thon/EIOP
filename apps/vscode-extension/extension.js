const vscode = require('vscode');
const http = require('node:http');
const https = require('node:https');
const path = require('node:path');

function activate(context) {
  let selected;
  async function call(endpoint, body) {
    const token = await context.secrets.get('eoip-token');
    if (!token) throw new Error('Run EOIP: Set Access Token first.');
    const base = vscode.workspace.getConfiguration('eoip').get('apiUrl');
    const url = new URL(endpoint, base);
    const payload = body === undefined ? undefined : JSON.stringify(body);
    return new Promise((resolve, reject) => {
      const req = (url.protocol === 'https:' ? https : http).request(url, {method: payload ? 'POST' : 'GET', headers: {Authorization: `Bearer ${token}`, ...(payload ? {'Content-Type': 'application/json', 'Content-Length': Buffer.byteLength(payload)} : {})}, timeout: 60000}, res => {
        let data = '';
        res.on('data', chunk => {data += chunk; if (data.length > 4000000) req.destroy(new Error('Result is too large'));});
        res.on('end', () => {try {const json = JSON.parse(data); res.statusCode >= 400 ? reject(new Error(json.detail || 'EOIP request failed')) : resolve(json);} catch (error) {reject(error);}});
      });
      req.on('error', reject); req.on('timeout', () => req.destroy(new Error('EOIP request timed out')));
      if (payload) req.write(payload); req.end();
    });
  }
  async function choose(query) {
    const result = await call(`/api/v1/search?q=${encodeURIComponent(query)}`);
    const pick = await vscode.window.showQuickPick(result.nodes.map(n => ({label: n.properties.name || n.properties.qualified_name || n.properties.summary || n.label, description: n.label, detail: n.id, node: n})), {placeHolder: 'Choose an EOIP graph entity'});
    if (pick) selected = pick.node;
    return pick?.node;
  }
  async function show(value) {const doc = await vscode.workspace.openTextDocument({content: JSON.stringify(value, null, 2), language: 'json'}); await vscode.window.showTextDocument(doc, {preview: true});}
  function command(name, action) {context.subscriptions.push(vscode.commands.registerCommand(name, async () => {try {await action();} catch (e) {vscode.window.showErrorMessage(e.message);}}));}
  command('eoip.setToken', async () => {const token = await vscode.window.showInputBox({prompt: 'EOIP_API_TOKEN from deploy/.env', password: true, ignoreFocusOut: true}); if (token) await context.secrets.store('eoip-token', token);});
  command('eoip.search', async () => {const query = await vscode.window.showInputBox({prompt: 'Issue key, symbol, or source path'}); if (query) {const node = await choose(query); if (node) await show(await call(`/api/v1/entities/${encodeURIComponent(node.id)}`));}});
  command('eoip.context', async () => {const editor = vscode.window.activeTextEditor; if (!editor) throw new Error('Open a source file first.'); const range = editor.document.getWordRangeAtPosition(editor.selection.active); const symbol = range ? editor.document.getText(range) : ''; const node = await choose(symbol || path.basename(editor.document.fileName)); if (node) await show(await call(`/api/v1/entities/${encodeURIComponent(node.id)}`));});
  command('eoip.impact', async () => {if (!selected) throw new Error('Select an entity using EOIP: Search Knowledge Graph.'); await show(await call('/api/v1/impact', {canonical_id: selected.id, max_depth: 4}));});
  command('eoip.path', async () => {if (!selected) throw new Error('Select a code entity using EOIP: Search Knowledge Graph.'); const source = await vscode.window.showInputBox({prompt: 'Source canonical ID', value: 'urn:eoip:work:item:jira:EOIP-1'}); if (source) await show(await call('/api/v1/path', {source_id: source, target_id: selected.id}));});
  command('eoip.lineage', async () => {const id = await vscode.window.showInputBox({prompt: 'Canonical ID to trace provenance', value: selected?.id || 'urn:eoip:work:item:jira:EOIP-1'}); if (id) await show(await call('/api/v1/lineage', {canonical_id: id, max_depth: 4}));});
  command('eoip.retrieval', async () => {const id = await vscode.window.showInputBox({prompt: 'Canonical ID', value: selected?.id || 'urn:eoip:work:item:jira:EOIP-1'}); const question = await vscode.window.showInputBox({prompt: 'Question', value: 'Explain the implementation and its evidence'}); if (id && question) await show(await call('/api/v1/rag', {canonical_id: id, question, synthesize: false}));});
  command('eoip.openSource', async () => {if (!selected?.properties.path) throw new Error('Select a code symbol first.'); const root = vscode.workspace.getConfiguration('eoip').get('repositoryRoot'); if (!root) throw new Error('Set eoip.repositoryRoot to the local ingested repository root.'); const file = path.resolve(root, selected.properties.path); const relative = path.relative(path.resolve(root), file); if (relative.startsWith('..') || path.isAbsolute(relative)) throw new Error('Source path is outside the repository root.'); const editor = await vscode.window.showTextDocument(await vscode.workspace.openTextDocument(vscode.Uri.file(file))); const line = Math.max(0, (selected.properties.start_line || 1) - 1); const position = new vscode.Position(line, 0); editor.selection = new vscode.Selection(position, position); editor.revealRange(new vscode.Range(position, position));});
}
module.exports = {activate};
