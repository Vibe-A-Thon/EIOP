const {spawnSync} = require('node:child_process');
const path = require('node:path');
const {options} = require('./browser-demo');

const root = path.resolve(__dirname, '..', '..');
const args = process.argv.slice(2);

function run(command, arguments_) {
  const child = spawnSync(command, arguments_, {cwd: root, stdio: 'inherit', env: process.env});
  if (child.error) throw child.error;
  if (child.status !== 0) throw new Error(`${path.basename(command)} failed (${child.status ?? child.signal})`);
}

try {
  if (args.includes('--help') || args.includes('-h')) {
    console.log('Usage: run-demo.bat [full|manual|pipeline|admin] [--delay MS] [--headless] [--no-pause] [--dry-run] [--output FILE]');
    console.log('Full: visible enterprise walkthrough, both ingestion datasets, administration and isolated VS Code NLQ/MCP.');
    console.log('Defaults: local Docker services, Edge browser, 2500 ms per result/window, pause before closing launcher.');
    console.log('Receipts distinguish demonstrated capabilities from unexecuted/prerequisite-dependent operations.');
  } else {
    const config = options(args, 'full');
    const forwarded = ['--delay', String(config.delay), '--base-url', config.baseURL, '--api-url', config.apiURL];
    if (config.headless) forwarded.push('--headless');
    if (config.dryRun) forwarded.push('--dry-run');
    if (config.noPause) forwarded.push('--no-pause');
    const phases = config.mode === 'full'
      ? [{script: 'application-demo.js', mode: 'full'},
        {script: 'administration-demo.js', mode: 'admin', dataset: 'manual'},
        {script: 'administration-demo.js', mode: 'admin', dataset: 'pipelines'}]
      : [{script: config.mode === 'admin' ? 'administration-demo.js' : 'application-demo.js', mode: config.mode}];
    // Validate all arguments before starting services or accessing credentials.
    if (!config.dryRun) run('powershell.exe', ['-NoProfile', '-ExecutionPolicy', 'Bypass',
      '-File', path.join(root, 'scripts', 'docker.ps1'), 'up']);
    for (const [index, phase] of phases.entries()) {
      const childArgs = [path.join(__dirname, phase.script), '--mode', phase.mode, ...forwarded];
      if (phase.dataset) childArgs.push('--dataset', phase.dataset);
      if (config.output) {
        const extension = path.extname(config.output);
        childArgs.push('--output', phases.length === 1 ? config.output :
          `${config.output.slice(0, config.output.length - extension.length)}-${index + 1}${extension || '.json'}`);
      }
      run(process.execPath, childArgs);
    }
    if (config.mode === 'full') run(process.execPath, [path.join(__dirname, 'vscode-demo.js'),
      '--delay', String(config.delay),
      ...(config.noPause ? ['--no-pause'] : []),
      ...(config.dryRun ? ['--dry-run'] : [])]);
    console.log('Selected demo sequences finished. Read receipts for coverage boundaries; this is not an all-requirements certification.');
  }
} catch (error) {
  console.error(`Demo launcher failed: ${error.message}`);
  process.exitCode = 1;
}
