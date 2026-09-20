import { expect, test } from "@playwright/test";

// End-to-end happy path against the real stack (web + api + postgres).
// Requires the API and a database to be running - see the "e2e" job in
// .github/workflows/ci.yml for how CI wires that up with docker services.
test("a visitor can create a poll, vote, and see the results update", async ({ page }) => {
  await page.goto("/");

  await page.getByLabel("Question").fill("Tabs or spaces?");
  await page.getByLabel("Option 1").fill("Tabs");
  await page.getByLabel("Option 2").fill("Spaces");
  await page.getByRole("button", { name: "Create poll" }).click();

  await expect(page.getByRole("heading", { name: "Tabs or spaces?" })).toBeVisible();

  await page.getByRole("button", { name: "Tabs" }).click();

  await expect(page.getByLabel("poll results")).toBeVisible();
  await expect(page.getByText(/1 votes \(100%\)/)).toBeVisible();
});
