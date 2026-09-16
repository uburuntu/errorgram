import { expect, test, type Page } from "@playwright/test";

const issueUrl = "https://github.com/uburuntu/errorgram/issues/new?template=unknown-error.yml";

async function classify(page: Page, response: unknown, method = "") {
  await page.getByRole("textbox", { name: "API response JSON", exact: true }).fill(JSON.stringify(response));
  await page.getByRole("textbox", { name: "API method (optional)", exact: true }).fill(method);
  await page.getByRole("button", { name: "Classify response", exact: true }).click();
  return page.getByRole("region", { name: "Classification result", exact: true });
}

test.beforeEach(async ({ page }) => {
  await page.goto("/playground/");
  await expect(page.getByRole("button", { name: "Classify response", exact: true })).toBeEnabled();
});

test("a known response uses the SDK condition, summary, and reference", async ({ page }) => {
  const result = await classify(page, { ok: false, error_code: 400, description: "Bad Request: chat not found" });
  await expect(result.locator("#playground-status")).toHaveText("matched");
  await expect(result.locator("#playground-condition")).toHaveText("chat.not_found");
  await expect(result).toContainText("The bot could not resolve this chat.");
  await expect(result.locator("#playground-facts")).toHaveText("{}");
  await expect(result.getByRole("link", { name: "Read this condition’s reference" })).toHaveAttribute("href", "/errors/chat.not_found/");
  await result.getByRole("link", { name: "Read this condition’s reference" }).click();
  await expect(page.getByRole("heading", { level: 1 })).toContainText("chat.not_found");
});

test("method-specific conditions require method context", async ({ page }) => {
  const response = { ok: false, error_code: 400, description: "Bad Request: file is too big" };
  const result = await classify(page, response);
  await expect(result.locator("#playground-status")).toHaveText("insufficient_context");
  await expect(result.getByRole("link", { name: "file.download_too_large", exact: true })).toBeVisible();
  await classify(page, response, "  GETFILE  ");
  await expect(result.locator("#playground-status")).toHaveText("matched");
  await expect(result.locator("#playground-condition")).toHaveText("file.download_too_large");
  await classify(page, response, "sendMessage");
  await expect(result.locator("#playground-status")).toHaveText("unknown");
});

test("structured values match independently of text and conflicting values stay ambiguous", async ({ page }) => {
  const result = await classify(page, {
    ok: false, error_code: 429, description: "A different description", parameters: { retry_after: 17 },
  });
  await expect(result.locator("#playground-condition")).toHaveText("request.retry_after");
  expect(JSON.parse(await result.locator("#playground-facts").innerText())).toEqual({ retry_after: 17 });

  await classify(page, {
    ok: false, error_code: 400, description: "Another description", parameters: { migrate_to_chat_id: -1001234567890 },
  });
  await expect(result.locator("#playground-condition")).toHaveText("chat.migrated");
  expect(JSON.parse(await result.locator("#playground-facts").innerText())).toEqual({ migrate_to_chat_id: -1001234567890 });

  await classify(page, {
    ok: false, error_code: 429, description: "Too Many Requests: retry after 17",
    parameters: { retry_after: 17, migrate_to_chat_id: -1001234567890 },
  });
  await expect(result.locator("#playground-status")).toHaveText("ambiguous");
  await expect(result.getByRole("link", { name: "request.retry_after", exact: true })).toBeVisible();
  await expect(result.getByRole("link", { name: "chat.migrated", exact: true })).toBeVisible();
  await expect(result.locator("#playground-facts")).toHaveText("{}");

  await classify(page, {
    ok: false, error_code: 429, description: "Too Many Requests: retry after 17", parameters: { retry_after: "17" },
  });
  await expect(result.locator("#playground-status")).toHaveText("unknown");
});

test("unknown data is never rendered as markup or included in the issue URL", async ({ page }) => {
  const result = await classify(page, {
    ok: false, error_code: 400,
    description: '<img src="/private-probe" onerror="document.body.dataset.injected=1"> private-example-marker',
  });
  await expect(result.locator("#playground-status")).toHaveText("unknown");
  await expect(result.locator("img")).toHaveCount(0);
  await expect(result).not.toContainText("private-example-marker");
  expect(await page.locator("body").getAttribute("data-injected")).toBeNull();
  const report = result.getByRole("link", { name: "Open the unknown-error form", exact: true });
  await expect(report).toHaveAttribute("href", issueUrl);
  await expect(report).toHaveAttribute("rel", "noopener noreferrer");
  expect(new URL((await report.getAttribute("href"))!).searchParams.size).toBe(1);
});

