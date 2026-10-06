import {test, expect} from '@playwright/test';
import {readFileSync} from 'node:fs';
import {runInNewContext} from 'node:vm';

test('Hubble language bootstrap defaults to English and preserves preferences', () => {
  const script = readFileSync(new URL('../../../deploy/hubble/default-language.js', import.meta.url), 'utf8');
  for (const initial of [null, 'en-US', 'zh-CN']) {
    const values = new Map(initial === null ? [] : [['languageType', initial]]);
    const localStorage = {
      getItem: key => values.has(key) ? values.get(key) : null,
      setItem: (key, value) => values.set(key, value)
    };
    const window = {addEventListener() {}};
    runInNewContext(script, {localStorage, window});
    runInNewContext(script, {localStorage, window});
    expect(values.get('languageType')).toBe(initial === null ? 'en-US' : initial);
  }
});

test('Hubble bundle exposes the Graph IDL studio launcher and static assets', () => {
  const bootstrap = readFileSync(new URL('../../../deploy/hubble/default-language.js', import.meta.url), 'utf8');
  const dockerfile = readFileSync(new URL('../../../deploy/hubble/Dockerfile', import.meta.url), 'utf8');
  const page = readFileSync(new URL('../../../deploy/hubble/graph-idl.html', import.meta.url), 'utf8');

  expect(bootstrap).toContain('/graph-idl.html');
  expect(bootstrap).toContain('Graph IDL');
  expect(dockerfile).toContain('graph-idl.html');
  expect(dockerfile).toContain('graph-idl.css');
  expect(dockerfile).toContain('graph-idl.js');
  expect(page).toContain('Graph Integrated Development Studio');
});

test('Graph IDL renders a live Hubble-style graph with mocked graph APIs', async ({page}) => {
  const files = new Map([
    ['/graph-idl.html', ['text/html', readFileSync(new URL('../../../deploy/hubble/graph-idl.html', import.meta.url), 'utf8')]],
    ['/graph-idl.css', ['text/css', readFileSync(new URL('../../../deploy/hubble/graph-idl.css', import.meta.url), 'utf8')]],
    ['/graph-idl.js', ['text/javascript', readFileSync(new URL('../../../deploy/hubble/graph-idl.js', import.meta.url), 'utf8')]],
  ]);
  const vertices = [
    {id: 'v1', label: 'WorkItem', properties: {canonical_id: 'urn:work:1', summary: 'Checkout conversion', graph_domain: 'WORK'}},
    {id: 'v2', label: 'Service', properties: {canonical_id: 'urn:svc:1', name: 'Checkout API', graph_domain: 'CODE'}},
  ];
  const edges = [
    {id: 'e1', label: 'IMPLEMENTS', source: 'v2', target: 'v1', properties: {creation_status: 'DETERMINISTIC'}},
  ];
  const errors = [];
  page.on('pageerror', error => errors.push(error.message));
  await page.route('**/*', async route => {
    const url = new URL(route.request().url());
    if (files.has(url.pathname)) {
      const [contentType, body] = files.get(url.pathname);
      return route.fulfill({contentType, body});
    }
    if (url.pathname === '/api/v1.2/graph-connections') {
      return route.fulfill({
        contentType: 'application/json',
        body: JSON.stringify({status: 200, data: {records: [{id: 7, host: 'hugegraph-server', graph: 'hugegraph'}]}}),
      });
    }
    if (url.pathname.endsWith('/gremlin-query')) {
      const request = JSON.parse(route.request().postData() || '{}');
      const graph = request.content.startsWith('g.V()')
        ? {vertices, edges: []}
        : {vertices, edges};
      return route.fulfill({
        contentType: 'application/json',
        body: JSON.stringify({status: 200, data: {graph_view: graph}}),
      });
    }
    return route.abort();
  });

  await page.goto('http://graph-idl.test/graph-idl.html');
  await expect(page.locator('#result-status')).toContainText('2 vertices / 1 relationships');
  await expect(page.locator('.node')).toHaveCount(2);
  await page.getByRole('button', {name: 'Table', exact: true}).click();
  await expect(page.locator('#relations')).toContainText('IMPLEMENTS');
  await page.getByRole('button', {name: 'RDF', exact: true}).click();
  await expect(page.locator('#rdf-view')).toContainText('eoip:IMPLEMENTS');
  await page.selectOption('#backend', 'neptune');
  await expect(page.locator('#backend-status')).toContainText('Amazon Neptune');
  expect(errors).toEqual([]);
});

