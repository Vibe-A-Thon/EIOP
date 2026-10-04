const assert = require('node:assert/strict');
const fs = require('node:fs/promises');
const vscode = require('vscode');

async function run() {
  const steps = [];
  const output = vscode.window.createOutputChannel('EOIP Live Demo');
  const originalInput = vscode.window.showInputBox;
  const token = process.env.EOIP_DEMO_TOKEN;
  const anchor = process.env.EOIP_DEMO_ANCHOR;
  delete process.env.EOIP_DEMO_TOKEN;
  try {
    assert.ok(token, 'Demo access token is required.');
    assert.ok(anchor, 'A ready live scenario anchor is required.');
    const extension = vscode.extensions.getExtension('eoip-local.eoip-context');
    assert.ok(extension, 'EOIP extension must be loaded.');
    await extension.activate();
    output.show();
    output.appendLine('EOIP 0.1.0 source extension / isolated profile / LIVE API and MCP');
    vscode.window.showInputBox = async () => token;
    await vscode.commands.executeCommand('eoip.setToken');
    vscode.window.showInputBox = originalInput;
    async function step(name, action) {
      output.appendLine(`Running: ${name}`);
      const value = await action();
      assert.notEqual(value?.ok, false, `${name} command failed.`);
      steps.push({name, status: 'PASS'});
      output.appendLine(`PASS: ${name}`);
      await new Promise(resolve => setTimeout(resolve, 2500));
      return value;
    }
    const nlq = await step(`Natural-language impact query: ${anchor}`, async () => {
      const result = await vscode.commands.executeCommand('eoip.nlq', `What is the impact of ${anchor}?`);
      assert.ok(result?.interpretation?.plan, 'NLQ must resolve a query plan.');
      assert.ok(result?.result?.nodes?.length, 'NLQ must return live graph nodes.');
      assert.ok(result.result.nodes.some(node => node.id === anchor), 'NLQ must resolve the requested live anchor.');
      return result;
    });
    const search = await step('MCP initialize / tools.list / search', async () => {
      const result = await vscode.commands.executeCommand('eoip.mcp', {tool: 'search', arguments: {q: anchor.split(':').at(-1), limit: 5}});
      assert.equal(result?.tool, 'search');
      const graph = result.result.structuredContent || JSON.parse(result.result.content.find(item => item.type === 'text').text);
      assert.ok(graph.nodes?.length, 'MCP search must return live graph nodes.');
      assert.ok(graph.nodes.some(node => node.id === anchor), 'MCP search must include the scenario anchor.');
      return {...result, graph};
    });
    await step('MCP provenance / lineage', async () => {
      const result = await vscode.commands.executeCommand('eoip.mcp', {
        tool: 'lineage', arguments: {canonical_id: anchor, max_depth: 4, result_limit: 100},
      });
      assert.equal(result?.tool, 'lineage');
      const graph = result.result.structuredContent || JSON.parse(result.result.content.find(item => item.type === 'text').text);
      assert.ok(graph.nodes?.length, 'Lineage must return the live entity.');
      return result;
    });
    await fs.writeFile(process.env.EOIP_DEMO_RECEIPT, JSON.stringify({
      status: 'PASS', mode: 'live-isolated-development-host', extensionVersion: extension.packageJSON.version,
      steps, anchor, nlqEngine: nlq.engine, mcpProtocol: search.protocolVersion,
      limitations: ['Source extension, not installed VSIX certification', 'Does not certify all product scenarios or independent QA'],
    }, null, 2));
  } catch (error) {
    output.appendLine(`FAIL: ${error.message}`);
    await fs.writeFile(process.env.EOIP_DEMO_RECEIPT, JSON.stringify({status: 'FAIL', steps, error: error.message}, null, 2));
    throw error;
  } finally {
    vscode.window.showInputBox = originalInput;
    output.dispose();
  }
}

module.exports = {run};
