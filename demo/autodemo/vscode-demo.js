const fs = require('node:fs/promises');
const path = require('node:path');
const {randomUUID} = require('node:crypto');

const NLQ_INTENTS = ['SEARCH', 'PATH', 'IMPACT', 'NEIGHBORHOOD', 'LINEAGE', 'TRACEABILITY'];
const MCP_TOOLS = [
  'search', 'entity', 'path', 'impact', 'lineage', 'neighbors',
  'document', 'code_symbol', 'jira_issue', 'evidence', 'query',
];
const EXPECTED_STEPS = NLQ_INTENTS.length + MCP_TOOLS.length;
let receiptPath;
let demoToken;

function parseOptions(args) {
  const options = {dryRun: false, noPause: false, delay: 2500, help: false};
  for (let index = 0; index < args.length; index++) {
    const arg = args[index];
    if (arg === '--dry-run') options.dryRun = true;
    else if (arg === '--no-pause') options.noPause = true;
    else if (arg === '--help' || arg === '-h') options.help = true;
    else if (arg === '--delay') {
      const value = args[++index];
      if (value === undefined || value.startsWith('--')) {
        throw new Error('Usage: node vscode-demo.js [--dry-run] [--no-pause] [--delay MS] [--help] (--delay requires a value)');
      }
      options.delay = Number(value);
      if (!Number.isFinite(options.delay) || options.delay < 0 || options.delay > 60000) {
        throw new Error('--delay must be a number from 0 to 60000 milliseconds.');
      }
    }
    else throw new Error(`Usage: node vscode-demo.js [--dry-run] [--no-pause] [--help] (unknown option: ${arg})`);
  }
  return options;
}

function printHelp() {
  console.log('Usage: node vscode-demo.js [--dry-run] [--no-pause] [--delay MS] [--help]');
  console.log('Runs the visible eoip-context 0.1.0 source extension against live EOIP API and MCP services.');
  console.log('--dry-run   Print coverage and prerequisites without reading credentials or contacting services.');
  console.log('--delay MS  Set result hold time between steps (0..60000; default 2500).');
  console.log('--no-pause  Skip result hold delays and the final VS Code confirmation prompt (equivalent to --delay 0).');
}

function printDryRun(root, options) {
  const extension = path.join(root, 'apps', 'vscode-extension');
  const executable = process.env.VSCODE_EXECUTABLE ||
    path.join(extension, '.vscode-test', 'vscode-win32-x64-archive-1.96.4', 'Code.exe');
  console.log('DRY RUN: visible VS Code development host using the eoip-context 0.1.0 source extension.');
  console.log(`Coverage: ${NLQ_INTENTS.length} NLQ intents (${NLQ_INTENTS.join(', ')}).`);
  console.log(`Coverage: ${MCP_TOOLS.length} read-only MCP tools (${MCP_TOOLS.join(', ')}), each using initialize, tools/list, and tools/call.`);
  console.log(`Expected live steps: ${EXPECTED_STEPS}.`);
  console.log(`Result hold: ${options.noPause ? 0 : options.delay} ms between steps; final confirmation ${options.noPause ? 'disabled' : 'enabled'}.`);
  console.log(`VS Code executable: ${executable}`);
  console.log('Live prerequisites: Node.js, extension dependencies, VS Code executable, healthy API and MCP endpoints, ready intent-to-runtime and knowledge-provenance scenarios, EOIP_API_TOKEN.');
  console.log('No VSIX is installed or certified. No credentials or services were accessed.');
}

function hasExactCoverage(actual, expected) {
  if (!Array.isArray(actual) || actual.length !== expected.length) return false;
  const sortedExpected = [...expected].sort();
  return [...actual].sort().every((value, index) => value === sortedExpected[index]);
}

