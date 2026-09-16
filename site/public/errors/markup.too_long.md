# Markup too long · markup.too\_long

Canonical page: https://errorgram.rmbk.me/errors/markup.too_long/

**Stable ID:** `markup.too_long` · **Evidence:** source derived

Telegram rejected the size of the reply markup.

The mapping does not specify a size limit or identify which keyboard field exceeds it.

## When it matches

Every field in a rule must match. Alternative rules are joined with OR.
Codes below are JSON response fields, not inferred HTTP statuses.

- JSON `error_code`: **400**.

Exact description:

```text
Bad Request: reply markup is too long
```

See [matching rules](https://errorgram.rmbk.me/matching/) for parameter precedence
and unknown or ambiguous results.

**Illustrative methods:** `sendMessage`, `editMessageReplyMarkup`.

## Possible causes

- The reply markup exceeds a size constraint enforced by Telegram.

## Before deciding what to do

**Application decision:** reduce reply markup.
**Repeat request:** after relevant change.

- Reduce the keyboard or button payload and check the current limits for the chosen button types.

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
  "description": "Bad Request: reply markup is too long"
}
```

### Python

```python
from errorgram import classify

response = {
    "ok": False,
    "error_code": 400,
    "description": "Bad Request: reply markup is too long",
}
result = classify(response, method='sendMessage')

assert result.id == 'markup.too_long'
print(result.entry["summary"])
```

### JavaScript and TypeScript

```ts
import { classify } from "errorgram";

const response = {
  "ok": false,
  "error_code": 400,
  "description": "Bad Request: reply markup is too long"
};
const result = classify(response, { method: "sendMessage" });

if (result.status === "matched" && result.id === "markup.too_long") {
  console.log(result.entry.summary);
}
```

## Framework names

| Integration | Type or ID |
| --- | --- |
| Python | `errorgram.MarkupTooLong` |
| aiogram | `errorgram.aiogram.MarkupTooLong` extends `TelegramBadRequest` |
| grammY | `EnrichedGrammyError` with `classification.id` equal to `markup.too_long` |

Enrichment is explicit and keeps framework catch compatibility.
Follow the [Python and aiogram guide](https://errorgram.rmbk.me/python/) or
[JavaScript, TypeScript, and grammY guide](https://errorgram.rmbk.me/javascript/).

## Evidence

- [Bot API 10.3 · telegram-bot-api/Client.cpp:121–123](https://github.com/tdlib/telegram-bot-api/blob/e3e9dd8e5b3d7ab8537cd5a10dc31d5ffa8f82d1/telegram-bot-api/Client.cpp#L121-L123). REPLY\_MARKUP\_TOO\_LONG becomes this description in the code-400 branch. Revision `e3e9dd8e5b3d7ab8537cd5a10dc31d5ffa8f82d1`.
- [Bot API 10.3 · telegram-bot-api/Client.cpp:85–106](https://github.com/tdlib/telegram-bot-api/blob/e3e9dd8e5b3d7ab8537cd5a10dc31d5ffa8f82d1/telegram-bot-api/Client.cpp#L85-L106). Normalizes lower codes, 404, and uppercase machine-style 403 errors to 400 before rewriting. Revision `e3e9dd8e5b3d7ab8537cd5a10dc31d5ffa8f82d1`.
- [Bot API 10.3 · telegram-bot-api/Client.cpp:165–205](https://github.com/tdlib/telegram-bot-api/blob/e3e9dd8e5b3d7ab8537cd5a10dc31d5ffa8f82d1/telegram-bot-api/Client.cpp#L165-L205). Adds the code-specific prefix and lowercases only the initial character of ordinary messages. Revision `e3e9dd8e5b3d7ab8537cd5a10dc31d5ffa8f82d1`.

Source references identify the reviewed revision, not the first release
that introduced this response.

## Data and versions

Catalogue `0.1.0` · schema `1.0.0` · reviewed 2026-09-16.

[Markdown](https://errorgram.rmbk.me/errors/markup.too_long.md) · [Condition JSON](https://errorgram.rmbk.me/errors/markup.too_long.json) · [Full catalogue and sources](https://errorgram.rmbk.me/catalogue.json) · [JSON Schema](https://errorgram.rmbk.me/schema.json)
