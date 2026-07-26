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
    "/blogs/home/reading-nook-ideas/": [
        "/blogs/home/quietly-dramatic-home-decor/",
        "/blogs/home/whimsical-interiors-without-the-theme/",
        "/blogs/home/most-beautiful-kitchen-colour-combinations/",
    ],
    "/blogs/home/quietly-dramatic-home-decor/": [
        "/blogs/home/reading-nook-ideas/",
        "/blogs/home/whimsical-interiors-without-the-theme/",
        "/blogs/home/most-beautiful-kitchen-colour-combinations/",
    ],
    "/blogs/fashion/fall-2026-fashion-trends-worth-wearing/": [
        "/blogs/fashion/how-to-wear-colour-again/",
        "/blogs/fashion/dressing-with-intention/",
        "/blogs/fashion/summer-loafers-outfit-guide/",
    ],
    "/blogs/fashion/literary-chic-without-the-costume/": [
        "/blogs/fashion/dressing-with-intention/",
        "/blogs/fashion/fall-2026-fashion-trends-worth-wearing/",
        "/blogs/fashion/how-to-wear-colour-again/",
    ],
    "/blogs/fashion/dressing-with-intention/": [
        "/blogs/fashion/literary-chic-without-the-costume/",
        "/blogs/fashion/fall-2026-fashion-trends-worth-wearing/",
        "/blogs/fashion/how-to-wear-colour-again/",
    ],
    "/blogs/home/whimsical-interiors-without-the-theme/": [
        "/blogs/home/quietly-dramatic-home-decor/",
        "/blogs/home/most-beautiful-kitchen-colour-combinations/",
        "/blogs/home/coffee-table-styling-that-looks-collected/",
    ],
    "/blogs/home/most-beautiful-kitchen-colour-combinations/": [
        "/blogs/home/how-to-make-a-home-look-expensive/",
        "/blogs/home/quietly-dramatic-home-decor/",
        "/blogs/home/whimsical-interiors-without-the-theme/",
    ],
    "/blogs/beauty/skin-scent-perfume-guide/": [
        "/blogs/beauty/perfume-wardrobe-by-mood/",
        "/blogs/beauty/the-vanity-table-as-still-life/",
        "/blogs/home/coffee-table-styling-that-looks-collected/",
    ],
    "/blogs/beauty/the-vanity-table-as-still-life/": [
        "/blogs/beauty/perfume-wardrobe-by-mood/",
        "/blogs/beauty/skin-scent-perfume-guide/",
        "/blogs/home/coffee-table-styling-that-looks-collected/",
    ],
    "/blogs/culture/how-to-create-an-analogue-listening-room/": [
        "/blogs/culture/how-taste-is-built/",
        "/blogs/home/coffee-table-styling-that-looks-collected/",
        "/blogs/home/whimsical-interiors-without-the-theme/",
    ],
    "/blogs/culture/how-taste-is-built/": [
        "/blogs/culture/how-to-create-an-analogue-listening-room/",
        "/blogs/fashion/literary-chic-without-the-costume/",
        "/blogs/fashion/dressing-with-intention/",
    ],
    "/blogs/home/how-to-make-a-home-look-expensive/": [
        "/blogs/home/coffee-table-styling-that-looks-collected/",
        "/blogs/home/small-entryway-that-looks-expensive/",
        "/blogs/home/bathroom-that-feels-like-a-hotel/",
    ],
    "/blogs/home/warm-minimalist-bedroom/": [
        "/blogs/home/how-to-make-a-home-look-expensive/",
        "/blogs/home/reading-nook-ideas/",
        "/blogs/home/bathroom-that-feels-like-a-hotel/",
    ],
    "/blogs/home/bathroom-that-feels-like-a-hotel/": [
        "/blogs/home/how-to-make-a-home-look-expensive/",
        "/blogs/home/warm-minimalist-bedroom/",
        "/blogs/home/small-entryway-that-looks-expensive/",
    ],
    "/blogs/home/small-entryway-that-looks-expensive/": [
        "/blogs/home/how-to-make-a-home-look-expensive/",
        "/blogs/home/coffee-table-styling-that-looks-collected/",
        "/blogs/home/outdoor-space-that-feels-expensive/",
    ],
    "/blogs/home/outdoor-space-that-feels-expensive/": [
        "/blogs/home/how-to-make-a-home-look-expensive/",
        "/blogs/home/most-beautiful-kitchen-colour-combinations/",
        "/blogs/home/quietly-dramatic-home-decor/",
    ],
    "/blogs/home/coffee-table-styling-that-looks-collected/": [
        "/blogs/home/how-to-make-a-home-look-expensive/",
        "/blogs/home/quietly-dramatic-home-decor/",
        "/blogs/home/whimsical-interiors-without-the-theme/",
    ],
    "/blogs/fashion/how-to-wear-colour-again/": [
        "/blogs/fashion/fall-2026-fashion-trends-worth-wearing/",
        "/blogs/fashion/dressing-with-intention/",
        "/blogs/fashion/summer-loafers-outfit-guide/",
    ],
    "/blogs/fashion/summer-loafers-outfit-guide/": [
        "/blogs/fashion/dressing-with-intention/",
        "/blogs/fashion/how-to-wear-colour-again/",
        "/blogs/fashion/fall-2026-fashion-trends-worth-wearing/",
    ],
    "/blogs/fashion/celebrity-style-is-getting-personal/": [
        "/blogs/fashion/fall-2026-fashion-trends-worth-wearing/",
        "/blogs/fashion/how-to-wear-colour-again/",
        "/blogs/fashion/dressing-with-intention/",
    ],
    "/blogs/beauty/perfume-wardrobe-by-mood/": [
        "/blogs/beauty/skin-scent-perfume-guide/",
        "/blogs/beauty/the-vanity-table-as-still-life/",
        "/blogs/home/coffee-table-styling-that-looks-collected/",
    ],
}

