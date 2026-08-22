"""Build due stories from the 22-26 August 2026 by.foro schedule.

The script is idempotent. By default it publishes through today's date in
Europe/Warsaw. Use ``--through YYYY-MM-DD`` for local validation.
"""

from __future__ import annotations

import argparse
import html
import json
import re
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

import build_august_two_features as base
from august_22_scheduled_content import ARTICLES


ROOT = Path(__file__).resolve().parents[1]
CATALOGUE = ROOT / "content" / "articles.json"
SCHEDULE = ROOT / "content" / "publishing_schedule.json"
MONTHS = (
    "January",
    "February",
    "March",
    "April",
    "May",
    "June",
    "July",
    "August",
    "September",
    "October",
    "November",
    "December",
)


def visible_word_count(body: str) -> int:
    text = html.unescape(re.sub(r"<[^>]+>", " ", body))
    return len(re.findall(r"\b[\w’'-]+\b", text, flags=re.UNICODE))


def published_label(value: str) -> str:
    parsed = datetime.strptime(value, "%Y-%m-%d")
    return f"{parsed.day} {MONTHS[parsed.month - 1]} {parsed.year}"


def article_record(item: dict[str, object], words: int) -> dict[str, object]:
    department = str(item["department"])
    topic = str(item["topic"])
    hero = str(item["hero"])
    return {
        "title": item["title"],
        "seoTitle": item["seo"],
        "department": department.lower(),
        "topic": topic.lower().replace(" ", "-"),
        "published": item["publish_on"],
        "readingMinutes": max(8, round(words / 195)),
        "readingWordsPerMinute": 195,
        "url": item["url"],
        "excerpt": html.unescape(str(item["deck"])),
        "metaDescription": item["description"],
        "image": {
            "webp": f"{hero}.webp",
            "fallback": f"{hero}.jpg",
            "alt": item["alt"],
            "width": 1536,
            "height": 1024,
        },
        "articleSection": topic,
        "breadcrumbTopic": True,
    }


def build_page(item: dict[str, object], words: int) -> None:
    publish_on = str(item["publish_on"])
    base.PUBLISHED = publish_on
    base.PUBLISHED_LABEL = published_label(publish_on)
    base.PUBLISHED_ISO = f"{publish_on}T08:15:00+02:00"
    document = base.page(
        str(item["url"]),
        str(item["seo"]),
        str(item["title"]),
        str(item["description"]),
        str(item["deck"]),
        str(item["department"]),
        str(item["topic"]),
        str(item["hero"]),
        str(item["alt"]),
        str(item["body"]),
        "BlogPosting",
        words,
        list(item["keywords"]),
    )
    destination = ROOT / str(item["url"]).strip("/") / "index.html"
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(document, encoding="utf-8", newline="\n")


def add_reciprocal_link(item: dict[str, object]) -> None:
    reciprocal = dict(item["reciprocal"])
    path = ROOT / str(reciprocal["path"])
    sentence = str(reciprocal["sentence"])
    text = path.read_text(encoding="utf-8")
    if sentence in text:
        return
    opening = re.search(r'(<p class="article-opening">.*?</p>)', text, flags=re.S)
    if not opening:
        raise RuntimeError(f"Could not find opening paragraph in {path}")
    text = text[: opening.end()] + sentence + text[opening.end() :]
    path.write_text(text, encoding="utf-8", newline="\n")


def write_schedule(public_urls: set[str]) -> None:
    records = [
        {
            "title": item["title"],
            "url": item["url"],
            "publishOn": item["publish_on"],
            "status": "published" if item["url"] in public_urls else "scheduled",
        }
        for item in ARTICLES
    ]
    SCHEDULE.write_text(
        json.dumps(records, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
        newline="\n",
    )


def publish(through: str) -> int:
    datetime.strptime(through, "%Y-%m-%d")
    catalogue = json.loads(CATALOGUE.read_text(encoding="utf-8"))
    known = {article["url"] for article in catalogue}
    due = [
        item
        for item in ARTICLES
        if str(item["publish_on"]) <= through and str(item["url"]) not in known
    ]
    additions: list[dict[str, object]] = []
    for item in due:
        words = visible_word_count(str(item["body"]))
        build_page(item, words)
        add_reciprocal_link(item)
        additions.append(article_record(item, words))
        print(f"Published {item['url']} ({words} words)")

    if additions:
        additions.sort(key=lambda article: str(article["published"]), reverse=True)
        catalogue = additions + catalogue
        CATALOGUE.write_text(
            json.dumps(catalogue, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
            newline="\n",
        )
        known.update(str(article["url"]) for article in additions)
    else:
        print(f"No stories due through {through}")

    write_schedule(known)
    return len(additions)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--through",
        default=datetime.now(ZoneInfo("Europe/Warsaw")).strftime("%Y-%m-%d"),
        help="Publish all scheduled stories on or before this date.",
    )
    args = parser.parse_args()
    publish(args.through)


if __name__ == "__main__":
    main()
