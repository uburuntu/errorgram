# Error catalogue

**45 conditions** · catalogue `0.1.0` · reviewed 2026-09-16

Start with the response text, a stable ID, or a framework exception name.
Each page explains the match, its limits, and the evidence behind it.

Telegram Bot API error responses, reviewed against source with selected hosted observations. Live verification is incomplete; see each record’s evidence.
Synthetic examples derived from the cited source.

Coverage is incomplete. Unrecognized responses remain unknown.

| Condition | Meaning |
| --- | --- |
| [auth.invalid\_token\_format](https://errorgram.rmbk.me/errors/auth.invalid_token_format/) | The server rejected the token during local validation. |
| [bot.blocked\_by\_user](https://errorgram.rmbk.me/errors/bot.blocked_by_user/) | The user has blocked the bot. |
| [bot.kicked](https://errorgram.rmbk.me/errors/bot.kicked/) | The bot was removed or banned from the chat. |
| [bot.not\_member](https://errorgram.rmbk.me/errors/bot.not_member/) | The bot lacks the chat membership required for this operation. |
| [chat.group\_deleted](https://errorgram.rmbk.me/errors/chat.group_deleted/) | Telegram reports that the group chat was deleted. |
| [chat.migrated](https://errorgram.rmbk.me/errors/chat.migrated/) | The group has moved to a supergroup with a new ID. |
| [chat.not\_found](https://errorgram.rmbk.me/errors/chat.not_found/) | The bot could not resolve this chat. |
| [file.download\_too\_large](https://errorgram.rmbk.me/errors/file.download_too_large/) | The file exceeds the server’s non-local download limit. |
| [file.id\_invalid](https://errorgram.rmbk.me/errors/file.id_invalid/) | The server could not resolve the supplied file\_id. |
| [file.id\_missing](https://errorgram.rmbk.me/errors/file.id_missing/) | The file\_id argument is missing or empty. |
| [file.unavailable](https://errorgram.rmbk.me/errors/file.unavailable/) | The file could not be downloaded with the supplied identifier. |
| [file.url\_content\_type\_invalid](https://errorgram.rmbk.me/errors/file.url_content_type_invalid/) | The retrieved web content is unsuitable for the requested operation. |
| [file.url\_fetch\_failed](https://errorgram.rmbk.me/errors/file.url_fetch_failed/) | Telegram could not retrieve content from the HTTP URL. |
| [file.url\_invalid](https://errorgram.rmbk.me/errors/file.url_invalid/) | The HTTP URL was rejected. |
| [file.url\_upload\_failed](https://errorgram.rmbk.me/errors/file.url_upload_failed/) | Telegram could not upload the file from its URL. |
| [format.entity\_not\_object](https://errorgram.rmbk.me/errors/format.entity_not_object/) | An item in the message entities array is not a JSON object. |
| [format.entity\_type\_unsupported](https://errorgram.rmbk.me/errors/format.entity_type_unsupported/) | A message entity specifies an unsupported type. |
| [format.parse\_mode\_unsupported](https://errorgram.rmbk.me/errors/format.parse_mode_unsupported/) | The requested parse\_mode is unsupported. |
| [markup.invalid\_json](https://errorgram.rmbk.me/errors/markup.invalid_json/) | The reply\_markup argument is not valid JSON. |
| [markup.not\_object](https://errorgram.rmbk.me/errors/markup.not_object/) | The reply\_markup value is not a JSON object. |
| [markup.too\_long](https://errorgram.rmbk.me/errors/markup.too_long/) | Telegram rejected the size of the reply markup. |
| [member.is\_administrator](https://errorgram.rmbk.me/errors/member.is_administrator/) | The operation was rejected because the target user is a chat administrator. |
| [message.copy\_not\_found](https://errorgram.rmbk.me/errors/message.copy_not_found/) | The message to copy could not be resolved. |
| [message.delete\_forbidden](https://errorgram.rmbk.me/errors/message.delete_forbidden/) | Telegram rejected deletion of the message. |
| [message.delete\_not\_found](https://errorgram.rmbk.me/errors/message.delete_not_found/) | The message to delete could not be resolved. |
| [message.edit\_not\_found](https://errorgram.rmbk.me/errors/message.edit_not_found/) | The message to edit could not be resolved. |
| [message.forward\_not\_found](https://errorgram.rmbk.me/errors/message.forward_not_found/) | The message to forward could not be resolved. |
| [message.identifier\_missing](https://errorgram.rmbk.me/errors/message.identifier_missing/) | The request did not specify a message identifier for the selected operation. |
| [message.identifiers\_missing](https://errorgram.rmbk.me/errors/message.identifiers_missing/) | The request did not specify the list of message identifiers. |
| [message.not\_modified](https://errorgram.rmbk.me/errors/message.not_modified/) | The requested message content and reply markup are unchanged. |
| [message.pin\_not\_found](https://errorgram.rmbk.me/errors/message.pin_not_found/) | The message to pin could not be resolved. |
| [message.reply\_not\_found](https://errorgram.rmbk.me/errors/message.reply_not_found/) | The message being replied to could not be resolved. |
| [permissions.invalid\_json](https://errorgram.rmbk.me/errors/permissions.invalid_json/) | The permissions argument is not valid JSON. |
| [permissions.not\_object](https://errorgram.rmbk.me/errors/permissions.not_object/) | The permissions value is not a JSON object. |
| [query.invalid\_or\_expired](https://errorgram.rmbk.me/errors/query.invalid_or_expired/) | The query ID is invalid or its response window has expired. |
| [request.retry\_after](https://errorgram.rmbk.me/errors/request.retry_after/) | The server asks the bot to wait before trying again. |
| [routing.token\_not\_served](https://errorgram.rmbk.me/errors/routing.token_not_served/) | The token failed the server’s bot-ID or routing check. |
| [server.restarting](https://errorgram.rmbk.me/errors/server.restarting/) | The bot client is closing for a server restart. |
| [session.logged\_out](https://errorgram.rmbk.me/errors/session.logged_out/) | The bot session has logged out. |
| [text.empty](https://errorgram.rmbk.me/errors/text.empty/) | The message text is empty. |
| [text.too\_long](https://errorgram.rmbk.me/errors/text.too_long/) | The text exceeds the limit checked by this response path. |
| [updates.concurrent\_poll](https://errorgram.rmbk.me/errors/updates.concurrent_poll/) | Another getUpdates request interrupted the pending long poll. |
| [updates.webhook\_active](https://errorgram.rmbk.me/errors/updates.webhook_active/) | Polling was requested while a webhook is active or being configured. |
| [user.deactivated](https://errorgram.rmbk.me/errors/user.deactivated/) | Telegram rejected the operation because the user is deactivated. |
| [webhook.certificate\_too\_large](https://errorgram.rmbk.me/errors/webhook.certificate_too_large/) | The uploaded webhook certificate exceeds the server’s size limit. |

Download the [catalogue JSON](https://errorgram.rmbk.me/catalogue.json) or
[JSON Schema](https://errorgram.rmbk.me/schema.json). For programmatic retrieval,
see [AI agents](https://errorgram.rmbk.me/agents/).
