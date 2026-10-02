import {test, expect} from '@playwright/test';

test('login, search, trace graph evidence, and administer persisted data', async ({page}) => {
  const errors = [];
  page.on('pageerror', error => errors.push(error.message));
  await page.goto('/app');
  await page.getByLabel('Access token').fill(process.env.EOIP_API_TOKEN);
  await page.getByRole('button', {name: 'Connect', exact: true}).click();
  await expect(page.getByRole('heading', {name: 'Relationship map'})).toBeVisible();
  await page.getByRole('textbox', {name: 'Search knowledge graph'}).fill('compute_impact');
  await page.getByRole('button', {name: 'Search graph'}).click();
  await page.locator('.entity-list button').first().click();
  await expect(page.getByRole('button', {name: 'Explore impact'})).toBeVisible();
  await page.getByRole('button', {name: 'Find path'}).click();
  const graph = page.getByRole('img', {name: /Knowledge graph/});
  await expect(graph).toBeVisible();
  await expect(graph).toHaveAttribute('aria-label', /IMPLEMENTS/);
  await expect(graph).toHaveAttribute('aria-label', /DECLARES/);
  await page.getByRole('button', {name: 'Run TraceImpact'}).click();
  await expect(page.getByRole('heading', {name: 'TraceImpact result'})).toBeVisible();
  await expect(page.getByText('connected entities within', {exact: false})).toBeVisible();
  await page.screenshot({path: 'test-results/explorer.png', fullPage: true});
  await page.getByRole('button', {name: 'Administration'}).click();
  await expect(page.getByRole('heading', {name: 'Ingestion jobs'})).toBeVisible();
  await page.getByRole('button', {name: 'Run validation'}).click();
  await expect(page.getByText('No findings in the checked graph.', {exact: false})).toBeVisible();
  await page.screenshot({path: 'test-results/admin.png', fullPage: true});
  expect(errors).toEqual([]);
});

test('invalid credentials show an error without granting access', async ({page}) => {
  await page.goto('/app');
  await page.getByLabel('Access token').fill('invalid');
  await page.getByRole('button', {name: 'Connect', exact: true}).click();
  await expect(page.getByRole('alert')).toContainText('valid Bearer token');
  await expect(page.getByRole('heading', {name: 'Relationship map'})).toHaveCount(0);
});
