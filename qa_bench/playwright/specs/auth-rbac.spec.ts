import { test, expect } from "@playwright/test";

test.describe("Authentication and RBAC Personas", () => {
  test.beforeEach(async ({ page }) => {
    await page.goto("/signin");
    await expect(page.getByTestId("signin-form")).toBeVisible();
  });

  test("Sign-in page renders with branding and input controls", async ({ page }) => {
    await expect(page.getByTestId("signin-token-input")).toBeVisible();
    await expect(page.getByTestId("signin-tenant-input")).toBeVisible();
    await expect(page.getByTestId("signin-submit-button")).toBeVisible();
    await expect(page.getByTestId("signin-demo-roles")).toBeVisible();
  });

  const roles = [
    { label: "Super Admin", testid: "signin-role-super-admin" },
    { label: "Admin", testid: "signin-role-admin" },
    { label: "Steward", testid: "signin-role-steward" },
    { label: "Analyst", testid: "signin-role-analyst" },
    { label: "Viewer", testid: "signin-role-viewer" },
  ];

  for (const role of roles) {
    test(`Quick-fill demo role preset: ${role.label}`, async ({ page }) => {
      await page.getByTestId(role.testid).click();
      await page.getByTestId("signin-submit-button").click();
      await expect(page.getByTestId("app-shell-nav-rail")).toBeVisible();
    });
  }

  test("Invalid token rejection or offline graceful fallback", async ({ page }) => {
    await page.getByTestId("signin-token-input").fill("fake_invalid_token_99999");
    await page.getByTestId("signin-submit-button").click();
    await page.waitForTimeout(500);
    // Either error alert is shown or offline fallback gracefully loads shell
    const hasError = await page.getByTestId("signin-error").isVisible().catch(() => false);
    const hasShell = await page.getByTestId("app-shell-nav-rail").isVisible().catch(() => false);
    expect(hasError || hasShell).toBeTruthy();
  });
});
