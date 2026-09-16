---
title: "Text too long · text.too_long"
description: "The text exceeds the limit checked by this response path."
slug: "errors/text.too_long"
editUrl: "https://github.com/uburuntu/errorgram/edit/main/catalogue/errors.json"
sidebar:
  label: "text.too_long"
---

**Stable ID:** `text.too_long` · **Evidence:** source derived

The text exceeds the limit checked by this response path.

The local guard is not the public character limit for every method. Other message and caption limits can produce different descriptions.

## When it matches

Every field in a rule must match. Alternative rules are joined with OR.
Codes below are JSON response fields, not inferred HTTP statuses.

- JSON `error_code`: **400**.

Exact description:

```text
Bad Request: text is too long
```

See [matching rules](/matching/) for parameter precedence
and unknown or ambiguous results.

**Illustrative methods:** `sendMessage`, `editMessageText`, `sendPhoto`.

## Possible causes

- Text supplied to the formatting helper exceeds its local byte-size guard.

## Before deciding what to do

**Application decision:** shorten text for method.
**Repeat request:** after relevant change.

- Check the selected method’s text or caption limits and preserve valid formatting when shortening or splitting text.

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
  "description": "Bad Request: text is too long"
}
```

### Python

```python
from errorgram import classify

response = {
    "ok": False,
    "error_code": 400,
    "description": "Bad Request: text is too long",
}
result = classify(response, method='sendMessage')

assert result.id == 'text.too_long'
print(result.entry["summary"])
```

### JavaScript and TypeScript

```ts
import { classify } from "errorgram";

const response = {
  "ok": false,
  "error_code": 400,
  "description": "Bad Request: text is too long"
};
const result = classify(response, { method: "sendMessage" });

if (result.status === "matched" && result.id === "text.too_long") {
  console.log(result.entry.summary);
}
```

## Framework names

| Integration | Type or ID |
| --- | --- |
| Python | `errorgram.TextTooLong` |
| aiogram | `errorgram.aiogram.TextTooLong` extends `TelegramBadRequest` |
| grammY | `EnrichedGrammyError` with `classification.id` equal to `text.too_long` |

Enrichment is explicit and keeps framework catch compatibility.
Follow the [Python and aiogram guide](/python/) or
[JavaScript, TypeScript, and grammY guide](/javascript/).

## Evidence

- [Bot API 10.3 · telegram-bot-api/Client.cpp:11955–11958](https://github.com/tdlib/telegram-bot-api/blob/e3e9dd8e5b3d7ab8537cd5a10dc31d5ffa8f82d1/telegram-bot-api/Client.cpp#L11955-L11958). The formatting helper rejects text.size() greater than 32768 before parsing. Revision `e3e9dd8e5b3d7ab8537cd5a10dc31d5ffa8f82d1`.
- [Bot API 10.3 · telegram-bot-api/Client.cpp:13800–13803](https://github.com/tdlib/telegram-bot-api/blob/e3e9dd8e5b3d7ab8537cd5a10dc31d5ffa8f82d1/telegram-bot-api/Client.cpp#L13800-L13803). Method validation errors are passed to the response normalizer. Revision `e3e9dd8e5b3d7ab8537cd5a10dc31d5ffa8f82d1`.
- [Bot API 10.3 · telegram-bot-api/Client.cpp:165–205](https://github.com/tdlib/telegram-bot-api/blob/e3e9dd8e5b3d7ab8537cd5a10dc31d5ffa8f82d1/telegram-bot-api/Client.cpp#L165-L205). Adds the code-specific prefix and lowercases only the initial character of ordinary messages. Revision `e3e9dd8e5b3d7ab8537cd5a10dc31d5ffa8f82d1`.

Source references identify the reviewed revision, not the first release
that introduced this response.

## Data and versions

Catalogue `0.1.0` · schema `1.0.0` · reviewed 2026-09-16.

[Markdown](/errors/text.too_long.md) · [Condition JSON](/errors/text.too_long.json) · [Full catalogue and sources](/catalogue.json) · [JSON Schema](/schema.json)
