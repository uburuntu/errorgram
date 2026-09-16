---
title: "Auth invalid token format · auth.invalid_token_format"
description: "The server rejected the token during local validation."
slug: "errors/auth.invalid_token_format"
editUrl: "https://github.com/uburuntu/errorgram/edit/main/catalogue/errors.json"
sidebar:
  label: "auth.invalid_token_format"
---

**Stable ID:** `auth.invalid_token_format` · **Evidence:** source derived

The server rejected the token during local validation.

This signature is narrower than generic Unauthorized. Other malformed-token paths may produce different codes.

## When it matches

Every field in a rule must match. Alternative rules are joined with OR.
Codes below are JSON response fields, not inferred HTTP statuses.

- JSON `error_code`: **401**.

Exact description:

```text
Unauthorized: invalid token specified
```

See [matching rules](/matching/) for parameter precedence
and unknown or ambiguous results.

**Illustrative methods:** `getMe`.

## Possible causes

- A locally checked token structure or numeric identifier constraint failed.

## Before deciding what to do

**Application decision:** correct token configuration.
**Repeat request:** after configuration change.

- Verify the configured token without placing it in logs or inventory submissions.

These are application choices. Errorgram does not retry, suppress the error,
or change bot state.

## Facts

This condition adds no extracted facts; `result.facts` is empty.

## Example

Synthetic examples derived from the cited source.

API method: `getMe`.

```json
{
  "ok": false,
  "error_code": 401,
  "description": "Unauthorized: invalid token specified"
}
```

### Python

```python
from errorgram import classify

response = {
    "ok": False,
    "error_code": 401,
    "description": "Unauthorized: invalid token specified",
}
result = classify(response, method='getMe')

assert result.id == 'auth.invalid_token_format'
print(result.entry["summary"])
```

### JavaScript and TypeScript

```ts
import { classify } from "errorgram";

const response = {
  "ok": false,
  "error_code": 401,
  "description": "Unauthorized: invalid token specified"
};
const result = classify(response, { method: "getMe" });

if (result.status === "matched" && result.id === "auth.invalid_token_format") {
  console.log(result.entry.summary);
}
```

## Framework names

| Integration | Type or ID |
| --- | --- |
| Python | `errorgram.AuthInvalidTokenFormat` |
| aiogram | `errorgram.aiogram.AuthInvalidTokenFormat` extends `TelegramUnauthorizedError` |
| grammY | `EnrichedGrammyError` with `classification.id` equal to `auth.invalid_token_format` |

Enrichment is explicit and keeps framework catch compatibility.
Follow the [Python and aiogram guide](/python/) or
[JavaScript, TypeScript, and grammY guide](/javascript/).

## Evidence

- [Bot API 10.3 · telegram-bot-api/ClientManager.cpp:73–84](https://github.com/tdlib/telegram-bot-api/blob/e3e9dd8e5b3d7ab8537cd5a10dc31d5ffa8f82d1/telegram-bot-api/ClientManager.cpp#L73-L84). Two local checks return this exact response; the intervening check can return 421. Revision `e3e9dd8e5b3d7ab8537cd5a10dc31d5ffa8f82d1`.

Source references identify the reviewed revision, not the first release
that introduced this response.

## Data and versions

Catalogue `0.1.0` · schema `1.0.0` · reviewed 2026-09-16.

[Markdown](/errors/auth.invalid_token_format.md) · [Condition JSON](/errors/auth.invalid_token_format.json) · [Full catalogue and sources](/catalogue.json) · [JSON Schema](/schema.json)
