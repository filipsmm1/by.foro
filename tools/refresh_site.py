"""Refresh repeated by.foro catalogue, article, SEO and image markup.

The editorial catalogue in content/articles.json is the source of truth for
related stories and department indexes. Run this after adding or editing a post:

    python tools/refresh_site.py
"""

from __future__ import annotations

import html
import json
import re
from pathlib import Path
from urllib.parse import quote


ROOT = Path(__file__).resolve().parents[1]
ARTICLES = json.loads((ROOT / "content" / "articles.json").read_text(encoding="utf-8"))
BY_URL = {article["url"]: article for article in ARTICLES}

RELATED = {
    "/blogs/fashion/fall-2026-fashion-trends-worth-wearing/": [
        "/blogs/fashion/dressing-with-intention/",
        "/blogs/fashion/literary-chic-without-the-costume/",
        "/blogs/culture/how-taste-is-built/",
    ],
    "/blogs/fashion/literary-chic-without-the-costume/": [
        "/blogs/fashion/dressing-with-intention/",
        "/blogs/fashion/fall-2026-fashion-trends-worth-wearing/",
        "/blogs/culture/how-taste-is-built/",
    ],
    "/blogs/fashion/dressing-with-intention/": [
        "/blogs/fashion/literary-chic-without-the-costume/",
        "/blogs/fashion/fall-2026-fashion-trends-worth-wearing/",
        "/blogs/culture/how-taste-is-built/",
    ],
    "/blogs/home/whimsical-interiors-without-the-theme/": [
        "/blogs/home/most-beautiful-kitchen-colour-combinations/",
        "/blogs/beauty/the-vanity-table-as-still-life/",
        "/blogs/culture/how-taste-is-built/",
    ],
    "/blogs/home/most-beautiful-kitchen-colour-combinations/": [
        "/blogs/home/whimsical-interiors-without-the-theme/",
        "/blogs/beauty/the-vanity-table-as-still-life/",
        "/blogs/culture/how-to-create-an-analogue-listening-room/",
    ],
    "/blogs/beauty/skin-scent-perfume-guide/": [
        "/blogs/beauty/the-vanity-table-as-still-life/",
        "/blogs/fashion/dressing-with-intention/",
        "/blogs/culture/how-taste-is-built/",
    ],
    "/blogs/beauty/the-vanity-table-as-still-life/": [
        "/blogs/beauty/skin-scent-perfume-guide/",
        "/blogs/home/whimsical-interiors-without-the-theme/",
        "/blogs/culture/how-taste-is-built/",
    ],
    "/blogs/culture/how-to-create-an-analogue-listening-room/": [
        "/blogs/culture/how-taste-is-built/",
        "/blogs/home/whimsical-interiors-without-the-theme/",
        "/blogs/home/most-beautiful-kitchen-colour-combinations/",
    ],
    "/blogs/culture/how-taste-is-built/": [
        "/blogs/culture/how-to-create-an-analogue-listening-room/",
        "/blogs/fashion/literary-chic-without-the-costume/",
        "/blogs/fashion/dressing-with-intention/",
    ],
}

TOPIC_LABELS = {
    "trends": "Trends",
    "personal-style": "Personal style",
    "kitchens": "Kitchens",
    "living-rooms": "Living rooms",
    "fragrance": "Fragrance",
    "beauty-objects": "Beauty objects",
    "music": "Music",
    "essays": "Essays",
}

