---
title: "Updates concurrent poll · updates.concurrent_poll"
description: "Another getUpdates request interrupted the pending long poll."
slug: "errors/updates.concurrent_poll"
editUrl: "https://github.com/uburuntu/errorgram/edit/main/catalogue/errors.json"
sidebar:
  label: "updates.concurrent_poll"
---

**Stable ID:** `updates.concurrent_poll` · **Evidence:** source derived

Another getUpdates request interrupted the pending long poll.

Overlapping requests may originate in one process or multiple deployments; the response does not prove how many bot processes exist.

## When it matches

Every field in a rule must match. Alternative rules are joined with OR.
Codes below are JSON response fields, not inferred HTTP statuses.

- JSON `error_code`: **409**.

Exact description:

```text
Conflict: terminated by other getUpdates request; make sure that only one bot instance is running
```

See [matching rules](/matching/) for parameter precedence
and unknown or ambiguous results.

**Illustrative methods:** `getUpdates`.

## Possible causes

- Overlapping getUpdates requests for the same bot.

## Before deciding what to do

**Application decision:** ensure single polling owner.
**Repeat request:** after concurrency change.

- Stop competing polling loops or establish ownership before resuming.

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
  "description": "Conflict: terminated by other getUpdates request; make sure that only one bot instance is running"
}
```

### Python

```python
from errorgram import classify

response = {
    "ok": False,
    "error_code": 409,
    "description": "Conflict: terminated by other getUpdates request; make sure that only one bot instance is running",
}
result = classify(response, method='getUpdates')

assert result.id == 'updates.concurrent_poll'
print(result.entry["summary"])
```

### JavaScript and TypeScript

```ts
import { classify } from "errorgram";

const response = {
  "ok": false,
  "error_code": 409,
  "description": "Conflict: terminated by other getUpdates request; make sure that only one bot instance is running"
};
const result = classify(response, { method: "getUpdates" });

if (result.status === "matched" && result.id === "updates.concurrent_poll") {
  console.log(result.entry.summary);
}
```

## Framework names

| Integration | Type or ID |
| --- | --- |
| Python | `errorgram.UpdatesConcurrentPoll` |
| aiogram | `errorgram.aiogram.UpdatesConcurrentPoll` extends `TelegramConflictError` |
| grammY | `EnrichedGrammyError` with `classification.id` equal to `updates.concurrent_poll` |

Enrichment is explicit and keeps framework catch compatibility.
Follow the [Python and aiogram guide](/python/) or
[JavaScript, TypeScript, and grammY guide](/javascript/).

## Evidence

- [Bot API 10.3 · telegram-bot-api/Client.cpp:17493–17514](https://github.com/tdlib/telegram-bot-api/blob/e3e9dd8e5b3d7ab8537cd5a10dc31d5ffa8f82d1/telegram-bot-api/Client.cpp#L17493-L17514). The alternate branch emits a different description for termination by setWebhook. Revision `e3e9dd8e5b3d7ab8537cd5a10dc31d5ffa8f82d1`.

Source references identify the reviewed revision, not the first release
that introduced this response.

## Data and versions

Catalogue `0.1.0` · schema `1.0.0` · reviewed 2026-09-16.

[Markdown](/errors/updates.concurrent_poll.md) · [Condition JSON](/errors/updates.concurrent_poll.json) · [Full catalogue and sources](/catalogue.json) · [JSON Schema](/schema.json)
