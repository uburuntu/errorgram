# Catalogue

Version **0.1.0** · **15 conditions**

Each ID describes an observable failure. Read its evidence before drawing conclusions
about the cause. Examples are source-derived and synthetic; coverage is incomplete.

| ID | Meaning | Evidence |
| --- | --- | --- |
| `auth.invalid_token_format` | The server rejected the token during local validation. | [source derived](https://github.com/tdlib/telegram-bot-api/blob/e3e9dd8e5b3d7ab8537cd5a10dc31d5ffa8f82d1/telegram-bot-api/ClientManager.cpp#L73) |
| `bot.blocked_by_user` | The user has blocked the bot. | [source derived](https://github.com/tdlib/telegram-bot-api/blob/e3e9dd8e5b3d7ab8537cd5a10dc31d5ffa8f82d1/telegram-bot-api/Client.cpp#L127) |
| `chat.migrated` | The group has moved to a supergroup with a new ID. | [source derived](https://github.com/tdlib/telegram-bot-api/blob/e3e9dd8e5b3d7ab8537cd5a10dc31d5ffa8f82d1/telegram-bot-api/Client.cpp#L8821) |
| `chat.not_found` | The bot could not resolve this chat. | [source derived](https://github.com/tdlib/telegram-bot-api/blob/e3e9dd8e5b3d7ab8537cd5a10dc31d5ffa8f82d1/telegram-bot-api/Client.cpp#L7239) |
| `file.download_too_large` | The file exceeds the server’s non-local download limit. | [source derived](https://github.com/tdlib/telegram-bot-api/blob/e3e9dd8e5b3d7ab8537cd5a10dc31d5ffa8f82d1/telegram-bot-api/Client.cpp#L17032) |
| `message.delete_forbidden` | Telegram rejected deletion of the message. | [source derived](https://github.com/tdlib/telegram-bot-api/blob/e3e9dd8e5b3d7ab8537cd5a10dc31d5ffa8f82d1/telegram-bot-api/Client.cpp#L151) |
| `message.not_modified` | The requested message content and reply markup are unchanged. | [source derived](https://github.com/tdlib/telegram-bot-api/blob/e3e9dd8e5b3d7ab8537cd5a10dc31d5ffa8f82d1/telegram-bot-api/Client.cpp#L106) |
| `query.invalid_or_expired` | The query ID is invalid or its response window has expired. | [source derived](https://github.com/tdlib/telegram-bot-api/blob/e3e9dd8e5b3d7ab8537cd5a10dc31d5ffa8f82d1/telegram-bot-api/Client.cpp#L148) |
| `request.retry_after` | The server asks the bot to wait before trying again. | [source derived](https://github.com/tdlib/telegram-bot-api/blob/e3e9dd8e5b3d7ab8537cd5a10dc31d5ffa8f82d1/telegram-bot-api/Query.cpp#L120) |
| `routing.token_not_served` | The token failed the server’s bot-ID or routing check. | [source derived](https://github.com/tdlib/telegram-bot-api/blob/e3e9dd8e5b3d7ab8537cd5a10dc31d5ffa8f82d1/telegram-bot-api/ClientManager.cpp#L78) |
| `server.restarting` | The bot client is closing for a server restart. | [source derived](https://github.com/tdlib/telegram-bot-api/blob/e3e9dd8e5b3d7ab8537cd5a10dc31d5ffa8f82d1/telegram-bot-api/Client.cpp#L17560) |
| `session.logged_out` | The bot session has logged out. | [source derived](https://github.com/tdlib/telegram-bot-api/blob/e3e9dd8e5b3d7ab8537cd5a10dc31d5ffa8f82d1/telegram-bot-api/Client.cpp#L17553) |
| `updates.concurrent_poll` | Another getUpdates request interrupted the pending long poll. | [source derived](https://github.com/tdlib/telegram-bot-api/blob/e3e9dd8e5b3d7ab8537cd5a10dc31d5ffa8f82d1/telegram-bot-api/Client.cpp#L17493) |
| `updates.webhook_active` | Polling was requested while a webhook is active or being configured. | [source derived](https://github.com/tdlib/telegram-bot-api/blob/e3e9dd8e5b3d7ab8537cd5a10dc31d5ffa8f82d1/telegram-bot-api/Client.cpp#L16926) |
| `webhook.certificate_too_large` | The uploaded webhook certificate exceeds the server’s size limit. | [source derived](https://github.com/tdlib/telegram-bot-api/blob/e3e9dd8e5b3d7ab8537cd5a10dc31d5ffa8f82d1/telegram-bot-api/Client.cpp#L17261) |

[Full records](../catalogue/errors.json) include matching rules, context, possible causes,
guidance, and source references. [Matching rules](design.md) explain how classification works.

Generated from `catalogue/errors.json`. Run `make generate` after editing the catalogue.
