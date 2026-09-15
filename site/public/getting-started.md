# Get started

Canonical page: https://errorgram.rmbk.me/getting-started/

Start with a raw Telegram error response. Add a stable condition ID, then decide how your application should handle it.

Errorgram is at **0.1.0**. Packages are available from this repository; npm and PyPI releases have not been published yet.

## Build from source

The checked-in toolchain uses Python **3.14.7**, Node **26.8.2**, npm **12.0.2**, and [uv](https://docs.astral.sh/uv/getting-started/installation/) **0.12.15**. Dependency versions are locked.

```sh
git clone https://github.com/uburuntu/errorgram.git
cd errorgram
make setup
make check
make build
```

The build writes a Python wheel, a source distribution, and an npm tarball to `dist/`.

## Python

From the checkout, install the core package into an environment:

```sh
uv venv
uv pip install -e .
```

```python
from errorgram import classify

result = classify({
    "ok": False,
    "error_code": 400,
    "description": "Bad Request: chat not found",
}, method="sendMessage")

assert result.id == "chat.not_found"
```

Use `uv pip install -e '.[aiogram]'` to include aiogram. See [Python & aiogram](https://errorgram.rmbk.me/python/) for concrete exceptions and adapter behavior.

## JavaScript and TypeScript

After building, install the tarball in your bot project:

```sh
npm install /path/to/errorgram/dist/errorgram-0.1.0.tgz
```

```ts
import { classify } from "errorgram";

const result = classify({
  ok: false,
  error_code: 400,
  description: "Bad Request: chat not found",
}, { method: "sendMessage" });

if (result.status === "matched") {
  console.log(result.id, result.entry.summary);
}
```

The package includes ESM JavaScript and TypeScript declarations. The core has no runtime dependencies. See [JavaScript & grammY](https://errorgram.rmbk.me/javascript/) for the optional framework adapter.

## Choose a small first integration

Add `result.id` and `result.status` to your existing diagnostics. Once you understand the condition and its limits, use the ID in the part of your application that owns the handling decision.

Pass the API method when available. Keep your existing fallback for an `unknown`, `ambiguous`, or `insufficient_context` result. Read [how matching works](https://errorgram.rmbk.me/matching/) before using a classification to branch.

[Read this page as Markdown](https://errorgram.rmbk.me/getting-started.md)
