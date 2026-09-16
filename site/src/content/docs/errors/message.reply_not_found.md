---
title: "Message reply not found · message.reply_not_found"
description: "The message being replied to could not be resolved."
slug: "errors/message.reply_not_found"
editUrl: "https://github.com/uburuntu/errorgram/edit/main/catalogue/errors.json"
sidebar:
  label: "message.reply_not_found"
---

**Stable ID:** `message.reply_not_found` · **Evidence:** source derived

The message being replied to could not be resolved.

The response does not prove that the message was deleted. Reply settings and the referenced chat also affect this lookup.

## When it matches

Every field in a rule must match. Alternative rules are joined with OR.
Codes below are JSON response fields, not inferred HTTP statuses.

- JSON `error_code`: **400**.

Exact description:

```text
Bad Request: message to be replied not found
```

See [matching rules](/matching/) for parameter precedence
and unknown or ambiguous results.

**Illustrative methods:** `sendMessage`, `sendPhoto`.

## Possible causes

- The bot cannot access the referenced message.
- A reply-message lookup failed and its original error was replaced.

## Before deciding what to do

**Application decision:** inspect reply target and access.
**Repeat request:** after relevant change.

- Verify the reply message and chat; omit the reply only if the application permits sending without it.

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
  "error_code": 400,
  "description": "Bad Request: message to be replied not found"
}
```

### Python

```python
from errorgram import classify

response = {
    "ok": False,
    "error_code": 400,
    "description": "Bad Request: message to be replied not found",
}
result = classify(response, method='sendMessage')

assert result.id == 'message.reply_not_found'
print(result.entry["summary"])
```

### JavaScript and TypeScript

```ts
import { classify } from "errorgram";

const response = {
  "ok": false,
  "error_code": 400,
  "description": "Bad Request: message to be replied not found"
};
const result = classify(response, { method: "sendMessage" });

if (result.status === "matched" && result.id === "message.reply_not_found") {
  console.log(result.entry.summary);
}
```

## Framework names

| Integration | Type or ID |
| --- | --- |
| Python | `errorgram.MessageReplyNotFound` |
| aiogram | `errorgram.aiogram.MessageReplyNotFound` extends `TelegramBadRequest` |
| grammY | `EnrichedGrammyError` with `classification.id` equal to `message.reply_not_found` |

Enrichment is explicit and keeps framework catch compatibility.
Follow the [Python and aiogram guide](/python/) or
[JavaScript, TypeScript, and grammY guide](/javascript/).

## Evidence

- [Bot API 10.3 · telegram-bot-api/Client.cpp:9190–9198](https://github.com/tdlib/telegram-bot-api/blob/e3e9dd8e5b3d7ab8537cd5a10dc31d5ffa8f82d1/telegram-bot-api/Client.cpp#L9190-L9198). Reply lookup uses this fallback for unavailable access or a failed required-message lookup. Revision `e3e9dd8e5b3d7ab8537cd5a10dc31d5ffa8f82d1`.
- [Bot API 10.3 · telegram-bot-api/Client.cpp:7390–7399](https://github.com/tdlib/telegram-bot-api/blob/e3e9dd8e5b3d7ab8537cd5a10dc31d5ffa8f82d1/telegram-bot-api/Client.cpp#L7390-L7399). allow\_sending\_without\_reply can permit an empty result instead of failing. Revision `e3e9dd8e5b3d7ab8537cd5a10dc31d5ffa8f82d1`.
- [Bot API 10.3 · telegram-bot-api/Client.cpp:85–108](https://github.com/tdlib/telegram-bot-api/blob/e3e9dd8e5b3d7ab8537cd5a10dc31d5ffa8f82d1/telegram-bot-api/Client.cpp#L85-L108). The fallback replaces only errors normalized to code 400. Revision `e3e9dd8e5b3d7ab8537cd5a10dc31d5ffa8f82d1`.
- [Bot API 10.3 · telegram-bot-api/Client.cpp:165–205](https://github.com/tdlib/telegram-bot-api/blob/e3e9dd8e5b3d7ab8537cd5a10dc31d5ffa8f82d1/telegram-bot-api/Client.cpp#L165-L205). Adds the code-specific prefix and lowercases only the initial character of ordinary messages. Revision `e3e9dd8e5b3d7ab8537cd5a10dc31d5ffa8f82d1`.

Source references identify the reviewed revision, not the first release
that introduced this response.

## Data and versions

Catalogue `0.1.0` · schema `1.0.0` · reviewed 2026-09-16.

[Markdown](/errors/message.reply_not_found.md) · [Condition JSON](/errors/message.reply_not_found.json) · [Full catalogue and sources](/catalogue.json) · [JSON Schema](/schema.json)
