# Error catalogue

**15 conditions** · catalogue `0.1.0` · reviewed 2026-09-15

Start with the response text, a stable ID, or a framework exception name.
Each page explains the match, its limits, and the evidence behind it.

Telegram Bot API error responses. Source-derived; hosted deployment behavior is unverified.
Synthetic examples derived from the cited source.

Coverage is incomplete. Unrecognized responses remain unknown.

| Condition | Meaning |
| --- | --- |
| [auth.invalid\_token\_format](https://errorgram.rmbk.me/errors/auth.invalid_token_format/) | The server rejected the token during local validation. |
| [bot.blocked\_by\_user](https://errorgram.rmbk.me/errors/bot.blocked_by_user/) | The user has blocked the bot. |
| [chat.migrated](https://errorgram.rmbk.me/errors/chat.migrated/) | The group has moved to a supergroup with a new ID. |
| [chat.not\_found](https://errorgram.rmbk.me/errors/chat.not_found/) | The bot could not resolve this chat. |
| [file.download\_too\_large](https://errorgram.rmbk.me/errors/file.download_too_large/) | The file exceeds the server’s non-local download limit. |
| [message.delete\_forbidden](https://errorgram.rmbk.me/errors/message.delete_forbidden/) | Telegram rejected deletion of the message. |
| [message.not\_modified](https://errorgram.rmbk.me/errors/message.not_modified/) | The requested message content and reply markup are unchanged. |
| [query.invalid\_or\_expired](https://errorgram.rmbk.me/errors/query.invalid_or_expired/) | The query ID is invalid or its response window has expired. |
| [request.retry\_after](https://errorgram.rmbk.me/errors/request.retry_after/) | The server asks the bot to wait before trying again. |
| [routing.token\_not\_served](https://errorgram.rmbk.me/errors/routing.token_not_served/) | The token failed the server’s bot-ID or routing check. |
| [server.restarting](https://errorgram.rmbk.me/errors/server.restarting/) | The bot client is closing for a server restart. |
| [session.logged\_out](https://errorgram.rmbk.me/errors/session.logged_out/) | The bot session has logged out. |
| [updates.concurrent\_poll](https://errorgram.rmbk.me/errors/updates.concurrent_poll/) | Another getUpdates request interrupted the pending long poll. |
| [updates.webhook\_active](https://errorgram.rmbk.me/errors/updates.webhook_active/) | Polling was requested while a webhook is active or being configured. |
| [webhook.certificate\_too\_large](https://errorgram.rmbk.me/errors/webhook.certificate_too_large/) | The uploaded webhook certificate exceeds the server’s size limit. |

Download the [catalogue JSON](https://errorgram.rmbk.me/catalogue.json) or
[JSON Schema](https://errorgram.rmbk.me/schema.json). For programmatic retrieval,
see [AI agents](https://errorgram.rmbk.me/agents/).
