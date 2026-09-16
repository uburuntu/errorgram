---
title: "File id missing · file.id_missing"
description: "The file_id argument is missing or empty."
slug: "errors/file.id_missing"
editUrl: "https://github.com/uburuntu/errorgram/edit/main/catalogue/errors.json"
sidebar:
  label: "file.id_missing"
---

**Stable ID:** `file.id_missing` · **Evidence:** observed

The file\_id argument is missing or empty.

This response concerns a missing file identifier; it does not validate an upload or a nonempty identifier.

## When it matches

Every field in a rule must match. Alternative rules are joined with OR.
Codes below are JSON response fields, not inferred HTTP statuses.

- JSON `error_code`: **400**.

Exact description:

```text
Bad Request: file_id not specified
```

See [matching rules](/matching/) for parameter precedence
and unknown or ambiguous results.

**Illustrative methods:** `getFile`.

## Possible causes

- The remote-file lookup received an empty file\_id.

## Before deciding what to do

**Application decision:** supply file identifier.
**Repeat request:** after relevant change.

- Use the file\_id supplied for this bot by Telegram, rather than file\_unique\_id.

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
  "description": "Bad Request: file_id not specified"
}
```

### Python

```python
from errorgram import classify

response = {
    "ok": False,
    "error_code": 400,
    "description": "Bad Request: file_id not specified",
}
result = classify(response, method='getFile')

assert result.id == 'file.id_missing'
print(result.entry["summary"])
```

### JavaScript and TypeScript

```ts
import { classify } from "errorgram";

const response = {
  "ok": false,
  "error_code": 400,
  "description": "Bad Request: file_id not specified"
};
const result = classify(response, { method: "getFile" });

if (result.status === "matched" && result.id === "file.id_missing") {
  console.log(result.entry.summary);
}
```

## Framework names

| Integration | Type or ID |
| --- | --- |
| Python | `errorgram.FileIdMissing` |
| aiogram | `errorgram.aiogram.FileIdMissing` extends `TelegramBadRequest` |
| grammY | `EnrichedGrammyError` with `classification.id` equal to `file.id_missing` |

Enrichment is explicit and keeps framework catch compatibility.
Follow the [Python and aiogram guide](/python/) or
[JavaScript, TypeScript, and grammY guide](/javascript/).

## Evidence

- [Recorded observation](https://github.com/uburuntu/errorgram/blob/4314ac1f9d29d105b10e9b537a7643cc65d097aa/observations/2026-09-16.json). getFile with an empty file\_id returned this description. Accessed 2026-09-16.
- [Bot API 10.3 · telegram-bot-api/Client.cpp:9034–9041](https://github.com/tdlib/telegram-bot-api/blob/e3e9dd8e5b3d7ab8537cd5a10dc31d5ffa8f82d1/telegram-bot-api/Client.cpp#L9034-L9041). The remote-file helper directly rejects an empty file\_id. Revision `e3e9dd8e5b3d7ab8537cd5a10dc31d5ffa8f82d1`.
- [Bot API 10.3 · telegram-bot-api/Client.cpp:17032–17035](https://github.com/tdlib/telegram-bot-api/blob/e3e9dd8e5b3d7ab8537cd5a10dc31d5ffa8f82d1/telegram-bot-api/Client.cpp#L17032-L17035). getFile passes its file\_id argument to the helper. Revision `e3e9dd8e5b3d7ab8537cd5a10dc31d5ffa8f82d1`.

Source references identify the reviewed revision, not the first release
that introduced this response.

## Data and versions

Catalogue `0.1.0` · schema `1.0.0` · reviewed 2026-09-16.

[Markdown](/errors/file.id_missing.md) · [Condition JSON](/errors/file.id_missing.json) · [Full catalogue and sources](/catalogue.json) · [JSON Schema](/schema.json)
