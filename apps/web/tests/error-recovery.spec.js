import {test, expect} from '@playwright/test';

test('unavailable API denies entry and reconnects after recovery', async ({page}) => {
  const errors = [];
  page.on('pageerror', error => errors.push(error.message));
  const unavailable = route => route.fulfill({
    status: 503,
    contentType: 'application/json',
    headers: {'X-Correlation-ID': 'browser-api-unavailable'},
    body: JSON.stringify({detail: 'Graph service temporarily unavailable'}),
  });
  await page.route('**/api/**', unavailable);
  await page.goto('/app');
  await page.getByLabel('Access token').fill(process.env.EOIP_API_TOKEN);
  await page.getByRole('button', {name: 'Connect', exact: true}).click();
  await expect(page.getByRole('alert')).toContainText('Graph service temporarily unavailable');
  await expect(page.getByRole('alert')).toContainText('browser-api-unavailable');
  await expect(page.getByRole('heading', {name: 'Relationship map'})).toHaveCount(0);
  await expect(page.getByRole('button', {name: 'Connect', exact: true})).toBeEnabled();
  await page.unroute('**/api/**', unavailable);
  await page.getByRole('button', {name: 'Connect', exact: true}).click();
  await expect(page.getByRole('heading', {name: 'Relationship map'})).toBeVisible();
  await expect(page.getByRole('alert')).toHaveCount(0);
  expect(errors).toEqual([]);
});

test('network interruption is visible and login can be retried', async ({page}) => {
  const disconnect = route => route.abort('failed');
  await page.route('**/api/**', disconnect);
  await page.goto('/app');
  await page.getByLabel('Access token').fill(process.env.EOIP_API_TOKEN);
  await page.getByRole('button', {name: 'Connect', exact: true}).click();
  await expect(page.getByRole('alert')).toContainText('Check that the local API and graph services are available.');
  await expect(page.getByRole('heading', {name: 'Relationship map'})).toHaveCount(0);
  await page.unroute('**/api/**', disconnect);
  await page.getByRole('button', {name: 'Connect', exact: true}).click();
  await expect(page.getByRole('heading', {name: 'Relationship map'})).toBeVisible();
  await expect(page.getByRole('alert')).toHaveCount(0);
});
