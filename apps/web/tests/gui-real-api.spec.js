import {test, expect} from '@playwright/test';

const token = process.env.EOIP_GUI_TEST_TOKEN;
test.skip(!token, 'Requires an isolated real API configured by the GUI verification launcher.');

test('real security issuance, verification, revocation and policy replacement', async ({page}, testInfo) => {
  const errors = [];
  page.on('pageerror', error => errors.push(error.message));
  const requests = [];
  page.on('response', response => {
    const url = new URL(response.url());
    if (url.pathname.startsWith('/api/v1/')) requests.push({path: url.pathname, status: response.status()});
  });
  await page.goto('/admin');
  await page.getByLabel('Access token', {exact: true}).fill(token);
  await page.getByRole('button', {name: 'Connect', exact: true}).click();
  await expect(page.getByRole('heading', {name: 'Ingestion jobs'})).toBeVisible();
  await page.getByRole('tab', {name: 'Users & policy'}).click();
  await page.getByRole('tab', {name: 'Token Governance & CRL'}).click();
  await expect(page.getByText('FAIL_CLOSED', {exact: true})).toBeVisible();
  await page.getByLabel('Subject', {exact: true}).fill(`gui-browser-${testInfo.workerIndex}`);
  await page.getByLabel('Tenant ID', {exact: true}).fill('gui-fixture');
  await page.getByRole('button', {name: 'Issue scoped token', exact: true}).click();
  await expect(page.getByRole('status').filter({hasText: 'Issued token:'})).toBeVisible();
  await page.getByRole('button', {name: 'Verify token', exact: true}).click();
  await expect(page.getByRole('status').filter({hasText: 'Valid token'})).toBeVisible();
  await page.getByLabel('Reason', {exact: true}).fill('Isolated GUI verification');
  await page.getByLabel('Confirm revocation').check();
  await page.getByRole('button', {name: 'Revoke', exact: true}).click();
  await expect(page.getByRole('status').filter({hasText: 'Revocation recorded.'})).toBeVisible();
  await page.getByRole('button', {name: 'Verify token', exact: true}).click();
  await expect(page.locator('.security-workspace').getByRole('alert')).toBeVisible();
  await expect(page.getByRole('status').filter({hasText: 'Valid token'})).toHaveCount(0);
  await page.screenshot({path: testInfo.outputPath('security-real.png'), fullPage: true});
  await page.getByRole('tab', {name: 'Policies & RBAC'}).click();
  const editor = page.getByLabel(/POLICY YAML/);
  await expect(editor).not.toHaveValue('');
  const original = JSON.parse(await editor.inputValue());
  const changed = structuredClone(original);
  expect(changed.policies.length).toBeGreaterThan(0);
  changed.policies[0].description = 'GUI real API verification';
  try {
    await editor.fill(JSON.stringify(changed, null, 2));
    await page.getByRole('button', {name: 'Save & reload policies'}).click();
    await expect(page.getByRole('status').filter({hasText: 'Policy set reloaded'})).toBeVisible();
    const response = await page.request.get('/api/v1/authz/policies', {headers: {Authorization: `Bearer ${token}`}});
    expect(response.ok()).toBe(true);
    expect(await response.json()).toEqual(changed);
  } finally {
    const response = await page.request.post('/api/v1/authz/policies/reload?replace_existing=true', {
      headers: {Authorization: `Bearer ${token}`, 'Content-Type': 'application/yaml'}, data: JSON.stringify(original),
    });
    expect(response.ok()).toBe(true);
  }
  expect(requests.some(request => request.path === '/api/v1/security/tokens/revoke' && request.status === 200)).toBe(true);
  expect(errors).toEqual([]);
  await testInfo.attach('real-api-requests', {body: JSON.stringify(requests), contentType: 'application/json'});
});

test('real graph event polling sends bearer only in headers and cleans up on navigation', async ({page}) => {
  const seen = [];
  page.on('request', request => {
    if (new URL(request.url()).pathname === '/api/v1/graph/events') {
      seen.push({url: request.url(), authenticated: request.headers().authorization === `Bearer ${token}`});
    }
  });
  await page.goto('/app');
  await page.getByLabel('Access token', {exact: true}).fill(token);
  await page.getByRole('button', {name: 'Connect', exact: true}).click();
  await page.getByRole('tab', {name: 'KGR', exact: true}).click();
  await page.getByRole('button', {name: 'Show event feed', exact: true}).click();
  await expect(page.locator('.event-feed-title')).toContainText('polling');
  expect(seen.length).toBeGreaterThan(0);
  expect(seen.every(request => request.authenticated && !request.url.includes('token='))).toBe(true);
  await page.getByRole('link', {name: 'Appearance', exact: true}).click();
  const count = seen.length;
  await page.waitForTimeout(2500);
  expect(seen.length).toBe(count);
});
