import { expect, test } from "@playwright/test";

test("landing page links into the workspace", async ({ page }) => {
  await page.goto("/");
  await expect(page.getByRole("heading", { name: /bounded autonomous agents/i })).toBeVisible();
  await page.getByRole("link", { name: /open workspace/i }).click();
  await expect(page).toHaveURL(/dashboard/);
});
