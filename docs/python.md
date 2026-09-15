# Python

A `400` groups many failures together. Errorgram names the condition while keeping the response and your handling decisions intact.

For a fresh checkout, create an environment and install the core package:

```sh
uv venv
uv pip install -e .
```

To include aiogram, use `uv pip install -e '.[aiogram]'` for the install command. Registry packages are not published yet. The core has no runtime dependencies.

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

Only `matched` results have an ID and entry. Other statuses are `unknown`, `ambiguous`, `insufficient_context`, and `not_api_error`. Ambiguous results list candidate IDs; missing method context can prevent a match. `facts` contains extracted values such as `retry_after`.

`catalogue()` returns a fresh copy of all entries and their evidence sources. `CATALOGUE_VERSION` identifies the data version; `ConditionId` and `CONDITION_IDS` expose its stable IDs. Classifications include the catalogue version, and their entry metadata is an independent snapshot.

## Use concrete exceptions

```python
from errorgram import ApiError, ChatNotFound, to_exception

error = to_exception(response, method="sendMessage")
assert isinstance(error, ChatNotFound)
assert isinstance(error, ApiError)
assert error.response is response
```

`to_exception()` builds an exception without raising it. Unclassified API failures use `ApiError`; inputs outside the Bot API error envelope return `None`. Every exception carries its `classification`, `id`, and `facts`.

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

The new exception keeps the original message, method, recovery parameters, and catch compatibility. It adds `classification`, `id`, `facts`, `original`, and `fidelity`. Unknown conditions and transport exceptions pass through unchanged. Repeated enrichment returns the same object.

aiogram discards the wire error code and some response fields. Errorgram therefore marks its reconstructed response and inferred code in `fidelity`; retry and migration descriptions are marked `framework_modified`. Parameter fidelity is always `partial`. Use `classify()` on the raw response when exact wire evidence matters.

Enrichment does not retry, suppress exceptions, update chat IDs, or register handlers.
