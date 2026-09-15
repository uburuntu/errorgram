"""Run the Python guide's examples through their public APIs."""

from __future__ import annotations

import asyncio
import re
from pathlib import Path

import pytest
from aiogram.exceptions import TelegramBadRequest
from aiogram.methods import EditMessageText
from errorgram.aiogram import ChatNotFound


def test_python_guide_examples() -> None:
    guide = Path(__file__).resolve().parents[2] / "docs/python.md"
    namespace: dict = {}
    for snippet in re.findall(r"```python\n(.*?)```", guide.read_text(), re.DOTALL):
        exec(compile(snippet, str(guide), "exec"), namespace)

    original = TelegramBadRequest(
        EditMessageText(text="Hello", chat_id=42, message_id=7),
        "Bad Request: chat not found",
    )

    class BotStub:
        async def edit_message_text(self, **kwargs):
            raise original

    with pytest.raises(ChatNotFound) as caught:
        asyncio.run(namespace["edit_message"](BotStub(), 42, 7, "Hello"))
    assert caught.value.original is original
    assert caught.value.__cause__ is original
