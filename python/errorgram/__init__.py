"""Generated from catalogue/errors.json. Run make generate to update."""

from ._classifier import Classification, Status, catalogue, classify
from ._exceptions import ApiError, to_exception
from ._generated import CATALOGUE_VERSION, CONDITION_IDS, ConditionId
from .errors import (
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
    'ApiError',
    'AuthInvalidTokenFormat',
    'BotBlockedByUser',
    'CATALOGUE_VERSION',
    'CONDITION_IDS',
    'ChatMigrated',
    'ChatNotFound',
    'Classification',
    'ConditionId',
    'FileDownloadTooLarge',
    'MessageDeleteForbidden',
    'MessageNotModified',
    'QueryInvalidOrExpired',
    'RequestRetryAfter',
    'RoutingTokenNotServed',
    'ServerRestarting',
    'SessionLoggedOut',
    'Status',
    'UpdatesConcurrentPoll',
    'UpdatesWebhookActive',
    'WebhookCertificateTooLarge',
    'catalogue',
    'classify',
    'to_exception',
]
