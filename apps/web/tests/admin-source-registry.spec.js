import {test, expect} from '@playwright/test';

test('admin source registry supports onboarding, discovery, and source operations', async ({page}) => {
  const errors = [];
  page.on('pageerror', error => errors.push(error.message));

  let sourceEnabled = true;
  const source = () => ({
    source_id: 'jira-prod',
    source_type: 'jira',
    name: 'Jira Prod',
    enabled: sourceEnabled,
    health: 'HEALTHY',
    acquisition_modes: ['baseline', 'poll', 'replay'],
    checkpoint: '2026-10-05T10:00:00Z',
    capabilities: {
      baseline: true,
      polling: true,
      webhooks: true,
      discovery: true,
      reconciliation: false,
      replay: true,
    },
  });

  await page.route('**/health/ready', route => route.fulfill({
    status: 200,
    contentType: 'application/json',
    body: '{"status":"ready"}',
  }));

  await page.route('**/api/**', async route => {
    const url = new URL(route.request().url());
    const path = url.pathname;
    const method = route.request().method();
    let status = 200;
    let body = {};

    if (path === '/api/v1/admin/stats') {
      body = {vertices: 0, edges: 0, labels: {}, worker: {status: 'ready'}};
    } else if (path === '/api/v1/admin/system') {
      body = {graph: {status: 'ready'}, model: {status: 'deterministic'}, backup: {status: 'not_created'}};
    } else if (path === '/api/v1/admin/jobs') {
      body = [];
    } else if (path === '/api/v1/connectors/catalog') {
      body = {connectors: [
        {id: 'jira', name: 'Jira', type: 'api', capabilities: ['baseline', 'poll', 'webhook', 'replay']},
        {id: 'web', name: 'Web Crawler', type: 'crawler', capabilities: ['baseline', 'poll', 'reconcile']},
      ]};
    } else if (path === '/api/v1/sources' && method === 'GET') {
      body = [source()];
    } else if (path === '/api/v1/sources' && method === 'POST') {
      status = 201;
      body = {...source(), source_id: 'web-prod', source_type: 'web', name: 'Web Prod'};
    } else if (path === '/api/v1/sources/jira-prod/discover') {
      body = {source_id: 'jira-prod', status: 'COMPLETE', items: [{key: 'EOIP-1', type: 'issue'}]};
    } else if (path === '/api/v1/sources/jira-prod/dry-run') {
      status = 202;
      body = {job_id: 'dry-run-1', status: 'PENDING'};
    } else if (path === '/api/v1/sources/jira-prod' && method === 'PATCH') {
      sourceEnabled = false;
      body = source();
    }

    await route.fulfill({status, contentType: 'application/json', body: JSON.stringify(body)});
  });

  await page.goto('/admin');
  await page.getByLabel('Access token').fill('source-registry-browser-fixture');
  await page.getByRole('button', {name: 'Connect', exact: true}).click();
  await page.getByRole('tab', {name: 'Sources & jobs'}).click();
  await page.getByRole('button', {name: 'Load source control'}).click();

  await expect(page.getByRole('heading', {name: 'Registered sources'})).toBeVisible();
  await expect(page.getByText('Jira Prod')).toBeVisible();
  await expect(page.getByText('baseline, poll, replay')).toBeVisible();

  await page.getByRole('button', {name: 'Discover'}).click();
  await expect(page.getByRole('heading', {name: 'jira-prod'})).toBeVisible();
  await expect(page.getByText('EOIP-1')).toBeVisible();

  await page.getByRole('button', {name: 'Dry run'}).click();
  await page.getByRole('button', {name: 'Disable'}).click();
  await expect(page.getByText('DISABLED')).toBeVisible();

  await page.getByText('Web Crawler').click();
  await page.getByLabel('Source ID').fill('web-prod');
  await page.getByLabel('Name').fill('Web Prod');
  await page.getByLabel('Base URL').fill('https://docs.example.local');
  await page.getByRole('button', {name: 'Create source'}).click();

  expect(errors).toEqual([]);
});
