"""Exercise publication checks without requiring a Node build during pytest."""

import copy
import html
import json
from pathlib import Path

import pytest

from tools.check_site import SITE_URL, Page, SiteError, check_site, evidence_url

ROOT = Path(__file__).resolve().parents[2]


@pytest.fixture
def built_site(tmp_path):
    catalogue = json.loads((ROOT / "catalogue/errors.json").read_text(encoding="utf-8"))
    catalogue["entries"] = [catalogue["entries"][0], catalogue["entries"][-1]]
    schema = {"type": "object"}

    def write(relative, content):
        path = tmp_path / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")

    write("CNAME", "errorgram.rmbk.me\n")
    write("catalogue.json", json.dumps(catalogue))
    write("schema.json", json.dumps(schema))
    write("robots.txt", f"User-agent: *\nAllow: /\nSitemap: {SITE_URL}/sitemap.xml\n")
    llms = [f"[Full documentation]({SITE_URL}/llms-full.txt)",
            f"[Catalogue]({SITE_URL}/catalogue.json)", f"[Schema]({SITE_URL}/schema.json)"]
    full = []
    locations = []
    for entry in catalogue["entries"]:
        identifier = entry["id"]
        url = f"{SITE_URL}/errors/{identifier}/"
        locations.append(f"<url><loc>{url}</loc></url>")
        description = entry["example"]["response"]["description"]
        evidence = "\n".join(
            f'<a href="{evidence_url(item, catalogue["sources"])}">Source</a>'
            for item in entry["evidence"]
        )
        template = entry["match_any"][0].get("description_template", "")
        write(f"errors/{identifier}/index.html", f"""
<!doctype html><html><head>
<title>{identifier} — Errorgram</title>
<meta name="description" content="{html.escape(entry['summary'])}">
<link rel="canonical" href="{url}"></head><body>
<main><h1 id="condition">{identifier}</h1><p>{entry['summary']}</p>
<pre><span>{html.escape(description[:10])}</span><span>{html.escape(description[10:])}</span></pre>
<pre>{html.escape(template)}</pre>{evidence}
<a href="#condition">Condition</a><a href="/errors/{identifier}.md">Markdown</a>
<a href="/errors/{identifier}.json">JSON</a></main></body></html>
""")
        write(f"errors/{identifier}.json", json.dumps(entry))
        write(f"errors/{identifier}.md", f"# {identifier}\n\n{entry['summary']}\n\n{description}\n")
        full.append(f"# {identifier}\n\n{entry['summary']}\n\n{description}\n")
        llms.extend([f"[{identifier}]({url})",
                     f"[Markdown]({SITE_URL}/errors/{identifier}.md)"])
    write("llms.txt", "\n".join(llms))
    write("llms-full.txt", "\n".join(full))
    write("sitemap.xml", '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'
          + "".join(locations) + "</urlset>")
    write("pagefind/pagefind.js", "export const search = () => {};\n")
    write("pagefind/pagefind-entry.json", '{"version":"1.0.0"}')
    write("pagefind/index/en.pf_index", "test-index")
    write("pagefind/fragment/en.pf_fragment", "test-fragment")
    return tmp_path, catalogue, schema


def test_built_site_links_html_search_and_data_are_consistent(built_site):
    assert check_site(*built_site) == (2, 2)


def test_astro_404_canonical_need_not_be_a_physical_page(built_site):
    (built_site[0] / "404.html").write_text(
        f'<link rel="canonical" href="{SITE_URL}/404/"><h1>Page not found</h1>', encoding="utf-8"
    )
    assert check_site(*built_site) == (3, 2)


@pytest.mark.parametrize(("relative", "message"), [
    ("errors/message.not_modified/index.html", "Broken internal link|Missing condition page"),
    ("errors/message.not_modified.md", "Broken internal link|Missing site output"),
    ("llms-full.txt", "Broken internal link|Missing site output"),
    ("pagefind/index/en.pf_index", "Pagefind has no populated"),
])
def test_missing_published_outputs_fail(built_site, relative, message):
    (built_site[0] / relative).unlink()
    with pytest.raises(SiteError, match=message):
        check_site(*built_site)


