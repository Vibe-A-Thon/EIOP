const assert = require('node:assert/strict');
const fs = require('node:fs/promises');
const vscode = require('vscode');

const NLQ_JOURNEYS = [
  {intent: 'SEARCH', question: (issueKey) => `Search for ${issueKey}`, anchors: context => [context.issueId]},
  {intent: 'PATH', question: (_issueKey, _symbolName, context) =>
    `Show the path from ${context.issueId} to ${context.symbolId}`,
    anchors: context => [context.issueId, context.symbolId]},
  {intent: 'IMPACT', question: issueKey => `What is the impact of ${issueKey}?`, anchors: context => [context.issueId]},
  {intent: 'NEIGHBORHOOD', question: issueKey => `Show neighbors around ${issueKey}`, anchors: context => [context.issueId]},
  {intent: 'LINEAGE', question: issueKey => `Show provenance and evidence for ${issueKey}`, anchors: context => [context.issueId]},
  {intent: 'TRACEABILITY', question: issueKey => `Trace the implementation of ${issueKey}`, anchors: context => [context.issueId]},
];
const MCP_TOOLS = [
  'search', 'entity', 'path', 'impact', 'lineage', 'neighbors',
  'document', 'code_symbol', 'jira_issue', 'evidence', 'query',
];

function getGraph(value) {
  if (value?.result?.structuredContent && typeof value.result.structuredContent === 'object') {
    return value.result.structuredContent;
  }
  const text = value?.result?.content?.find(item => item.type === 'text')?.text;
  assert.ok(text, 'MCP tool response must contain structured content or a JSON text result.');
  return JSON.parse(text);
}

function graphIds(value, ids = new Set(), visited = new WeakSet()) {
  if (!value || typeof value !== 'object' || visited.has(value)) return ids;
  visited.add(value);
  if (typeof value.id === 'string') ids.add(value.id);
  if (typeof value.canonical_id === 'string') ids.add(value.canonical_id);
  for (const child of Object.values(value)) graphIds(child, ids, visited);
  return ids;
}

function findEntity(value, canonicalId, visited = new WeakSet()) {
  if (!value || typeof value !== 'object' || visited.has(value)) return undefined;
  visited.add(value);
  if (value.id === canonicalId || value.canonical_id === canonicalId ||
      value.properties?.canonical_id === canonicalId) return value;
  for (const child of Object.values(value)) {
    const found = findEntity(child, canonicalId, visited);
    if (found) return found;
  }
  return undefined;
}

function assertContainsIds(value, expectedIds, message) {
  const ids = graphIds(value);
  for (const expectedId of expectedIds) {
    assert.ok(ids.has(expectedId), `${message}: expected live graph entity ${expectedId}.`);
  }
}

