import {test, expect} from '@playwright/test';

async function proxyApiRequests(page) {
  if (!process.env.PLAYWRIGHT_API_PROXY) return;
  const target = new URL(process.env.PLAYWRIGHT_API_PROXY);
  await page.route('**/api/**', route => {
    const url = new URL(route.request().url());
    url.protocol = target.protocol;
    url.host = target.host;
    return route.fetch({url: url.toString()});
  });
}

test('login, search, trace graph evidence, and administer persisted data', async ({page}) => {
  const errors = [];
  page.on('pageerror', error => errors.push(error.message));
  await proxyApiRequests(page);
  await page.goto('/app');
  await page.getByLabel('Access token').fill(process.env.EOIP_API_TOKEN);
  await page.getByRole('button', {name: 'Connect', exact: true}).click();
  await expect(page.getByRole('heading', {name: 'Relationship map'})).toBeVisible();
  await page.getByRole('textbox', {name: 'Search knowledge graph'}).fill('compute_impact');
  await page.getByRole('button', {name: 'Search graph'}).click();
  await page.locator('.entity-list button').first().click();
  await expect(page.getByRole('button', {name: 'Explore impact'})).toBeVisible();
  await page.getByRole('tab', {name: 'Impact'}).click();
  await page.getByLabel('From canonical ID').fill('urn:eoip:work:item:jira:EOIP-1');
  await page.getByRole('button', {name: 'Find path'}).click();
  const graph = page.getByRole('img', {name: /Knowledge graph/});
  await expect(graph).toBeVisible();
  await expect(graph).toHaveAttribute('aria-label', /IMPLEMENTS/);
  await expect(graph).toHaveAttribute('aria-label', /DECLARES/);
  await page.getByRole('button', {name: 'Run TraceImpact'}).click();
  await expect(page.getByRole('heading', {name: 'TraceImpact result'})).toBeVisible({timeout: 15000});
  await expect(page.getByText('connected entities within', {exact: false})).toBeVisible({timeout: 15000});
  await page.screenshot({path: 'test-results/explorer.png', fullPage: true});
  await page.getByRole('button', {name: 'Administration'}).click();
  await expect(page.getByRole('heading', {name: 'Ingestion jobs'})).toBeVisible();
  await page.getByRole('button', {name: 'Run validation'}).click();
  await expect(page.getByText(/Checked \d+ entities and \d+ relationships/)).toBeVisible();
  await page.getByRole('tab', {name: 'Quality & ontology'}).click();
  await page.getByRole('button', {name: 'Load ontology schema'}).click();
  await expect(page.getByRole('heading', {name: /Vertex labels/})).toBeVisible();
  await expect(page.getByRole('heading', {name: /Edge labels/})).toBeVisible();
  await expect(page.getByRole('heading', {name: /Index coverage/})).toBeVisible();
  await page.screenshot({path: 'test-results/admin.png', fullPage: true});
  await page.route('**/api/v1/admin/dlq?limit=25', route => route.fulfill({
    status: 200,
    contentType: 'application/json',
    body: JSON.stringify([{
      event_id: 'a'.repeat(64),
      source_system: 'jira',
      source_record_id: 'missing-key-record',
      payload_hash: 'b'.repeat(64),
      error_category: 'mapping_error',
      error: 'Issue key is required',
    }]),
  }));
  await page.getByRole('tab', {name: 'Audit & recovery'}).click();
  await page.getByRole('button', {name: 'Load DLQ'}).click();
  await expect(page.getByText('Issue key is required')).toBeVisible();
  await expect(page.getByText('missing-key-record')).toBeVisible();
  await expect(page.getByRole('button', {name: 'Replay'})).toBeVisible();
  await expect(page.getByText('b'.repeat(64))).toHaveCount(0);
  expect(errors).toEqual([]);
});

test('invalid credentials show an error without granting access', async ({page}) => {
  await proxyApiRequests(page);
  await page.goto('/app');
  await page.getByLabel('Access token').fill('invalid');
  await page.getByRole('button', {name: 'Connect', exact: true}).click();
  await expect(page.getByRole('alert')).toContainText('valid Bearer token');
  await expect(page.getByRole('heading', {name: 'Relationship map'})).toHaveCount(0);
});
