"""Build three search-led by.foro guides published 25 September 2026."""
from __future__ import annotations

import html
import json
import re
from pathlib import Path

import build_august_two_features as base
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
base.PUBLISHED = "2026-09-25"
base.PUBLISHED_LABEL = "25 September 2026"
base.PUBLISHED_ISO = "2026-09-25T12:00:00+02:00"
SOURCE = Path(r"C:\Users\filip\.codex\generated_images\01a0d9de-ac34-7932-beb5-c4d3df8b396e")

STORIES = [
    {
        "slug": "cord-pendant-necklace-necklines", "department": "fashion", "topic": "accessories",
        "title": "The Cord Pendant Necklace Works Best When It Has Room to Land",
        "seo": "How to Wear a Cord Pendant Necklace With Every Neckline",
        "description": "A practical guide to cord pendant length, neckline pairings and layering, from crew necks and shirts to V-necks and high collars, with easy fit checks.",
        "deck": "The cord is simple. The placement makes it look considered.",
        "alt": "Sculptural silver pendant on a dark leather cord draped over a cream linen blouse on limestone",
        "image_source": "exec-5c1ff44b-063f-41c2-b6da-ee80dc020d2e.png",
        "inline_sources": [
            ("exec-1a4f5404-98bb-4dd4-a2df-c1399f51e7e1.png", "crew-neck", "Silver cord pendant placed below the neckline of a charcoal crew-neck sweater"),
            ("exec-f50ca3c5-3f86-4f90-bc90-2e2df4db251e.png", "open-shirt", "Leather cord and silver pendant arranged inside the open collar of an ivory linen shirt"),
        ],
        "keywords": ["how to wear a cord pendant necklace", "cord necklace with crew neck", "cord pendant length", "leather cord necklace styling"],
        "body": """
<p class="article-opening">To wear a cord pendant necklace well, choose where the pendant should land before choosing the cord length. Keep it clearly above or below a neckline, rather than resting on its edge. A short cord suits an open collar or scoop neck; a longer one gives a crew neck or simple knit a focal point. The pendant should have enough empty fabric around it to be seen.</p>
<p>British Vogue has identified the cord pendant as a continuing jewellery direction in 2026, describing its easy pairing with pared-back clothes. The useful question is less whether it is on trend than whether the pendant and neckline occupy different visual spaces.</p>
<div class="summary-box" id="answer"><p class="kicker">The short answer</p><h2>Make a clear gap between pendant and neckline</h2><p>Put a short pendant inside an open neck, or a longer pendant over an uninterrupted top. If the pendant collides with a collar point, top button or V, adjust the cord by a few centimetres. Check the placement while standing and sitting.</p></div>
<section id="necklines"><h2>Which length works with each neckline?</h2><h3>Crew neck and high neck</h3><p>Let the pendant sit visibly below the neck seam. A medium or long cord works better than one that disappears into the collar. Against a thick knit, choose a pendant with enough weight to lie flat; tiny charms can bounce or turn sideways.</p><h3>V-neck</h3><p>Either echo the V with a smaller pendant inside the open space or use a long cord that lands well below its point. Avoid placing the pendant exactly at the tip of the V: two focal points compete at the same height.</p><h3>Open shirt</h3><p>Wear the cord against skin, framed by the open collar, or lengthen it so the pendant falls over the shirt front. With a button-down, check that the pendant does not sit directly on a button or swing into the placket.</p><h3>Square and boat neck</h3><p>Both necklines already draw a strong horizontal line. A pendant just below the edge can look crowded. Try a short cord on bare skin above the garment, or a longer cord that creates a deliberate vertical line over it.</p></section>
<section id="length"><h2>Measure the landing point, not a number on a product page</h2><p>Necklace lengths vary in effect with body shape, pendant size and clothing. Use a piece of string to mimic the cord over the actual top. Mark the point where the pendant should rest, then measure the string. Repeat with your most worn neckline before ordering a fixed-length cord.</p><p>An adjustable slider is particularly useful if you alternate between tees, shirts and winter knits. Leave enough cord to make a secure knot or use the maker's intended adjustment method. Inspect the fastening regularly; leather and suede can wear where they rub a pendant bail.</p><p>If the necklace has an oversized object or several charms, the <a href="/blogs/fashion/kitchen-sink-necklace/">kitchen-sink necklace guide</a> explains how to give a busy composition one clear centre.</p></section>
<section id="style"><h2>Three ways to make the pendant feel intentional</h2><ol><li><strong>Repeat one material.</strong> A silver pendant can echo a belt buckle or watch. It need not match every piece of jewellery.</li><li><strong>Keep the background quiet.</strong> Plain linen, cotton or a fine knit lets the cord's matte texture and the pendant's shape register.</li><li><strong>Use scale deliberately.</strong> A delicate pendant suits a narrow cord and open collar; a sculptural stone or metal form can carry a longer drop over a heavier garment.</li></ol><p>Layering works when lengths are genuinely different. Place a fine, shorter chain near the collarbone and let the cord pendant sit lower. If both pendants land together, remove one or change a length. A <a href="/blogs/fashion/how-to-wear-a-bib-necklace/">bib necklace</a> already fills the neckline and rarely needs a cord beside it.</p></section>
<section id="materials"><h2>Choose a cord that suits the way you wear clothes</h2><p>Smooth leather gives a crisp line against linen and tailoring. Suede is softer and can look especially good against cotton, but its nap may catch on a fuzzy knit. Waxed cotton feels lighter and more casual. None is automatically better; the right material is the one that lets the pendant hang cleanly over your usual fabrics.</p><p>Check the cord from the side as well as the front. A stiff cord can make a shallow arc that pushes a light pendant away from the body. A very soft cord may collapse into a V and pull the pendant too low. If you are shopping online, ask for a photograph of the necklace worn rather than relying on a flat-lay product image.</p><p>Colour also changes the reading. Black cord against black clothing almost disappears and leaves the pendant floating. Brown cord against ivory feels warmer and more visible. A coloured cord can be the statement itself; in that case keep the pendant simple. Try the necklace with three pieces you already own before buying another top to make it work.</p></section>
<section class="article-faq"><h2>Cord necklace questions</h2><h3>Can you wear a cord pendant with a crew neck?</h3><p>Yes. Let the pendant fall clearly below the crew-neck seam so it reads against the garment rather than being caught at the collar.</p><h3>Can a cord necklace be dressed up?</h3><p>Yes. A clean cord and considered pendant can work with a tailored jacket or simple dress. Keep the cord in good condition and let the pendant be the focus.</p><h3>What if the pendant keeps turning around?</h3><p>Check whether its bail is large enough for the cord and whether the weight is balanced. A slightly heavier pendant or a flatter cord may settle better.</p></section>
<section class="source-note"><h2>Sources and image note</h2><p>Trend context: <a href="https://www.vogue.co.uk/article/article/chunky-necklace-trend">British Vogue's 2026 cord pendant coverage</a>. Fit, length and outfit guidance is by.foro editorial analysis. The image is a fictional, unbranded editorial scene created for this guide.</p></section>
<div class="article-end"><span>End</span><p>Published by by.foro Editorial on 25 September 2026. For corrections, contact <a href="mailto:hello@byforo.com">hello@byforo.com</a>.</p></div>
""",
    },
    {
        "slug": "violet-leaf-perfume-guide", "department": "beauty", "topic": "fragrance",
        "title": "Violet Leaf Perfume Smells Like the Garden After Rain",
        "seo": "Violet Leaf Perfume: What It Smells Like and How to Choose",
        "description": "What does violet leaf perfume smell like? Compare its green, watery character with powdery violet flower and learn which notes make it wearable on skin.",
        "deck": "Green, cool and faintly metallic: the leaf is a different story from the flower.",
        "alt": "Clear unbranded perfume bottle beside fresh violet leaves, a purple flower and a scent blotter on limestone",
        "image_source": "exec-b096a6ec-3049-4523-8104-b25ea59e5a60.png",
        "inline_sources": [
            ("exec-286b1ba8-b9e5-41f2-bbc0-1d6c2a4fb400.png", "violet-leaves", "Dew on fresh violet leaves beside unbranded perfume blotters on pale limestone"),
            ("exec-c8005183-7f20-442c-8d72-0963ef15b537.png", "testing-notes", "Unbranded scent samples with violet leaves, iris root and cedar shavings"),
        ],
        "keywords": ["what does violet leaf perfume smell like", "violet leaf vs violet flower perfume", "green violet leaf fragrance", "violet leaf perfume guide"],
        "body": """
<p class="article-opening">Violet leaf perfume usually smells green, watery and cool, with an edge that can recall cucumber peel, crushed stems or wet metal. It is quite different from the sweet, powdery violet-flower effect many people expect from the word violet. The rest of the formula determines whether the leaf feels like a dewy garden, a clean floral, an inky wood or a soft leather.</p>
<p>The distinction is useful when buying samples. A bottle described simply as violet may lean towards face powder and sweets, while a violet-leaf note can bring the outdoors into a musk or floral. Search by the complete note list and the desired effect, rather than assuming the purple flower and its leaf smell alike.</p>
<div class="summary-box" id="answer"><p class="kicker">The short answer</p><h2>Think crushed green leaves, not violet sweets</h2><p>Violet leaf is fresh, watery, cucumber-like and sometimes metallic. Violet flower accords tend to be softer, sweeter and more powdery. Pair the leaf with citrus or herbs for brightness, iris and musk for softness, or woods and leather for a darker scent.</p></div>
<section id="difference"><h2>Violet leaf versus violet flower</h2><p>Perfumer &amp; Flavorist describes violet leaf aldehyde as having a fresh green cucumber-like odour. That small piece of scent chemistry helps explain why a leaf-led fragrance can feel cool or almost aqueous. A powdery violet-flower impression is usually constructed as an accord; a note name on a box does not tell you which material or combination produced it.</p><p>On skin, ask which side is dominant at thirty minutes. If the opening is sharply green but the heart becomes sweet and cosmetic, the leaf may be a lift rather than the main character. If the green persists into the woods or musk, the fragrance is more likely to satisfy someone searching specifically for violet leaf.</p></section>
<section id="pairings"><h2>Choose a violet leaf perfume by what sits beside it</h2><h3>With citrus and herbs</h3><p>Bergamot, grapefruit, basil and aromatic herbs sharpen the wet-green effect. This is the most brisk style. Try it if you like the cut-stem quality of <a href="/blogs/beauty/tomato-leaf-perfume-guide/">tomato leaf perfume</a> but want something cooler and less savoury.</p><h3>With iris and musk</h3><p>Iris and soft musks turn the edge into a calmer skin scent. They can also make a violet-leaf opening dry down into something much more powdery. Test well past the first spray if powder is exactly what you are trying to avoid.</p><h3>With woods or leather</h3><p>Cedar, vetiver, suede and leather give the leaf a dark frame. The contrast can feel inky or mineral, especially when a metallic facet remains. A sample is more informative than a note pyramid here: balance differs widely between perfumes.</p></section>
<section id="test"><h2>How to test the note without mistaking the opening for the whole scent</h2><ol><li>Try one spray on a paper strip. Note whether you get cucumber, cut stems, grass or a watery floral.</li><li>Smell again after thirty minutes. Check whether the leaf remains clear or gives way to powder, musk or wood.</li><li>Wear the promising sample on unscented skin for several hours. Skin warmth can soften a sharp opening.</li><li>Compare it with a powdery violet or iris fragrance on another day. The contrast makes your preference easier to name.</li></ol><p>Do not buy a full bottle only because the first green minute feels vivid. The drydown is what you will wear for most of the day. Our <a href="/blogs/beauty/carrot-seed-perfume-guide/">carrot seed perfume guide</a> is another useful comparison: both notes can bring earthy or powdery texture, but violet leaf tends to feel wetter and greener.</p></section>
<section id="choose"><h2>How to find the right version for your wardrobe</h2><p>Start with the role you want the perfume to play. A brisk violet leaf with citrus can feel refreshing on a warm commute. A leaf-and-musk composition is easier to wear close to others. A leaf-and-leather blend can add tension to a minimal evening outfit. The same named note can support three different moods, so a list of violet-leaf perfumes is less useful than a map of their surrounding materials.</p><p>Consider how much greenness you enjoy after the first hour. Some people love the flash of crushed stem but prefer the base to become clean and soft. Others want the wet, metallic quality to persist. Write that preference down while testing; memory tends to preserve the exciting opening and forget the ordinary drydown.</p><p>If a sample turns too powdery, look for citrus, vetiver or herbs in the next one. If it feels too sharp, compare a version with musk, iris or pale wood. Test only a few at a time, on separate days, and note the weather. A cool green accord can seem bracing in winter and relieving in summer. The useful purchase is the one that fits how you actually want to feel, not the one with the most unusual note list.</p></section>
<section class="article-faq"><h2>Violet leaf questions</h2><h3>Does violet leaf smell like violet sweets?</h3><p>Usually no. That sweet powdery effect belongs more to violet-flower accords. The leaf is greener, cooler and sometimes cucumber-like.</p><h3>Is violet leaf a masculine note?</h3><p>No note has a fixed gender. In woody or leathery blends it can feel austere; with florals and musk it can feel delicate. Choose by the composition you enjoy.</p><h3>Is violet leaf the same as iris?</h3><p>No. Both can appear in elegant, powdery fragrances, but violet leaf's signature is green and watery. Iris or orris often contributes a dry, cosmetic or root-like quality.</p></section>
<section class="source-note"><h2>Sources and image note</h2><p>Odour description was checked against <a href="https://www.perfumerflavorist.com/flavor/ingredients/article/21860884/ez-26-nonadienal">Perfumer &amp; Flavorist's ingredient note on violet leaf aldehyde</a>. Pairing, testing and comparison advice is by.foro editorial analysis. The image is a fictional, unbranded editorial scene created for this guide.</p></section>
<div class="article-end"><span>End</span><p>Published by by.foro Editorial on 25 September 2026. For corrections, contact <a href="mailto:hello@byforo.com">hello@byforo.com</a>.</p></div>
""",
    },
    {
        "slug": "picture-light-small-art", "department": "home", "topic": "living-rooms",
        "title": "A Picture Light Can Make Small Art Feel Important",
        "seo": "Picture Light for Small Art: Size, Position and Warmth",
        "description": "Choose a picture light for a small painting or print with practical advice on width, mounting, glare, colour temperature and battery versus wired fittings.",
        "deck": "The right light gives a modest frame presence without turning the wall into a gallery set.",
        "alt": "Slim brass picture light illuminating a small framed artwork above a dark wood sideboard in a warm sitting room",
        "image_source": "exec-d84d90b7-2a32-48ed-850f-e9df0bcaeaa8.png",
        "inline_sources": [
            ("exec-525f5dec-9a9d-4aac-907a-ac832c313a8c.png", "small-print", "Small abstract print evenly illuminated by a slim brass picture light above a walnut sideboard"),
            ("exec-b92cd082-4897-48d8-bab0-534df6cfa996.png", "reading-nook", "Bronze picture light over a modest framed landscape in a warm reading nook"),
        ],
        "keywords": ["picture light for small art", "picture light for small painting", "what size picture light for art", "how high to hang a picture light"],
        "body": """
<p class="article-opening">For a small artwork, choose a picture light that looks proportional to the frame and spreads light across the whole image. Begin with a fitting roughly half to two-thirds as wide as the framed piece, then check the maker's beam and mounting guidance. Position and angle matter as much as width: the light should reveal the art without shining into seated eyes or producing a bright patch at the top.</p>
<p>A picture light also changes the hierarchy of a room. A modest print above a sideboard can feel deliberate at night, when the rest of the wall recedes. That makes it a useful finishing layer for a <a href="/blogs/home/reading-nook-ideas/">reading nook</a> or a quiet corner of a living room.</p>
<div class="summary-box" id="answer"><p class="kicker">The short answer</p><h2>Size for the artwork, then test the beam</h2><p>Start with a light around half to two-thirds of the frame width. Use a warm white source around 2700–3000K for a living room, if the fitting allows it. Hold the light in place temporarily and check the artwork from standing and seated positions before drilling or fixing the mount.</p></div>
<section id="size"><h2>What size picture light suits small art?</h2><p>Visual Comfort recommends roughly half to two-thirds of the artwork's width; Lumens gives a broader two-thirds to three-quarters guideline on one of its picture-light guides. Those are starting proportions, not a rule to follow against what you see. A wide beam can cover art with a smaller-looking fitting, while a narrow beam can leave the corners dark even when the metal bar looks correctly sized.</p><p>Measure the outer frame, including the moulding. Tape a paper strip the proposed width above it and step back. If the strip looks wider than the picture's visual weight, choose a slimmer bar or a less prominent finish. For very small pieces, a directional wall spotlight may be easier to proportion than a conventional horizontal picture light.</p></section>
<section id="position"><h2>Find the right height and angle</h2><p>Manufacturers give different mounting distances because fixture arms and optics differ. Lumens suggests around four to six inches above the frame on one guide. Treat the fitting's own instructions as decisive and test the light before making holes. Aim for an even wash from top to bottom, then sit in the chairs from which the work will be seen.</p><p>Glass and glossy paint can reflect a visible light source. A deeper arm, a different tilt or a slightly lower output may fix the glare. If the artwork is valuable or light-sensitive, consult a conservator about exposure rather than assuming any domestic LED setting is harmless.</p></section>
<section id="power"><h2>Battery, plug-in or hardwired?</h2><h3>Battery</h3><p>Good for a rental or a wall where wiring is impractical. Check how the unit charges, how easily it detaches and whether brightness fades as the battery runs down. A rechargeable fitting is convenient only if taking it down does not disturb the artwork.</p><h3>Plug-in</h3><p>Useful when a socket is near a sideboard or shelving. Plan the cable route as part of the composition; a visible cord can be neat when it follows a wall edge rather than crossing empty space.</p><h3>Hardwired</h3><p>The cleanest look for a permanent display, but installation belongs in the room's electrical plan. Use a qualified electrician where required, and confirm the fixture's dimensions before placing an outlet box.</p><p>The broader lesson is the same as <a href="/blogs/home/coffee-table-styling-that-looks-collected/">styling a collected coffee table</a>: give one object a clear role instead of adding several decorative signals at once.</p></section>
<section id="colour"><h2>Choose light quality before the metal finish</h2><p>Warm white around 2700–3000K usually sits comfortably with residential lamps; Lumens recommends that range for picture lights. Visual Comfort advises a high colour-rendering index, around CRI 90 or above, when accurate art colour matters. Dimming lets the art remain a focus without becoming the brightest object in the room.</p><p>Brass, bronze and black can each work. Repeat the finish once nearby if you want the fitting to feel integrated, or let it stand alone if the room already mixes metals. Avoid matching every handle, frame and lamp mechanically. The small pool of light should do more work than the metal bar.</p></section>
<section id="layout"><h2>Make the wall composition work in daylight too</h2><p>The fixture becomes a visible horizontal line even when it is switched off. Before installing, stand back and look at the relationship between the bar, frame and furniture below. A tiny print in a very large field of wall can still feel lost if the light is the only other object nearby. A sideboard, chair or narrow shelf can anchor the grouping without filling every gap.</p><p>Keep enough air between the frame and the furniture for the picture to read as its own piece. If a table lamp sits directly below, switch both lights on together; two bright pools in the same small area can flatten the art. A dimmer or a lower-output picture light can restore the hierarchy.</p><p>For a pair of small works, decide whether they are one composition or two. A single wide light may illuminate both unevenly, while two miniature bars can make the wall busy. Mock up both options with paper strips and photographs taken from the doorway. The doorway view is often more revealing than a close inspection from the sideboard.</p></section>
<section class="article-faq"><h2>Picture light questions</h2><h3>Can a picture light be wider than the art?</h3><p>It can, but the fixture may dominate a small frame. Test the actual width on the wall and check the beam; a smaller or more discreet spotlight may work better.</p><h3>How high should it sit above the frame?</h3><p>Follow the specific product's instructions. A few inches above the top edge is common, but arm projection and beam angle change the result.</p><h3>Will an LED picture light damage art?</h3><p>LEDs usually produce less heat and ultraviolet exposure than older lamps, but sensitive or valuable works need individual conservation advice and controlled exposure.</p></section>
<section class="source-note"><h2>Sources and image note</h2><p>Fixture sizing and colour guidance were checked against <a href="https://www.visualcomfort.com/us/c/wall/picture">Visual Comfort's picture-light guidance</a> and <a href="https://www.lumens.com/picture-and-display-lights/design/">Lumens' display-light guide</a>. Installation and composition advice is by.foro editorial analysis. The image shows a fictional interior created for this guide.</p></section>
<div class="article-end"><span>End</span><p>Published by by.foro Editorial on 25 September 2026. For corrections, contact <a href="mailto:hello@byforo.com">hello@byforo.com</a>.</p></div>
""",
    },
]


