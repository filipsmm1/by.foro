"""Strengthen the by.foro pages already earning Google impressions.

This is intentionally a focused refresh rather than a new-article generator.
It expands weak intent coverage, preserves pages that already rank well and
adds contextual links into the two culture opportunities.
"""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


LITERARY_SECTION = """<!-- SEARCH-OPPORTUNITY:LITERARY-COMPARISON:START -->
<section id="literary-chic-vs-dark-academia" data-reveal><h2>Literary chic vs dark academia: what is the difference?</h2><p>Literary chic is a way of styling clothes. Dark academia is a broader visual world with collegiate architecture, Gothic references, sepia palettes and a stronger sense of character. The two can share loafers, tailoring, shirts and old leather, but literary chic needs fewer signals. It can include a pale blue shirt, clean black trouser and silver watch without using brown tweed, a tie or anything that looks borrowed from a school uniform.</p><p>The distinction is useful when an outfit begins to feel theatrical. Keep the literary line, then remove the period clues. Exchange a crest knit for a plain cardigan, a novelty satchel for a modern leather bag or a full tweed suit for one dry-wool jacket. The result should suggest that books belong to the person wearing the clothes, not that the clothes were selected to prove an interest in books.</p><div class="article-table-wrap" role="region" aria-label="Literary chic and dark academia compared" tabindex="0"><table class="article-visual-table"><thead><tr><th>Detail</th><th>Literary chic</th><th>Dark academia</th></tr></thead><tbody><tr><td>Starting point</td><td>Useful wardrobe pieces</td><td>A complete visual atmosphere</td></tr><tr><td>Palette</td><td>Ink, cream, grey, tobacco, oxblood</td><td>Brown, black, forest green, parchment</td></tr><tr><td>Best moderniser</td><td>Clean denim, a technical coat or sharp bag</td><td>A contemporary shoe or simplified layer</td></tr><tr><td>Main risk</td><td>Looking over-styled</td><td>Looking like period costume</td></tr></tbody></table></div><p>A simple test works in daylight: remove the library setting from the picture. If the clothes still make sense on a train, at work and over dinner, the reference has been translated into personal style.</p></section>
<!-- SEARCH-OPPORTUNITY:LITERARY-COMPARISON:END -->"""


ART_DECO_SECTION = """<!-- SEARCH-OPPORTUNITY:NEO-DECO:START -->
<section id="neo-deco" data-reveal><h2>Art Deco revival vs Neo Deco: the useful difference</h2><p><em>Art Deco</em> names a historical design movement. <em>Neo Deco</em> is a contemporary label for work that borrows its geometry, polish and theatrical lighting without claiming to reproduce the 1920s or 1930s. The difference is not a strict academic border, but it is a useful search and shopping distinction. An original lacquer cabinet with documented period provenance belongs to design history. A new fluted-glass sconce with a stepped silhouette is better described as Deco-inspired or Neo Deco.</p><p>In Art Deco interior design, the modern shift is usually visible in scale and restraint. Historic rooms could coordinate architecture, furniture, textiles and objects as a total scheme. A current living room is more convincing when one curved seat, one geometric light and an existing plain sofa share the space. Contemporary performance matters too. New lighting should meet present electrical standards, seating should support ordinary use and a reproduction cabinet should be judged by its construction rather than an applied sunburst.</p><p>Art Deco fashion follows the same rule. A velvet column dress with a geometric cuff reads as a current evening look. Adding finger waves, a beaded cap, opera gloves and a period shoe turns the reference into costume. Neo Deco keeps the line and removes the reenactment.</p><p>This distinction also opens the trend beyond the familiar black-and-gold palette. Cream lacquer, smoked glass, nickel, pale peach, dark timber and mineral blue can carry Deco structure without repeating the visual shorthand of a themed restaurant. Look for the principle behind the reference: symmetry, a stepped profile, a controlled curve or ornament that follows construction.</p></section>
<!-- SEARCH-OPPORTUNITY:NEO-DECO:END -->"""


