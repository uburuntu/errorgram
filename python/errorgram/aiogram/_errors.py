"""Generated from catalogue/errors.json. Run make generate to update."""

from aiogram.exceptions import (
    RestartingTelegram,
    TelegramAPIError,
    TelegramBadRequest,
    TelegramConflictError,
    TelegramForbiddenError,
    TelegramMigrateToChat,
    TelegramRetryAfter,
    TelegramUnauthorizedError,
)

from ._adapter import EnrichedError


class AuthInvalidTokenFormat(EnrichedError, TelegramUnauthorizedError):
    'The server rejected the token during local validation.'


class BotBlockedByUser(EnrichedError, TelegramForbiddenError):
    'The user has blocked the bot.'


class ChatMigrated(EnrichedError, TelegramMigrateToChat):
    'The group has moved to a supergroup with a new ID.'


class ChatNotFound(EnrichedError, TelegramBadRequest):
    'The bot could not resolve this chat.'


class FileDownloadTooLarge(EnrichedError, TelegramBadRequest):
    'The file exceeds the server’s non-local download limit.'


class MessageDeleteForbidden(EnrichedError, TelegramBadRequest):
    'Telegram rejected deletion of the message.'


class MessageNotModified(EnrichedError, TelegramBadRequest):
    'The requested message content and reply markup are unchanged.'


class QueryInvalidOrExpired(EnrichedError, TelegramBadRequest):
    'The query ID is invalid or its response window has expired.'


class RequestRetryAfter(EnrichedError, TelegramRetryAfter):
    'The server asks the bot to wait before trying again.'


class RoutingTokenNotServed(EnrichedError, TelegramAPIError):
    'The token failed the server’s bot-ID or routing check.'


class ServerRestarting(EnrichedError, RestartingTelegram):
    'The bot client is closing for a server restart.'


class SessionLoggedOut(EnrichedError, TelegramBadRequest):
    'The bot session has logged out.'


class UpdatesConcurrentPoll(EnrichedError, TelegramConflictError):
    'Another getUpdates request interrupted the pending long poll.'


class UpdatesWebhookActive(EnrichedError, TelegramConflictError):
    'Polling was requested while a webhook is active or being configured.'


class WebhookCertificateTooLarge(EnrichedError, TelegramBadRequest):
    'The uploaded webhook certificate exceeds the server’s size limit.'


EXCEPTION_TYPES: dict[str | None, type[EnrichedError]] = {
    'auth.invalid_token_format': AuthInvalidTokenFormat,
    'bot.blocked_by_user': BotBlockedByUser,
    'chat.migrated': ChatMigrated,
    'chat.not_found': ChatNotFound,
    'file.download_too_large': FileDownloadTooLarge,
    'message.delete_forbidden': MessageDeleteForbidden,
    'message.not_modified': MessageNotModified,
    'query.invalid_or_expired': QueryInvalidOrExpired,
    'request.retry_after': RequestRetryAfter,
    'routing.token_not_served': RoutingTokenNotServed,
    'server.restarting': ServerRestarting,
    'session.logged_out': SessionLoggedOut,
    'updates.concurrent_poll': UpdatesConcurrentPoll,
    'updates.webhook_active': UpdatesWebhookActive,
    'webhook.certificate_too_large': WebhookCertificateTooLarge,
}
