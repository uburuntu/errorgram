# Session logged out · session.logged\_out

Canonical page: https://errorgram.rmbk.me/errors/session.logged_out/

**Stable ID:** `session.logged_out` · **Evidence:** source derived

The bot session has logged out.

Not every 400 response begins with Bad Request. This signature alone does not explain why logout was initiated.

## When it matches

Every field in a rule must match. Alternative rules are joined with OR.
Codes below are JSON response fields, not inferred HTTP statuses.

- JSON `error_code`: **400**.

Exact description:

```text
Logged out
```

See [matching rules](https://errorgram.rmbk.me/matching/) for parameter precedence
and unknown or ambiguous results.

## Possible causes

- The server is completing a bot logout.

## Before deciding what to do

**Application decision:** reconcile bot session lifecycle.
**Repeat request:** after lifecycle resolution.

- Determine whether logout or a server move was intentional before resuming requests.

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
  "error_code": 400,
  "description": "Logged out"
}
```

### Python

```python
from errorgram import classify

response = {
    "ok": False,
    "error_code": 400,
    "description": "Logged out",
}
result = classify(response, method='getMe')

assert result.id == 'session.logged_out'
print(result.entry["summary"])
```

### JavaScript and TypeScript

```ts
import { classify } from "errorgram";

const response = {
  "ok": false,
  "error_code": 400,
  "description": "Logged out"
};
const result = classify(response, { method: "getMe" });

if (result.status === "matched" && result.id === "session.logged_out") {
  console.log(result.entry.summary);
}
```

## Framework names

| Integration | Type or ID |
| --- | --- |
| Python | `errorgram.SessionLoggedOut` |
| aiogram | `errorgram.aiogram.SessionLoggedOut` extends `TelegramBadRequest` |
| grammY | `EnrichedGrammyError` with `classification.id` equal to `session.logged_out` |

Enrichment is explicit and keeps framework catch compatibility.
Follow the [Python and aiogram guide](https://errorgram.rmbk.me/python/) or
[JavaScript, TypeScript, and grammY guide](https://errorgram.rmbk.me/javascript/).

## Evidence

- [Bot API 10.3 · telegram-bot-api/Client.cpp:17553–17555](https://github.com/tdlib/telegram-bot-api/blob/e3e9dd8e5b3d7ab8537cd5a10dc31d5ffa8f82d1/telegram-bot-api/Client.cpp#L17553-L17555). Stores a 400 description with no Bad Request prefix. Revision `e3e9dd8e5b3d7ab8537cd5a10dc31d5ffa8f82d1`.
- [Bot API 10.3 · telegram-bot-api/Client.cpp:17520–17525](https://github.com/tdlib/telegram-bot-api/blob/e3e9dd8e5b3d7ab8537cd5a10dc31d5ffa8f82d1/telegram-bot-api/Client.cpp#L17520-L17525). The direct fail\_query path preserves that description. Revision `e3e9dd8e5b3d7ab8537cd5a10dc31d5ffa8f82d1`.

Source references identify the reviewed revision, not the first release
that introduced this response.

## Data and versions

Catalogue `0.1.0` · schema `1.0.0` · reviewed 2026-09-15.

[Markdown](https://errorgram.rmbk.me/errors/session.logged_out.md) · [Condition JSON](https://errorgram.rmbk.me/errors/session.logged_out.json) · [Full catalogue and sources](https://errorgram.rmbk.me/catalogue.json) · [JSON Schema](https://errorgram.rmbk.me/schema.json)
