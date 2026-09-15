---
title: "Error catalogue"
description: "Telegram Bot API error conditions, stable IDs, matching rules, and source evidence."
slug: "catalogue"
editUrl: "https://github.com/uburuntu/errorgram/edit/main/catalogue/errors.json"
sidebar:
  label: "Error catalogue"
---

**15 conditions** · catalogue `0.1.0` · reviewed 2026-09-15

Start with the response text, a stable ID, or a framework exception name.
Each page explains the match, its limits, and the evidence behind it.

Telegram Bot API error responses. Source-derived; hosted deployment behavior is unverified.
Synthetic examples derived from the cited source.

Coverage is incomplete. Unrecognized responses remain unknown.

| Condition | Meaning |
| --- | --- |
| [auth.invalid\_token\_format](/errors/auth.invalid_token_format/) | The server rejected the token during local validation. |
| [bot.blocked\_by\_user](/errors/bot.blocked_by_user/) | The user has blocked the bot. |
| [chat.migrated](/errors/chat.migrated/) | The group has moved to a supergroup with a new ID. |
| [chat.not\_found](/errors/chat.not_found/) | The bot could not resolve this chat. |
| [file.download\_too\_large](/errors/file.download_too_large/) | The file exceeds the server’s non-local download limit. |
| [message.delete\_forbidden](/errors/message.delete_forbidden/) | Telegram rejected deletion of the message. |
| [message.not\_modified](/errors/message.not_modified/) | The requested message content and reply markup are unchanged. |
| [query.invalid\_or\_expired](/errors/query.invalid_or_expired/) | The query ID is invalid or its response window has expired. |
| [request.retry\_after](/errors/request.retry_after/) | The server asks the bot to wait before trying again. |
| [routing.token\_not\_served](/errors/routing.token_not_served/) | The token failed the server’s bot-ID or routing check. |
| [server.restarting](/errors/server.restarting/) | The bot client is closing for a server restart. |
| [session.logged\_out](/errors/session.logged_out/) | The bot session has logged out. |
| [updates.concurrent\_poll](/errors/updates.concurrent_poll/) | Another getUpdates request interrupted the pending long poll. |
| [updates.webhook\_active](/errors/updates.webhook_active/) | Polling was requested while a webhook is active or being configured. |
| [webhook.certificate\_too\_large](/errors/webhook.certificate_too_large/) | The uploaded webhook certificate exceeds the server’s size limit. |

Download the [catalogue JSON](/catalogue.json) or
[JSON Schema](/schema.json). For programmatic retrieval,
see [AI agents](/agents/).
