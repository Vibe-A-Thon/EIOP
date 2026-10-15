import assert from 'node:assert/strict';
import {readFile} from 'node:fs/promises';
import {test} from 'node:test';
import {markdownCells, sourceRegistry} from '../../../../scripts/audit_gui.mjs';

test('intake table parser preserves pipes in code and escaped prose', () => {
  assert.deepEqual(markdownCells('| `POST /query/a|b` | a\\|b | final |'), ['`POST /query/a|b`', 'a\\|b', 'final']);
});

test('all nonblank source lines and all original IDs survive intake without promotion', async () => {
  const buffer = await readFile(new URL('../../../../GUI-UIX-requirements.md', import.meta.url));
  const result = sourceRegistry(buffer);
  assert.equal(result.integrations.length, 735);
  assert.equal(result.screens.length, 27);
  assert.equal(result.backends.length, 20);
  const lines = buffer.toString('utf8').split(/\r?\n/).filter(line => line.trim());
  assert.deepEqual(result.intake.map(item => item.text), lines);
  assert.ok(result.intake.every(item => item.acceptance_status === 'NOT_EVALUATED'));
  assert.throws(() => sourceRegistry(Buffer.from(buffer.toString('utf8').replaceAll('`INT-735`', '`INT-001`'))), /baseline changed/);
});
