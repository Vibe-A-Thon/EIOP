import {defineConfig} from '@playwright/test';

const executablePath = process.env.PLAYWRIGHT_EXECUTABLE_PATH || undefined;

export default defineConfig({
  testDir: './tests',
  testIgnore: ['**/unit/**'],
  timeout: 60000,
  expect: {timeout: 15000},
  workers: 1,
  retries: 0,
  reporter: [['list']],
  use: {
    baseURL: process.env.PLAYWRIGHT_BASE_URL || 'http://eoip-web:8080',
    channel: executablePath ? undefined : process.env.PLAYWRIGHT_CHANNEL || undefined,
    headless: true,
    launchOptions: executablePath ? {executablePath} : undefined,
    viewport: {width: 1440, height: 1000},
    screenshot: 'only-on-failure',
  },
});
