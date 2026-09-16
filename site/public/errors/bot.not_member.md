# Bot not member · bot.not\_member

Canonical page: https://errorgram.rmbk.me/errors/bot.not_member/

**Stable ID:** `bot.not_member` · **Evidence:** source derived

The bot lacks the chat membership required for this operation.

Membership requirements depend on the chat type, public access, and operation. This is separate from the explicit kicked response.

## When it matches

Every field in a rule must match. Alternative rules are joined with OR.
Codes below are JSON response fields, not inferred HTTP statuses.

### Rule 1

- JSON `error_code`: **403**.

Exact description:

```text
Forbidden: bot is not a member of the group chat
```

### Rule 2

- JSON `error_code`: **403**.

Exact description:

```text
Forbidden: bot is not a member of the supergroup chat
```

### Rule 3

- JSON `error_code`: **403**.

Exact description:

```text
Forbidden: bot is not a member of the channel chat
```

See [matching rules](https://errorgram.rmbk.me/matching/) for parameter precedence
and unknown or ambiguous results.

**Illustrative methods:** `sendMessage`, `deleteMessage`.

## Possible causes

- The bot has left an active group.
- The bot is not a member of a supergroup or channel and the requested access requires membership.

## Before deciding what to do

**Application decision:** restore bot membership.
**Repeat request:** after access change.

- Add or rejoin the bot with the required access through an authorized chat administrator before resuming.

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
  "description": "Forbidden: bot is not a member of the group chat"
}
```

### Python

```python
from errorgram import classify

response = {
    "ok": False,
    "error_code": 403,
    "description": "Forbidden: bot is not a member of the group chat",
}
result = classify(response, method='sendMessage')

assert result.id == 'bot.not_member'
print(result.entry["summary"])
```

### JavaScript and TypeScript

```ts
import { classify } from "errorgram";

const response = {
  "ok": false,
  "error_code": 403,
  "description": "Forbidden: bot is not a member of the group chat"
};
const result = classify(response, { method: "sendMessage" });

if (result.status === "matched" && result.id === "bot.not_member") {
  console.log(result.entry.summary);
}
```

## Framework names

| Integration | Type or ID |
| --- | --- |
| Python | `errorgram.BotNotMember` |
| aiogram | `errorgram.aiogram.BotNotMember` extends `TelegramForbiddenError` |
| grammY | `EnrichedGrammyError` with `classification.id` equal to `bot.not_member` |

Enrichment is explicit and keeps framework catch compatibility.
Follow the [Python and aiogram guide](https://errorgram.rmbk.me/python/) or
[JavaScript, TypeScript, and grammY guide](https://errorgram.rmbk.me/javascript/).

## Evidence

- [Bot API 10.3 · telegram-bot-api/Client.cpp:8835–8836](https://github.com/tdlib/telegram-bot-api/blob/e3e9dd8e5b3d7ab8537cd5a10dc31d5ffa8f82d1/telegram-bot-api/Client.cpp#L8835-L8836). An active group with a departed bot fails edit or write access. Revision `e3e9dd8e5b3d7ab8537cd5a10dc31d5ffa8f82d1`.
- [Bot API 10.3 · telegram-bot-api/Client.cpp:8850–8856](https://github.com/tdlib/telegram-bot-api/blob/e3e9dd8e5b3d7ab8537cd5a10dc31d5ffa8f82d1/telegram-bot-api/Client.cpp#L8850-L8856). Public visibility and requested access determine whether supergroup or channel membership is required. Revision `e3e9dd8e5b3d7ab8537cd5a10dc31d5ffa8f82d1`.
- [Bot API 10.3 · telegram-bot-api/Client.cpp:9045–9055](https://github.com/tdlib/telegram-bot-api/blob/e3e9dd8e5b3d7ab8537cd5a10dc31d5ffa8f82d1/telegram-bot-api/Client.cpp#L9045-L9055). Banned, left, and restricted nonmember statuses do not count as membership. Revision `e3e9dd8e5b3d7ab8537cd5a10dc31d5ffa8f82d1`.

Source references identify the reviewed revision, not the first release
that introduced this response.

## Data and versions

Catalogue `0.1.0` · schema `1.0.0` · reviewed 2026-09-16.

[Markdown](https://errorgram.rmbk.me/errors/bot.not_member.md) · [Condition JSON](https://errorgram.rmbk.me/errors/bot.not_member.json) · [Full catalogue and sources](https://errorgram.rmbk.me/catalogue.json) · [JSON Schema](https://errorgram.rmbk.me/schema.json)
