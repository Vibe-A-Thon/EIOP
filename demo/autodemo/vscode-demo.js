const fs = require('node:fs/promises');
const path = require('node:path');
const {randomUUID} = require('node:crypto');
let receiptPath;

async function main() {
  const root = path.resolve(__dirname, '..', '..');
  const extension = path.join(root, 'apps', 'vscode-extension');
  const executable = path.join(extension, '.vscode-test', 'vscode-win32-x64-archive-1.96.4', 'Code.exe');
  const receipt = path.join(root, 'test-results', `vscode-live-demo-${randomUUID()}.json`);
  const dryRun = process.argv.includes('--dry-run');
  if (process.argv.slice(2).some(arg => arg !== '--dry-run')) throw new Error('Usage: node vscode-demo.js [--dry-run]');
  if (dryRun) {
    console.log('DRY RUN: isolated visible VS Code 0.1.0 source extension; NLQ impact, MCP handshake/search/lineage; no credentials or services accessed.');
    console.log(`Required cached runtime: ${executable}`);
    return;
  }
  receiptPath = receipt;
  await fs.mkdir(path.dirname(receipt), {recursive: true});
  await fs.access(executable);
  const {runTests} = require(path.join(extension, 'node_modules', '@vscode', 'test-electron'));
  let token = process.env.EOIP_API_TOKEN;
  if (!token) {
    const env = await fs.readFile(path.join(root, 'deploy', '.env'), 'utf8');
    token = env.match(/^EOIP_API_TOKEN=(.+)$/m)?.[1].trim();
  }
  if (!token) throw new Error('EOIP_API_TOKEN is required in the environment or deploy .env.');
  const catalogResponse = await fetch('http://localhost:8000/api/v1/demo/scenarios', {
    headers: {Authorization: `Bearer ${token}`}, signal: AbortSignal.timeout(60000),
  });
  if (!catalogResponse.ok) throw new Error(`Live demo catalog failed with HTTP ${catalogResponse.status}.`);
  const catalog = await catalogResponse.json();
  const scenario = catalog.scenarios?.find(item => item.id === 'intent-to-runtime' && item.ready === true);
  if (!scenario || typeof scenario.entrypoint !== 'string') throw new Error('The live intent-to-runtime scenario is not ready. Load the approved demo dataset first.');
  delete process.env.ELECTRON_RUN_AS_NODE;
  const profile = path.join(extension, '.vscode-test', `demo-${randomUUID()}`);
  await fs.mkdir(profile, {recursive: true});
  await fs.mkdir(path.dirname(receipt), {recursive: true});
  try {
    await runTests({
      vscodeExecutablePath: executable, extensionDevelopmentPath: extension,
      extensionTestsPath: path.join(extension, 'demo'),
      launchArgs: ['--disable-gpu', '--skip-welcome', '--disable-extensions',
        `--user-data-dir=${path.join(profile, 'user-data')}`, `--extensions-dir=${path.join(profile, 'extensions')}`],
      extensionTestsEnv: {EOIP_DEMO_TOKEN: token, EOIP_DEMO_RECEIPT: receipt, EOIP_DEMO_ANCHOR: scenario.entrypoint},
    });
    const result = JSON.parse(await fs.readFile(receipt, 'utf8'));
    if (result.status !== 'PASS' || result.steps.length !== 3) throw new Error('VS Code demo did not complete all live steps.');
    await fs.writeFile(receipt, JSON.stringify({...result, exit_code: 0, timestamp: new Date().toISOString()}, null, 2));
    console.log(`Live VS Code demo receipt: ${receipt}`);
  } finally {
    await fs.rm(profile, {recursive: true, force: true, maxRetries: 20, retryDelay: 250});
  }
}

main().catch(async error => {
  if (receiptPath) {
    let detail;
    try {
      detail = JSON.parse(await fs.readFile(receiptPath, 'utf8'));
    } catch (readError) {
      if (readError.code !== 'ENOENT') {
        console.error(`Unable to read demo receipt: ${readError.message}`);
      }
      detail = {};
    }
    await fs.writeFile(receiptPath, JSON.stringify({...detail, status: 'FAIL', exit_code: 1, hostError: error.message}, null, 2));
    console.error(`Failure receipt: ${receiptPath}`);
  }
  console.error(`VS Code demo error: ${error.message}`);
  console.error('VS Code live demo failed. Check the visible EOIP output/receipt and prerequisites: cached VS Code 1.96.4, extension node_modules, API:8000, MCP:8001, ready intent-to-runtime scenario and access token. No fixture fallback was used.');
  process.exitCode = 1;
}).catch(error => {
  console.error(`Unable to persist failure receipt: ${error.message}`);
  process.exitCode = 1;
});