TOPIC_LABELS = {
    "trends": "Trends",
    "personal-style": "Personal style",
    "luxury-decor": "Luxury decor",
    "reading-nooks": "Reading nooks",
    "kitchens": "Kitchens",
    "bedrooms": "Bedrooms",
    "bathrooms": "Bathrooms",
    "entryways": "Entryways",
    "outdoor-living": "Outdoor living",
    "living-rooms": "Living rooms",
    "fragrance": "Fragrance",
    "beauty-routines": "Beauty routines",
    "beauty-objects": "Beauty objects",
    "music": "Music",
    "essays": "Essays",
    "celebrity-style": "Celebrity style",
    "hosting": "Hosting",
    "objects": "Objects",
}

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

EDITION_BAR = (
    '<div class="edition-bar"><span>Independent editorial</span>'
    '<span>Edition 01 &middot; 2026</span>'
    '<span>Fashion &middot; Home &middot; Beauty &middot; Culture</span></div>'
)

PRIMARY_NAV = (
    ("Start here", "/start-here/"),
    ("Journal", "/journal/"),
    ("The Edit", "/the-edit/"),
    ("Home", "/home/"),
    ("Fashion", "/fashion/"),
    ("Beauty", "/beauty/"),
    ("Culture", "/culture/"),
)

NAV_DRAWER = """<div class="nav-drawer" aria-label="Editorial index">
  <div><span>Begin</span><a href="/start-here/">Where to start</a><a href="/the-edit/">The current edit</a><a href="/journal/">Search all stories</a></div>
  <div><span>Home</span><a href="/journal/?department=home&amp;topic=reading-nooks">Reading nooks</a><a href="/journal/?department=home&amp;topic=luxury-decor">Luxury decor</a><a href="/journal/?department=home&amp;topic=kitchens">Kitchens</a><a href="/journal/?department=home&amp;q=small%20spaces">Small spaces</a></div>
  <div><span>Style and beauty</span><a href="/journal/?department=fashion">Fashion</a><a href="/journal/?department=beauty&amp;topic=fragrance">Fragrance</a><a href="/journal/?department=beauty&amp;topic=beauty-objects">Beauty objects</a><a href="/journal/?q=personal%20style">Personal style</a></div>
  <div><span>Reference</span><a href="/journal/?department=culture">Culture</a><a href="/about/">About by.foro</a><a href="/studio/">FORO Studio</a><a href="/contact/">Contact</a></div>
</div>"""

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


def route_for_path(path: Path) -> str:
    if path.name == "404.html":
        return "/404.html"
    relative = path.relative_to(ROOT)
    if relative == Path("index.html"):
        return "/"
    if relative.name == "index.html":
        return "/" + "/".join(relative.parts[:-1]) + "/"
    return "/" + "/".join(relative.parts)