CONTENT_EXPANSIONS = {
    "/blogs/fashion/dressing-with-intention/": {
        "toc": "<li><a href=\"#section-5\">Inventory before aspiration</a></li><li><a href=\"#section-6\">A rule for the next purchase</a></li>",
        "sections": """<section data-reveal id="section-5"><h2>Inventory before aspiration</h2><p>Before making a wish list, make a record of what is actually worn. For two ordinary weeks, note the pieces that leave the wardrobe, the combinations that survive a long day and the moments when an outfit creates friction. The useful information is rarely glamorous: a coat has the wrong pocket, a trouser only works with one shoe, a knit is too warm for every room in which it is worn.</p><p>This turns vague dissatisfaction into a practical brief. It may reveal that the wardrobe does not need more personality; it needs a better layer between shirt and coat, or one trouser length that works with the shoes already owned. It also shows which repeated shapes have earned their place. Those repetitions are not gaps to fill. They are the beginning of a signature.</p><p>A reference can still help, provided it is translated rather than copied. Our approach to <a href="/blogs/fashion/literary-chic-without-the-costume/">literary chic</a>, for example, begins with texture, proportion and restraint rather than a shopping list of bookish symbols.</p></section><section data-reveal id="section-6"><h2>A rule for the next purchase</h2><p>A useful new piece should enter at least three convincing outfits using clothes that already exist. This is a stricter test than asking whether the object is beautiful on its own. It considers the wardrobe as a system and exposes purchases that depend on buying several more things before they make sense.</p><p>Time is another useful filter. Save the image, write down the exact function and wait long enough for the first intensity to fade. If the need remains, compare material, construction and maintenance rather than searching for a cheaper approximation of the original feeling. The point is not to remove pleasure from buying clothes. It is to make the pleasure last beyond the parcel.</p><p>Trends can still sharpen an existing wardrobe. The distinction is whether they answer a real interest. Our <a href="/blogs/fashion/fall-2026-fashion-trends-worth-wearing/">Fall 2026 edit</a> keeps only the runway ideas with enough structure to survive ordinary life.</p></section>""",
    },
    "/blogs/beauty/the-vanity-table-as-still-life/": {
        "toc": "<li><a href=\"#section-5\">Edit by frequency</a></li><li><a href=\"#section-6\">Light, height and the final five minutes</a></li>",
        "sections": """<section data-reveal id="section-5"><h2>Edit by frequency, not category</h2><p>Beauty storage is often organised by product type: every lipstick together, every cream on one shelf. A working vanity benefits from a different hierarchy. Keep the daily sequence within reach, the weekly objects nearby and everything occasional behind a door. The arrangement begins to follow time rather than retail categories.</p><p>A small tray can hold the morning edit without becoming a permanent boundary. Change it when the weather, routine or mood changes. Empty products leave immediately; duplicates stay out of sight until needed. This keeps the visible surface useful and prevents beautiful packaging from becoming an excuse for visual congestion.</p><p>Fragrance deserves particular restraint because it is sensitive to heat and direct light. Keep the current bottle somewhere cool and shaded, then let its presence be quiet. Our guide to <a href="/blogs/beauty/skin-scent-perfume-guide/">skin scents</a> applies the same principle to perfume itself: intimacy can be more memorable than projection.</p></section><section data-reveal id="section-6"><h2>Light, height and the final five minutes</h2><p>Good lighting matters more than an elaborate piece of furniture. A lamp at roughly face height gives more useful illumination than a bright ceiling light and creates fewer shadows. If the table sits beside a window, keep the mirror perpendicular to it rather than directly opposite; the light will feel softer and the reflection less exposed.</p><p>Varying height prevents the surface from reading as a row of packaging. One taller bottle, a low dish and a compact leaning against a small mirror are usually enough. Leave a section completely clear for the actual act of getting ready. Negative space is not decorative minimalism here. It is working room.</p><p>The final five minutes should return the arrangement to readiness, not perfection: close the compact, wipe the brush, put the cap back on the bottle and leave tomorrow's essentials where the hand expects them. A vanity table becomes elegant when maintenance is easy enough to repeat.</p></section>""",
    },
    "/blogs/culture/how-taste-is-built/": {
        "toc": "<li><a href=\"#section-5\">Separate admiration from acquisition</a></li><li><a href=\"#section-6\">Practise with constraints</a></li>",
        "sections": """<section data-reveal id="section-5"><h2>Separate admiration from acquisition</h2><p>Not everything admired needs to be owned, worn or reproduced at home. This distinction protects taste from becoming a shopping habit. A severe concrete room can be fascinating without being a desirable place to live; an embroidered coat can be extraordinary without belonging in a particular wardrobe. Admiration is allowed to remain intellectual.</p><p>Once acquisition is removed from the decision, looking becomes more generous. It is possible to study an unfamiliar object for its construction, context or refusal of easy beauty. The reference library becomes broader because it no longer has to function as a catalogue of the self.</p><p>This is also how interests begin to cross categories. The low light and deliberate pacing of an <a href="/blogs/culture/how-to-create-an-analogue-listening-room/">analogue listening room</a> may influence the way a dinner table is arranged. The discipline of a tailored jacket may clarify why a book cover feels resolved.</p></section><section data-reveal id="section-6"><h2>Practise with constraints</h2><p>Taste becomes useful when it can make a decision. Set a small constraint: choose three materials for a room, edit ten saved images down to two, or describe a garment without using the words chic, timeless or elevated. Constraint forces preference to become specific.</p><p>Then explain the exclusion. Why did one image stay while another left? Perhaps the colour was right but the scale was timid. Perhaps the object was beautifully made but too deferential to its references. Language makes the decision available for revision; instinct alone tends to repeat itself without noticing.</p><p>The goal is not a fixed personal brand. A point of view should be recognisable yet capable of surprise. Like <a href="/blogs/fashion/literary-chic-without-the-costume/">dressing from a literary reference without wearing a costume</a>, the work lies in translating influence until it belongs to the present.</p></section>""",
    },
}


