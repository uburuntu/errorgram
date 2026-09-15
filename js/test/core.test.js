import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import test from "node:test";
import { catalogue, catalogueVersion, classify } from "errorgram";

const fixtures = JSON.parse(readFileSync(new URL("../../fixtures/conformance.json", import.meta.url), "utf8"));

for (const fixture of fixtures.cases) {
  test(`shared: ${fixture.name}`, () => {
    const result = classify(fixture.response, fixture.method === undefined ? {} : { method: fixture.method });
    const actual = { status: result.status };
    if ("id" in result) actual.id = result.id;
    if (fixture.expected.facts !== undefined) actual.facts = result.facts;
    if (fixture.expected.candidates !== undefined) actual.candidates = result.candidates;
    assert.deepEqual(actual, fixture.expected);
    assert.equal(result.response, fixture.response);
    assert.equal(result.catalogue_version, catalogueVersion);
  });
}

const body = (description = "Bad Request: chat not found", overrides = {}) => ({ ok: false, error_code: 400, description, ...overrides });
const custom = (...entries) => ({ schema_version: "1.0.0", catalogue_version: "test", matching: { exclusive_parameter_groups: [] }, entries });
const entry = (id, ...match_any) => ({ id, category: "test", summary: "Test condition.", match_any });

test("every source example resolves to its own stable ID", () => {
  for (const entry of catalogue.entries) {
    const result = classify(entry.example.response, { method: entry.example.method });
    assert.equal(result.status, "matched", entry.id);
    assert.equal(result.id, entry.id);
    assert.equal(result.entry, entry);
    assert.deepEqual(result.candidates, []);
  }
});

test("bundled metadata and original response cannot change during classification", () => {
  const response = Object.freeze(body(undefined, { parameters: Object.freeze({ future_hint: "keep me" }) }));
  const result = classify(response);
  assert.equal(result.response, response);
  assert.equal(result.response.parameters.future_hint, "keep me");
  assert.throws(() => { catalogue.entries[0].summary = "Changed"; }, TypeError);
  assert.throws(() => { catalogue.entries[0].match_any[0].error_code = 401; }, TypeError);
});

test("JavaScript-only invalid values are not API responses", () => {
  for (const value of [undefined, NaN, new Error("no response"), new Date(), () => {}, body(undefined, { error_code: Infinity }), body(undefined, { parameters: undefined }), Object.assign(Object.create({ inherited: true }), body())]) {
    const result = classify(value);
    assert.equal(result.status, "not_api_error");
    assert.equal(result.response, value);
    assert.equal("id" in result, false);
  }
  assert.equal(classify(Object.assign(Object.create(null), body())).status, "matched");
});

test("overlapping signatures report all candidates without depending on entry order", () => {
  const rules = { error_code: 400, description_exact: "Bad Request: chat not found" };
  const entries = [entry("test.second", rules), entry("test.first", rules)];
  for (const ordered of [entries, [...entries].reverse()]) {
    const result = classify(body(), { catalogue: custom(...ordered) });
    assert.equal(result.status, "ambiguous");
    assert.deepEqual(result.candidates, ["test.first", "test.second"]);
    assert.equal("id" in result, false);
  }
});

test("missing method context cannot silently select a competing generic condition", () => {
  const rule = { error_code: 400, description_exact: "Bad Request: chat not found" };
  const catalogue = custom(entry("test.generic", rule), entry("test.file", { ...rule, method: "getfile" }));
  const absent = classify(body(), { catalogue });
  assert.equal(absent.status, "insufficient_context");
  assert.deepEqual(absent.candidates, ["test.file", "test.generic"]);
  assert.equal(classify(body(), { catalogue, method: "getFile" }).status, "ambiguous");
  assert.equal(classify(body(), { catalogue, method: "sendMessage" }).id, "test.generic");
});

test("a complete alternative resolves missing context for the same ID", () => {
  const rule = { error_code: 400, description_exact: "Bad Request: chat not found" };
  const catalogue = custom(entry("test.same", { ...rule, method: "getfile" }, rule));
  assert.equal(classify(body(), { catalogue }).id, "test.same");
});

