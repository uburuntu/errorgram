---
title: "File unavailable · file.unavailable"
description: "The file could not be downloaded with the supplied identifier."
slug: "errors/file.unavailable"
editUrl: "https://github.com/uburuntu/errorgram/edit/main/catalogue/errors.json"
sidebar:
  label: "file.unavailable"
---

**Stable ID:** `file.unavailable` · **Evidence:** source derived

The file could not be downloaded with the supplied identifier.

The source notes that this path also hides upstream 5xx and 429 errors. The response supplies no retry delay and does not prove that the ID is wrong.

## When it matches

Every field in a rule must match. Alternative rules are joined with OR.
Codes below are JSON response fields, not inferred HTTP statuses.

- JSON `error_code`: **400**.

Exact description:

```text
Bad Request: wrong file_id or the file is temporarily unavailable
```

See [matching rules](/matching/) for parameter precedence
and unknown or ambiguous results.

**Illustrative methods:** `getFile`.

## Possible causes

- A started download stopped before completion without an active shutdown or logout state.

## Before deciding what to do

**Application decision:** check file and retry policy.
**Repeat request:** after relevant change.

- Verify the file\_id; if a temporary failure is plausible, apply a bounded retry policy without inventing a server delay.

These are application choices. Errorgram does not retry, suppress the error,
or change bot state.

## Facts

This condition adds no extracted facts; `result.facts` is empty.

## Example

Synthetic examples derived from the cited source.

API method: `getFile`.

```json
{
  "ok": false,
  "error_code": 400,
  "description": "Bad Request: wrong file_id or the file is temporarily unavailable"
}
```

### Python

```python
from errorgram import classify

response = {
    "ok": False,
    "error_code": 400,
    "description": "Bad Request: wrong file_id or the file is temporarily unavailable",
}
result = classify(response, method='getFile')

assert result.id == 'file.unavailable'
print(result.entry["summary"])
```

### JavaScript and TypeScript

```ts
import { classify } from "errorgram";

const response = {
  "ok": false,
  "error_code": 400,
  "description": "Bad Request: wrong file_id or the file is temporarily unavailable"
};
const result = classify(response, { method: "getFile" });

if (result.status === "matched" && result.id === "file.unavailable") {
  console.log(result.entry.summary);
}
```

## Framework names

| Integration | Type or ID |
| --- | --- |
| Python | `errorgram.FileUnavailable` |
| aiogram | `errorgram.aiogram.FileUnavailable` extends `TelegramBadRequest` |
| grammY | `EnrichedGrammyError` with `classification.id` equal to `file.unavailable` |

Enrichment is explicit and keeps framework catch compatibility.
Follow the [Python and aiogram guide](/python/) or
[JavaScript, TypeScript, and grammY guide](/javascript/).

## Evidence

- [Bot API 10.3 · telegram-bot-api/Client.cpp:9385–9396](https://github.com/tdlib/telegram-bot-api/blob/e3e9dd8e5b3d7ab8537cd5a10dc31d5ffa8f82d1/telegram-bot-api/Client.cpp#L9385-L9396). An inactive, incomplete started download is converted to this generic 400 response. Revision `e3e9dd8e5b3d7ab8537cd5a10dc31d5ffa8f82d1`.
- [Bot API 10.3 · telegram-bot-api/Client.cpp:17056–17067](https://github.com/tdlib/telegram-bot-api/blob/e3e9dd8e5b3d7ab8537cd5a10dc31d5ffa8f82d1/telegram-bot-api/Client.cpp#L17056-L17067). The download failure is forwarded to waiting getFile queries through the normalizer. Revision `e3e9dd8e5b3d7ab8537cd5a10dc31d5ffa8f82d1`.
- [Bot API 10.3 · telegram-bot-api/Client.cpp:165–205](https://github.com/tdlib/telegram-bot-api/blob/e3e9dd8e5b3d7ab8537cd5a10dc31d5ffa8f82d1/telegram-bot-api/Client.cpp#L165-L205). Adds the code-specific prefix and lowercases only the initial character of ordinary messages. Revision `e3e9dd8e5b3d7ab8537cd5a10dc31d5ffa8f82d1`.

Source references identify the reviewed revision, not the first release
that introduced this response.

## Data and versions

Catalogue `0.1.0` · schema `1.0.0` · reviewed 2026-09-16.

[Markdown](/errors/file.unavailable.md) · [Condition JSON](/errors/file.unavailable.json) · [Full catalogue and sources](/catalogue.json) · [JSON Schema](/schema.json)
