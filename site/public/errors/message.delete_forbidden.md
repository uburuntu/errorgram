# Message delete forbidden · message.delete\_forbidden

Canonical page: https://errorgram.rmbk.me/errors/message.delete_forbidden/

**Stable ID:** `message.delete_forbidden` · **Evidence:** source derived

Telegram rejected deletion of the message.

The source proves the response mapping, not which deletion restriction caused a particular failure. The causes above are diagnostic hypotheses.

## When it matches

Every field in a rule must match. Alternative rules are joined with OR.
Codes below are JSON response fields, not inferred HTTP statuses.

- JSON `error_code`: **400**.

Exact description:

```text
Bad Request: message can't be deleted
```

See [matching rules](https://errorgram.rmbk.me/matching/) for parameter precedence
and unknown or ambiguous results.

**Illustrative methods:** `deleteMessage`, `deleteMessages`.

## Possible causes

- A permissions, message-type or message-age restriction may prevent deletion.

## Before deciding what to do

**Application decision:** check deletion eligibility.
**Repeat request:** after relevant change.

- Check the current deleteMessage rules and bot permissions; a permanent message restriction may have no repair.

These are application choices. Errorgram does not retry, suppress the error,
or change bot state.

## Facts

This condition adds no extracted facts; `result.facts` is empty.

## Example

Synthetic examples derived from the cited source.

API method: `deleteMessage`.

```json
{
  "ok": false,
  "error_code": 400,
  "description": "Bad Request: message can't be deleted"
}
```

### Python

```python
from errorgram import classify

response = {
    "ok": False,
    "error_code": 400,
    "description": "Bad Request: message can't be deleted",
}
result = classify(response, method='deleteMessage')

assert result.id == 'message.delete_forbidden'
print(result.entry["summary"])
```

### JavaScript and TypeScript

```ts
import { classify } from "errorgram";

const response = {
  "ok": false,
  "error_code": 400,
  "description": "Bad Request: message can't be deleted"
};
const result = classify(response, { method: "deleteMessage" });

if (result.status === "matched" && result.id === "message.delete_forbidden") {
  console.log(result.entry.summary);
}
```

## Framework names

| Integration | Type or ID |
| --- | --- |
| Python | `errorgram.MessageDeleteForbidden` |
| aiogram | `errorgram.aiogram.MessageDeleteForbidden` extends `TelegramBadRequest` |
| grammY | `EnrichedGrammyError` with `classification.id` equal to `message.delete_forbidden` |

Enrichment is explicit and keeps framework catch compatibility.
Follow the [Python and aiogram guide](https://errorgram.rmbk.me/python/) or
[JavaScript, TypeScript, and grammY guide](https://errorgram.rmbk.me/javascript/).

## Evidence

- [Bot API 10.3 · telegram-bot-api/Client.cpp:151–153](https://github.com/tdlib/telegram-bot-api/blob/e3e9dd8e5b3d7ab8537cd5a10dc31d5ffa8f82d1/telegram-bot-api/Client.cpp#L151-L153). MESSAGE\_DELETE\_FORBIDDEN is rewritten before the Bad Request prefix is added. Revision `e3e9dd8e5b3d7ab8537cd5a10dc31d5ffa8f82d1`.

Source references identify the reviewed revision, not the first release
that introduced this response.

## Data and versions

Catalogue `0.1.0` · schema `1.0.0` · reviewed 2026-09-16.

[Markdown](https://errorgram.rmbk.me/errors/message.delete_forbidden.md) · [Condition JSON](https://errorgram.rmbk.me/errors/message.delete_forbidden.json) · [Full catalogue and sources](https://errorgram.rmbk.me/catalogue.json) · [JSON Schema](https://errorgram.rmbk.me/schema.json)
