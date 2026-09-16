# Format entity type unsupported · format.entity\_type\_unsupported

Canonical page: https://errorgram.rmbk.me/errors/format.entity_type_unsupported/

**Stable ID:** `format.entity_type_unsupported` · **Evidence:** source derived

A message entity specifies an unsupported type.

The response does not identify the offending array item or establish whether its other fields are valid.

## When it matches

Every field in a rule must match. Alternative rules are joined with OR.
Codes below are JSON response fields, not inferred HTTP statuses.

- JSON `error_code`: **400**.

Exact description:

```text
Bad Request: can't parse MessageEntity: Unsupported type specified
```

See [matching rules](https://errorgram.rmbk.me/matching/) for parameter precedence
and unknown or ambiguous results.

**Illustrative methods:** `sendMessage`, `editMessageText`, `sendPhoto`.

## Possible causes

- An entity object uses a type that the server’s entity parser does not support.

## Before deciding what to do

**Application decision:** correct entity type.
**Repeat request:** after relevant change.

- Use a supported MessageEntity type and include its required fields.

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
  "description": "Bad Request: can't parse MessageEntity: Unsupported type specified"
}
```

### Python

```python
from errorgram import classify

response = {
    "ok": False,
    "error_code": 400,
    "description": "Bad Request: can't parse MessageEntity: Unsupported type specified",
}
result = classify(response, method='sendMessage')

assert result.id == 'format.entity_type_unsupported'
print(result.entry["summary"])
```

### JavaScript and TypeScript

```ts
import { classify } from "errorgram";

const response = {
  "ok": false,
  "error_code": 400,
  "description": "Bad Request: can't parse MessageEntity: Unsupported type specified"
};
const result = classify(response, { method: "sendMessage" });

if (result.status === "matched" && result.id === "format.entity_type_unsupported") {
  console.log(result.entry.summary);
}
```

## Framework names

| Integration | Type or ID |
| --- | --- |
| Python | `errorgram.FormatEntityTypeUnsupported` |
| aiogram | `errorgram.aiogram.FormatEntityTypeUnsupported` extends `TelegramBadRequest` |
| grammY | `EnrichedGrammyError` with `classification.id` equal to `format.entity_type_unsupported` |

Enrichment is explicit and keeps framework catch compatibility.
Follow the [Python and aiogram guide](https://errorgram.rmbk.me/python/) or
[JavaScript, TypeScript, and grammY guide](https://errorgram.rmbk.me/javascript/).

## Evidence

- [Bot API 10.3 · telegram-bot-api/Client.cpp:11929–11946](https://github.com/tdlib/telegram-bot-api/blob/e3e9dd8e5b3d7ab8537cd5a10dc31d5ffa8f82d1/telegram-bot-api/Client.cpp#L11929-L11946). Unrecognized entity types return this literal, which propagates through get\_text\_entity. Revision `e3e9dd8e5b3d7ab8537cd5a10dc31d5ffa8f82d1`.
- [Bot API 10.3 · telegram-bot-api/Client.cpp:11984–11989](https://github.com/tdlib/telegram-bot-api/blob/e3e9dd8e5b3d7ab8537cd5a10dc31d5ffa8f82d1/telegram-bot-api/Client.cpp#L11984-L11989). The formatting helper wraps the item error with an explicit 400 code and preserves its initial capital. Revision `e3e9dd8e5b3d7ab8537cd5a10dc31d5ffa8f82d1`.
- [Bot API 10.3 · telegram-bot-api/Client.cpp:13800–13803](https://github.com/tdlib/telegram-bot-api/blob/e3e9dd8e5b3d7ab8537cd5a10dc31d5ffa8f82d1/telegram-bot-api/Client.cpp#L13800-L13803). Method validation errors are passed to the response normalizer. Revision `e3e9dd8e5b3d7ab8537cd5a10dc31d5ffa8f82d1`.
- [Bot API 10.3 · telegram-bot-api/Client.cpp:165–205](https://github.com/tdlib/telegram-bot-api/blob/e3e9dd8e5b3d7ab8537cd5a10dc31d5ffa8f82d1/telegram-bot-api/Client.cpp#L165-L205). Adds the code-specific prefix and lowercases only the initial character of ordinary messages. Revision `e3e9dd8e5b3d7ab8537cd5a10dc31d5ffa8f82d1`.

Source references identify the reviewed revision, not the first release
that introduced this response.

## Data and versions

Catalogue `0.1.0` · schema `1.0.0` · reviewed 2026-09-16.

[Markdown](https://errorgram.rmbk.me/errors/format.entity_type_unsupported.md) · [Condition JSON](https://errorgram.rmbk.me/errors/format.entity_type_unsupported.json) · [Full catalogue and sources](https://errorgram.rmbk.me/catalogue.json) · [JSON Schema](https://errorgram.rmbk.me/schema.json)
