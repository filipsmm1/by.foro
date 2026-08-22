"""Refresh repeated by.foro catalogue, article, SEO and image markup.

The editorial catalogue in content/articles.json is the source of truth for
related stories and department indexes. Run this after adding or editing a post:

    python tools/refresh_site.py
"""

from __future__ import annotations

import html
import json
import re
from datetime import datetime, timedelta, timezone
from email.utils import format_datetime
from pathlib import Path
from urllib.parse import quote


ROOT = Path(__file__).resolve().parents[1]
ASSET_VERSION = "20260822c"
ARTICLES = json.loads((ROOT / "content" / "articles.json").read_text(encoding="utf-8"))
BY_URL = {article["url"]: article for article in ARTICLES}

RELATED = {
    "/blogs/home/dorm-desk-hutch-ideas/": [
        "/blogs/home/how-to-keep-your-space-clean/",
        "/blogs/home/small-entryway-that-looks-expensive/",
        "/blogs/home/lived-in-interior-design-2026/",
    ],
    "/blogs/beauty/dragonfly-nails/": [
        "/blogs/beauty/vamp-romantic-beauty-guide/",
        "/blogs/beauty/the-vanity-table-as-still-life/",
        "/blogs/fashion/bug-jewellery-trend/",
    ],
    "/blogs/fashion/khaki-coded-style/": [
        "/blogs/fashion/fall-2026-fashion-trends-worth-wearing/",
        "/blogs/fashion/dressing-with-intention/",
        "/blogs/fashion/how-to-wear-colour-again/",
    ],
    "/blogs/fashion/bug-jewellery-trend/": [
        "/blogs/fashion/how-to-wear-brooches/",
        "/blogs/fashion/how-to-wear-a-bib-necklace/",
        "/blogs/beauty/dragonfly-nails/",
    ],
    "/blogs/fashion/how-to-wear-a-bib-necklace/": [
        "/blogs/fashion/how-to-wear-brooches/",
        "/blogs/fashion/mahjong-necklace-meaning/",
        "/blogs/fashion/glamoratti-style-2026/",
    ],
    "/blogs/culture/pen-pal-letter-ideas-for-adults/": [
        "/blogs/culture/how-taste-is-built/",
        "/blogs/culture/how-to-create-an-analogue-listening-room/",
        "/blogs/fashion/literary-chic-without-the-costume/",
    ],
    "/blogs/home/circus-interior-design/": [
        "/blogs/home/whimsical-interiors-without-the-theme/",
        "/blogs/home/quietly-dramatic-home-decor/",
        "/blogs/culture/art-deco-revival/",
    ],
    "/blogs/beauty/niche-perfume-collection/": [
        "/blogs/beauty/perfume-wardrobe-by-mood/",
        "/blogs/beauty/skin-scent-perfume-guide/",
        "/blogs/beauty/matcha-perfume-guide/",
    ],
    "/blogs/home/red-marble-bathroom-ideas/": [
        "/blogs/home/bathroom-that-feels-like-a-hotel/",
        "/blogs/culture/art-deco-revival/",
        "/blogs/home/how-to-make-a-home-look-expensive/",
    ],
    "/blogs/beauty/matcha-perfume-guide/": [
        "/blogs/beauty/skin-scent-perfume-guide/",
        "/blogs/beauty/perfume-wardrobe-by-mood/",
        "/blogs/beauty/the-vanity-table-as-still-life/",
    ],
    "/blogs/fashion/how-to-wear-peplum-tops/": [
        "/blogs/fashion/dressing-with-intention/",
        "/blogs/fashion/glamoratti-style-2026/",
        "/blogs/fashion/romantic-fashion-trend-2027/",
    ],
    "/blogs/beauty/ceramide-ampoule-guide/": [
        "/blogs/beauty/the-vanity-table-as-still-life/",
        "/blogs/beauty/skin-scent-perfume-guide/",
        "/blogs/beauty/perfume-wardrobe-by-mood/",
    ],
    "/blogs/fashion/jelly-kitten-heels/": [
        "/blogs/fashion/summer-loafers-outfit-guide/",
        "/blogs/fashion/european-summer-style-2026/",
        "/blogs/fashion/how-to-wear-a-scarf-belt/",
    ],
    "/blogs/fashion/subtle-cat-eye-sunglasses/": [
        "/blogs/fashion/european-summer-style-2026/",
        "/blogs/fashion/celebrity-style-is-getting-personal/",
        "/blogs/fashion/glamoratti-style-2026/",
    ],
    "/blogs/fashion/how-to-wear-a-scarf-belt/": [
        "/blogs/fashion/european-summer-style-2026/",
        "/blogs/fashion/romantic-fashion-trend-2027/",
        "/blogs/fashion/how-to-wear-brooches/",
    ],
    "/blogs/beauty/birkin-bangs-guide/": [
        "/blogs/beauty/japanese-bob-vs-scandi-bob/",
        "/blogs/beauty/the-vanity-table-as-still-life/",
        "/blogs/fashion/celebrity-style-is-getting-personal/",
    ],
    "/blogs/fashion/mahjong-necklace-meaning/": [
        "/blogs/fashion/how-to-wear-brooches/",
        "/blogs/fashion/glamoratti-style-2026/",
        "/blogs/culture/art-deco-revival/",
    ],
    "/blogs/culture/phoebe-bridgers-lost-weekend-meaning/": [
        "/blogs/culture/how-taste-is-built/",
        "/blogs/fashion/celebrity-style-is-getting-personal/",
        "/blogs/culture/how-to-create-an-analogue-listening-room/",
    ],
    "/blogs/fashion/romantic-fashion-trend-2027/": [
        "/blogs/fashion/literary-chic-without-the-costume/",
        "/blogs/fashion/how-to-wear-brooches/",
        "/blogs/fashion/european-summer-style-2026/",
    ],
    "/blogs/culture/ariana-grande-petal-streams-rankings/": [
        "/blogs/culture/ariana-grande-petal-meaning/",
        "/blogs/fashion/celebrity-style-is-getting-personal/",
        "/blogs/culture/how-taste-is-built/",
    ],
    "/blogs/home/how-to-keep-your-space-clean/": [
        "/blogs/home/lived-in-interior-design-2026/",
        "/blogs/home/how-to-make-a-home-look-expensive/",
        "/blogs/home/small-entryway-that-looks-expensive/",
    ],
    "/blogs/fashion/how-to-wear-brooches/": [
        "/blogs/fashion/how-to-wear-a-bib-necklace/",
        "/blogs/fashion/mahjong-necklace-meaning/",
        "/blogs/fashion/glamoratti-style-2026/",
    ],
    "/blogs/culture/ariana-grande-petal-meaning/": [
        "/blogs/culture/ariana-grande-petal-streams-rankings/",
        "/blogs/fashion/celebrity-style-is-getting-personal/",
        "/blogs/culture/how-taste-is-built/",
    ],
    "/blogs/home/lived-in-interior-design-2026/": [
        "/blogs/home/how-to-keep-your-space-clean/",
        "/blogs/home/quietly-dramatic-home-decor/",
        "/blogs/home/coffee-table-styling-that-looks-collected/",
    ],
    "/blogs/fashion/european-summer-style-2026/": [
        "/blogs/fashion/how-to-wear-a-scarf-belt/",
        "/blogs/fashion/jelly-kitten-heels/",
        "/blogs/fashion/dressing-with-intention/",
    ],
    "/blogs/fashion/glamoratti-style-2026/": [
        "/blogs/fashion/how-to-wear-peplum-tops/",
        "/blogs/culture/art-deco-revival/",
        "/blogs/fashion/fall-2026-fashion-trends-worth-wearing/",
    ],
    "/blogs/beauty/japanese-bob-vs-scandi-bob/": [
        "/blogs/beauty/birkin-bangs-guide/",
        "/blogs/beauty/the-vanity-table-as-still-life/",
        "/blogs/fashion/dressing-with-intention/",
    ],
    "/blogs/culture/art-deco-revival/": [
        "/blogs/fashion/fall-2026-fashion-trends-worth-wearing/",
        "/blogs/home/quietly-dramatic-home-decor/",
        "/blogs/culture/how-taste-is-built/",
    ],
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
        "/blogs/fashion/romantic-fashion-trend-2027/",
        "/blogs/fashion/dressing-with-intention/",
        "/blogs/fashion/fall-2026-fashion-trends-worth-wearing/",
    ],
    "/blogs/fashion/dressing-with-intention/": [
        "/blogs/fashion/how-to-wear-peplum-tops/",
        "/blogs/fashion/literary-chic-without-the-costume/",
        "/blogs/fashion/fall-2026-fashion-trends-worth-wearing/",
    ],
    "/blogs/home/whimsical-interiors-without-the-theme/": [
        "/blogs/home/circus-interior-design/",
        "/blogs/home/quietly-dramatic-home-decor/",
        "/blogs/home/most-beautiful-kitchen-colour-combinations/",
    ],
    "/blogs/home/most-beautiful-kitchen-colour-combinations/": [
        "/blogs/home/how-to-make-a-home-look-expensive/",
        "/blogs/home/quietly-dramatic-home-decor/",
        "/blogs/home/whimsical-interiors-without-the-theme/",
    ],
    "/blogs/beauty/skin-scent-perfume-guide/": [
        "/blogs/beauty/matcha-perfume-guide/",
        "/blogs/beauty/perfume-wardrobe-by-mood/",
        "/blogs/beauty/the-vanity-table-as-still-life/",
    ],
    "/blogs/beauty/the-vanity-table-as-still-life/": [
        "/blogs/beauty/ceramide-ampoule-guide/",
        "/blogs/beauty/perfume-wardrobe-by-mood/",
        "/blogs/beauty/skin-scent-perfume-guide/",
    ],
    "/blogs/culture/how-to-create-an-analogue-listening-room/": [
        "/blogs/culture/how-taste-is-built/",
        "/blogs/home/coffee-table-styling-that-looks-collected/",
        "/blogs/home/whimsical-interiors-without-the-theme/",
    ],
    "/blogs/culture/how-taste-is-built/": [
        "/blogs/culture/pen-pal-letter-ideas-for-adults/",
        "/blogs/culture/phoebe-bridgers-lost-weekend-meaning/",
        "/blogs/culture/how-to-create-an-analogue-listening-room/",
    ],
    "/blogs/home/how-to-make-a-home-look-expensive/": [
        "/blogs/home/reading-nook-ideas/",
        "/blogs/home/coffee-table-styling-that-looks-collected/",
        "/blogs/home/small-entryway-that-looks-expensive/",
    ],
    "/blogs/home/warm-minimalist-bedroom/": [
        "/blogs/home/how-to-make-a-home-look-expensive/",
        "/blogs/home/reading-nook-ideas/",
        "/blogs/home/bathroom-that-feels-like-a-hotel/",
    ],
    "/blogs/home/bathroom-that-feels-like-a-hotel/": [
        "/blogs/home/red-marble-bathroom-ideas/",
        "/blogs/home/how-to-make-a-home-look-expensive/",
        "/blogs/home/warm-minimalist-bedroom/",
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
        "/blogs/fashion/jelly-kitten-heels/",
        "/blogs/fashion/dressing-with-intention/",
        "/blogs/fashion/how-to-wear-colour-again/",
    ],
    "/blogs/fashion/celebrity-style-is-getting-personal/": [
        "/blogs/fashion/subtle-cat-eye-sunglasses/",
        "/blogs/culture/phoebe-bridgers-lost-weekend-meaning/",
        "/blogs/culture/ariana-grande-petal-meaning/",
    ],
    "/blogs/beauty/perfume-wardrobe-by-mood/": [
        "/blogs/beauty/niche-perfume-collection/",
        "/blogs/beauty/matcha-perfume-guide/",
        "/blogs/beauty/skin-scent-perfume-guide/",
    ],
    "/blogs/culture/the-last-house-ending-explained/": [
        "/blogs/culture/how-taste-is-built/",
        "/blogs/home/lived-in-interior-design-2026/",
        "/blogs/culture/how-to-create-an-analogue-listening-room/",
    ],
    "/blogs/culture/sam-smith-hazel-eyes-meaning/": [
        "/blogs/culture/ariana-grande-petal-meaning/",
        "/blogs/culture/phoebe-bridgers-lost-weekend-meaning/",
        "/blogs/culture/how-taste-is-built/",
    ],
    "/blogs/fashion/jennifer-lopez-green-versace-dress/": [
        "/blogs/fashion/celebrity-style-is-getting-personal/",
        "/blogs/fashion/glamoratti-style-2026/",
        "/blogs/culture/art-deco-revival/",
    ],
    "/blogs/home/elegant-summerween-decor/": [
        "/blogs/home/whimsical-interiors-without-the-theme/",
        "/blogs/home/quietly-dramatic-home-decor/",
        "/blogs/culture/how-to-serve-chilled-red-wine/",
    ],
    "/blogs/culture/how-to-serve-chilled-red-wine/": [
        "/blogs/home/elegant-summerween-decor/",
        "/blogs/home/outdoor-space-that-feels-expensive/",
        "/blogs/home/coffee-table-styling-that-looks-collected/",
    ],
}