def make_body(story: dict) -> str:
    body = story["body"].strip()
    headings = re.findall(r'<section id="([^"]+)"><h2>(.*?)</h2>', body)
    aside = '<aside class="article-aside"><p class="kicker">In this guide</p><ol><li><a href="#answer">The short answer</a></li>'
    aside += "".join(f'<li><a href="#{anchor}">{html.escape(re.sub("<.*?>", "", title))}</a></li>' for anchor, title in headings)
    aside += '</ol><button class="copy-link" data-copy-link type="button">Copy link</button></aside>'
    for index, (_, name, alt) in enumerate(story["inline_sources"]):
        root = f'/assets/images/blogs/{story["department"]}/{story["slug"]}/{name}'
        figure = (f'<figure class="media article-inline-image"><picture><source type="image/webp" '
                  f'srcset="{root}-640.webp 640w, {root}-960.webp 960w, {root}.webp 1536w" '
                  f'sizes="(max-width: 760px) 90vw, 760px"><img src="{root}.jpg" width="1536" height="1024" '
                  f'loading="lazy" decoding="async" alt="{html.escape(alt)}"></picture></figure>')
        sections = list(re.finditer(r'</section>', body))
        if len(sections) > index + 1:
            pos = sections[index + 1].end()
            body = body[:pos] + figure + body[pos:]
    return f'<div class="article-layout">{aside}<div class="article-body">{body}</div></div>'


