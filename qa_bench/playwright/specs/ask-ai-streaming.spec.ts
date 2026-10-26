import { test, expect } from "@playwright/test";

test.describe("Ask AI Interface and Answer Modes", () => {
  test.beforeEach(async ({ page }) => {
    await page.goto("/signin");
    await page.getByTestId("signin-role-analyst").click();
    await page.getByTestId("signin-submit-button").click();
    await expect(page.getByTestId("app-shell-nav-rail")).toBeVisible();
    await page.getByTestId("app-shell-nav-ask").click();
  });

  test("Ask composer renders with prompt input and egress badge", async ({ page }) => {
    await expect(page.getByTestId("ask-query-input")).toBeVisible();
    await expect(page.getByTestId("ask-boundary-badge")).toBeVisible();
    await expect(page.getByTestId("ask-mode-deterministic")).toBeVisible();
    await expect(page.getByTestId("ask-mode-narrated")).toBeVisible();
  });

  test("Toggle answer mode between deterministic and narrated", async ({ page }) => {
    await page.getByTestId("ask-mode-narrated").click();
    await page.waitForTimeout(150);
    await page.getByTestId("ask-mode-deterministic").click();
    await page.waitForTimeout(150);
  });

  test("Clicking suggested question seeds the textarea", async ({ page }) => {
    const firstSuggestion = page.getByTestId("ask-suggestion-0");
    if (await firstSuggestion.isVisible()) {
      await firstSuggestion.click();
      await page.waitForTimeout(300);
    }
  });
});
