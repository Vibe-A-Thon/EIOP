import { chromium } from '../apps/web/node_modules/playwright/index.mjs';
import { resolve } from 'node:path';

const root = resolve(import.meta.dirname, '..');
const asset = resolve(root, 'self-help-manual/site/assets');
const browser = await chromium.launch({ headless: true });
const page = await browser.newPage({ viewport: { width: 1440, height: 900 }, deviceScaleFactor: 1 });
const errors = [];
page.on('pageerror', error => errors.push(error.message));
await page.goto('http://127.0.0.1:5183/', { waitUntil: 'networkidle' });
await page.getByLabel('Access token').fill('local-help-capture-token-2026-long');
await page.getByRole('button', { name: /Connect/ }).click();
await page.getByText('Knowledge explorer', { exact: true }).first().waitFor({ timeout: 20000 });
const shots = [
  ['Knowledge explorer', 'explorer-screen.png'],
  ['Ontology studio', 'studio-screen.png'],
  ['Cognitive Dashboards', 'dashboards-screen.png'],
  ['Administration', 'administration-screen.png'],
];
for (const [label, file] of shots) {
  await page.getByText(label, { exact: true }).first().click();
  await page.locator('.route-loading').waitFor({ state: 'hidden', timeout: 20000 });
  await page.waitForTimeout(700);
  await page.screenshot({ path: resolve(asset, file), fullPage: false });
}
await page.getByText('Sources & jobs', { exact: true }).first().click();
await page.waitForTimeout(700);
await page.screenshot({ path: resolve(asset, 'sources-screen.png'), fullPage: false });
console.log(JSON.stringify({ screenshots: [...shots.map(x => x[1]), 'sources-screen.png'], errors }));
await browser.close();
if (errors.length) process.exitCode = 1;