TOPIC_LABELS = {
    "trends": "Trends",
    "accessories": "Accessories",
    "jewellery": "Jewellery",
    "personal-style": "Personal style",
    "summer-style": "Summer style",
    "luxury-decor": "Luxury decor",
    "lived-in-interiors": "Lived-in interiors",
    "reading-nooks": "Reading nooks",
    "kitchens": "Kitchens",
    "bedrooms": "Bedrooms",
    "bathrooms": "Bathrooms",
    "entryways": "Entryways",
    "outdoor-living": "Outdoor living",
    "living-rooms": "Living rooms",
    "cleaning": "Cleaning",
    "dorm-rooms": "Dorm rooms",
    "fragrance": "Fragrance",
    "beauty-routines": "Beauty routines",
    "beauty-objects": "Beauty objects",
    "hair": "Hair",
    "skincare": "Skincare",
    "nails": "Nails",
    "music": "Music",
    "film": "Film",
    "essays": "Essays",
    "design": "Design",
    "celebrity-style": "Celebrity style",
    "hosting": "Hosting",
    "seasonal": "Seasonal",
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

EDITION_BAR = ""

PRIMARY_NAV = (
    ("Journal", "/journal/"),
    ("Home", "/home/"),
    ("Fashion", "/fashion/"),
    ("Beauty", "/beauty/"),
    ("Culture", "/culture/"),
)

NAV_DRAWER = """<div class="nav-drawer" id="explore-menu" aria-label="Explore by.foro" aria-hidden="true">
  <div class="nav-drawer__intro"><p class="kicker">Explore by.foro</p><p>Find a useful guide, a beautiful idea or the next story worth keeping.</p><a class="nav-search-link" href="/journal/#journal-library-title">Search all stories <span aria-hidden="true">&rarr;</span></a></div>
  <div class="nav-drawer__group"><span>Begin</span><a href="/start-here/">Start here</a><a href="/the-edit/">The current edit</a><a href="/journal/">Complete Journal</a></div>
  <div class="nav-drawer__group"><span>Departments</span><a href="/home/">Home</a><a href="/fashion/">Fashion</a><a href="/beauty/">Beauty</a><a href="/culture/">Culture</a></div>
  <div class="nav-drawer__group"><span>Popular paths</span><a href="/journal/?department=home&amp;topic=reading-nooks">Reading nooks</a><a href="/journal/?department=beauty&amp;topic=fragrance">Fragrance</a><a href="/journal/?department=fashion&amp;topic=personal-style">Personal style</a><a href="/journal/?department=fashion&amp;topic=celebrity-style">Celebrity style</a></div>
  <div class="nav-drawer__group"><span>About</span><a href="/about/">About by.foro</a><a href="/editorial-policy/">How we work</a><a href="/studio/">FORO Studio</a><a href="/contact/">Contact</a></div>
</div>"""

CONTENT_EXPANSIONS = {
    "/blogs/fashion/dressing-with-intention/": {
        "toc": "<li><a href=\"#section-5\">Inventory before aspiration</a></li><li><a href=\"#section-6\">A rule for the next purchase</a></li>",
        "sections": """<section data-reveal id="section-5"><h2>Inventory before aspiration</h2><p>Before making a wish list, make a record of what is actually worn. For two ordinary weeks, note the pieces that leave the wardrobe, the combinations that survive a long day and the moments when an outfit creates friction. The useful information is rarely glamorous: a coat has the wrong pocket, a trouser only works with one shoe, a knit is too warm for every room in which it is worn.</p><p>This turns vague dissatisfaction into a practical brief. It may reveal that the wardrobe does not need more personality; it needs a better layer between shirt and coat, or one trouser length that works with the shoes already owned. It also shows which repeated shapes have earned their place. Those repetitions are not gaps to fill. They are the beginning of a signature.</p><p>A reference can still help, provided it is translated rather than copied. Our approach to <a href="/blogs/fashion/literary-chic-without-the-costume/">literary chic</a>, for example, begins with texture, proportion and restraint rather than a shopping list of bookish symbols.</p></section><section data-reveal id="section-6"><h2>A rule for the next purchase</h2><p>A useful new piece should enter at least three convincing outfits using clothes that already exist. This is a stricter test than asking whether the object is beautiful on its own. It considers the wardrobe as a system and exposes purchases that depend on buying several more things before they make sense. Before buying another garment, try <a href="/blogs/fashion/how-to-wear-brooches/">one well-placed brooch</a> on three pieces you already own; a small accessory can answer the need for change more intelligently.</p><p>Time is another useful filter. Save the image, write down the exact function and wait long enough for the first intensity to fade. If the need remains, compare material, construction and maintenance rather than searching for a cheaper approximation of the original feeling. The point is not to remove pleasure from buying clothes. It is to make the pleasure last beyond the parcel.</p><p>Trends can still sharpen an existing wardrobe. The distinction is whether they answer a real interest. Our <a href="/blogs/fashion/fall-2026-fashion-trends-worth-wearing/">Fall 2026 edit</a> keeps only the runway ideas with enough structure to survive ordinary life.</p></section>""",
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


def styled_title(value: str) -> str:
    """Give long editorial titles a clear lead and secondary line."""
    title = str(value)
    if ":" not in title:
        return esc(title)
    lead, secondary = title.split(":", 1)
    return (
        f'{esc(lead)}:<span class="title-secondary"> '
        f'{esc(secondary.strip())}</span>'
    )


def image_shape_class(article: dict) -> str:
    return " story-image--square" if article.get("imageShape") == "square" else ""


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
        'aria-label="by.foro homepage">by.foro</a>'
        f'<nav class="site-nav" id="site-nav" aria-label="Main navigation">{links}</nav>'
        '<div class="header-actions"><a class="header-search" href="/journal/#journal-library-title">Search</a>'
        '<button class="menu-toggle" type="button" aria-controls="explore-menu" aria-expanded="false">'
        '<span>Explore</span><i aria-hidden="true"></i></button></div>'
        f'{NAV_DRAWER}</header>'
    )


def site_footer() -> str:
    return """<footer class="site-footer"><div class="footer-top"><div class="footer-lead"><p class="kicker">Independent visual journal</p><a class="footer-wordmark" href="/">by.foro</a><p>Fashion, interiors, beauty and culture, edited for character and staying power.</p></div><div class="footer-invitation"><p class="kicker">Keep exploring</p><h2>Find something worth your time.</h2><a class="button button--light" href="/journal/#journal-library-title">Search the Journal</a></div></div><div class="footer-grid"><div><h2>Begin</h2><a href="/start-here/">Start here</a><a href="/the-edit/">The Edit</a><a href="/journal/">All stories</a></div><div><h2>Departments</h2><a href="/home/">Home</a><a href="/fashion/">Fashion</a><a href="/beauty/">Beauty</a><a href="/culture/">Culture</a></div><div><h2>About</h2><a href="/about/">About by.foro</a><a href="/studio/">FORO Studio</a><a href="/contact/">Contact</a><a href="/editorial-policy/">How we work</a></div><div><h2>Information</h2><a href="/accessibility/">Accessibility</a><a href="/privacy/">Privacy</a><a href="/cookies/">Cookie settings</a><a href="/terms/">Terms</a></div></div><div class="footer-bottom"><p>&copy; <span data-year>2026</span> by.foro</p><p>Curated by people, not an algorithm.</p></div></footer>"""


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
        f'<figure class="media story-image{image_shape_class(article)}"><picture><source type="image/webp" '
        f'srcset="{esc(webp_srcset(article))}" sizes="(max-width: 760px) 90vw, 31vw">'
        f'<img alt="{esc(image["alt"])}" decoding="async" height="{image["height"]}" '
        f'loading="lazy" src="{esc(image["fallback"])}" width="{image["width"]}"></picture></figure>'
        f'<div class="story-copy"><p class="kicker">{esc(department)} &middot; {esc(topic)}</p>'
        f'<h3>{styled_title(article["title"])}</h3><p>{esc(article["excerpt"])}</p>'
        f'<span class="read-link">Read story <span aria-hidden="true">&nearr;</span></span></div></a></article>'
    )


def display_date(value: str) -> str:
    year, month, day = value.split("-")
    return f"{int(day)} {MONTHS[int(month) - 1]} {year}"


JSON_LD_BLOCK = re.compile(
    r'(<script\b(?=[^>]*\btype="application/ld\+json")[^>]*>)(.*?)(</script>)',
    re.S,
)


def upsert_json_ld(text: str, schema_type: str, payload: dict, element_id: str) -> str:
    found = False

    def replace(match: re.Match[str]) -> str:
        nonlocal found
        try:
            current = json.loads(match.group(2))
        except json.JSONDecodeError:
            return match.group(0)
        if current.get("@type") != schema_type:
            return match.group(0)
        if found:
            return ""
        found = True
        return (
            f'<script id="{element_id}" type="application/ld+json">'
            + json.dumps(payload, ensure_ascii=False, separators=(",", ":"))
            + "</script>"
        )

    text = JSON_LD_BLOCK.sub(replace, text)
    if not found:
        block = (
            f'<script id="{element_id}" type="application/ld+json">'
            + json.dumps(payload, ensure_ascii=False, separators=(",", ":"))
            + "</script>"
        )
        text = text.replace("</head>", f"{block}</head>", 1)
    return text


def json_ld_payload(text: str, schema_type: str) -> dict | None:
    for match in JSON_LD_BLOCK.finditer(text):
        try:
            payload = json.loads(match.group(2))
        except json.JSONDecodeError:
            continue
        if payload.get("@type") == schema_type:
            return payload
    return None


def replace_meta_content(text: str, attribute: str, value: str, content: str) -> str:
    pattern = re.compile(
        rf'<meta\b(?=[^>]*\b{re.escape(attribute)}="{re.escape(value)}")[^>]*>'
    )
    replacement = f'<meta {attribute}="{esc(value)}" content="{esc(content)}">'
    return pattern.sub(replacement, text, count=1)


def sync_article_search_markup(text: str, article: dict) -> str:
    schema_type = article.get("schemaType", "BlogPosting")
    article_schema = json_ld_payload(text, schema_type)
    if article_schema is None:
        raise RuntimeError(f'Missing {schema_type} schema for {article["url"]}')

    description = article.get("metaDescription", article["excerpt"])
    published_datetime = article_schema.get(
        "datePublished",
        f'{article["published"]}T12:00:00+02:00',
    )
    modified_datetime = (
        f'{article["updated"]}T12:00:00+02:00'
        if article.get("updated")
        else published_datetime
    )
    page_url = f'https://byforo.com{article["url"]}'
    image_url = f'https://byforo.com{article["image"]["fallback"]}'

    text = re.sub(
        r'<h1>.*?</h1>',
        f'<h1 class="title-split">{styled_title(article["title"])}</h1>'
        if ":" in article["title"]
        else f'<h1>{styled_title(article["title"])}</h1>',
        text,
        count=1,
        flags=re.S,
    )
    text = text.replace(" article-hero-image--square", "")
    if article.get("imageShape") == "square":
        text = text.replace(
            'class="media article-hero-image"',
            'class="media article-hero-image article-hero-image--square"',
            1,
        )

    hero_pattern = re.compile(
        r'<figure\b(?=[^>]*class="[^"]*\barticle-hero-image\b[^"]*")[^>]*>.*?</figure>',
        re.S,
    )
    hero_match = hero_pattern.search(text)
    if hero_match:
        hero = hero_match.group(0)
        hero = re.sub(
            r'(<source\b[^>]*\bsrcset=")[^"]+("[^>]*>)',
            rf'\g<1>{esc(webp_srcset(article))}\g<2>',
            hero,
            count=1,
        )
        hero = re.sub(
            r'(<img\b[^>]*\bwidth=")\d+("[^>]*>)',
            rf'\g<1>{article["image"]["width"]}\g<2>',
            hero,
            count=1,
        )
        hero = re.sub(
            r'(<img\b[^>]*\bheight=")\d+("[^>]*>)',
            rf'\g<1>{article["image"]["height"]}\g<2>',
            hero,
            count=1,
        )
        text = text[: hero_match.start()] + hero + text[hero_match.end() :]

    if article.get("imageShape") == "square":
        text = replace_meta_content(
            text, "property", "og:image:width", str(article["image"]["width"])
        )
        text = replace_meta_content(
            text, "property", "og:image:height", str(article["image"]["height"])
        )

    article_schema.update(
        {
            "mainEntityOfPage": {"@type": "WebPage", "@id": page_url},
            "headline": article["title"],
            "description": description,
            "image": [image_url],
            "datePublished": published_datetime,
            "dateModified": modified_datetime,
            "author": {
                "@type": "Organization",
                "name": "by.foro Editorial",
                "url": "https://byforo.com/about/",
            },
            "publisher": {
                "@type": "Organization",
                "name": "by.foro",
                "url": "https://byforo.com/",
            },
            "articleSection": article.get(
                "articleSection", article["department"].title()
            ),
            "inLanguage": "en-GB",
        }
    )
    text = upsert_json_ld(text, schema_type, article_schema, "article-schema")

    breadcrumb_items = [
        {
            "@type": "ListItem",
            "position": 1,
            "name": "Home" if article.get("breadcrumbTopic") else "by.foro",
            "item": "https://byforo.com/",
        }
    ]
    if article["department"] != "home":
        breadcrumb_items.append({
            "@type": "ListItem",
            "position": len(breadcrumb_items) + 1,
            "name": article["department"].title(),
            "item": f'https://byforo.com/{article["department"]}/',
        })
    if article.get("breadcrumbTopic") or article["department"] == "home":
        breadcrumb_items.append(
            {
                "@type": "ListItem",
                "position": len(breadcrumb_items) + 1,
                "name": TOPIC_LABELS[article["topic"]],
                "item": (
                    "https://byforo.com/journal/?department="
                    f'{article["department"]}&topic={article["topic"]}'
                ),
            }
        )
    breadcrumb_items.append(
        {
            "@type": "ListItem",
            "position": len(breadcrumb_items) + 1,
            "name": article["title"],
            "item": page_url,
        }
    )
    breadcrumb = {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": breadcrumb_items,
    }
    text = upsert_json_ld(
        text,
        "BreadcrumbList",
        breadcrumb,
        "article-breadcrumb-schema",
    )
    text = replace_meta_content(
        text,
        "property",
        "article:modified_time",
        modified_datetime,
    )

    date_value = article.get("updated", article["published"])
    date_label = (
        f'Updated {display_date(date_value)}'
        if article.get("updated")
        else display_date(date_value)
    )
    article_meta = (
        '<div class="article-meta">'
        '<a class="article-byline" href="/about/" rel="author">by.foro Editorial</a>'
        f'<time datetime="{esc(date_value)}">{esc(date_label)}</time>'
        f'<span>{article["readingMinutes"]} min read</span></div>'
    )
    text = re.sub(
        r'<div class="article-meta">.*?</div>',
        article_meta,
        text,
        count=1,
        flags=re.S,
    )
    if article.get("breadcrumbTopic") or article["department"] == "home":
        department_crumb = (
            f'<a href="/{esc(article["department"])}/">'
            f'{esc(article["department"].title())}</a><span>/</span>'
            if article["department"] != "home"
            else ""
        )
        breadcrumb_nav = (
            '<nav class="breadcrumbs" aria-label="Breadcrumb">'
            '<a href="/">Home</a><span>/</span>'
            f'{department_crumb}'
            f'<a href="/journal/?department={esc(article["department"])}&amp;topic={esc(article["topic"])}">'
            f'{esc(TOPIC_LABELS[article["topic"]])}</a><span>/</span>'
            f'<span aria-current="page">{esc(article["title"])}</span>'
            "</nav>"
        )
    else:
        breadcrumb_nav = (
            '<nav class="breadcrumbs" aria-label="Breadcrumb">'
            '<a href="/">by.foro</a><span>/</span>'
            f'<a href="/{esc(article["department"])}/">'
            f'{esc(article["department"].title())}</a><span>/</span>'
            f'<span aria-current="page">{esc(TOPIC_LABELS[article["topic"]])}</span>'
            "</nav>"
        )
    text = re.sub(
        r'<nav\b(?=[^>]*class="breadcrumbs")[^>]*>.*?</nav>',
        breadcrumb_nav,
        text,
        count=1,
        flags=re.S,
    )
    return text


def feature_story(article: dict) -> str:
    department = article["department"].title()
    topic = TOPIC_LABELS[article["topic"]]
    image = article["image"]
    square = article.get("imageShape") == "square"
    section_class = "feature-story feature-story--square" if square else "feature-story"
    image_class = "feature-story__image feature-story__image--square" if square else "feature-story__image"
    return (
        f'<section class="{section_class}" data-reveal="">'
        f'<figure class="media {image_class}" data-zoom-media="">'
        f'<picture><source type="image/webp" srcset="{esc(webp_srcset(article))}" '
        'sizes="(max-width: 760px) 90vw, 55vw">'
        f'<img alt="{esc(image["alt"])}" decoding="async" height="{image["height"]}" loading="lazy" '
        f'src="{esc(image["fallback"])}" width="{image["width"]}"></picture></figure>'
        f'<div><p class="kicker">Latest &middot; {esc(department)} &middot; {esc(topic)}</p>'
        f'<h2 class="title-split">{styled_title(article["title"])}</h2><p>{esc(article["excerpt"])}</p>'
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
        f'<figure class="media story-image{image_shape_class(article)}"{zoom}><picture><source type="image/webp" '
        f'srcset="{esc(webp_srcset(article))}" sizes="(max-width: 760px) 90vw, (max-width: 1080px) 45vw, 31vw">'
        f'<img alt="{esc(image["alt"])}" decoding="async" height="{image["height"]}" loading="lazy" '
        f'src="{esc(image["fallback"])}" width="{image["width"]}"></picture></figure>'
        f'<div class="story-copy"><p class="kicker">{esc(department)} &middot; {esc(topic)}</p>'
        f'<h3>{styled_title(article["title"])}</h3><p>{esc(article["excerpt"])}</p>'
        '<span class="read-link">Read story <span aria-hidden="true">&nearr;</span></span></div></a></article>'
    )


def homepage_story_grid() -> str:
    cards = "".join(homepage_card(article, index) for index, article in enumerate(ARTICLES[:4]))
    return f'<section class="story-grid story-grid--editorial">{cards}</section>'


def homepage_entry_panel() -> str:
    return """<!-- HOMEPAGE-ENTRY:START -->
<section class="home-paths" aria-labelledby="home-paths-title" data-reveal>
  <div class="home-paths__intro"><p class="kicker">Browse by interest</p><h2 id="home-paths-title">Four worlds, one point of view.</h2><p>Go straight to the department you need, or search the complete Journal by topic.</p><a class="text-link" href="/journal/#journal-library-title">Search all stories</a></div>
  <div class="home-paths__grid">
    <a href="/home/"><span>01</span><strong>Home</strong><small>Rooms, objects and atmosphere</small></a>
    <a href="/fashion/"><span>02</span><strong>Fashion</strong><small>Personal style and considered trends</small></a>
    <a href="/beauty/"><span>03</span><strong>Beauty</strong><small>Fragrance, ritual and detail</small></a>
    <a href="/culture/"><span>04</span><strong>Culture</strong><small>Music, film and contemporary life</small></a>
  </div>
</section>
<!-- HOMEPAGE-ENTRY:END -->"""


def homepage_collections() -> str:
    return """<!-- HOMEPAGE-COLLECTIONS:START -->
<section class="collection-strip" aria-labelledby="homepage-collections-title" data-reveal>
  <div><p class="kicker">Collections</p><h2 id="homepage-collections-title">Curated routes through the archive.</h2></div>
  <div class="collection-strip__grid">
    <a href="/journal/?department=home&amp;q=expensive"><span>01</span><strong>The Expensive-Looking Home</strong><p>Stone, lighting, vintage pieces and rooms with weight.</p></a>
    <a href="/blogs/home/reading-nook-ideas/"><span>02</span><strong>The Reading Room</strong><p>Small private corners, shelves and places to pause.</p></a>
    <a href="/journal/?department=fashion"><span>03</span><strong>Wardrobe With Intention</strong><p>Trends, proportion and dressing without urgency.</p></a>
    <a href="/journal/?department=beauty"><span>04</span><strong>Beauty Objects</strong><p>Fragrance, vanity tables and daily ritual.</p></a>
  </div>
</section>
<!-- HOMEPAGE-COLLECTIONS:END -->"""


def homepage_picture(article: dict, sizes: str, *, eager: bool = False) -> str:
    image = article["image"]
    loading = "eager" if eager else "lazy"
    priority = ' fetchpriority="high"' if eager else ""
    return (
        f'<picture><source type="image/webp" srcset="{esc(webp_srcset(article))}" sizes="{esc(sizes)}">'
        f'<img alt="{esc(image["alt"])}" decoding="async" height="{image["height"]}" '
        f'loading="{loading}"{priority} src="{esc(image["fallback"])}" width="{image["width"]}"></picture>'
    )


def homepage_front_rail_card(article: dict, index: int) -> str:
    department = article["department"].title()
    topic = TOPIC_LABELS[article["topic"]]
    return (
        f'<article class="front-rail-card"><a href="{esc(article["url"])}">'
        f'<span class="front-rail-card__number">0{index}</span>'
        f'<div><p class="kicker">{esc(department)} &middot; {esc(topic)}</p>'
        f'<h3>{styled_title(article["title"])}</h3>'
        f'<p>{esc(article["excerpt"])}</p></div>'
        f'<figure class="media">{homepage_picture(article, "110px")}</figure>'
        '</a></article>'
    )


def homepage_latest_card(article: dict, index: int) -> str:
    department = article["department"].title()
    topic = TOPIC_LABELS[article["topic"]]
    return (
        f'<article class="front-card front-card--{index + 1}"><a href="{esc(article["url"])}">'
        f'<figure class="media">{homepage_picture(article, "(max-width: 760px) 92vw, 31vw")}</figure>'
        f'<div><p class="kicker">{esc(department)} &middot; {esc(topic)}</p>'
        f'<h3>{styled_title(article["title"])}</h3><p>{esc(article["excerpt"])}</p>'
        f'<span>{article["readingMinutes"]} min read</span></div></a></article>'
    )


def homepage_department_panel(department: str, number: int) -> str:
    articles = [article for article in ARTICLES if article["department"] == department][1:4]
    links = "".join(
        f'<li><a href="{esc(article["url"])}"><span>{TOPIC_LABELS[article["topic"]]}</span>'
        f'<strong>{styled_title(article["title"])}</strong><i aria-hidden="true">&rarr;</i></a></li>'
        for article in articles
    )
    return (
        f'<section class="front-department"><header><span>0{number}</span><h3>{department.title()}</h3>'
        f'<a href="/{department}/">Open department</a></header><ol>{links}</ol></section>'
    )


def homepage_main() -> str:
    lead = ARTICLES[0]
    lead_department = lead["department"].title()
    lead_topic = TOPIC_LABELS[lead["topic"]]
    rail_articles = [ARTICLES[index] for index in (1, 2, 3, 7)]
    rail = "".join(
        homepage_front_rail_card(article, index)
        for index, article in enumerate(rail_articles, start=1)
    )
    latest = "".join(
        homepage_latest_card(article, index)
        for index, article in enumerate(ARTICLES[8:14])
    )
    departments = "".join(
        homepage_department_panel(department, index)
        for index, department in enumerate(("home", "fashion", "beauty", "culture"), start=1)
    )
    return f'''<main class="front-page" id="main">
<section class="front-opening" aria-labelledby="front-opening-title">
  <div><p class="kicker">The by.foro front page &middot; Updated 22 August</p><h1 id="front-opening-title">The stories worth opening today.</h1></div>
  <p>Fashion, rooms, beauty and culture, edited for people who want a useful point of view, not more noise.</p>
</section>
<nav class="front-channels" aria-label="Browse the Journal"><span>Go straight to</span><a href="/journal/">All stories</a><a href="/home/">Home</a><a href="/fashion/">Fashion</a><a href="/beauty/">Beauty</a><a href="/culture/">Culture</a><a href="/journal/#journal-library-title">Search</a></nav>
<section class="front-desk" aria-label="Today’s lead stories">
  <article class="front-lead"><a href="{esc(lead["url"])}"><figure class="media">{homepage_picture(lead, "(max-width: 760px) 94vw, 64vw", eager=True)}</figure><div class="front-lead__copy"><p class="kicker">Lead story &middot; {esc(lead_department)} &middot; {esc(lead_topic)}</p><h2>{styled_title(lead["title"])}</h2><p>{esc(lead["excerpt"])}</p><span class="front-read">Read the story &middot; {lead["readingMinutes"]} min <i aria-hidden="true">&rarr;</i></span></div></a></article>
  <aside class="front-rail"><header><div><p class="kicker">New in the Journal</p><h2>Choose your next read.</h2></div><a href="/journal/">View all {len(ARTICLES)}</a></header>{rail}</aside>
</section>
<section class="front-find" aria-labelledby="front-find-title"><div><p class="kicker">Choose by mood</p><h2 id="front-find-title">What are you here for?</h2></div><nav><a href="/journal/?department=home&amp;q=expensive">Make a room feel expensive</a><a href="/journal/?department=fashion&amp;q=personal%20style">Dress with more intention</a><a href="/journal/?department=beauty&amp;q=perfume">Find a new fragrance</a><a href="/journal/?department=culture">Read the culture desk</a><a href="/start-here/">Show me where to begin</a></nav></section>
<section class="front-latest" aria-labelledby="front-latest-title"><header><div><p class="kicker">Recently published</p><h2 id="front-latest-title">More from the desk.</h2></div><p>Six new reads, arranged for fast scanning. Pick the idea that earns your attention.</p></header><div class="front-card-grid">{latest}</div><a class="front-all-link" href="/journal/">Browse all {len(ARTICLES)} stories <span aria-hidden="true">&rarr;</span></a></section>
<section class="front-departments" aria-labelledby="front-departments-title"><header><p class="kicker">Explore by department</p><h2 id="front-departments-title">A clearer way into the archive.</h2></header><div>{departments}</div></section>
<section class="front-edit" aria-labelledby="front-edit-title"><div><p class="kicker">The current edit</p><h2 id="front-edit-title">Three routes with somewhere to go.</h2><p>No endless mood-board scrolling. Each edit gathers stories around a useful idea.</p></div><nav><a href="/journal/?department=home&amp;q=expensive"><span>01 &middot; Home</span><strong>The Expensive-Looking Home</strong><i>Lighting, stone, scale and rooms with weight.</i></a><a href="/blogs/home/reading-nook-ideas/"><span>02 &middot; Home</span><strong>The Reading Room</strong><i>Private corners, shelves and places to pause.</i></a><a href="/journal/?department=fashion"><span>03 &middot; Fashion</span><strong>Wardrobe With Intention</strong><i>Proportion, detail and dressing without urgency.</i></a></nav></section>
<section class="newsletter front-letter"><div><p class="kicker">The FORO Letter</p><h2>One sharp edit. No daily noise.</h2></div><div><p>Fashion, rooms, beauty, objects and culture, sent only when there is something worth keeping.</p><form action="https://formsubmit.co/hello@byforo.com" class="newsletter-form" data-ajax-form data-form-kind="newsletter" method="post"><input name="_subject" type="hidden" value="New by.foro newsletter request"><input name="_template" type="hidden" value="table"><input autocomplete="off" class="hp" name="_honey" tabindex="-1" type="text"><label for="newsletter-home">Email address</label><div class="field-line"><input autocomplete="email" id="newsletter-home" name="email" placeholder="you@example.com" required type="email"><button type="submit">Request invitation</button></div><label class="consent"><input name="consent" required type="checkbox" value="Yes"><span>I agree to receive The FORO Letter and understand I can unsubscribe at any time.</span></label><p aria-live="polite" class="form-status"></p></form></div></section>
</main>'''


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
        f'<figure class="media story-image{image_shape_class(article)}"><picture><source type="image/webp" srcset="{esc(webp_srcset(article))}" '
        'sizes="(max-width: 760px) 90vw, (max-width: 1080px) 45vw, 31vw">'
        f'<img alt="{esc(image["alt"])}" decoding="async" height="{image["height"]}" loading="lazy" '
        f'src="{esc(image["fallback"])}" width="{image["width"]}"></picture></figure>'
        f'<div class="story-copy"><p class="kicker">{esc(department.title())} &middot; {esc(TOPIC_LABELS[topic])}</p>'
        f'<h3>{styled_title(article["title"])}</h3><p>{esc(article["excerpt"])}</p>'
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
  <div class="journal-library__heading"><div><p class="kicker">The complete archive</p><h2 id="journal-library-title">What would you like to read?</h2></div><p class="journal-status" data-journal-status aria-live="polite">Showing all {len(ARTICLES)} stories</p></div>
  <div class="journal-search-row"><label class="journal-search" for="journal-search"><span>Search by idea, room, person or problem</span><input id="journal-search" type="search" inputmode="search" autocomplete="off" placeholder="Search the Journal" data-journal-search></label><label class="journal-sort" for="journal-sort"><span>Order</span><select id="journal-sort" data-journal-sort><option value="newest">Newest first</option><option value="longest">Long reads</option><option value="shortest">Quick reads</option><option value="az">A to Z</option></select></label><button class="journal-clear" type="button" data-journal-clear hidden>Clear</button></div>
  <div class="journal-quick-search" aria-label="Popular searches"><span>Popular now</span><div><button type="button" data-journal-query="reading nook">Reading nooks</button><button type="button" data-journal-query="kitchen colour">Kitchens</button><button type="button" data-journal-query="quiet luxury">Quiet luxury</button><button type="button" data-journal-query="perfume">Perfume</button><button type="button" data-journal-query="personal style">Personal style</button></div></div>
  {journal_department_filters()}
  <details class="journal-topic-disclosure"><summary>Browse all subcategories <span>Topics</span></summary>{journal_topic_filters()}</details>
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
    related = [BY_URL[url] for url in related_urls[:3]]
    linked_titles = [
        f'<a href="{esc(item["url"])}">{esc(item["title"])}</a>' for item in related
    ]
    links = (
        linked_titles[0]
        if len(linked_titles) == 1
        else ", ".join(linked_titles[:-1]) + f" and {linked_titles[-1]}"
    )
    block = (
        '<!-- FURTHER-READING:START --><aside class="article-further" aria-label="Further reading">'
        f'<p class="kicker">Further reading</p><p>Continue the idea with {links}.</p>'
        "</aside><!-- FURTHER-READING:END -->"
    )
    return re.sub(
        r'(<(?:div|footer) class="article-end">)',
        rf'{block}\g<1>',
        text,
        count=1,
    )


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


def polish_public_copy(text: str) -> str:
    """Keep internal production language out of published articles."""
    text = re.sub(
        r'<p>\s*For searchers comparing ideas quickly,.*?</p>',
        "",
        text,
        flags=re.S,
    )
    text = re.sub(
        r'<section class="summary-box seo-upgrade"[^>]*>.*?</section>',
        "",
        text,
        flags=re.S,
    )
    text = re.sub(
        r'<section id="(?:upgrade|detail)-how-to-use-this-guide"[^>]*>.*?</section>',
        "",
        text,
        flags=re.S,
    )
    text = re.sub(
        r'<section id="(?:upgrade|detail)-common-mistakes"[^>]*>.*?</section>',
        "",
        text,
        flags=re.S,
    )
    text = text.replace("<!-- SEO-UPGRADE:START -->", "<!-- EDITORIAL-EXPANSION:START -->")
    text = text.replace("<!-- SEO-UPGRADE:END -->", "<!-- EDITORIAL-EXPANSION:END -->")
    text = text.replace('id="upgrade-', 'id="detail-')
    text = text.replace("<h2>Suggested internal reading</h2>", "<h2>More from by.foro</h2>")
    text = text.replace("<h2>Sources and reading notes</h2>", "<h2>Further reading</h2>")
    text = re.sub(
        r"<p>(?:Factual and current trend references were checked against recent editorial sources before publication\.|These sources offer useful context and practical detail related to this story\.)</p>",
        "",
        text,
    )
    text = text.replace(
        '<section id="detail-search-intent-answered" data-reveal><h2>Search intent answered</h2>',
        '<section id="detail-style-in-one-sentence" data-reveal><h2>The style in one sentence</h2>',
    )
    return text


def update_word_count(text: str, article: dict) -> str:
    start = re.search(r'<(?:div|article) class="article-body">', text)
    if not start:
        return text
    ends = [
        position
        for marker in ("<!-- ARTICLE-AFTERWORD:START -->", "</main>")
        if (position := text.find(marker, start.end())) != -1
    ]
    if not ends:
        return text
    article_html = text[start.end() : min(ends)]
    visible = re.sub(r'<script.*?</script>|<style.*?</style>', ' ', article_html, flags=re.S)
    visible = html.unescape(re.sub(r'<[^>]+>', ' ', visible))
    count = len(re.findall(r"\b[\w’-]+\b", visible, flags=re.UNICODE))
    words_per_minute = article.get("readingWordsPerMinute", 180)
    minutes = max(5, (count + words_per_minute - 1) // words_per_minute)
    article["readingMinutes"] = minutes
    text = re.sub(r'("wordCount":\s*)\d+', rf'\g<1>{count}', text, count=1)
    text = re.sub(
        r'(<div class="article-meta">.*?<span>)\d+\s+min read(</span></div>)',
        rf"\g<1>{minutes} min read\g<2>",
        text,
        count=1,
        flags=re.S,
    )
    return text


def refresh_articles() -> None:
    for article in ARTICLES:
        path = article_path(article)
        text = path.read_text(encoding="utf-8")
        text = expand_article(text, article)
        text = polish_public_copy(text)
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
            text, replaced = re.subn(
                r'<section class="next-story">.*?</section>',
                modules,
                text,
                count=1,
                flags=re.S,
            )
            if not replaced:
                text = text.replace("</main>", f"</main>{modules}", 1)
        text = update_word_count(text, article)
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
    <div><span>By room</span><a href="/journal/?department=home&amp;topic=kitchens">Kitchen</a><a href="/journal/?department=home&amp;q=bedroom">Bedroom</a><a href="/journal/?department=home&amp;q=bathroom">Bathroom</a><a href="/journal/?department=home&amp;topic=living-rooms">Living room</a><a href="/blogs/home/reading-nook-ideas/">Reading nook guide</a><a href="/journal/?department=home&amp;q=exterior">Exterior</a></div>
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
        r'<main\b[^>]*id="main"[^>]*>.*?</main>',
        homepage_main(),
        text,
        count=1,
        flags=re.S,
    )
    text = re.sub(
        r'<body(?:\s+class="[^"]*")?>',
        '<body class="front-page-body">',
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
        text = re.sub(
            r'<script id="journal-collection-schema".*?</script>',
            lambda _: schema,
            text,
            count=1,
            flags=re.S,
        )
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
        if "/blogs/" in path.as_posix() and "/how-to-wear-brooches/" not in path.as_posix():
            text = re.sub(r"\s*<figcaption\b[^>]*>.*?</figcaption>", "", text, flags=re.S)
        path.write_text(text, encoding="utf-8", newline="\n")


def refresh_metadata() -> None:
    for article in ARTICLES:
        page = article_path(article)
        text = page.read_text(encoding="utf-8")
        description = article.get("metaDescription", article["excerpt"])
        seo_title = article.get("seoTitle", f'{article["title"]} | by.foro')
        escaped = esc(description)
        text = re.sub(
            r"<title>.*?</title>",
            f"<title>{esc(seo_title)}</title>",
            text,
            count=1,
            flags=re.S,
        )
        text = re.sub(
            r'<meta\b(?=[^>]*\bname="description")[^>]*>',
            f'<meta name="description" content="{escaped}">',
            text,
            count=1,
        )
        text = re.sub(
            r'<meta\b(?=[^>]*\bproperty="og:description")[^>]*>',
            f'<meta property="og:description" content="{escaped}">',
            text,
            count=1,
        )
        text = re.sub(
            r'<meta\b(?=[^>]*\bname="twitter:description")[^>]*>',
            f'<meta name="twitter:description" content="{escaped}">',
            text,
            count=1,
        )
        text = re.sub(
            r'<meta\b(?=[^>]*\bproperty="og:title")[^>]*>',
            f'<meta property="og:title" content="{esc(seo_title)}">',
            text,
            count=1,
        )
        text = re.sub(
            r'<meta\b(?=[^>]*\bname="twitter:title")[^>]*>',
            f'<meta name="twitter:title" content="{esc(seo_title)}">',
            text,
            count=1,
        )
        text = sync_article_search_markup(text, article)
        page.write_text(text, encoding="utf-8", newline="\n")

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
        chrome = EDITION_BAR + site_header(route)
        if '<div class="edition-bar">' in text:
            text = re.sub(
                r'<div class="edition-bar">.*?</div>\s*<header class="site-header".*?</header>',
                chrome,
                text,
                count=1,
                flags=re.S,
            )
        else:
            text = re.sub(
                r'<header class="site-header".*?</header>',
                chrome,
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
        text = re.sub(
            r'(?<=href=")/styles\.css(?:\?v=[^"&]+)?',
            f"/styles.css?v={ASSET_VERSION}",
            text,
        )
        text = re.sub(
            r'(?<=src=")/(script|journal/journal)\.js(?:\?v=[^"&]+)?',
            rf"/\1.js?v={ASSET_VERSION}",
            text,
        )
        path.write_text(text, encoding="utf-8", newline="\n")


def refresh_discovery_files() -> None:
    latest_article_date = max(
        article.get("updated", article["published"]) for article in ARTICLES
    )
    static_routes = [
        ("/", latest_article_date, "weekly", "1.0"),
        ("/start-here/", latest_article_date, "monthly", "0.8"),
        ("/the-edit/", latest_article_date, "weekly", "0.8"),
        ("/journal/", latest_article_date, "weekly", "0.9"),
        ("/fashion/", latest_article_date, "weekly", "0.8"),
        ("/home/", latest_article_date, "weekly", "0.8"),
        ("/beauty/", latest_article_date, "weekly", "0.8"),
        ("/culture/", latest_article_date, "weekly", "0.8"),
        ("/studio/", "2026-07-19", "monthly", "0.5"),
        ("/about/", "2026-07-19", "yearly", "0.5"),
        ("/contact/", "2026-07-19", "yearly", "0.4"),
        ("/editorial-policy/", "2026-07-19", "yearly", "0.4"),
        ("/affiliate-disclosure/", "2026-07-19", "yearly", "0.3"),
        ("/accessibility/", "2026-07-21", "yearly", "0.3"),
        ("/privacy/", "2026-07-19", "yearly", "0.3"),
        ("/cookies/", "2026-07-19", "yearly", "0.3"),
        ("/terms/", "2026-07-21", "yearly", "0.3"),
    ]
    sitemap_entries = [
        (
            f"<url><loc>https://byforo.com{route}</loc><lastmod>{lastmod}</lastmod>"
            f"<changefreq>{frequency}</changefreq><priority>{priority}</priority></url>"
        )
        for route, lastmod, frequency, priority in static_routes
    ]
    for article in ARTICLES:
        lastmod = article.get("updated", article["published"])
        page_text = article_path(article).read_text(encoding="utf-8")
        article_figures = re.findall(
            r'<figure\b[^>]*class="[^"]*\barticle-(?:hero|inline)-image\b[^"]*"[^>]*>.*?</figure>',
            page_text,
            flags=re.S,
        )
        image_paths = list(
            dict.fromkeys(
                source
                for figure in article_figures
                for source in re.findall(r'<img\b[^>]*\bsrc="([^"]+)"', figure)
            )
        )
        image_entries = "".join(
            "<image:image><image:loc>"
            f"https://byforo.com{html.escape(source)}"
            "</image:loc></image:image>"
            for source in image_paths
        )
        sitemap_entries.append(
            f'<url><loc>https://byforo.com{article["url"]}</loc><lastmod>{lastmod}</lastmod>'
            f"<changefreq>monthly</changefreq><priority>0.7</priority>{image_entries}</url>"
        )
    sitemap = (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" '
        'xmlns:image="http://www.google.com/schemas/sitemap-image/1.1">\n'
        + "\n".join(sitemap_entries)
        + "\n</urlset>\n"
    )
    (ROOT / "sitemap.xml").write_text(sitemap, encoding="utf-8", newline="\n")

    tz = timezone(timedelta(hours=2))
    ordered = sorted(ARTICLES, key=lambda item: item["published"], reverse=True)
    latest = datetime.strptime(
        max(article.get("updated", article["published"]) for article in ARTICLES),
        "%Y-%m-%d",
    ).replace(hour=12, tzinfo=tz)
    items = []
    for article in ordered:
        published = datetime.strptime(article["published"], "%Y-%m-%d").replace(
            hour=12,
            tzinfo=tz,
        )
        title = html.escape(article["title"])
        excerpt = html.escape(article["excerpt"])
        url = f'https://byforo.com{article["url"]}'
        items.append(
            f"<item><title>{title}</title><link>{url}</link><guid>{url}</guid>"
            f"<description>{excerpt}</description><pubDate>{format_datetime(published)}</pubDate></item>"
        )
    rss = (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<rss version="2.0"><channel><title>by.foro Journal</title>'
        '<link>https://byforo.com/</link>'
        '<description>Fashion, interiors, beauty and culture selected by by.foro.</description>'
        f"<language>en-gb</language><lastBuildDate>{format_datetime(latest)}</lastBuildDate>\n"
        + "\n".join(items)
        + "\n</channel></rss>\n"
    )
    (ROOT / "rss.xml").write_text(rss, encoding="utf-8", newline="\n")


def save_catalog() -> None:
    payload = json.dumps(ARTICLES, ensure_ascii=False, indent=2) + "\n"
    (ROOT / "content" / "articles.json").write_text(
        payload,
        encoding="utf-8",
        newline="\n",
    )


def main() -> None:
    refresh_articles()
    refresh_departments()
    refresh_homepage()
    refresh_journal()
    refresh_metadata()
    refresh_newsletter_language()
    refresh_image_markup()
    refresh_navigation()
    refresh_discovery_files()
    save_catalog()
    print(f"Refreshed {len(ARTICLES)} articles, four departments and the Journal.")


if __name__ == "__main__":
    main()
