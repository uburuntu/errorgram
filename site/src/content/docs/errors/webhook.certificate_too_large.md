---
title: "Webhook certificate too large · webhook.certificate_too_large"
description: "The uploaded webhook certificate exceeds the server’s size limit."
slug: "errors/webhook.certificate_too_large"
editUrl: "https://github.com/uburuntu/errorgram/edit/main/catalogue/errors.json"
sidebar:
  label: "webhook.certificate_too_large"
---

**Stable ID:** `webhook.certificate_too_large` · **Evidence:** source derived

The uploaded webhook certificate exceeds the server’s size limit.

The captured size describes the rejected upload; it is not the configured limit or a Telegram media limit.

## When it matches

Every field in a rule must match. Alternative rules are joined with OR.
Codes below are JSON response fields, not inferred HTTP statuses.

- JSON `error_code`: **400**.

Description template; literal text must match exactly:

```text
Bad Request: certificate size is too big ({size_bytes} bytes)
```

- `size_bytes`: a positive safe integer, captured from the description.

See [matching rules](/matching/) for parameter precedence
and unknown or ambiguous results.

**Illustrative methods:** `setWebhook`.

## Possible causes

- The uploaded certificate file is larger than MAX\_CERTIFICATE\_FILE\_SIZE.

## Before deciding what to do

**Application decision:** correct webhook certificate file.
**Repeat request:** after payload change.

- Verify that the uploaded file is the intended certificate and satisfies this server revision's limit.

These are application choices. Errorgram does not retry, suppress the error,
or change bot state.

## Facts

Values extracted into `result.facts`:

- `size_bytes`: a positive safe integer, from `description`.

Version-specific metadata is available in `result.entry` under `facts`.
These values are catalogue metadata, not measurements from the response.

```json
{
  "verified_limit_bytes": 3145728,
  "limit_version_source": "server-10.3"
}
```

## Example

Synthetic examples derived from the cited source.

API method: `setWebhook`.

```json
{
  "ok": false,
  "error_code": 400,
  "description": "Bad Request: certificate size is too big (4194304 bytes)"
}
```

### Python

```python
from errorgram import classify

response = {
    "ok": False,
    "error_code": 400,
    "description": "Bad Request: certificate size is too big (4194304 bytes)",
}
result = classify(response, method='setWebhook')

assert result.id == 'webhook.certificate_too_large'
print(result.entry["summary"])
```

### JavaScript and TypeScript

```ts
import { classify } from "errorgram";

const response = {
  "ok": false,
  "error_code": 400,
  "description": "Bad Request: certificate size is too big (4194304 bytes)"
};
const result = classify(response, { method: "setWebhook" });

if (result.status === "matched" && result.id === "webhook.certificate_too_large") {
  console.log(result.entry.summary);
}
```

## Framework names

| Integration | Type or ID |
| --- | --- |
| Python | `errorgram.WebhookCertificateTooLarge` |
| aiogram | `errorgram.aiogram.WebhookCertificateTooLarge` extends `TelegramBadRequest` |
| grammY | `EnrichedGrammyError` with `classification.id` equal to `webhook.certificate_too_large` |

Enrichment is explicit and keeps framework catch compatibility.
Follow the [Python and aiogram guide](/python/) or
[JavaScript, TypeScript, and grammY guide](/javascript/).

## Evidence

- [Bot API 10.3 · telegram-bot-api/Client.cpp:17261–17266](https://github.com/tdlib/telegram-bot-api/blob/e3e9dd8e5b3d7ab8537cd5a10dc31d5ffa8f82d1/telegram-bot-api/Client.cpp#L17261-L17266). The description interpolates the actual file size; one literal string cannot represent all responses. Revision `e3e9dd8e5b3d7ab8537cd5a10dc31d5ffa8f82d1`.
- [Bot API 10.3 · telegram-bot-api/Client.h:71](https://github.com/tdlib/telegram-bot-api/blob/e3e9dd8e5b3d7ab8537cd5a10dc31d5ffa8f82d1/telegram-bot-api/Client.h#L71). The constant is 3 &lt;&lt; 20 bytes in this revision. Revision `e3e9dd8e5b3d7ab8537cd5a10dc31d5ffa8f82d1`.

Source references identify the reviewed revision, not the first release
that introduced this response.

## Data and versions

Catalogue `0.1.0` · schema `1.0.0` · reviewed 2026-09-15.

[Markdown](/errors/webhook.certificate_too_large.md) · [Condition JSON](/errors/webhook.certificate_too_large.json) · [Full catalogue and sources](/catalogue.json) · [JSON Schema](/schema.json)
