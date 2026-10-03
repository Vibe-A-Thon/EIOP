const path = require('node:path');
const fs = require('node:fs/promises');
const {randomUUID} = require('node:crypto');
const {runTests} = require('@vscode/test-electron');

async function main() {
  const runId = randomUUID();
  const profile = path.resolve(__dirname, '..', '.vscode-test', runId);
  const receipt = path.resolve(__dirname, '..', '..', '..', 'test-results', `extension-host-${runId}.json`);
  await fs.mkdir(profile, {recursive: true});
  await fs.mkdir(path.dirname(receipt), {recursive: true});
  const options = {
    extensionDevelopmentPath: path.resolve(__dirname, '..'),
    extensionTestsPath: path.resolve(__dirname, 'suite'),
    launchArgs: [
      '--disable-gpu', '--skip-welcome', '--disable-extensions',
      `--user-data-dir=${path.join(profile, 'user-data')}`,
      `--extensions-dir=${path.join(profile, 'extensions')}`,
    ],
    extensionTestsEnv: {EOIP_EXTENSION_RECEIPT: receipt},
  };
  if (process.env.VSCODE_EXECUTABLE) {
    options.vscodeExecutablePath = process.env.VSCODE_EXECUTABLE;
  }
  try {
    try {
      await runTests(options);
    } finally {
      await fs.rm(profile, {recursive: true, force: true, maxRetries: 20, retryDelay: 250});
    }
    const result = JSON.parse(await fs.readFile(receipt, 'utf8'));
    if (result.status !== 'PASS' || result.passed !== 4 || result.failed !== 0) {
      throw new Error('Extension host did not produce all four passing journey receipts.');
    }
    result.exit_code = 0;
    await fs.writeFile(receipt, JSON.stringify(result, null, 2));
    console.log(`Acceptance receipt: ${receipt}`);
  } catch (error) {
    await fs.writeFile(receipt, JSON.stringify({status: 'FAIL', exit_code: 1, error: error.message}, null, 2));
    throw error;
  }
}

main().catch(error => {
  console.error('VS Code extension-host tests failed:', error);
  process.exitCode = 1;
});
