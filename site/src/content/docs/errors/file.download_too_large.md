---
title: "File download too large · file.download_too_large"
description: "The file exceeds the server’s non-local download limit."
slug: "errors/file.download_too_large"
editUrl: "https://github.com/uburuntu/errorgram/edit/main/catalogue/errors.json"
sidebar:
  label: "file.download_too_large"
---

**Stable ID:** `file.download_too_large` · **Evidence:** source derived

The file exceeds the server’s non-local download limit.

A bare file-is-too-big description without method context is insufficient for this download-specific classification. This is not an upload-size rule.

## When it matches

Every field in a rule must match. Alternative rules are joined with OR.
Codes below are JSON response fields, not inferred HTTP statuses.

- JSON `error_code`: **400**.
- Required method: `getfile`, ignoring ASCII case.

Exact description:

```text
Bad Request: file is too big
```

See [matching rules](/matching/) for parameter precedence
and unknown or ambiguous results.

**Illustrative methods:** `getFile`.

Source guard applies when local\_mode is false.

## Possible causes

- Expected or downloaded file size exceeds MAX\_DOWNLOAD\_FILE\_SIZE while local mode is disabled.

## Before deciding what to do

**Application decision:** change download strategy.
**Repeat request:** after relevant change.

- Use a suitable smaller file or deliberately configure a server with the required local-mode download capability.

These are application choices. Errorgram does not retry, suppress the error,
or change bot state.

## Facts

This condition adds no extracted facts; `result.facts` is empty.

Version-specific metadata is available in `result.entry` under `facts`.
These values are catalogue metadata, not measurements from the response.

```json
{
  "verified_limit_bytes": 20971520,
  "limit_version_source": "server-10.3"
}
```

## Example

Synthetic examples derived from the cited source.

API method: `getFile`.

```json
{
  "ok": false,
  "error_code": 400,
  "description": "Bad Request: file is too big"
}
```

### Python

```python
from errorgram import classify

response = {
    "ok": False,
    "error_code": 400,
    "description": "Bad Request: file is too big",
}
result = classify(response, method='getFile')

assert result.id == 'file.download_too_large'
print(result.entry["summary"])
```

### JavaScript and TypeScript

```ts
import { classify } from "errorgram";

const response = {
  "ok": false,
  "error_code": 400,
  "description": "Bad Request: file is too big"
};
const result = classify(response, { method: "getFile" });

if (result.status === "matched" && result.id === "file.download_too_large") {
  console.log(result.entry.summary);
}
```

## Framework names

| Integration | Type or ID |
| --- | --- |
| Python | `errorgram.FileDownloadTooLarge` |
| aiogram | `errorgram.aiogram.FileDownloadTooLarge` extends `TelegramBadRequest` |
| grammY | `EnrichedGrammyError` with `classification.id` equal to `file.download_too_large` |

Enrichment is explicit and keeps framework catch compatibility.
Follow the [Python and aiogram guide](/python/) or
[JavaScript, TypeScript, and grammY guide](/javascript/).

## Evidence

- [Bot API 10.3 · telegram-bot-api/Client.cpp:17032–17049](https://github.com/tdlib/telegram-bot-api/blob/e3e9dd8e5b3d7ab8537cd5a10dc31d5ffa8f82d1/telegram-bot-api/Client.cpp#L17032-L17049). getFile reaches the size check guarded by local\_mode. Revision `e3e9dd8e5b3d7ab8537cd5a10dc31d5ffa8f82d1`.
- [Bot API 10.3 · telegram-bot-api/Client.cpp:9373–9383](https://github.com/tdlib/telegram-bot-api/blob/e3e9dd8e5b3d7ab8537cd5a10dc31d5ffa8f82d1/telegram-bot-api/Client.cpp#L9373-L9383). The download update path enforces the same limit. Revision `e3e9dd8e5b3d7ab8537cd5a10dc31d5ffa8f82d1`.
- [Bot API 10.3 · telegram-bot-api/Client.h:72](https://github.com/tdlib/telegram-bot-api/blob/e3e9dd8e5b3d7ab8537cd5a10dc31d5ffa8f82d1/telegram-bot-api/Client.h#L72). The constant is 20 &lt;&lt; 20 bytes in this revision. Revision `e3e9dd8e5b3d7ab8537cd5a10dc31d5ffa8f82d1`.

Source references identify the reviewed revision, not the first release
that introduced this response.

## Data and versions

Catalogue `0.1.0` · schema `1.0.0` · reviewed 2026-09-15.

[Markdown](/errors/file.download_too_large.md) · [Condition JSON](/errors/file.download_too_large.json) · [Full catalogue and sources](/catalogue.json) · [JSON Schema](/schema.json)