def esc(value: str) -> str:
    return html.escape(str(value), quote=True)


def article_path(article: dict) -> Path:
    return ROOT / article["url"].strip("/") / "index.html"


def webp_srcset(article: dict) -> str:
    webp = article["image"]["webp"]
    stem = webp.removesuffix(".webp")
    width = article["image"]["width"]
    candidates = [f"{stem}-640.webp 640w"]
    if width > 960:
        candidates.append(f"{stem}-960.webp 960w")
    candidates.append(f"{webp} {width}w")
    return ", ".join(candidates)


def story_card(article: dict, css_class: str = "story-card") -> str:
    department = article["department"].title()
    topic = TOPIC_LABELS[article["topic"]]
    image = article["image"]
    return (
        f'<article class="{css_class}"><a href="{esc(article["url"])}">'
        f'<figure class="media story-image"><picture><source type="image/webp" '
        f'srcset="{esc(webp_srcset(article))}" sizes="(max-width: 760px) 90vw, 31vw">'
        f'<img alt="{esc(image["alt"])}" decoding="async" height="{image["height"]}" '
        f'loading="lazy" src="{esc(image["fallback"])}" width="{image["width"]}"></picture></figure>'
        f'<div class="story-copy"><p class="kicker">{esc(department)} &middot; {esc(topic)}</p>'
        f'<h3>{esc(article["title"])}</h3><p>{esc(article["excerpt"])}</p>'
        f'<span class="read-link">Read story <span aria-hidden="true">&nearr;</span></span></div></a></article>'
    )


