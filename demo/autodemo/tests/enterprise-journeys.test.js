const {test} = require('node:test');
const assert = require('node:assert/strict');
const {enterpriseJourneys} = require('../enterprise-journeys');

test('extended journeys are distinct and do not silently accept empty federation', async () => {
  const steps = enterpriseJourneys(async () => ({sources: []}), 'EOIP-1', 'test-run');
  assert.equal(steps.length, 8);
  assert.equal(new Set(steps.map(([title]) => title)).size, steps.length);
  await assert.rejects(steps[0][1](), /no registered sources/);
});

test('template cleanup deletes only its created ID even after binding fails', async () => {
  const calls = [];
  const api = async (route, body, verify, options) => {
    calls.push({route, options});
    if (route === '/api/v1/query/templates') return {template_id: 'owned-by-test'};
    if (route.endsWith('/bind')) return {anchors: ['wrong-anchor']};
    if (options?.method === 'DELETE') return {deleted: true};
    throw new Error(`Unexpected request: ${route}`);
  };
  await assert.rejects(enterpriseJourneys(api, 'EOIP-1', 'test-run')[2][1](), /wrong anchor/);
  assert.deepEqual(calls.at(-1), {
    route: '/api/v1/query/templates/owned-by-test', options: {method: 'DELETE'},
  });
  assert.equal(calls.filter(item => item.options?.method === 'DELETE').length, 1);
});

test('a deliberately failing graph assertion must actually fail, not just return HTTP 200', async () => {
  let count = 0;
  const api = async () => {
    count++;
    return {conformant: true, passed: 1, failed: 0};
  };
  await assert.rejects(enterpriseJourneys(api, 'EOIP-1', 'test-run')[4][1](), /not reported/);
  assert.equal(count, 2);
});

test('negative graph assertion uses a valid seeded label and contradictory connection bounds', async () => {
  const bodies = [];
  const api = async (route, body) => {
    assert.equal(route, '/api/v1/graph-tests/run');
    bodies.push(body);
    return {conformant: bodies.length === 1, failed: bodies.length === 1 ? 0 : 1};
  };
  await enterpriseJourneys(api, 'EOIP-1', 'test-run')[4][1]();
  assert.equal(bodies[0].assertions[0].min_count, 1);
  assert.equal(bodies[1].assertions[0].max_count, 0);
  for (const body of bodies) {
    assert.equal(body.assertions[0].label, 'WorkItem');
    assert.deepEqual(body.assertions[0].filters, {canonical_id: 'urn:eoip:work:item:jira:EOIP-1'});
  }
});

test('truth resolution rejects a success-shaped response selecting the weaker source', async () => {
  const api = async route => route.endsWith('/resolve') ? {chosen_claim_id: 'secondary'} : {};
  await assert.rejects(enterpriseJourneys(api, 'EOIP-1', 'test-run')[1][1](), /wrong authority/);
});