def active_for(current: str, href: str) -> bool:
    if current == href:
        return True
    if href in ("/home/", "/fashion/", "/beauty/", "/culture/"):
        department = href.strip("/")
        return current.startswith(f"/blogs/{department}/")
    return False


def site_header(current: str) -> str:
    parts = []
    for label, href in PRIMARY_NAV:
        current_attr = ' aria-current="page"' if active_for(current, href) else ""
        parts.append(f'<a href="{href}"{current_attr}>{label}</a>')
    links = "".join(parts)
    return (
        '<header class="site-header" data-header><a class="wordmark" href="/" '
        'aria-label="by.foro homepage">by.foro</a><button class="menu-toggle" type="button" '
        'aria-controls="site-nav" aria-expanded="false"><span>Menu</span></button>'
        f'<nav class="site-nav" id="site-nav" aria-label="Main navigation">{links}{NAV_DRAWER}</nav></header>'
    )


def site_footer() -> str:
    return """<footer class="site-footer"><div class="footer-lead"><a class="footer-wordmark" href="/">by.foro</a><p>A point of view on fashion, interiors, beauty and contemporary culture.</p></div><div class="footer-grid"><div><h2>Begin</h2><a href="/start-here/">Start Here</a><a href="/the-edit/">The Edit</a><a href="/journal/">Journal</a></div><div><h2>Departments</h2><a href="/home/">Home</a><a href="/fashion/">Fashion</a><a href="/beauty/">Beauty</a><a href="/culture/">Culture</a></div><div><h2>Work</h2><a href="/studio/">FORO Studio</a><a href="/contact/">Contact</a><a href="/about/">About</a></div><div><h2>Standards</h2><a href="/editorial-policy/">Editorial policy</a><a href="/affiliate-disclosure/">Affiliate disclosure</a><a href="/accessibility/">Accessibility</a><a href="/privacy/">Privacy</a><a href="/cookies/">Cookies</a><a href="/terms/">Terms</a></div></div><div class="footer-bottom"><p>&copy; <span data-year>2026</span> by.foro</p><p>Curated by people, not an algorithm.</p></div></footer>"""


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


def display_date(value: str) -> str:
    year, month, day = value.split("-")
    return f"{int(day)} {MONTHS[int(month) - 1]} {year}"


def feature_story(article: dict) -> str:
    department = article["department"].title()
    topic = TOPIC_LABELS[article["topic"]]
    image = article["image"]
    return (
        '<section class="feature-story" data-reveal="">'
        '<figure class="media feature-story__image" data-zoom-media="">'
        f'<picture><source type="image/webp" srcset="{esc(webp_srcset(article))}" '
        'sizes="(max-width: 760px) 90vw, 55vw">'
        f'<img alt="{esc(image["alt"])}" decoding="async" height="{image["height"]}" loading="lazy" '
        f'src="{esc(image["fallback"])}" width="{image["width"]}"></picture></figure>'
        f'<div><p class="kicker">Latest &middot; {esc(department)} &middot; {esc(topic)}</p>'
        f'<h2>{esc(article["title"])}</h2><p>{esc(article["excerpt"])}</p>'
        f'<div class="story-meta"><span>{display_date(article["published"])}</span>'
        f'<span>{article["readingMinutes"]} min</span></div>'
        f'<a class="button button--dark" href="{esc(article["url"])}">Read the story</a></div></section>'
    )


def homepage_card(article: dict, index: int) -> str:
    css_class = "story-card story-card--featured" if index == 0 else "story-card"
    zoom = ' data-zoom-media=""' if index == 0 else ""
    department = article["department"].title()
    topic = TOPIC_LABELS[article["topic"]]
    image = article["image"]
    return (
        f'<article class="{css_class}" data-reveal=""><a href="{esc(article["url"])}">'
        f'<figure class="media story-image"{zoom}><picture><source type="image/webp" '
        f'srcset="{esc(webp_srcset(article))}" sizes="(max-width: 760px) 90vw, (max-width: 1080px) 45vw, 31vw">'
        f'<img alt="{esc(image["alt"])}" decoding="async" height="{image["height"]}" loading="lazy" '
        f'src="{esc(image["fallback"])}" width="{image["width"]}"></picture></figure>'
        f'<div class="story-copy"><p class="kicker">{esc(department)} &middot; {esc(topic)}</p>'
        f'<h3>{esc(article["title"])}</h3><p>{esc(article["excerpt"])}</p>'
        '<span class="read-link">Read story <span aria-hidden="true">&nearr;</span></span></div></a></article>'
    )


