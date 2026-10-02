import {defineConfig} from '@playwright/test';
export default defineConfig({
  testDir: './tests',
  timeout: 60000,
  workers: 1,
  retries: 0,
  reporter: [['list']],
  use: {baseURL: 'http://eoip-web:8080', headless: true, viewport: {width: 1440, height: 1000}, screenshot: 'only-on-failure'},
});
