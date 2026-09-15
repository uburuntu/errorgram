# Contributing

Start with a failure that changes how a bot should respond. Show the response, the method, and the evidence behind your explanation.

1. Add or update a condition in `catalogue/errors.json`. Keep its stable ID when wording changes but meaning does not.
2. Cite a pinned source revision, official documentation, or a reproducible observation. Distinguish an observed condition from a possible cause.
3. Add a case to `fixtures/conformance.json`. Include a nearby response that should not match when that distinction matters.
4. Run `make generate` and `make check`.

Keep descriptions short and concrete. Prefer “The bot cannot resolve this chat” to a claim that the chat was deleted. One response can have several causes.

Public examples must omit bot tokens, token-bearing URLs, and private message content. Synthetic examples should say so.

Adapters preserve framework fields, catch compatibility, and the original exception. A match must never trigger a retry or change application state.

The catalogue, generated bindings, and original project code use the MIT license. External source references retain their own licenses.
