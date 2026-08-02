"""Build the Petal streaming report and the five-system cleaning guide."""

from __future__ import annotations

import html
import json
import re
from pathlib import Path

from refresh_site import ROOT, site_footer, site_header


PUBLISHED = "2026-08-02"
PUBLISHED_LABEL = "2 August 2026"
PUBLISHED_ISO = "2026-08-02T14:30:00+02:00"


def picture(root: str, name: str, alt: str, portrait: bool = True) -> str:
    cls = "media article-inline-image article-inline-image--portrait" if portrait else "media article-inline-image"
    width, height = ((1200, 1500) if portrait else (1536, 1024))
    return f'''<figure class="{cls}"><picture><source type="image/webp" srcset="{root}/{name}-640.webp 640w, {root}/{name}-960.webp 960w, {root}/{name}.webp {width}w" sizes="(max-width: 760px) calc(100vw - 2rem), 680px"><img src="{root}/{name}.jpg" width="{width}" height="{height}" loading="lazy" decoding="async" alt="{html.escape(alt)}"></picture></figure>'''


def schemas(url: str, title: str, description: str, image: str, section: str, kind: str, words: int, topic: str, keywords: list[str]) -> tuple[dict, dict]:
    canonical = f"https://byforo.com{url}"
    article = {
        "@context": "https://schema.org",
        "@type": kind,
        "mainEntityOfPage": {"@type": "WebPage", "@id": canonical},
        "headline": title,
        "description": description,
        "image": [f"https://byforo.com{image}.jpg"],
        "datePublished": PUBLISHED_ISO,
        "dateModified": PUBLISHED_ISO,
        "author": {"@type": "Organization", "name": "by.foro Editorial", "url": "https://byforo.com/about/"},
        "publisher": {"@type": "Organization", "name": "by.foro", "url": "https://byforo.com/"},
        "articleSection": section,
        "keywords": keywords,
        "inLanguage": "en-GB",
        "isAccessibleForFree": True,
        "wordCount": words,
    }
    if section.lower() == "home":
        crumb_items = [
            {"@type": "ListItem", "position": 1, "name": "Home", "item": "https://byforo.com/"},
            {"@type": "ListItem", "position": 2, "name": topic, "item": f"https://byforo.com/journal/?department=home&topic={topic.lower()}"},
            {"@type": "ListItem", "position": 3, "name": title, "item": canonical},
        ]
    else:
        crumb_items = [
            {"@type": "ListItem", "position": 1, "name": "Home", "item": "https://byforo.com/"},
            {"@type": "ListItem", "position": 2, "name": section, "item": f"https://byforo.com/{section.lower()}/"},
            {"@type": "ListItem", "position": 3, "name": topic, "item": f"https://byforo.com/journal/?department={section.lower()}&topic={topic.lower()}"},
            {"@type": "ListItem", "position": 4, "name": title, "item": canonical},
        ]
    crumbs = {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": crumb_items,
    }
    return article, crumbs


def page(url: str, seo_title: str, title: str, description: str, deck: str, department: str, topic: str, hero: str, hero_alt: str, body: str, schema_type: str, words: int, keywords: list[str]) -> str:
    canonical = f"https://byforo.com{url}"
    article_schema, crumb_schema = schemas(url, title, description, hero, department, schema_type, words, topic, keywords)
    head = f'''<!DOCTYPE html><html lang="en-GB"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover"><meta name="theme-color" content="#f2eee7"><meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1, max-video-preview:-1"><title>{html.escape(seo_title)}</title><meta name="description" content="{html.escape(description)}"><link rel="canonical" href="{canonical}"><link rel="icon" href="/assets/icons/favicon.svg" type="image/svg+xml"><link rel="manifest" href="/site.webmanifest"><meta property="og:type" content="article"><meta property="og:locale" content="en_GB"><meta property="og:site_name" content="by.foro"><meta property="og:title" content="{html.escape(seo_title)}"><meta property="og:description" content="{html.escape(description)}"><meta property="og:url" content="{canonical}"><meta property="og:image" content="https://byforo.com{hero}.jpg"><meta property="og:image:alt" content="{html.escape(hero_alt)}"><meta property="og:image:width" content="1536"><meta property="og:image:height" content="1024"><meta property="og:image:type" content="image/jpeg"><meta name="twitter:card" content="summary_large_image"><meta name="twitter:title" content="{html.escape(seo_title)}"><meta name="twitter:description" content="{html.escape(description)}"><meta name="twitter:image" content="https://byforo.com{hero}.jpg"><meta property="article:section" content="{department}"><meta property="article:published_time" content="{PUBLISHED_ISO}"><meta property="article:modified_time" content="{PUBLISHED_ISO}"><meta name="author" content="by.foro Editorial"><link rel="preload" as="style" href="/styles.css"><link rel="stylesheet" href="/styles.css"><link rel="alternate" type="application/rss+xml" title="by.foro Journal" href="https://byforo.com/rss.xml"><script id="article-schema" type="application/ld+json">{json.dumps(article_schema, ensure_ascii=False, separators=(',', ':'))}</script><script id="article-breadcrumb-schema" type="application/ld+json">{json.dumps(crumb_schema, ensure_ascii=False, separators=(',', ':'))}</script></head><body><a class="skip-link" href="#main">Skip to content</a>{site_header(url)}'''
    if department.lower() == "home":
        breadcrumb_html = f'<a href="/">Home</a><span>/</span><a href="/journal/?department=home&amp;topic={topic.lower()}">{topic}</a><span>/</span><span aria-current="page">{html.escape(title)}</span>'
    else:
        breadcrumb_html = f'<a href="/">Home</a><span>/</span><a href="/{department.lower()}/">{department}</a><span>/</span><a href="/journal/?department={department.lower()}&amp;topic={topic.lower()}">{topic}</a><span>/</span><span aria-current="page">{html.escape(title)}</span>'
    article = f'''<main id="main"><article class="article"><header class="article-hero"><nav class="breadcrumbs" aria-label="Breadcrumb">{breadcrumb_html}</nav><p class="kicker">{department} &middot; {topic}</p><h1>{html.escape(title)}</h1><p class="article-deck">{deck}</p><div class="article-meta"><a class="article-byline" href="/about/" rel="author">by.foro Editorial</a><time datetime="{PUBLISHED}">{PUBLISHED_LABEL}</time><span>{max(8, round(words / 195))} min read</span></div></header><figure class="media article-hero-image"><picture><source type="image/webp" srcset="{hero}-640.webp 640w, {hero}-960.webp 960w, {hero}.webp 1536w" sizes="(max-width:760px) calc(100vw - 2rem), 93vw"><img src="{hero}.jpg" width="1536" height="1024" loading="eager" fetchpriority="high" decoding="async" alt="{html.escape(hero_alt)}"></picture></figure>{body}<section class="next-story"></section></article></main>'''
    return head + article + site_footer() + '<script defer src="/script.js"></script></body></html>\n'