def main() -> None:
    catalogue_path = ROOT / "content/articles.json"
    catalogue = json.loads(catalogue_path.read_text(encoding="utf-8"))
    additions = []
    for story in STORIES:
        slug, department = story["slug"], story["department"]
        url = f"/blogs/{department}/{slug}/"
        hero = f"/assets/images/blogs/{department}/{slug}/{slug}-hero"
        image_dir = ROOT / hero.lstrip("/").rsplit("/", 1)[0]
        image_dir.mkdir(parents=True, exist_ok=True)
        images = [(story["image_source"], hero)] + [
            (source, f"/assets/images/blogs/{department}/{slug}/{name}")
            for source, name, _ in story["inline_sources"]
        ]
        for source_name, stem in images:
            with Image.open(SOURCE / source_name) as source:
                image = source.convert("RGB").resize((1536, 1024), Image.Resampling.LANCZOS)
                image.save(ROOT / f"{stem.lstrip('/')}.jpg", quality=86, optimize=True)
                image.save(ROOT / f"{stem.lstrip('/')}.webp", quality=82, method=6)
                for width in (640, 960):
                    resized = image.resize((width, round(width * 2 / 3)), Image.Resampling.LANCZOS)
                    resized.save(ROOT / f"{stem.lstrip('/')}-{width}.webp", quality=80, method=6)
        body = make_body(story)
        words = len(re.findall(r"\b[\w’-]+\b", re.sub(r"<[^>]*>", " ", body)))
        page = base.page(url, story["seo"], story["title"], story["description"], story["deck"],
                         department.title(), story["topic"].replace("-", " ").title(), hero,
                         story["alt"], body, "BlogPosting", words, story["keywords"])
        dest = ROOT / url.strip("/") / "index.html"
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(page, encoding="utf-8", newline="\n")
        additions.append({
            "title": story["title"], "seoTitle": story["seo"], "department": department,
            "topic": story["topic"], "published": "2026-09-25",
            "readingMinutes": max(1, round(words / 195)), "readingWordsPerMinute": 195,
            "url": url, "excerpt": story["deck"], "metaDescription": story["description"],
            "image": {"webp": f"{hero}.webp", "fallback": f"{hero}.jpg", "alt": story["alt"], "width": 1536, "height": 1024},
            "articleSection": story["topic"].replace("-", " ").title(), "breadcrumbTopic": True,
        })
        print(url, words)
    urls = {x["url"] for x in additions}
    catalogue_path.write_text(json.dumps(additions + [x for x in catalogue if x["url"] not in urls],
                                         ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
