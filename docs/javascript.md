# JavaScript and TypeScript

One broad exception can hide several different failures. Errorgram gives the
response a stable identity while keeping the original information available.

The package ships ESM JavaScript and TypeScript declarations. Use the Node version
in [`.node-version`](../.node-version) to build it. Until the first registry release,
install a local tarball:

```sh
cd js
npm ci
npm pack
```

Then, in your bot project:

```sh
npm install /path/to/errorgram/js/errorgram-0.1.0.tgz
```

Pass the error body to `classify`. Include the method when you have it: a download
error may need that context to distinguish it from an upload failure.

```ts
import { classify } from "errorgram";

const response = {
  ok: false,
  error_code: 400,
  description: "Bad Request: group chat was upgraded to a supergroup chat",
  parameters: { migrate_to_chat_id: -1001234567890 },
};

const result = classify(response, { method: "sendMessage" });
if (result.status === "matched" && result.id === "chat.migrated") {
  // TypeScript knows this fact is a number.
  console.log(result.facts.migrate_to_chat_id);
  console.log(result.entry.summary);
}
```

`result.response` is the original object. `facts` contains values extracted from
that response; version-specific metadata stays in `entry`. The full catalogue and
its source references are available as `catalogue` from the same import.

| Status | Meaning |
| --- | --- |
| `matched` | One condition fits. `id` and `entry` are available. |
| `unknown` | A valid API error has no safe match. |
| `ambiguous` | Evidence supports conflicting conditions. See `candidates`. |
| `insufficient_context` | A possible match needs the API method. See `candidates`. |
| `not_api_error` | The input is not a valid Bot API failure body. |

Descriptions match exactly. Structured recovery fields take precedence, and invalid
recovery fields prevent a text-only match. Telegram's `error_code` is preserved;
Errorgram does not infer an HTTP status from it.

For grammY, install the framework and enrich errors inside your existing handler:

```sh
npm install grammy@1.46.0
```

For strict TypeScript checks, grammY's declarations also need Node and node-fetch
types:

```sh
npm install --save-dev @types/node@26.5.1 @types/node-fetch@2.6.13
```

```ts
import { Bot } from "grammy";
import { enrich, EnrichedGrammyError } from "errorgram/grammy";

const bot = new Bot(process.env.BOT_TOKEN!);

bot.catch(({ error }) => {
  const failure = enrich(error);
  if (failure instanceof EnrichedGrammyError) {
    const result = failure.classification;
    console.log(result.id, result.entry.summary);
    if (result.id === "request.retry_after") {
      console.log(result.facts.retry_after); // number, in seconds
    }
  }
});
```

`EnrichedGrammyError` extends `GrammyError`, so broad framework catches still work.
It keeps the method, payload, description, parameters, message and stack. The original
exception is available through both `original` and `cause`. `id` and `facts` provide
shortcuts to classification data. Narrow on `classification.id` for precise fact types.

Unknown errors and `HttpError` pass through unchanged. Calling `enrich` again returns
the same enriched object. For a `BotError` wrapper, pass its `error` field as above.
The adapter never retries, suppresses an error or changes bot state.

The `fidelity` object describes what the framework makes available:

| Field | Value | Meaning |
| --- | --- | --- |
| `description` | `preserved` | Telegram's description remains intact. |
| `parameters` | `framework_normalized` | grammY replaces missing parameters with `{}`. |
| `method` | `preserved` | The method comes from the original exception. |
| `response` | `reconstructed` | The adapter rebuilds the body from framework fields. |

HTTP status and discarded response fields are unavailable. The core package has no
runtime dependencies; grammY is an optional peer dependency used only by the adapter.

Run `npm test` from `js/` to build the package, test its JavaScript exports and real
grammY error handling, and compile the TypeScript consumer examples. Shared fixtures
keep classifications aligned with Python. Network responses are simulated; these
tests do not contact Telegram.
