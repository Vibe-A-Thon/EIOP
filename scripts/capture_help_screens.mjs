import { chromium } from '../apps/web/node_modules/playwright/index.mjs';
import { mkdir } from 'node:fs/promises';
import { resolve } from 'node:path';

const root = resolve(import.meta.dirname, '..');
const asset = resolve(root, 'self-help-manual/site/assets');
await mkdir(asset, { recursive: true });
const browser = await chromium.launch({ headless: true });
const errors = [];

const connection = await browser.newPage({ viewport: { width: 1440, height: 900 }, deviceScaleFactor: 1 });
connection.on('pageerror', error => errors.push(`connection: ${error.message}`));
await connection.goto('http://127.0.0.1:5182/', { waitUntil: 'networkidle' });
await connection.screenshot({ path: resolve(asset, 'connection-screen.png'), fullPage: true });
if (!await connection.getByRole('heading', { name: 'Connect to EOIP' }).isVisible()) throw new Error('Connection UI did not render');

const dashboard = await browser.newPage({ viewport: { width: 1440, height: 900 }, deviceScaleFactor: 1 });
dashboard.on('pageerror', error => errors.push(`dashboard: ${error.message}`));
await dashboard.goto(`file://${resolve(root, 'EOIP-master-dashboard.html').replaceAll('\\', '/')}`);
await dashboard.screenshot({ path: resolve(root, '.audit-scratch/dashboard-desktop.png'), fullPage: true });
await dashboard.getByRole('button', { name: /Requirements/ }).first().click();
await dashboard.getByRole('searchbox', { name: 'Search requirements' }).fill('PUR-');
const results = await dashboard.locator('tbody tr').count();
await dashboard.getByRole('button', { name: /Gaps & risks/ }).first().click();
const gapVisible = await dashboard.getByRole('heading', { name: 'Gaps and risks' }).isVisible();
const mobile = await browser.newPage({ viewport: { width: 390, height: 844 }, deviceScaleFactor: 1 });
mobile.on('pageerror', error => errors.push(`mobile dashboard: ${error.message}`));
await mobile.goto(`file://${resolve(root, 'EOIP-master-dashboard.html').replaceAll('\\', '/')}`);
await mobile.screenshot({ path: resolve(root, '.audit-scratch/dashboard-mobile.png'), fullPage: true });
const mobileOverflow = await mobile.evaluate(() => document.documentElement.scrollWidth > window.innerWidth);
console.log(JSON.stringify({ results, gapVisible, mobileOverflow, errors }));
await browser.close();
if (!results || !gapVisible || mobileOverflow || errors.length) process.exitCode = 1;
