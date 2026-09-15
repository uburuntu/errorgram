---
title: "Python & aiogram"
description: "Classify Telegram Bot API responses in Python and enrich aiogram exceptions with precise types while preserving existing catches."
---

A `400` groups many failures together. Errorgram names the condition while keeping the response and your handling decisions intact.

From a [local checkout](/getting-started/), run `uv venv` and `uv pip install -e .`. Use `uv pip install -e '.[aiogram]'` to include aiogram. The core has no runtime dependencies.

## Read a response

```python
from errorgram import classify

response = {
    "ok": False,
    "error_code": 400,
    "description": "Bad Request: chat not found",
}
result = classify(response, method="sendMessage")

assert result.id == "chat.not_found"
assert result.response is response
print(result.entry["summary"])
```

Only `matched` results have an ID and entry. Other statuses are `unknown`, `ambiguous`, `insufficient_context`, and `not_api_error`. Candidate IDs explain ambiguous results or missing method context. `facts` contains extracted values such as `retry_after`.

`catalogue()` returns a fresh copy of the catalogue and its evidence sources. `CATALOGUE_VERSION` identifies the data version; `ConditionId` and `CONDITION_IDS` expose its stable IDs. Each classification includes the catalogue version and an independent snapshot of the matched entry.

## Use concrete exceptions

```python
from errorgram import ApiError, ChatNotFound, to_exception

error = to_exception(response, method="sendMessage")
assert isinstance(error, ChatNotFound)
assert isinstance(error, ApiError)
assert error.response is response
```

`to_exception()` creates an exception without raising it. Unclassified API failures use `ApiError`; inputs outside the Bot API error envelope return `None`. Every exception carries its `classification`, `id`, and `facts`.

Each [condition page](/catalogue/) lists its generated Python type.

## Add aiogram details

Enrichment is explicit. Keep your existing `TelegramBadRequest` catches, or catch a generated subtype such as `errorgram.aiogram.MessageNotModified`.

```python
from aiogram.exceptions import TelegramAPIError
from errorgram.aiogram import enrich

async def edit_message(bot, chat_id, message_id, text):
    try:
        return await bot.edit_message_text(
            text=text, chat_id=chat_id, message_id=message_id
        )
    except TelegramAPIError as original:
        error = enrich(original)
        if error is original:
            raise
        raise error from original
```

The enriched exception keeps the original message, method, recovery parameters, and catch compatibility. It adds `classification`, `id`, `facts`, `original`, and `fidelity`.

Unknown conditions and transport exceptions pass through unchanged. Repeated enrichment returns the same object. Enrichment never retries, suppresses exceptions, updates chat IDs, or registers handlers.

## Understand framework fidelity

aiogram discards the wire error code and some response fields. Errorgram labels the information it can reconstruct:

| Field | What to expect |
| --- | --- |
| `response` | Reconstructed from the exception. |
| `error_code` | Inferred from the framework exception type and supported rules. |
| `description` | Retry and migration descriptions are marked `framework_modified`. |
| `parameters` | Always marked `partial`. |

Use `classify()` on the raw response when exact wire evidence matters. The original aiogram exception remains available as `original`.

[How matching works](/matching/) · [Read this page as Markdown](/python.md)
