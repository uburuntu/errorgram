# Bot blocked by user · bot.blocked\_by\_user

Canonical page: https://errorgram.rmbk.me/errors/bot.blocked_by_user/

**Stable ID:** `bot.blocked_by_user` · **Evidence:** source derived

The user has blocked the bot.

The response establishes the current rejection, not that access can never be restored.

## When it matches

Every field in a rule must match. Alternative rules are joined with OR.
Codes below are JSON response fields, not inferred HTTP statuses.

- JSON `error_code`: **403**.

Exact description:

```text
Forbidden: bot was blocked by the user
```

See [matching rules](https://errorgram.rmbk.me/matching/) for parameter precedence
and unknown or ambiguous results.

**Illustrative methods:** `sendMessage`.

## Possible causes

- The recipient has blocked the bot.

## Before deciding what to do

**Application decision:** suspend sends until access changes.
**Repeat request:** after access change.

- Use application policy to track reachability and resume only when there is evidence that access changed.

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
  "description": "Forbidden: bot was blocked by the user"
}
```

### Python

```python
from errorgram import classify

response = {
    "ok": False,
    "error_code": 403,
    "description": "Forbidden: bot was blocked by the user",
}
result = classify(response, method='sendMessage')

assert result.id == 'bot.blocked_by_user'
print(result.entry["summary"])
```

### JavaScript and TypeScript

```ts
import { classify } from "errorgram";

const response = {
  "ok": false,
  "error_code": 403,
  "description": "Forbidden: bot was blocked by the user"
};
const result = classify(response, { method: "sendMessage" });

if (result.status === "matched" && result.id === "bot.blocked_by_user") {
  console.log(result.entry.summary);
}
```

## Framework names

| Integration | Type or ID |
| --- | --- |
| Python | `errorgram.BotBlockedByUser` |
| aiogram | `errorgram.aiogram.BotBlockedByUser` extends `TelegramForbiddenError` |
| grammY | `EnrichedGrammyError` with `classification.id` equal to `bot.blocked_by_user` |

Enrichment is explicit and keeps framework catch compatibility.
Follow the [Python and aiogram guide](https://errorgram.rmbk.me/python/) or
[JavaScript, TypeScript, and grammY guide](https://errorgram.rmbk.me/javascript/).

## Evidence

- [Bot API 10.3 · telegram-bot-api/Client.cpp:127–129](https://github.com/tdlib/telegram-bot-api/blob/e3e9dd8e5b3d7ab8537cd5a10dc31d5ffa8f82d1/telegram-bot-api/Client.cpp#L127-L129). USER\_IS\_BLOCKED changes both the code (to 403) and the description. Revision `e3e9dd8e5b3d7ab8537cd5a10dc31d5ffa8f82d1`.

Source references identify the reviewed revision, not the first release
that introduced this response.

## Data and versions

Catalogue `0.1.0` · schema `1.0.0` · reviewed 2026-09-15.

[Markdown](https://errorgram.rmbk.me/errors/bot.blocked_by_user.md) · [Condition JSON](https://errorgram.rmbk.me/errors/bot.blocked_by_user.json) · [Full catalogue and sources](https://errorgram.rmbk.me/catalogue.json) · [JSON Schema](https://errorgram.rmbk.me/schema.json)
