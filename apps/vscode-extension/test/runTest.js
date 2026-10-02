const path = require('node:path');
const {runTests} = require('@vscode/test-electron');

async function main() {
  const options = {
    extensionDevelopmentPath: path.resolve(__dirname, '..'),
    extensionTestsPath: path.resolve(__dirname, 'suite'),
    launchArgs: ['--disable-gpu', '--skip-welcome'],
  };
  if (process.env.VSCODE_EXECUTABLE) {
    options.vscodeExecutablePath = process.env.VSCODE_EXECUTABLE;
  }
  await runTests(options);
}

main().catch(error => {
  console.error('VS Code extension-host tests failed:', error);
  process.exitCode = 1;
});