SKIN_CONCENTRATION = """<!-- SEARCH-OPPORTUNITY:SKIN-CONCENTRATION:START -->
<section id="projection-longevity" data-reveal><h2>Projection, longevity and concentration are not the same</h2><p>Three separate qualities are often collapsed into the word <em>strength</em>. Projection is how far the scent travels. Longevity is how long it remains detectable. Concentration describes the proportion and format of aromatic material in a particular formula. An eau de parfum can stay close, while an eau de toilette can create a brighter opening that travels farther for a shorter time. The label alone cannot predict the wearing experience.</p><p>Skin scents are usually designed around a small scent bubble, but that does not excuse an empty dry-down. Check the perfume at three distances: directly above the skin, at normal conversational distance and on clothing the following morning if the formula is fabric-safe. A useful intimate perfume still changes over time. It may move from a bright opening to musk, iris or pale wood while keeping its volume low.</p><div class="article-table-wrap" role="region" aria-label="Perfume projection longevity and concentration explained" tabindex="0"><table class="article-visual-table"><thead><tr><th>Measure</th><th>The question it answers</th><th>How to test it</th></tr></thead><tbody><tr><td>Projection</td><td>How far does it travel?</td><td>Ask someone at conversational distance after one hour</td></tr><tr><td>Longevity</td><td>How long is it detectable?</td><td>Check without respraying at two, four and eight hours</td></tr><tr><td>Development</td><td>Does the smell change well?</td><td>Compare the opening, middle and final dry-down</td></tr><tr><td>Concentration</td><td>What format did the brand formulate?</td><td>Use it as context, not a performance guarantee</td></tr></tbody></table></div></section>
<!-- SEARCH-OPPORTUNITY:SKIN-CONCENTRATION:END -->"""


SKIN_CHEMISTRY = """<!-- SEARCH-OPPORTUNITY:SKIN-CHEMISTRY:START -->
<section id="skin-chemistry" data-reveal><h2>What skin chemistry really changes</h2><p>Perfume does not become a completely different formula on every person, but the wearing conditions do change. Skin temperature, moisture, application site, weather and scented body products affect evaporation and what the wearer notices. A fragrance tested on a cool wrist in a shop may feel softer at the warm collarbone during a commute. A vanilla body cream underneath can also change the impression even when the perfume itself has not changed.</p><p>Run a controlled test before declaring that a scent does not work with your chemistry. Wear it once on clean, bare skin with no fragranced lotion. On another day, repeat the same number of sprays in similar weather. If the result is consistently flat, sharp or too faint, trust the pattern. Comparing six perfumes across both arms in one visit creates more noise than evidence.</p><p>Perception matters as much as evaporation. Repeated exposure can reduce perceived intensity, a form of olfactory adaptation documented in smell research. A perfume may appear to vanish because the wearer has been inside its scent bubble for hours. The practical response is not immediate overspraying. Step into unscented air, wait, then ask another person whether the perfume remains noticeable. The <a href="https://pubmed.ncbi.nlm.nih.gov/24500750/" target="_blank" rel="noopener noreferrer">published research on perceptual odour adaptation and recovery</a> supports treating temporary loss of perception as a real sensory effect rather than automatic proof of poor longevity.</p></section>
<!-- SEARCH-OPPORTUNITY:SKIN-CHEMISTRY:END -->"""


SKIN_TROUBLESHOOT = """<!-- SEARCH-OPPORTUNITY:SKIN-TROUBLESHOOT:START -->
<section id="troubleshoot" data-reveal><h2>Why a skin scent disappears and what to change</h2><h3>It disappears in the first hour</h3><p>Test fewer variables before using more perfume. Apply the scent to one unscented, moisturised area and leave another spray on a paper strip nearby. If both are empty after an hour, the formula may simply be too fleeting for what you want. If the strip remains clear while the skin seems blank, heat, application position or sensory adaptation may be shaping the result.</p><h3>You can smell it only with your nose against your wrist</h3><p>Ask for a second opinion at normal distance. If nobody else can detect it, try the collarbone or back of the neck, where warmth and movement can create a small trail. Do not chase projection by spraying the same wrist repeatedly. A deliberately quiet construction may become denser without travelling farther.</p><h3>It turns sharp, sweet or dusty</h3><p>Remove other scented products and test in different weather. Clean musks can feel severe in dry cold, while milky and amber notes can become dense in heat. The issue may be the family rather than the entire skin-scent category. Move from laundry musk to iris and tea, or from sweet ambrette to mineral woods.</p><h3>It lasts, but you no longer enjoy the dry-down</h3><p>Longevity is not automatically quality. A long-lasting base that feels scratchy, metallic or monotonous is still a poor match. Judge the final four hours more strictly than the first ten minutes. This is why discovery samples and travel sizes are more informative than a quick counter spray.</p></section>
<!-- SEARCH-OPPORTUNITY:SKIN-TROUBLESHOOT:END -->"""


