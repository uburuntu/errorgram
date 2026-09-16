# Markup invalid json · markup.invalid\_json

Canonical page: https://errorgram.rmbk.me/errors/markup.invalid_json/

**Stable ID:** `markup.invalid_json` · **Evidence:** source derived

The reply\_markup argument is not valid JSON.

Valid JSON with the wrong shape or invalid button fields produces different errors.

## When it matches

Every field in a rule must match. Alternative rules are joined with OR.
Codes below are JSON response fields, not inferred HTTP statuses.

- JSON `error_code`: **400**.

Exact description:

```text
Bad Request: can't parse reply keyboard markup JSON object
```

See [matching rules](https://errorgram.rmbk.me/matching/) for parameter precedence
and unknown or ambiguous results.

**Illustrative methods:** `sendMessage`, `editMessageReplyMarkup`.

## Possible causes

- A nonempty reply\_markup argument failed JSON decoding.

## Before deciding what to do

**Application decision:** correct reply markup json.
**Repeat request:** after relevant change.

- Serialize reply\_markup as a JSON object with the structure required by the selected keyboard type.

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
  "description": "Bad Request: can't parse reply keyboard markup JSON object"
}
```

### Python

```python
from errorgram import classify

response = {
    "ok": False,
    "error_code": 400,
    "description": "Bad Request: can't parse reply keyboard markup JSON object",
}
result = classify(response, method='sendMessage')

assert result.id == 'markup.invalid_json'
print(result.entry["summary"])
```

### JavaScript and TypeScript

```ts
import { classify } from "errorgram";

const response = {
  "ok": false,
  "error_code": 400,
  "description": "Bad Request: can't parse reply keyboard markup JSON object"
};
const result = classify(response, { method: "sendMessage" });

if (result.status === "matched" && result.id === "markup.invalid_json") {
  console.log(result.entry.summary);
}
```

## Framework names

| Integration | Type or ID |
| --- | --- |
| Python | `errorgram.MarkupInvalidJson` |
| aiogram | `errorgram.aiogram.MarkupInvalidJson` extends `TelegramBadRequest` |
| grammY | `EnrichedGrammyError` with `classification.id` equal to `markup.invalid_json` |

Enrichment is explicit and keeps framework catch compatibility.
Follow the [Python and aiogram guide](https://errorgram.rmbk.me/python/) or
[JavaScript, TypeScript, and grammY guide](https://errorgram.rmbk.me/javascript/).

## Evidence

- [Bot API 10.3 · telegram-bot-api/Client.cpp:10504–10518](https://github.com/tdlib/telegram-bot-api/blob/e3e9dd8e5b3d7ab8537cd5a10dc31d5ffa8f82d1/telegram-bot-api/Client.cpp#L10504-L10518). The reply\_markup parser emits this literal only when JSON decoding fails. Revision `e3e9dd8e5b3d7ab8537cd5a10dc31d5ffa8f82d1`.
- [Bot API 10.3 · telegram-bot-api/Client.cpp:13800–13803](https://github.com/tdlib/telegram-bot-api/blob/e3e9dd8e5b3d7ab8537cd5a10dc31d5ffa8f82d1/telegram-bot-api/Client.cpp#L13800-L13803). Method validation errors are passed to the response normalizer. Revision `e3e9dd8e5b3d7ab8537cd5a10dc31d5ffa8f82d1`.
- [Bot API 10.3 · telegram-bot-api/Client.cpp:165–205](https://github.com/tdlib/telegram-bot-api/blob/e3e9dd8e5b3d7ab8537cd5a10dc31d5ffa8f82d1/telegram-bot-api/Client.cpp#L165-L205). Adds the code-specific prefix and lowercases only the initial character of ordinary messages. Revision `e3e9dd8e5b3d7ab8537cd5a10dc31d5ffa8f82d1`.

Source references identify the reviewed revision, not the first release
that introduced this response.

## Data and versions

Catalogue `0.1.0` · schema `1.0.0` · reviewed 2026-09-16.

[Markdown](https://errorgram.rmbk.me/errors/markup.invalid_json.md) · [Condition JSON](https://errorgram.rmbk.me/errors/markup.invalid_json.json) · [Full catalogue and sources](https://errorgram.rmbk.me/catalogue.json) · [JSON Schema](https://errorgram.rmbk.me/schema.json)
