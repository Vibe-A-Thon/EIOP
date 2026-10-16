import { test, expect } from '@playwright/test';

test.describe('Cognitive Engineering & AI Lab GUI', () => {
  test('renders cognitive engineering hub and navigation', async ({ page }) => {
    // Stub local health and admin stats
    await page.route('**/health/ready', route => route.fulfill({
      status: 200,
      contentType: 'application/json',
      body: JSON.stringify({ status: 'ready' }),
    }));

    await page.route('**/api/v1/admin/stats', route => route.fulfill({
      status: 200,
      contentType: 'application/json',
      body: JSON.stringify({
        vertices: 1540,
        edges: 3820,
        labels: { APIService: 12, Database: 8, WorkItem: 54 },
        worker: { status: 'READY', updated_at: new Date().toISOString() },
        schema: { ontology_version: 'v2.1', schema_version: '2026.1' },
      }),
    }));

    await page.route('**/api/v1/admin/system', route => route.fulfill({
      status: 200,
      contentType: 'application/json',
      body: JSON.stringify({ status: 'HEALTHY' }),
    }));

    await page.route('**/api/v1/admin/jobs', route => route.fulfill({
      status: 200,
      contentType: 'application/json',
      body: JSON.stringify([]),
    }));

    // Stub cognitive endpoints
    await page.route('**/api/v1/guardrails/reflection-sandbox', route => route.fulfill({
      status: 200,
      contentType: 'application/json',
      body: JSON.stringify({
        allowed: true,
        step_id: 'step-101',
        violations: [],
      }),
    }));

    await page.route('**/api/v1/guardrails/inoculate', route => route.fulfill({
      status: 200,
      contentType: 'application/json',
      body: JSON.stringify({
        resistance_score: 0.98,
        probes_tested: 4,
        probes_blocked: 4,
        inoculated_prompt: 'System prompt fortified with active adversarial shields.',
      }),
    }));

    await page.route('**/api/v1/context/slice-graph', route => route.fulfill({
      status: 200,
      contentType: 'application/json',
      body: JSON.stringify({
        query: 'checkout',
        total_candidates: 25,
        retained_count: 8,
        compression_ratio: 0.68,
        entities: [{ id: 'checkout-api', label: 'APIService', attention: 0.95 }],
        rendered_context: '# Compressed Context Slate',
      }),
    }));

    // Seed session token
    await page.addInitScript(() => {
      sessionStorage.setItem('eoip-token', 'mock-valid-token-secret-123');
    });

    // Navigate to local app
    await page.goto('/cognitive');

    // Check sidebar navigation item exists
    const cognitiveNav = page.locator('nav button:has-text("Cognitive Engineering")');
    await expect(cognitiveNav).toBeVisible();

    // Check Hero title
    await expect(page.locator('text=COGNITIVE INTELLIGENCE & ENGINEERING PLATFORM')).toBeVisible();
    await expect(page.locator('text=Autonomous Intelligence & Multi-Paradigm Engine')).toBeVisible();

    // Check tabs
    await expect(page.locator('text=15 Engineering Disciplines')).toBeVisible();
    await expect(page.locator('text=Reflection Sandbox & Inoculator')).toBeVisible();
    await expect(page.locator('text=Attention Slicer & Bitemporal')).toBeVisible();
    await expect(page.locator('text=Graph Repair & Distillation')).toBeVisible();
    await expect(page.locator('text=External MCP & Attestation')).toBeVisible();
    await expect(page.locator('text=Token Economics & Latency')).toBeVisible();

    // Verify 15 disciplines cards exist in matrix
    await expect(page.locator('text=Loop Engineering')).toBeVisible();
    await expect(page.locator('text=Harness Engineering')).toBeVisible();
    await expect(page.locator('text=Memory Engineering')).toBeVisible();
    await expect(page.locator('text=Graph-over-Loop Engineering')).toBeVisible();
    await expect(page.locator('text=Loop-over-Graph Engineering')).toBeVisible();
    await expect(page.locator('text=Tool & API Contracts (MCP)')).toBeVisible();
  });
});
