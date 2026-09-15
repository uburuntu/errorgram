---
title: "JavaScript & grammY"
description: "Use Errorgram's JavaScript and TypeScript bindings, narrow on stable condition IDs, and enrich grammY exceptions without changing framework behavior."
---

Give a Telegram response a stable identity, with TypeScript facts that narrow alongside the condition ID.

The package ships ESM JavaScript and TypeScript declarations. [Build from the repository](/getting-started/), then install `dist/errorgram-0.1.0.tgz` in your bot project. The core has no runtime dependencies.

## Classify a response

Pass the error body to `classify`. Include the API method when available: some responses need that context to distinguish their meaning.

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

`result.response` is the original object. `facts` contains values extracted from the response; version-specific metadata stays in `entry`. Import `catalogue` from the same package for the complete data and source references.

Only `matched` results carry an ID and entry. Other statuses are `unknown`, `ambiguous`, `insufficient_context`, and `not_api_error`; see [how matching works](/matching/) for their meaning.

## Add grammY details

Install the optional framework:

```sh
npm install grammy@1.46.0
```

For strict TypeScript checks, grammY's declarations also need Node and node-fetch types:

```sh
npm install --save-dev @types/node@26.5.1 @types/node-fetch@2.6.13
```

Enrich errors inside your existing handler:

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

`EnrichedGrammyError` extends `GrammyError`, so broad framework catches still work. It keeps the method, payload, description, parameters, message, and stack. The original exception is available through both `original` and `cause`.

`id` and `facts` provide shortcuts to classification data. Narrow on `classification.id` for precise fact types. For a `BotError` wrapper, pass its `error` field as shown above.

Unknown errors and `HttpError` pass through unchanged. Repeated enrichment returns the same object. The adapter never retries, suppresses an error, or changes bot state.

## Understand framework fidelity

The `fidelity` object describes what the framework makes available:

| Field | Value | Meaning |
| --- | --- | --- |
| `description` | `preserved` | Telegram's description remains intact. |
| `parameters` | `framework_normalized` | grammY replaces missing parameters with `{}`. |
| `method` | `preserved` | The method comes from the original exception. |
| `response` | `reconstructed` | The adapter rebuilds the body from framework fields. |

HTTP status and discarded response fields are unavailable. Use the raw response with `classify()` when you need its exact contents.

[Browse the catalogue](/catalogue/) · [Read this page as Markdown](/javascript.md)
