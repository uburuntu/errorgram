---
title: "Member is administrator · member.is_administrator"
description: "The operation was rejected because the target user is a chat administrator."
slug: "errors/member.is_administrator"
editUrl: "https://github.com/uburuntu/errorgram/edit/main/catalogue/errors.json"
sidebar:
  label: "member.is_administrator"
---

**Stable ID:** `member.is_administrator` · **Evidence:** source derived

The operation was rejected because the target user is a chat administrator.

The mapping does not identify the user’s exact administrative role or authorize changing it.

## When it matches

Every field in a rule must match. Alternative rules are joined with OR.
Codes below are JSON response fields, not inferred HTTP statuses.

- JSON `error_code`: **400**.

Exact description:

```text
Bad Request: user is an administrator of the chat
```

See [matching rules](/matching/) for parameter precedence
and unknown or ambiguous results.

**Illustrative methods:** `banChatMember`, `restrictChatMember`.

## Possible causes

- The requested action targets a chat administrator.

## Before deciding what to do

**Application decision:** review target member role.
**Repeat request:** after relevant change.

- Confirm the intended user and current role; any necessary role change must follow the chat’s authorization policy.

These are application choices. Errorgram does not retry, suppress the error,
or change bot state.

## Facts

This condition adds no extracted facts; `result.facts` is empty.

## Example

Synthetic examples derived from the cited source.

API method: `banChatMember`.

```json
{
  "ok": false,
  "error_code": 400,
  "description": "Bad Request: user is an administrator of the chat"
}
```

### Python

```python
from errorgram import classify

response = {
    "ok": False,
    "error_code": 400,
    "description": "Bad Request: user is an administrator of the chat",
}
result = classify(response, method='banChatMember')

assert result.id == 'member.is_administrator'
print(result.entry["summary"])
```

### JavaScript and TypeScript

```ts
import { classify } from "errorgram";

const response = {
  "ok": false,
  "error_code": 400,
  "description": "Bad Request: user is an administrator of the chat"
};
const result = classify(response, { method: "banChatMember" });

if (result.status === "matched" && result.id === "member.is_administrator") {
  console.log(result.entry.summary);
}
```

## Framework names

| Integration | Type or ID |
| --- | --- |
| Python | `errorgram.MemberIsAdministrator` |
| aiogram | `errorgram.aiogram.MemberIsAdministrator` extends `TelegramBadRequest` |
| grammY | `EnrichedGrammyError` with `classification.id` equal to `member.is_administrator` |

Enrichment is explicit and keeps framework catch compatibility.
Follow the [Python and aiogram guide](/python/) or
[JavaScript, TypeScript, and grammY guide](/javascript/).

## Evidence

- [Bot API 10.3 · telegram-bot-api/Client.cpp:130–132](https://github.com/tdlib/telegram-bot-api/blob/e3e9dd8e5b3d7ab8537cd5a10dc31d5ffa8f82d1/telegram-bot-api/Client.cpp#L130-L132). USER\_ADMIN\_INVALID becomes this description with code 400. Revision `e3e9dd8e5b3d7ab8537cd5a10dc31d5ffa8f82d1`.
- [Bot API 10.3 · telegram-bot-api/Client.cpp:85–106](https://github.com/tdlib/telegram-bot-api/blob/e3e9dd8e5b3d7ab8537cd5a10dc31d5ffa8f82d1/telegram-bot-api/Client.cpp#L85-L106). Uppercase machine-style 403 errors can become 400 before this rewrite. Revision `e3e9dd8e5b3d7ab8537cd5a10dc31d5ffa8f82d1`.
- [Bot API 10.3 · telegram-bot-api/Client.cpp:165–205](https://github.com/tdlib/telegram-bot-api/blob/e3e9dd8e5b3d7ab8537cd5a10dc31d5ffa8f82d1/telegram-bot-api/Client.cpp#L165-L205). Adds the code-specific prefix and lowercases only the initial character of ordinary messages. Revision `e3e9dd8e5b3d7ab8537cd5a10dc31d5ffa8f82d1`.

Source references identify the reviewed revision, not the first release
that introduced this response.

## Data and versions

Catalogue `0.1.0` · schema `1.0.0` · reviewed 2026-09-16.

[Markdown](/errors/member.is_administrator.md) · [Condition JSON](/errors/member.is_administrator.json) · [Full catalogue and sources](/catalogue.json) · [JSON Schema](/schema.json)
