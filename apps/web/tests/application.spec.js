import {test, expect} from '@playwright/test';

async function proxyApiRequests(page) {
  if (!process.env.PLAYWRIGHT_API_PROXY) return;
  const target = new URL(process.env.PLAYWRIGHT_API_PROXY);
  await page.route('**/api/v1/**', async route => {
    const url = new URL(route.request().url());
    url.protocol = target.protocol;
    url.host = target.host;
    const response = await route.fetch({url: url.toString()});
    await route.fulfill({response});
  });
}

const workItemId = 'urn:eoip:work:item:jira:EOIP-1';
const symbolId = 'urn:eoip:code:symbol:compute_impact';
const fileId = 'urn:eoip:code:file:impact.py';

const fixtureGraph = {
  nodes: [
    {id: workItemId, label: 'WorkItem', properties: {issue_key: 'EOIP-1', display_name: 'EOIP-1'}},
    {id: symbolId, label: 'CodeSymbol', properties: {qualified_name: 'compute_impact', name: 'compute_impact'}},
    {id: fileId, label: 'File', properties: {path: 'packages/eoip/graph/impact.py'}},
  ],
  edges: [
    {id: 'edge-implements', from_id: workItemId, to_id: symbolId, type: 'IMPLEMENTS', properties: {source_ref: 'jira:EOIP-1'}},
    {id: 'edge-declares', from_id: fileId, to_id: symbolId, type: 'DECLARES', properties: {source_ref: 'git:impact.py'}},
  ],
  paths: [{node_ids: [workItemId, symbolId, fileId], edge_ids: ['edge-implements', 'edge-declares']}],
  warnings: [],
  partial: false,
};

async function stubApplicationApi(page) {
  await page.route('**/health/ready', route => route.fulfill({
    status: 200,
    contentType: 'application/json',
    body: '{"status":"ready"}',
  }));
  await page.route('**/api/v1/**', async route => {
    const request = route.request();
    const url = new URL(request.url());
    const path = url.pathname;
    const token = request.headers().authorization || '';
    if (token === 'Bearer invalid') {
      return route.fulfill({
        status: 401,
        contentType: 'application/json',
        headers: {'X-Correlation-ID': 'browser-invalid-token'},
        body: JSON.stringify({detail: 'Provide a valid Bearer token'}),
      });
    }

    let status = 200;
    let body = {};
    if (path === '/api/v1/admin/stats') {
      body = {vertices: 3, edges: 2, labels: {WorkItem: 1, CodeSymbol: 1, File: 1}, backend: 'memory', worker: {status: 'ready'}, schema: {ontology_version: 'g2', schema_version: '1.0'}};
    } else if (path === '/api/v1/admin/system') {
      body = {graph: {status: 'ready'}, model: {status: 'deterministic'}, backup: {status: 'not_created'}};
    } else if (path === '/api/v1/admin/jobs') {
      body = [];
    } else if (path === '/api/v1/query/nl') {
      body = {interpretation: {plan: {intent: 'impact'}, explanation: 'bounded impact query'}, result: fixtureGraph};
    } else if (path === '/api/v1/search') {
      body = fixtureGraph;
    } else if (path.startsWith('/api/v1/entities/')) {
      body = fixtureGraph.nodes.find(node => node.id === decodeURIComponent(path.replace('/api/v1/entities/', ''))) || fixtureGraph.nodes[1];
    } else if (path === '/api/v1/impact' || path === '/api/v1/path') {
      body = fixtureGraph;
    } else if (path === '/api/v1/agents/trace-impact') {
      body = {summary: '2 connected entities within deterministic TraceImpact scope', evidence_refs: ['jira:EOIP-1', 'git:impact.py'], partial: false};
    } else if (path === '/api/v1/admin/validation') {
      body = {valid: true, vertices_checked: 3, edges_checked: 2, finished_at: '2026-10-05T00:00:00Z', quality: {evidence_coverage: 1, provenance_coverage: 1, schema_compliance: 1, completeness: 1, freshness: 1, orphan_rate: 0, duplicate_rate: 0, error_count: 0, warning_count: 0}, findings: []};
    } else if (path === '/api/v1/graph/schema') {
      body = {ontology_version: 'g2', schema_version: '1.0', domains: ['WORK', 'CODE'], vertex_labels: {WorkItem: {domain: 'WORK', instance_count: 1, required_properties: ['issue_key']}, CodeSymbol: {domain: 'CODE', instance_count: 1, required_properties: ['qualified_name']}}, edge_labels: {IMPLEMENTS: {source_labels: ['WorkItem'], target_labels: ['CodeSymbol'], properties: ['source_ref']}, DECLARES: {source_labels: ['File'], target_labels: ['CodeSymbol'], properties: ['source_ref']}}, indexes: [{name: 'by_canonical_id', type: 'composite', label: 'global', fields: ['canonical_id']}]};
    } else if (path === '/api/v1/connectors/catalog') {
      body = {connectors: [
        {id: 'jira', name: 'Jira', type: 'api', capabilities: ['baseline', 'poll', 'webhook', 'replay']},
        {id: 'web', name: 'Web Crawler', type: 'crawler', capabilities: ['baseline', 'poll', 'reconcile']},
      ]};
    } else if (path === '/api/v1/sources') {
      body = [{
        source_id: 'jira-prod',
        source_type: 'jira',
        name: 'Jira Prod',
        enabled: true,
        health: 'HEALTHY',
        acquisition_modes: ['baseline', 'poll', 'replay'],
        checkpoint: '2026-10-05T10:00:00Z',
        capabilities: {baseline: true, polling: true, webhooks: true, discovery: true, reconciliation: false, replay: true},
      }];
    } else if (path === '/api/v1/sources/jira-prod/discover') {
      body = {source_id: 'jira-prod', status: 'COMPLETE', items: [{key: 'EOIP-1', type: 'issue'}]};
    } else if (path === '/api/v1/sources/jira-prod/dry-run') {
      status = 202;
      body = {job_id: 'job-dry-run', status: 'PENDING'};
    } else if (path === '/api/v1/admin/dlq') {
      body = [{
        event_id: 'a'.repeat(64),
        source_system: 'jira',
        source_record_id: 'missing-key-record',
        payload_hash: 'b'.repeat(64),
        error_category: 'mapping_error',
        error: 'Issue key is required',
      }];
    } else {
      status = 404;
      body = {detail: `Unexpected API request: ${path}`};
    }
    return route.fulfill({status, contentType: 'application/json', body: JSON.stringify(body)});
  });
}