def article_modules(article: dict) -> str:
    slug = article["url"].strip("/").split("/")[-1]
    department = article["department"].title()
    related = [BY_URL[url] for url in RELATED[article["url"]]]
    cards = "".join(story_card(item, "related-card") for item in related)
    title = esc(article["title"])
    page_url = f'https://byforo.com{article["url"]}'
    pinterest = (
        "https://www.pinterest.com/pin/create/button/?url="
        + quote(page_url, safe="")
        + "&media="
        + quote(f'https://byforo.com{article["image"]["fallback"]}', safe="")
        + "&description="
        + quote(article["title"], safe="")
    )
    return f'''<!-- ARTICLE-AFTERWORD:START -->
<section class="article-afterword" aria-label="About this story and The FORO Letter">
  <div class="article-credit"><p class="kicker">About the desk</p><h2>Edited by by.foro.</h2><p>by.foro Editorial is the independent desk behind the Journal. Every story is reviewed for clarity, usefulness and visual judgement, with corrections handled openly.</p><p class="article-credit__links"><a href="/about/">About by.foro</a><a href="/editorial-policy/">How we work</a></p><div class="article-share" aria-label="Share this story"><button type="button" data-share-story data-share-title="{title}">Share story</button><button type="button" data-copy-link>Copy link</button><a href="{esc(pinterest)}" target="_blank" rel="noopener noreferrer">Save to Pinterest</a></div></div>
  <div class="article-letter"><p class="kicker">The FORO Letter</p><h2>Keep the next story close.</h2><p>One considered email across fashion, rooms, beauty and culture. Request an invitation; no daily noise.</p><form action="https://formsubmit.co/hello@byforo.com" class="newsletter-form" data-ajax-form data-form-kind="newsletter" method="post"><input name="_subject" type="hidden" value="New FORO Letter request from {esc(slug)}"><input name="source" type="hidden" value="{esc(article["url"])}"><input name="_template" type="hidden" value="table"><input autocomplete="off" class="hp" name="_honey" tabindex="-1" type="text"><label for="newsletter-{esc(slug)}">Email address</label><div class="field-line"><input autocomplete="email" id="newsletter-{esc(slug)}" name="email" placeholder="you@example.com" required type="email"><button type="submit">Request invitation</button></div><label class="consent"><input name="consent" required type="checkbox" value="Yes"><span>I agree to receive The FORO Letter and understand I can unsubscribe at any time.</span></label><p aria-live="polite" class="form-status"></p></form></div>
</section>
<!-- ARTICLE-AFTERWORD:END -->
<!-- RELATED-STORIES:START -->
<section class="related-stories" aria-labelledby="related-{esc(slug)}"><header><div><p class="kicker">Continue reading</p><h2 id="related-{esc(slug)}">Three stories, chosen for this one.</h2></div><a class="text-link" href="/{article["department"]}/">Explore FORO {esc(department)}</a></header><div class="related-grid">{cards}</div></section>
<!-- RELATED-STORIES:END -->'''


def add_further_reading(text: str, article: dict) -> str:
    if "<!-- FURTHER-READING:START -->" in text:
        text = re.sub(
            r"<!-- FURTHER-READING:START -->.*?<!-- FURTHER-READING:END -->",
            "",
            text,
            flags=re.S,
        )
    related = [BY_URL[url] for url in RELATED[article["url"]][:2]]
    links = " and ".join(
        f'<a href="{esc(item["url"])}">{esc(item["title"])}</a>' for item in related
    )
    block = (
        '<!-- FURTHER-READING:START --><aside class="article-further" aria-label="Further reading">'
        f'<p class="kicker">Further reading</p><p>Continue the idea with {links}.</p>'
        "</aside><!-- FURTHER-READING:END -->"
    )
    return text.replace('<div class="article-end">', f'{block}<div class="article-end">', 1)


def expand_article(text: str, article: dict) -> str:
    expansion = CONTENT_EXPANSIONS.get(article["url"])
    if not expansion or f'id="section-6"' in text:
        return text
    text = text.replace(
        '</ol><button class="copy-link"',
        f'{expansion["toc"]}</ol><button class="copy-link"',
        1,
    )
    text = text.replace(
        '<div class="article-end">',
        f'{expansion["sections"]}<div class="article-end">',
        1,
    )
    text = re.sub(
        r'(<meta content=")2026-07-19T10:00:00\+02:00(" property="article:modified_time")',
        r'\g<1>2026-07-21T12:00:00+02:00\g<2>',
        text,
        count=1,
    )
    text = re.sub(
        r'("dateModified":")2026-07-19T10:00:00\+02:00(")',
        r'\g<1>2026-07-21T12:00:00+02:00\g<2>',
        text,
        count=1,
    )
    text = text.replace('<span>19 July 2026</span><span>6 min read</span>', '<span>Updated 21 July 2026</span><span>7 min read</span>', 1)
    text = text.replace('<span>19 July 2026</span><span>5 min read</span>', '<span>Updated 21 July 2026</span><span>7 min read</span>', 1)
    return text