SKIN_SAFETY = """<!-- SEARCH-OPPORTUNITY:SKIN-SAFETY:START -->
<section id="safety" data-reveal><h2>Skin scent does not mean hypoallergenic</h2><p>A close-wearing perfume is not automatically gentler than a projecting one. <em>Skin scent</em>, <em>clean</em> and <em>hypoallergenic</em> are not interchangeable safety categories. The <a href="https://www.fda.gov/cosmetics/cosmetic-ingredients/fragrances-cosmetics" target="_blank" rel="noopener noreferrer">US Food and Drug Administration&rsquo;s fragrance guidance</a> notes that fragrance formulas can contain many ingredients and that some people may be allergic or sensitive to particular components. The agency also explains that ingredients may sometimes appear under the collective label &ldquo;fragrance&rdquo; in the United States.</p><p>Use the product according to its label, avoid broken or irritated skin and stop if redness, itching, swelling or breathing symptoms appear. Anyone with a known fragrance allergy should discuss testing and ingredient avoidance with a qualified clinician rather than relying on marketing language. Industry standards are useful background, but they are not a personal allergy test. The <a href="https://ifrafragrance.org/initiatives-positions/safe-use-fragrance-science/ifra-standards/ifra-code-of-practice" target="_blank" rel="noopener noreferrer">International Fragrance Association Code of Practice</a> describes how member companies apply ingredient restrictions and safety standards.</p><p>Storage is part of sensible use. Keep the bottle away from direct sun, repeated heat and steam, with the cap secure. A bathroom shelf may look beautiful, but a stable bedroom drawer or shaded cabinet is usually the more dependable place for a fragrance you want to keep.</p></section>
<!-- SEARCH-OPPORTUNITY:SKIN-SAFETY:END -->"""


def replace_once(text: str, old: str, new: str, label: str) -> str:
    if old not in text:
        raise RuntimeError(f"Missing replacement anchor: {label}")
    return text.replace(old, new, 1)


