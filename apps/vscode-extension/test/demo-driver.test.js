const assert = require('node:assert/strict');
const path = require('node:path');
const {spawnSync} = require('node:child_process');
const {test} = require('node:test');

const driver = path.resolve(__dirname, '..', '..', '..', 'demo', 'autodemo', 'vscode-demo.js');

test('desktop dry-run succeeds without a token or live-service access', () => {
  const env = {...process.env};
  delete env.EOIP_API_TOKEN;
  const result = spawnSync(process.execPath, [driver, '--dry-run'], {env, encoding: 'utf8', timeout: 5000});
  assert.equal(result.status, 0, result.stderr);
  assert.match(result.stdout, /DRY RUN/);
  assert.match(result.stdout, /no credentials or services accessed/);
  assert.doesNotMatch(result.stdout, /Live VS Code demo receipt/);
});

test('desktop driver refuses unknown options before launching a host', () => {
  const result = spawnSync(process.execPath, [driver, '--unknown'], {encoding: 'utf8', timeout: 5000});
  assert.equal(result.status, 1);
  assert.match(result.stderr, /Usage: node vscode-demo.js/);
  assert.doesNotMatch(result.stdout, /Live VS Code demo receipt/);
});
