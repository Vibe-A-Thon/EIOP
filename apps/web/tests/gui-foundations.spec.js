import {test, expect} from '@playwright/test';

const token = 'gui-component-fixture-credential';

async function fixture(page) {
  await page.route('**/health/ready', route => route.fulfill({json: {status: 'ready'}}));
  await page.route('**/api/v1/**', route => {
    const path = new URL(route.request().url()).pathname;
    const data = path.endsWith('/stats') ? {vertices: 0, edges: 0, labels: {}, backend: 'fixture'}
      : path.endsWith('/jobs') ? [] : path.endsWith('/system') ? {} : null;
    return data === null ? route.fulfill({status: 503, json: {detail: 'Fixture service unavailable'}}) : route.fulfill({json: data});
  });
}

async function connect(page, path = '/settings') {
  await page.goto(path);
  await page.getByLabel('Access token', {exact: true}).fill(token);
  await page.getByRole('button', {name: 'Connect', exact: true}).click();
  await expect(page.getByRole('button', {name: 'Disconnect this browser session'})).toBeVisible();
}

test('credential lifetime, palette keyboard, navigation history and focus', async ({page}) => {
  await fixture(page);
  await connect(page);
  expect(await page.evaluate(() => sessionStorage.getItem('eoip-token'))).toBeNull();
  await page.getByRole('button', {name: 'Open command palette'}).click();
  await expect(page.getByRole('dialog')).toBeVisible();
  await page.getByLabel('Find a screen').fill('Administration');
  await page.getByRole('button', {name: 'Administration', exact: true}).click();
  await expect(page).toHaveURL(/\/admin$/);
  await expect(page.locator('.atlas-heading h1')).toBeFocused();
  await page.goBack();
  await expect(page).toHaveURL(/\/settings$/);
  await expect(page.getByRole('heading', {name: 'Appearance', exact: true}).last()).toBeVisible();
  await page.keyboard.press('Control+k');
  await expect(page.getByRole('dialog')).toBeVisible();
  await page.keyboard.press('Escape');
  await expect(page.getByRole('dialog')).not.toBeVisible();
  await page.getByRole('button', {name: 'Disconnect this browser session'}).click();
  await expect(page.getByLabel('Access token', {exact: true})).toHaveValue('');
  await page.reload();
  await expect(page.getByRole('heading', {name: 'Connect to EOIP'})).toBeVisible();
});

for (const viewport of [{width: 1440, height: 900}, {width: 390, height: 844}, {width: 320, height: 568}]) {
  test(`four appearance themes fit ${viewport.width}px and honor reduced motion`, async ({page}, testInfo) => {
    await page.setViewportSize(viewport);
    await fixture(page);
    await connect(page);
    for (const theme of ['Light', 'Dark', 'High contrast light', 'High contrast dark']) {
      await page.getByRole('radio', {name: theme, exact: true}).check();
      const dimensions = await page.evaluate(() => ({width: document.documentElement.clientWidth, scroll: document.documentElement.scrollWidth}));
      expect(dimensions.scroll).toBeLessThanOrEqual(dimensions.width);
      await page.screenshot({path: testInfo.outputPath(`${theme.toLowerCase().replaceAll(' ', '-')}.png`), fullPage: true});
    }
    await page.getByRole('checkbox', {name: 'Reduce motion'}).check();
    await expect(page.locator('html')).toHaveAttribute('data-motion', 'reduce');
    expect(await page.locator('.atlas-content > :first-child').evaluate(element => getComputedStyle(element).animationName)).toBe('none');
  });
}

test('system reduced motion disables route animation', async ({page}) => {
  await page.emulateMedia({reducedMotion: 'reduce'});
  await fixture(page);
  await connect(page);
  expect(await page.locator('.atlas-content > :first-child').evaluate(element => getComputedStyle(element).animationName)).toBe('none');
});

test('unknown routes have recoverable state and do not open administration', async ({page}) => {
  await fixture(page);
  await connect(page, '/administrator');
  await expect(page.getByRole('heading', {name: 'Page not found'}).last()).toBeVisible();
  await expect(page.getByRole('heading', {name: 'Ingestion jobs'})).toHaveCount(0);
});

test('security and administration never replace failed requests with sample results', async ({page}) => {
  await fixture(page);
  await connect(page, '/admin');
  await page.getByRole('tab', {name: 'Users & policy'}).click();
  await page.getByRole('tab', {name: 'Token Governance & CRL'}).click();
  await expect(page.getByRole('alert').last()).toContainText('Fixture service unavailable');
  await expect(page.getByText('FAIL_CLOSED', {exact: true})).toHaveCount(0);
  await expect(page.getByRole('button', {name: 'Issue scoped token', exact: true})).toBeDisabled();
  for (const label of ['Ingestion & Reconciliation', 'Checkpoints & DLQ', 'Drift & Freshness', 'Timeline & Journal', 'Quality, SLOs & Debt']) {
    await page.getByRole('tab', {name: label, exact: true}).click();
    await expect(page.locator('.admin-content-area').getByRole('alert')).toContainText('Fixture service unavailable');
    await expect(page.getByText('run-801', {exact: true})).toHaveCount(0);
    await expect(page.getByText('18402', {exact: true})).toHaveCount(0);
    await expect(page.getByText('err-evt-991', {exact: true})).toHaveCount(0);
  }
});

test('refresh and issue do not invent key rotation or a successful revocation', async ({page}) => {
  await fixture(page);
  await page.route('**/api/v1/security/status', route => route.fulfill({json: {
    enforcement_mode: 'OBSERVE_ONLY', algorithm: 'test', key_rotation_supported: false, active_revocations_count: 0,
  }}));
  await page.route('**/api/v1/security/policy-matrix', route => route.fulfill({json: {roles_hierarchy: {viewer: {rank: 1}}}}));
  await connect(page, '/admin');
  await page.getByRole('tab', {name: 'Users & policy'}).click();
  await page.getByRole('tab', {name: 'Token Governance & CRL'}).click();
  await expect(page.getByText('Not supported', {exact: true})).toBeVisible();
  await page.getByLabel('Token identifier', {exact: true}).fill('test-id');
  await page.getByLabel('Reason', {exact: true}).fill('test revocation');
  await page.getByLabel('Confirm revocation').check();
  await page.getByRole('button', {name: 'Revoke', exact: true}).click();
  await expect(page.getByRole('alert').last()).toContainText('Fixture service unavailable');
  await expect(page.getByText('Revocation recorded.', {exact: false})).toHaveCount(0);
});
