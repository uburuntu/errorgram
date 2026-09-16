# Errorgram

`Bad Request` is a category. Your bot needs a condition.

Errorgram turns Telegram Bot API failures into stable IDs, typed facts and concise
diagnostics. The JSON catalogue generates this package and its Python counterpart.

The package is ready to build locally; registry publication comes later. From the
repository, run `cd js && npm ci && npm pack`, then install the resulting tarball
in your bot project:

```sh
npm install /path/to/errorgram/js/errorgram-0.1.0.tgz
```

```ts
import { classify } from "errorgram";

const result = classify(response, { method: "sendMessage" });
if (result.status === "matched" && result.id === "chat.migrated") {
  console.log(result.facts.migrate_to_chat_id);
}
```

For grammY, install the framework. TypeScript projects also need its declaration
dependencies:

```sh
npm install grammy@1.46.0
# TypeScript only:
npm install --save-dev @types/node@26.5.1 @types/node-fetch@2.6.13
```

Then enrich an error where you already handle it:

```ts
import { enrich, EnrichedGrammyError } from "errorgram/grammy";

bot.catch(({ error }) => {
  const failure = enrich(error);
  if (failure instanceof EnrichedGrammyError) {
    console.log(failure.id, failure.classification.entry.summary);
  }
});
```

Enriched errors remain `GrammyError` instances and retain the original error.
Unknown errors pass through unchanged. Your application controls what happens next.

The core has no runtime dependencies. The adapter requires grammY 1.46 or later
within version 1. Node.js 22 or later is supported.

The catalogue contains 45 conditions, each with evidence and diagnostic limits.
Coverage is incomplete. Unrecognized responses return `unknown`;
conflicting evidence returns `ambiguous`; missing method context can return
`insufficient_context`. Malformed responses return `not_api_error`.

The grammY adapter reconstructs the response from framework fields. grammY
normalizes missing response parameters to an empty object; HTTP status is unavailable.
The error's `fidelity` object records these limits.

[Read the JavaScript guide](https://github.com/uburuntu/errorgram/blob/main/docs/javascript.md)
for matching rules, TypeScript narrowing and adapter details.
