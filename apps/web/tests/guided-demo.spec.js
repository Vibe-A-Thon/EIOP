import {readFileSync} from 'node:fs';
import {test, expect} from '@playwright/test';

const scenarioPack = JSON.parse(readFileSync(
  new URL('../../../demo/demodata/enterprise/scenario-pack.json', import.meta.url),
  'utf8',
));
const scenarioRelationships = [...new Set(scenarioPack.edges.map(edge => edge.label))].sort();

async function stubAuthenticatedApi(page, {failPath = false, failCatalog = false, emptyCatalog = false, catalogDelayMs = 0} = {}) {
  const pathRequests = [];
  let catalogFailuresRemaining = failCatalog ? 1 : 0;
  await page.route('**/api/v1/**', async route => {
    const request = route.request();
    const url = new URL(request.url());
    if (url.pathname === '/api/v1/admin/stats') {
      return route.fulfill({json: {vertices: 0, edges: 0, labels: {}, worker: {status: 'ready'}}});
    }
    if (url.pathname === '/api/v1/admin/system') {
      return route.fulfill({json: {}});
    }
    if (url.pathname === '/api/v1/admin/jobs') {
      return route.fulfill({json: []});
    }
    if (url.pathname === '/api/v1/demo/scenarios') {
      if (catalogDelayMs) {
        await new Promise(resolve => setTimeout(resolve, catalogDelayMs));
      }
      if (catalogFailuresRemaining > 0) {
        catalogFailuresRemaining -= 1;
        return route.fulfill({status: 503, json: {detail: 'Scenario service unavailable'}});
      }
      return route.fulfill({json: {
        ...scenarioPack,
        scenarios: (emptyCatalog ? [] : scenarioPack.scenarios).map(scenario => ({
          ...scenario,
          ready: true,
          relationship_allowlist: scenarioRelationships,
          expected_path_state: scenario.expected_path.map(canonical_id => ({canonical_id, available: true})),
        })),
      }});
    }
    if (url.pathname === '/api/v1/path' && request.method() === 'POST') {
      const body = request.postDataJSON();
      pathRequests.push(body);
      if (failPath) {
        return route.fulfill({status: 404, json: {detail: 'Declared target is not in the live graph'}});
      }
      return route.fulfill({json: {
        nodes: [
          {id: body.source_id, label: 'WorkItem', domain: 'WORK', properties: {canonical_id: body.source_id}},
          {id: body.target_id, label: 'Symbol', domain: 'CODE', properties: {canonical_id: body.target_id}},
        ],
        edges: [],
        paths: [[body.source_id, body.target_id]],
        warnings: [],
        partial: false,
      }});
    }
    return route.fulfill({status: 404, json: {detail: `Unexpected API request: ${url.pathname}`}});
  });
  await page.route('**/health/ready', route => route.fulfill({status: 200, body: 'ready'}));
  return pathRequests;
}

async function loginAndOpenDemo(page) {
  await page.goto('/app');
  await page.getByLabel('Access token').fill('test-token');
  await page.getByRole('button', {name: 'Connect', exact: true}).click();
  await page.getByRole('link', {name: 'Guided demo', exact: true}).click();
  await expect(page.getByRole('heading', {name: 'Follow the enterprise digital thread'})).toBeVisible();
}

test('guided demo lists and executes a live-contract path for every declared scenario', async ({page}) => {
  const pathRequests = await stubAuthenticatedApi(page);
  await loginAndOpenDemo(page);

  await expect(page.locator('.guided-scenario')).toHaveCount(scenarioPack.scenarios.length);
  for (const scenario of scenarioPack.scenarios) {
    const card = page.getByTestId(`scenario-${scenario.id}`);
    await expect(card.getByRole('heading', {name: scenario.title})).toBeVisible();
    await expect(card).toContainText(scenario.audience);
    await expect(card).toContainText(scenario.story);
    await card.getByRole('button', {name: 'Run declared path'}).click();
    await expect(card.getByRole('status', {name: `${scenario.title} result`})).toContainText('Path returned');
    await expect(card.getByRole('status', {name: `${scenario.title} result`}))
      .toContainText(scenario.expected_path.at(-1));
  }

  expect(pathRequests).toHaveLength(scenarioPack.scenarios.length);
  expect(pathRequests).toEqual(scenarioPack.scenarios.map(scenario => ({
    source_id: scenario.expected_path[0],
    target_id: scenario.expected_path.at(-1),
    max_depth: 8,
    relationship_allowlist: scenarioRelationships,
  })));
});

test('guided demo displays the API error returned for a scenario path', async ({page}) => {
  await stubAuthenticatedApi(page, {failPath: true});
  await loginAndOpenDemo(page);

  const scenario = scenarioPack.scenarios[0];
  const card = page.getByTestId(`scenario-${scenario.id}`);
  await card.getByRole('button', {name: 'Run declared path'}).click();
  await expect(card.getByRole('status', {name: `${scenario.title} result`}))
    .toContainText('Declared target is not in the live graph');
});

test('guided demo makes catalog loading visible while the local API responds', async ({page}) => {
  await stubAuthenticatedApi(page, {catalogDelayMs: 500});
  await page.goto('/app');
  await page.getByLabel('Access token').fill('test-token');
  await page.getByRole('button', {name: 'Connect', exact: true}).click();
  await page.getByRole('link', {name: 'Guided demo', exact: true}).click();
  await expect(page.getByText('Loading scenarios from the local API…')).toBeVisible();
  await expect(page.getByRole('heading', {name: 'Follow the enterprise digital thread'})).toBeVisible();
});

test('guided demo explains an empty scenario catalog', async ({page}) => {
  await stubAuthenticatedApi(page, {emptyCatalog: true});
  await loginAndOpenDemo(page);
  await expect(page.getByRole('status')).toContainText('No enterprise scenarios available');
  await expect(page.locator('.guided-scenario')).toHaveCount(0);
});

test('guided demo shows catalog API errors and allows a refresh', async ({page}) => {
  await stubAuthenticatedApi(page, {failCatalog: true});
  await loginAndOpenDemo(page);
  await expect(page.getByRole('alert')).toContainText('Scenario service unavailable');
  await page.getByRole('button', {name: 'Refresh scenario catalog'}).click();
  await expect(page.locator('.guided-scenario')).toHaveCount(scenarioPack.scenarios.length);
});