test("invalid JSON, success responses, and oversized input have clear distinct outcomes", async ({ page }) => {
  const input = page.getByRole("textbox", { name: "API response JSON", exact: true });
  const submit = page.getByRole("button", { name: "Classify response", exact: true });
  const error = page.getByRole("alert");
  await submit.click();
  await expect(error).toContainText("Paste a JSON response");
  await expect(input).toBeFocused();
  await input.fill('{ "private-example-marker": }');
  await submit.click();
  await expect(error).toContainText("This is not valid JSON");
  await expect(error).not.toContainText("private-example-marker");
  await expect(input).toHaveAttribute("aria-invalid", "true");
  await expect(page.locator("#playground-result")).toBeHidden();

  const result = await classify(page, { ok: true, result: [] });
  await expect(result.locator("#playground-status")).toHaveText("not_api_error");
  await expect(input).not.toHaveAttribute("aria-invalid");
  await expect(result.getByRole("link", { name: "Open the unknown-error form" })).toBeHidden();

  await input.fill(JSON.stringify({ ok: false, error_code: 400, description: "x".repeat(32_768) }));
  await submit.click();
  await expect(error).toContainText("Use at most 32,768 characters");
  await expect(page.locator("#playground-result")).toBeHidden();
});

test("typing, example loading, classification, and clearing stay local", async ({ page, context }) => {
  // Begin after static scripts and styles load, then observe every subsequent request.
  await page.waitForLoadState("networkidle");
  const requests: string[] = [];
  const logs: string[] = [];
  const failures: string[] = [];
  page.on("request", (request) => requests.push(request.url()));
  page.on("console", (message) => logs.push(message.text()));
  page.on("pageerror", (error) => failures.push(error.message));
  await context.setOffline(true);
  const storageBefore = await page.evaluate(() => ({ local: { ...localStorage }, session: { ...sessionStorage }, cookie: document.cookie }));

  const result = await classify(page, { ok: false, error_code: 400, description: "private-example-marker" }, "private-method-marker");
  await expect(result.locator("#playground-status")).toHaveText("unknown");
  await page.getByRole("button", { name: "Load example", exact: true }).click();
  await page.getByRole("button", { name: "Classify response", exact: true }).click();
  await expect(result.locator("#playground-condition")).toHaveText("request.retry_after");
  await page.getByRole("button", { name: "Clear", exact: true }).click();
  await expect(page.getByRole("textbox", { name: "API response JSON", exact: true })).toHaveValue("");
  await expect(page.getByRole("textbox", { name: "API method (optional)", exact: true })).toHaveValue("");
  await expect(result).toBeHidden();

  expect(await page.evaluate(() => ({ local: { ...localStorage }, session: { ...sessionStorage }, cookie: document.cookie }))).toEqual(storageBefore);
  expect(await page.evaluate(() => location.search + location.hash)).toBe("");
  expect(requests).toEqual([]);
  expect(logs).toEqual([]);
  expect(failures).toEqual([]);
});

test("keyboard controls, result focus, and narrow screens stay usable", async ({ page }) => {
  const input = page.getByRole("textbox", { name: "API response JSON", exact: true });
  const method = page.getByRole("textbox", { name: "API method (optional)", exact: true });
  const submit = page.getByRole("button", { name: "Classify response", exact: true });
  await input.fill('{"ok":false,"error_code":400,"description":"Bad Request: chat not found"}');
  await input.focus();
  await page.keyboard.press("Tab");
  await expect(method).toBeFocused();
  await page.keyboard.press("Tab");
  await expect(submit).toBeFocused();
  await page.keyboard.press("Enter");
  const result = page.getByRole("region", { name: "Classification result", exact: true });
  await expect(result).toBeFocused();
  await expect(result.locator("#playground-status")).toHaveText("matched");
  expect(await page.evaluate(() => document.documentElement.scrollWidth - innerWidth)).toBeLessThanOrEqual(1);
  expect((await submit.boundingBox())!.height).toBeGreaterThanOrEqual(44);
  await input.fill("{}");
  await expect(result).toBeHidden();
});

test("leaving the page clears transient input", async ({ page }) => {
  await classify(page, { ok: false, error_code: 400, description: "private-example-marker" });
  await page.getByRole("main").getByRole("link", { name: "How matching works", exact: true }).click();
  await page.goBack();
  await expect(page.getByRole("textbox", { name: "API response JSON", exact: true })).toHaveValue("");
  await expect(page.locator("#playground-result")).toBeHidden();
});

test("the guide has a canonical URL and readable search metadata", async ({ page }) => {
  await expect(page).toHaveTitle(/Try a Bot API response/);
  await expect(page.locator('link[rel="canonical"]')).toHaveAttribute("href", "https://errorgram.rmbk.me/playground/");
  await expect(page.locator('meta[name="description"]')).toHaveAttribute("content", /Classify Telegram Bot API error JSON locally/);
  await expect(page.getByRole("heading", { name: "How to use the playground", exact: true })).toBeVisible();
});
