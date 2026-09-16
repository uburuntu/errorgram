---
title: "Permissions invalid json · permissions.invalid_json"
description: "The permissions argument is not valid JSON."
slug: "errors/permissions.invalid_json"
editUrl: "https://github.com/uburuntu/errorgram/edit/main/catalogue/errors.json"
sidebar:
  label: "permissions.invalid_json"
---

**Stable ID:** `permissions.invalid_json` · **Evidence:** source derived

The permissions argument is not valid JSON.

This is a request-format error; it does not establish whether the bot has permission to change chat rights.

## When it matches

Every field in a rule must match. Alternative rules are joined with OR.
Codes below are JSON response fields, not inferred HTTP statuses.

- JSON `error_code`: **400**.

Exact description:

```text
Bad Request: can't parse permissions JSON object
```

See [matching rules](/matching/) for parameter precedence
and unknown or ambiguous results.

**Illustrative methods:** `setChatPermissions`, `restrictChatMember`.

## Possible causes

- The supplied permissions argument failed JSON decoding.

## Before deciding what to do

**Application decision:** correct permissions json.
**Repeat request:** after relevant change.

- Serialize permissions as a ChatPermissions object and verify the intended boolean values.

These are application choices. Errorgram does not retry, suppress the error,
or change bot state.

## Facts

This condition adds no extracted facts; `result.facts` is empty.

## Example

Synthetic examples derived from the cited source.

API method: `setChatPermissions`.

```json
{
  "ok": false,
  "error_code": 400,
  "description": "Bad Request: can't parse permissions JSON object"
}
```

### Python

```python
from errorgram import classify

response = {
    "ok": False,
    "error_code": 400,
    "description": "Bad Request: can't parse permissions JSON object",
}
result = classify(response, method='setChatPermissions')

assert result.id == 'permissions.invalid_json'
print(result.entry["summary"])
```

### JavaScript and TypeScript

```ts
import { classify } from "errorgram";

const response = {
  "ok": false,
  "error_code": 400,
  "description": "Bad Request: can't parse permissions JSON object"
};
const result = classify(response, { method: "setChatPermissions" });

if (result.status === "matched" && result.id === "permissions.invalid_json") {
  console.log(result.entry.summary);
}
```

## Framework names

| Integration | Type or ID |
| --- | --- |
| Python | `errorgram.PermissionsInvalidJson` |
| aiogram | `errorgram.aiogram.PermissionsInvalidJson` extends `TelegramBadRequest` |
| grammY | `EnrichedGrammyError` with `classification.id` equal to `permissions.invalid_json` |

Enrichment is explicit and keeps framework catch compatibility.
Follow the [Python and aiogram guide](/python/) or
[JavaScript, TypeScript, and grammY guide](/javascript/).

## Evidence

- [Bot API 10.3 · telegram-bot-api/Client.cpp:12555–12561](https://github.com/tdlib/telegram-bot-api/blob/e3e9dd8e5b3d7ab8537cd5a10dc31d5ffa8f82d1/telegram-bot-api/Client.cpp#L12555-L12561). An explicitly supplied permissions argument is decoded as JSON and rejected here if decoding fails. Revision `e3e9dd8e5b3d7ab8537cd5a10dc31d5ffa8f82d1`.
- [Bot API 10.3 · telegram-bot-api/Client.cpp:13800–13803](https://github.com/tdlib/telegram-bot-api/blob/e3e9dd8e5b3d7ab8537cd5a10dc31d5ffa8f82d1/telegram-bot-api/Client.cpp#L13800-L13803). Method validation errors are passed to the response normalizer. Revision `e3e9dd8e5b3d7ab8537cd5a10dc31d5ffa8f82d1`.
- [Bot API 10.3 · telegram-bot-api/Client.cpp:165–205](https://github.com/tdlib/telegram-bot-api/blob/e3e9dd8e5b3d7ab8537cd5a10dc31d5ffa8f82d1/telegram-bot-api/Client.cpp#L165-L205). Adds the code-specific prefix and lowercases only the initial character of ordinary messages. Revision `e3e9dd8e5b3d7ab8537cd5a10dc31d5ffa8f82d1`.

Source references identify the reviewed revision, not the first release
that introduced this response.

## Data and versions

Catalogue `0.1.0` · schema `1.0.0` · reviewed 2026-09-16.

[Markdown](/errors/permissions.invalid_json.md) · [Condition JSON](/errors/permissions.invalid_json.json) · [Full catalogue and sources](/catalogue.json) · [JSON Schema](/schema.json)
