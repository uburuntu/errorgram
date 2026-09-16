---
title: "File url upload failed · file.url_upload_failed"
description: "Telegram could not upload the file from its URL."
slug: "errors/file.url_upload_failed"
editUrl: "https://github.com/uburuntu/errorgram/edit/main/catalogue/errors.json"
sidebar:
  label: "file.url_upload_failed"
---

**Stable ID:** `file.url_upload_failed` · **Evidence:** source derived

Telegram could not upload the file from its URL.

The response mapping does not identify the original retrieval or file-generation failure.

## When it matches

Every field in a rule must match. Alternative rules are joined with OR.
Codes below are JSON response fields, not inferred HTTP statuses.

- JSON `error_code`: **400**.

Exact description:

```text
Bad Request: can't upload file by URL
```

See [matching rules](/matching/) for parameter precedence
and unknown or ambiguous results.

**Illustrative methods:** `sendPhoto`, `sendDocument`.

## Possible causes

- Generating a file from the supplied URL failed.

## Before deciding what to do

**Application decision:** inspect url file input.
**Repeat request:** after relevant change.

- Check the URL and file requirements; use a direct upload if the method supports it and the application can supply the file.

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
  "description": "Bad Request: can't upload file by URL"
}
```

### Python

```python
from errorgram import classify

response = {
    "ok": False,
    "error_code": 400,
    "description": "Bad Request: can't upload file by URL",
}
result = classify(response, method='sendPhoto')

assert result.id == 'file.url_upload_failed'
print(result.entry["summary"])
```

### JavaScript and TypeScript

```ts
import { classify } from "errorgram";

const response = {
  "ok": false,
  "error_code": 400,
  "description": "Bad Request: can't upload file by URL"
};
const result = classify(response, { method: "sendPhoto" });

if (result.status === "matched" && result.id === "file.url_upload_failed") {
  console.log(result.entry.summary);
}
```

## Framework names

| Integration | Type or ID |
| --- | --- |
| Python | `errorgram.FileUrlUploadFailed` |
| aiogram | `errorgram.aiogram.FileUrlUploadFailed` extends `TelegramBadRequest` |
| grammY | `EnrichedGrammyError` with `classification.id` equal to `file.url_upload_failed` |

Enrichment is explicit and keeps framework catch compatibility.
Follow the [Python and aiogram guide](/python/) or
[JavaScript, TypeScript, and grammY guide](/javascript/).

## Evidence

- [Bot API 10.3 · telegram-bot-api/Client.cpp:133–135](https://github.com/tdlib/telegram-bot-api/blob/e3e9dd8e5b3d7ab8537cd5a10dc31d5ffa8f82d1/telegram-bot-api/Client.cpp#L133-L135). File generation failed is rewritten to this description and code 400. Revision `e3e9dd8e5b3d7ab8537cd5a10dc31d5ffa8f82d1`.
- [Bot API 10.3 · telegram-bot-api/Client.cpp:85–106](https://github.com/tdlib/telegram-bot-api/blob/e3e9dd8e5b3d7ab8537cd5a10dc31d5ffa8f82d1/telegram-bot-api/Client.cpp#L85-L106). The rewrite runs only after the error is normalized to code 400. Revision `e3e9dd8e5b3d7ab8537cd5a10dc31d5ffa8f82d1`.
- [Bot API 10.3 · telegram-bot-api/Client.cpp:165–205](https://github.com/tdlib/telegram-bot-api/blob/e3e9dd8e5b3d7ab8537cd5a10dc31d5ffa8f82d1/telegram-bot-api/Client.cpp#L165-L205). Adds the code-specific prefix and lowercases only the initial character of ordinary messages. Revision `e3e9dd8e5b3d7ab8537cd5a10dc31d5ffa8f82d1`.

Source references identify the reviewed revision, not the first release
that introduced this response.

## Data and versions

Catalogue `0.1.0` · schema `1.0.0` · reviewed 2026-09-16.

[Markdown](/errors/file.url_upload_failed.md) · [Condition JSON](/errors/file.url_upload_failed.json) · [Full catalogue and sources](/catalogue.json) · [JSON Schema](/schema.json)