def homepage_story_grid() -> str:
    cards = "".join(homepage_card(article, index) for index, article in enumerate(ARTICLES[:4]))
    return f'<section class="story-grid story-grid--editorial">{cards}</section>'


def homepage_entry_panel() -> str:
    return """<!-- HOMEPAGE-ENTRY:START -->
<section class="luxury-ledger" aria-label="by.foro orientation" data-reveal>
  <a href="/start-here/"><span>New here</span><strong>Start with the five stories that explain the point of view.</strong></a>
  <a href="/the-edit/"><span>The Edit</span><strong>Browse the current mood, collections and essential reads.</strong></a>
  <a href="/journal/"><span>Search</span><strong>Find stories by room, object, style, problem or department.</strong></a>
</section>
<!-- HOMEPAGE-ENTRY:END -->"""


def homepage_collections() -> str:
    return """<!-- HOMEPAGE-COLLECTIONS:START -->
<section class="collection-strip" aria-labelledby="homepage-collections-title" data-reveal>
  <div><p class="kicker">Collections</p><h2 id="homepage-collections-title">Curated routes through the archive.</h2></div>
  <div class="collection-strip__grid">
    <a href="/journal/?department=home&amp;q=expensive"><span>01</span><strong>The Expensive-Looking Home</strong><p>Stone, lighting, vintage pieces and rooms with weight.</p></a>
    <a href="/journal/?department=home&amp;topic=reading-nooks"><span>02</span><strong>The Reading Room</strong><p>Small private corners, shelves and places to pause.</p></a>
    <a href="/journal/?department=fashion"><span>03</span><strong>Wardrobe With Intention</strong><p>Trends, proportion and dressing without urgency.</p></a>
    <a href="/journal/?department=beauty"><span>04</span><strong>Beauty Objects</strong><p>Fragrance, vanity tables and daily ritual.</p></a>
  </div>
</section>
<!-- HOMEPAGE-COLLECTIONS:END -->"""


def journal_card(article: dict) -> str:
    department = article["department"]
    topic = article["topic"]
    image = article["image"]
    search = " ".join(
        [
            article["title"],
            article["excerpt"],
            department,
            TOPIC_LABELS[topic],
            topic.replace("-", " "),
        ]
    ).lower()
    search = re.sub(r"\s+", " ", search)
    date = f'Updated {display_date(article["updated"])}' if article.get("updated") else display_date(article["published"])
    return (
        f'<article class="story-card" data-department="{esc(department)}" data-topic="{esc(topic)}" '
        f'data-date="{esc(article.get("updated", article["published"]))}" data-minutes="{article["readingMinutes"]}" '
        f'data-title="{esc(article["title"])}" data-search="{esc(search)}"><a href="{esc(article["url"])}">'
        f'<figure class="media story-image"><picture><source type="image/webp" srcset="{esc(webp_srcset(article))}" '
        'sizes="(max-width: 760px) 90vw, (max-width: 1080px) 45vw, 31vw">'
        f'<img alt="{esc(image["alt"])}" decoding="async" height="{image["height"]}" loading="lazy" '
        f'src="{esc(image["fallback"])}" width="{image["width"]}"></picture></figure>'
        f'<div class="story-copy"><p class="kicker">{esc(department.title())} &middot; {esc(TOPIC_LABELS[topic])}</p>'
        f'<h3>{esc(article["title"])}</h3><p>{esc(article["excerpt"])}</p>'
        f'<p class="story-date">{esc(date)} &middot; {article["readingMinutes"]} min</p>'
        '<span class="read-link">Read story <span aria-hidden="true">&nearr;</span></span></div></a></article>'
    )


