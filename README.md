# Errorgram

One `BadRequest` can mean an unchanged message, a missing chat, or a request that needs a new chat ID. Your bot needs to tell them apart.

Errorgram gives Telegram Bot API errors stable IDs, useful context, and typed bindings. One JSON catalogue powers Python, JavaScript, TypeScript, aiogram, and grammY.

[Read the docs](https://errorgram.rmbk.me/) · [Find an error](https://errorgram.rmbk.me/catalogue/) · [Try a response](https://errorgram.rmbk.me/playground/) · [For AI agents](https://errorgram.rmbk.me/agents/)

```python
from errorgram import classify

failure = classify({
    "ok": False,
    "error_code": 400,
    "description": "Bad Request: chat not found",
})

if failure.id == "chat.not_found":
    print("Check the chat ID and the bot's access.")
```

```typescript
import { classify } from "errorgram";

const failure = classify({
  ok: false,
  error_code: 400,
  description: "Bad Request: chat not found",
});

if (failure.status === "matched" && failure.id === "chat.not_found") {
  console.log("Check the chat ID and the bot's access.");
}
```

## What you get

- Stable IDs for branching, logs, metrics, and documentation.
- Explanations backed by pinned source references.
- Python exception types and TypeScript types generated from the catalogue.
- Opt-in aiogram and grammY adapters that preserve existing catch behavior.
- Explicit results for unknown errors, ambiguous matches, and missing context.

Your application decides what to do next. Errorgram classifies errors; existing handlers keep control of retries, delivery, and state changes.

The catalogue covers **45 conditions**, reviewed against Bot API **10.3**. Each record links to its evidence; examples use synthetic data. [Coverage notes](docs/coverage.md) explain the limits. Transport failures and framework validation errors are outside this catalogue.

## Try it

Use Python **3.14.7**, Node **26.8.2**, npm **12.0.2**, and [uv](https://docs.astral.sh/uv/getting-started/installation/) **0.12.15**. Dependency versions are locked.

```sh
git clone https://github.com/uburuntu/errorgram.git
cd errorgram
make setup
make check
make build
```

Builds produce a Python wheel, a source distribution, and an npm tarball in `dist/`. Registry publication is a separate step.

The [release guide](docs/releasing.md) covers artifact checks and trusted publishing to PyPI and npm.

See the [Python and aiogram guide](docs/python.md), [JavaScript and grammY guide](docs/javascript.md), and [catalogue](docs/catalogue.md).

## Documentation

The [Starlight site](https://errorgram.rmbk.me/) gives every condition a searchable page, a Markdown copy, and a JSON record. `llms.txt` and `llms-full.txt` help agents read the same reference.

```sh
make docs-dev
make docs-check
make docs-browser-setup
make docs-browser-test
```

Edit guides in `site/src/content/docs/`. Condition pages and agent exports are generated with `make generate`. Passing checks on `main` publish the site to GitHub Pages; `site/public/CNAME` records the custom domain.

## Keep it current

Edit [catalogue/errors.json](catalogue/errors.json), add a shared test case, then regenerate the bindings and reference:

```sh
make generate
make check
```

The [update guide](docs/updating.md) explains how to scan a newer Telegram revision and review the differences. Source changes nominate candidates for review; the catalogue records the conditions we can support with evidence.

A monthly workflow prepares the source review. Optional [live checks](docs/live-checks.md) record selected hosted responses using a dedicated test bot. The [discovery guide](docs/discovery.md) covers search-engine submission.

[Matching rules](docs/design.md) · [Contributing](CONTRIBUTING.md) · [MIT license](LICENSE)
