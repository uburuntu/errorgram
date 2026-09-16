---
title: "Updates webhook active · updates.webhook_active"
description: "Polling was requested while a webhook is active or being configured."
slug: "errors/updates.webhook_active"
editUrl: "https://github.com/uburuntu/errorgram/edit/main/catalogue/errors.json"
sidebar:
  label: "updates.webhook_active"
---

**Stable ID:** `updates.webhook_active` · **Evidence:** source derived

Polling was requested while a webhook is active or being configured.

This is a different condition from two simultaneous getUpdates requests.

## When it matches

Every field in a rule must match. Alternative rules are joined with OR.
Codes below are JSON response fields, not inferred HTTP statuses.

- JSON `error_code`: **409**.

Exact description:

```text
Conflict: can't use getUpdates method while webhook is active; use deleteWebhook to delete the webhook first
```

See [matching rules](/matching/) for parameter precedence
and unknown or ambiguous results.

**Illustrative methods:** `getUpdates`.

## Possible causes

- The bot has an active or pending webhook configuration.

## Before deciding what to do

**Application decision:** choose update delivery mode.
**Repeat request:** after configuration change.

- If polling is intended, remove the webhook deliberately; if webhooks are intended, stop polling.

These are application choices. Errorgram does not retry, suppress the error,
or change bot state.

## Facts

This condition adds no extracted facts; `result.facts` is empty.

## Example

Synthetic examples derived from the cited source.

API method: `getUpdates`.

```json
{
  "ok": false,
  "error_code": 409,
  "description": "Conflict: can't use getUpdates method while webhook is active; use deleteWebhook to delete the webhook first"
}
```

### Python

```python
from errorgram import classify

response = {
    "ok": False,
    "error_code": 409,
    "description": "Conflict: can't use getUpdates method while webhook is active; use deleteWebhook to delete the webhook first",
}
result = classify(response, method='getUpdates')

assert result.id == 'updates.webhook_active'
print(result.entry["summary"])
```

### JavaScript and TypeScript

```ts
import { classify } from "errorgram";

const response = {
  "ok": false,
  "error_code": 409,
  "description": "Conflict: can't use getUpdates method while webhook is active; use deleteWebhook to delete the webhook first"
};
const result = classify(response, { method: "getUpdates" });

if (result.status === "matched" && result.id === "updates.webhook_active") {
  console.log(result.entry.summary);
}
```

## Framework names

| Integration | Type or ID |
| --- | --- |
| Python | `errorgram.UpdatesWebhookActive` |
| aiogram | `errorgram.aiogram.UpdatesWebhookActive` extends `TelegramConflictError` |
| grammY | `EnrichedGrammyError` with `classification.id` equal to `updates.webhook_active` |

Enrichment is explicit and keeps framework catch compatibility.
Follow the [Python and aiogram guide](/python/) or
[JavaScript, TypeScript, and grammY guide](/javascript/).

## Evidence

- [Bot API 10.3 · telegram-bot-api/Client.cpp:16926–16931](https://github.com/tdlib/telegram-bot-api/blob/e3e9dd8e5b3d7ab8537cd5a10dc31d5ffa8f82d1/telegram-bot-api/Client.cpp#L16926-L16931). Checks configured and pending webhook state before polling. Revision `e3e9dd8e5b3d7ab8537cd5a10dc31d5ffa8f82d1`.

Source references identify the reviewed revision, not the first release
that introduced this response.

## Data and versions

Catalogue `0.1.0` · schema `1.0.0` · reviewed 2026-09-16.

[Markdown](/errors/updates.webhook_active.md) · [Condition JSON](/errors/updates.webhook_active.json) · [Full catalogue and sources](/catalogue.json) · [JSON Schema](/schema.json)
