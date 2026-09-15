#!/usr/bin/env python3
"""Check the built documentation, search index and machine-readable exports."""

from __future__ import annotations

import argparse
import json
import re
import sys
import xml.etree.ElementTree as ET
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urljoin, urlsplit

ROOT = Path(__file__).resolve().parents[1]
SITE_URL = "https://errorgram.rmbk.me"


class SiteError(ValueError):
    """The built site does not meet its publication checks."""


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SiteError(message)


def compact(text: str) -> str:
    return " ".join(text.split())


class Page(HTMLParser):
    """Read static content and links without executing client-side scripts."""

    def __init__(self, html: str):
        super().__init__(convert_charrefs=True)
        self.links: list[tuple[str, bool]] = []
        self.anchors: set[str] = set()
        self.canonicals: list[str] = []
        self.descriptions: list[str] = []
        self.parts: list[str] = []
        self.title_parts: list[str] = []
        self.hidden = 0
        self.in_title = False
        self.feed(html)

    def handle_starttag(self, tag: str, attributes: list[tuple[str, str | None]]) -> None:
        attrs = dict(attributes)
        if tag in {"script", "style", "template"}:
            self.hidden += 1
        if tag == "title":
            self.in_title = True
        if value := attrs.get("id"):
            self.anchors.add(value)
        if tag == "a" and (value := attrs.get("name")):
            self.anchors.add(value)
        canonical = tag == "link" and "canonical" in (attrs.get("rel") or "").split()
        if tag in {"a", "link"} and not canonical and (value := attrs.get("href")):
            self.links.append((value, tag == "a"))
        if tag in {"script", "img", "source", "video", "audio", "iframe"}:
            if value := attrs.get("src"):
                self.links.append((value, False))
        if canonical:
            self.canonicals.append(attrs.get("href") or "")
        if tag == "meta" and attrs.get("name") == "description":
            self.descriptions.append(attrs.get("content") or "")

    def handle_endtag(self, tag: str) -> None:
        if tag in {"script", "style", "template"}:
            self.hidden = max(0, self.hidden - 1)
        if tag == "title":
            self.in_title = False

    def handle_data(self, data: str) -> None:
        if self.in_title:
            self.title_parts.append(data)
        elif not self.hidden:
            self.parts.append(data)

    @property
    def text(self) -> str:
        return compact("".join(self.parts))

    @property
    def title(self) -> str:
        return compact("".join(self.title_parts))


def page_url(path: Path, dist: Path, site_url: str) -> str:
    relative = path.relative_to(dist).as_posix()
    if relative.endswith("index.html"):
        relative = relative.removesuffix("index.html")
    return f"{site_url}/{relative}"


def local_target(url: str, dist: Path, site_url: str) -> Path | None:
    parsed = urlsplit(url)
    if parsed.scheme not in {"http", "https"} or parsed.netloc != urlsplit(site_url).netloc:
        return None
    path = (dist / unquote(parsed.path).lstrip("/")).resolve()
    require(path.is_relative_to(dist), f"Link escapes the site: {url}")
    if path.is_dir():
        path /= "index.html"
    if not path.is_file() and not parsed.path.endswith("/"):
        alternative = Path(str(path) + ".html")
        if alternative.is_file():
            path = alternative
    require(path.is_file(), f"Broken internal link: {url}")
    return path


def check_links(
    links: list[tuple[str, bool]],
    source_url: str,
    dist: Path,
    site_url: str,
    pages: dict[Path, Page],
) -> None:
    for href, check_anchor in links:
        url = urljoin(source_url, href)
        target = local_target(url, dist, site_url)
        fragment = unquote(urlsplit(url).fragment).split(":~:text=", 1)[0]
        if target in pages and check_anchor and fragment:
            require(fragment in pages[target].anchors, f"Broken internal anchor: {url}")


def markdown_links(text: str) -> list[tuple[str, bool]]:
    return [(url, True) for url in re.findall(r"\[[^\]\n]*\]\(([^\s)]+)\)", text)]


def evidence_url(item: dict, sources: dict) -> str:
    source = sources[item["source"]]
    if source["kind"] == "official_documentation":
        return source["url"]
    start, end = item["lines"]
    return (
        f"{source['repository']}/blob/{source['revision']}/{item['path']}"
        f"#L{start}-L{end}"
    )


