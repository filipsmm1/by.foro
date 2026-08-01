"""Run structural checks against the static by.foro build.

Usage: python tools/check_site.py
"""

from __future__ import annotations

import html
import json
import re
import xml.etree.ElementTree as ET
from collections import Counter
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit


ROOT = Path(__file__).resolve().parents[1]
ARTICLES = json.loads((ROOT / "content" / "articles.json").read_text(encoding="utf-8"))
ARTICLES_BY_URL = {article["url"]: article for article in ARTICLES}


class PageParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.h1_count = 0
        self.title = ""
        self.description = ""
        self.canonical = ""
        self.ids: list[str] = []
        self.links: list[str] = []
        self.assets: list[str] = []
        self.images: list[dict[str, str]] = []
        self.webp_sources = 0
        self.json_blocks: list[str] = []
        self._in_title = False
        self._in_json = False
        self._json_buffer: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        values = {name: value or "" for name, value in attrs}
        if values.get("id"):
            self.ids.append(values["id"])
        if tag == "h1":
            self.h1_count += 1
        elif tag == "title":
            self._in_title = True
        elif tag == "meta" and values.get("name") == "description":
            self.description = values.get("content", "")
        elif tag == "link" and values.get("rel") == "canonical":
            self.canonical = values.get("href", "")
        elif tag == "a" and values.get("href"):
            self.links.append(values["href"])
        elif tag == "img":
            self.images.append(values)
            if values.get("src"):
                self.assets.append(values["src"])
        elif tag == "source" and values.get("type") == "image/webp":
            self.webp_sources += 1
            for candidate in values.get("srcset", "").split(","):
                asset = candidate.strip().split(" ", 1)[0]
                if asset:
                    self.assets.append(asset)
        elif tag == "script" and values.get("type") == "application/ld+json":
            self._in_json = True
            self._json_buffer = []

    def handle_endtag(self, tag: str) -> None:
        if tag == "title":
            self._in_title = False
        elif tag == "script" and self._in_json:
            self._in_json = False
            self.json_blocks.append("".join(self._json_buffer).strip())

    def handle_data(self, data: str) -> None:
        if self._in_title:
            self.title += data
        if self._in_json:
            self._json_buffer.append(data)


def canonical_pages() -> list[Path]:
    return sorted(ROOT.rglob("index.html"))


def local_target(value: str) -> Path | None:
    parsed = urlsplit(value)
    if parsed.scheme or parsed.netloc or not parsed.path or not parsed.path.startswith("/"):
        return None
    path = unquote(parsed.path)
    if path == "/":
        return ROOT / "index.html"
    candidate = ROOT / path.lstrip("/")
    if path.endswith("/"):
        return candidate / "index.html"
    return candidate


