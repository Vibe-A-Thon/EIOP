import {test, expect} from '@playwright/test';
import AxeBuilder from '@axe-core/playwright';

async function check(page, testInfo, name) {
  const result = await new AxeBuilder({page}).withTags(['wcag2a', 'wcag2aa', 'wcag21a', 'wcag21aa', 'wcag22aa']).analyze();
  await testInfo.attach(name, {body: JSON.stringify(result.violations, null, 2), contentType: 'application/json'});
  expect(result.violations.filter(violation => ['serious', 'critical'].includes(violation.impact)),
    JSON.stringify(result.violations.map(violation => ({id: violation.id, impact: violation.impact, nodes: violation.nodes.map(node => node.target)})))).toEqual([]);
}

test('connection controls meet automated WCAG checks', async ({page}, testInfo) => {
  await page.goto('/');
  await expect(page.getByLabel('Access token', {exact: true})).toBeVisible();
  await check(page, testInfo, 'connection-axe');
});

test('appearance and keyboard dialog meet automated checks across four themes', async ({page}, testInfo) => {
  await page.route('**/api/v1/admin/**', route => route.fulfill({json:
    route.request().url().endsWith('/jobs') ? [] : {vertices: 0, edges: 0, labels: {}},
  }));
  await page.goto('/settings');
  await page.getByLabel('Access token', {exact: true}).fill('axe-component-fixture');
  await page.getByRole('button', {name: 'Connect', exact: true}).click();
  for (const name of ['Light', 'Dark', 'High contrast light', 'High contrast dark']) {
    await page.getByRole('radio', {name, exact: true}).check();
    await check(page, testInfo, `${name}-axe`);
  }
  await page.getByRole('button', {name: 'Open command palette'}).click();
  await expect(page.getByRole('dialog')).toBeVisible();
  await check(page, testInfo, 'command-dialog-axe');
});
