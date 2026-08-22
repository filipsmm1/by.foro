"""Validate every story in the 22-26 August release queue without publishing it."""

from __future__ import annotations

import html
import json
import re
import sys
from datetime import datetime, timedelta
from pathlib import Path
from urllib.parse import urlsplit

import build_august_two_features as base
from august_22_scheduled_content import ARTICLES
from publish_august_22_schedule import published_label, visible_word_count


ROOT = Path(__file__).resolve().parents[1]


def fail(message: str) -> None:
    print(f"ERROR: {message}")
    raise SystemExit(1)


def main() -> None:
    urls = {str(item["url"]): str(item["publish_on"]) for item in ARTICLES}
    if len(urls) != len(ARTICLES):
        fail("duplicate scheduled URL")

    dates = [datetime.strptime(str(item["publish_on"]), "%Y-%m-%d") for item in ARTICLES]
    if any(later - earlier != timedelta(days=1) for earlier, later in zip(dates, dates[1:])):
        fail("release dates are not consecutive")

    for item in ARTICLES:
        seo = str(item["seo"])
        description = str(item["description"])
        body = str(item["body"])
        url = str(item["url"])
        publish_on = str(item["publish_on"])
        words = visible_word_count(body)
        if not 35 <= len(seo) <= 60:
            fail(f"{url}: SEO title length {len(seo)}")
        if not 145 <= len(description) <= 160:
            fail(f"{url}: meta description length {len(description)}")
        if not 1800 <= words <= 2300:
            fail(f"{url}: visible word count {words}")
        if "—" in body or "&mdash;" in body:
            fail(f"{url}: em dash remains")

        inline_images = re.findall(r'<img\b[^>]*\bsrc="([^"]+)"', body)
        all_images = [f'{item["hero"]}.jpg', *inline_images]
        if len(all_images) != 3 or len(set(all_images)) != 3:
            fail(f"{url}: expected three unique article images")
        expected_prefix = f'/assets/images/blogs/{item["department"].lower()}/{url.strip("/").split("/")[-1]}/'
        for image_path in all_images:
            if not image_path.startswith(expected_prefix):
                fail(f"{url}: mismatched image {image_path}")
            source = ROOT / image_path.lstrip("/")
            variants = [
                source,
                source.with_suffix(".webp"),
                source.with_name(f"{source.stem}-640.webp"),
                source.with_name(f"{source.stem}-960.webp"),
            ]
            missing = [path for path in variants if not path.exists()]
            if missing:
                fail(f"{url}: missing image variants {missing}")

        contextual = {
            urlsplit(link).path
            for link in re.findall(r'href="([^"]+)"', body)
            if urlsplit(link).path.startswith("/blogs/") and urlsplit(link).path != url
        }
        if len(contextual) < 3:
            fail(f"{url}: fewer than three contextual internal links")
        for target in contextual:
            target_path = ROOT / target.strip("/") / "index.html"
            if target_path.exists():
                continue
            if target not in urls or urls[target] > publish_on:
                fail(f"{url}: link will be broken on publication: {target}")

        base.PUBLISHED = publish_on
        base.PUBLISHED_LABEL = published_label(publish_on)
        base.PUBLISHED_ISO = f"{publish_on}T08:15:00+02:00"
        document = base.page(
            url,
            seo,
            str(item["title"]),
            description,
            str(item["deck"]),
            str(item["department"]),
            str(item["topic"]),
            str(item["hero"]),
            str(item["alt"]),
            body,
            "BlogPosting",
            words,
            list(item["keywords"]),
        )
        if len(re.findall(r"<h1\b", document)) != 1:
            fail(f"{url}: expected one H1")
        schema_match = re.search(
            r'<script id="article-schema" type="application/ld\+json">(.*?)</script>',
            document,
            flags=re.S,
        )
        if not schema_match:
            fail(f"{url}: missing article schema")
        schema = json.loads(html.unescape(schema_match.group(1)))
        if schema.get("wordCount") != words or schema.get("headline") != item["title"]:
            fail(f"{url}: article schema does not match copy")

        print(
            f"OK {publish_on} {url}: {words} words, "
            f"{len(contextual)} contextual links, 3 unique images"
        )

    print(f"Scheduled-story check passed: {len(ARTICLES)} complete articles across five consecutive days.")


if __name__ == "__main__":
    try:
        main()
    except (KeyError, TypeError, ValueError, json.JSONDecodeError) as exc:
        print(f"ERROR: {exc}")
        sys.exit(1)
