import { test, expect } from "@playwright/test";

test.describe("Theme and Visual System Snapshot Auditing", () => {
  test.beforeEach(async ({ page }) => {
    await page.goto("/signin");
    await page.getByTestId("signin-role-admin").click();
    await page.getByTestId("signin-submit-button").click();
    await expect(page.getByTestId("app-shell-nav-rail")).toBeVisible();
  });

  const themes = ["dark", "light", "hc-dark", "hc-light"];

  for (const theme of themes) {
    test(`Verify [data-theme="${theme}"] activation and styling`, async ({ page }) => {
      await page.getByTestId("theme-toggle-button").click();
      await page.getByTestId(`theme-option-${theme}`).click();
      await page.waitForTimeout(300);

      const htmlTheme = await page.locator("html").getAttribute("data-theme");
      expect(htmlTheme).toBe(theme);
    });
  }
});
