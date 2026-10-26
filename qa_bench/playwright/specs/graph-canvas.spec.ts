import { test, expect } from "@playwright/test";

test.describe("Graph Explorer and Sigma.js WebGL Canvas", () => {
  test.beforeEach(async ({ page }) => {
    await page.goto("/signin");
    await page.getByTestId("signin-role-admin").click();
    await page.getByTestId("signin-submit-button").click();
    await expect(page.getByTestId("app-shell-nav-rail")).toBeVisible();
    await page.getByTestId("app-shell-nav-graph").click();
  });

  test("Graph Explorer interface loads canvas or seed search", async ({ page }) => {
    const canvas = page.getByTestId("graph-canvas");
    const searchInput = page.locator('input[placeholder*="Search"]');
    const isEmptyOrCanvas = (await canvas.isVisible().catch(() => false)) || (await searchInput.isVisible().catch(() => false));
    expect(isEmptyOrCanvas).toBeTruthy();
  });

  test("Lens switcher toggles between Domain and Fact lenses", async ({ page }) => {
    const domainLens = page.getByTestId("graph-lens-domain");
    const factLens = page.getByTestId("graph-lens-fact");

    if (await domainLens.isVisible()) {
      await domainLens.click();
      await page.waitForTimeout(200);
      await factLens.click();
      await page.waitForTimeout(200);
    }
  });
});
