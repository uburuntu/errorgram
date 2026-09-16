---
title: "User deactivated · user.deactivated"
description: "Telegram rejected the operation because the user is deactivated."
slug: "errors/user.deactivated"
editUrl: "https://github.com/uburuntu/errorgram/edit/main/catalogue/errors.json"
sidebar:
  label: "user.deactivated"
---

**Stable ID:** `user.deactivated` · **Evidence:** source derived

Telegram rejected the operation because the user is deactivated.

The response establishes the current rejection; it does not expose account history or a replacement recipient.

## When it matches

Every field in a rule must match. Alternative rules are joined with OR.
Codes below are JSON response fields, not inferred HTTP statuses.

- JSON `error_code`: **403**.

Exact description:

```text
Forbidden: user is deactivated
```

See [matching rules](/matching/) for parameter precedence
and unknown or ambiguous results.

**Illustrative methods:** `sendMessage`, `editMessageText`.

## Possible causes

- The target private-chat user is marked deleted.
- Telegram reported that the target account is deactivated.

## Before deciding what to do

**Application decision:** suspend operations for recipient.
**Repeat request:** after access change.

- Stop repeating this operation for the recipient unless there is evidence that the target or its availability changed.

These are application choices. Errorgram does not retry, suppress the error,
or change bot state.

## Facts

This condition adds no extracted facts; `result.facts` is empty.

## Example

Synthetic examples derived from the cited source.

API method: `sendMessage`.

```json
{
  "ok": false,
  "error_code": 403,
  "description": "Forbidden: user is deactivated"
}
```

### Python

```python
from errorgram import classify

response = {
    "ok": False,
    "error_code": 403,
    "description": "Forbidden: user is deactivated",
}
result = classify(response, method='sendMessage')

assert result.id == 'user.deactivated'
print(result.entry["summary"])
```

### JavaScript and TypeScript

```ts
import { classify } from "errorgram";

const response = {
  "ok": false,
  "error_code": 403,
  "description": "Forbidden: user is deactivated"
};
const result = classify(response, { method: "sendMessage" });

if (result.status === "matched" && result.id === "user.deactivated") {
  console.log(result.entry.summary);
}
```

## Framework names

| Integration | Type or ID |
| --- | --- |
| Python | `errorgram.UserDeactivated` |
| aiogram | `errorgram.aiogram.UserDeactivated` extends `TelegramForbiddenError` |
| grammY | `EnrichedGrammyError` with `classification.id` equal to `user.deactivated` |

Enrichment is explicit and keeps framework catch compatibility.
Follow the [Python and aiogram guide](/python/) or
[JavaScript, TypeScript, and grammY guide](/javascript/).

## Evidence

- [Bot API 10.3 · telegram-bot-api/Client.cpp:8803–8807](https://github.com/tdlib/telegram-bot-api/blob/e3e9dd8e5b3d7ab8537cd5a10dc31d5ffa8f82d1/telegram-bot-api/Client.cpp#L8803-L8807). Edit or write access to a deleted private-chat user is rejected directly with code 403. Revision `e3e9dd8e5b3d7ab8537cd5a10dc31d5ffa8f82d1`.
- [Bot API 10.3 · telegram-bot-api/Client.cpp:124–126](https://github.com/tdlib/telegram-bot-api/blob/e3e9dd8e5b3d7ab8537cd5a10dc31d5ffa8f82d1/telegram-bot-api/Client.cpp#L124-L126). INPUT\_USER\_DEACTIVATED also maps to this exact 403 response. Revision `e3e9dd8e5b3d7ab8537cd5a10dc31d5ffa8f82d1`.
- [Bot API 10.3 · telegram-bot-api/Client.cpp:165–205](https://github.com/tdlib/telegram-bot-api/blob/e3e9dd8e5b3d7ab8537cd5a10dc31d5ffa8f82d1/telegram-bot-api/Client.cpp#L165-L205). Adds the code-specific prefix and lowercases only the initial character of ordinary messages. Revision `e3e9dd8e5b3d7ab8537cd5a10dc31d5ffa8f82d1`.

Source references identify the reviewed revision, not the first release
that introduced this response.

## Data and versions

Catalogue `0.1.0` · schema `1.0.0` · reviewed 2026-09-16.

[Markdown](/errors/user.deactivated.md) · [Condition JSON](/errors/user.deactivated.json) · [Full catalogue and sources](/catalogue.json) · [JSON Schema](/schema.json)