def journal_department_filters() -> str:
    counts = {department: 0 for department in ("fashion", "home", "beauty", "culture")}
    for article in ARTICLES:
        counts[article["department"]] += 1
    buttons = [
        f'<button type="button" data-department="all" aria-pressed="true">All <small data-department-count="all">{len(ARTICLES)}</small></button>'
    ]
    for department in ("fashion", "home", "beauty", "culture"):
        buttons.append(
            f'<button type="button" data-department="{department}" aria-pressed="false">{department.title()} '
            f'<small data-department-count="{department}">{counts[department]}</small></button>'
        )
    return (
        '<div class="journal-filter-group" role="group" aria-label="Filter by department">'
        f'<span>Department</span><div>{"".join(buttons)}</div></div>'
    )


def journal_topic_filters() -> str:
    counts: dict[str, int] = {}
    departments: dict[str, set[str]] = {}
    for article in ARTICLES:
        topic = article["topic"]
        counts[topic] = counts.get(topic, 0) + 1
        departments.setdefault(topic, set()).add(article["department"])
    buttons = [f'<button type="button" data-topic="all" aria-pressed="true">All topics <small>{len(ARTICLES)}</small></button>']
    for topic, label in TOPIC_LABELS.items():
        if topic not in counts:
            continue
        department_list = " ".join(sorted(departments[topic]))
        buttons.append(
            f'<button type="button" data-topic="{esc(topic)}" data-departments="{esc(department_list)}" '
            f'data-has-stories="true" aria-pressed="false">{esc(label)} <small>{counts[topic]}</small></button>'
        )
    return (
        '<div class="journal-filter-group journal-topic-group" role="group" aria-label="Filter by topic">'
        f'<span>Topic</span><div>{"".join(buttons)}</div></div>'
    )


def journal_story_grid() -> str:
    return (
        '<section class="story-grid story-grid--journal" data-journal-results aria-label="Journal stories">'
        + "".join(journal_card(article) for article in ARTICLES)
        + "</section>"
    )


def journal_library() -> str:
    return f'''<section class="journal-library" aria-labelledby="journal-library-title" data-journal-library>
  <div class="journal-library__heading"><div><p class="kicker">All stories</p><h2 id="journal-library-title">Browse the Journal.</h2></div><p class="journal-status" data-journal-status aria-live="polite">Showing all {len(ARTICLES)} stories</p></div>
  <div class="journal-search-row"><label class="journal-search" for="journal-search"><span>Search the Journal</span><input id="journal-search" type="search" inputmode="search" autocomplete="off" placeholder="Try reading nooks, perfume, kitchens or personal style" data-journal-search></label><label class="journal-sort" for="journal-sort"><span>Sort</span><select id="journal-sort" data-journal-sort><option value="newest">Newest first</option><option value="longest">Long reads</option><option value="shortest">Quick reads</option><option value="az">A to Z</option></select></label><button class="journal-clear" type="button" data-journal-clear hidden>Clear search</button></div>
  <div class="journal-quick-search" aria-label="Popular searches"><span>Popular searches</span><div><button type="button" data-journal-query="reading nook">Reading nook</button><button type="button" data-journal-query="kitchen colour">Kitchen colour</button><button type="button" data-journal-query="quiet luxury">Quiet luxury</button><button type="button" data-journal-query="perfume">Perfume</button><button type="button" data-journal-query="personal style">Personal style</button></div></div>
  {journal_department_filters()}
  {journal_topic_filters()}
</section>'''


def article_modules(article: dict) -> str:
    slug = article["url"].strip("/").split("/")[-1]
    department = article["department"].title()
    related_urls = RELATED.get(article["url"])
    if not related_urls:
        related_urls = [
            item["url"]
            for item in ARTICLES
            if item["url"] != article["url"] and item["department"] == article["department"]
        ][:3]
        if len(related_urls) < 3:
            related_urls += [
                item["url"]
                for item in ARTICLES
                if item["url"] != article["url"] and item["url"] not in related_urls
            ][: 3 - len(related_urls)]
    related = [BY_URL[url] for url in related_urls[:3]]
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
    related_urls = RELATED.get(article["url"])
    if not related_urls:
        related_urls = [
            item["url"]
            for item in ARTICLES
            if item["url"] != article["url"] and item["department"] == article["department"]
        ][:2]
        if len(related_urls) < 2:
            related_urls += [
                item["url"]
                for item in ARTICLES
                if item["url"] != article["url"] and item["url"] not in related_urls
            ][: 2 - len(related_urls)]
    related = [BY_URL[url] for url in related_urls[:2]]
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


