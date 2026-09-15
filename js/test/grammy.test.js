import assert from "node:assert/strict";
import test from "node:test";
import { Bot, BotError, GrammyError, HttpError } from "grammy";
import { catalogue } from "errorgram";
import { enrich, EnrichedGrammyError } from "errorgram/grammy";

const sample = (id) => catalogue.entries.find((entry) => entry.id === id).example;

test("every known condition enriches a real GrammyError without losing its fields", () => {
  for (const entry of catalogue.entries) {
    const payload = { chat_id: 42, text: "Hello" };
    const original = new GrammyError("Request failed", entry.example.response, entry.example.method, payload);
    const before = Object.getOwnPropertyDescriptors(original);
    const result = enrich(original);
    assert.ok(result instanceof EnrichedGrammyError, entry.id);
    assert.ok(result instanceof GrammyError);
    assert.equal(result.id, entry.id);
    assert.equal(result.facts, result.classification.facts);
    assert.equal(result.original, original);
    assert.equal(result.cause, original);
    assert.equal(result.payload, payload);
    assert.equal(result.parameters, original.parameters);
    assert.equal(result.description, original.description);
    assert.equal(result.method, original.method);
    assert.equal(result.message, original.message);
    assert.equal(result.stack, original.stack);
    assert.equal(result.error_code, original.error_code);
    assert.equal(result.ok, false);
    assert.deepEqual(Object.getOwnPropertyDescriptors(original), before);
    assert.equal(enrich(result), result);
  }
});

test("unknown API failures, transport failures and unrelated values pass through", () => {
  const values = [
    new GrammyError("Unknown", { ok: false, error_code: 400, description: "New Telegram error" }, "sendMessage", {}),
    new HttpError("Network failed", new Error("offline")),
    new Error("Application failure"), null, undefined, "failure",
  ];
  for (const value of values) assert.equal(enrich(value), value);
});

test("a real grammY API call produces an enrichable exception with one request", async () => {
  let calls = 0;
  const response = sample("message.not_modified").response;
  const bot = new Bot("123456:TEST_TOKEN", {
    client: {
      fetch: async (url, init) => {
        calls += 1;
        assert.equal(new URL(url).pathname.endsWith("/editMessageText"), true);
        assert.equal(JSON.parse(init.body).text, "Hello");
        return new Response(JSON.stringify(response), { status: 400, headers: { "content-type": "application/json" } });
      },
    },
  });
  let caught;
  try {
    await bot.api.editMessageText(42, 7, "Hello");
  } catch (error) {
    caught = enrich(error);
  }
  assert.ok(caught instanceof EnrichedGrammyError);
  assert.ok(caught instanceof GrammyError);
  assert.equal(caught.id, "message.not_modified");
  assert.equal(caught.method, "editMessageText");
  assert.equal(caught.payload.message_id, 7);
  assert.equal(calls, 1);
});

test("a real grammY transport failure remains outside the catalogue", async () => {
  const network = new Error("Offline for this test");
  const bot = new Bot("123456:TEST_TOKEN", { client: { fetch: async () => { throw network; } } });
  await assert.rejects(bot.api.getMe(), (error) => {
    assert.ok(error instanceof HttpError);
    assert.equal(enrich(error), error);
    assert.equal(error.error, network);
    return true;
  });
});

test("bot.catch callers can enrich the wrapped error without changing context", () => {
  const { response, method } = sample("chat.not_found");
  const original = new GrammyError("Request failed", response, method, { chat_id: 42 });
  const context = { update: { update_id: 17 } };
  const wrapped = new BotError(original, context);
  assert.equal(enrich(wrapped), wrapped);
  assert.equal(enrich(wrapped.error).id, "chat.not_found");
  assert.equal(wrapped.ctx, context);
});

test("adapter reports fields grammY normalizes or reconstructs", () => {
  const { response, method } = sample("request.retry_after");
  const result = enrich(new GrammyError("Request failed", response, method, {}));
  assert.deepEqual(result.classification.facts, { retry_after: 5 });
  assert.deepEqual(result.fidelity, {
    description: "preserved", parameters: "framework_normalized", method: "preserved", response: "reconstructed",
  });
  assert.equal("http_status" in result.classification, false);
});
