# Follow upstream changes

Canonical page: https://errorgram.rmbk.me/updating/

Telegram adds methods, rewrites messages, and changes how errors reach the Bot API. Errorgram tracks those changes against a pinned source revision.

The survey produces candidates for review. It does not change the catalogue or recommend a recovery action.

## Scan a revision

Use a local clone of the [official server](https://github.com/tdlib/telegram-bot-api). Fetching updates is separate from scanning:

```sh
git -C ../telegram-bot-api fetch origin --tags
python tools/upstream.py scan \
  --source ../telegram-bot-api \
  --ref e3e9dd8e5b3d7ab8537cd5a10dc31d5ffa8f82d1 \
  --output .cache/upstream-next.json
python tools/upstream.py diff \
  catalogue/upstream.json .cache/upstream-next.json \
  --output .cache/upstream-diff.json
```

Choose the tag or commit to review. `--ref` resolves to an immutable commit; omitting it uses `HEAD`. The scanner reads committed Git objects, so it neither switches branches nor includes staged, edited, or untracked files. Dirty tracked source is reported as context. TDLib does not need to be checked out.

If your network requires bypassing proxy variables, prefix the fetch command with `env -u HTTP_PROXY -u HTTPS_PROXY -u http_proxy -u https_proxy`.

## Read the diff

| Field | What changed |
| --- | --- |
| `added`, `removed` | Candidate messages and expressions. |
| `normalizer_changes` | Message rewriting, including branches and codes. |
| `occurrence_changes` | Moved or duplicated call sites; line shifts do not create new candidates. |
| `file_changes` and method lists | Context for changes the lexer cannot interpret. |

Each snapshot records the API version, commit, TDLib pin, and source hashes. Candidate fingerprints belong to the scanner; they are separate from Errorgram condition IDs.

## Review before accepting

Trace each useful candidate to a response path. An internal status, a normalization input, and a public description can contain different text. Dynamic expressions need context; a source literal alone does not establish a reachable API response.

For a catalogue update, retain the stable condition ID where its meaning holds, pin its evidence, and add representative matching and nonmatching fixtures. Keep the verification status honest: reading source is not a live reproduction.

Regenerate bindings and documentation with `make generate`, then run `make check` before replacing the baseline.

## Understand the survey's limits

The lexer skips comments, quoted code, declarations, and common logging statements. It joins adjacent literals and retains dynamic expressions. It does not compile C++, expand macros, resolve templates, or trace calls.

TDLib, remote Telegram responses, and dependency behavior remain outside the survey. Counts describe source candidates, not complete Bot API coverage.

[Contribute a condition](https://errorgram.rmbk.me/contributing/) · [Read this page as Markdown](https://errorgram.rmbk.me/updating.md)
