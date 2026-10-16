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
  assert.match(result.stdout, /No credentials or services were accessed/);
  assert.match(result.stdout, /SEARCH, PATH, IMPACT, NEIGHBORHOOD, LINEAGE, TRACEABILITY/);
  assert.match(result.stdout, /11 read-only MCP tools/);
  assert.match(result.stdout, /Expected live steps: 17/);
  assert.doesNotMatch(result.stdout, /Live VS Code demo receipt/);
});

test('desktop dry-run accepts no-pause without contacting live services', () => {
  const env = {...process.env};
  env.EOIP_API_TOKEN = 'demo-secret-not-for-output';
  const result = spawnSync(process.execPath, [driver, '--no-pause', '--dry-run'], {
    env, encoding: 'utf8', timeout: 5000,
  });
  assert.equal(result.status, 0, result.stderr);
  assert.match(result.stdout, /DRY RUN/);
  assert.match(result.stdout, /Result hold: 0 ms.*final confirmation disabled/);
  assert.doesNotMatch(result.stdout, /demo-secret-not-for-output/);
});

test('desktop dry-run reports configurable visible result pacing', () => {
  const result = spawnSync(process.execPath, [driver, '--dry-run', '--delay', '1200'], {
    encoding: 'utf8', timeout: 5000,
  });
  assert.equal(result.status, 0, result.stderr);
  assert.match(result.stdout, /Result hold: 1200 ms.*final confirmation enabled/);
});

test('desktop driver rejects invalid delays before launching a host', () => {
  const result = spawnSync(process.execPath, [driver, '--delay', '60001'], {encoding: 'utf8', timeout: 5000});
  assert.equal(result.status, 1);
  assert.match(result.stderr, /--delay must be a number from 0 to 60000 milliseconds/);
  assert.doesNotMatch(result.stdout, /Live VS Code demo receipt/);
});

test('desktop driver refuses unknown options before launching a host', () => {
  const result = spawnSync(process.execPath, [driver, '--unknown'], {encoding: 'utf8', timeout: 5000});
  assert.equal(result.status, 1);
  assert.match(result.stderr, /Usage: node vscode-demo.js/);
  assert.doesNotMatch(result.stdout, /Live VS Code demo receipt/);
});
