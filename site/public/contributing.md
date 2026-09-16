# Contribute a condition

Canonical page: https://errorgram.rmbk.me/contributing/

Start with a failure that changes how a bot should respond. Show the response, the API method, and the evidence behind your explanation.

## Make the change

1. Add or update a condition in [`catalogue/errors.json`](https://github.com/uburuntu/errorgram/blob/main/catalogue/errors.json). Keep its stable ID when wording changes but meaning does not.
2. Cite a pinned source revision, official documentation, or a reproducible observation. Distinguish an observed condition from a possible cause.
3. Add a case to [`fixtures/conformance.json`](https://github.com/uburuntu/errorgram/blob/main/fixtures/conformance.json). Include a nearby response that should not match when that distinction matters.
4. Run `make generate` and `make check`, then open a [pull request](https://github.com/uburuntu/errorgram/pulls).

Edit the catalogue to change a condition's reference page. Edit the Markdown under `site/src/content/docs/` to improve an authored guide. Generated files carry the same data into the SDKs, website, and agent exports.

## Write what you can support

Keep descriptions short and concrete. Prefer “The bot cannot resolve this chat” to a claim that the chat was deleted. One response can have several causes.

Public examples must omit bot tokens, token-bearing URLs, and private message content. Label synthetic examples as synthetic. Reading source provides useful evidence, but it does not establish live hosted behavior.

Adapters preserve framework fields, catch compatibility, and the original exception. A match must never trigger a retry or change application state.

## Keep the inventory open

The catalogue, generated bindings, documentation, and original project code use the [MIT license](https://github.com/uburuntu/errorgram/blob/main/LICENSE). External source references retain their own licenses.

Have a new response but no complete patch? [Try the playground](https://errorgram.rmbk.me/playground/), then [open the unknown-error form](https://github.com/uburuntu/errorgram/issues/new?template=unknown-error.yml) with a sanitized example, the method, framework version, and what you have verified. The form starts empty; the playground never copies your input into it.

[Follow upstream changes](https://errorgram.rmbk.me/updating/) · [Read this page as Markdown](https://errorgram.rmbk.me/contributing.md)
