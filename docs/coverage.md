# Catalogue coverage

Errorgram reviews observable Bot API responses against a pinned official server
revision. The catalogue is selective: an unknown response remains unknown. Method
examples show where a condition can occur; they restrict matching only when a rule
explicitly requires a method.

The current source review covers message editing, deletion, replies, forwarding,
copying and pinning; chat lookup, migration and bot membership; text, entity,
keyboard and permission validation; file identifiers, URL input and downloads;
update-delivery conflicts; and selected authentication, backoff and server states.

Each condition includes evidence, a representative response, diagnostic limits and
conditional guidance. Shared fixtures exercise exact descriptions, error codes,
structured parameters and nearby responses that must remain unknown. Evidence tests
also check selected literals and composed descriptions against the pinned source
survey. These tests verify the review's internal consistency; they do not execute
Telegram's server or establish hosted deployment behavior.

[Seven live observations](../observations/2026-09-16.json) cover migration, missing
file input, empty text, unsupported parse mode, unchanged edits, and edits or deletes
after deletion. The test created one silent message and removed it successfully.
Identifiers are omitted or synthetic. These observations apply to the tested
requests; the hosted API does not advertise its exact server version.

Several distinctions matter when interpreting a match:

- A missing message or invalid file identifier can be a generic replacement for a
  failed lookup. It does not prove permanent deletion or an irreparable identifier.
- Batch deletion can skip missing messages. A successful batch response does not
  enumerate which messages were removed.
- Text length checks in the server do not establish a universal public character
  limit. Method and caption limits still apply.
- Invalid JSON, an invalid object shape and insufficient authority are different
  failures. A request-format match says nothing about the bot's permissions.
- Download failures can hide transient upstream errors without exposing a retry
  delay. Only a valid structured `retry_after` supports the catalogue's server-delay
  advice.
- A response nested inside another description, such as an album item failure,
  does not match an exact leaf description.

The source survey is a review queue, not a list of public conditions. It includes
internal statuses, dynamic messages and normalization steps; one candidate may
produce several responses, and several candidates may produce the same response.
Its candidate count is therefore not a coverage denominator. TDLib-only formatting
errors, arbitrary upstream descriptions and unreviewed dynamic wrappers can remain
unknown even when they resemble a documented condition.

Consult each catalogue entry's `evidence_level` and evidence links for its support.
A source-derived example is synthetic unless an observation is explicitly recorded.
Live observations apply to the tested request and deployment; they do not imply
that every listed method or cause was reproduced. See [Follow upstream changes](updating.md)
for the process used to extend the review.