test('login, search, trace graph evidence, and administer persisted data', async ({page}) => {
  const errors = [];
  page.on('pageerror', error => errors.push(error.message));
  if (process.env.PLAYWRIGHT_API_PROXY) await proxyApiRequests(page);
  else await stubApplicationApi(page);
  await page.goto('/app');
  await page.getByLabel('Access token').fill(process.env.EOIP_API_TOKEN);
  await page.getByRole('button', {name: 'Connect', exact: true}).click();
  await expect(page.getByRole('heading', {name: 'Relationship map'})).toBeVisible();
  await page.getByRole('textbox', {name: 'Ask the knowledge graph'}).fill('what is the impact of EOIP-1');
  await page.getByRole('button', {name: 'Ask graph'}).click();
  await expect(page.getByRole('status')).toContainText('Interpreted as', {timeout: 15000});
  await page.getByRole('textbox', {name: 'Search knowledge graph'}).fill('compute_impact');
  await page.getByRole('button', {name: 'Search graph'}).click();
  const symbol = page.locator('.entity-list button').filter({hasText: 'compute_impact'}).first();
  await expect(symbol).toBeVisible();
  await symbol.click();
  await expect(page.getByRole('button', {name: 'Explore impact'})).toBeVisible();
  await page.getByRole('tab', {name: 'Impact'}).click();
  await page.getByLabel('From canonical ID').fill('urn:eoip:work:item:jira:EOIP-1');
  await page.getByRole('button', {name: 'Find path'}).click();
  const graph = page.getByRole('img', {name: /Knowledge graph/});
  await expect(graph).toBeVisible();
  await expect(graph).toHaveAttribute('aria-label', /IMPLEMENTS/);
  await expect(graph).toHaveAttribute('aria-label', /DECLARES/);
  await page.getByRole('button', {name: 'Run TraceImpact'}).click();
  await expect(page.getByRole('heading', {name: 'TraceImpact result'})).toBeVisible({timeout: 15000});
  await expect(page.getByText('connected entities within', {exact: false})).toBeVisible({timeout: 15000});
  await page.screenshot({path: 'test-results/explorer.png', fullPage: true});
  await page.getByRole('link', {name: 'Administration', exact: true}).click();
  await expect(page.getByRole('heading', {name: 'Ingestion jobs'})).toBeVisible();
  await page.route('**/api/v1/connectors/catalog', route => route.fulfill({
    status: 200,
    contentType: 'application/json',
    body: JSON.stringify({connectors: [
      {id: 'jira', name: 'Jira', type: 'api', capabilities: ['baseline', 'poll', 'webhook', 'replay']},
      {id: 'web', name: 'Web Crawler', type: 'crawler', capabilities: ['baseline', 'poll', 'reconcile']},
    ]}),
  }));
  await page.route('**/api/v1/sources', route => {
    if (route.request().method() === 'POST') {
      return route.fulfill({
        status: 201,
        contentType: 'application/json',
        body: JSON.stringify({source_id: 'jira-prod', source_type: 'jira', name: 'Jira Prod', enabled: true}),
      });
    }
    return route.fulfill({
      status: 200,
      contentType: 'application/json',
      body: JSON.stringify([{
        source_id: 'jira-prod',
        source_type: 'jira',
        name: 'Jira Prod',
        enabled: true,
        health: 'HEALTHY',
        acquisition_modes: ['baseline', 'poll', 'replay'],
        checkpoint: '2026-10-05T10:00:00Z',
        capabilities: {baseline: true, polling: true, webhooks: true, discovery: true, reconciliation: false, replay: true},
      }]),
    });
  });
  await page.route('**/api/v1/sources/jira-prod/discover', route => route.fulfill({
    status: 200,
    contentType: 'application/json',
    body: JSON.stringify({source_id: 'jira-prod', status: 'COMPLETE', items: [{key: 'EOIP-1', type: 'issue'}]}),
  }));
  await page.route('**/api/v1/sources/jira-prod/dry-run', route => route.fulfill({
    status: 202,
    contentType: 'application/json',
    body: JSON.stringify({job_id: 'job-dry-run', status: 'PENDING'}),
  }));
  await page.getByRole('tab', {name: 'Sources & jobs'}).click();
  await page.getByRole('button', {name: 'Load source control'}).click();
  await expect(page.getByRole('heading', {name: 'Registered sources'})).toBeVisible();
  await expect(page.getByText('Jira Prod')).toBeVisible();
  await expect(page.getByText('baseline, poll, replay')).toBeVisible();
  const jiraRow = page.getByRole('row', {name: /Jira Prod/});
  await jiraRow.getByRole('button', {name: 'Discover'}).click();
  await expect(page.getByRole('heading', {name: 'jira-prod'})).toBeVisible();
  await expect(page.getByText('EOIP-1')).toBeVisible();
  await jiraRow.getByRole('button', {name: 'Dry run'}).click();
  await page.getByRole('button', {name: 'Run validation'}).click();
  await expect(page.getByText(/Checked \d+ entities and \d+ relationships/)).toBeVisible();
  await page.getByRole('tab', {name: 'Quality & ontology'}).click();
  await page.getByRole('button', {name: 'Load ontology schema'}).click();
  await expect(page.getByRole('heading', {name: /Vertex labels/})).toBeVisible();
  await expect(page.getByRole('heading', {name: /Edge labels/})).toBeVisible();
  await expect(page.getByRole('heading', {name: /Index coverage/})).toBeVisible();
  await page.screenshot({path: 'test-results/admin.png', fullPage: true});
  await page.route('**/api/v1/admin/dlq?limit=25', route => route.fulfill({
    status: 200,
    contentType: 'application/json',
    body: JSON.stringify([{
      event_id: 'a'.repeat(64),
      source_system: 'jira',
      source_record_id: 'missing-key-record',
      payload_hash: 'b'.repeat(64),
      error_category: 'mapping_error',
      error: 'Issue key is required',
    }]),
  }));
  await page.getByRole('tab', {name: 'Audit & recovery'}).click();
  await page.getByRole('button', {name: 'Load DLQ'}).click();
  await expect(page.getByText('Issue key is required')).toBeVisible();
  await expect(page.getByText('missing-key-record')).toBeVisible();
  await expect(page.getByRole('button', {name: 'Replay', exact: true})).toBeVisible();
  await expect(page.getByText('b'.repeat(64))).toHaveCount(0);
  expect(errors).toEqual([]);
});

test('invalid credentials show an error without granting access', async ({page}) => {
  if (process.env.PLAYWRIGHT_API_PROXY) await proxyApiRequests(page);
  else await stubApplicationApi(page);
  await page.goto('/app');
  await page.getByLabel('Access token').fill('invalid');
  await page.getByRole('button', {name: 'Connect', exact: true}).click();
  await expect(page.getByRole('alert')).toContainText('valid Bearer token');
  await expect(page.getByRole('heading', {name: 'Relationship map'})).toHaveCount(0);
});