async function readToken(root) {
  if (process.env.EOIP_API_TOKEN?.trim()) return process.env.EOIP_API_TOKEN.trim();
  try {
    const envFile = await fs.readFile(path.join(root, 'deploy', '.env'), 'utf8');
    const match = envFile.match(/^EOIP_API_TOKEN=(.*)$/m);
    const value = match?.[1]?.trim().replace(/^(['"])(.*)\1$/, '$2');
    if (value) return value;
  } catch (error) {
    if (error.code !== 'ENOENT') throw new Error('Unable to read deploy/.env for the EOIP access token.');
  }
  throw new Error('EOIP_API_TOKEN is required in the process environment or deploy/.env.');
}

function safeMessage(error) {
  const message = error?.message || 'The demo failed.';
  return demoToken ? message.replaceAll(demoToken, '[REDACTED]') : message;
}

async function request(url, token) {
  let response;
  try {
    response = await fetch(url, {
      headers: {Authorization: `Bearer ${token}`},
      signal: AbortSignal.timeout(10000),
    });
  } catch (error) {
    throw new Error(`Could not reach ${new URL(url).origin} (${error.name || 'network error'}).`);
  }
  if (!response.ok) throw new Error(`Live prerequisite returned HTTP ${response.status} at ${new URL(url).pathname}.`);
  return response;
}

async function verifyLivePrerequisites(apiUrl, mcpUrl, token) {
  const apiRoot = apiUrl.replace(/\/+$/, '');
  await request(`${apiRoot}/health/ready`, token);
  await request(new URL('/health/live', mcpUrl).toString(), token);
  const response = await request(`${apiRoot}/api/v1/demo/scenarios`, token);
  const catalog = await response.json();
  const intentScenario = catalog.scenarios?.find(item => item.id === 'intent-to-runtime' && item.ready === true);
  const knowledgeScenario = catalog.scenarios?.find(item => item.id === 'knowledge-provenance' && item.ready === true);
  const missing = ['intent-to-runtime', 'knowledge-provenance'].filter(id =>
    !catalog.scenarios?.some(item => item.id === id && item.ready === true));
  if (missing.length) {
    throw new Error(`Required live demo scenario(s) are not ready: ${missing.join(', ')}. Ingest the approved demo scenario pack and verify /api/v1/demo/scenarios reports them ready. This launcher does not seed or preload graph data.`);
  }
  const expectedPath = intentScenario.expected_path;
  const symbolId = expectedPath?.find(id => id.includes(':symbol:'));
  const issueKey = intentScenario.entrypoint?.match(/[A-Z][A-Z0-9]+-\d+/)?.[0];
  if (!Array.isArray(expectedPath) || expectedPath.length < 2 || !symbolId || !issueKey) {
    throw new Error('The ready intent-to-runtime scenario is missing its expected issue-to-code path.');
  }
  return {
    issueId: intentScenario.entrypoint,
    issueKey,
    symbolId,
    knowledgeDocumentId: knowledgeScenario.entrypoint,
    expectedPath,
  };
}

async function persistFailure(error) {
  if (!receiptPath) return;
  let existing = {};
  try {
    existing = JSON.parse(await fs.readFile(receiptPath, 'utf8'));
  } catch (readError) {
    if (readError.code !== 'ENOENT') throw readError;
  }
  await fs.writeFile(receiptPath, JSON.stringify({
    ...existing, status: 'FAIL', exit_code: 1, hostError: safeMessage(error), timestamp: new Date().toISOString(),
  }, null, 2));
  console.error(`Failure receipt: ${receiptPath}`);
}

async function main() {
  const options = parseOptions(process.argv.slice(2));
  if (options.help) {
    printHelp();
    return;
  }
  const root = path.resolve(__dirname, '..', '..');
  const extensionPath = path.join(root, 'apps', 'vscode-extension');
  const executable = process.env.VSCODE_EXECUTABLE ||
    path.join(extensionPath, '.vscode-test', 'vscode-win32-x64-archive-1.96.4', 'Code.exe');
  if (options.dryRun) {
    printDryRun(root, options);
    return;
  }

  receiptPath = path.join(root, 'test-results',
    `vscode-live-demo-${new Date().toISOString().replace(/[:.]/g, '-')}-${randomUUID()}.json`);
  await fs.mkdir(path.dirname(receiptPath), {recursive: true});
  let profile;
  try {
    try {
      await fs.access(executable);
    } catch {
      throw new Error(`VS Code executable not found at ${executable}. Set VSCODE_EXECUTABLE to a compatible Code.exe.`);
    }
    demoToken = await readToken(root);
    const apiUrl = process.env.EOIP_API_URL || 'http://localhost:8000';
    const mcpUrl = process.env.EOIP_MCP_URL || 'http://localhost:8001/mcp';
    const context = await verifyLivePrerequisites(apiUrl, mcpUrl, demoToken);
    try {
      await fs.access(path.join(extensionPath, 'node_modules', '@vscode', 'test-electron'));
    } catch {
      throw new Error('VS Code extension dependencies are missing. Run npm install in apps/vscode-extension.');
    }
    const {runTests} = require(path.join(extensionPath, 'node_modules', '@vscode', 'test-electron'));
    delete process.env.ELECTRON_RUN_AS_NODE;
    profile = path.join(extensionPath, '.vscode-test', `demo-${randomUUID()}`);
    await fs.mkdir(profile, {recursive: true});
    await runTests({
      vscodeExecutablePath: executable,
      extensionDevelopmentPath: extensionPath,
      extensionTestsPath: path.join(extensionPath, 'demo'),
      launchArgs: ['--disable-gpu', '--skip-welcome', '--disable-extensions',
        `--user-data-dir=${path.join(profile, 'user-data')}`, `--extensions-dir=${path.join(profile, 'extensions')}`],
      extensionTestsEnv: {
        EOIP_DEMO_TOKEN: demoToken,
        EOIP_DEMO_RECEIPT: receiptPath,
        EOIP_DEMO_API_URL: apiUrl,
        EOIP_DEMO_MCP_URL: mcpUrl,
        EOIP_DEMO_NO_PAUSE: options.noPause ? '1' : '',
        EOIP_DEMO_DELAY_MS: String(options.noPause ? 0 : options.delay),
        EOIP_DEMO_CONTEXT: JSON.stringify(context),
      },
    });
    const result = JSON.parse(await fs.readFile(receiptPath, 'utf8'));
    if (result.status !== 'PASS' || result.steps?.length !== EXPECTED_STEPS ||
        !result.steps.every(item => item.status === 'PASS') ||
        !hasExactCoverage(result.coverage?.nlqIntents, NLQ_INTENTS) ||
        !hasExactCoverage(result.coverage?.mcpTools, MCP_TOOLS)) {
      throw new Error(`VS Code demo receipt is incomplete: expected ${EXPECTED_STEPS} passing steps, ${NLQ_INTENTS.length} NLQ intents, and ${MCP_TOOLS.length} MCP tools.`);
    }
    await fs.writeFile(receiptPath, JSON.stringify({...result, exit_code: 0, timestamp: new Date().toISOString()}, null, 2));
    console.log(`Live VS Code demo receipt: ${receiptPath}`);
  } catch (error) {
    await persistFailure(error);
    throw error;
  } finally {
    if (profile) await fs.rm(profile, {recursive: true, force: true, maxRetries: 20, retryDelay: 250});
  }
}

main().catch(error => {
  console.error(`VS Code live demo failed: ${safeMessage(error)}`);
  console.error('The demo uses the visible source extension, not an installed VSIX. Check the receipt for passed steps and the specific missing live prerequisite.');
  process.exitCode = 1;
});
