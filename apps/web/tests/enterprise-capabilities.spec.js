import {test, expect} from '@playwright/test';
import {createRequire} from 'node:module';
import {readFileSync} from 'node:fs';
import {randomUUID} from 'node:crypto';

const require = createRequire(import.meta.url);
const {enterpriseJourneys} = require('../../../demo/autodemo/enterprise-journeys.js');

test('extended enterprise journeys execute against the authenticated persisted application', async ({request}) => {
  test.skip(process.env.EOIP_RUNTIME_HUBBLE !== '1', 'Opt-in live local application test');
  test.setTimeout(240000);
  const entries = readFileSync(new URL('../../../deploy/.env', import.meta.url), 'utf8')
    .split(/\r?\n/).filter(line => line.startsWith('EOIP_API_TOKEN='));
  const token = process.env.EOIP_API_TOKEN || (entries.length === 1 && entries[0].split('=').slice(1).join('='));
  expect(token, 'A configured local token is required').toBeTruthy();
  const baseURL = process.env.EOIP_RUNTIME_API_URL || 'http://localhost:8000';
  const anonymous = await request.post(`${baseURL}/api/v1/catalog/products`,
    {data: {name: 'Must not be created', owner: 'anonymous'}});
  expect(anonymous.status()).toBe(401);
  const api = async (route, body, verify, options = {}) => {
    const response = await request.fetch(`${baseURL}${route}`, {
      method: options.method || (body === undefined ? 'GET' : 'POST'),
      headers: {Authorization: `Bearer ${token}`},
      ...(body === undefined ? {} : {data: body}),
      timeout: 120000,
    });
    expect(response.ok(), `${route} returned HTTP ${response.status()}`).toBeTruthy();
    const value = await response.json();
    expect(value.error, `${route} reported an application error`).toBeFalsy();
    expect(value.error_count || 0).toBe(0);
    return value;
  };
  const receipts = [];
  const catalog = await api('/api/v1/demo/scenarios');
  const anchor = catalog.scenarios.find(item => item.id === 'intent-to-runtime' && item.ready)?.entrypoint;
  expect(anchor, 'A ready enterprise work anchor is required').toBeTruthy();
  for (const [name, action] of enterpriseJourneys(api, anchor, randomUUID())) {
    await test.step(name, async () => receipts.push({name, result: await action()}));
  }
  const product = receipts.find(item => item.result.product)?.result.product;
  expect(product).toBeTruthy();
  const entity = await api(`/api/v1/entities/${product.product_id}`);
  expect(JSON.stringify(entity)).toContain(product.name);
  await test.info().attach('enterprise-journeys', {
    body: JSON.stringify(receipts, null, 2), contentType: 'application/json',
  });
});