def home_compass() -> str:
    return """<!-- HOME-COMPASS:START -->
<section class="home-compass" aria-labelledby="home-compass-title" data-reveal>
  <div class="home-compass__intro"><p class="kicker">Interiors index</p><h2 id="home-compass-title">Find the room, the mood, or the problem.</h2><p>Home stories are organised by how people actually search: the room they are changing, the atmosphere they want, or the issue they need solved.</p></div>
  <div class="home-compass__columns">
    <div><span>By room</span><a href="/journal/?department=home&amp;topic=kitchens">Kitchen</a><a href="/journal/?department=home&amp;q=bedroom">Bedroom</a><a href="/journal/?department=home&amp;q=bathroom">Bathroom</a><a href="/journal/?department=home&amp;topic=living-rooms">Living room</a><a href="/journal/?department=home&amp;topic=reading-nooks">Reading nook</a><a href="/journal/?department=home&amp;q=exterior">Exterior</a></div>
    <div><span>By style</span><a href="/journal/?department=home&amp;topic=luxury-decor">Quiet luxury</a><a href="/journal/?department=home&amp;topic=living-rooms">Whimsical interiors</a><a href="/journal/?department=home&amp;q=traditional">Traditional</a><a href="/journal/?department=home&amp;q=rustic">Modern rustic</a><a href="/journal/?department=home&amp;q=parisian">Parisian</a><a href="/journal/?department=home&amp;q=mediterranean">Mediterranean</a></div>
    <div><span>By problem</span><a href="/journal/?department=home&amp;q=expensive">Make it look expensive</a><a href="/journal/?department=home&amp;q=small%20space">Small spaces</a><a href="/journal/?department=home&amp;q=colour">Colour ideas</a><a href="/journal/?department=home&amp;q=lighting">Lighting</a><a href="/journal/?department=home&amp;q=storage">Storage</a><a href="/journal/?department=home&amp;q=rental">Rental friendly</a></div>
  </div>
</section>
<!-- HOME-COMPASS:END -->"""


def refresh_departments() -> None:
    for department in ("fashion", "home", "beauty", "culture"):
        path = ROOT / department / "index.html"
        text = path.read_text(encoding="utf-8")
        topics, more = department_modules(department)
        stories = [item for item in ARTICLES if item["department"] == department]
        feature = feature_story(stories[0])
        text = re.sub(
            r'(<section class="category-hero">.*?<a class="text-link" href=")[^"]+(">\s*Read the latest story</a>)',
            rf'\g<1>{stories[0]["url"]}\g<2>',
            text,
            count=1,
            flags=re.S,
        )
        text = re.sub(r'<section class="department-topics".*?</section>', topics, text, count=1, flags=re.S)
        if department == "home":
            if "<!-- HOME-COMPASS:START -->" in text:
                text = re.sub(
                    r'<!-- HOME-COMPASS:START -->.*?<!-- HOME-COMPASS:END -->',
                    home_compass(),
                    text,
                    count=1,
                    flags=re.S,
                )
            else:
                text = text.replace(topics, topics + "\n" + home_compass(), 1)
        text = re.sub(
            r'<section class="feature-story".*?</section>(?=<!-- DEPARTMENT-STORIES:START -->)',
            feature,
            text,
            count=1,
            flags=re.S,
        )
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


