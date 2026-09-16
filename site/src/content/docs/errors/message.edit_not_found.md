---
title: "Message edit not found · message.edit_not_found"
description: "The message to edit could not be resolved."
slug: "errors/message.edit_not_found"
editUrl: "https://github.com/uburuntu/errorgram/edit/main/catalogue/errors.json"
sidebar:
  label: "message.edit_not_found"
---

**Stable ID:** `message.edit_not_found` · **Evidence:** observed

The message to edit could not be resolved.

The response does not distinguish a deleted message from an incorrect identifier, missing access or a masked lookup error.

## When it matches

Every field in a rule must match. Alternative rules are joined with OR.
Codes below are JSON response fields, not inferred HTTP statuses.

- JSON `error_code`: **400**.

Exact description:

```text
Bad Request: message to edit not found
```

See [matching rules](/matching/) for parameter precedence
and unknown or ambiguous results.

**Illustrative methods:** `editMessageText`, `editMessageCaption`, `editMessageReplyMarkup`.

## Possible causes

- The message identifier is missing or nonpositive.
- The bot cannot access messages in the chat.
- A message lookup failed and its original error was replaced.

## Before deciding what to do

**Application decision:** inspect message target and access.
**Repeat request:** after relevant change.

- Check the chat and message identifiers together, then confirm the bot can access the target message.

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
  "description": "Bad Request: message to edit not found"
}
```

### Python

```python
from errorgram import classify

response = {
    "ok": False,
    "error_code": 400,
    "description": "Bad Request: message to edit not found",
}
result = classify(response, method='editMessageText')

assert result.id == 'message.edit_not_found'
print(result.entry["summary"])
```

### JavaScript and TypeScript

```ts
import { classify } from "errorgram";

const response = {
  "ok": false,
  "error_code": 400,
  "description": "Bad Request: message to edit not found"
};
const result = classify(response, { method: "editMessageText" });

if (result.status === "matched" && result.id === "message.edit_not_found") {
  console.log(result.entry.summary);
}
```

## Framework names

| Integration | Type or ID |
| --- | --- |
| Python | `errorgram.MessageEditNotFound` |
| aiogram | `errorgram.aiogram.MessageEditNotFound` extends `TelegramBadRequest` |
| grammY | `EnrichedGrammyError` with `classification.id` equal to `message.edit_not_found` |

Enrichment is explicit and keeps framework catch compatibility.
Follow the [Python and aiogram guide](/python/) or
[JavaScript, TypeScript, and grammY guide](/javascript/).

## Evidence

- [Recorded observation](https://github.com/uburuntu/errorgram/blob/4314ac1f9d29d105b10e9b537a7643cc65d097aa/observations/2026-09-16.json). Editing the test bot’s own message after confirmed deletion returned this description. Accessed 2026-09-16.
- [Bot API 10.3 · telegram-bot-api/Client.cpp:14694–14700](https://github.com/tdlib/telegram-bot-api/blob/e3e9dd8e5b3d7ab8537cd5a10dc31d5ffa8f82d1/telegram-bot-api/Client.cpp#L14694-L14700). The editMessageText path checks the target as "message to edit". Revision `e3e9dd8e5b3d7ab8537cd5a10dc31d5ffa8f82d1`.
- [Bot API 10.3 · telegram-bot-api/Client.cpp:9084–9102](https://github.com/tdlib/telegram-bot-api/blob/e3e9dd8e5b3d7ab8537cd5a10dc31d5ffa8f82d1/telegram-bot-api/Client.cpp#L9084-L9102). Missing identifiers and unavailable message access produce this operation-specific fallback. Revision `e3e9dd8e5b3d7ab8537cd5a10dc31d5ffa8f82d1`.
- [Bot API 10.3 · telegram-bot-api/Client.cpp:7390–7399](https://github.com/tdlib/telegram-bot-api/blob/e3e9dd8e5b3d7ab8537cd5a10dc31d5ffa8f82d1/telegram-bot-api/Client.cpp#L7390-L7399). Failed lookups use the same fallback when an empty result is not allowed. Revision `e3e9dd8e5b3d7ab8537cd5a10dc31d5ffa8f82d1`.
- [Bot API 10.3 · telegram-bot-api/Client.cpp:85–108](https://github.com/tdlib/telegram-bot-api/blob/e3e9dd8e5b3d7ab8537cd5a10dc31d5ffa8f82d1/telegram-bot-api/Client.cpp#L85-L108). The fallback replaces only errors normalized to code 400. Revision `e3e9dd8e5b3d7ab8537cd5a10dc31d5ffa8f82d1`.
- [Bot API 10.3 · telegram-bot-api/Client.cpp:165–205](https://github.com/tdlib/telegram-bot-api/blob/e3e9dd8e5b3d7ab8537cd5a10dc31d5ffa8f82d1/telegram-bot-api/Client.cpp#L165-L205). Adds the code-specific prefix and lowercases only the initial character of ordinary messages. Revision `e3e9dd8e5b3d7ab8537cd5a10dc31d5ffa8f82d1`.

Source references identify the reviewed revision, not the first release
that introduced this response.

## Data and versions

Catalogue `0.1.0` · schema `1.0.0` · reviewed 2026-09-16.

[Markdown](/errors/message.edit_not_found.md) · [Condition JSON](/errors/message.edit_not_found.json) · [Full catalogue and sources](/catalogue.json) · [JSON Schema](/schema.json)
