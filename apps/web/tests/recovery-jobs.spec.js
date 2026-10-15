import {test, expect} from '@playwright/test';

test('held jobs require confirmation, show refusals, and support readmission and cancellation', async ({page}) => {
  const errors = [];
  page.on('pageerror', error => errors.push(error.message));
  const job = {
    job_id: 'ed748adf-4ba6-47e0-bf98-3d237603b78a',
    kind: 'JIRA_JSON', status: 'HELD', created_at: '2026-10-03T00:00:00Z',
  };
  let requests = 0;
  let refuse = true;
  await page.route('**/health/ready', route => route.fulfill({
    status: 200, contentType: 'application/json', body: '{"status":"ready"}',
  }));
  await page.route('**/api/v1/**', async route => {
    const path = new URL(route.request().url()).pathname;
    let status = 200;
    let body = {};
    if (path === '/api/v1/admin/jobs') body = [job];
    else if (path === '/api/v1/admin/stats') body = {vertices: 0, edges: 0, labels: {}};
    else if (path.endsWith('/readmit')) {
      requests += 1;
      if (refuse) {
        status = 409;
        body = {detail: 'source is paused'};
      } else {
        status = 202;
        job.status = 'PENDING';
        body = job;
      }
    } else if (path.endsWith('/cancel')) {
      job.status = 'CANCELLED';
      body = job;
    }
    await route.fulfill({status, contentType: 'application/json',
      headers: {'X-Correlation-ID': 'recovery-browser'}, body: JSON.stringify(body)});
  });
  await page.goto('/admin');
  await page.getByLabel('Access token').fill('recovery-browser-fixture');
  await page.getByRole('button', {name: 'Connect', exact: true}).click();
  await page.getByRole('tab', {name: 'Sources & jobs'}).click();
  await expect(page.getByText('Recovery hold:', {exact: false})).toBeVisible();
  const dismiss = dialog => dialog.dismiss();
  page.on('dialog', dismiss);
  await page.getByRole('button', {name: 'Readmit', exact: true}).click();
  expect(requests).toBe(0);
  page.off('dialog', dismiss);
  page.on('dialog', dialog => {
    expect(dialog.message()).toContain('repeat side effects');
    dialog.accept();
  });
  await page.getByRole('button', {name: 'Readmit', exact: true}).click();
  await expect(page.getByRole('alert')).toContainText('source is paused');
  await expect(page.getByRole('alert')).toContainText('recovery-browser');
  await expect(page.getByText('Recovery hold:', {exact: false})).toBeVisible();
  refuse = false;
  await page.getByRole('button', {name: 'Readmit', exact: true}).click();
  await expect(page.getByRole('button', {name: 'Readmit', exact: true})).toHaveCount(0);
  await expect(page.getByText('PENDING', {exact: true})).toBeVisible();
  await page.getByRole('button', {name: 'Cancel', exact: true}).click();
  await expect(page.getByText('CANCELLED', {exact: true})).toBeVisible();
  await expect(page.getByRole('button', {name: 'Cancel', exact: true})).toHaveCount(0);
  expect(requests).toBe(2);
  expect(errors).toEqual([]);
});