def main() -> None:
    errors: list[str] = []
    titles: list[tuple[str, Path]] = []
    descriptions: list[tuple[str, Path]] = []

    for path in canonical_pages():
        parser = PageParser()
        parser.feed(path.read_text(encoding="utf-8"))
        relative = path.relative_to(ROOT)

        if parser.h1_count != 1:
            errors.append(f"{relative}: expected one H1, found {parser.h1_count}")
        if not parser.title.strip():
            errors.append(f"{relative}: missing title")
        else:
            titles.append((parser.title.strip(), relative))
        if not parser.description.strip():
            errors.append(f"{relative}: missing meta description")
        else:
            descriptions.append((parser.description.strip(), relative))
        if not parser.canonical.startswith("https://byforo.com/"):
            errors.append(f"{relative}: missing or invalid canonical")

        duplicate_ids = [key for key, count in Counter(parser.ids).items() if count > 1]
        if duplicate_ids:
            errors.append(f"{relative}: duplicate IDs {', '.join(duplicate_ids)}")

        for image in parser.images:
            if "alt" not in image:
                errors.append(f"{relative}: image missing alt attribute: {image.get('src', '')}")
            if not image.get("width") or not image.get("height"):
                errors.append(f"{relative}: image missing width/height: {image.get('src', '')}")
        if parser.images and parser.webp_sources < len(parser.images):
            errors.append(
                f"{relative}: {len(parser.images)} images but only {parser.webp_sources} WebP sources"
            )

        for value in parser.links + parser.assets:
            target = local_target(value)
            if target is not None and not target.exists():
                errors.append(f"{relative}: broken local target {value}")

        for block in parser.json_blocks:
            try:
                json.loads(block)
            except json.JSONDecodeError as exc:
                errors.append(f"{relative}: invalid JSON-LD ({exc.msg})")

        if "blogs" in relative.parts:
            article_url = "/" + "/".join(relative.parts[:-1]) + "/"
            article = ARTICLES_BY_URL.get(article_url)
            if article is None:
                errors.append(f"{relative}: missing from content/articles.json")
                continue
            expected_title = article.get("seoTitle", f'{article["title"]} | by.foro')
            if parser.title.strip() != expected_title:
                errors.append(f"{relative}: title does not match catalogue SEO title")
            expected_description = article.get(
                "metaDescription",
                article["excerpt"],
            )
            if parser.description.strip() != expected_description:
                errors.append(
                    f"{relative}: description does not match article catalogue"
                )
            if not 35 <= len(parser.title.strip()) <= 60:
                errors.append(f"{relative}: article title length is {len(parser.title.strip())}, expected 35-60")
            if not 145 <= len(parser.description.strip()) <= 160:
                errors.append(
                    f"{relative}: article description length is {len(parser.description.strip())}, expected 145-160"
                )
            raw = path.read_text(encoding="utf-8")
            if re.search(r'<meta\b(?=[^>]*name="robots")[^>]*noindex', raw, flags=re.I):
                errors.append(f"{relative}: article is marked noindex")
            if "<figcaption" in raw and relative.as_posix() != "blogs/fashion/how-to-wear-brooches/index.html":
                errors.append(f"{relative}: public image caption remains")
            disallowed = (
                "editorial upgrade",
                "arriving from google",
                "search intent answered",
                "rank-worthy",
                "ranking value",
                "keyword ",
                "optimized for reach",
                "optimised for reach",
            )
            lowered = raw.casefold()
            for phrase in disallowed:
                if phrase in lowered:
                    errors.append(f'{relative}: internal production phrase remains: "{phrase}"')

            body_start = re.search(r'<(?:div|article) class="article-body">', raw)
            body_end = raw.find("<!-- ARTICLE-AFTERWORD:START -->", body_start.end() if body_start else 0)
            if not body_start or body_end == -1:
                errors.append(f"{relative}: article body or afterword boundary missing")
            else:
                body_html = raw[body_start.end() : body_end]
                visible = html.unescape(re.sub(r"<[^>]+>", " ", body_html))
                word_count = len(re.findall(r"\b[\w’'-]+\b", visible, flags=re.UNICODE))
                if word_count < 900:
                    errors.append(f"{relative}: article body has only {word_count} words")

                contextual_links = {
                    urlsplit(link).path
                    for link in re.findall(r'href="([^"]+)"', body_html)
                    if urlsplit(link).path.startswith("/blogs/")
                    and urlsplit(link).path != article_url
                }
                if len(contextual_links) < 3:
                    errors.append(
                        f"{relative}: fewer than three contextual article links"
                    )

                schema_type = article.get("schemaType", "BlogPosting")
                structured_count = None
                payloads = []
                for block in parser.json_blocks:
                    try:
                        payload = json.loads(block)
                    except json.JSONDecodeError:
                        continue
                    payloads.append(payload)
                    if payload.get("@type") == schema_type:
                        structured_count = int(payload.get("wordCount", 0))
                if structured_count is None:
                    errors.append(f"{relative}: missing {schema_type} structured data")
                elif abs(word_count - structured_count) > 30:
                    errors.append(
                        f"{relative}: visible word count {word_count} differs from structured count {structured_count}"
                    )

                article_schemas = [
                    payload
                    for payload in payloads
                    if payload.get("@type") == schema_type
                ]
                breadcrumb_schemas = [
                    payload
                    for payload in payloads
                    if payload.get("@type") == "BreadcrumbList"
                ]
                if len(article_schemas) != 1:
                    errors.append(
                        f"{relative}: expected one {schema_type} schema, found {len(article_schemas)}"
                    )
                else:
                    blog_schema = article_schemas[0]
                    expected_modified = article.get("updated", article["published"])
                    if blog_schema.get("headline") != article["title"]:
                        errors.append(
                            f"{relative}: structured headline does not match article catalogue"
                        )
                    if not str(blog_schema.get("dateModified", "")).startswith(
                        expected_modified
                    ):
                        errors.append(
                            f"{relative}: structured dateModified does not match catalogue"
                        )
                    if blog_schema.get("author", {}).get("url") != (
                        "https://byforo.com/about/"
                    ):
                        errors.append(
                            f"{relative}: structured author is missing the About URL"
                        )
                if len(breadcrumb_schemas) != 1:
                    errors.append(
                        f"{relative}: expected one BreadcrumbList schema, found {len(breadcrumb_schemas)}"
                    )
                else:
                    crumbs = breadcrumb_schemas[0].get("itemListElement", [])
                    expected_crumbs = 4 if article.get("breadcrumbTopic") else 3
                    if len(crumbs) != expected_crumbs or crumbs[-1].get("name") != article["title"]:
                        errors.append(
                            f"{relative}: breadcrumb schema does not match article hierarchy"
                        )

            department = relative.parts[1]
            slug = relative.parts[2]
            expected_image_prefix = f"/assets/images/blogs/{department}/{slug}/"
            article_figures = re.findall(
                r'<figure\b[^>]*class="[^"]*\barticle-(?:hero|inline)-image\b[^"]*"[^>]*>.*?</figure>',
                raw,
                flags=re.S,
            )
            article_images = [
                source
                for figure in article_figures
                for source in re.findall(r'<img\b[^>]*\bsrc="([^"]+)"', figure)
            ]
            if len(article_images) < 3:
                errors.append(f"{relative}: fewer than three article images")
            for source in article_images:
                if not source.startswith(expected_image_prefix):
                    errors.append(f"{relative}: mismatched article image {source}")

    for label, records in (("title", titles), ("description", descriptions)):
        grouped: dict[str, list[Path]] = {}
        for value, path in records:
            grouped.setdefault(value, []).append(path)
        for value, paths in grouped.items():
            if len(paths) > 1:
                errors.append(f"duplicate {label} on {', '.join(map(str, paths))}: {value}")

    not_found = (ROOT / "404.html").read_text(encoding="utf-8")
    if not (
        'content="noindex, follow" name="robots"' in not_found
        or 'name="robots" content="noindex, follow"' in not_found
    ):
        errors.append("404.html: missing noindex, follow")
    if list(ROOT.glob("*.zip")):
        errors.append("repository root contains a publishable ZIP archive")
    journal = (ROOT / "journal" / "index.html").read_text(encoding="utf-8")
    if 'data-has-stories="false"' in journal:
        errors.append("Journal exposes empty topic filters")

    expected_urls = set()
    blog_urls = set()
    for path in canonical_pages():
        parser = PageParser()
        parser.feed(path.read_text(encoding="utf-8"))
        expected_urls.add(parser.canonical)
        if "blogs" in path.relative_to(ROOT).parts:
            blog_urls.add(parser.canonical)

    sitemap_root = ET.parse(ROOT / "sitemap.xml").getroot()
    sitemap_urls = {
        node.text
        for node in sitemap_root.findall("{http://www.sitemaps.org/schemas/sitemap/0.9}url/{http://www.sitemaps.org/schemas/sitemap/0.9}loc")
        if node.text
    }
    if sitemap_urls != expected_urls:
        missing = sorted(expected_urls - sitemap_urls)
        extra = sorted(sitemap_urls - expected_urls)
        errors.append(f"sitemap mismatch; missing={missing}, extra={extra}")
    sitemap_namespace = "{http://www.sitemaps.org/schemas/sitemap/0.9}"
    image_namespace = "{http://www.google.com/schemas/sitemap-image/1.1}"
    for entry in sitemap_root.findall(f"{sitemap_namespace}url"):
        location = entry.find(f"{sitemap_namespace}loc")
        if location is None or location.text not in blog_urls:
            continue
        image_locations = {
            node.text
            for node in entry.findall(
                f"{image_namespace}image/{image_namespace}loc"
            )
            if node.text
        }
        if len(image_locations) < 3:
            errors.append(
                f"{location.text}: fewer than three images in the image sitemap"
            )
        for image_url in image_locations:
            target = local_target(image_url.replace("https://byforo.com", "", 1))
            if target is None or not target.exists():
                errors.append(
                    f"{location.text}: invalid sitemap image {image_url}"
                )

    rss_root = ET.parse(ROOT / "rss.xml").getroot()
    rss_urls = {
        node.text
        for node in rss_root.findall("./channel/item/link")
        if node.text
    }
    if rss_urls != blog_urls:
        missing = sorted(blog_urls - rss_urls)
        extra = sorted(rss_urls - blog_urls)
        errors.append(f"RSS mismatch; missing={missing}, extra={extra}")

    if errors:
        print(f"Site check failed with {len(errors)} issue(s):")
        for error in errors:
            print(f"- {error}")
        raise SystemExit(1)

    print(
        f"Site check passed: {len(canonical_pages())} canonical pages, unique metadata, "
        "complete discovery feeds, polished article copy, responsive images and no broken local targets."
    )


if __name__ == "__main__":
    main()
