---
title: "Message identifier missing · message.identifier_missing"
description: "The request did not specify a message identifier for the selected operation."
slug: "errors/message.identifier_missing"
editUrl: "https://github.com/uburuntu/errorgram/edit/main/catalogue/errors.json"
sidebar:
  label: "message.identifier_missing"
---

**Stable ID:** `message.identifier_missing` · **Evidence:** source derived

The request did not specify a message identifier for the selected operation.

This signature does not diagnose all missing message\_id arguments; a chat-based lookup may return an operation-specific not-found error.

## When it matches

Every field in a rule must match. Alternative rules are joined with OR.
Codes below are JSON response fields, not inferred HTTP statuses.

- JSON `error_code`: **400**.

Exact description:

```text
Bad Request: message identifier is not specified
```

See [matching rules](/matching/) for parameter precedence
and unknown or ambiguous results.

**Illustrative methods:** `editMessageText`, `editMessageCaption`.

## Possible causes

- The inline-message path was selected without a nonempty inline\_message\_id.

## Before deciding what to do

**Application decision:** supply message target.
**Repeat request:** after relevant change.

- Supply the intended inline\_message\_id or the appropriate chat\_id and message\_id pair.

These are application choices. Errorgram does not retry, suppress the error,
or change bot state.

## Facts

This condition adds no extracted facts; `result.facts` is empty.

## Example

Synthetic examples derived from the cited source.

API method: `editMessageText`.

```json
{
  "ok": false,
  "error_code": 400,
  "description": "Bad Request: message identifier is not specified"
}
```

### Python

```python
from errorgram import classify

response = {
    "ok": False,
    "error_code": 400,
    "description": "Bad Request: message identifier is not specified",
}
result = classify(response, method='editMessageText')

assert result.id == 'message.identifier_missing'
print(result.entry["summary"])
```

### JavaScript and TypeScript

```ts
import { classify } from "errorgram";

const response = {
  "ok": false,
  "error_code": 400,
  "description": "Bad Request: message identifier is not specified"
};
const result = classify(response, { method: "editMessageText" });

if (result.status === "matched" && result.id === "message.identifier_missing") {
  console.log(result.entry.summary);
}
```

## Framework names

| Integration | Type or ID |
| --- | --- |
| Python | `errorgram.MessageIdentifierMissing` |
| aiogram | `errorgram.aiogram.MessageIdentifierMissing` extends `TelegramBadRequest` |
| grammY | `EnrichedGrammyError` with `classification.id` equal to `message.identifier_missing` |

Enrichment is explicit and keeps framework catch compatibility.
Follow the [Python and aiogram guide](/python/) or
[JavaScript, TypeScript, and grammY guide](/javascript/).

## Evidence

- [Bot API 10.3 · telegram-bot-api/Client.cpp:13540–13545](https://github.com/tdlib/telegram-bot-api/blob/e3e9dd8e5b3d7ab8537cd5a10dc31d5ffa8f82d1/telegram-bot-api/Client.cpp#L13540-L13545). The inline-message identifier helper rejects an empty argument. Revision `e3e9dd8e5b3d7ab8537cd5a10dc31d5ffa8f82d1`.
- [Bot API 10.3 · telegram-bot-api/Client.cpp:14659–14665](https://github.com/tdlib/telegram-bot-api/blob/e3e9dd8e5b3d7ab8537cd5a10dc31d5ffa8f82d1/telegram-bot-api/Client.cpp#L14659-L14665). Editing takes this path when chat\_id is empty and the parsed message\_id is zero. Revision `e3e9dd8e5b3d7ab8537cd5a10dc31d5ffa8f82d1`.
- [Bot API 10.3 · telegram-bot-api/Client.cpp:13800–13803](https://github.com/tdlib/telegram-bot-api/blob/e3e9dd8e5b3d7ab8537cd5a10dc31d5ffa8f82d1/telegram-bot-api/Client.cpp#L13800-L13803). Method validation errors are passed to the response normalizer. Revision `e3e9dd8e5b3d7ab8537cd5a10dc31d5ffa8f82d1`.
- [Bot API 10.3 · telegram-bot-api/Client.cpp:165–205](https://github.com/tdlib/telegram-bot-api/blob/e3e9dd8e5b3d7ab8537cd5a10dc31d5ffa8f82d1/telegram-bot-api/Client.cpp#L165-L205). Adds the code-specific prefix and lowercases only the initial character of ordinary messages. Revision `e3e9dd8e5b3d7ab8537cd5a10dc31d5ffa8f82d1`.

Source references identify the reviewed revision, not the first release
that introduced this response.

## Data and versions

Catalogue `0.1.0` · schema `1.0.0` · reviewed 2026-09-16.

[Markdown](/errors/message.identifier_missing.md) · [Condition JSON](/errors/message.identifier_missing.json) · [Full catalogue and sources](/catalogue.json) · [JSON Schema](/schema.json)
