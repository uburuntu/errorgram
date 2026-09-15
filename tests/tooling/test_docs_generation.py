"""Exercise published examples, data fidelity, and safe Markdown generation."""

import ast
import copy
import json
import re

import pytest

from tools import codegen_docs
from tools.validate import load_catalogue


@pytest.fixture
def authored_docs(tmp_path, monkeypatch):
    monkeypatch.setattr(codegen_docs, "ROOT", tmp_path)
    (tmp_path / "catalogue").mkdir()
    (tmp_path / "catalogue/schema.json").write_text('{"title":"A schema"}\n')
    docs = tmp_path / "site/src/content/docs"
    docs.mkdir(parents=True)
    for slug in codegen_docs.GUIDES:
        (docs / f"{slug}.md").write_text(
            f'---\ntitle: "Guide {slug}"\ndescription: "A guide"\n---\n\n'
            f"Text for {slug}. [Catalogue](/catalogue/).\n"
        )
    return tmp_path


def test_exported_records_keep_all_fields_and_sources(authored_docs):
    catalogue = load_catalogue()
    files = codegen_docs.render(catalogue)
    assert json.loads(files["site/public/catalogue.json"]) == catalogue
    assert json.loads(files["site/public/schema.json"]) == {"title": "A schema"}
    for entry in catalogue["entries"]:
        prefix = f"site/public/errors/{entry['id']}"
        assert json.loads(files[prefix + ".json"]) == entry
        page = files[f"site/src/content/docs/errors/{entry['id']}.md"]
        assert f'slug: "errors/{entry["id"]}"' in page
        label = entry["id"].replace(".", " ").replace("_", " ").capitalize()
        assert page.startswith(f'---\ntitle: "{label} · {entry["id"]}"\n')
        assert f"](/errors/{entry['id']}.md)" in page
        assert "](/matching/)" in page
        assert "](https://errorgram.rmbk.me/matching/)" in files[prefix + ".md"]
        assert "https://github.com/uburuntu/errorgram/edit/main/catalogue/errors.json" in page
        assert f"https://errorgram.rmbk.me/errors/{entry['id']}/" in files[prefix + ".md"]
        for evidence in entry["evidence"]:
            source = catalogue["sources"][evidence["source"]]
            if "revision" in source:
                assert f"/blob/{source['revision']}/{evidence['path']}#L" in page
            else:
                assert source["url"] in page


def test_every_published_python_example_classifies_its_own_response(authored_docs, capsys):
    catalogue = load_catalogue()
    files = codegen_docs.render(catalogue)
    for entry in catalogue["entries"]:
        page = files[f"site/src/content/docs/errors/{entry['id']}.md"]
        code = re.search(r"```python\n(.*?)\n```", page, re.DOTALL)
        assert code is not None
        assert 'response = {\n    "ok": False,' in code[1]
        namespace = {}
        exec(compile(code[1], f"docs/{entry['id']}.py", "exec"), namespace)
        assert namespace["result"].id == entry["id"]
    capsys.readouterr()


def test_python_example_formatting_preserves_nested_json_values():
    response = {
        "ok": False,
        "description": 'Keep false, null, "quotes", and Unicode: café.',
        "parameters": {"future": [None, True, "a\nb", {}, []]},
    }
    assert ast.literal_eval(codegen_docs._python_literal(response)) == response


