# Format entity not object · format.entity\_not\_object

Canonical page: https://errorgram.rmbk.me/errors/format.entity_not_object/

**Stable ID:** `format.entity_not_object` · **Evidence:** source derived

An item in the message entities array is not a JSON object.

This identifies an item-shape failure, not invalid offsets, lengths, or markup syntax.

## When it matches

Every field in a rule must match. Alternative rules are joined with OR.
Codes below are JSON response fields, not inferred HTTP statuses.

- JSON `error_code`: **400**.

Exact description:

```text
Bad Request: can't parse MessageEntity: expected an Object
```

See [matching rules](https://errorgram.rmbk.me/matching/) for parameter precedence
and unknown or ambiguous results.

**Illustrative methods:** `sendMessage`, `editMessageText`, `sendPhoto`.

## Possible causes

- An entities or caption\_entities array contains a non-object item.

## Before deciding what to do

**Application decision:** correct entity objects.
**Repeat request:** after relevant change.

- Provide each entity as an object with the fields required by its type, using the API’s UTF-16 offset convention.

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
  "error_code": 400,
  "description": "Bad Request: can't parse MessageEntity: expected an Object"
}
```

### Python

```python
from errorgram import classify

response = {
    "ok": False,
    "error_code": 400,
    "description": "Bad Request: can't parse MessageEntity: expected an Object",
}
result = classify(response, method='sendMessage')

assert result.id == 'format.entity_not_object'
print(result.entry["summary"])
```

### JavaScript and TypeScript

```ts
import { classify } from "errorgram";

const response = {
  "ok": false,
  "error_code": 400,
  "description": "Bad Request: can't parse MessageEntity: expected an Object"
};
const result = classify(response, { method: "sendMessage" });

if (result.status === "matched" && result.id === "format.entity_not_object") {
  console.log(result.entry.summary);
}
```

## Framework names

| Integration | Type or ID |
| --- | --- |
| Python | `errorgram.FormatEntityNotObject` |
| aiogram | `errorgram.aiogram.FormatEntityNotObject` extends `TelegramBadRequest` |
| grammY | `EnrichedGrammyError` with `classification.id` equal to `format.entity_not_object` |

Enrichment is explicit and keeps framework catch compatibility.
Follow the [Python and aiogram guide](https://errorgram.rmbk.me/python/) or
[JavaScript, TypeScript, and grammY guide](https://errorgram.rmbk.me/javascript/).

## Evidence

- [Bot API 10.3 · telegram-bot-api/Client.cpp:11938–11946](https://github.com/tdlib/telegram-bot-api/blob/e3e9dd8e5b3d7ab8537cd5a10dc31d5ffa8f82d1/telegram-bot-api/Client.cpp#L11938-L11946). Entity parsing rejects a non-object item before reading its fields. Revision `e3e9dd8e5b3d7ab8537cd5a10dc31d5ffa8f82d1`.
- [Bot API 10.3 · telegram-bot-api/Client.cpp:11984–11989](https://github.com/tdlib/telegram-bot-api/blob/e3e9dd8e5b3d7ab8537cd5a10dc31d5ffa8f82d1/telegram-bot-api/Client.cpp#L11984-L11989). The formatting helper wraps the item error in the MessageEntity description with code 400. Revision `e3e9dd8e5b3d7ab8537cd5a10dc31d5ffa8f82d1`.
- [Bot API 10.3 · telegram-bot-api/Client.cpp:13800–13803](https://github.com/tdlib/telegram-bot-api/blob/e3e9dd8e5b3d7ab8537cd5a10dc31d5ffa8f82d1/telegram-bot-api/Client.cpp#L13800-L13803). Method validation errors are passed to the response normalizer. Revision `e3e9dd8e5b3d7ab8537cd5a10dc31d5ffa8f82d1`.
- [Bot API 10.3 · telegram-bot-api/Client.cpp:165–205](https://github.com/tdlib/telegram-bot-api/blob/e3e9dd8e5b3d7ab8537cd5a10dc31d5ffa8f82d1/telegram-bot-api/Client.cpp#L165-L205). Adds the code-specific prefix and lowercases only the initial character of ordinary messages. Revision `e3e9dd8e5b3d7ab8537cd5a10dc31d5ffa8f82d1`.

Source references identify the reviewed revision, not the first release
that introduced this response.

## Data and versions

Catalogue `0.1.0` · schema `1.0.0` · reviewed 2026-09-16.

[Markdown](https://errorgram.rmbk.me/errors/format.entity_not_object.md) · [Condition JSON](https://errorgram.rmbk.me/errors/format.entity_not_object.json) · [Full catalogue and sources](https://errorgram.rmbk.me/catalogue.json) · [JSON Schema](https://errorgram.rmbk.me/schema.json)