PETAL_URL = "/blogs/culture/ariana-grande-petal-streams-rankings/"
PETAL_TITLE = "Petal's First-Day Numbers: What Ariana Grande's Streaming Debut Actually Means"
PETAL_SEO = "Ariana Grande Petal Streams: First-Day Rankings"
PETAL_DESCRIPTION = "Ariana Grande's Petal opened with 62.2 million Spotify streams. See every track's global ranking and what the first-day debut means worldwide in 2026."
PETAL_ROOT = "/assets/images/blogs/culture/ariana-grande-petal-streams-rankings"
PETAL_HERO = f"{PETAL_ROOT}/ariana-petal-streams-hero"


petal_body = f'''<div class="article-layout"><aside class="article-aside"><p class="kicker">In this report</p><ol><li><a href="#answer">The number</a></li><li><a href="#ranking">Track rankings</a></li><li><a href="#shape">Shape of the debut</a></li><li><a href="#context">What it proves</a></li><li><a href="#pending">What is pending</a></li><li><a href="#next">What to watch</a></li><li><a href="#faq">Questions answered</a></li></ol><button class="copy-link" data-copy-link type="button">Copy link</button></aside><div class="article-body"><p class="article-opening">Ariana Grande&rsquo;s <em>Petal</em> opened with 62,194,069 filtered Spotify streams on 31 July 2026, according to Kworb&rsquo;s archive of Spotify&rsquo;s global daily chart. All 12 tracks entered the global top 15. Nine landed inside the top 10, led by the title track at number one with 7,822,894 streams.</p>
<p>That is the clean answer to the search question. The more interesting answer is what the shape of those numbers says. <em>Petal</em> did not arrive with one giant single pulling a quiet album behind it. Listening spread across the track list, while the established single &ldquo;Hate That I Made You Love Me&rdquo; held almost level with the new title track. It is a powerful opening. It is not yet a weekly chart result, a sales total or proof of long-term popularity.</p>

<div class="summary-box" id="answer"><p class="kicker">The first-day snapshot</p><h2>62.2 million Spotify streams, with every song in the global top 15</h2><ul><li><strong>Album total:</strong> 62,194,069 filtered Spotify streams</li><li><strong>Highest new entry:</strong> &ldquo;Petal&rdquo; at number one</li><li><strong>Top 10:</strong> nine of 12 tracks</li><li><strong>Top 15:</strong> all 12 tracks</li><li><strong>Measurement:</strong> Spotify global daily chart for 31 July 2026</li></ul><p class="small">Figures checked 2 August 2026. Spotify&rsquo;s chart uses filtered streams, so these numbers differ from the public play counters shown inside the app.</p></div>

<section id="ranking"><h2>Every Petal song ranked by first-day Spotify streams</h2><p>The table below preserves the chart order rather than rearranging the album into a review. &ldquo;Hate That I Made You Love Me&rdquo; had already been released, so its 7.69 million figure is a release-day lift for an existing single, not that song&rsquo;s lifetime total. That distinction matters.</p>
<div class="article-table-wrap" role="region" aria-label="Petal first-day Spotify rankings" tabindex="0"><table class="article-visual-table"><thead><tr><th>Global rank</th><th>Track</th><th>Filtered streams</th></tr></thead><tbody>
<tr><td>1</td><td>Petal</td><td>7,822,894</td></tr><tr><td>2</td><td>Hate That I Made You Love Me</td><td>7,685,008</td></tr><tr><td>3</td><td>Kiss Me</td><td>6,256,639</td></tr><tr><td>5</td><td>Stay</td><td>5,297,903</td></tr><tr><td>6</td><td>Oh Well</td><td>5,198,225</td></tr><tr><td>7</td><td>Big Feelings</td><td>4,821,310</td></tr><tr><td>8</td><td>Like I Do</td><td>4,772,203</td></tr><tr><td>9</td><td>Freak</td><td>4,566,216</td></tr><tr><td>10</td><td>Never Get Over Me</td><td>4,156,908</td></tr><tr><td>12</td><td>Bad Thing (Bunny Hop)</td><td>4,010,155</td></tr><tr><td>13</td><td>Warning Signs (Interlude)</td><td>3,982,011</td></tr><tr><td>15</td><td>Nowhere, Nobody</td><td>3,624,597</td></tr></tbody></table></div>
<p>The missing chart positions belonged to songs by other artists. Adding only the 12 <em>Petal</em> entries produces the 62,194,069 total. That calculation is transparent and reproducible from the linked daily chart rather than borrowed from an unattributed fan graphic.</p></section>

{picture(PETAL_ROOT, "ariana-petal-chart-impact", "Ariana Grande performing in a white costume under blue stage lighting during the 2026 Eternal Sunshine Tour")}

<section id="shape"><h2>The shape of the debut matters more than one headline number</h2><h3>The title track won by a narrow margin</h3><p>&ldquo;Petal&rdquo; finished only 137,886 streams ahead of &ldquo;Hate That I Made You Love Me&rdquo;. That close finish gives the opening two centres of gravity. The title track had novelty, the album name and the era&rsquo;s visual thesis working for it. The earlier single had familiarity, repeat listeners and a running total that rose to more than 301 million on the same chart page.</p><p>The useful editorial reading is not that one song defeated the other. It is that the album release redirected attention without erasing the campaign&rsquo;s established anchor. If the title track holds close during the next several days, it has a plausible path to becoming the era&rsquo;s second durable centre. If it drops sharply while the single stabilises, the opening will look more event-driven.</p>
<h3>&ldquo;Kiss Me&rdquo; emerged as the clearest non-single favourite</h3><p>At number three globally and 6.26 million streams, &ldquo;Kiss Me&rdquo; opened more than 950,000 streams above the album&rsquo;s fourth-highest song. First-day listening is shaped by track order, playlist exposure, social discussion and curiosity, so it is too soon to call it a lasting fan favourite. Still, it is the first track to watch for organic lift. A small decline relative to the rest of the album would say more than its debut position alone.</p>
<h3>The lower half did not collapse</h3><p>The difference between the highest new song and the lowest was about 4.2 million streams, but even &ldquo;Nowhere, Nobody&rdquo; reached number 15 globally. That breadth is unusually legible. Many album releases produce a dramatic staircase, with the opening tracks occupying the chart and later songs falling out of sight as casual listeners leave. <em>Petal</em> kept the complete sequence visible.</p><p>Track order still plays a role. Later songs have fewer chances to be reached in full-album sessions, and an interlude is not designed to compete with a lead single. The presence of &ldquo;Warning Signs (Interlude)&rdquo; at number 13 therefore describes audience commitment more convincingly than treating every song as an equal commercial proposition.</p><p>It also gives the next update a useful baseline. If the later tracks keep a similar share of the album total after launch day, listeners are returning to the project as a sequence rather than visiting only the songs already circulating in clips and playlists.</p></section>

<section id="context"><h2>What Petal&rsquo;s streaming debut proves, and what it does not</h2><p>It proves that the release generated concentrated global attention on Spotify. It proves that listeners moved beyond the previously available single. It proves that the project&rsquo;s visual campaign, release-week conversation and Grande&rsquo;s existing audience converted into full-album sampling at scale.</p><p>It does not prove how many unique people listened. Stream totals count plays, subject to Spotify&rsquo;s filtering, rather than individual listeners. It does not represent Apple Music, YouTube, Amazon Music, physical sales or downloads. It does not reveal how much of the traffic came from editorial playlists, personal libraries, artist pages or social links. Spotify publishes the chart result, not the private route each listener took to reach a track.</p><p>Most importantly, a first-day number does not establish longevity. Album launches concentrate curiosity into a few hours, especially when a major artist releases on a Friday at the start of the chart-tracking week. The more demanding test begins on day two: how much listening remains once the first complete play, notifications and opening-night conversation have passed.</p>
<div class="update-note"><strong>Confirmed versus pending</strong><br>Confirmed as of 2 August: Spotify&rsquo;s 31 July global daily rankings and filtered stream counts; the 12-track release; the existing single&rsquo;s number-one history. Pending: <em>Petal</em>&rsquo;s first Billboard 200 position, its first Official Albums Chart position in the UK, first-week album-equivalent units and complete week-one streaming totals.</div></section>

<section id="pending"><h2>Why there is no honest Billboard 200 ranking yet</h2><p><em>Petal</em> was released on Friday, 31 July. On Sunday, 2 August, the album had not completed a full chart week. A claimed Billboard 200 debut at this point would be a forecast, leak or invention, not a published result. The same applies to the UK Official Albums Chart. We will add those positions after the chart organisations publish them.</p><p>There is useful context without pretending the future has happened. The Associated Press identified <em>Petal</em> as Grande&rsquo;s eighth studio album and noted that &ldquo;Hate That I Made You Love Me&rdquo; became her tenth Billboard Hot 100 number one. The Official Charts Company records five UK number-one albums before <em>Petal</em>. Those are established career markers. They are not substitutes for this album&rsquo;s result.</p><p>This separation between confirmed data and pending data is particularly important around celebrity releases. Search results fill quickly with screenshots that omit whether a figure is filtered, global, platform-specific or estimated. One number can be accurate and still be described inaccurately. &ldquo;62.2 million Spotify streams on the global daily chart&rdquo; is precise. &ldquo;62.2 million streams everywhere&rdquo; is not.</p></section>

{picture(PETAL_ROOT, "ariana-petal-next-week", "Ariana Grande singing with one arm raised during a 2026 arena performance")}

<section id="next"><h2>The three numbers that will matter next</h2><h3>1. Day-two retention</h3><p>Day-two streams reveal which songs survived the launch ritual. Compare each track with itself rather than obsessing over a single album-wide percentage. A song can lose fewer streams than its neighbours and climb in relative importance even while its raw total falls.</p><h3>2. First-week chart units</h3><p>The Billboard 200 combines several forms of consumption under published chart rules. The final rank will locate <em>Petal</em> within the US market, while the breakdown between streaming and traditional album sales will show what kind of release this was. The UK chart will offer a separate market comparison, not a duplicate verdict.</p><h3>3. The second-week floor</h3><p>Week one measures event power. Week two begins to measure habit. A large second-week drop is normal for a blockbuster release and should not be treated automatically as failure. What matters is where the album settles, which tracks continue to travel independently and whether a video, live performance or new single changes the distribution of attention.</p><p>The older by.foro feature, <a href="/blogs/culture/ariana-grande-petal-meaning/">Ariana Grande&rsquo;s <em>Petal</em> era explained</a>, reads the flowers, monochrome imagery and anger beneath the visual softness. This report has a narrower job: keep the commercial record accurate as the campaign develops. Each article links back to the other because the numbers and the aesthetic answer different questions.</p></section>

<section id="faq" class="article-faq"><h2>Petal streams and chart questions</h2><h3>How many Spotify streams did Petal get on its first day?</h3><p>The 12 tracks totalled 62,194,069 filtered global Spotify streams on 31 July 2026, calculated from Spotify&rsquo;s daily chart as archived by Kworb.</p><h3>What was Petal&rsquo;s biggest song on release day?</h3><p>The title track ranked number one globally with 7,822,894 filtered streams. &ldquo;Hate That I Made You Love Me&rdquo; followed at number two with 7,685,008.</p><h3>Did every Petal song enter Spotify&rsquo;s global chart?</h3><p>Yes. All 12 songs appeared in the global top 15, and nine appeared in the top 10 on the 31 July daily chart.</p><h3>What is Petal&rsquo;s Billboard 200 ranking?</h3><p>There was no published debut position when this report was checked on 2 August 2026. The album had only just begun its first full tracking week. This page will be updated when Billboard publishes the result.</p></section>

<section class="source-note"><h2>Sources, method and image credits</h2><p>Streaming positions and filtered counts come from <a href="https://kworb.net/spotify/country/global_daily.html">Kworb&rsquo;s archive of Spotify&rsquo;s global daily chart</a> for 31 July 2026. Release and career context was checked against the <a href="https://apnews.com/article/ariana-grande-petal-album-music-review-6c689addb7892b2f08aa57568e722bb2">Associated Press review published 31 July 2026</a> and <a href="https://www.officialcharts.com/artist/26221/ariana-grande/">Ariana Grande&rsquo;s Official Charts artist history</a>. Album totals were calculated by adding the 12 displayed track figures. No unverified fan estimate is presented as an official chart result.</p><p>Photographs: GZMUSICRECORDS, Ariana Grande performing &ldquo;Break Free&rdquo; on the Eternal Sunshine Tour at Oakland Arena, 6 June 2026, via Wikimedia Commons (<a href="https://commons.wikimedia.org/wiki/File:Ariana_-_Break_Free_-_Eternal_Sunshine_Tour_2.jpg">image 2</a>, <a href="https://commons.wikimedia.org/wiki/File:Ariana_-_Break_Free_-_Eternal_Sunshine_Tour_6.jpg">image 6</a>, <a href="https://commons.wikimedia.org/wiki/File:Ariana_-_Break_Free_-_Eternal_Sunshine_Tour_8.jpg">image 8</a>), licensed <a href="https://creativecommons.org/licenses/by/3.0/">CC BY 3.0</a>. Images have been cropped and compressed for the page.</p></section>
<section><h2>The useful reading of a very large opening</h2><p><em>Petal</em> arrived as both an album and a coordinated public event. Its first day shows that the event worked. The full track list was heard, the title song competed immediately with an established hit and the audience did not disappear halfway through the running order. That is more informative than declaring victory from one enormous total.</p><p>The next phase is quieter and more revealing. Songs separate from campaign imagery. Repeat listening replaces curiosity. Official weekly charts replace projections. This page will follow that movement without turning every fluctuation into a crisis or every fan claim into fact.</p></section>
<div class="article-end"><span>End</span><p>Data checked 2 August 2026. This live report will be updated after the first weekly charts. For corrections, contact <a href="mailto:hello@byforo.com">hello@byforo.com</a>.</p></div></div></div>'''