def update_word_count(text: str) -> str:
    match = re.search(r'<(?:div|article) class="article-body">(.*?)</(?:div|article)>\s*</div>', text, re.S)
    if not match:
        return text
    visible = re.sub(r'<script.*?</script>|<style.*?</style>', ' ', match.group(1), flags=re.S)
    visible = html.unescape(re.sub(r'<[^>]+>', ' ', visible))
    count = len(re.findall(r"\b[\w’-]+\b", visible, flags=re.UNICODE))
    return re.sub(r'("wordCount":)\d+', rf'\g<1>{count}', text, count=1)


def refresh_articles() -> None:
    for article in ARTICLES:
        path = article_path(article)
        text = path.read_text(encoding="utf-8")
        text = expand_article(text, article)
        text = add_further_reading(text, article)
        modules = article_modules(article)
        if "<!-- ARTICLE-AFTERWORD:START -->" in text:
            text = re.sub(
                r'<!-- ARTICLE-AFTERWORD:START -->.*?<!-- RELATED-STORIES:END -->',
                modules,
                text,
                flags=re.S,
            )
        else:
            text = re.sub(r'<section class="next-story">.*?</section>', modules, text, count=1, flags=re.S)
        text = update_word_count(text)
        path.write_text(text, encoding="utf-8", newline="\n")


def department_modules(department: str) -> tuple[str, str]:
    stories = [item for item in ARTICLES if item["department"] == department]
    counts: dict[str, int] = {}
    for item in stories:
        counts[item["topic"]] = counts.get(item["topic"], 0) + 1
    links = [f'<a href="/journal/?department={department}">All {department.title()} <small>{len(stories)}</small></a>']
    for topic, count in counts.items():
        links.append(
            f'<a href="/journal/?department={department}&amp;topic={topic}">{esc(TOPIC_LABELS[topic])} <small>{count}</small></a>'
        )
    topics = (
        f'<section class="department-topics" aria-label="Browse {department.title()} topics">'
        f'<span>Browse {department.title()}</span><nav>{"".join(links)}</nav></section>'
    )
    remaining = stories[1:]
    cards = "".join(story_card(item) for item in remaining)
    more = (
        '<!-- DEPARTMENT-STORIES:START -->'
        f'<section class="section-head section-head--compact"><div><p class="kicker">The {department.title()} archive</p>'
        f'<h2>More from FORO {department.title()}.</h2></div><a class="text-link" href="/journal/?department={department}">View all {len(stories)} stories</a></section>'
        f'<section class="story-grid story-grid--department" aria-label="More {department.title()} stories">{cards}</section>'
        '<!-- DEPARTMENT-STORIES:END -->'
    )
    return topics, more


def refresh_departments() -> None:
    for department in ("fashion", "home", "beauty", "culture"):
        path = ROOT / department / "index.html"
        text = path.read_text(encoding="utf-8")
        topics, more = department_modules(department)
        text = re.sub(r'<section class="department-topics".*?</section>', topics, text, count=1, flags=re.S)
        if "<!-- DEPARTMENT-STORIES:START -->" in text:
            text = re.sub(
                r'<!-- DEPARTMENT-STORIES:START -->.*?<!-- DEPARTMENT-STORIES:END -->',
                more,
                text,
                count=1,
                flags=re.S,
            )
        else:
            text = re.sub(
                r'(<section class="feature-story".*?</section>)',
                rf'\g<1>{more}',
                text,
                count=1,
                flags=re.S,
            )
        path.write_text(text, encoding="utf-8", newline="\n")


