"""Run structural checks against the static by.foro build.

Usage: python tools/check_site.py
"""

from __future__ import annotations

import json
from collections import Counter
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit


ROOT = Path(__file__).resolve().parents[1]


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
            article_links = {urlsplit(link).path for link in parser.links if urlsplit(link).path.startswith("/blogs/")}
            if len(article_links) < 3:
                errors.append(f"{relative}: fewer than three internal article links")

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

    if errors:
        print(f"Site check failed with {len(errors)} issue(s):")
        for error in errors:
            print(f"- {error}")
        raise SystemExit(1)

    print(
        f"Site check passed: {len(canonical_pages())} canonical pages, unique metadata, "
        "valid JSON-LD, responsive images and no broken local targets."
    )


if __name__ == "__main__":
    main()
