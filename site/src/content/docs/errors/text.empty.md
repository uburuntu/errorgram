---
title: "Text empty · text.empty"
description: "The message text is empty."
slug: "errors/text.empty"
editUrl: "https://github.com/uburuntu/errorgram/edit/main/catalogue/errors.json"
sidebar:
  label: "text.empty"
---

**Stable ID:** `text.empty` · **Evidence:** observed

The message text is empty.

This validates the message text input; it does not establish a rule for optional media captions.

## When it matches

Every field in a rule must match. Alternative rules are joined with OR.
Codes below are JSON response fields, not inferred HTTP statuses.

- JSON `error_code`: **400**.

Exact description:

```text
Bad Request: message text is empty
```

See [matching rules](/matching/) for parameter precedence
and unknown or ambiguous results.

**Illustrative methods:** `sendMessage`, `editMessageText`.

## Possible causes

- The text argument is absent or empty.

## Before deciding what to do

**Application decision:** supply message text.
**Repeat request:** after relevant change.

- Provide nonempty text appropriate for the selected method.

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
  "description": "Bad Request: message text is empty"
}
```

### Python

```python
from errorgram import classify

response = {
    "ok": False,
    "error_code": 400,
    "description": "Bad Request: message text is empty",
}
result = classify(response, method='sendMessage')

assert result.id == 'text.empty'
print(result.entry["summary"])
```

### JavaScript and TypeScript

```ts
import { classify } from "errorgram";

const response = {
  "ok": false,
  "error_code": 400,
  "description": "Bad Request: message text is empty"
};
const result = classify(response, { method: "sendMessage" });

if (result.status === "matched" && result.id === "text.empty") {
  console.log(result.entry.summary);
}
```

## Framework names

| Integration | Type or ID |
| --- | --- |
| Python | `errorgram.TextEmpty` |
| aiogram | `errorgram.aiogram.TextEmpty` extends `TelegramBadRequest` |
| grammY | `EnrichedGrammyError` with `classification.id` equal to `text.empty` |

Enrichment is explicit and keeps framework catch compatibility.
Follow the [Python and aiogram guide](/python/) or
[JavaScript, TypeScript, and grammY guide](/javascript/).

## Evidence

- [Recorded observation](https://github.com/uburuntu/errorgram/blob/4314ac1f9d29d105b10e9b537a7643cc65d097aa/observations/2026-09-16.json). sendMessage with empty text returned this description. Accessed 2026-09-16.
- [Bot API 10.3 · telegram-bot-api/Client.cpp:12039–12052](https://github.com/tdlib/telegram-bot-api/blob/e3e9dd8e5b3d7ab8537cd5a10dc31d5ffa8f82d1/telegram-bot-api/Client.cpp#L12039-L12052). Text-message construction rejects empty text before formatting. Revision `e3e9dd8e5b3d7ab8537cd5a10dc31d5ffa8f82d1`.
- [Bot API 10.3 · telegram-bot-api/Client.cpp:13981–13993](https://github.com/tdlib/telegram-bot-api/blob/e3e9dd8e5b3d7ab8537cd5a10dc31d5ffa8f82d1/telegram-bot-api/Client.cpp#L13981-L13993). sendMessage constructs its text with this helper. Revision `e3e9dd8e5b3d7ab8537cd5a10dc31d5ffa8f82d1`.
- [Bot API 10.3 · telegram-bot-api/Client.cpp:13800–13803](https://github.com/tdlib/telegram-bot-api/blob/e3e9dd8e5b3d7ab8537cd5a10dc31d5ffa8f82d1/telegram-bot-api/Client.cpp#L13800-L13803). Method validation errors are passed to the response normalizer. Revision `e3e9dd8e5b3d7ab8537cd5a10dc31d5ffa8f82d1`.
- [Bot API 10.3 · telegram-bot-api/Client.cpp:165–205](https://github.com/tdlib/telegram-bot-api/blob/e3e9dd8e5b3d7ab8537cd5a10dc31d5ffa8f82d1/telegram-bot-api/Client.cpp#L165-L205). Adds the code-specific prefix and lowercases only the initial character of ordinary messages. Revision `e3e9dd8e5b3d7ab8537cd5a10dc31d5ffa8f82d1`.

Source references identify the reviewed revision, not the first release
that introduced this response.

## Data and versions

Catalogue `0.1.0` · schema `1.0.0` · reviewed 2026-09-16.

[Markdown](/errors/text.empty.md) · [Condition JSON](/errors/text.empty.json) · [Full catalogue and sources](/catalogue.json) · [JSON Schema](/schema.json)
