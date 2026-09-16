# Query invalid or expired · query.invalid\_or\_expired

Canonical page: https://errorgram.rmbk.me/errors/query.invalid_or_expired/

**Stable ID:** `query.invalid_or_expired` · **Evidence:** source derived

The query ID is invalid or its response window has expired.

The description explicitly combines causes; it does not establish a universal timeout duration.

## When it matches

Every field in a rule must match. Alternative rules are joined with OR.
Codes below are JSON response fields, not inferred HTTP statuses.

- JSON `error_code`: **400**.

Exact description:

```text
Bad Request: query is too old and response timeout expired or query ID is invalid
```

See [matching rules](https://errorgram.rmbk.me/matching/) for parameter precedence
and unknown or ambiguous results.

**Illustrative methods:** `answerCallbackQuery`.

## Possible causes

- The query identifier is invalid.
- The response arrived after the query's response window.

## Before deciding what to do

**Application decision:** verify identifier and response timing.
**Repeat request:** unhelpful for expired identifier.

- Use the identifier from the correct incoming query and respond promptly to future queries.

These are application choices. Errorgram does not retry, suppress the error,
or change bot state.

## Facts

This condition adds no extracted facts; `result.facts` is empty.

## Example

Synthetic examples derived from the cited source.

API method: `answerCallbackQuery`.

```json
{
  "ok": false,
  "error_code": 400,
  "description": "Bad Request: query is too old and response timeout expired or query ID is invalid"
}
```

### Python

```python
from errorgram import classify

response = {
    "ok": False,
    "error_code": 400,
    "description": "Bad Request: query is too old and response timeout expired or query ID is invalid",
}
result = classify(response, method='answerCallbackQuery')

assert result.id == 'query.invalid_or_expired'
print(result.entry["summary"])
```

### JavaScript and TypeScript

```ts
import { classify } from "errorgram";

const response = {
  "ok": false,
  "error_code": 400,
  "description": "Bad Request: query is too old and response timeout expired or query ID is invalid"
};
const result = classify(response, { method: "answerCallbackQuery" });

if (result.status === "matched" && result.id === "query.invalid_or_expired") {
  console.log(result.entry.summary);
}
```

## Framework names

| Integration | Type or ID |
| --- | --- |
| Python | `errorgram.QueryInvalidOrExpired` |
| aiogram | `errorgram.aiogram.QueryInvalidOrExpired` extends `TelegramBadRequest` |
| grammY | `EnrichedGrammyError` with `classification.id` equal to `query.invalid_or_expired` |

Enrichment is explicit and keeps framework catch compatibility.
Follow the [Python and aiogram guide](https://errorgram.rmbk.me/python/) or
[JavaScript, TypeScript, and grammY guide](https://errorgram.rmbk.me/javascript/).

## Evidence

- [Bot API 10.3 · telegram-bot-api/Client.cpp:148–150](https://github.com/tdlib/telegram-bot-api/blob/e3e9dd8e5b3d7ab8537cd5a10dc31d5ffa8f82d1/telegram-bot-api/Client.cpp#L148-L150). QUERY\_ID\_INVALID is deliberately expanded to a description containing alternatives. Revision `e3e9dd8e5b3d7ab8537cd5a10dc31d5ffa8f82d1`.

Source references identify the reviewed revision, not the first release
that introduced this response.

## Data and versions

Catalogue `0.1.0` · schema `1.0.0` · reviewed 2026-09-16.

[Markdown](https://errorgram.rmbk.me/errors/query.invalid_or_expired.md) · [Condition JSON](https://errorgram.rmbk.me/errors/query.invalid_or_expired.json) · [Full catalogue and sources](https://errorgram.rmbk.me/catalogue.json) · [JSON Schema](https://errorgram.rmbk.me/schema.json)