async function run() {
  const steps = [];
  const output = vscode.window.createOutputChannel('EOIP Live Demo');
  const originalInputBox = vscode.window.showInputBox;
  const token = process.env.EOIP_DEMO_TOKEN;
  const receipt = process.env.EOIP_DEMO_RECEIPT;
  const apiUrl = process.env.EOIP_DEMO_API_URL;
  const mcpUrl = process.env.EOIP_DEMO_MCP_URL;
  const context = JSON.parse(process.env.EOIP_DEMO_CONTEXT || '{}');
  const noPause = process.env.EOIP_DEMO_NO_PAUSE === '1';
  const delayMs = Number(process.env.EOIP_DEMO_DELAY_MS ?? 2500);
  delete process.env.EOIP_DEMO_TOKEN;
  function safeMessage(error) {
    const message = error?.message || 'The live demo failed.';
    return token ? message.replaceAll(token, '[REDACTED]') : message;
  }

  try {
    assert.ok(token, 'Demo access token is required.');
    assert.ok(receipt, 'A live demo receipt path is required.');
    assert.ok(apiUrl && mcpUrl, 'Live API and MCP URLs must be provided by the demo driver.');
    assert.ok(Number.isInteger(delayMs) && delayMs >= 0 && delayMs <= 60000,
      'Demo result hold time must be an integer from 0 to 60000 milliseconds.');
    assert.ok(context.issueId && context.issueKey && context.symbolId && context.knowledgeDocumentId &&
      Array.isArray(context.expectedPath), 'Ready live scenario anchors are required.');
    const extension = vscode.extensions.getExtension('eoip-local.eoip-context');
    assert.ok(extension, 'EOIP extension must be loaded.');
    await extension.activate();
    output.show(true);
    output.appendLine('EOIP 0.1.0 source extension / isolated visible profile / LIVE API and MCP');
    const configuration = vscode.workspace.getConfiguration('eoip');
    await configuration.update('apiUrl', apiUrl, vscode.ConfigurationTarget.Global);
    await configuration.update('mcpUrl', mcpUrl, vscode.ConfigurationTarget.Global);
    vscode.window.showInputBox = async () => token;
    await vscode.commands.executeCommand('eoip.setToken');
    vscode.window.showInputBox = originalInputBox;

    async function step(id, name, action) {
      output.appendLine(`Running: ${name}`);
      try {
        const value = await action();
        assert.notEqual(value?.ok, false, `${name} command failed: ${value?.message || value?.code || 'unknown error'}`);
        const receiptStep = {id, name, status: 'PASS'};
        if (value?.interpretation?.plan) {
          receiptStep.intent = value.interpretation.plan.intent;
          receiptStep.anchors = value.interpretation.plan.anchors;
        }
        if (value?.tool) {
          receiptStep.tool = value.tool;
          receiptStep.protocolVersion = value.protocolVersion;
          receiptStep.advertised = value.tools?.includes(value.tool) === true;
        }
        steps.push(receiptStep);
        output.appendLine(`PASS: ${name}`);
        if (delayMs > 0) await new Promise(resolve => setTimeout(resolve, delayMs));
        return value;
      } catch (error) {
        steps.push({id, name, status: 'FAIL', error: safeMessage(error)});
        throw error;
      }
    }

    let symbolName;
    await step('mcp-entity', 'MCP entity lookup for the live code symbol', async () => {
      const result = await vscode.commands.executeCommand('eoip.mcp', {
        tool: 'entity', arguments: {canonical_id: context.symbolId},
      });
      assert.equal(result?.tool, 'entity', 'MCP must return the requested entity tool result.');
      assert.ok(result.protocolVersion, 'MCP entity must complete protocol initialization.');
      assert.ok(result.tools?.includes('entity'), 'MCP tools/list must advertise entity.');
      const symbolGraph = getGraph(result);
      assertContainsIds(symbolGraph, [context.symbolId], 'MCP entity lookup');
      const symbol = findEntity(symbolGraph, context.symbolId);
      symbolName = symbol?.properties?.qualified_name || symbol?.qualified_name;
      assert.ok(symbolName, 'The live code symbol must include a qualified name for symbol lookup and NLQ path.');
      return result;
    });

    const nlqContext = {issueId: context.issueId, symbolId: context.symbolId};
    for (const journey of NLQ_JOURNEYS) {
      const anchors = journey.anchors(nlqContext);
      const question = journey.question(context.issueKey, symbolName, context);
      await step(`nlq-${journey.intent.toLowerCase()}`, `NLQ ${journey.intent}: ${question}`, async () => {
        const result = await vscode.commands.executeCommand('eoip.nlq', question);
        assert.notEqual(result?.ok, false,
          `NLQ ${journey.intent} command failed: ${result?.message || result?.code || 'unknown error'}`);
        assert.equal(result?.interpretation?.plan?.intent, journey.intent,
          'NLQ must select the expected query-plan intent.');
        for (const anchor of anchors) {
          assert.ok(result.interpretation.plan.anchors.includes(anchor),
            `NLQ ${journey.intent} must anchor on ${anchor}.`);
        }
        assertContainsIds(result.result, anchors, `NLQ ${journey.intent}`);
        if (journey.intent === 'PATH') assert.ok(result.result.paths?.length, 'NLQ PATH must return a connected path.');
        if (journey.intent === 'LINEAGE') assert.ok(result.result.evidence?.length, 'NLQ LINEAGE must return source evidence.');
        return result;
      });
    }

    const mcpSteps = [
      {
        tool: 'search', args: {q: context.issueKey, limit: 5},
        verify: graph => assertContainsIds(graph, [context.issueId], 'MCP search'),
      },
      {
        tool: 'path', args: {source_id: context.expectedPath[0], target_id: context.expectedPath[1], max_depth: 8},
        verify: graph => {
          assertContainsIds(graph, [context.expectedPath[0], context.expectedPath[1]], 'MCP path');
          assert.ok(graph.paths?.length, 'MCP path must return a connected path.');
        },
      },
      {
        tool: 'impact', args: {canonical_id: context.issueId, max_depth: 4},
        verify: graph => assertContainsIds(graph, [context.issueId], 'MCP impact'),
      },
      {
        tool: 'lineage', args: {canonical_id: context.issueId, max_depth: 4, result_limit: 100},
        verify: graph => {
          assertContainsIds(graph, [context.issueId], 'MCP lineage');
          assert.ok(graph.evidence?.length, 'MCP lineage must return source evidence.');
        },
      },
      {
        tool: 'neighbors', args: {canonical_id: context.issueId, max_depth: 1, result_limit: 50},
        verify: graph => {
          assertContainsIds(graph, [context.issueId], 'MCP neighbors');
          assert.ok(graph.nodes?.length > 1, 'MCP neighbors must return at least one adjacent live entity.');
        },
      },
      {
        tool: 'document', args: {canonical_id: context.knowledgeDocumentId},
        verify: graph => assertContainsIds(graph, [context.knowledgeDocumentId], 'MCP document'),
      },
      {
        tool: 'code_symbol', args: {qualified_name: symbolName},
        verify: graph => assertContainsIds(graph, [context.symbolId], 'MCP code_symbol'),
      },
      {
        tool: 'jira_issue', args: {issue_key: context.issueKey},
        verify: graph => assertContainsIds(graph, [context.issueId], 'MCP jira_issue'),
      },
      {
        tool: 'evidence', args: {canonical_id: context.issueId},
        verify: graph => {
          assertContainsIds(graph, [context.issueId], 'MCP evidence');
          assert.ok(graph.evidence?.length, 'MCP evidence must return source evidence.');
        },
      },
      {
        tool: 'query',
        args: {plan: {intent: 'IMPACT', anchors: [context.issueId], max_depth: 4,
          result_limit: 100, evidence_mode: 'SUMMARY'}},
        verify: graph => assertContainsIds(graph, [context.issueId], 'MCP query'),
      },
    ];
    assert.deepEqual(['entity', ...mcpSteps.map(item => item.tool)].sort(), [...MCP_TOOLS].sort(),
      'The live demo must cover the complete approved MCP tool set.');
    for (const item of mcpSteps) {
      await step(`mcp-${item.tool}`, `MCP ${item.tool}`, async () => {
        const result = await vscode.commands.executeCommand('eoip.mcp', {tool: item.tool, arguments: item.args});
        assert.equal(result?.tool, item.tool, `MCP must return the requested ${item.tool} tool result.`);
        assert.ok(result.protocolVersion, `MCP ${item.tool} must complete protocol initialization.`);
        assert.ok(result.tools?.includes(item.tool), `MCP tools/list must advertise ${item.tool}.`);
        item.verify(getGraph(result));
        return result;
      });
    }

    const expectedStepCount = NLQ_JOURNEYS.length + MCP_TOOLS.length;
    assert.equal(steps.length, expectedStepCount, 'Every declared live journey must have a passing receipt.');
    assert.ok(steps.every(item => item.status === 'PASS'), 'Every declared live journey must pass.');
    assert.deepEqual(steps.filter(item => item.intent).map(item => item.intent),
      NLQ_JOURNEYS.map(item => item.intent), 'Receipt must prove each NLQ intent executed.');
    assert.deepEqual(steps.filter(item => item.tool).map(item => item.tool).sort(),
      [...MCP_TOOLS].sort(), 'Receipt must prove each approved MCP tool executed.');
    await fs.writeFile(receipt, JSON.stringify({
      status: 'PASS',
      mode: 'live-visible-source-extension-host',
      extensionVersion: extension.packageJSON.version,
      vscode: vscode.version,
      scenario: 'intent-to-runtime',
      entrypoint: context.issueId,
      steps,
      coverage: {
        nlqIntents: NLQ_JOURNEYS.map(item => item.intent),
        mcpTools: MCP_TOOLS,
        mcpHandshake: 'initialize + notifications/initialized + tools/list + tools/call for each MCP tool invocation',
      },
      limitations: ['Loads the workspace source extension in an isolated VS Code development host; does not install or certify a VSIX.',
        'Live graph data must already contain the required ready demo scenarios; this runner does not provision or seed graph data.',
        'Does not certify all product scenarios, independent QA, or visual layout.'],
    }, null, 2));
    output.appendLine(`PASS: ${steps.length}/${expectedStepCount} live journeys. Receipt: ${receipt}`);
    if (!noPause) {
      await vscode.window.showInformationMessage(
        `EOIP live demo complete: ${steps.length}/${expectedStepCount} steps passed. The receipt is saved under test-results/.`,
        'Close Demo',
      );
    }
  } catch (error) {
    const message = safeMessage(error);
    output.appendLine(`FAIL: ${message}`);
    if (receipt) {
      await fs.writeFile(receipt, JSON.stringify({
        status: 'FAIL', mode: 'live-visible-source-extension-host', steps, error: message,
      }, null, 2));
    }
    throw error;
  } finally {
    vscode.window.showInputBox = originalInputBox;
    output.dispose();
  }
}

module.exports = {run};