def journal_schema() -> str:
    items = [
        {
            "@type": "ListItem",
            "position": index,
            "url": f'https://byforo.com{article["url"]}',
            "name": article["title"],
        }
        for index, article in enumerate(ARTICLES, start=1)
    ]
    data = {
        "@context": "https://schema.org",
        "@type": "CollectionPage",
        "name": "The by.foro Journal",
        "url": "https://byforo.com/journal/",
        "mainEntity": {
            "@type": "ItemList",
            "numberOfItems": len(items),
            "itemListElement": items,
        },
    }
    return '<script id="journal-collection-schema" type="application/ld+json">' + json.dumps(data, separators=(",", ":")) + "</script>"


def refresh_journal() -> None:
    path = ROOT / "journal" / "index.html"
    text = path.read_text(encoding="utf-8")
    text = re.sub(r'<button[^>]+data-has-stories="false"[^>]*>.*?</button>', '', text)
    text = text.replace(
        '<main id="main"><section class="page-hero page-hero--journal"><div data-reveal><p class="kicker">The complete Journal</p><h1>Every story, <em>in one place.</em></h1></div><p data-reveal>Search the full archive, browse a department or narrow it to a useful topic. New stories join this index automatically as the catalogue grows.</p></section>',
        '<main id="main"><section class="page-hero page-hero--journal"><div data-reveal><p class="kicker">The complete Journal</p><h1>Find your <em>next story.</em></h1></div><div class="journal-hero__intro" data-reveal><p>Search the archive or browse the active departments and topics.</p><a class="text-link" href="#journal-library-title">Browse all nine stories</a></div></section>',
    )
    text = text.replace('<h2 id="journal-library-title">Find what you want to read.</h2>', '<h2 id="journal-library-title">Browse the Journal.</h2>')
    text = re.sub(r'(?:Updated )+19 July 2026 &middot; 12 min', 'Updated 19 July 2026 &middot; 12 min', text)
    text = text.replace('<p class="story-date">19 July 2026 &middot; 12 min', '<p class="story-date">Updated 19 July 2026 &middot; 12 min')
    text = text.replace('<p class="story-date">19 July 2026 &middot; 6 min', '<p class="story-date">Updated 21 July 2026 &middot; 7 min')
    text = text.replace('<p class="story-date">19 July 2026 &middot; 5 min', '<p class="story-date">Updated 21 July 2026 &middot; 7 min')
    schema = journal_schema()
    if 'id="journal-collection-schema"' in text:
        text = re.sub(r'<script id="journal-collection-schema".*?</script>', schema, text, count=1, flags=re.S)
    else:
        text = text.replace('</head>', f'{schema}</head>', 1)
    path.write_text(text, encoding="utf-8", newline="\n")


FIGURE_PICTURE = re.compile(
    r'(<figure\b[^>]*class="([^"]+)"[^>]*>\s*<picture>)(.*?)(</picture>)',
    re.S,
)


def sizes_for(classes: str) -> str:
    if "full-bleed-image" in classes:
        return "100vw"
    if "article-hero-image" in classes:
        return "(max-width: 760px) 90vw, 93vw"
    if "article-inline-image" in classes:
        return "(max-width: 760px) 90vw, 760px"
    if "story-image" in classes:
        return "(max-width: 760px) 90vw, (max-width: 1080px) 45vw, 31vw"
    if "category-hero__image" in classes or "home-hero__image" in classes:
        return "(max-width: 760px) 90vw, 45vw"
    return "(max-width: 760px) 90vw, 55vw"


