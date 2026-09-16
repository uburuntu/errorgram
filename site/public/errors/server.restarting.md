# Server restarting · server.restarting

Canonical page: https://errorgram.rmbk.me/errors/server.restarting/

**Stable ID:** `server.restarting` · **Evidence:** source derived

The bot client is closing for a server restart.

An exception wrapper that discarded the original 5xx description cannot recover this distinction from the status alone.

## When it matches

Every field in a rule must match. Alternative rules are joined with OR.
Codes below are JSON response fields, not inferred HTTP statuses.

- JSON `error_code`: **500**.

Exact description:

```text
Internal Server Error: restart
```

See [matching rules](https://errorgram.rmbk.me/matching/) for parameter precedence
and unknown or ambiguous results.

## Possible causes

- The bot client is closing without taking the logout branches.

## Before deciding what to do

**Application decision:** backoff and reassess operation.
**Repeat request:** policy dependent.

- Apply bounded backoff and evaluate whether repeating the particular operation is safe; do not derive replay safety from a 5xx status alone.

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
  "error_code": 500,
  "description": "Internal Server Error: restart"
}
```

### Python

```python
from errorgram import classify

response = {
    "ok": False,
    "error_code": 500,
    "description": "Internal Server Error: restart",
}
result = classify(response, method='getMe')

assert result.id == 'server.restarting'
print(result.entry["summary"])
```

### JavaScript and TypeScript

```ts
import { classify } from "errorgram";

const response = {
  "ok": false,
  "error_code": 500,
  "description": "Internal Server Error: restart"
};
const result = classify(response, { method: "getMe" });

if (result.status === "matched" && result.id === "server.restarting") {
  console.log(result.entry.summary);
}
```

## Framework names

| Integration | Type or ID |
| --- | --- |
| Python | `errorgram.ServerRestarting` |
| aiogram | `errorgram.aiogram.ServerRestarting` extends `RestartingTelegram` |
| grammY | `EnrichedGrammyError` with `classification.id` equal to `server.restarting` |

Enrichment is explicit and keeps framework catch compatibility.
Follow the [Python and aiogram guide](https://errorgram.rmbk.me/python/) or
[JavaScript, TypeScript, and grammY guide](https://errorgram.rmbk.me/javascript/).

## Evidence

- [Bot API 10.3 · telegram-bot-api/Client.cpp:17560–17564](https://github.com/tdlib/telegram-bot-api/blob/e3e9dd8e5b3d7ab8537cd5a10dc31d5ffa8f82d1/telegram-bot-api/Client.cpp#L17560-L17564). The closing error is passed directly to fail\_query by fail\_query\_closing. Revision `e3e9dd8e5b3d7ab8537cd5a10dc31d5ffa8f82d1`.

Source references identify the reviewed revision, not the first release
that introduced this response.

## Data and versions

Catalogue `0.1.0` · schema `1.0.0` · reviewed 2026-09-16.

[Markdown](https://errorgram.rmbk.me/errors/server.restarting.md) · [Condition JSON](https://errorgram.rmbk.me/errors/server.restarting.json) · [Full catalogue and sources](https://errorgram.rmbk.me/catalogue.json) · [JSON Schema](https://errorgram.rmbk.me/schema.json)
