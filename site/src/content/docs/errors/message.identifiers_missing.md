---
title: "Message identifiers missing · message.identifiers_missing"
description: "The request did not specify the list of message identifiers."
slug: "errors/message.identifiers_missing"
editUrl: "https://github.com/uburuntu/errorgram/edit/main/catalogue/errors.json"
sidebar:
  label: "message.identifiers_missing"
---

**Stable ID:** `message.identifiers_missing` · **Evidence:** source derived

The request did not specify the list of message identifiers.

An empty argument and an encoded empty JSON array are different inputs; this response covers the former.

## When it matches

Every field in a rule must match. Alternative rules are joined with OR.
Codes below are JSON response fields, not inferred HTTP statuses.

- JSON `error_code`: **400**.

Exact description:

```text
Bad Request: message identifiers are not specified
```

See [matching rules](/matching/) for parameter precedence
and unknown or ambiguous results.

**Illustrative methods:** `deleteMessages`, `forwardMessages`, `copyMessages`.

## Possible causes

- The message\_ids argument is absent or empty.

## Before deciding what to do

**Application decision:** supply message identifiers.
**Repeat request:** after relevant change.

- Provide a JSON array of the intended message identifiers and check the method-specific count limit.

These are application choices. Errorgram does not retry, suppress the error,
or change bot state.

## Facts

This condition adds no extracted facts; `result.facts` is empty.

## Example

Synthetic examples derived from the cited source.

API method: `deleteMessages`.

```json
{
  "ok": false,
  "error_code": 400,
  "description": "Bad Request: message identifiers are not specified"
}
```

### Python

```python
from errorgram import classify

response = {
    "ok": False,
    "error_code": 400,
    "description": "Bad Request: message identifiers are not specified",
}
result = classify(response, method='deleteMessages')

assert result.id == 'message.identifiers_missing'
print(result.entry["summary"])
```

### JavaScript and TypeScript

```ts
import { classify } from "errorgram";

const response = {
  "ok": false,
  "error_code": 400,
  "description": "Bad Request: message identifiers are not specified"
};
const result = classify(response, { method: "deleteMessages" });

if (result.status === "matched" && result.id === "message.identifiers_missing") {
  console.log(result.entry.summary);
}
```

## Framework names

| Integration | Type or ID |
| --- | --- |
| Python | `errorgram.MessageIdentifiersMissing` |
| aiogram | `errorgram.aiogram.MessageIdentifiersMissing` extends `TelegramBadRequest` |
| grammY | `EnrichedGrammyError` with `classification.id` equal to `message.identifiers_missing` |

Enrichment is explicit and keeps framework catch compatibility.
Follow the [Python and aiogram guide](/python/) or
[JavaScript, TypeScript, and grammY guide](/javascript/).

## Evidence

- [Bot API 10.3 · telegram-bot-api/Client.cpp:13500–13504](https://github.com/tdlib/telegram-bot-api/blob/e3e9dd8e5b3d7ab8537cd5a10dc31d5ffa8f82d1/telegram-bot-api/Client.cpp#L13500-L13504). The list parser rejects an absent or empty argument before JSON decoding. Revision `e3e9dd8e5b3d7ab8537cd5a10dc31d5ffa8f82d1`.
- [Bot API 10.3 · telegram-bot-api/Client.cpp:15000–15003](https://github.com/tdlib/telegram-bot-api/blob/e3e9dd8e5b3d7ab8537cd5a10dc31d5ffa8f82d1/telegram-bot-api/Client.cpp#L15000-L15003). deleteMessages passes message\_ids to this parser. Revision `e3e9dd8e5b3d7ab8537cd5a10dc31d5ffa8f82d1`.
- [Bot API 10.3 · telegram-bot-api/Client.cpp:13800–13803](https://github.com/tdlib/telegram-bot-api/blob/e3e9dd8e5b3d7ab8537cd5a10dc31d5ffa8f82d1/telegram-bot-api/Client.cpp#L13800-L13803). Method validation errors are passed to the response normalizer. Revision `e3e9dd8e5b3d7ab8537cd5a10dc31d5ffa8f82d1`.
- [Bot API 10.3 · telegram-bot-api/Client.cpp:165–205](https://github.com/tdlib/telegram-bot-api/blob/e3e9dd8e5b3d7ab8537cd5a10dc31d5ffa8f82d1/telegram-bot-api/Client.cpp#L165-L205). Adds the code-specific prefix and lowercases only the initial character of ordinary messages. Revision `e3e9dd8e5b3d7ab8537cd5a10dc31d5ffa8f82d1`.

Source references identify the reviewed revision, not the first release
that introduced this response.

## Data and versions

Catalogue `0.1.0` · schema `1.0.0` · reviewed 2026-09-16.

[Markdown](/errors/message.identifiers_missing.md) · [Condition JSON](/errors/message.identifiers_missing.json) · [Full catalogue and sources](/catalogue.json) · [JSON Schema](/schema.json)
