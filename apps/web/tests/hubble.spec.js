import {test, expect} from '@playwright/test';
import {readFileSync} from 'node:fs';
import {runInNewContext} from 'node:vm';

test('Hubble language bootstrap defaults to English and preserves preferences', () => {
  const script = readFileSync(new URL('../../../deploy/hubble/default-language.js', import.meta.url), 'utf8');
  for (const initial of [null, 'en-US', 'zh-CN']) {
    const values = new Map(initial === null ? [] : [['languageType', initial]]);
    const localStorage = {
      getItem: key => values.has(key) ? values.get(key) : null,
      setItem: (key, value) => values.set(key, value)
    };
    runInNewContext(script, {localStorage});
    runInNewContext(script, {localStorage});
    expect(values.get('languageType')).toBe(initial === null ? 'en-US' : initial);
  }
});

test('Hubble opens the existing graph, executes Gremlin and displays metadata', async ({page}) => {
  test.skip(process.env.EOIP_RUNTIME_HUBBLE !== '1', 'Opt-in local Hubble administration test');
  await page.goto(process.env.EOIP_RUNTIME_HUBBLE_URL || 'http://localhost:8088');
  await expect(page.getByText('English', {exact: true})).toBeVisible();
  await expect(page.getByText('EOIP', {exact: true})).toBeVisible();
  await page.getByRole('button', {name: 'Visit', exact: true}).click();
  await expect(page).toHaveURL(/\/graph-management\/\d+\/data-analyze/);
  const editor = page.locator('.CodeMirror');
  await editor.click();
  await page.keyboard.type('g.V().limit(5)');
  const queryResponse = page.waitForResponse(response =>
    response.url().includes('/gremlin-query') && response.request().method() === 'POST'
  );
  await page.getByRole('button', {name: 'Execute Query', exact: true}).click();
  const result = await (await queryResponse).json();
  expect(result.status).toBe(200);
  expect(result.data.graph_view.vertices.length).toBeGreaterThan(0);
  await page.getByText('Json', {exact: true}).click();
  await expect(page.locator('body')).toContainText('canonical_id');
  await page.getByText('Metadata Configuration', {exact: true}).click();
  await page.getByText('Vertex Type', {exact: true}).click();
  await expect(page.locator('body')).toContainText('WorkItem');
});

test('Hubble preserves an explicit language choice', async ({page}) => {
  test.skip(process.env.EOIP_RUNTIME_HUBBLE !== '1', 'Opt-in local Hubble administration test');
  await page.addInitScript(() => localStorage.setItem('languageType', 'zh-CN'));
  await page.goto(process.env.EOIP_RUNTIME_HUBBLE_URL || 'http://localhost:8088');
  await expect(page.getByText('English', {exact: true})).not.toBeVisible();
  expect(await page.evaluate(() => localStorage.getItem('languageType'))).toBe('zh-CN');
});