test('guided Hubble displays all scenarios as live named connected domain graphs', async ({page}) => {
  test.skip(process.env.EOIP_RUNTIME_HUBBLE !== '1', 'Opt-in local Hubble administration test');
  test.setTimeout(180000);
  const errors = [];
  page.on('pageerror', error => errors.push(error.message));
  const responses = [];
  page.on('response', response => {
    if (response.url().includes('/gremlin-query')) responses.push(response);
  });
  await page.goto((process.env.EOIP_RUNTIME_HUBBLE_URL || 'http://localhost:8088') + '/enterprise.html');
  await expect(page.locator('#status')).toContainText('directed relationships displayed', {timeout: 65000});
  expect(await page.locator('#legend .badge').count()).toBeGreaterThan(1);
  const scenarios = await page.locator('#scenario option').evaluateAll(options => options.map(o => o.value));
  expect(scenarios).toHaveLength(13);
  for (const scenario of scenarios) {
    await page.selectOption('#scenario', scenario);
    await expect(page.locator('#status')).toContainText('directed relationships displayed', {timeout: 65000});
    expect(await page.locator('.node').count()).toBeGreaterThan(2);
    expect(await page.locator('.edge path[marker-end="url(#arrow)"]').count()).toBeGreaterThan(0);
    const domains = await page.locator('.node text:last-child').allTextContents();
    expect((await page.locator('#legend .badge').allTextContents()).sort()).toEqual(
      [...new Set(domains.map(text => text.split(' / ')[0]))].sort()
    );
    expect(await page.locator('.node').first().getAttribute('aria-label')).not.toMatch(/^eoip-/);
  }
  await page.selectOption('#scenario', 'business-value');
  await expect(page.locator('#status')).toContainText('directed relationships displayed', {timeout: 65000});
  await page.getByRole('button', {name: 'Increase successful checkout conversion', exact: true}).click();
  await expect(page.locator('#details')).toContainText('canonical_id');
  await expect(page.locator('#details')).toContainText(/synthetic/i);
  const before = await page.locator('.node').count();
  await page.getByRole('checkbox', {name: 'Show provenance and ingestion nodes'}).check();
  expect(await page.locator('.node').count()).toBeGreaterThan(before);
  await page.fill('#search', 'Maya');
  expect(await page.locator('#entity option').count()).toBe(1);
  await page.getByRole('button', {name: 'Explore selected entity'}).click();
  await expect(page.locator('#status')).toContainText('directed relationships displayed', {timeout: 65000});
  await expect(page.getByRole('button', {name: 'Maya Chen', exact: true})).toBeVisible();
  for (const response of responses) expect((await response.json()).status).toBe(200);
  expect(errors).toEqual([]);
  await page.getByRole('button', {name: 'Start walkthrough', exact: true}).click();
  await expect(page.locator('#status')).toContainText('directed relationships displayed', {timeout: 65000});
  await page.getByRole('button', {name: 'Stop walkthrough', exact: true}).click();
  await expect(page.getByRole('button', {name: 'Start walkthrough', exact: true})).toBeEnabled({timeout: 2000});
  await page.getByRole('button', {name: 'Start walkthrough', exact: true}).click();
  await page.getByRole('button', {name: 'Stop walkthrough', exact: true}).click();
  await expect(page.getByRole('button', {name: 'Start walkthrough', exact: true})).toBeEnabled({timeout: 65000});
});

test('guided Hubble surfaces application errors instead of displaying fixture data', async ({page}) => {
  test.skip(process.env.EOIP_RUNTIME_HUBBLE !== '1', 'Opt-in local Hubble administration test');
  await page.route('**/gremlin-query', route => route.fulfill({
    contentType: 'application/json', body: JSON.stringify({status: 400, message: 'Query rejected for test'})
  }));
  await page.goto((process.env.EOIP_RUNTIME_HUBBLE_URL || 'http://localhost:8088') + '/enterprise.html');
  await expect(page.locator('#status')).toHaveText('Hubble 400: Query rejected for test');
  expect(await page.locator('.node').count()).toBe(0);
});

test('Hubble opens the existing graph, executes Gremlin and displays metadata', async ({page}) => {
  test.skip(process.env.EOIP_RUNTIME_HUBBLE !== '1', 'Opt-in local Hubble administration test');
  await page.goto(process.env.EOIP_RUNTIME_HUBBLE_URL || 'http://localhost:8088');
  await expect(page.getByText('English', {exact: true})).toBeVisible();
  await expect(page.getByText('EOIP', {exact: true})).toBeVisible();
  await page.getByRole('button', {name: 'Visit', exact: true}).click();
  await expect(page).toHaveURL(/\/graph-management\/\d+\/data-analyze/);
  const editor = page.locator('.CodeMirror');
  await editor.click();
  await page.keyboard.type('g.V().limit(5)');
  const queryResponse = page.waitForResponse(response =>
    response.url().includes('/gremlin-query') && response.request().method() === 'POST'
  );
  await page.getByRole('button', {name: 'Execute Query', exact: true}).click();
  const result = await (await queryResponse).json();
  expect(result.status).toBe(200);
  expect(result.data.graph_view.vertices.length).toBeGreaterThan(0);
  await page.getByText('Json', {exact: true}).click();
  await expect(page.locator('body')).toContainText('canonical_id');
  await page.getByText('Metadata Configuration', {exact: true}).click();
  await page.getByText('Vertex Type', {exact: true}).click();
  await expect(page.locator('body')).toContainText('WorkItem');
});

test('Hubble preserves an explicit language choice', async ({page}) => {
  test.skip(process.env.EOIP_RUNTIME_HUBBLE !== '1', 'Opt-in local Hubble administration test');
  await page.addInitScript(() => localStorage.setItem('languageType', 'zh-CN'));
  await page.goto(process.env.EOIP_RUNTIME_HUBBLE_URL || 'http://localhost:8088');
  await expect(page.getByText('English', {exact: true})).not.toBeVisible();
  expect(await page.evaluate(() => localStorage.getItem('languageType'))).toBe('zh-CN');
});
