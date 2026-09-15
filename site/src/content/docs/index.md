---
title: "Telegram errors, explained."
description: "Turn broad Telegram Bot API errors into stable IDs, useful diagnostics, and typed results for Python, TypeScript, aiogram, and grammY."
sidebar:
  label: Overview
---

One `BadRequest` can mean an unchanged message, a missing chat, or a request that needs a new chat ID. Your bot needs to tell them apart.

**Errorgram gives each supported condition a stable name.** One open JSON catalogue powers the reference, Python and TypeScript bindings, and opt-in aiogram and grammY adapters.

## Find the error in front of you

Search by Telegram's response text, a condition ID, or a framework exception name. Each condition has its own page with an example, possible causes, diagnostic limits, and pinned source evidence.

| Telegram says… | Start here |
| --- | --- |
| `Bad Request: chat not found` | [chat.not_found](/errors/chat.not_found/) |
| `Bad Request: message is not modified…` | [message.not_modified](/errors/message.not_modified/) |
| `Too Many Requests: retry after…` | [request.retry_after](/errors/request.retry_after/) |
| `Forbidden: bot was blocked by the user` | [bot.blocked_by_user](/errors/bot.blocked_by_user/) |

[Browse every condition →](/catalogue/)

## Give your handler something precise

```python
from errorgram import classify

failure = classify({
    "ok": False,
    "error_code": 400,
    "description": "Bad Request: chat not found",
})

if failure.id == "chat.not_found":
    print("Check the chat ID and the bot's access.")
```

The same IDs work across languages, logs, metrics, and documentation. Your application keeps control of retries, delivery, and state changes.

| Build with | What you get |
| --- | --- |
| [Python & aiogram](/python/) | Plain response classification and concrete exception types. |
| [JavaScript, TypeScript & grammY](/javascript/) | ESM bindings, typed facts, and framework-compatible enrichment. |
| [JSON & AI agents](/agents/) | The complete catalogue, schema, and plain Markdown reference. |

## Know what the evidence supports

The first catalogue covers **15 conditions** from Bot API **10.3**. Examples are synthetic and derived from pinned server source; they have not been verified against the hosted API. Coverage will grow through reviewed contributions.

A stable ID describes the observed condition. It cannot prove every underlying cause. Unknown responses stay unknown, and transport failures and framework validation errors remain outside the catalogue.

[Get started](/getting-started/) · [How matching works](/matching/) · [Read this page as Markdown](/index.md)
