const {test} = require('node:test');
const assert = require('node:assert/strict');
const {spawnSync} = require('node:child_process');
const path = require('node:path');

function run(script, args) {
  return spawnSync(process.execPath, [path.join(__dirname, '..', script), ...args],
    {encoding: 'utf8', env: {...process.env, EOIP_API_TOKEN: ''}});
}

test('application and admin dry runs need no token, Docker, browser or installed Playwright', () => {
  for (const script of ['application-demo.js', 'administration-demo.js']) {
    const child = run(script, ['--dry-run']);
    assert.equal(child.status, 0, child.stderr);
    const plan = JSON.parse(child.stdout);
    assert.ok(plan.stages.length >= 7);
    assert.ok(plan.coverage.includes('NOT_DEMONSTRATED'));
  }
});

test('manual and pipeline shared launcher dry runs execute the selected sequence', () => {
  for (const mode of ['manual', 'pipeline']) {
    const child = run('launch-demo.js', [mode, '--dry-run', '--no-pause']);
    assert.equal(child.status, 0, child.stderr);
    assert.ok(child.stdout.includes(`"mode": "${mode}"`));
  }
});

test('invalid launch arguments fail rather than start a partial demo', () => {
  const child = run('launch-demo.js', ['--unknown']);
  assert.equal(child.status, 1);
  assert.ok(child.stderr.includes('Unknown argument'));
});

test('full dry-run includes independent administration datasets and paced extension', () => {
  const child = run('launch-demo.js', ['full', '--dry-run', '--delay', '123']);
  assert.equal(child.status, 0, child.stderr);
  assert.equal((child.stdout.match(/"mode": "admin"/g) || []).length, 2);
  assert.ok(child.stdout.includes('Expected live steps: 17.'));
  assert.ok(child.stdout.includes('Result hold: 123 ms'));
});
