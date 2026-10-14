import {test, expect} from '@playwright/test';
import {generateInteractiveHTML} from '../src/kgr/export/InteractiveExport.js';

test('export renders hostile titles and script-like graph data as inert text', async ({page}) => {
  const title = '</title><img src=x onerror="window.injected=true">';
  const payload = '</script><script>window.injected=true</script>';
  const node = {id: '__proto__', label: 'WorkItem', properties: {name: payload}};
  const errors = [];
  page.on('pageerror', error => errors.push(error.message));
  await page.setContent(generateInteractiveHTML([node], [], {title}));
  await expect(page).toHaveTitle(title);
  await expect(page.locator('#toolbar strong')).toHaveText(title);
  await expect(page.locator('img')).toHaveCount(0);
  await expect(page.locator('canvas')).toBeVisible();
  await expect(page.locator('#info')).toContainText('1 nodes');
  expect(await page.evaluate(() => window.injected)).toBeUndefined();
  expect(errors).toEqual([]);
});

test('inspector properties cannot inject markup and normal interaction still works', async ({page}) => {
  const hostileKey = '<img src=x onerror="window.injected=true">';
  const hostileValue = '<svg onload="window.injected=true">';
  await page.setContent(generateInteractiveHTML([
    {id: 'node-1', label: 'WorkItem', properties: {name: 'Real item', [hostileKey]: hostileValue}},
  ], []));
  await page.locator('canvas').click({position: {x: 700, y: 300}});
  await expect(page.locator('#ins-title')).toHaveText('Real item');
  await expect(page.locator('#ins-props')).toContainText(hostileKey);
  await expect(page.locator('#ins-props')).toContainText(hostileValue);
  await expect(page.locator('#ins-props img, #ins-props svg')).toHaveCount(0);
  expect(await page.evaluate(() => window.injected)).toBeUndefined();
  await page.locator('#search').fill('Real item');
  await expect(page.locator('#info')).toContainText('zoom 1.0x');
});
