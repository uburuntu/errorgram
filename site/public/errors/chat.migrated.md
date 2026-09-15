# Chat migrated · chat.migrated

Canonical page: https://errorgram.rmbk.me/errors/chat.migrated/

**Stable ID:** `chat.migrated` · **Evidence:** source derived

The group has moved to a supergroup with a new ID.

Use the structured replacement identifier; a description alone does not supply the new target.

## When it matches

Every field in a rule must match. Alternative rules are joined with OR.
Codes below are JSON response fields, not inferred HTTP statuses.

- JSON `error_code`: **400**.
- `parameters.migrate_to_chat_id`: a nonzero safe integer.

The structured parameter decides the match; the description may vary.

See [matching rules](https://errorgram.rmbk.me/matching/) for parameter precedence
and unknown or ambiguous results.

**Illustrative methods:** `sendMessage`.

## Possible causes

- The request addresses a group that was upgraded to a supergroup.

## Before deciding what to do

**Application decision:** migrate chat reference.
**Repeat request:** after target update.

- Update the intended chat reference from parameters.migrate\_to\_chat\_id, account for concurrent updates, and bound retries.

These are application choices. Errorgram does not retry, suppress the error,
or change bot state.

## Facts

Values extracted into `result.facts`:

- `migrate_to_chat_id`: a nonzero safe integer, from `parameters.migrate_to_chat_id`.

## Example

Synthetic examples derived from the cited source.

API method: `sendMessage`.

```json
{
  "ok": false,
  "error_code": 400,
  "description": "Bad Request: group chat was upgraded to a supergroup chat",
  "parameters": {
    "migrate_to_chat_id": -1001234567890
  }
}
```

### Python

```python
from errorgram import classify

response = {
    "ok": False,
    "error_code": 400,
    "description": "Bad Request: group chat was upgraded to a supergroup chat",
    "parameters": {
        "migrate_to_chat_id": -1001234567890,
    },
}
result = classify(response, method='sendMessage')

assert result.id == 'chat.migrated'
print(result.entry["summary"])
```

### JavaScript and TypeScript

```ts
import { classify } from "errorgram";

const response = {
  "ok": false,
  "error_code": 400,
  "description": "Bad Request: group chat was upgraded to a supergroup chat",
  "parameters": {
    "migrate_to_chat_id": -1001234567890
  }
};
const result = classify(response, { method: "sendMessage" });

if (result.status === "matched" && result.id === "chat.migrated") {
  console.log(result.entry.summary);
}
```

## Framework names

| Integration | Type or ID |
| --- | --- |
| Python | `errorgram.ChatMigrated` |
| aiogram | `errorgram.aiogram.ChatMigrated` extends `TelegramMigrateToChat` |
| grammY | `EnrichedGrammyError` with `classification.id` equal to `chat.migrated` |

Enrichment is explicit and keeps framework catch compatibility.
Follow the [Python and aiogram guide](https://errorgram.rmbk.me/python/) or
[JavaScript, TypeScript, and grammY guide](https://errorgram.rmbk.me/javascript/).

## Evidence

- [Bot API 10.3 · telegram-bot-api/Client.cpp:8821–8827](https://github.com/tdlib/telegram-bot-api/blob/e3e9dd8e5b3d7ab8537cd5a10dc31d5ffa8f82d1/telegram-bot-api/Client.cpp#L8821-L8827). The replacement chat ID is placed in response parameters. Revision `e3e9dd8e5b3d7ab8537cd5a10dc31d5ffa8f82d1`.
- [Official documentation](https://core.telegram.org/bots/api#responseparameters). Documents migrate\_to\_chat\_id, including its maximum of 52 significant bits. Accessed 2026-09-15.

Source references identify the reviewed revision, not the first release
that introduced this response.

## Data and versions

Catalogue `0.1.0` · schema `1.0.0` · reviewed 2026-09-15.

[Markdown](https://errorgram.rmbk.me/errors/chat.migrated.md) · [Condition JSON](https://errorgram.rmbk.me/errors/chat.migrated.json) · [Full catalogue and sources](https://errorgram.rmbk.me/catalogue.json) · [JSON Schema](https://errorgram.rmbk.me/schema.json)
