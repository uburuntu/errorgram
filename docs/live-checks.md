# Live checks

Live checks compare a small set of controlled requests with the hosted Telegram
Bot API. They are opt-in and do not run during normal tests, pushes, pull requests
or scheduled maintenance.

## Run locally

Use a dedicated test bot and a group you control. Supply credentials through these
environment variables, keeping their values outside the repository:

| Variable | Purpose |
| --- | --- |
| `TELEGRAM_TEST_BOT_TOKEN` | Test bot credential. |
| `TELEGRAM_TEST_CHAT_ID` | Chat available to the bot for chat checks and optional message tests. |
| `TELEGRAM_MIGRATED_CHAT_ID` | Old group ID for a group already migrated to a supergroup. |

```sh
uv sync --locked
uv run python -m tools.live_checks --output .cache/live/observations.json
```

You can supply `--token-file /path/outside/the/repository/token`, `--chat-id` and
`--migrated-chat-id` instead of the corresponding environment variables. Keep
private values out of shell transcripts and committed files. `--direct` bypasses
environment proxy settings when your network requires a direct connection.

By default, the harness sends known-invalid requests and read-only checks; it
creates no messages. Add `--allow-message-tests` only when you want it to create
one silent message in the test chat, check an unchanged edit, delete its own
message ID in cleanup, and then check responses for the deleted message. Cleanup
is attempted in `finally`; an interrupted process or failed deletion can leave
that message behind. The harness does not retry requests or call update or
webhook methods.

## Run in GitHub Actions

Configure repository secrets named `TELEGRAM_TEST_BOT_TOKEN`,
`TELEGRAM_TEST_CHAT_ID` and `TELEGRAM_MIGRATED_CHAT_ID`. Open
[Live checks](https://github.com/uburuntu/errorgram/actions/workflows/live.yml)
and dispatch it against `main`. Other branches are skipped. The
`allow_message_tests` input defaults to false and enables the same message
lifecycle as the local flag.

Runs share a concurrency group so they do not compete for the test bot. A new
dispatch does not cancel an active run. The job has a five-minute timeout, and
credentials are available only to the harness step.

## Review observations

The workflow uploads only `.cache/live/observations.json` as the
`live-observations` artifact, including after a failed harness run when a report
exists. Reports are sanitized: credentials are omitted and private identifiers
or other private values are synthetic or omitted. Raw requests and responses
are not artifacts.

Review every report before committing selected observations or updating catalogue
verification. Check the matched condition, exact error code and description, and
the request context. A live observation describes that request at that time;
the exact hosted Bot API version is unknown, and a result does not establish
behavior for all chat types or permissions. Running the harness neither commits
observations nor publishes a release.
