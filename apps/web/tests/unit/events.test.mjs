import assert from 'node:assert/strict';
import {test} from 'node:test';
import {mergeEvents} from '../../src/shared/events/merge.ts';

const event = id => ({event_id: id, type: 'vertex_upserted', data: {canonical_id: `fixture:${id}`}});

test('out of order and replayed events are sorted, deduplicated and bounded', () => {
  const result = mergeEvents([event(1), event(2)], [event(5), event(3), event(3), event(2)], 2, 3);
  assert.deepEqual(result.events.map(item => item.event_id), [2, 3, 5]);
  assert.equal(result.cursor, 5);
});

test('an empty replay preserves the cursor and malformed events are rejected', () => {
  assert.equal(mergeEvents([], [], 7).cursor, 7);
  for (const invalid of [null, {}, [{event_id: NaN}], [{...event(1), data: []}], [{...event(1), event_id: 1.5}]]) {
    assert.throws(() => mergeEvents([], invalid, 0));
  }
});
