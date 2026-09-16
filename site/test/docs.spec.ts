import { readFileSync } from "node:fs";
import { expect, test, type Page } from "@playwright/test";

const catalogue = JSON.parse(
  readFileSync(new URL("../../catalogue/errors.json", import.meta.url), "utf8"),
);

async function openSearch(page: Page) {
  await page.goto("/");
  await page.getByRole("button", { name: "Search", exact: true }).click();
  return page.getByRole("dialog", { name: "Search", exact: true });
}

test("every condition can be found by its stable ID", async ({ page }) => {
  // Each query includes the search UI debounce; allow the catalogue to grow.
  test.setTimeout(30_000 + catalogue.entries.length * 1_000);
  const dialog = await openSearch(page);
  for (const entry of catalogue.entries) {
    await dialog.getByRole("textbox", { name: "Search", exact: true }).fill(entry.id);
    await expect(dialog.locator(`a[href="/errors/${entry.id}/"]`)).toBeVisible();
  }
});

for (const [query, id] of [
  ["message is not modified", "message.not_modified"],
  ["ChatMigrated", "chat.migrated"],
]) {
  test(`searching ${query} opens the condition page`, async ({ page }) => {
    const dialog = await openSearch(page);
    await dialog.getByRole("textbox", { name: "Search", exact: true }).fill(query);
    await dialog.locator(`a[href="/errors/${id}/"]`).click();
    await expect(page).toHaveURL(new RegExp(`/errors/${id.replaceAll(".", "\\.")}/$`));
    await expect(page.getByRole("heading", { level: 1 })).toContainText(id);
    await expect(page.getByRole("heading", { name: "Evidence", exact: true })).toBeVisible();
  });
}

test("condition navigation and agent exports work on the current host", async ({ page, request }) => {
  const errors: string[] = [];
  page.on("pageerror", (error) => errors.push(error.message));
  await page.goto("/");
  await page.getByRole("main").getByRole("link", { name: "chat.not_found", exact: true }).click();
  await expect(page).toHaveURL("http://127.0.0.1:4173/errors/chat.not_found/");
  await expect(page.getByRole("main")).toContainText("The bot could not resolve this chat.");

  const markdownLink = page.getByRole("link", { name: "Markdown", exact: true });
  const markdown = await request.get((await markdownLink.getAttribute("href"))!);
  expect(markdown.ok()).toBe(true);
  expect(await markdown.text()).toContain("https://errorgram.rmbk.me/errors/chat.not_found/");
  expect(await markdown.text()).toContain("Bad Request: chat not found");

  const recordLink = page.getByRole("link", { name: "Condition JSON", exact: true });
  const record = await request.get((await recordLink.getAttribute("href"))!);
  expect(record.ok()).toBe(true);
  expect(JSON.stringify(await record.json())).toContain('"chat.not_found"');

  for (const path of ["/", "/catalogue/", "/errors/message.not_modified/", "/agents/"]) {
    await page.goto(path);
    expect(await page.evaluate(() => document.documentElement.scrollWidth - innerWidth)).toBeLessThanOrEqual(1);
  }
  await page.getByRole("main").getByRole("link", { name: "llms.txt", exact: true }).click();
  await expect(page).toHaveURL("http://127.0.0.1:4173/llms.txt");
  expect(errors).toEqual([]);
});
