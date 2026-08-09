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


def picture(root: str, name: str, alt: str, portrait: bool = True, cinema: bool = False) -> str:
    if cinema:
        cls = "media article-inline-image article-inline-image--cinema"
        width, height = (1280, 720)
    else:
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


def page(url: str, seo_title: str, title: str, description: str, deck: str, department: str, topic: str, hero: str, hero_alt: str, body: str, schema_type: str, words: int, keywords: list[str], hero_square: bool = False) -> str:
    canonical = f"https://byforo.com{url}"
    article_schema, crumb_schema = schemas(url, title, description, hero, department, schema_type, words, topic, keywords)
    head = f'''<!DOCTYPE html><html lang="en-GB"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover"><meta name="theme-color" content="#f2eee7"><meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1, max-video-preview:-1"><title>{html.escape(seo_title)}</title><meta name="description" content="{html.escape(description)}"><link rel="canonical" href="{canonical}"><link rel="icon" href="/assets/icons/favicon.svg" type="image/svg+xml"><link rel="manifest" href="/site.webmanifest"><meta property="og:type" content="article"><meta property="og:locale" content="en_GB"><meta property="og:site_name" content="by.foro"><meta property="og:title" content="{html.escape(seo_title)}"><meta property="og:description" content="{html.escape(description)}"><meta property="og:url" content="{canonical}"><meta property="og:image" content="https://byforo.com{hero}.jpg"><meta property="og:image:alt" content="{html.escape(hero_alt)}"><meta property="og:image:width" content="1536"><meta property="og:image:height" content="1024"><meta property="og:image:type" content="image/jpeg"><meta name="twitter:card" content="summary_large_image"><meta name="twitter:title" content="{html.escape(seo_title)}"><meta name="twitter:description" content="{html.escape(description)}"><meta name="twitter:image" content="https://byforo.com{hero}.jpg"><meta property="article:section" content="{department}"><meta property="article:published_time" content="{PUBLISHED_ISO}"><meta property="article:modified_time" content="{PUBLISHED_ISO}"><meta name="author" content="by.foro Editorial"><link rel="preload" as="style" href="/styles.css"><link rel="stylesheet" href="/styles.css"><link rel="alternate" type="application/rss+xml" title="by.foro Journal" href="https://byforo.com/rss.xml"><script id="article-schema" type="application/ld+json">{json.dumps(article_schema, ensure_ascii=False, separators=(',', ':'))}</script><script id="article-breadcrumb-schema" type="application/ld+json">{json.dumps(crumb_schema, ensure_ascii=False, separators=(',', ':'))}</script></head><body><a class="skip-link" href="#main">Skip to content</a>{site_header(url)}'''
    head = head.replace(f'property="article:section" content="{department}"', f'property="article:section" content="{topic}"')
    if department.lower() == "home":
        breadcrumb_html = f'<a href="/">Home</a><span>/</span><a href="/journal/?department=home&amp;topic={topic.lower()}">{topic}</a><span>/</span><span aria-current="page">{html.escape(title)}</span>'
    else:
        breadcrumb_html = f'<a href="/">Home</a><span>/</span><a href="/{department.lower()}/">{department}</a><span>/</span><a href="/journal/?department={department.lower()}&amp;topic={topic.lower()}">{topic}</a><span>/</span><span aria-current="page">{html.escape(title)}</span>'
    article = f'''<main id="main"><article class="article"><header class="article-hero"><nav class="breadcrumbs" aria-label="Breadcrumb">{breadcrumb_html}</nav><p class="kicker">{department} &middot; {topic}</p><h1>{html.escape(title)}</h1><p class="article-deck">{deck}</p><div class="article-meta"><a class="article-byline" href="/about/" rel="author">by.foro Editorial</a><time datetime="{PUBLISHED}">{PUBLISHED_LABEL}</time><span>{max(8, round(words / 195))} min read</span></div></header><figure class="media article-hero-image"><picture><source type="image/webp" srcset="{hero}-640.webp 640w, {hero}-960.webp 960w, {hero}.webp 1536w" sizes="(max-width:760px) calc(100vw - 2rem), 93vw"><img src="{hero}.jpg" width="1536" height="1024" loading="eager" fetchpriority="high" decoding="async" alt="{html.escape(hero_alt)}"></picture></figure>{body}<section class="next-story"></section></article></main>'''
    if hero_square:
        head = head.replace('<meta property="og:image:width" content="1536"><meta property="og:image:height" content="1024">', '<meta property="og:image:width" content="1024"><meta property="og:image:height" content="1024">')
        article = article.replace('class="media article-hero-image"', 'class="media article-hero-image article-hero-image--square"', 1)
        article = article.replace(f'{hero}.webp 1536w', f'{hero}.webp 1024w', 1)
        article = article.replace(f'<img src="{hero}.jpg" width="1536" height="1024"', f'<img src="{hero}.jpg" width="1024" height="1024"', 1)
    return head + article + site_footer() + '<script defer src="/script.js"></script></body></html>\n'


