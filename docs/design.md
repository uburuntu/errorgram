# Matching errors

Telegram supplies a broad code and a description. Errorgram adds a stable condition ID while keeping the original response available.

The catalogue is the source of truth. A record contains match rules, possible causes, diagnostic limits, guidance, and evidence. Generated Python and TypeScript bindings carry the same records and IDs.

## Results

| Status | Meaning |
| --- | --- |
| `matched` | One supported condition fits the available information. |
| `unknown` | The response is an API error, but no supported condition fits safely. |
| `ambiguous` | Conditions or structured signals conflict. |
| `insufficient_context` | A rule needs information such as the API method. |
| `not_api_error` | The input does not have a valid Bot API error envelope. |

A matched ID identifies what can be observed. It does not prove one underlying cause. `chat.not_found`, for example, can result from different lookup failures.

## Rules

Fields within a rule are combined with AND; `match_any` combines alternatives with OR.

- Codes come from the JSON response. HTTP status is separate information.
- Exact descriptions preserve case and punctuation.
- Templates match the whole description. Literal text is escaped; named captures accept typed ASCII digits.
- API method names are compared after ASCII lowercasing.
- Numeric predicates accept finite, integral values within JavaScript's safe integer range. Booleans and numeric strings do not qualify.
- Valid structured parameters take precedence over description text. Malformed recovery parameters produce `unknown`; mutually exclusive signals produce `ambiguous`.
- A recognized recovery parameter with an incompatible code produces `unknown` rather than a text-only match.
- Competing conditions remain ambiguous. Missing context must not silently select a competing rule.

`facts` contains values extracted from the response, such as `retry_after` or a byte count. Version-specific constants remain in the condition's metadata.

Unknown response fields are preserved. New Telegram wording can therefore fall back without breaking existing handlers.

## Frameworks

The adapters are opt-in. Known conditions gain a more precise type or ID while retaining framework catch compatibility. Unknown and out-of-scope exceptions pass through unchanged.

grammY retains useful response fields. aiogram can discard codes and rewrite messages. Adapters label reconstructed or inferred information and retain the original exception; they do not present reconstruction as the original wire response.

## Evidence and versions

`source_derived`, `documented`, and `observed` describe the evidence behind a record. A source-derived example is not a captured production response.

Catalogue, schema, and package versions are separate. Source references identify verified revisions, not the release that first introduced a condition. Stable IDs survive wording changes; changed meaning requires review.
