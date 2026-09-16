"""Generated from catalogue/errors.json. Run make generate to update."""

from ._exceptions import ApiError


class AuthInvalidTokenFormat(ApiError):
    'The server rejected the token during local validation.'


class BotBlockedByUser(ApiError):
    'The user has blocked the bot.'


class BotKicked(ApiError):
    'The bot was removed or banned from the chat.'


class BotNotMember(ApiError):
    'The bot lacks the chat membership required for this operation.'


class ChatGroupDeleted(ApiError):
    'Telegram reports that the group chat was deleted.'


class ChatMigrated(ApiError):
    'The group has moved to a supergroup with a new ID.'


class ChatNotFound(ApiError):
    'The bot could not resolve this chat.'


class FileDownloadTooLarge(ApiError):
    'The file exceeds the server’s non-local download limit.'


class FileIdInvalid(ApiError):
    'The server could not resolve the supplied file_id.'


class FileIdMissing(ApiError):
    'The file_id argument is missing or empty.'


class FileUnavailable(ApiError):
    'The file could not be downloaded with the supplied identifier.'


class FileUrlContentTypeInvalid(ApiError):
    'The retrieved web content is unsuitable for the requested operation.'


class FileUrlFetchFailed(ApiError):
    'Telegram could not retrieve content from the HTTP URL.'


class FileUrlInvalid(ApiError):
    'The HTTP URL was rejected.'


class FileUrlUploadFailed(ApiError):
    'Telegram could not upload the file from its URL.'


class FormatEntityNotObject(ApiError):
    'An item in the message entities array is not a JSON object.'


class FormatEntityTypeUnsupported(ApiError):
    'A message entity specifies an unsupported type.'


class FormatParseModeUnsupported(ApiError):
    'The requested parse_mode is unsupported.'


class MarkupInvalidJson(ApiError):
    'The reply_markup argument is not valid JSON.'


class MarkupNotObject(ApiError):
    'The reply_markup value is not a JSON object.'


class MarkupTooLong(ApiError):
    'Telegram rejected the size of the reply markup.'


class MemberIsAdministrator(ApiError):
    'The operation was rejected because the target user is a chat administrator.'


class MessageCopyNotFound(ApiError):
    'The message to copy could not be resolved.'


class MessageDeleteForbidden(ApiError):
    'Telegram rejected deletion of the message.'


class MessageDeleteNotFound(ApiError):
    'The message to delete could not be resolved.'


class MessageEditNotFound(ApiError):
    'The message to edit could not be resolved.'


class MessageForwardNotFound(ApiError):
    'The message to forward could not be resolved.'


class MessageIdentifierMissing(ApiError):
    'The request did not specify a message identifier for the selected operation.'


class MessageIdentifiersMissing(ApiError):
    'The request did not specify the list of message identifiers.'


class MessageNotModified(ApiError):
    'The requested message content and reply markup are unchanged.'


class MessagePinNotFound(ApiError):
    'The message to pin could not be resolved.'


class MessageReplyNotFound(ApiError):
    'The message being replied to could not be resolved.'


class PermissionsInvalidJson(ApiError):
    'The permissions argument is not valid JSON.'


class PermissionsNotObject(ApiError):
    'The permissions value is not a JSON object.'


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


class TextEmpty(ApiError):
    'The message text is empty.'


class TextTooLong(ApiError):
    'The text exceeds the limit checked by this response path.'


class UpdatesConcurrentPoll(ApiError):
    'Another getUpdates request interrupted the pending long poll.'


class UpdatesWebhookActive(ApiError):
    'Polling was requested while a webhook is active or being configured.'


class UserDeactivated(ApiError):
    'Telegram rejected the operation because the user is deactivated.'


class WebhookCertificateTooLarge(ApiError):
    'The uploaded webhook certificate exceeds the server’s size limit.'


EXCEPTION_TYPES: dict[str | None, type[ApiError]] = {
    'auth.invalid_token_format': AuthInvalidTokenFormat,
    'bot.blocked_by_user': BotBlockedByUser,
    'bot.kicked': BotKicked,
    'bot.not_member': BotNotMember,
    'chat.group_deleted': ChatGroupDeleted,
    'chat.migrated': ChatMigrated,
    'chat.not_found': ChatNotFound,
    'file.download_too_large': FileDownloadTooLarge,
    'file.id_invalid': FileIdInvalid,
    'file.id_missing': FileIdMissing,
    'file.unavailable': FileUnavailable,
    'file.url_content_type_invalid': FileUrlContentTypeInvalid,
    'file.url_fetch_failed': FileUrlFetchFailed,
    'file.url_invalid': FileUrlInvalid,
    'file.url_upload_failed': FileUrlUploadFailed,
    'format.entity_not_object': FormatEntityNotObject,
    'format.entity_type_unsupported': FormatEntityTypeUnsupported,
    'format.parse_mode_unsupported': FormatParseModeUnsupported,
    'markup.invalid_json': MarkupInvalidJson,
    'markup.not_object': MarkupNotObject,
    'markup.too_long': MarkupTooLong,
    'member.is_administrator': MemberIsAdministrator,
    'message.copy_not_found': MessageCopyNotFound,
    'message.delete_forbidden': MessageDeleteForbidden,
    'message.delete_not_found': MessageDeleteNotFound,
    'message.edit_not_found': MessageEditNotFound,
    'message.forward_not_found': MessageForwardNotFound,
    'message.identifier_missing': MessageIdentifierMissing,
    'message.identifiers_missing': MessageIdentifiersMissing,
    'message.not_modified': MessageNotModified,
    'message.pin_not_found': MessagePinNotFound,
    'message.reply_not_found': MessageReplyNotFound,
    'permissions.invalid_json': PermissionsInvalidJson,
    'permissions.not_object': PermissionsNotObject,
    'query.invalid_or_expired': QueryInvalidOrExpired,
    'request.retry_after': RequestRetryAfter,
    'routing.token_not_served': RoutingTokenNotServed,
    'server.restarting': ServerRestarting,
    'session.logged_out': SessionLoggedOut,
    'text.empty': TextEmpty,
    'text.too_long': TextTooLong,
    'updates.concurrent_poll': UpdatesConcurrentPoll,
    'updates.webhook_active': UpdatesWebhookActive,
    'user.deactivated': UserDeactivated,
    'webhook.certificate_too_large': WebhookCertificateTooLarge,
}
