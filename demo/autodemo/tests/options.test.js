const {test} = require('node:test');
const assert = require('node:assert/strict');
const {options} = require('../browser-demo');

test('visible paced defaults and unattended override', () => {
  assert.equal(options([], 'full').delay, 2500);
  assert.equal(options([], 'full').headless, false);
  assert.equal(options(['--no-pause', '--delay', '0', '--headless'], 'admin').delay, 0);
});

test('invalid input is rejected before any service or credential access', () => {
  for (const args of [['--mode'], ['--delay', 'NaN'], ['--delay', '-1'],
    ['--mode', 'unknown'], ['--dataset', 'wrong'], ['--data-dir', 'legacy'],
    ['--api-url', 'https://example.com']]) assert.throws(() => options(args, 'full'));
});

test('manual, pipeline and administration modes remain selectable', () => {
  for (const mode of ['manual', 'pipeline', 'admin']) {
    assert.equal(options([mode, '--dry-run'], 'full').mode, mode);
    assert.equal(options([mode, '--dry-run'], 'full').dryRun, true);
  }
});
