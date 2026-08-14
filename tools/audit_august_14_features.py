"""Focused content and media audit for the five 14 August features."""
from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
URLS = [
    "/blogs/fashion/how-to-wear-a-bib-necklace/",
    "/blogs/culture/pen-pal-letter-ideas-for-adults/",
    "/blogs/home/circus-interior-design/",
    "/blogs/beauty/niche-perfume-collection/",
    "/blogs/home/red-marble-bathroom-ideas/",
]

def text_content(fragment: str) -> str:
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", fragment)).strip()

def main() -> None:
    problems = []
    for url in URLS:
        path = ROOT / url.strip("/") / "index.html"
        source = path.read_text(encoding="utf-8")
        title = re.search(r"<title>(.*?)</title>", source, re.S).group(1)
        description = re.search(r'<meta name="description" content="(.*?)">', source, re.S).group(1)
        body = re.search(r'<div class="article-body">(.*?)<div class="article-end">', source, re.S).group(1)
        words = len(re.findall(r"\b[\w’'-]+\b", text_content(body)))
        images = re.findall(r'<img [^>]*src="([^"]+)"[^>]*alt="([^"]*)"', source)
        h1s = len(re.findall(r"<h1(?:\s|>)", source))
        schemas = len(re.findall(r'application/ld\+json', source))
        print(f"{url} words={words} title={len(title)} meta={len(description)} images={len(images)} h1={h1s} schemas={schemas}")
        if not 1800 <= words <= 2300:
            problems.append(f"{url}: {words} article words")
        if not 50 <= len(title) <= 60:
            problems.append(f"{url}: SEO title length {len(title)}")
        if not 145 <= len(description) <= 160:
            problems.append(f"{url}: meta description length {len(description)}")
        if len(images) != 3 or any(not alt.strip() for _, alt in images):
            problems.append(f"{url}: expected exactly 3 images with alt text")
        if h1s != 1 or schemas < 2:
            problems.append(f"{url}: heading or schema count")
        if "—" in source:
            problems.append(f"{url}: contains an em dash")

    files = []
    for url in URLS:
        files.extend((ROOT / "assets/images/blogs" / "/".join(url.strip("/").split("/")[1:])).glob("*.webp"))
    full = [path for path in files if not re.search(r"-(640|960)\.webp$", path.name)]
    hashes = [hashlib.sha256(path.read_bytes()).hexdigest() for path in full]
    print(f"full_images={len(full)} unique_hashes={len(set(hashes))} largest_webp_kb={max(path.stat().st_size for path in files) // 1024}")
    if len(full) != 15 or len(set(hashes)) != 15:
        problems.append("image set is missing or contains duplicates")
    if problems:
        print(json.dumps(problems, indent=2))
        raise SystemExit(1)
    print("Focused feature audit passed.")

if __name__ == "__main__":
    main()