def refresh_homepage() -> None:
    path = ROOT / "index.html"
    text = path.read_text(encoding="utf-8")
    text = re.sub(
        r'<div class="hero-actions">.*?</div>',
        '<div class="hero-actions"><a class="button button--dark" href="/start-here/">Start here</a><a class="text-link" href="/the-edit/">See the edit</a></div>',
        text,
        count=1,
        flags=re.S,
    )
    text = re.sub(
        r'<section aria-label="by\.foro editorial themes" class="marquee">.*?</section>',
        '<section aria-label="by.foro editorial themes" class="marquee"><div>Personal style &middot; Characterful rooms &middot; Beautiful objects &middot; Visual culture &middot; Personal style &middot; Characterful rooms &middot; Beautiful objects &middot; Visual culture</div></section>',
        text,
        count=1,
        flags=re.S,
    )
    if "<!-- HOMEPAGE-ENTRY:START -->" in text:
        text = re.sub(
            r'<!-- HOMEPAGE-ENTRY:START -->.*?<!-- HOMEPAGE-ENTRY:END -->',
            homepage_entry_panel(),
            text,
            count=1,
            flags=re.S,
        )
    else:
        text = re.sub(
            r'(<section aria-label="by\.foro editorial themes" class="marquee">.*?</section>)',
            rf'\g<1>{homepage_entry_panel()}',
            text,
            count=1,
            flags=re.S,
        )
    text = re.sub(
        r'<section class="story-grid story-grid--editorial">.*?</section>',
        homepage_story_grid(),
        text,
        count=1,
        flags=re.S,
    )
    if "<!-- HOMEPAGE-COLLECTIONS:START -->" in text:
        text = re.sub(
            r'<!-- HOMEPAGE-COLLECTIONS:START -->.*?<!-- HOMEPAGE-COLLECTIONS:END -->',
            homepage_collections(),
            text,
            count=1,
            flags=re.S,
        )
    else:
        text = re.sub(
            r'(</section>\s*)(?=<section class="foro-index")',
            rf'\g<1>{homepage_collections()}',
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
    text = re.sub(r'Browse all (?:\d+|\w+) stories', f'Browse all {len(ARTICLES)} stories', text)
    text = re.sub(r'Showing all \d+ stories', f'Showing all {len(ARTICLES)} stories', text)
    text = re.sub(
        r'<section class="journal-library".*?</section>\s*(?=<section class="story-grid story-grid--journal")',
        journal_library() + "\n\n",
        text,
        count=1,
        flags=re.S,
    )
    text = re.sub(r'(?:Updated )+19 July 2026 &middot; 12 min', 'Updated 19 July 2026 &middot; 12 min', text)
    text = text.replace('<p class="story-date">19 July 2026 &middot; 12 min', '<p class="story-date">Updated 19 July 2026 &middot; 12 min')
    text = text.replace('<p class="story-date">19 July 2026 &middot; 6 min', '<p class="story-date">Updated 21 July 2026 &middot; 7 min')
    text = text.replace('<p class="story-date">19 July 2026 &middot; 5 min', '<p class="story-date">Updated 21 July 2026 &middot; 7 min')
    schema = journal_schema()
    if 'id="journal-collection-schema"' in text:
        text = re.sub(r'<script id="journal-collection-schema".*?</script>', schema, text, count=1, flags=re.S)
    else:
        text = text.replace('</head>', f'{schema}</head>', 1)
    text = re.sub(
        r'<div class="journal-filter-group" role="group" aria-label="Filter by department">.*?</div></div>(?=\s*<div class="journal-filter-group journal-topic-group")',
        journal_department_filters(),
        text,
        count=1,
        flags=re.S,
    )
    text = re.sub(
        r'<div class="journal-filter-group journal-topic-group" role="group" aria-label="Filter by topic">.*?</div></div>(?=\s*</section>)',
        journal_topic_filters(),
        text,
        count=1,
        flags=re.S,
    )
    text = re.sub(
        r'<section class="story-grid story-grid--journal" data-journal-results aria-label="Journal stories">.*?</section>',
        journal_story_grid(),
        text,
        count=1,
        flags=re.S,
    )
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


def refresh_navigation() -> None:
    paths = list(ROOT.rglob("index.html")) + [ROOT / "404.html"]
    for path in paths:
        if not path.exists():
            continue
        route = route_for_path(path)
        text = path.read_text(encoding="utf-8")
        text = re.sub(
            r'<div class="edition-bar">.*?</div>\s*<header class="site-header".*?</header>',
            EDITION_BAR + site_header(route),
            text,
            count=1,
            flags=re.S,
        )
        text = re.sub(
            r'<footer class="site-footer">.*?</footer>',
            site_footer(),
            text,
            count=1,
            flags=re.S,
        )
        path.write_text(text, encoding="utf-8", newline="\n")


def main() -> None:
    refresh_articles()
    refresh_departments()
    refresh_homepage()
    refresh_journal()
    refresh_metadata()
    refresh_newsletter_language()
    refresh_image_markup()
    refresh_navigation()
    print(f"Refreshed {len(ARTICLES)} articles, four departments and the Journal.")


if __name__ == "__main__":
    main()
