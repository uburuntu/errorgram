# Format parse mode unsupported · format.parse\_mode\_unsupported

Canonical page: https://errorgram.rmbk.me/errors/format.parse_mode_unsupported/

**Stable ID:** `format.parse_mode_unsupported` · **Evidence:** observed

The requested parse\_mode is unsupported.

The server lowercases parse\_mode before checking it. This response does not identify a malformed entity inside a supported mode.

## When it matches

Every field in a rule must match. Alternative rules are joined with OR.
Codes below are JSON response fields, not inferred HTTP statuses.

- JSON `error_code`: **400**.

Exact description:

```text
Bad Request: unsupported parse_mode
```

See [matching rules](https://errorgram.rmbk.me/matching/) for parameter precedence
and unknown or ambiguous results.

**Illustrative methods:** `sendMessage`, `editMessageText`, `sendPhoto`.

## Possible causes

- Nonempty text was supplied with a parse\_mode that the server does not recognize.

## Before deciding what to do

**Application decision:** correct parse mode.
**Repeat request:** after relevant change.

- Choose a supported parse\_mode, or omit it and use plain text or explicit entities.

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
  "description": "Bad Request: unsupported parse_mode"
}
```

### Python

```python
from errorgram import classify

response = {
    "ok": False,
    "error_code": 400,
    "description": "Bad Request: unsupported parse_mode",
}
result = classify(response, method='sendMessage')

assert result.id == 'format.parse_mode_unsupported'
print(result.entry["summary"])
```

### JavaScript and TypeScript

```ts
import { classify } from "errorgram";

const response = {
  "ok": false,
  "error_code": 400,
  "description": "Bad Request: unsupported parse_mode"
};
const result = classify(response, { method: "sendMessage" });

if (result.status === "matched" && result.id === "format.parse_mode_unsupported") {
  console.log(result.entry.summary);
}
```

## Framework names

| Integration | Type or ID |
| --- | --- |
| Python | `errorgram.FormatParseModeUnsupported` |
| aiogram | `errorgram.aiogram.FormatParseModeUnsupported` extends `TelegramBadRequest` |
| grammY | `EnrichedGrammyError` with `classification.id` equal to `format.parse_mode_unsupported` |

Enrichment is explicit and keeps framework catch compatibility.
Follow the [Python and aiogram guide](https://errorgram.rmbk.me/python/) or
[JavaScript, TypeScript, and grammY guide](https://errorgram.rmbk.me/javascript/).

## Evidence

- [Recorded observation](https://github.com/uburuntu/errorgram/blob/4314ac1f9d29d105b10e9b537a7643cc65d097aa/observations/2026-09-16.json). sendMessage with an unsupported parse\_mode returned this description. Accessed 2026-09-16.
- [Bot API 10.3 · telegram-bot-api/Client.cpp:11961–11977](https://github.com/tdlib/telegram-bot-api/blob/e3e9dd8e5b3d7ab8537cd5a10dc31d5ffa8f82d1/telegram-bot-api/Client.cpp#L11961-L11977). Nonempty text accepts markdown, markdownv2, html, or the no-parsing path; other modes fail. Revision `e3e9dd8e5b3d7ab8537cd5a10dc31d5ffa8f82d1`.
- [Bot API 10.3 · telegram-bot-api/Client.cpp:13800–13803](https://github.com/tdlib/telegram-bot-api/blob/e3e9dd8e5b3d7ab8537cd5a10dc31d5ffa8f82d1/telegram-bot-api/Client.cpp#L13800-L13803). Method validation errors are passed to the response normalizer. Revision `e3e9dd8e5b3d7ab8537cd5a10dc31d5ffa8f82d1`.
- [Bot API 10.3 · telegram-bot-api/Client.cpp:165–205](https://github.com/tdlib/telegram-bot-api/blob/e3e9dd8e5b3d7ab8537cd5a10dc31d5ffa8f82d1/telegram-bot-api/Client.cpp#L165-L205). Adds the code-specific prefix and lowercases only the initial character of ordinary messages. Revision `e3e9dd8e5b3d7ab8537cd5a10dc31d5ffa8f82d1`.

Source references identify the reviewed revision, not the first release
that introduced this response.

## Data and versions

Catalogue `0.1.0` · schema `1.0.0` · reviewed 2026-09-16.

[Markdown](https://errorgram.rmbk.me/errors/format.parse_mode_unsupported.md) · [Condition JSON](https://errorgram.rmbk.me/errors/format.parse_mode_unsupported.json) · [Full catalogue and sources](https://errorgram.rmbk.me/catalogue.json) · [JSON Schema](https://errorgram.rmbk.me/schema.json)