def check_site(
    dist: Path,
    catalogue: dict,
    schema: dict,
    site_url: str = SITE_URL,
) -> tuple[int, int]:
    dist = dist.resolve()
    site_url = site_url.rstrip("/")
    require(dist.is_dir(), "No built site found. Run make build-site first.")
    pages = {
        path: Page(path.read_text(encoding="utf-8")) for path in sorted(dist.rglob("*.html"))
    }
    require(bool(pages), "The site has no static HTML pages.")
    for path, page in pages.items():
        url = page_url(path, dist, site_url)
        check_links(page.links, url, dist, site_url, pages)
        if path.name == "index.html":
            require(page.canonicals == [url], f"Wrong canonical URL: {url}")
        for canonical in page.canonicals:
            require(canonical.startswith(site_url + "/"), f"Wrong canonical domain: {canonical}")

    def read(relative: str) -> str:
        path = dist / relative
        require(path.is_file(), f"Missing site output: {relative}")
        return path.read_text(encoding="utf-8")

    require(read("CNAME").strip() == urlsplit(site_url).hostname, "CNAME has the wrong domain.")
    require(json.loads(read("catalogue.json")) == catalogue, "Published catalogue has drifted.")
    require(json.loads(read("schema.json")) == schema, "Published schema has drifted.")

    locations: set[str] = set()
    sitemaps = sorted(dist.glob("sitemap*.xml"))
    require(bool(sitemaps), "No sitemap was built.")
    for path in sitemaps:
        for element in ET.parse(path).iter():
            if element.tag.rsplit("}", 1)[-1] == "loc" and element.text:
                url = element.text.strip()
                require(url.startswith(site_url + "/"), f"Wrong sitemap domain: {url}")
                local_target(url, dist, site_url)
                locations.add(url)
    robots = read("robots.txt")
    robot_sitemaps = re.findall(r"(?im)^Sitemap:\s*(\S+)", robots)
    require(bool(robot_sitemaps), "robots.txt does not advertise a sitemap.")
    for url in robot_sitemaps:
        require(url in {page_url(path, dist, site_url) for path in sitemaps},
                f"robots.txt advertises an unknown sitemap: {url}")

    llms = read("llms.txt")
    full = read("llms-full.txt")
    llms_urls = {urljoin(site_url + "/llms.txt", url) for url, _ in markdown_links(llms)}
    for resource in ("llms-full.txt", "catalogue.json", "schema.json"):
        require(site_url + "/" + resource in llms_urls, f"llms.txt omits {resource}.")
    for path in [*dist.rglob("*.md"), dist / "llms.txt", dist / "llms-full.txt"]:
        check_links(markdown_links(path.read_text(encoding="utf-8")),
                    page_url(path, dist, site_url), dist, site_url, pages)

    for entry in catalogue["entries"]:
        identifier = entry["id"]
        relative = f"errors/{identifier}"
        url = f"{site_url}/{relative}/"
        path = dist / relative / "index.html"
        require(path in pages, f"Missing condition page: {identifier}")
        page = pages[path]
        require(page.canonicals == [url], f"Wrong canonical URL: {identifier}")
        require(identifier in page.title, f"Condition ID missing from title: {identifier}")
        require(bool(page.descriptions) and bool(page.descriptions[0].strip()),
                f"Missing search description: {identifier}")
        require(identifier in page.text, f"Condition ID is not static HTML: {identifier}")
        require(compact(entry["summary"]) in page.text, f"Missing summary: {identifier}")
        descriptions = [entry["example"]["response"]["description"]]
        descriptions.extend(
            rule[key] for rule in entry["match_any"]
            for key in ("description_exact", "description_template") if key in rule
        )
        for description in descriptions:
            require(compact(description) in page.text,
                    f"Response text is not static HTML: {identifier}: {description}")
        hrefs = {urljoin(url, href) for href, _ in page.links}
        for item in entry["evidence"]:
            expected = evidence_url(item, catalogue["sources"])
            # A one-line citation may use GitHub's shorter #L123 spelling.
            alternatives = {expected}
            if item.get("lines", [0, 1])[0] == item.get("lines", [0, 1])[1]:
                alternatives.add(expected.rsplit("-L", 1)[0])
            require(bool(alternatives & hrefs), f"Missing evidence link: {identifier}")
        require(url in locations, f"Sitemap omits condition: {identifier}")
        require(identifier in llms and identifier in full, f"AI exports omit: {identifier}")
        require(entry["summary"] in full and descriptions[0] in full,
                f"Full AI documentation omits condition content: {identifier}")
        for suffix in ("/", ".md"):
            require(f"{site_url}/{relative}{suffix}" in llms_urls,
                    f"llms.txt omits {relative}{suffix}")
        require(f"{site_url}/{relative}.md" in hrefs,
                f"Condition page does not link its Markdown: {identifier}")
        markdown = read(relative + ".md")
        require(identifier in markdown and entry["summary"] in markdown
                and descriptions[0] in markdown,
                f"Incomplete Markdown export: {identifier}")
        require(json.loads(read(relative + ".json")) == entry,
                f"Published condition JSON has drifted: {identifier}")

    search = next((dist / name for name in ("pagefind", "_pagefind")
                   if (dist / name).is_dir()), None)
    require(search is not None, "No Pagefind search output was built.")
    assert search is not None
    require((search / "pagefind.js").is_file(), "Pagefind JavaScript is missing.")
    require((search / "pagefind-entry.json").is_file(), "Pagefind entry index is missing.")
    for suffix in ("*.pf_index", "*.pf_fragment"):
        require(any(path.stat().st_size for path in search.rglob(suffix)),
                f"Pagefind has no populated {suffix} files.")
    return len(pages), len(catalogue["entries"])


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dist", type=Path, default=ROOT / "site/dist")
    args = parser.parse_args()
    try:
        catalogue = json.loads((ROOT / "catalogue/errors.json").read_text(encoding="utf-8"))
        schema = json.loads((ROOT / "catalogue/schema.json").read_text(encoding="utf-8"))
        pages, conditions = check_site(args.dist, catalogue, schema)
    except (SiteError, OSError, ValueError, ET.ParseError) as error:
        print(f"Site check failed: {error}", file=sys.stderr)
        return 1
    print(f"Site checks passed: {pages} pages, {conditions} conditions, search and AI exports.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
