---
title: "Message not modified · message.not_modified"
description: "The requested message content and reply markup are unchanged."
slug: "errors/message.not_modified"
editUrl: "https://github.com/uburuntu/errorgram/edit/main/catalogue/errors.json"
sidebar:
  label: "message.not_modified"
---

**Stable ID:** `message.not_modified` · **Evidence:** source derived

The requested message content and reply markup are unchanged.

The response does not include the current message or establish the history of concurrent edits.

## When it matches

Every field in a rule must match. Alternative rules are joined with OR.
Codes below are JSON response fields, not inferred HTTP statuses.

- JSON `error_code`: **400**.

Exact description:

```text
Bad Request: message is not modified: specified new message content and reply markup are exactly the same as a current content and reply markup of the message
```

See [matching rules](/matching/) for parameter precedence
and unknown or ambiguous results.

**Illustrative methods:** `editMessageText`, `editMessageCaption`, `editMessageReplyMarkup`.

## Possible causes

- The requested edit repeats the current content and markup.

## Before deciding what to do

**Application decision:** accept existing state if intended.
**Repeat request:** unhelpful without change.

- The application considers an already-applied desired state a successful outcome.

These are application choices. Errorgram does not retry, suppress the error,
or change bot state.

## Facts

This condition adds no extracted facts; `result.facts` is empty.

## Example

Synthetic examples derived from the cited source.

API method: `editMessageText`.

```json
{
  "ok": false,
  "error_code": 400,
  "description": "Bad Request: message is not modified: specified new message content and reply markup are exactly the same as a current content and reply markup of the message"
}
```

### Python

```python
from errorgram import classify

response = {
    "ok": False,
    "error_code": 400,
    "description": "Bad Request: message is not modified: specified new message content and reply markup are exactly the same as a current content and reply markup of the message",
}
result = classify(response, method='editMessageText')

assert result.id == 'message.not_modified'
print(result.entry["summary"])
```

### JavaScript and TypeScript

```ts
import { classify } from "errorgram";

const response = {
  "ok": false,
  "error_code": 400,
  "description": "Bad Request: message is not modified: specified new message content and reply markup are exactly the same as a current content and reply markup of the message"
};
const result = classify(response, { method: "editMessageText" });

if (result.status === "matched" && result.id === "message.not_modified") {
  console.log(result.entry.summary);
}
```

## Framework names

| Integration | Type or ID |
| --- | --- |
| Python | `errorgram.MessageNotModified` |
| aiogram | `errorgram.aiogram.MessageNotModified` extends `TelegramBadRequest` |
| grammY | `EnrichedGrammyError` with `classification.id` equal to `message.not_modified` |

Enrichment is explicit and keeps framework catch compatibility.
Follow the [Python and aiogram guide](/python/) or
[JavaScript, TypeScript, and grammY guide](/javascript/).

## Evidence

- [Bot API 10.3 · telegram-bot-api/Client.cpp:106–113](https://github.com/tdlib/telegram-bot-api/blob/e3e9dd8e5b3d7ab8537cd5a10dc31d5ffa8f82d1/telegram-bot-api/Client.cpp#L106-L113). MESSAGE\_NOT\_MODIFIED is rewritten here; prefix and initial-case handling are at lines 165-205. Revision `e3e9dd8e5b3d7ab8537cd5a10dc31d5ffa8f82d1`.

Source references identify the reviewed revision, not the first release
that introduced this response.

## Data and versions

Catalogue `0.1.0` · schema `1.0.0` · reviewed 2026-09-15.

[Markdown](/errors/message.not_modified.md) · [Condition JSON](/errors/message.not_modified.json) · [Full catalogue and sources](/catalogue.json) · [JSON Schema](/schema.json)
