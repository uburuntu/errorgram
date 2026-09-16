---
title: "Permissions not object · permissions.not_object"
description: "The permissions value is not a JSON object."
slug: "errors/permissions.not_object"
editUrl: "https://github.com/uburuntu/errorgram/edit/main/catalogue/errors.json"
sidebar:
  label: "permissions.not_object"
---

**Stable ID:** `permissions.not_object` · **Evidence:** source derived

The permissions value is not a JSON object.

This validates only the top-level shape, not individual rights or the bot’s authority to change them.

## When it matches

Every field in a rule must match. Alternative rules are joined with OR.
Codes below are JSON response fields, not inferred HTTP statuses.

- JSON `error_code`: **400**.

Exact description:

```text
Bad Request: object expected as permissions
```

See [matching rules](/matching/) for parameter precedence
and unknown or ambiguous results.

**Illustrative methods:** `setChatPermissions`, `restrictChatMember`.

## Possible causes

- The permissions argument decoded to an array, scalar, or null instead of an object.

## Before deciding what to do

**Application decision:** correct permissions shape.
**Repeat request:** after relevant change.

- Provide a ChatPermissions object with the intended rights, then check the operation’s access requirements.

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
  "description": "Bad Request: object expected as permissions"
}
```

### Python

```python
from errorgram import classify

response = {
    "ok": False,
    "error_code": 400,
    "description": "Bad Request: object expected as permissions",
}
result = classify(response, method='setChatPermissions')

assert result.id == 'permissions.not_object'
print(result.entry["summary"])
```

### JavaScript and TypeScript

```ts
import { classify } from "errorgram";

const response = {
  "ok": false,
  "error_code": 400,
  "description": "Bad Request: object expected as permissions"
};
const result = classify(response, { method: "setChatPermissions" });

if (result.status === "matched" && result.id === "permissions.not_object") {
  console.log(result.entry.summary);
}
```

## Framework names

| Integration | Type or ID |
| --- | --- |
| Python | `errorgram.PermissionsNotObject` |
| aiogram | `errorgram.aiogram.PermissionsNotObject` extends `TelegramBadRequest` |
| grammY | `EnrichedGrammyError` with `classification.id` equal to `permissions.not_object` |

Enrichment is explicit and keeps framework catch compatibility.
Follow the [Python and aiogram guide](/python/) or
[JavaScript, TypeScript, and grammY guide](/javascript/).

## Evidence

- [Bot API 10.3 · telegram-bot-api/Client.cpp:12564–12566](https://github.com/tdlib/telegram-bot-api/blob/e3e9dd8e5b3d7ab8537cd5a10dc31d5ffa8f82d1/telegram-bot-api/Client.cpp#L12564-L12566). Decoded permissions must have object type. Revision `e3e9dd8e5b3d7ab8537cd5a10dc31d5ffa8f82d1`.
- [Bot API 10.3 · telegram-bot-api/Client.cpp:13800–13803](https://github.com/tdlib/telegram-bot-api/blob/e3e9dd8e5b3d7ab8537cd5a10dc31d5ffa8f82d1/telegram-bot-api/Client.cpp#L13800-L13803). Method validation errors are passed to the response normalizer. Revision `e3e9dd8e5b3d7ab8537cd5a10dc31d5ffa8f82d1`.
- [Bot API 10.3 · telegram-bot-api/Client.cpp:165–205](https://github.com/tdlib/telegram-bot-api/blob/e3e9dd8e5b3d7ab8537cd5a10dc31d5ffa8f82d1/telegram-bot-api/Client.cpp#L165-L205). Adds the code-specific prefix and lowercases only the initial character of ordinary messages. Revision `e3e9dd8e5b3d7ab8537cd5a10dc31d5ffa8f82d1`.

Source references identify the reviewed revision, not the first release
that introduced this response.

## Data and versions

Catalogue `0.1.0` · schema `1.0.0` · reviewed 2026-09-16.

[Markdown](/errors/permissions.not_object.md) · [Condition JSON](/errors/permissions.not_object.json) · [Full catalogue and sources](/catalogue.json) · [JSON Schema](/schema.json)
