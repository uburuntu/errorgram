# Chat not found · chat.not\_found

Canonical page: https://errorgram.rmbk.me/errors/chat.not_found/

**Stable ID:** `chat.not_found` · **Evidence:** source derived

The bot could not resolve this chat.

This is not proof that the chat was deleted, the bot was blocked, or the identifier is permanently unusable.

## When it matches

Every field in a rule must match. Alternative rules are joined with OR.
Codes below are JSON response fields, not inferred HTTP statuses.

- JSON `error_code`: **400**.

Exact description:

```text
Bad Request: chat not found
```

See [matching rules](https://errorgram.rmbk.me/matching/) for parameter precedence
and unknown or ambiguous results.

**Illustrative methods:** `sendMessage`, `getChat`.

## Possible causes

- An upstream lookup error was replaced with the generic chat lookup message.
- A username resolved to a chat type that this lookup does not allow.

## Before deciding what to do

**Application decision:** inspect target and access.
**Repeat request:** after relevant change.

- Verify the identifier, target type and bot access before changing stored chat records.

These are application choices. Errorgram does not retry, suppress the error,
or change bot state.

## Facts

This condition adds no extracted facts; `result.facts` is empty.

## Example

Synthetic examples derived from the cited source.

API method: `getChat`.

```json
{
  "ok": false,
  "error_code": 400,
  "description": "Bad Request: chat not found"
}
```

### Python

```python
from errorgram import classify

response = {
    "ok": False,
    "error_code": 400,
    "description": "Bad Request: chat not found",
}
result = classify(response, method='getChat')

assert result.id == 'chat.not_found'
print(result.entry["summary"])
```

### JavaScript and TypeScript

```ts
import { classify } from "errorgram";

const response = {
  "ok": false,
  "error_code": 400,
  "description": "Bad Request: chat not found"
};
const result = classify(response, { method: "getChat" });

if (result.status === "matched" && result.id === "chat.not_found") {
  console.log(result.entry.summary);
}
```

## Framework names

| Integration | Type or ID |
| --- | --- |
| Python | `errorgram.ChatNotFound` |
| aiogram | `errorgram.aiogram.ChatNotFound` extends `TelegramBadRequest` |
| grammY | `EnrichedGrammyError` with `classification.id` equal to `chat.not_found` |

Enrichment is explicit and keeps framework catch compatibility.
Follow the [Python and aiogram guide](https://errorgram.rmbk.me/python/) or
[JavaScript, TypeScript, and grammY guide](https://errorgram.rmbk.me/javascript/).

## Evidence

- [Bot API 10.3 · telegram-bot-api/Client.cpp:7239–7266](https://github.com/tdlib/telegram-bot-api/blob/e3e9dd8e5b3d7ab8537cd5a10dc31d5ffa8f82d1/telegram-bot-api/Client.cpp#L7239-L7266). A fallback masks upstream 400-class errors, and a separate local branch emits the same description. Revision `e3e9dd8e5b3d7ab8537cd5a10dc31d5ffa8f82d1`.
- [Bot API 10.3 · telegram-bot-api/Client.cpp:85–108](https://github.com/tdlib/telegram-bot-api/blob/e3e9dd8e5b3d7ab8537cd5a10dc31d5ffa8f82d1/telegram-bot-api/Client.cpp#L85-L108). Some upstream codes are converted to 400 before the fallback description is applied. Revision `e3e9dd8e5b3d7ab8537cd5a10dc31d5ffa8f82d1`.

Source references identify the reviewed revision, not the first release
that introduced this response.

## Data and versions

Catalogue `0.1.0` · schema `1.0.0` · reviewed 2026-09-15.

[Markdown](https://errorgram.rmbk.me/errors/chat.not_found.md) · [Condition JSON](https://errorgram.rmbk.me/errors/chat.not_found.json) · [Full catalogue and sources](https://errorgram.rmbk.me/catalogue.json) · [JSON Schema](https://errorgram.rmbk.me/schema.json)
