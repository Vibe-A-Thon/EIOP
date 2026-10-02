import {defineConfig} from '@playwright/test';
export default defineConfig({
  testDir: './tests',
  timeout: 60000,
  expect: {timeout: 15000},
  workers: 1,
  retries: 0,
  reporter: [['list']],
  use: {baseURL: process.env.PLAYWRIGHT_BASE_URL || 'http://eoip-web:8080', channel: process.env.PLAYWRIGHT_CHANNEL || undefined, headless: true, viewport: {width: 1440, height: 1000}, screenshot: 'only-on-failure'},
});