PETAL_URL = "/blogs/culture/ariana-grande-petal-streams-rankings/"
PETAL_TITLE = "Petal's First Week: What Ariana Grande's Debut Numbers Actually Mean"
PETAL_SEO = "Ariana Grande Petal Streams and UK Chart Debut Explained"
PETAL_DESCRIPTION = "Ariana Grande's Petal opened with 62.2 million Spotify streams and became her sixth UK number-one album. See the first-day and first-week data in full."
PETAL_ROOT = "/assets/images/blogs/culture/ariana-grande-petal-streams-rankings"
PETAL_HERO = f"{PETAL_ROOT}/ariana-petal-streams-hero"


petal_body = f'''<div class="article-layout"><aside class="article-aside"><p class="kicker">In this report</p><ol><li><a href="#answer">The short answer</a></li><li><a href="#ranking">First-day rankings</a></li><li><a href="#shape">Shape of the debut</a></li><li><a href="#week-one">Week-one streams</a></li><li><a href="#uk-chart">UK chart result</a></li><li><a href="#next">What comes next</a></li><li><a href="#faq">Questions answered</a></li></ol><button class="copy-link" data-copy-link type="button">Copy link</button></aside><div class="article-body"><p class="article-opening">Ariana Grande&rsquo;s <em>Petal</em> opened with 62,194,069 filtered Spotify streams on 31 July 2026. All 12 tracks entered the global top 15 and nine reached the top 10. One week later, the album became Grande&rsquo;s sixth UK number-one album. The official US Billboard 200 result had not been published when this report was updated on 9 August.</p>
<p>The first-day headline was enormous, but the more useful story is how the listening spread. <em>Petal</em> did not arrive with one giant single pulling a quiet album behind it. The title track opened at number one, the established single held almost level with it, and every song made Spotify&rsquo;s global top 15. Across the first seven release days, the 12 tracks recorded at least 236.1 million chart-counted global Spotify streams. That is a conservative total because the interlude fell below the daily chart after six days.</p>

<div class="summary-box" id="answer"><p class="kicker">The verified picture</p><h2>62.2 million on day one, then a sixth UK number one</h2><ul><li><strong>First day:</strong> 62,194,069 filtered global Spotify streams</li><li><strong>First seven release days:</strong> at least 236,096,457 chart-counted streams</li><li><strong>Title track:</strong> 33,833,025 streams across its first seven days</li><li><strong>UK result:</strong> number one, Grande&rsquo;s sixth UK chart-topping album</li><li><strong>US result:</strong> Billboard 200 debut still awaiting official publication at the time of this update</li></ul><p class="small">Updated 9 August 2026. Spotify&rsquo;s chart uses filtered streams. The week-one album figure is a minimum assembled from the public daily chart, not a claim about streams that fell outside it.</p></div>

<section id="ranking"><h2>Every Petal song ranked by first-day Spotify streams</h2><p>The table below preserves the chart order rather than rearranging the album into a review. &ldquo;Hate That I Made You Love Me&rdquo; had already been released, so its 7.69 million figure is a release-day lift for an existing single, not that song&rsquo;s lifetime total. That distinction matters.</p>
<div class="article-table-wrap" role="region" aria-label="Petal first-day Spotify rankings" tabindex="0"><table class="article-visual-table"><thead><tr><th>Global rank</th><th>Track</th><th>Filtered streams</th></tr></thead><tbody>
<tr><td>1</td><td>Petal</td><td>7,822,894</td></tr><tr><td>2</td><td>Hate That I Made You Love Me</td><td>7,685,008</td></tr><tr><td>3</td><td>Kiss Me</td><td>6,256,639</td></tr><tr><td>5</td><td>Stay</td><td>5,297,903</td></tr><tr><td>6</td><td>Oh Well</td><td>5,198,225</td></tr><tr><td>7</td><td>Big Feelings</td><td>4,821,310</td></tr><tr><td>8</td><td>Like I Do</td><td>4,772,203</td></tr><tr><td>9</td><td>Freak</td><td>4,566,216</td></tr><tr><td>10</td><td>Never Get Over Me</td><td>4,156,908</td></tr><tr><td>12</td><td>Bad Thing (Bunny Hop)</td><td>4,010,155</td></tr><tr><td>13</td><td>Warning Signs (Interlude)</td><td>3,982,011</td></tr><tr><td>15</td><td>Nowhere, Nobody</td><td>3,624,597</td></tr></tbody></table></div>
<p>The missing chart positions belonged to songs by other artists. Adding only the 12 <em>Petal</em> entries produces the 62,194,069 total. That calculation is transparent and reproducible from the linked daily chart rather than borrowed from an unattributed fan graphic.</p></section>

{picture(PETAL_ROOT, "ariana-petal-chart-impact", "White flower growing through a cracked pink star in Ariana Grande's Petal music video", cinema=True)}

<section id="shape"><h2>The shape of the debut matters more than one headline number</h2><h3>The title track won by a narrow margin</h3><p>&ldquo;Petal&rdquo; finished only 137,886 streams ahead of &ldquo;Hate That I Made You Love Me&rdquo;. That close finish gave the opening two centres of gravity. The title track had novelty, the album name and the era&rsquo;s visual thesis working for it. The earlier single had familiarity, repeat listeners and a running total that rose to more than 301 million on the same chart page.</p><p>The first week has since made that relationship clearer. The established single recorded 36,772,371 filtered streams during the seven release days, while &ldquo;Petal&rdquo; recorded 33,833,025. The older song remained the campaign&rsquo;s streaming anchor, but the title track stayed close enough to operate as a second centre rather than a one-day curiosity.</p>
<h3>&ldquo;Kiss Me&rdquo; emerged as the clearest non-single favourite</h3><p>At number three globally and 6.26 million streams, &ldquo;Kiss Me&rdquo; opened more than 950,000 streams above the album&rsquo;s fourth-highest song. First-day listening is shaped by track order, playlist exposure, social discussion and curiosity, so it is too soon to call it a lasting fan favourite. Still, it is the first track to watch for organic lift. A small decline relative to the rest of the album would say more than its debut position alone.</p>
<h3>The lower half did not collapse</h3><p>The difference between the highest new song and the lowest was about 4.2 million streams, but even &ldquo;Nowhere, Nobody&rdquo; reached number 15 globally. That breadth is unusually legible. Many album releases produce a dramatic staircase, with the opening tracks occupying the chart and later songs falling out of sight as casual listeners leave. <em>Petal</em> kept the complete sequence visible.</p><p>Track order still plays a role. Later songs have fewer chances to be reached in full-album sessions, and an interlude is not designed to compete with a lead single. The presence of &ldquo;Warning Signs (Interlude)&rdquo; at number 13 therefore describes audience commitment more convincingly than treating every song as an equal commercial proposition.</p></section>

<section id="week-one"><h2>What Petal&rsquo;s first week on Spotify actually shows</h2><p>Kworb&rsquo;s Spotify archive gives the title track 37,857,417 chart-counted streams through 7 August. Removing that day&rsquo;s 4,024,392 streams produces 33,833,025 for the first seven release days, 31 July through 6 August. The same method works for the other new tracks because their public chart totals began on release day. For the pre-release single, the seven-day window was reconstructed from the archive&rsquo;s rolling total and its known release-day figure.</p><p>Adding the 12 songs produces a minimum of 236,096,457 chart-counted streams during the release week. The word <em>minimum</em> matters. &ldquo;Warning Signs (Interlude)&rdquo; appeared on the global chart for six days and accumulated 12,217,765 chart-counted streams before falling below the public table. Any seventh-day streams outside the chart are not visible in this dataset and are not guessed here.</p><h3>The title track retained just over half of its opening-day pace</h3><p>&ldquo;Petal&rdquo; moved from 7.82 million filtered streams on release day to just under 3.98 million on 6 August, the seventh day of the release window. That is about 51 per cent of its opening pace. Decline after a major Friday launch is expected because notifications, first listens and release-night conversation are concentrated on day one. The important point is that the song still sat near four million daily streams a week later, while the established single remained slightly ahead.</p><p>&ldquo;Kiss Me&rdquo; finished the first seven days with 20,561,433 chart-counted streams, the strongest week among the remaining album tracks. &ldquo;Stay&rdquo;, &ldquo;Like I Do&rdquo; and &ldquo;Oh Well&rdquo; formed the next tier, each between 18.7 and 19 million. Those are listening patterns, not declarations about which track deserves a single campaign. Playlist placement, video support and audience behaviour can still change the order.</p></section>

<section id="context"><h2>What the streaming data proves, and what it does not</h2><p>It proves that the release generated concentrated global attention on Spotify. It proves that listeners moved beyond the previously available single. It proves that the project&rsquo;s visual campaign, release-week conversation and Grande&rsquo;s existing audience converted into full-album sampling at scale.</p><p>It does not prove how many unique people listened. Stream totals count plays, subject to Spotify&rsquo;s filtering, rather than individual listeners. It does not represent Apple Music, YouTube, Amazon Music, physical sales or downloads. It does not reveal how much traffic came from editorial playlists, personal libraries, artist pages or social links. Spotify publishes the chart result, not the private route each listener took to reach a track.</p><p>The first-week minimum is also not an album-equivalent unit total. Different charts combine streaming, downloads and physical sales under their own published rules. A clean Spotify count and an official album-chart position answer different questions.</p></section>

<section id="uk-chart"><h2>Petal debuted at number one in the UK</h2><p>On 7 August 2026, the Official Charts Company confirmed that <em>Petal</em> entered the UK Official Albums Chart at number one. It is Grande&rsquo;s sixth UK chart-topping album, extending a run that began with <em>Dangerous Woman</em> in 2016.</p><p>The result is useful because it moves the conversation beyond a platform-specific launch. Spotify&rsquo;s global daily chart describes listening activity on one service. The Official Albums Chart combines eligible UK consumption under its own rules and locates the album within one national market. Neither number replaces the other.</p><div class="update-note"><strong>Confirmed versus pending, 9 August</strong><br>Confirmed: the 31 July Spotify debut, the first seven days of public Spotify chart data and the UK number-one album. Pending at the time of this update: the official Billboard 200 debut and its reported US album-equivalent units. Forecasts and fan screenshots are not presented as results.</div></section>

{picture(PETAL_ROOT, "ariana-petal-next-week", "Ariana Grande seated between audition panellists in the official Petal music video", cinema=True)}

<section id="next"><h2>The two results that matter next</h2><h3>The official US debut</h3><p>The Billboard 200 will locate <em>Petal</em> within the US album market and, when a verified breakdown is published, show the balance between streaming and traditional album sales. Until Billboard posts the result, any position or unit total remains a projection. This article will not convert predictions into facts simply because they circulate widely.</p><h3>The second-week floor</h3><p>Week one measures event power. Week two begins to measure habit. A large decline after a blockbuster launch is normal and should not automatically be treated as failure. What matters is where the album settles, which tracks continue to travel independently and whether a video, live performance or new single redistributes attention.</p><p>The companion by.foro feature, <a href="/blogs/culture/ariana-grande-petal-meaning/">Ariana Grande&rsquo;s <em>Petal</em> era explained</a>, reads the flowers, monochrome imagery and anger beneath the visual softness. This report has a narrower job: keep the commercial record accurate as the campaign develops. The numbers and the aesthetic answer different questions, so the articles are connected without being duplicates.</p></section>

<section id="faq" class="article-faq"><h2>Petal streams and chart questions</h2><h3>How many Spotify streams did Petal get on its first day?</h3><p>The 12 tracks totalled 62,194,069 filtered global Spotify streams on 31 July 2026, calculated from Spotify&rsquo;s daily chart as archived by Kworb.</p><h3>How many Spotify streams did Petal get in its first week?</h3><p>The public daily chart records at least 236,096,457 filtered streams across the 12 tracks during the first seven release days. The true filtered total may be slightly higher because &ldquo;Warning Signs (Interlude)&rdquo; fell below the public global chart after six days.</p><h3>Did Petal reach number one in the UK?</h3><p>Yes. <em>Petal</em> debuted at number one on the UK Official Albums Chart on 7 August 2026, becoming Grande&rsquo;s sixth UK number-one album.</p><h3>What is Petal&rsquo;s Billboard 200 ranking?</h3><p>Billboard had not published the album&rsquo;s official debut when this report was checked on 9 August 2026. Any position circulating before that publication should be treated as a projection.</p></section>

<section class="source-note"><h2>Sources, method and image credits</h2><p>Streaming positions and filtered counts come from <a href="https://kworb.net/spotify/country/global_daily.html">Kworb&rsquo;s archive of Spotify&rsquo;s global daily chart</a> and its <a href="https://kworb.net/spotify/country/global_daily_totals.html">global chart totals</a>, checked through 7 August 2026. Release context was checked against the <a href="https://apnews.com/article/ariana-grande-petal-album-music-review-6c689addb7892b2f08aa57568e722bb2">Associated Press review published 31 July 2026</a>. The UK result and career total were checked against <a href="https://www.officialcharts.com/artist/26221/ariana-grande/">Ariana Grande&rsquo;s Official Charts history</a>. Calculations use only displayed filtered counts; no fan estimate is presented as an official result.</p><p>Visuals: official <em>Petal</em> album artwork photographed by Katia Temkin for Ariana Grande / Republic Records, via AP; stills from Ariana Grande&rsquo;s official <a href="https://www.youtube.com/watch?v=afSgBNwmZrQ">&ldquo;petal&rdquo; music video</a>, directed by Christian Breslauer and released by Babydoll Music / Republic Records. Images have been compressed into responsive WebP and JPG formats without changing their original aspect ratios.</p></section>
<section><h2>The useful reading of a very large opening</h2><p><em>Petal</em> arrived as both an album and a coordinated public event. Its first day shows that the event worked. The full track list was heard, the title song competed immediately with an established hit and the audience did not disappear halfway through the running order. The UK number one now shows that the attention translated into an official weekly result.</p><p>The next phase is quieter and more revealing. Songs separate from campaign imagery and repeat listening replaces curiosity. The US result will add another market view, but it will not rewrite the Spotify pattern or the UK outcome. The more durable question is where the album settles after the release event is over.</p></section>
<div class="article-end"><span>End</span><p>Published 2 August and updated 9 August 2026. The next update will follow the official Billboard 200 publication. For corrections, contact <a href="mailto:hello@byforo.com">hello@byforo.com</a>.</p></div></div></div>'''


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
            "updated": "2026-08-09",
            "readingMinutes": 11,
            "readingWordsPerMinute": 195,
            "url": PETAL_URL,
            "excerpt": "Ariana Grande's Petal opened with 62.2 million Spotify streams, recorded at least 236.1 million in its first seven days and became her sixth UK number-one album.",
            "image": {"webp": f"{PETAL_HERO}.webp", "fallback": f"{PETAL_HERO}.jpg", "alt": "Black-and-white Petal album cover portrait of Ariana Grande smiling behind loose hair", "width": 1024, "height": 1024},
            "imageShape": "square",
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
    write_article(PETAL_URL, page(PETAL_URL, PETAL_SEO, PETAL_TITLE, PETAL_DESCRIPTION, "A 62.2 million-stream opening put every track in Spotify&rsquo;s global top 15. One week later, <em>Petal</em> became Ariana Grande&rsquo;s sixth UK number-one album.", "Culture", "Music", PETAL_HERO, "Black-and-white Petal album cover portrait of Ariana Grande smiling behind loose hair", petal_body, "NewsArticle", 2250, ["Ariana Grande Petal streams", "Petal first week streams", "Petal Spotify ranking", "Ariana Grande Petal UK chart debut"], hero_square=True))
    write_article(CLEAN_URL, page(CLEAN_URL, CLEAN_SEO, CLEAN_TITLE, CLEAN_DESCRIPTION, "A cleaner home starts before the cloth comes out. These five precise systems control the routes that dirt and clutter use to spread.", "Home", "Cleaning", CLEAN_HERO, "Calm lived-in living room with oak shelving, linen seating and a clear stone coffee table", clean_body, "BlogPosting", 2150, ["how to keep your space clean", "how to keep a room clean", "clean home systems", "unusual cleaning tips"]))
    update_catalogue()
    add_reciprocal_link(
        ROOT / "blogs" / "culture" / "ariana-grande-petal-meaning" / "index.html",
        r"(<p class=\"article-opening\">.*?</p>)",
        '<p>For the commercial picture, our separate <a href="/blogs/culture/ariana-grande-petal-streams-rankings/">Petal streams and chart report</a> now covers the confirmed first-week Spotify pattern, the album&rsquo;s UK number-one debut and the still-pending US result.</p>',
    )
    add_reciprocal_link(
        ROOT / "blogs" / "home" / "lived-in-interior-design-2026" / "index.html",
        r"(<p class=\"article-opening\">.*?</p>)",
        '<p>A lived-in room still needs working order. Our guide to <a href="/blogs/home/how-to-keep-your-space-clean/">keeping a space clean with five uncommon systems</a> separates useful signs of life from dirt and unresolved clutter.</p>',
    )


if __name__ == "__main__":
    main()
