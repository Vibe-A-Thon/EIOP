const {test} = require('node:test');
const assert = require('node:assert/strict');
const {requireGraph, requireAgent, requirePath, operationCoverage} = require('../browser-demo');

test('a successful HTTP response with empty graph cannot pass the demo', () => {
  for (const value of [{}, {nodes: []}, {nodes: 'fake'}]) assert.throws(() => requireGraph(value));
  requireGraph({nodes: [{id: 'source'}]});
});

test('scenario paths must connect the declared source and target', () => {
  const scenario = {id: 'example', expected_path: ['source', 'target']};
  requirePath({nodes: [{id: 'source'}], paths: [['source', 'middle', 'target']]}, scenario);
  requirePath({nodes: [{id: 'source'}], paths: [{node_ids: ['source', 'middle', 'target']}]}, scenario);
  assert.throws(() => requirePath({nodes: [{id: 'source'}], paths: [['target', 'source']]}, scenario));
  assert.throws(() => requirePath({nodes: [{id: 'source'}], paths: []}, scenario));
});

test('coverage cannot certify unexecuted APIs or destructive operations', () => {
  const coverage = operationCoverage({paths: {'/a': {get: {}, parameters: []}, '/b': {post: {}, delete: {}}}},
    new Set(['GET /a']));
  assert.equal(coverage.length, 3);
  assert.equal(coverage[0].status, 'DEMONSTRATED');
  assert.ok(coverage.slice(1).every(item => item.status === 'NOT_DEMONSTRATED' && item.reason));
});

test('coverage matches parameterized routes by method and segment, not loose prefixes', () => {
  const schema = {paths: {
    '/products/{product_id}/transition': {post: {}, delete: {}},
    '/products/{product_id}': {get: {}},
    '/products/all/extra': {get: {}},
  }};
  const coverage = operationCoverage(schema, new Set([
    'POST /products/urn:demo:one/transition', 'GET /products/urn:demo:one?verbose=1',
    'GET /products/all/extra/more',
  ]));
  assert.deepEqual(coverage.map(item => item.status),
    ['DEMONSTRATED', 'NOT_DEMONSTRATED', 'DEMONSTRATED', 'NOT_DEMONSTRATED']);
});

test('agent aliases show their actual execution without accepting invalid results', () => {
  const types = [{name: 'simple_reflex', category: 'reactive'}];
  const result = {agent_type: 'simple_reflex', category: 'reactive', answer: 'Live graph analysis',
    confidence: 0.4, actions: [], reasoning: []};
  requireAgent(result, types);
  for (const overrides of [
    {agent_type: 'unknown'}, {category: 'unknown'}, {answer: ''},
    {confidence: 2}, {confidence: null}, {actions: null}, {reasoning: null},
  ]) assert.throws(() => requireAgent({...result, ...overrides}, types));
});
