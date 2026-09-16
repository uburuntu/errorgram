# Telegram errors, explained.

Canonical page: https://errorgram.rmbk.me/

One `BadRequest` can mean an unchanged message, a missing chat, or a request that needs a new chat ID. Your bot needs to tell them apart.

**Errorgram gives each supported condition a stable name.** One open JSON catalogue powers the reference, Python and TypeScript bindings, and opt-in aiogram and grammY adapters.

## Find the error in front of you

Search by Telegram's response text, a condition ID, or a framework exception name. Each condition has its own page with an example, possible causes, diagnostic limits, and pinned source evidence.

| Telegram says… | Start here |
| --- | --- |
| `Bad Request: chat not found` | [chat.not_found](https://errorgram.rmbk.me/errors/chat.not_found/) |
| `Bad Request: message is not modified…` | [message.not_modified](https://errorgram.rmbk.me/errors/message.not_modified/) |
| `Too Many Requests: retry after…` | [request.retry_after](https://errorgram.rmbk.me/errors/request.retry_after/) |
| `Forbidden: bot was blocked by the user` | [bot.blocked_by_user](https://errorgram.rmbk.me/errors/bot.blocked_by_user/) |

[Try your response in the playground →](https://errorgram.rmbk.me/playground/) · [Browse every condition →](https://errorgram.rmbk.me/catalogue/)

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
| [Python & aiogram](https://errorgram.rmbk.me/python/) | Plain response classification and concrete exception types. |
| [JavaScript, TypeScript & grammY](https://errorgram.rmbk.me/javascript/) | ESM bindings, typed facts, and framework-compatible enrichment. |
| [JSON & AI agents](https://errorgram.rmbk.me/agents/) | The complete catalogue, schema, and plain Markdown reference. |

## Know what the evidence supports

The catalogue tracks Bot API **10.3**. Seven conditions also have recorded live observations. Examples use synthetic data; each record links to its evidence. Coverage is incomplete and grows through reviewed contributions.

A stable ID describes the observed condition. It cannot prove every underlying cause. Unknown responses stay unknown, and transport failures and framework validation errors remain outside the catalogue.

[Get started](https://errorgram.rmbk.me/getting-started/) · [How matching works](https://errorgram.rmbk.me/matching/) · [Read this page as Markdown](https://errorgram.rmbk.me/index.md)
