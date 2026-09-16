# Routing token not served · routing.token\_not\_served

Canonical page: https://errorgram.rmbk.me/errors/routing.token_not_served/

**Stable ID:** `routing.token_not_served` · **Evidence:** source derived

The token failed the server’s bot-ID or routing check.

The same response covers a routing failure and a token-format failure; it does not prove that Telegram revoked the token.

## When it matches

Every field in a rule must match. Alternative rules are joined with OR.
Codes below are JSON response fields, not inferred HTTP statuses.

- JSON `error_code`: **421**.

Exact description:

```text
Misdirected Request: forbidden token specified
```

See [matching rules](https://errorgram.rmbk.me/matching/) for parameter precedence
and unknown or ambiguous results.

**Illustrative methods:** `getMe`.

Relevant to the open-source server's token-range routing; hosted occurrence is unverified.

## Possible causes

- The bot ID is outside the server’s configured token range.
- The token’s numeric prefix could not be parsed.

## Before deciding what to do

**Application decision:** inspect token prefix and server routing.
**Repeat request:** after configuration change.

- Check token formatting and, when operating a local server, its token-range configuration.

These are application choices. Errorgram does not retry, suppress the error,
or change bot state.

## Facts

This condition adds no extracted facts; `result.facts` is empty.

## Example

Synthetic examples derived from the cited source.

API method: `getMe`.

```json
{
  "ok": false,
  "error_code": 421,
  "description": "Misdirected Request: forbidden token specified"
}
```

### Python

```python
from errorgram import classify

response = {
    "ok": False,
    "error_code": 421,
    "description": "Misdirected Request: forbidden token specified",
}
result = classify(response, method='getMe')

assert result.id == 'routing.token_not_served'
print(result.entry["summary"])
```

### JavaScript and TypeScript

```ts
import { classify } from "errorgram";

const response = {
  "ok": false,
  "error_code": 421,
  "description": "Misdirected Request: forbidden token specified"
};
const result = classify(response, { method: "getMe" });

if (result.status === "matched" && result.id === "routing.token_not_served") {
  console.log(result.entry.summary);
}
```

## Framework names

| Integration | Type or ID |
| --- | --- |
| Python | `errorgram.RoutingTokenNotServed` |
| aiogram | `errorgram.aiogram.RoutingTokenNotServed` extends `TelegramAPIError` |
| grammY | `EnrichedGrammyError` with `classification.id` equal to `routing.token_not_served` |

Enrichment is explicit and keeps framework catch compatibility.
Follow the [Python and aiogram guide](https://errorgram.rmbk.me/python/) or
[JavaScript, TypeScript, and grammY guide](https://errorgram.rmbk.me/javascript/).

## Evidence

- [Bot API 10.3 · telegram-bot-api/ClientManager.cpp:78–80](https://github.com/tdlib/telegram-bot-api/blob/e3e9dd8e5b3d7ab8537cd5a10dc31d5ffa8f82d1/telegram-bot-api/ClientManager.cpp#L78-L80). Both sides of the condition emit the same 421 response. Revision `e3e9dd8e5b3d7ab8537cd5a10dc31d5ffa8f82d1`.

Source references identify the reviewed revision, not the first release
that introduced this response.

## Data and versions

Catalogue `0.1.0` · schema `1.0.0` · reviewed 2026-09-16.

[Markdown](https://errorgram.rmbk.me/errors/routing.token_not_served.md) · [Condition JSON](https://errorgram.rmbk.me/errors/routing.token_not_served.json) · [Full catalogue and sources](https://errorgram.rmbk.me/catalogue.json) · [JSON Schema](https://errorgram.rmbk.me/schema.json)