CLEAN_URL = "/blogs/home/how-to-keep-your-space-clean/"
CLEAN_TITLE = "How to Keep Your Space Clean: 5 Systems You Probably Haven't Tried"
CLEAN_SEO = "How to Keep Your Space Clean: 5 Unusual Systems"
CLEAN_DESCRIPTION = "Keep your space clean with five uncommon systems for stopping dirt, clutter and half-finished tasks before they spread through your home every day."
CLEAN_ROOT = "/assets/images/blogs/home/how-to-keep-your-space-clean"
CLEAN_HERO = f"{CLEAN_ROOT}/how-to-keep-your-space-clean-hero"


clean_body = f'''<div class="article-layout"><aside class="article-aside"><p class="kicker">Five systems</p><ol><li><a href="#answer">Start here</a></li><li><a href="#transfer">Map transfers</a></li><li><a href="#third-state">Add a third state</a></li><li><a href="#light">Audit with light</a></li><li><a href="#close">End the room</a></li><li><a href="#clear">Keep one span clear</a></li><li><a href="#routine">Build your routine</a></li></ol><button class="copy-link" data-copy-link type="button">Copy link</button></aside><div class="article-body"><p class="article-opening">To keep your space clean, stop treating the whole home as one enormous job. Control the five moments when disorder spreads: when outdoor dirt crosses the door, when an object is left between uses, when dust becomes invisible, when a room&rsquo;s activity ends and when every surface loses its last empty patch.</p><p>The standard advice is familiar: make a schedule, buy matching containers, clean as you go. None of it is wrong. It fails when it asks motivation to compensate for a badly designed room. The five systems below change the route of mess before they ask you to clean more. They work in a rented room, a family home or a small flat because each one is attached to behaviour you already repeat.</p>

<div class="summary-box" id="answer"><p class="kicker">The short answer</p><h2>Design for the handoff, not the perfect room</h2><p>A consistently clean home has a place for dirt at the entrance, a temporary home for objects still in use, a reliable way to reveal residue, a closing action for each room and one surface that is never allowed to fill. Set up those five points first. Then clean only what the evidence says needs attention.</p></div>

<section id="transfer"><h2>1. Map the transfer chain</h2><p>Most cleaning plans are organised by room: kitchen on Tuesday, bathroom on Thursday, floors at the weekend. Dirt does not respect that map. It travels in a chain. Shoes touch pavement, then an entry floor, then perhaps a bedroom rug. Grocery bags land on a hall console, then a kitchen counter. A wet umbrella leans against a wall, drips on the floor and gets moved again because it blocks the door.</p><p>Trace the first three handoffs instead. Stand outside your door and narrate what happens when you arrive carrying a bag. Where do your shoes stop? Where do keys leave your hand? Where does outerwear wait if it is damp? Every place where the answer is &ldquo;wherever there is space&rdquo; is a transfer leak.</p><h3>Build a capture point at the first contact</h3><p>Use two mats rather than one decorative mat. The outside mat removes coarse grit; a washable inside mat catches what remains. Add a shoe position that is genuinely closer than the bedroom, a rigid tray for wet soles and a hook or rail that can be reached while holding a bag. This does not require a grand boot room. A 60-centimetre strip beside a flat door can hold a mat, three hooks and a shallow tray.</p><p>The United States Environmental Protection Agency recommends mats and leaving shoes at the door as practical ways to reduce dirt and dust tracked indoors. That is source control: stop material before it becomes a whole-floor problem. The same logic applies inside. Put a small cloth where coffee is made, not in a distant utility cupboard. Keep a hair-catching brush beside the bathroom bin, not with the vacuum.</p>{picture(CLEAN_ROOT, "clean-entry-transfer-route", "Calm apartment entry with two doormats, a shoe tray, oak bench, wall hooks and a small landing tray")}
<h3>The 20-second transfer test</h3><p>Walk through the door as you normally do and give yourself 20 seconds to put everything down correctly. If an object has no destination, note it. If the destination requires opening a crowded cupboard or crossing the home, move it closer. A system that works only when both hands are free and you are in a good mood is decoration, not infrastructure.</p><p>For children, lower the hook rather than repeating the instruction. For pets, put the towel where the lead comes off. For a tiny rental, a removable adhesive rail and one lidded basket can define the landing zone without changing the building. The goal is not to display an immaculate entrance. It is to keep the outside from travelling farther.</p></section>

<section id="third-state"><h2>2. Give belongings a third state</h2><p>Storage advice usually offers two conditions: put away or dirty. Real life has a third. The jumper worn for two hours is not ready for the laundry and not clean enough for the wardrobe. The book beside the sofa is in progress. The charger belongs to a phone that will need it again tonight. A bag contains tomorrow&rsquo;s return. When a home refuses this middle state, chairs, floors and worktops become unofficial storage.</p><p>Create one active-use station in each relevant zone. In a bedroom, it might be a narrow valet rail with three hangers and a small basket. In a living room, it can be a tray that holds the current book, glasses and remote. Near the door, use a single hook for the bag that is packed for tomorrow. The boundary must be smaller than your ambition. A whole chair becomes a pile; one hook becomes a decision.</p><h3>Set an expiry rule</h3><p>The station is not permanent storage. Give every active object a condition for leaving. Half-worn clothes are reviewed when the rail reaches three pieces. A current-project tray is reset on Sunday evening. Returns leave beside the keys on the next errand day. The rule should be visible and physical, not a reminder buried in an app.</p><p>This system also protects the look of a <a href="/blogs/home/lived-in-interior-design-2026/">lived-in interior</a>. A home can show evidence of life without every surface becoming a holding area. One open book and a folded throw read as use. Seven unrelated errands spread across a table read as unresolved decisions. The third state gives everyday life a frame.</p><h3>Do not buy the container first</h3><p>Observe the pile for a week before choosing its boundary. If clothes gather on the chair, a lidded basket may hide them but make airing impossible. If mail accumulates near the kitchen, a pretty box can delay decisions until it overflows. Match the container to the behaviour: rail for airing, vertical file for papers, tray for objects that must leave together, hook for a single repeat-use bag.</p></section>

<section id="light"><h2>3. Use an oblique-light audit</h2><p>Dust is difficult to judge under soft overhead light. A surface can look clean at noon and reveal a fine field of crumbs, hair and residue when evening light crosses it from the side. Use that fact deliberately. Once or twice a week, hold a small flashlight or adjustable task lamp low and parallel to the counter, shelf or floor. The raking light casts tiny shadows and turns invisible residue into a precise cleaning list.</p><p>This is not a ritual for inspecting every centimetre of the home. Choose the places where touch and food matter: the kitchen worktop, dining table, bathroom ledge, desk and the floor beside the bed. Thirty seconds of low light can tell you whether a wipe is needed more reliably than the calendar.</p>{picture(CLEAN_ROOT, "oblique-light-cleaning-check", "Low task light revealing a few crumbs on a dark stone kitchen counter beside a folded cloth and brush")}
<h3>Clean what the light reveals</h3><p>Start at the far edge and work towards yourself with a damp microfibre cloth that suits the surface. Fold the cloth into quarters so each pass can use a clean face. For dry dust on a shelf, dampness helps keep particles from returning immediately to the air. The EPA similarly advises damp cloths for settled dust and notes that a high-efficiency particulate air vacuum can help capture fine particles.</p><p>Do not turn the audit into indiscriminate disinfecting. The US Centers for Disease Control and Prevention says routine cleaning with soap and water, or a suitable household cleaner, is usually enough in most homes; disinfecting is generally needed when someone is ill or at greater risk. If you do disinfect, clean first, follow the label and never mix products. Marble, unsealed wood and speciality finishes need surface-specific care.</p><h3>Use the audit before guests, not after panic begins</h3><p>Low light is especially useful the evening before people visit. It exposes the places daylight flatters and directs ten focused minutes towards the marks guests actually encounter. It also prevents waste. If the shelf passes the test, leave it alone. A cleaning routine should produce confidence, not a compulsive search for contamination.</p></section>

<section id="close"><h2>4. End the room, not the day</h2><p>&ldquo;Reset the house before bed&rdquo; sounds efficient until bedtime arrives with four rooms still open. Instead, close each room when its main activity ends. The trigger is already part of your life, so the reset does not need a new time slot.</p><p>When the kettle boils after dinner, close the kitchen: load the last cups, wipe the preparation strip and hang the cloth. When the television switches off, close the living room: return the remote, straighten one cushion and carry out glasses. When you brush your teeth, close the bathroom: rinse the basin and hang the towel flat. When you plug in the laptop, close the desk: remove cups, stack current papers and leave the keyboard clear.</p><h3>A closure has three moves</h3><ol><li><strong>Remove:</strong> take away anything that belongs in another room.</li><li><strong>Restore:</strong> return the room&rsquo;s working objects to their first position.</li><li><strong>Ready:</strong> prepare the first action of the next use, such as leaving a clear chopping area or an empty desk chair.</li></ol><p>Keep the closure under three minutes. If it regularly takes longer, the room has too many active objects or an inconvenient home for something used every day. Change the storage rather than lengthening the ritual.</p><h3>What happens when you miss it</h3><p>Nothing dramatic. Close the room at the next natural endpoint. A resilient system expects late trains, headaches and interrupted evenings. It does not create a second mess made from guilt. The purpose is to break the habit of carrying every unfinished room into tomorrow.</p></section>

<section id="clear"><h2>5. Keep one hand-span legally empty</h2><p>A cluttered surface becomes harder to restore because there is nowhere to begin. You pick up one object, need to move another and create a chain of temporary piles. Reserve one hand-span, roughly the width of your open hand plus forearm, that must remain empty on the kitchen counter, dining table and desk. This is the restoration lane.</p><p>The empty strip is not wasted space. It is where you set the cloth, sort the first small group and create momentum. In the kitchen it provides a safe landing point for a hot tray. On a desk it lets you open a notebook without shifting a week of papers. On a dining table it preserves one place where a meal can begin.</p><h3>Make the boundary visible at first</h3><p>Use a seam in the worktop, the edge of a placemat or a strip between two objects. If somebody places something there, move it immediately, because the value comes from reliability. After a few weeks the boundary becomes spatial memory and no marker is needed.</p><p>This is particularly effective in a <a href="/blogs/home/small-entryway-that-looks-expensive/">small entryway</a>, where a console often turns into a general deposit. Keep the section nearest the door empty, then confine keys and post to a single tray at the far end. The room feels calmer, but the larger gain is functional: you always have a clear place to sign a form, put down groceries or wipe the surface.</p><h3>Do not confuse clear with bare</h3><p>The rest of the surface can still hold a lamp, bowl, books or flowers. The rule is not minimalist theatre. It is an access point. In a more layered room, the empty hand-span makes the objects around it appear deliberate. In a very minimal room, it protects the working space from slow accumulation.</p></section>

<section id="routine"><h2>Turn the five ideas into one quiet routine</h2><p>Begin with the transfer chain today. It usually removes the most future cleaning for the least effort. Add the third-state station once you know which pile returns most often. Try the oblique-light audit after dark, then attach one closure to the room that frustrates you most. Reserve the empty hand-span last, when each surface has fewer homeless objects.</p><div class="article-table-wrap" role="region" aria-label="Five cleaning systems and triggers" tabindex="0"><table class="article-visual-table"><thead><tr><th>Problem</th><th>System</th><th>Trigger</th><th>Useful limit</th></tr></thead><tbody><tr><td>Dirt travels indoors</td><td>Transfer chain</td><td>Crossing the threshold</td><td>First three handoffs</td></tr><tr><td>Objects are between uses</td><td>Third state</td><td>Taking off or pausing</td><td>One small station</td></tr><tr><td>Residue hides</td><td>Oblique light</td><td>Twice weekly or before guests</td><td>Five high-use surfaces</td></tr><tr><td>Rooms stay unfinished</td><td>Room closure</td><td>Last action in the room</td><td>Three minutes</td></tr><tr><td>There is nowhere to start</td><td>Empty hand-span</td><td>Any object enters the lane</td><td>One reliable clear patch</td></tr></tbody></table></div>
<p>After two weeks, remove anything you are performing only for the system itself. If the entry tray never catches wet shoes, it may be unnecessary. If the bedroom rail is always full, reduce its capacity or change the expiry rule. If the flashlight shows the same clean surface repeatedly, audit it less often. A good home system gets smaller as it learns the household.</p><p>The result should also support the visual life of the room. For a more refined baseline, use the principles in <a href="/blogs/home/how-to-make-a-home-look-expensive/">how to make a home look expensive</a>: fewer weak objects, better light and clear relationships between materials. Cleanliness cannot manufacture taste, but it can reveal the choices already present.</p></section>

<section class="article-faq"><h2>Questions people ask about keeping a space clean</h2><h3>How do I keep my room clean every day?</h3><p>Give active objects one temporary station, close the room after its final use and preserve one clear area where tomorrow&rsquo;s reset can begin. Those three systems take less effort than repeatedly clearing an entire room.</p><h3>Why does my space get messy so quickly?</h3><p>Usually because frequently used objects have inconvenient storage, or because items that are still in use have no temporary home. Track where the first pile forms instead of blaming a lack of discipline.</p><h3>Should I clean or disinfect my home?</h3><p>For ordinary household maintenance, cleaning is usually sufficient. Disinfect when illness or specific risk makes it appropriate, clean the surface first and follow the product label. Never mix cleaning chemicals.</p></section>

<section class="source-note"><h2>Sources and editorial notes</h2><p>Health and surface-care guidance was checked on 2 August 2026 against the <a href="https://www.cdc.gov/hygiene/about/when-and-how-to-clean-and-disinfect-your-home.html">CDC&rsquo;s household cleaning and disinfecting guidance</a>, updated 31 January 2025. Entry source control and particle-cleaning advice was cross-checked with the US Environmental Protection Agency&rsquo;s pages on <a href="https://www.epa.gov/indoor-air-quality-iaq/biological-contaminants-and-indoor-air-quality">biological contaminants and indoor air</a> and <a href="https://www.epa.gov/indoor-air-quality-iaq/sources-indoor-particulate-matter-pm">indoor particulate matter</a>. The five household systems and all photographs are original by.foro editorial work. Product labels and manufacturers&rsquo; care instructions take priority for specialist finishes.</p></section>
<section><h2>A clean home is a route, not a performance</h2><p>The most useful shift is to stop measuring cleanliness by the heroic reset. A home stays easier when grit is intercepted at the door, half-finished life has a recognised place and each room is allowed to end. The low light tells you what needs attention. The empty hand-span gives you somewhere to begin.</p><p>None of these ideas asks a house to look unused. They do the opposite. They protect the space required for cooking, reading, dressing, hosting and resting. The clean room is not the one with no evidence of a person. It is the one where that evidence has a shape.</p></section>
<div class="article-end"><span>End</span><p>Published by by.foro Editorial on 2 August 2026. For corrections, contact <a href="mailto:hello@byforo.com">hello@byforo.com</a>.</p></div></div></div>'''