def responsive_picture(match: re.Match[str]) -> str:
    opening, classes, inner, closing = match.groups()
    image_match = re.search(r'<img\b([^>]+)>', inner)
    if not image_match:
        return match.group(0)
    attrs = image_match.group(1)
    src_match = re.search(r'\bsrc="([^"]+\.jpg)"', attrs)
    width_match = re.search(r'\bwidth="(\d+)"', attrs)
    if not src_match or not width_match:
        return match.group(0)
    jpg = src_match.group(1)
    width = int(width_match.group(1))
    webp = jpg[:-4] + ".webp"
    stem = webp[:-5]
    srcset = [f"{stem}-640.webp 640w"]
    if width > 960:
        srcset.append(f"{stem}-960.webp 960w")
    srcset.append(f"{webp} {width}w")
    source = f'<source type="image/webp" srcset="{", ".join(srcset)}" sizes="{sizes_for(classes)}">'
    inner = re.sub(r'<source\b[^>]*type="image/webp"[^>]*>', source, inner, count=1)
    if 'type="image/webp"' not in inner:
        inner = source + inner
    opening = re.sub(r'\s+tabindex="0"', '', opening)
    return opening + inner + closing


def refresh_image_markup() -> None:
    for path in ROOT.rglob("index.html"):
        text = path.read_text(encoding="utf-8")
        for article in ARTICLES:
            fallback = re.escape(article["image"]["fallback"])
            alt = esc(article["image"]["alt"])
            pattern = re.compile(rf'<img\b(?=[^>]*\bsrc="{fallback}")([^>]*)>')

            def update_alt(match: re.Match[str]) -> str:
                attrs = re.sub(r'\balt="[^"]*"', f'alt="{alt}"', match.group(1), count=1)
                if 'alt="' not in attrs:
                    attrs = f' alt="{alt}"' + attrs
                return f'<img{attrs}>'

            text = pattern.sub(update_alt, text)
        text = FIGURE_PICTURE.sub(responsive_picture, text)
        path.write_text(text, encoding="utf-8", newline="\n")


def refresh_metadata() -> None:
    path = ROOT / "404.html"
    text = path.read_text(encoding="utf-8")
    text = re.sub(
        r'<meta\s+(?:name="robots"\s+content="[^"]+"|content="[^"]+"\s+name="robots")\s*/?>',
        '<meta content="noindex, follow" name="robots"/>',
        text,
        count=1,
    )
    path.write_text(text, encoding="utf-8", newline="\n")

    replacements = {
        ROOT / "terms" / "index.html": "The terms governing access to and use of by.foro, including intellectual property, acceptable use, liability and contact information.",
        ROOT / "accessibility" / "index.html": "Read by.foro's accessibility commitment, supported features, known limitations and how to report a barrier or request assistance.",
    }
    for page, description in replacements.items():
        text = page.read_text(encoding="utf-8")
        text = re.sub(r'<meta content="[^"]*" name="description"/>', f'<meta content="{esc(description)}" name="description"/>', text, count=1)
        page.write_text(text, encoding="utf-8", newline="\n")

    kitchen = article_path(BY_URL["/blogs/home/most-beautiful-kitchen-colour-combinations/"])
    text = kitchen.read_text(encoding="utf-8")
    old = "The Most Beautiful Kitchen Colour Combinations Right Now | by.foro"
    new = "10 Beautiful Kitchen Colour Combinations | by.foro"
    text = text.replace(f'<title>{old}</title>', f'<title>{new}</title>')
    text = text.replace(f'property="og:title"/><meta content="{old}"', f'property="og:title"/><meta content="{new}"') if False else text
    text = text.replace(f'<meta content="{old}" property="og:title"/>', f'<meta content="{new}" property="og:title"/>')
    text = text.replace(f'<meta content="{old}" name="twitter:title"/>', f'<meta content="{new}" name="twitter:title"/>')
    kitchen.write_text(text, encoding="utf-8", newline="\n")


def refresh_newsletter_language() -> None:
    for path in ROOT.rglob("index.html"):
        text = path.read_text(encoding="utf-8")
        text = text.replace('>Join the letter</button>', '>Request invitation</button>')
        path.write_text(text, encoding="utf-8", newline="\n")


def main() -> None:
    refresh_articles()
    refresh_departments()
    refresh_journal()
    refresh_metadata()
    refresh_newsletter_language()
    refresh_image_markup()
    print(f"Refreshed {len(ARTICLES)} articles, four departments and the Journal.")


if __name__ == "__main__":
    main()
