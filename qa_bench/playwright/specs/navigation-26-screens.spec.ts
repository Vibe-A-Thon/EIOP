import { test, expect } from "@playwright/test";

const ROUTES = [
  { id: "overview", path: "/overview", title: "Overview" },
  { id: "ask", path: "/ask", title: "Ask" },
  { id: "graph", path: "/graph", title: "Graph Explorer" },
  { id: "meta-graph", path: "/meta-graph", title: "Meta-graph" },
  { id: "query", path: "/query", title: "Query" },
  { id: "impact", path: "/impact", title: "Impact" },
  { id: "changes", path: "/changes", title: "Changes" },
  { id: "time", path: "/time", title: "Time Travel" },
  { id: "incidents", path: "/incidents", title: "Incidents" },
  { id: "ontology", path: "/ontology", title: "Ontology" },
  { id: "quality", path: "/quality", title: "Quality" },
  { id: "snapshots", path: "/snapshots", title: "Snapshots" },
  { id: "ingestion", path: "/ingestion", title: "Ingestion" },
  { id: "agents", path: "/agents", title: "Agents" },
  { id: "reports", path: "/reports", title: "Reports" },
  { id: "collaboration", path: "/collaboration", title: "Collaboration" },
  { id: "health", path: "/health", title: "Health" },
  { id: "governance", path: "/governance", title: "Governance" },
  { id: "brand", path: "/brand", title: "Brand" },
  { id: "tenant", path: "/tenant", title: "Tenant" },
  { id: "settings", path: "/settings", title: "Settings" },
  { id: "help", path: "/help", title: "Help" },
];

test.describe("Full 22+ Task Screen Route Audit", () => {
  test.beforeEach(async ({ page }) => {
    // Authenticate as Admin
    await page.goto("/signin");
    await page.getByTestId("signin-role-admin").click();
    await page.getByTestId("signin-submit-button").click();
    await expect(page.getByTestId("app-shell-nav-rail")).toBeVisible();
  });

  for (const route of ROUTES) {
    test(`Screen Audit: ${route.title} (${route.path})`, async ({ page }) => {
      const consoleErrors: string[] = [];
      page.on("console", (msg) => {
        if (msg.type() === "error") {
          consoleErrors.push(msg.text());
        }
      });

      // Navigate via NavRail link
      const navItem = page.getByTestId(`app-shell-nav-${route.id}`);
      if (await navItem.isVisible()) {
        await navItem.click();
      } else {
        await page.goto(route.path);
      }

      await page.waitForTimeout(300);
      const mainContent = page.locator("main");
      await expect(mainContent).toBeVisible();

      // Check no uncaught runtime exceptions
      const fatalErrors = consoleErrors.filter((e) => e.includes("Uncaught") || e.includes("TypeError"));
      expect(fatalErrors).toHaveLength(0);
    });
  }
});