@pytest.mark.parametrize(("relative", "old", "new", "message"), [
    ("CNAME", "errorgram.rmbk.me", "uburuntu.github.io", "CNAME has the wrong domain"),
    ("errors/message.not_modified/index.html", f"{SITE_URL}/errors/",
     f"{SITE_URL}/errorgram/errors/",
     "Broken internal link|Wrong canonical URL"),
    ("errors/message.not_modified/index.html", 'href="#condition"', 'href="#missing"',
     "Broken internal anchor"),
    ("errors/message.not_modified/index.html", "#L106-L113", "#L1-L2", "Missing evidence link"),
    ("errors/message.not_modified/index.html", "<title>message.not_modified", "<title>Unknown",
     "Condition ID missing from title"),
    ("robots.txt", "sitemap.xml", "missing.xml", "unknown sitemap"),
    ("sitemap.xml", "errorgram.rmbk.me", "example.com", "Wrong sitemap domain"),
    ("llms.txt", "[Markdown](https://errorgram.rmbk.me/errors/message.not_modified.md)", "",
     "llms.txt omits errors/message.not_modified.md"),
    ("llms-full.txt", "message.not_modified", "unrelated.condition", "AI exports omit"),
])
def test_publication_regressions_fail(built_site, relative, old, new, message):
    path = built_site[0] / relative
    content = path.read_text(encoding="utf-8")
    assert old in content
    path.write_text(content.replace(old, new), encoding="utf-8")
    with pytest.raises(SiteError, match=message):
        check_site(*built_site)


@pytest.mark.parametrize("relative", ["catalogue.json", "schema.json",
                                     "errors/message.not_modified.json"])
def test_exports_must_equal_canonical_data(built_site, relative):
    path = built_site[0] / relative
    data = json.loads(path.read_text(encoding="utf-8"))
    data["unexpected"] = True
    path.write_text(json.dumps(data), encoding="utf-8")
    with pytest.raises(SiteError, match="drifted"):
        check_site(*built_site)


def test_script_data_does_not_count_as_readable_error_content(built_site):
    path = built_site[0] / "errors/message.not_modified/index.html"
    content = path.read_text(encoding="utf-8")
    content = content.replace("<pre><span>", "<script><span>").replace(
        "</span></pre>", "</span></script>"
    )
    path.write_text(content, encoding="utf-8")
    with pytest.raises(SiteError, match="Response text is not static HTML"):
        check_site(*built_site)


def test_full_ai_export_needs_content_beyond_an_index(built_site):
    (built_site[0] / "llms-full.txt").write_text(
        "message.not_modified\nwebhook.certificate_too_large\n", encoding="utf-8"
    )
    with pytest.raises(SiteError, match="Full AI documentation omits condition content"):
        check_site(*built_site)


def test_safely_escaped_markdown_summary_keeps_its_meaning(built_site):
    dist, catalogue, schema = built_site
    entry = catalogue["entries"][0]
    old_summary = entry["summary"]
    entry["summary"] = "The parse_mode value & formatting were rejected."
    identifier = entry["id"]
    (dist / "catalogue.json").write_text(json.dumps(catalogue))
    (dist / f"errors/{identifier}.json").write_text(json.dumps(entry))
    page = dist / f"errors/{identifier}/index.html"
    page.write_text(page.read_text().replace(old_summary, html.escape(entry["summary"])))
    for path in (dist / "llms-full.txt", dist / f"errors/{identifier}.md"):
        path.write_text(path.read_text().replace(
            old_summary, r"The parse\_mode value &amp; formatting were rejected."
        ))
    assert check_site(dist, catalogue, schema) == (2, 2)


def test_new_condition_requires_a_dedicated_page(built_site):
    dist, catalogue, schema = built_site
    catalogue = copy.deepcopy(catalogue)
    new_entry = copy.deepcopy(catalogue["entries"][0])
    new_entry["id"] = "new.condition"
    catalogue["entries"].append(new_entry)
    (dist / "catalogue.json").write_text(json.dumps(catalogue), encoding="utf-8")
    with pytest.raises(SiteError, match="Missing condition page: new.condition"):
        check_site(dist, catalogue, schema)


def test_html_parser_decodes_entities_and_joins_highlighted_tokens():
    page = Page('<p><span>can</span><span>&#39;t</span> &amp; <b>won&#39;t</b></p>'
                '<script>unreadable text</script><style>invisible text</style>')
    assert page.text == "can't & won't"
