---
title: "For AI agents"
description: "Read Errorgram through llms.txt, complete Markdown documentation, individual condition pages, and the canonical JSON catalogue and schema."
---

Use structured data for matching rules and plain Markdown for explanations. Both come from the same catalogue as the human reference and SDKs.

## Choose an entry point

| Resource | Use it for |
| --- | --- |
| [llms.txt](/llms.txt) | A short introduction and an index of the documentation. |
| [llms-full.txt](/llms-full.txt) | The complete guides and condition reference in one file. |
| [catalogue.json](/catalogue.json) | IDs, exact rules, examples, diagnostic limits, and evidence. |
| [schema.json](/schema.json) | The JSON Schema for catalogue validation. |
| [Catalogue as Markdown](/catalogue.md) | A compact list of supported conditions. |

Every guide and condition has a plain Markdown version. For example:

```text
https://errorgram.rmbk.me/python.md
https://errorgram.rmbk.me/errors/chat.not_found.md
```

The website URL for that condition is `https://errorgram.rmbk.me/errors/chat.not_found/`. The ID is part of the permanent path.

## Use the evidence carefully

1. Read the catalogue version and coverage metadata before assuming a condition is supported.
2. Match against the response code, description, structured parameters, and method context. A shared phrase is not enough.
3. Keep possible causes separate from what the response establishes. Cite the condition page and its pinned evidence.
4. Preserve unknown or ambiguous results. Leave retries, suppression, and state changes to the application.

The initial catalogue is source-derived and incomplete. Examples are synthetic, and hosted API behavior has not been verified. Transport failures and framework validation errors are outside the inventory.

`llms.txt` is a discovery convention, not a requirement for clients. All exports are ordinary static files available without JavaScript or authentication.

[How matching works](/matching/) · [Read this page as Markdown](/agents.md)
