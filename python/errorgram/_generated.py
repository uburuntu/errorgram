"""Generated from catalogue/errors.json. Run make generate to update."""

from typing import Literal

CATALOGUE_VERSION = '0.1.0'
ConditionId = Literal[
    'auth.invalid_token_format',
    'bot.blocked_by_user',
    'chat.migrated',
    'chat.not_found',
    'file.download_too_large',
    'message.delete_forbidden',
    'message.not_modified',
    'query.invalid_or_expired',
    'request.retry_after',
    'routing.token_not_served',
    'server.restarting',
    'session.logged_out',
    'updates.concurrent_poll',
    'updates.webhook_active',
    'webhook.certificate_too_large',
]
CONDITION_IDS: tuple[ConditionId, ...] = (
    'auth.invalid_token_format',
    'bot.blocked_by_user',
    'chat.migrated',
    'chat.not_found',
    'file.download_too_large',
    'message.delete_forbidden',
    'message.not_modified',
    'query.invalid_or_expired',
    'request.retry_after',
    'routing.token_not_served',
    'server.restarting',
    'session.logged_out',
    'updates.concurrent_poll',
    'updates.webhook_active',
    'webhook.certificate_too_large',
)
