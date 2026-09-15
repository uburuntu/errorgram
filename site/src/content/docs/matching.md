---
title: "How matching works"
description: "Understand Errorgram's match statuses, exact descriptions, structured parameters, method context, stable IDs, and evidence levels."
---

Telegram supplies a broad code and a description. Errorgram adds a condition ID when the available evidence supports one.

The [JSON catalogue](/catalogue.json) is the source of truth. Each record contains match rules, possible causes, diagnostic limits, guidance, and evidence. Generated Python and TypeScript bindings use the same records and IDs.

## Read the result

| Status | Meaning |
| --- | --- |
| `matched` | One supported condition fits. `id` and `entry` are available. |
| `unknown` | The response is an API error, but no supported condition fits safely. |
| `ambiguous` | Conditions or structured signals conflict. See `candidates`. |
| `insufficient_context` | A possible match needs the API method. See `candidates`. |
| `not_api_error` | The input lacks a valid Bot API error envelope. |

A matched ID identifies what can be observed. It does not prove one underlying cause. [chat.not_found](/errors/chat.not_found/), for example, can result from several lookup failures.

## Match conservatively

Fields within a rule are combined with AND; `match_any` combines alternatives with OR.

- Codes come from the JSON response. HTTP status is separate information.
- Exact descriptions preserve case and punctuation.
- Templates match the whole description. Literal text is escaped; named captures accept typed ASCII digits.
- API methods are compared after ASCII lowercasing.
- Numeric predicates accept finite, integral values within JavaScript's safe integer range. Booleans and numeric strings do not qualify.
- Valid structured parameters take precedence over description text. Malformed recovery parameters produce `unknown`; mutually exclusive signals produce `ambiguous`.
- A recognized recovery parameter with an incompatible code produces `unknown`.
- Competing conditions remain ambiguous. Missing context cannot silently select a competing rule.

`facts` contains values extracted from the response, such as `retry_after` or an upload's byte count. Version-specific constants remain in the condition's metadata.

Unknown response fields are preserved. New Telegram wording can fall back without breaking existing handlers.

## Keep framework behavior

The adapters are opt-in. Known conditions gain a precise type or ID while retaining framework catch compatibility. Unknown and out-of-scope exceptions pass through unchanged.

grammY retains useful response fields. aiogram can discard codes and rewrite messages. Adapters label reconstructed or inferred information and retain the original exception. For exact wire evidence, classify the raw response.

Your application owns retries, suppression, and state changes. Classification itself has none of those effects.

## Read evidence and versions

`source_derived`, `documented`, and `observed` describe the evidence behind a record. A source-derived example is synthetic; it is not a captured production response.

Catalogue, schema, and package versions are separate. Source references identify reviewed revisions, not the release that first introduced a condition. Stable IDs survive wording changes; changed meaning requires review.

[Read this page as Markdown](/matching.md)
