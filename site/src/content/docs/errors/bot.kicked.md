---
title: "Bot kicked · bot.kicked"
description: "The bot was removed or banned from the chat."
slug: "errors/bot.kicked"
editUrl: "https://github.com/uburuntu/errorgram/edit/main/catalogue/errors.json"
sidebar:
  label: "bot.kicked"
---

**Stable ID:** `bot.kicked` · **Evidence:** source derived

The bot was removed or banned from the chat.

The response does not identify who removed the bot or guarantee that rejoining is currently allowed.

## When it matches

Every field in a rule must match. Alternative rules are joined with OR.
Codes below are JSON response fields, not inferred HTTP statuses.

### Rule 1

- JSON `error_code`: **403**.

Exact description:

```text
Forbidden: bot was kicked from the group chat
```

### Rule 2

- JSON `error_code`: **403**.

Exact description:

```text
Forbidden: bot was kicked from the supergroup chat
```

### Rule 3

- JSON `error_code`: **403**.

Exact description:

```text
Forbidden: bot was kicked from the channel chat
```

See [matching rules](/matching/) for parameter precedence
and unknown or ambiguous results.

**Illustrative methods:** `sendMessage`, `deleteMessage`.

## Possible causes

- An active group records the bot as kicked.
- The supergroup or channel membership status is banned.

## Before deciding what to do

**Application decision:** restore bot membership.
**Repeat request:** after access change.

- An authorized chat administrator must restore the bot’s access before the application resumes the operation.

These are application choices. Errorgram does not retry, suppress the error,
or change bot state.

## Facts

This condition adds no extracted facts; `result.facts` is empty.

## Example

Synthetic examples derived from the cited source.

API method: `sendMessage`.

```json
{
  "ok": false,
  "error_code": 403,
  "description": "Forbidden: bot was kicked from the group chat"
}
```

### Python

```python
from errorgram import classify

response = {
    "ok": False,
    "error_code": 403,
    "description": "Forbidden: bot was kicked from the group chat",
}
result = classify(response, method='sendMessage')

assert result.id == 'bot.kicked'
print(result.entry["summary"])
```

### JavaScript and TypeScript

```ts
import { classify } from "errorgram";

const response = {
  "ok": false,
  "error_code": 403,
  "description": "Forbidden: bot was kicked from the group chat"
};
const result = classify(response, { method: "sendMessage" });

if (result.status === "matched" && result.id === "bot.kicked") {
  console.log(result.entry.summary);
}
```

## Framework names

| Integration | Type or ID |
| --- | --- |
| Python | `errorgram.BotKicked` |
| aiogram | `errorgram.aiogram.BotKicked` extends `TelegramForbiddenError` |
| grammY | `EnrichedGrammyError` with `classification.id` equal to `bot.kicked` |

Enrichment is explicit and keeps framework catch compatibility.
Follow the [Python and aiogram guide](/python/) or
[JavaScript, TypeScript, and grammY guide](/javascript/).

## Evidence

- [Bot API 10.3 · telegram-bot-api/Client.cpp:8832–8833](https://github.com/tdlib/telegram-bot-api/blob/e3e9dd8e5b3d7ab8537cd5a10dc31d5ffa8f82d1/telegram-bot-api/Client.cpp#L8832-L8833). An active group with a kicked bot fails edit or write access. Revision `e3e9dd8e5b3d7ab8537cd5a10dc31d5ffa8f82d1`.
- [Bot API 10.3 · telegram-bot-api/Client.cpp:8840–8847](https://github.com/tdlib/telegram-bot-api/blob/e3e9dd8e5b3d7ab8537cd5a10dc31d5ffa8f82d1/telegram-bot-api/Client.cpp#L8840-L8847). Banned supergroup and channel memberships produce the corresponding descriptions. Revision `e3e9dd8e5b3d7ab8537cd5a10dc31d5ffa8f82d1`.

Source references identify the reviewed revision, not the first release
that introduced this response.

## Data and versions

Catalogue `0.1.0` · schema `1.0.0` · reviewed 2026-09-16.

[Markdown](/errors/bot.kicked.md) · [Condition JSON](/errors/bot.kicked.json) · [Full catalogue and sources](/catalogue.json) · [JSON Schema](/schema.json)
