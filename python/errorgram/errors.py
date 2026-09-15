"""Generated from catalogue/errors.json. Run make generate to update."""

from ._exceptions import ApiError


class AuthInvalidTokenFormat(ApiError):
    'The server rejected the token during local validation.'


class BotBlockedByUser(ApiError):
    'The user has blocked the bot.'


class ChatMigrated(ApiError):
    'The group has moved to a supergroup with a new ID.'


class ChatNotFound(ApiError):
    'The bot could not resolve this chat.'


class FileDownloadTooLarge(ApiError):
    'The file exceeds the server’s non-local download limit.'


class MessageDeleteForbidden(ApiError):
    'Telegram rejected deletion of the message.'


class MessageNotModified(ApiError):
    'The requested message content and reply markup are unchanged.'


class QueryInvalidOrExpired(ApiError):
    'The query ID is invalid or its response window has expired.'


class RequestRetryAfter(ApiError):
    'The server asks the bot to wait before trying again.'


class RoutingTokenNotServed(ApiError):
    'The token failed the server’s bot-ID or routing check.'


class ServerRestarting(ApiError):
    'The bot client is closing for a server restart.'


class SessionLoggedOut(ApiError):
    'The bot session has logged out.'


class UpdatesConcurrentPoll(ApiError):
    'Another getUpdates request interrupted the pending long poll.'


class UpdatesWebhookActive(ApiError):
    'Polling was requested while a webhook is active or being configured.'


class WebhookCertificateTooLarge(ApiError):
    'The uploaded webhook certificate exceeds the server’s size limit.'


EXCEPTION_TYPES: dict[str | None, type[ApiError]] = {
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
