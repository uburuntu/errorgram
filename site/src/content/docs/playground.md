---
title: "Try a Bot API response"
description: "Classify Telegram Bot API error JSON locally in your browser. See its stable condition ID, explanation, extracted facts, and reference page."
---

## How to use the playground

Paste the JSON response body and choose **Classify response**. The API method is optional; add it when a result needs more context. **Load example** inserts a synthetic catalogue response. **Clear** removes your input and result.

The [interactive form](https://errorgram.rmbk.me/playground/) runs the Errorgram JavaScript classifier in your browser. No bot token is needed.

For example, this response matches [request.retry_after](/errors/request.retry_after/) and extracts `retry_after: 5`:

```json
{
  "ok": false,
  "error_code": 429,
  "description": "Too Many Requests: retry after 5",
  "parameters": { "retry_after": 5 }
}
```

## Read the result

| Status | Meaning |
| --- | --- |
| `matched` | One condition matches. Read its ID, summary, extracted facts, and linked reference. |
| `unknown` | The response is an API error, but the catalogue has no matching rule. |
| `insufficient_context` | A potential match requires the API method. Add it and try again. |
| `ambiguous` | Competing matches or conflicting parameters prevent a single result. |
| `not_api_error` | The JSON does not have the Bot API error-response shape. |

The form accepts up to 32,768 characters and explains invalid JSON before classification. Empty facts, `{}`, means no values were extracted. A condition identifies what the response establishes, not every underlying cause. Each record states its evidence. Coverage is incomplete.

## Privacy and reporting

Your response and method are never uploaded, logged, or saved by this page, and are cleared when you leave. Classification requires JavaScript; the guide and reference do not.

For an unknown error, [open the empty GitHub form](https://github.com/uburuntu/errorgram/issues/new?template=unknown-error.yml). Your input is never copied into it. Reports are public: remove tokens, token-bearing URLs, private identifiers, and message content before sharing. Include the method and whether your example is live, synthetic, or source-derived.

[How matching works](/matching/) · [Contribute a condition](/contributing/) · [Read this page as Markdown](/playground.md)
