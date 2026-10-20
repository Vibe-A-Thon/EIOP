import { chromium } from '../apps/web/node_modules/playwright/index.mjs';
import { resolve } from 'node:path';
import { access } from 'node:fs/promises';
import { fileURLToPath } from 'node:url';

const root = resolve(import.meta.dirname, '..');
const browser = await chromium.launch({ headless: true });
const failures = [];
for (const viewport of [{ width: 1440, height: 900 }, { width: 390, height: 844 }]) {
  const page = await browser.newPage({ viewport, deviceScaleFactor: 1 });
  page.on('pageerror', error => failures.push(error.message));
  const target = `file://${resolve(root, 'self-help-manual/site/index.html').replaceAll('\\', '/')}`;
  await page.goto(target);
  await page.screenshot({ path: resolve(root, `.audit-scratch/help-${viewport.width}.png`), fullPage: true });
  if (!await page.getByRole('heading', { name: 'EOIP Help Center' }).isVisible()) failures.push('index heading missing');
  const overflow = await page.evaluate(() => document.documentElement.scrollWidth > window.innerWidth);
  if (overflow) failures.push(`horizontal overflow at ${viewport.width}`);
  const open = viewport.width < 700 ? page.getByRole('button', { name: 'Search', exact: true }) : page.getByRole('button', { name: 'Search all help pages' });
  await open.click();
  await page.getByRole('searchbox', { name: 'Search all help pages' }).fill('token');
  const count = await page.locator('#search-results a').count();
  if (count < 1) failures.push('search returned no token results');
  await page.locator('#search-results a').first().click();
  if (!page.url().includes('.html#section-')) failures.push('search result navigation failed');
  await page.close();
}
const test = await browser.newPage();
for (const slug of ['index','connect','manuals','explore','studio','data-admin','reports','security','troubleshoot']) {
  await test.goto(`file://${resolve(root, `self-help-manual/site/${slug}.html`).replaceAll('\\', '/')}`);
  if (!await test.locator('h1').count()) failures.push(`${slug} missing h1`);
  const images = await test.locator('main img').evaluateAll(nodes => nodes.map(node => ({ src: node.src, loaded: node.complete && node.naturalWidth > 0 })));
  if (images.some(x => !x.loaded)) failures.push(`${slug} image failed`);
}
await test.goto(`file://${resolve(root, 'self-help-manual/site/manuals.html').replaceAll('\\', '/')}`);
const downloads = await test.locator('a[download]').evaluateAll(nodes => nodes.map(node => node.href));
if (downloads.length !== 10) failures.push(`Expected 10 manual downloads, got ${downloads.length}`);
for (const href of downloads) {
  try { await access(fileURLToPath(href)); } catch { failures.push(`Broken download: ${href}`); }
}
console.log(JSON.stringify({ pages: 9, viewports: 2, failures }));
await browser.close();
if (failures.length) process.exitCode = 1;
