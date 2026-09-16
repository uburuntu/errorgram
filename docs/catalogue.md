# Catalogue

Version **0.1.0** · **45 conditions**

Each ID describes an observable failure. Read its evidence before drawing conclusions
about the cause. Examples are source-derived and synthetic; coverage is incomplete.

| ID | Meaning | Evidence |
| --- | --- | --- |
| `auth.invalid_token_format` | The server rejected the token during local validation. | [source derived](https://github.com/tdlib/telegram-bot-api/blob/e3e9dd8e5b3d7ab8537cd5a10dc31d5ffa8f82d1/telegram-bot-api/ClientManager.cpp#L73) |
| `bot.blocked_by_user` | The user has blocked the bot. | [source derived](https://github.com/tdlib/telegram-bot-api/blob/e3e9dd8e5b3d7ab8537cd5a10dc31d5ffa8f82d1/telegram-bot-api/Client.cpp#L127) |
| `bot.kicked` | The bot was removed or banned from the chat. | [source derived](https://github.com/tdlib/telegram-bot-api/blob/e3e9dd8e5b3d7ab8537cd5a10dc31d5ffa8f82d1/telegram-bot-api/Client.cpp#L8832) |
| `bot.not_member` | The bot lacks the chat membership required for this operation. | [source derived](https://github.com/tdlib/telegram-bot-api/blob/e3e9dd8e5b3d7ab8537cd5a10dc31d5ffa8f82d1/telegram-bot-api/Client.cpp#L8835) |
| `chat.group_deleted` | Telegram reports that the group chat was deleted. | [source derived](https://github.com/tdlib/telegram-bot-api/blob/e3e9dd8e5b3d7ab8537cd5a10dc31d5ffa8f82d1/telegram-bot-api/Client.cpp#L8814) |
| `chat.migrated` | The group has moved to a supergroup with a new ID. | [observed](https://github.com/uburuntu/errorgram/blob/4314ac1f9d29d105b10e9b537a7643cc65d097aa/observations/2026-09-16.json) |
| `chat.not_found` | The bot could not resolve this chat. | [source derived](https://github.com/tdlib/telegram-bot-api/blob/e3e9dd8e5b3d7ab8537cd5a10dc31d5ffa8f82d1/telegram-bot-api/Client.cpp#L7239) |
| `file.download_too_large` | The file exceeds the server’s non-local download limit. | [source derived](https://github.com/tdlib/telegram-bot-api/blob/e3e9dd8e5b3d7ab8537cd5a10dc31d5ffa8f82d1/telegram-bot-api/Client.cpp#L17032) |
| `file.id_invalid` | The server could not resolve the supplied file_id. | [source derived](https://github.com/tdlib/telegram-bot-api/blob/e3e9dd8e5b3d7ab8537cd5a10dc31d5ffa8f82d1/telegram-bot-api/Client.cpp#L7525) |
| `file.id_missing` | The file_id argument is missing or empty. | [observed](https://github.com/uburuntu/errorgram/blob/4314ac1f9d29d105b10e9b537a7643cc65d097aa/observations/2026-09-16.json) |
| `file.unavailable` | The file could not be downloaded with the supplied identifier. | [source derived](https://github.com/tdlib/telegram-bot-api/blob/e3e9dd8e5b3d7ab8537cd5a10dc31d5ffa8f82d1/telegram-bot-api/Client.cpp#L9385) |
| `file.url_content_type_invalid` | The retrieved web content is unsuitable for the requested operation. | [source derived](https://github.com/tdlib/telegram-bot-api/blob/e3e9dd8e5b3d7ab8537cd5a10dc31d5ffa8f82d1/telegram-bot-api/Client.cpp#L118) |
| `file.url_fetch_failed` | Telegram could not retrieve content from the HTTP URL. | [source derived](https://github.com/tdlib/telegram-bot-api/blob/e3e9dd8e5b3d7ab8537cd5a10dc31d5ffa8f82d1/telegram-bot-api/Client.cpp#L116) |
| `file.url_invalid` | The HTTP URL was rejected. | [source derived](https://github.com/tdlib/telegram-bot-api/blob/e3e9dd8e5b3d7ab8537cd5a10dc31d5ffa8f82d1/telegram-bot-api/Client.cpp#L114) |
| `file.url_upload_failed` | Telegram could not upload the file from its URL. | [source derived](https://github.com/tdlib/telegram-bot-api/blob/e3e9dd8e5b3d7ab8537cd5a10dc31d5ffa8f82d1/telegram-bot-api/Client.cpp#L133) |
| `format.entity_not_object` | An item in the message entities array is not a JSON object. | [source derived](https://github.com/tdlib/telegram-bot-api/blob/e3e9dd8e5b3d7ab8537cd5a10dc31d5ffa8f82d1/telegram-bot-api/Client.cpp#L11938) |
| `format.entity_type_unsupported` | A message entity specifies an unsupported type. | [source derived](https://github.com/tdlib/telegram-bot-api/blob/e3e9dd8e5b3d7ab8537cd5a10dc31d5ffa8f82d1/telegram-bot-api/Client.cpp#L11929) |
| `format.parse_mode_unsupported` | The requested parse_mode is unsupported. | [observed](https://github.com/uburuntu/errorgram/blob/4314ac1f9d29d105b10e9b537a7643cc65d097aa/observations/2026-09-16.json) |
| `markup.invalid_json` | The reply_markup argument is not valid JSON. | [source derived](https://github.com/tdlib/telegram-bot-api/blob/e3e9dd8e5b3d7ab8537cd5a10dc31d5ffa8f82d1/telegram-bot-api/Client.cpp#L10504) |
| `markup.not_object` | The reply_markup value is not a JSON object. | [source derived](https://github.com/tdlib/telegram-bot-api/blob/e3e9dd8e5b3d7ab8537cd5a10dc31d5ffa8f82d1/telegram-bot-api/Client.cpp#L10521) |
| `markup.too_long` | Telegram rejected the size of the reply markup. | [source derived](https://github.com/tdlib/telegram-bot-api/blob/e3e9dd8e5b3d7ab8537cd5a10dc31d5ffa8f82d1/telegram-bot-api/Client.cpp#L121) |
| `member.is_administrator` | The operation was rejected because the target user is a chat administrator. | [source derived](https://github.com/tdlib/telegram-bot-api/blob/e3e9dd8e5b3d7ab8537cd5a10dc31d5ffa8f82d1/telegram-bot-api/Client.cpp#L130) |
| `message.copy_not_found` | The message to copy could not be resolved. | [source derived](https://github.com/tdlib/telegram-bot-api/blob/e3e9dd8e5b3d7ab8537cd5a10dc31d5ffa8f82d1/telegram-bot-api/Client.cpp#L14373) |
| `message.delete_forbidden` | Telegram rejected deletion of the message. | [source derived](https://github.com/tdlib/telegram-bot-api/blob/e3e9dd8e5b3d7ab8537cd5a10dc31d5ffa8f82d1/telegram-bot-api/Client.cpp#L151) |
| `message.delete_not_found` | The message to delete could not be resolved. | [observed](https://github.com/uburuntu/errorgram/blob/4314ac1f9d29d105b10e9b537a7643cc65d097aa/observations/2026-09-16.json) |
| `message.edit_not_found` | The message to edit could not be resolved. | [observed](https://github.com/uburuntu/errorgram/blob/4314ac1f9d29d105b10e9b537a7643cc65d097aa/observations/2026-09-16.json) |
| `message.forward_not_found` | The message to forward could not be resolved. | [source derived](https://github.com/tdlib/telegram-bot-api/blob/e3e9dd8e5b3d7ab8537cd5a10dc31d5ffa8f82d1/telegram-bot-api/Client.cpp#L14441) |
| `message.identifier_missing` | The request did not specify a message identifier for the selected operation. | [source derived](https://github.com/tdlib/telegram-bot-api/blob/e3e9dd8e5b3d7ab8537cd5a10dc31d5ffa8f82d1/telegram-bot-api/Client.cpp#L13540) |
| `message.identifiers_missing` | The request did not specify the list of message identifiers. | [source derived](https://github.com/tdlib/telegram-bot-api/blob/e3e9dd8e5b3d7ab8537cd5a10dc31d5ffa8f82d1/telegram-bot-api/Client.cpp#L13500) |
| `message.not_modified` | The requested message content and reply markup are unchanged. | [observed](https://github.com/uburuntu/errorgram/blob/4314ac1f9d29d105b10e9b537a7643cc65d097aa/observations/2026-09-16.json) |
| `message.pin_not_found` | The message to pin could not be resolved. | [source derived](https://github.com/tdlib/telegram-bot-api/blob/e3e9dd8e5b3d7ab8537cd5a10dc31d5ffa8f82d1/telegram-bot-api/Client.cpp#L16054) |
| `message.reply_not_found` | The message being replied to could not be resolved. | [source derived](https://github.com/tdlib/telegram-bot-api/blob/e3e9dd8e5b3d7ab8537cd5a10dc31d5ffa8f82d1/telegram-bot-api/Client.cpp#L9190) |
| `permissions.invalid_json` | The permissions argument is not valid JSON. | [source derived](https://github.com/tdlib/telegram-bot-api/blob/e3e9dd8e5b3d7ab8537cd5a10dc31d5ffa8f82d1/telegram-bot-api/Client.cpp#L12555) |
| `permissions.not_object` | The permissions value is not a JSON object. | [source derived](https://github.com/tdlib/telegram-bot-api/blob/e3e9dd8e5b3d7ab8537cd5a10dc31d5ffa8f82d1/telegram-bot-api/Client.cpp#L12564) |
| `query.invalid_or_expired` | The query ID is invalid or its response window has expired. | [source derived](https://github.com/tdlib/telegram-bot-api/blob/e3e9dd8e5b3d7ab8537cd5a10dc31d5ffa8f82d1/telegram-bot-api/Client.cpp#L148) |
| `request.retry_after` | The server asks the bot to wait before trying again. | [source derived](https://github.com/tdlib/telegram-bot-api/blob/e3e9dd8e5b3d7ab8537cd5a10dc31d5ffa8f82d1/telegram-bot-api/Query.cpp#L120) |
| `routing.token_not_served` | The token failed the server’s bot-ID or routing check. | [source derived](https://github.com/tdlib/telegram-bot-api/blob/e3e9dd8e5b3d7ab8537cd5a10dc31d5ffa8f82d1/telegram-bot-api/ClientManager.cpp#L78) |
| `server.restarting` | The bot client is closing for a server restart. | [source derived](https://github.com/tdlib/telegram-bot-api/blob/e3e9dd8e5b3d7ab8537cd5a10dc31d5ffa8f82d1/telegram-bot-api/Client.cpp#L17560) |
| `session.logged_out` | The bot session has logged out. | [source derived](https://github.com/tdlib/telegram-bot-api/blob/e3e9dd8e5b3d7ab8537cd5a10dc31d5ffa8f82d1/telegram-bot-api/Client.cpp#L17553) |
| `text.empty` | The message text is empty. | [observed](https://github.com/uburuntu/errorgram/blob/4314ac1f9d29d105b10e9b537a7643cc65d097aa/observations/2026-09-16.json) |
| `text.too_long` | The text exceeds the limit checked by this response path. | [source derived](https://github.com/tdlib/telegram-bot-api/blob/e3e9dd8e5b3d7ab8537cd5a10dc31d5ffa8f82d1/telegram-bot-api/Client.cpp#L11955) |
| `updates.concurrent_poll` | Another getUpdates request interrupted the pending long poll. | [source derived](https://github.com/tdlib/telegram-bot-api/blob/e3e9dd8e5b3d7ab8537cd5a10dc31d5ffa8f82d1/telegram-bot-api/Client.cpp#L17493) |
| `updates.webhook_active` | Polling was requested while a webhook is active or being configured. | [source derived](https://github.com/tdlib/telegram-bot-api/blob/e3e9dd8e5b3d7ab8537cd5a10dc31d5ffa8f82d1/telegram-bot-api/Client.cpp#L16926) |
| `user.deactivated` | Telegram rejected the operation because the user is deactivated. | [source derived](https://github.com/tdlib/telegram-bot-api/blob/e3e9dd8e5b3d7ab8537cd5a10dc31d5ffa8f82d1/telegram-bot-api/Client.cpp#L8803) |
| `webhook.certificate_too_large` | The uploaded webhook certificate exceeds the server’s size limit. | [source derived](https://github.com/tdlib/telegram-bot-api/blob/e3e9dd8e5b3d7ab8537cd5a10dc31d5ffa8f82d1/telegram-bot-api/Client.cpp#L17261) |

[Full records](../catalogue/errors.json) include matching rules, context, possible causes,
guidance, and source references. [Matching rules](design.md) explain how classification works.

Generated from `catalogue/errors.json`. Run `make generate` after editing the catalogue.
