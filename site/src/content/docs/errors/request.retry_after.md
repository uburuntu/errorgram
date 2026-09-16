---
title: "Request retry after · request.retry_after"
description: "The server asks the bot to wait before trying again."
slug: "errors/request.retry_after"
editUrl: "https://github.com/uburuntu/errorgram/edit/main/catalogue/errors.json"
sidebar:
  label: "request.retry_after"
---

**Stable ID:** `request.retry_after` · **Evidence:** source derived

The server asks the bot to wait before trying again.

The response does not identify whether the limit is per chat, per bot, per method or caused by server lifecycle handling.

## When it matches

Every field in a rule must match. Alternative rules are joined with OR.
Codes below are JSON response fields, not inferred HTTP statuses.

- JSON `error_code`: **429**.
- `parameters.retry_after`: a positive safe integer.

The structured parameter decides the match; the description may vary.

See [matching rules](/matching/) for parameter precedence
and unknown or ambiguous results.

**Illustrative methods:** `sendMessage`, `setWebhook`, `close`.

## Possible causes

- Flood limiting.
- Authorization or startup throttling.
- An unfinished query being disposed, including during shutdown.

## Before deciding what to do

**Application decision:** schedule bounded retry.
**Repeat request:** after server delay and policy check.

- Wait at least the supplied delay, coordinate with any framework retry plugin, and bound attempts.

Delay parameter: `retry_after`.

These are application choices. Errorgram does not retry, suppress the error,
or change bot state.

## Facts

Values extracted into `result.facts`:

- `retry_after`: a positive safe integer, from `parameters.retry_after`.

## Example

Synthetic examples derived from the cited source.

API method: `sendMessage`.

```json
{
  "ok": false,
  "error_code": 429,
  "description": "Too Many Requests: retry after 5",
  "parameters": {
    "retry_after": 5
  }
}
```

### Python

```python
from errorgram import classify

response = {
    "ok": False,
    "error_code": 429,
    "description": "Too Many Requests: retry after 5",
    "parameters": {
        "retry_after": 5,
    },
}
result = classify(response, method='sendMessage')

assert result.id == 'request.retry_after'
print(result.entry["summary"])
```

### JavaScript and TypeScript

```ts
import { classify } from "errorgram";

const response = {
  "ok": false,
  "error_code": 429,
  "description": "Too Many Requests: retry after 5",
  "parameters": {
    "retry_after": 5
  }
};
const result = classify(response, { method: "sendMessage" });

if (result.status === "matched" && result.id === "request.retry_after") {
  console.log(result.entry.summary);
}
```

## Framework names

| Integration | Type or ID |
| --- | --- |
| Python | `errorgram.RequestRetryAfter` |
| aiogram | `errorgram.aiogram.RequestRetryAfter` extends `TelegramRetryAfter` |
| grammY | `EnrichedGrammyError` with `classification.id` equal to `request.retry_after` |

Enrichment is explicit and keeps framework catch compatibility.
Follow the [Python and aiogram guide](/python/) or
[JavaScript, TypeScript, and grammY guide](/javascript/).

## Evidence

- [Bot API 10.3 · telegram-bot-api/Query.cpp:120–126](https://github.com/tdlib/telegram-bot-api/blob/e3e9dd8e5b3d7ab8537cd5a10dc31d5ffa8f82d1/telegram-bot-api/Query.cpp#L120-L126). Builds both the description and structured retry\_after parameter. Revision `e3e9dd8e5b3d7ab8537cd5a10dc31d5ffa8f82d1`.
- [Bot API 10.3 · telegram-bot-api/Query.h:238–242](https://github.com/tdlib/telegram-bot-api/blob/e3e9dd8e5b3d7ab8537cd5a10dc31d5ffa8f82d1/telegram-bot-api/Query.h#L238-L242). The query deleter also produces this response with a five-second delay. Revision `e3e9dd8e5b3d7ab8537cd5a10dc31d5ffa8f82d1`.
- [Bot API 10.3 · telegram-bot-api/Client.cpp:17529–17550](https://github.com/tdlib/telegram-bot-api/blob/e3e9dd8e5b3d7ab8537cd5a10dc31d5ffa8f82d1/telegram-bot-api/Client.cpp#L17529-L17550). Flood and authorization paths share the response shape. Revision `e3e9dd8e5b3d7ab8537cd5a10dc31d5ffa8f82d1`.
- [Official documentation](https://core.telegram.org/bots/api#responseparameters). Documents retry\_after in seconds. Accessed 2026-09-15.

Source references identify the reviewed revision, not the first release
that introduced this response.

## Data and versions

Catalogue `0.1.0` · schema `1.0.0` · reviewed 2026-09-16.

[Markdown](/errors/request.retry_after.md) · [Condition JSON](/errors/request.retry_after.json) · [Full catalogue and sources](/catalogue.json) · [JSON Schema](/schema.json)