test("structured evidence takes precedence over an overlapping text signature", () => {
  const catalogue = custom(
    entry("test.text", { error_code: 400, description_exact: "Bad Request: chat not found" }),
    entry("test.structured", { error_code: 400, required_parameters: { replacement: "nonzero_integer" } }),
  );
  const result = classify(body(undefined, { parameters: { replacement: -42 } }), { catalogue });
  assert.equal(result.id, "test.structured");
  assert.deepEqual(result.facts, { replacement: -42 });
});

test("invalid or code-incompatible recovery fields prevent text fallback", () => {
  for (const value of [0, true, "5", 1.5, NaN, Infinity, Number.MAX_SAFE_INTEGER + 1, -1]) {
    assert.equal(classify(body(undefined, { parameters: { retry_after: value } })).status, "unknown");
  }
  assert.equal(classify(body(undefined, { parameters: { retry_after: 5 } })).status, "unknown");
});

test("a parameter accepts any declared kind without depending on entry order", () => {
  const entries = [
    entry("test.nonzero", { error_code: 400, required_parameters: { n: "nonzero_integer" } }),
    entry("test.positive", { error_code: 400, required_parameters: { n: "positive_integer" } }),
  ];
  for (const ordered of [entries, [...entries].reverse()]) {
    const catalogue = custom(...ordered);
    const negative = classify(body(undefined, { parameters: { n: -5 } }), { catalogue });
    assert.equal(negative.status, "matched");
    assert.equal(negative.id, "test.nonzero");
    assert.deepEqual(negative.facts, { n: -5 });
    const positive = classify(body(undefined, { parameters: { n: 5 } }), { catalogue });
    assert.equal(positive.status, "ambiguous");
    assert.deepEqual(positive.candidates, ["test.nonzero", "test.positive"]);
    assert.equal(classify(body(undefined, { parameters: { n: 0 } }), { catalogue }).status, "unknown");
  }
});

test("template captures and parameters with the same name must agree", () => {
  const catalogue = custom(entry("test.shared_fact", {
    error_code: 400,
    description_template: "Bad Request: retry after {n}",
    capture_types: { n: "positive_integer" },
    required_parameters: { n: "positive_integer" },
  }));
  const agreed = classify(body("Bad Request: retry after 5", { parameters: { n: 5 } }), { catalogue });
  assert.equal(agreed.id, "test.shared_fact");
  assert.deepEqual(agreed.facts, { n: 5 });
  const conflict = classify(body("Bad Request: retry after 5", { parameters: { n: 9 } }), { catalogue });
  assert.equal(conflict.status, "unknown");
  assert.deepEqual(conflict.facts, {});
});

test("template literals are escaped and captures are safe integers", () => {
  const catalogue = custom(entry("test.template", {
    error_code: 400,
    description_template: "Bad Request: size.+ [{size_bytes}]?",
    capture_types: { size_bytes: "positive_integer" },
  }));
  assert.deepEqual(classify(body("Bad Request: size.+ [42]?"), { catalogue }).facts, { size_bytes: 42 });
  for (const description of ["Bad Request: sizeXXX [42]?", "Bad Request: size.+ [42]?\n", "Bad Request: size.+ [+42]?", "Bad Request: size.+ [0]?", "Bad Request: size.+ [9007199254740992]?"]) {
    assert.equal(classify(body(description), { catalogue }).status, "unknown", description);
  }
});

test("method matching folds ASCII case only", () => {
  const response = body("Bad Request: file is too big");
  for (const method of ["getfile", "getFile", "GETFILE"]) assert.equal(classify(response, { method }).id, "file.download_too_large");
  assert.equal(classify(response, { method: "getFİle" }).status, "unknown");
  assert.deepEqual(classify(response, { method: "getFile" }).facts, {});
});

test("unknown signatures retain all original fields without inventing a condition", () => {
  const response = body("Bad Request: a future server description", { extra: { opaque: true } });
  const result = classify(response);
  assert.equal(result.status, "unknown");
  assert.equal(result.response, response);
  assert.deepEqual(result.facts, {});
  assert.deepEqual(result.candidates, []);
  assert.equal("id" in result, false);
});
