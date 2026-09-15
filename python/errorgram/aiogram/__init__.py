"""Generated from catalogue/errors.json. Run make generate to update."""

from ._adapter import EnrichedError, SourceFidelity, enrich
from ._errors import (
    AuthInvalidTokenFormat,
    BotBlockedByUser,
    ChatMigrated,
    ChatNotFound,
    FileDownloadTooLarge,
    MessageDeleteForbidden,
    MessageNotModified,
    QueryInvalidOrExpired,
    RequestRetryAfter,
    RoutingTokenNotServed,
    ServerRestarting,
    SessionLoggedOut,
    UpdatesConcurrentPoll,
    UpdatesWebhookActive,
    WebhookCertificateTooLarge,
)

__all__ = [
    'AuthInvalidTokenFormat',
    'BotBlockedByUser',
    'ChatMigrated',
    'ChatNotFound',
    'EnrichedError',
    'FileDownloadTooLarge',
    'MessageDeleteForbidden',
    'MessageNotModified',
    'QueryInvalidOrExpired',
    'RequestRetryAfter',
    'RoutingTokenNotServed',
    'ServerRestarting',
    'SessionLoggedOut',
    'SourceFidelity',
    'UpdatesConcurrentPoll',
    'UpdatesWebhookActive',
    'WebhookCertificateTooLarge',
    'enrich',
]
