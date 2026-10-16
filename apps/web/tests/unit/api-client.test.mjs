import assert from 'node:assert/strict';
import {test} from 'node:test';
import {ApiError, createApiClient} from '../../src/shared/api/client.ts';
import {policyDocument} from '../../src/shared/api/policies.ts';
import {destinationFor} from '../../src/app/navigation.ts';

test('requests carry in-memory credentials, unique correlation and serialize JSON', async () => {
  const calls = [];
  const api = createApiClient('test-secret', async (...args) => {
    calls.push(args); return new Response('{"ok":true}', {headers: {'content-type': 'application/json'}});
  });
  assert.deepEqual(await api('/api/items', {value: 4}), {ok: true});
  await api('/api/items');
  assert.equal(calls[0][1].headers.Authorization, 'Bearer test-secret');
  assert.equal(calls[0][1].body, '{"value":4}');
  assert.notEqual(calls[0][1].headers['X-Request-ID'], calls[1][1].headers['X-Request-ID']);
  assert.equal(calls[0][1].redirect, 'error');
});

test('204 responses remain empty and YAML policy bodies remain unquoted', async () => {
  let request;
  const api = createApiClient('secret', async (_path, init) => {
    request = init; return new Response(null, {status: 204});
  });
  assert.equal(await api('/api/policies', 'policies: []', 'POST', {contentType: 'application/yaml'}), null);
  assert.equal(request.body, 'policies: []');
  assert.equal(request.headers['Content-Type'], 'application/yaml');
});

for (const [status, body, message] of [
  [403, {detail: 'Access denied'}, 'Access denied'],
  [409, {title: 'Revision conflict'}, 'Revision conflict'],
  [422, {detail: [{loc: ['body'], msg: 'bad'}]}, 'Some fields are invalid.'],
]) test(`normalizes ${status} errors with correlation`, async () => {
  const api = createApiClient('secret', async () => new Response(JSON.stringify(body), {
    status, headers: {'content-type': 'application/problem+json', 'X-Correlation-ID': 'trace-fixture'},
  }));
  await assert.rejects(api('/api/items'), error => error instanceof ApiError && error.status === status
    && error.message.startsWith(message) && error.correlationId === 'trace-fixture');
});

test('rejects malformed JSON without accepting success', async () => {
  const api = createApiClient('secret', async () => new Response('{broken', {headers: {'content-type': 'application/json'}}));
  await assert.rejects(api('/api/items'), /unreadable response/);
});

test('never retries a failed mutation', async () => {
  let count = 0;
  const api = createApiClient('secret', async () => {count++; return new Response('', {status: 503});});
  await assert.rejects(api('/api/items', {value: 1}));
  assert.equal(count, 1);
});

test('refuses off-origin or protocol-relative requests before sending credentials', async () => {
  let calls = 0;
  const api = createApiClient('secret', async () => {calls++; return new Response('');});
  for (const path of ['https://other.invalid/api', '//other.invalid/api', '/\\other.invalid/api', 'api/items']) {
    await assert.rejects(api(path));
  }
  assert.equal(calls, 0);
});

test('disconnect aborts pending work and rejects late responses even if fetch ignores abort', async () => {
  let finish;
  let signal;
  const api = createApiClient('secret', async (_path, init) => {
    signal = init.signal;
    return await new Promise(resolve => {finish = resolve;});
  });
  const request = api('/api/items');
  api.dispose();
  assert.equal(signal.aborted, true);
  finish(new Response('{"private":"old connection"}', {headers: {'content-type': 'application/json'}}));
  await assert.rejects(request, {name: 'AbortError'});
  await assert.rejects(api('/api/items'), {name: 'AbortError'});
});

test('caller cancellation discards late results without closing the connection', async () => {
  const controller = new AbortController();
  const api = createApiClient('secret', async () => new Response('{"ok":true}', {headers: {'content-type': 'application/json'}}));
  controller.abort();
  await assert.rejects(api('/api/items', undefined, undefined, {signal: controller.signal}), {name: 'AbortError'});
  assert.deepEqual(await api('/api/items'), {ok: true});
});

test('policy round trip preserves ABAC conditions and identifiers exactly', () => {
  const policies = [{policy_id: 'p-1', role: 'analyst', permission: 'graph:read',
    conditions: [{attribute: 'classification', op: 'in', value: ['internal', 'public']}], description: 'Quoted "value"'}];
  assert.deepEqual(JSON.parse(policyDocument(policies)), {policies});
});

test('navigation does not misroute unknown prefixes to privileged screens', () => {
  assert.equal(destinationFor('/administrator'), null);
  assert.equal(destinationFor('/admin/security')?.id, 'admin');
  assert.equal(destinationFor('/not-a-screen'), null);
  assert.equal(destinationFor('/')?.id, 'app');
});
