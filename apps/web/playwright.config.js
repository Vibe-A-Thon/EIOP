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
  webServer: process.env.EOIP_GUI_WEB_SERVER === '1' ? {
    command: 'npm run dev -- --host 127.0.0.1 --port 5173 --strictPort',
    url: 'http://127.0.0.1:5173',
    reuseExistingServer: !process.env.CI,
    timeout: 60000,
  } : undefined,
  use: {
    baseURL: process.env.PLAYWRIGHT_BASE_URL || 'http://eoip-web:8080',
    channel: executablePath ? undefined : process.env.PLAYWRIGHT_CHANNEL || undefined,
    headless: true,
    launchOptions: executablePath ? {executablePath} : undefined,
    viewport: {width: 1440, height: 1000},
    screenshot: 'only-on-failure',
  },
});
