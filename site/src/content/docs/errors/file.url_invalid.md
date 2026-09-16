---
title: "File url invalid · file.url_invalid"
description: "The HTTP URL was rejected."
slug: "errors/file.url_invalid"
editUrl: "https://github.com/uburuntu/errorgram/edit/main/catalogue/errors.json"
sidebar:
  label: "file.url_invalid"
---

**Stable ID:** `file.url_invalid` · **Evidence:** source derived

The HTTP URL was rejected.

The response does not identify the invalid URL component or establish whether the resource is reachable.

## When it matches

Every field in a rule must match. Alternative rules are joined with OR.
Codes below are JSON response fields, not inferred HTTP statuses.

- JSON `error_code`: **400**.

Exact description:

```text
Bad Request: wrong HTTP URL specified
```

See [matching rules](/matching/) for parameter precedence
and unknown or ambiguous results.

**Illustrative methods:** `sendPhoto`, `sendDocument`.

## Possible causes

- The supplied external URL failed Telegram’s URL validation.

## Before deciding what to do

**Application decision:** correct file url.
**Repeat request:** after relevant change.

- Provide a valid HTTP URL for the intended resource and check the selected method’s URL-input rules.

These are application choices. Errorgram does not retry, suppress the error,
or change bot state.

## Facts

This condition adds no extracted facts; `result.facts` is empty.

## Example

Synthetic examples derived from the cited source.

API method: `sendPhoto`.

```json
{
  "ok": false,
  "error_code": 400,
  "description": "Bad Request: wrong HTTP URL specified"
}
```

### Python

```python
from errorgram import classify

response = {
    "ok": False,
    "error_code": 400,
    "description": "Bad Request: wrong HTTP URL specified",
}
result = classify(response, method='sendPhoto')

assert result.id == 'file.url_invalid'
print(result.entry["summary"])
```

### JavaScript and TypeScript

```ts
import { classify } from "errorgram";

const response = {
  "ok": false,
  "error_code": 400,
  "description": "Bad Request: wrong HTTP URL specified"
};
const result = classify(response, { method: "sendPhoto" });

if (result.status === "matched" && result.id === "file.url_invalid") {
  console.log(result.entry.summary);
}
```

## Framework names

| Integration | Type or ID |
| --- | --- |
| Python | `errorgram.FileUrlInvalid` |
| aiogram | `errorgram.aiogram.FileUrlInvalid` extends `TelegramBadRequest` |
| grammY | `EnrichedGrammyError` with `classification.id` equal to `file.url_invalid` |

Enrichment is explicit and keeps framework catch compatibility.
Follow the [Python and aiogram guide](/python/) or
[JavaScript, TypeScript, and grammY guide](/javascript/).

## Evidence

- [Bot API 10.3 · telegram-bot-api/Client.cpp:114–115](https://github.com/tdlib/telegram-bot-api/blob/e3e9dd8e5b3d7ab8537cd5a10dc31d5ffa8f82d1/telegram-bot-api/Client.cpp#L114-L115). Two upstream URL validation errors are rewritten to the same description. Revision `e3e9dd8e5b3d7ab8537cd5a10dc31d5ffa8f82d1`.
- [Bot API 10.3 · telegram-bot-api/Client.cpp:85–106](https://github.com/tdlib/telegram-bot-api/blob/e3e9dd8e5b3d7ab8537cd5a10dc31d5ffa8f82d1/telegram-bot-api/Client.cpp#L85-L106). The rewrite runs only after the error is normalized to code 400. Revision `e3e9dd8e5b3d7ab8537cd5a10dc31d5ffa8f82d1`.
- [Bot API 10.3 · telegram-bot-api/Client.cpp:165–205](https://github.com/tdlib/telegram-bot-api/blob/e3e9dd8e5b3d7ab8537cd5a10dc31d5ffa8f82d1/telegram-bot-api/Client.cpp#L165-L205). Adds the code-specific prefix and lowercases only the initial character of ordinary messages. Revision `e3e9dd8e5b3d7ab8537cd5a10dc31d5ffa8f82d1`.

Source references identify the reviewed revision, not the first release
that introduced this response.

## Data and versions

Catalogue `0.1.0` · schema `1.0.0` · reviewed 2026-09-16.

[Markdown](/errors/file.url_invalid.md) · [Condition JSON](/errors/file.url_invalid.json) · [Full catalogue and sources](/catalogue.json) · [JSON Schema](/schema.json)