def test_agent_exports_include_authored_guides_and_all_error_pages(authored_docs):
    catalogue = load_catalogue()
    files = codegen_docs.render(catalogue)
    assert files == codegen_docs.render(copy.deepcopy(catalogue))
    for slug in codegen_docs.GUIDES:
        raw = files[f"site/public/{slug}.md"]
        assert raw.startswith(f"# Guide {slug}\n")
        assert "description:" not in raw
        assert "[Catalogue](https://errorgram.rmbk.me/catalogue/)" in raw
        assert raw.rstrip() in files["site/public/llms-full.txt"]
        assert f"https://errorgram.rmbk.me/{slug}.md" in files["site/public/llms.txt"]
    for entry in catalogue["entries"]:
        condition_id = entry["id"]
        raw = files[f"site/public/errors/{condition_id}.md"]
        assert raw.rstrip() in files["site/public/llms-full.txt"]
        assert f"https://errorgram.rmbk.me/errors/{condition_id}.md" in files[
            "site/public/llms.txt"
        ]
    manifest = json.loads(files[codegen_docs.MANIFEST])
    assert manifest["paths"] == sorted(set(files) - {codegen_docs.MANIFEST})


def test_catalogue_and_guide_edits_refresh_agent_exports(authored_docs):
    catalogue = load_catalogue()
    original = codegen_docs.render(catalogue)
    entry = catalogue["entries"][0]
    entry["summary"] = "An updated, reviewed explanation."
    updated = codegen_docs.render(catalogue)
    for path in [
        f"site/src/content/docs/errors/{entry['id']}.md",
        f"site/public/errors/{entry['id']}.md",
        f"site/public/errors/{entry['id']}.json",
        "site/src/content/docs/catalogue.md",
        "site/public/catalogue.json",
        "site/public/llms.txt",
        "site/public/llms-full.txt",
    ]:
        assert original[path] != updated[path], path
        assert entry["summary"] in updated[path], path
    guide = authored_docs / "site/src/content/docs/matching.md"
    guide.write_text(guide.read_text() + "\nNew matching guidance.\n")
    refreshed = codegen_docs.render(catalogue)
    for path in ["site/public/matching.md", "site/public/llms-full.txt"]:
        assert updated[path] != refreshed[path]
        assert "New matching guidance." in refreshed[path]


def test_catalogue_text_cannot_inject_frontmatter_html_or_code_fences(authored_docs):
    catalogue = load_catalogue()
    entry = catalogue["entries"][0]
    entry["summary"] = 'A "quoted" <script> & [link](javascript:alert(1))\n---\nslug: stolen'
    entry["diagnostic_limits"] = "<img src=x onerror=alert(1)> **not bold** | literal"
    description = "Bad Request: ```\n</script>\n```\ntext with `ticks`"
    entry["match_any"][0]["description_exact"] = description
    entry["example"]["response"]["description"] = description
    files = codegen_docs.render(catalogue)
    page = files[f"site/src/content/docs/errors/{entry['id']}.md"]
    frontmatter, body = page[4:].split("\n---\n", 1)
    metadata_description = json.loads(frontmatter.splitlines()[1].removeprefix("description: "))
    assert metadata_description == entry["summary"]
    assert f'slug: "errors/{entry["id"]}"' in frontmatter
    assert "<img" not in body
    assert "&lt;img" in body
    assert r"\*\*not bold\*\* \| literal" in body
    assert f"````text\n{description}\n````" in body
    assert json.loads(files[f"site/public/errors/{entry['id']}.json"]) == entry


@pytest.mark.parametrize("condition_id", ["../../outside", "x/y", "x.y\nslug: bad"])
def test_unsafe_condition_paths_are_rejected(authored_docs, condition_id):
    catalogue = load_catalogue()
    catalogue["entries"][0]["id"] = condition_id
    with pytest.raises(ValueError, match="safe condition IDs"):
        codegen_docs.render(catalogue)


def test_missing_guides_fail_instead_of_publishing_incomplete_exports(authored_docs):
    (authored_docs / "site/src/content/docs/python.md").unlink()
    with pytest.raises(ValueError, match="Missing authored documentation"):
        codegen_docs.render(load_catalogue())


def test_non_http_evidence_link_is_rejected(authored_docs):
    catalogue = load_catalogue()
    catalogue["sources"]["response-parameters"]["url"] = "javascript:alert(1)"
    with pytest.raises(ValueError, match=r"HTTP\(S\)"):
        codegen_docs.render(catalogue)
