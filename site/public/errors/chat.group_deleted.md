# Chat group deleted · chat.group\_deleted

Canonical page: https://errorgram.rmbk.me/errors/chat.group_deleted/

**Stable ID:** `chat.group_deleted` · **Evidence:** source derived

Telegram reports that the group chat was deleted.

This signature is distinct from group migration and does not supply a replacement chat identifier.

## When it matches

Every field in a rule must match. Alternative rules are joined with OR.
Codes below are JSON response fields, not inferred HTTP statuses.

- JSON `error_code`: **403**.

Exact description:

```text
Forbidden: the group chat was deleted
```

See [matching rules](https://errorgram.rmbk.me/matching/) for parameter precedence
and unknown or ambiguous results.

**Illustrative methods:** `sendMessage`, `getChatAdministrators`.

## Possible causes

- The basic group is inactive and has no recorded supergroup replacement in this access check.

## Before deciding what to do

**Application decision:** retire or review chat target.
**Repeat request:** after relevant change.

- Review the stored target and stop repeated sends; use a replacement only when it is independently established.

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
  "error_code": 403,
  "description": "Forbidden: the group chat was deleted"
}
```

### Python

```python
from errorgram import classify

response = {
    "ok": False,
    "error_code": 403,
    "description": "Forbidden: the group chat was deleted",
}
result = classify(response, method='sendMessage')

assert result.id == 'chat.group_deleted'
print(result.entry["summary"])
```

### JavaScript and TypeScript

```ts
import { classify } from "errorgram";

const response = {
  "ok": false,
  "error_code": 403,
  "description": "Forbidden: the group chat was deleted"
};
const result = classify(response, { method: "sendMessage" });

if (result.status === "matched" && result.id === "chat.group_deleted") {
  console.log(result.entry.summary);
}
```

## Framework names

| Integration | Type or ID |
| --- | --- |
| Python | `errorgram.ChatGroupDeleted` |
| aiogram | `errorgram.aiogram.ChatGroupDeleted` extends `TelegramForbiddenError` |
| grammY | `EnrichedGrammyError` with `classification.id` equal to `chat.group_deleted` |

Enrichment is explicit and keeps framework catch compatibility.
Follow the [Python and aiogram guide](https://errorgram.rmbk.me/python/) or
[JavaScript, TypeScript, and grammY guide](https://errorgram.rmbk.me/javascript/).

## Evidence

- [Bot API 10.3 · telegram-bot-api/Client.cpp:8814–8829](https://github.com/tdlib/telegram-bot-api/blob/e3e9dd8e5b3d7ab8537cd5a10dc31d5ffa8f82d1/telegram-bot-api/Client.cpp#L8814-L8829). The inactive-group branch distinguishes a recorded migration from the deleted-group response. Revision `e3e9dd8e5b3d7ab8537cd5a10dc31d5ffa8f82d1`.

Source references identify the reviewed revision, not the first release
that introduced this response.

## Data and versions

Catalogue `0.1.0` · schema `1.0.0` · reviewed 2026-09-16.

[Markdown](https://errorgram.rmbk.me/errors/chat.group_deleted.md) · [Condition JSON](https://errorgram.rmbk.me/errors/chat.group_deleted.json) · [Full catalogue and sources](https://errorgram.rmbk.me/catalogue.json) · [JSON Schema](https://errorgram.rmbk.me/schema.json)