def update_catalogue() -> None:
    path = ROOT / "content" / "articles.json"
    articles = json.loads(path.read_text(encoding="utf-8"))
    changes = {
        "/blogs/fashion/literary-chic-without-the-costume/": {
            "updated": "2026-08-10",
            "seoTitle": "Literary Chic Outfits: How to Wear the Trend in 2026",
            "metaDescription": "Build literary chic outfits with a five-piece formula, modern proportions and tactile fabrics, plus the difference between literary chic and dark academia.",
            "excerpt": "A practical literary chic outfit formula, with modern proportions, tactile fabrics and the difference between literary chic and dark academia.",
        },
        "/blogs/culture/art-deco-revival/": {
            "updated": "2026-08-10",
            "excerpt": "The Art Deco revival across fashion and interiors, including the useful difference between historical Art Deco and contemporary Neo Deco.",
        },
        "/blogs/beauty/skin-scent-perfume-guide/": {
            "updated": "2026-08-10",
            "metaDescription": "Learn what skin scent perfume means, how projection differs from longevity, which notes to choose, how to test it and why a close fragrance can disappear.",
            "excerpt": "What skin scent perfume means, how projection differs from longevity, which notes to choose and how to troubleshoot a close-wearing fragrance.",
        },
    }
    seen = set()
    for article in articles:
        if article["url"] in changes:
            article.update(changes[article["url"]])
            seen.add(article["url"])
    missing = set(changes) - seen
    if missing:
        raise RuntimeError(f"Catalogue entries not found: {sorted(missing)}")
    path.write_text(
        json.dumps(articles, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
        newline="\n",
    )


def update_literary() -> None:
    path = ROOT / "blogs" / "fashion" / "literary-chic-without-the-costume" / "index.html"
    text = path.read_text(encoding="utf-8")
    if "SEARCH-OPPORTUNITY:LITERARY-COMPARISON" not in text:
        text = replace_once(
            text,
            '<li><a href="#modern">Keep it contemporary</a></li>',
            '<li><a href="#modern">Keep it contemporary</a></li><li><a href="#literary-chic-vs-dark-academia">Literary chic vs dark academia</a></li>',
            "literary contents",
        )
        text = replace_once(
            text,
            '<section id="avoid-costume" data-reveal>',
            f'{LITERARY_SECTION}\n<section id="avoid-costume" data-reveal>',
            "literary section",
        )
    path.write_text(text, encoding="utf-8", newline="\n")


def update_art_deco_page() -> None:
    path = ROOT / "blogs" / "culture" / "art-deco-revival" / "index.html"
    text = path.read_text(encoding="utf-8")
    if "SEARCH-OPPORTUNITY:NEO-DECO" not in text:
        text = replace_once(
            text,
            '<li><a href="#use">How to use Deco now</a></li>',
            '<li><a href="#neo-deco">Art Deco vs Neo Deco</a></li><li><a href="#use">How to use Deco now</a></li>',
            "Art Deco contents",
        )
        text = replace_once(
            text,
            '<section id="use" data-reveal>',
            f'{ART_DECO_SECTION}\n<section id="use" data-reveal>',
            "Art Deco section",
        )
    path.write_text(text, encoding="utf-8", newline="\n")


def update_skin_scent() -> None:
    path = ROOT / "blogs" / "beauty" / "skin-scent-perfume-guide" / "index.html"
    text = path.read_text(encoding="utf-8")
    if "SEARCH-OPPORTUNITY:SKIN-CONCENTRATION" in text:
        path.write_text(text, encoding="utf-8", newline="\n")
        return
    text = replace_once(
        text,
        '<li><a href="#types">Notes and types</a></li><li><a href="#test">How to test one</a></li><li><a href="#wear">How to wear it</a></li><li><a href="#choose">How to choose</a></li><li><a href="#faq">FAQ</a></li>',
        '<li><a href="#projection-longevity">Projection and longevity</a></li><li><a href="#types">Notes and types</a></li><li><a href="#skin-chemistry">Skin chemistry</a></li><li><a href="#test">How to test one</a></li><li><a href="#wear">How to wear it</a></li><li><a href="#troubleshoot">Troubleshooting</a></li><li><a href="#choose">How to choose</a></li><li><a href="#safety">Safety and sensitivity</a></li><li><a href="#faq">FAQ</a></li>',
        "skin scent contents",
    )
    text = replace_once(
        text,
        '<section id="types" data-reveal>',
        f'{SKIN_CONCENTRATION}\n<section id="types" data-reveal>',
        "skin concentration section",
    )
    text = replace_once(
        text,
        '<section id="test" data-reveal>',
        f'{SKIN_CHEMISTRY}\n<section id="test" data-reveal>',
        "skin chemistry section",
    )
    text = replace_once(
        text,
        '<section id="choose" data-reveal>',
        f'{SKIN_TROUBLESHOOT}\n<section id="choose" data-reveal>',
        "skin troubleshoot section",
    )
    text = replace_once(
        text,
        '<section id="faq" data-reveal>',
        f'{SKIN_SAFETY}\n<section id="faq" data-reveal>',
        "skin safety section",
    )
    path.write_text(text, encoding="utf-8", newline="\n")


def add_contextual_links() -> None:
    celebrity = ROOT / "blogs" / "fashion" / "celebrity-style-is-getting-personal" / "index.html"
    text = celebrity.read_text(encoding="utf-8")
    link = '/blogs/culture/ariana-grande-petal-meaning/'
    if link not in text:
        old = "A celebrity can reference a film, album or role without arriving in costume. The smarter approach is translation: a colour from the project, a silhouette that nods to the character, a vintage piece that extends the mood."
        new = old + ' Ariana Grande&rsquo;s <a href="/blogs/culture/ariana-grande-petal-meaning/"><em>Petal</em> era</a> shows the same process in music: a restrained visual code can carry a much more confrontational argument.'
        text = replace_once(text, old, new, "Petal contextual link")
        celebrity.write_text(text, encoding="utf-8", newline="\n")

    glamoratti = ROOT / "blogs" / "fashion" / "glamoratti-style-2026" / "index.html"
    text = glamoratti.read_text(encoding="utf-8")
    link = '/blogs/culture/art-deco-revival/'
    if link not in text:
        old = "Gold jewellery acknowledges decoration instead of pretending a watch is purely functional. It is not a rejection of good basics. It is a reminder that good basics can support theatre."
        new = old + ' That exchange between disciplined structure and visible glamour also explains the current <a href="/blogs/culture/art-deco-revival/">Art Deco revival across fashion and interiors</a>.'
        text = replace_once(text, old, new, "Art Deco contextual link")
        glamoratti.write_text(text, encoding="utf-8", newline="\n")


def main() -> None:
    update_catalogue()
    update_literary()
    update_art_deco_page()
    update_skin_scent()
    add_contextual_links()
    print("Focused Search Console opportunity refresh applied.")


if __name__ == "__main__":
    main()