def write_article(url: str, text: str) -> None:
    destination = ROOT / url.strip("/") / "index.html"
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(text, encoding="utf-8", newline="\n")
    print(f"Built {destination.relative_to(ROOT)}")


def update_catalogue() -> None:
    path = ROOT / "content" / "articles.json"
    articles = json.loads(path.read_text(encoding="utf-8"))
    new = [
        {
            "title": PETAL_TITLE,
            "department": "culture",
            "topic": "music",
            "published": PUBLISHED,
            "readingMinutes": 11,
            "readingWordsPerMinute": 195,
            "url": PETAL_URL,
            "excerpt": "Ariana Grande's Petal opened with 62.2 million filtered Spotify streams. Here is every track's global rank and what the debut can actually tell us.",
            "image": {"webp": f"{PETAL_HERO}.webp", "fallback": f"{PETAL_HERO}.jpg", "alt": "Ariana Grande performing in white under blue light during the 2026 Eternal Sunshine Tour", "width": 1536, "height": 1024},
            "metaDescription": PETAL_DESCRIPTION,
            "seoTitle": PETAL_SEO,
            "schemaType": "NewsArticle",
            "articleSection": "Music",
            "breadcrumbTopic": True,
        },
        {
            "title": CLEAN_TITLE,
            "department": "home",
            "topic": "cleaning",
            "published": PUBLISHED,
            "readingMinutes": 11,
            "readingWordsPerMinute": 195,
            "url": CLEAN_URL,
            "excerpt": "Five uncommon systems that stop dirt, clutter and half-finished tasks before they spread through a home.",
            "image": {"webp": f"{CLEAN_HERO}.webp", "fallback": f"{CLEAN_HERO}.jpg", "alt": "Calm lived-in living room with oak shelving, linen seating and a clear stone coffee table", "width": 1536, "height": 1024},
            "metaDescription": CLEAN_DESCRIPTION,
            "seoTitle": CLEAN_SEO,
            "articleSection": "Cleaning",
            "breadcrumbTopic": True,
        },
    ]
    known = {item["url"] for item in new}
    articles = new + [item for item in articles if item["url"] not in known]
    path.write_text(json.dumps(articles, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")


def add_reciprocal_link(path: Path, anchor_pattern: str, sentence: str) -> None:
    text = path.read_text(encoding="utf-8")
    if sentence in text:
        return
    match = re.search(anchor_pattern, text, flags=re.S)
    if not match:
        raise RuntimeError(f"Could not find reciprocal-link anchor in {path}")
    text = text[: match.end()] + sentence + text[match.end() :]
    path.write_text(text, encoding="utf-8", newline="\n")


def main() -> None:
    write_article(PETAL_URL, page(PETAL_URL, PETAL_SEO, PETAL_TITLE, PETAL_DESCRIPTION, "A 62.2 million-stream opening put every track in Spotify&rsquo;s global top 15. The real story is how the attention spread, what is confirmed and what remains too early to claim.", "Culture", "Music", PETAL_HERO, "Ariana Grande performing in white under blue light during the 2026 Eternal Sunshine Tour", petal_body, "NewsArticle", 2150, ["Ariana Grande Petal streams", "Petal first day streams", "Petal Spotify ranking", "Ariana Grande Petal chart debut"]))
    write_article(CLEAN_URL, page(CLEAN_URL, CLEAN_SEO, CLEAN_TITLE, CLEAN_DESCRIPTION, "A cleaner home starts before the cloth comes out. These five precise systems control the routes that dirt and clutter use to spread.", "Home", "Cleaning", CLEAN_HERO, "Calm lived-in living room with oak shelving, linen seating and a clear stone coffee table", clean_body, "BlogPosting", 2150, ["how to keep your space clean", "how to keep a room clean", "clean home systems", "unusual cleaning tips"]))
    update_catalogue()
    add_reciprocal_link(
        ROOT / "blogs" / "culture" / "ariana-grande-petal-meaning" / "index.html",
        r"(<p class=\"article-opening\">.*?</p>)",
        '<p>For the commercial picture, our separate <a href="/blogs/culture/ariana-grande-petal-streams-rankings/">Petal streams and first-day rankings report</a> tracks the confirmed Spotify data and upcoming weekly charts.</p>',
    )
    add_reciprocal_link(
        ROOT / "blogs" / "home" / "lived-in-interior-design-2026" / "index.html",
        r"(<p class=\"article-opening\">.*?</p>)",
        '<p>A lived-in room still needs working order. Our guide to <a href="/blogs/home/how-to-keep-your-space-clean/">keeping a space clean with five uncommon systems</a> separates useful signs of life from dirt and unresolved clutter.</p>',
    )


if __name__ == "__main__":
    main()
