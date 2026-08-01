"""Build the by.foro brooch styling feature."""

from __future__ import annotations

import json
from pathlib import Path

from refresh_site import ROOT, site_footer, site_header


URL = "/blogs/fashion/how-to-wear-brooches/"
CANONICAL = f"https://byforo.com{URL}"
TITLE = "Brooches Are Back: 17 Modern Ways to Wear Them in 2026"
SEO_TITLE = "How to Wear Brooches in 2026: 17 Modern Styling Ideas"
DESCRIPTION = (
    "Discover 17 modern ways to wear brooches on blazers, shirts, scarves, denim, "
    "bags and shoes, plus the styling mistakes that can make them look dated."
)
IMAGE_ROOT = "/assets/images/blogs/fashion/how-to-wear-brooches"
HERO = f"{IMAGE_ROOT}/how-to-wear-brooches-hero"


def picture(name: str, alt: str, caption: str) -> str:
    base = f"{IMAGE_ROOT}/{name}"
    return f'''<figure class="media article-inline-image article-inline-image--portrait">
<picture><source type="image/webp" srcset="{base}-640.webp 640w, {base}-960.webp 960w, {base}.webp 1200w" sizes="(max-width: 760px) calc(100vw - 2rem), 680px"><img src="{base}.jpg" width="1200" height="1500" loading="lazy" decoding="async" alt="{alt}"></picture>
<figcaption>{caption}</figcaption></figure>'''


article_schema = {
    "@context": "https://schema.org",
    "@type": "BlogPosting",
    "mainEntityOfPage": {"@type": "WebPage", "@id": CANONICAL},
    "headline": TITLE,
    "description": DESCRIPTION,
    "image": [f"https://byforo.com{HERO}.jpg"],
    "datePublished": "2026-08-01T13:15:00+02:00",
    "dateModified": "2026-08-01T13:15:00+02:00",
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
    "articleSection": "Accessories",
    "keywords": [
        "how to wear brooches",
        "brooch styling ideas",
        "brooch trend 2026",
        "modern ways to wear brooches",
        "brooch outfit ideas",
    ],
    "inLanguage": "en-GB",
    "isAccessibleForFree": True,
    "wordCount": 2900,
}

breadcrumb_schema = {
    "@context": "https://schema.org",
    "@type": "BreadcrumbList",
    "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": "Home", "item": "https://byforo.com/"},
        {"@type": "ListItem", "position": 2, "name": "Fashion", "item": "https://byforo.com/fashion/"},
        {
            "@type": "ListItem",
            "position": 3,
            "name": "Accessories",
            "item": "https://byforo.com/journal/?department=fashion&topic=accessories",
        },
        {"@type": "ListItem", "position": 4, "name": "How to Wear Brooches", "item": CANONICAL},
    ],
}


body = f'''<main id="main"><article class="article"><header class="article-hero"><nav class="breadcrumbs" aria-label="Breadcrumb"><a href="/">Home</a><span>/</span><a href="/fashion/">Fashion</a><span>/</span><a href="/journal/?department=fashion&amp;topic=accessories">Accessories</a><span>/</span><span aria-current="page">How to Wear Brooches</span></nav><p class="kicker">Fashion &middot; Accessories</p><h1>{TITLE}</h1><p class="article-deck">The brooch has moved on from the polite left lapel. The modern version lands on denim, ties, silk, waistbands and shoes, where it looks personal rather than ceremonial.</p><div class="article-meta"><a class="article-byline" href="/about/" rel="author">by.foro Editorial</a><time datetime="2026-08-01">1 August 2026</time><span>15 min read</span></div></header>
<figure class="media article-hero-image"><picture><source type="image/webp" srcset="{HERO}-640.webp 640w, {HERO}-960.webp 960w, {HERO}.webp 1536w" sizes="(max-width: 760px) calc(100vw - 2rem), 93vw"><img src="{HERO}.jpg" width="1536" height="1024" loading="eager" fetchpriority="high" decoding="async" alt="Three antique-style brooches arranged on an oversized charcoal blazer with an oxblood scarf"></picture><figcaption>Formal jewellery, ordinary clothes: the contrast that makes a brooch feel current.</figcaption></figure>
<div class="article-layout"><aside class="article-aside"><p class="kicker">In this guide</p><ol><li><a href="#quick-answer">Are brooches in style?</a></li><li><a href="#why-now">Why they are back</a></li><li><a href="#principles">Four modern rules</a></li><li><a href="#ideas">17 styling ideas</a></li><li><a href="#placement-map">Placement map</a></li><li><a href="#choose">Choosing a brooch</a></li><li><a href="#mistakes">What looks dated</a></li><li><a href="#care">Protecting clothes</a></li><li><a href="#faq">Questions answered</a></li></ol><button class="copy-link" data-copy-link type="button">Copy link</button></aside>
<div class="article-body"><p class="article-opening">The brooch has escaped the blazer lapel. In 2026, it is being pinned to ties, shirt collars, denim, silk scarves, waistbands and shoes, turning familiar clothes into something personal and slightly strange. The useful question is no longer whether brooches are back. It is how to wear brooches without allowing the rest of the outfit to drift into costume.</p>
<p>Pinterest named the wider movement &ldquo;Brooched&rdquo; in its forecast published on 9 December 2025. The platform reported growth in searches for brooch aesthetics, maximalist accessories, lapel shirts, brooches for men&rsquo;s suits and heirloom jewellery. Those numbers describe Pinterest activity during its own analysis period, not fashion as a whole, but the pattern is clear: people are looking for placement ideas, personal objects and accessories that do more than finish an outfit politely.</p>

<div class="brooch-quick-answer" id="quick-answer"><p class="kicker">Quick answer</p><h2>Are brooches in style in 2026?</h2><p>Yes. Brooches are one of 2026&rsquo;s clearest accessory revivals, supported by renewed interest in maximalist accessories, heirloom jewellery and individual styling. The modern approach is less formal than before. Instead of automatically placing one small pin on a blazer, wearers are clustering several pieces or attaching them to shirts, ties, denim, scarves, handbags, hats and removable shoe clips.</p></div>

<section id="why-now" data-reveal><h2>Why brooches are back in fashion</h2>
<p>The return makes sense after several seasons of anonymous minimalism. A plain coat, clean trouser and unmarked bag can be useful, but a wardrobe built entirely from discretion starts to lose evidence of its owner. A brooch restores specificity without requiring another garment. It can carry a family story, make a second-hand jacket feel singular or add wit to a shirt that has already earned its keep.</p>
<p>The official <a href="https://business.pinterest.com/en-gb/pinterest-predicts/">Pinterest Predicts 2026 report</a> lists &ldquo;brooch aesthetic&rdquo; at +110%, &ldquo;maximalist accessories&rdquo; at +105%, &ldquo;lapel shirt&rdquo; at +95%, &ldquo;brooch for men suit&rdquo; at +90% and &ldquo;heirloom jewellery&rdquo; at +45%. British Vogue&rsquo;s <a href="https://www.vogue.co.uk/gallery/jewellery-trend-brooches-aw26">3 March 2026 runway report</a> then traced brooches across autumn collections, from Giorgio Armani tailoring and Ralph Lauren pashminas to Ulla Johnson shoulders and Oscar Ouyang belt loops. Prediction had become visible styling.</p>
</section>

<section id="principles" data-reveal><h2>How to wear brooches without looking dated</h2>
<h3>Treat the brooch as contrast</h3><p>A crystal brooch looks newer against washed denim than beside a satin blouse, pearl earrings and a fitted formal jacket. This is the most reliable rule in the guide: the more formal the brooch, the more ordinary the garment should be. Pearl on a white T-shirt, Art Deco geometry on a masculine shirt and an animal pin on a broad wool coat all work because the object interrupts the outfit rather than completing a familiar set.</p>
<h3>Change the expected placement</h3><p>The traditional left lapel is not wrong. It simply needs a modern context. Moving the piece to a collar, pocket, waist or scarf removes inherited rules and makes the eye look twice. British Vogue&rsquo;s earlier study of the revival documented brooches on <a href="https://www.vogue.co.uk/article/brooches-trend">collars, belts, bags, hips, wrists and chains</a>. The range is the point.</p>
<h3>Repeat one detail, not every detail</h3><p>Connect the brooch to one colour, material or shape elsewhere. An oxblood enamel flower can answer a dark-red sock. A silver geometric pin can pick up the buckle of a black loafer. Stop there. Matching brooch, earrings, necklace and bracelet turns a visual echo into a jewellery suite.</p>
<h3>Choose one statement or a deliberate cluster</h3><p>One oversized piece reads as controlled. Three to seven smaller pieces can look collected if they share metal, motif or colour. Two medium brooches placed without a relationship often look accidental. Before pinning, arrange a cluster on a table and photograph it. The phone image reveals gaps and awkward tangents more quickly than the mirror.</p>
<div class="brooch-rule"><strong>The Formality Contrast Rule</strong><p>The more formal the brooch, the more ordinary the garment should be. Put crystal on denim, pearls on cotton and elaborate gold on dry wool. Let the contrast do the modernising.</p></div></section>

<section id="ideas" data-reveal><h2>17 modern ways to wear brooches in 2026</h2>
<h3><span class="number">01</span>On an oversized blazer</h3><p>Pin a sculptural brooch high on a broad charcoal lapel, then keep the inner layer relaxed. A white T-shirt, straight jeans and simple black shoe prevent the jacket from becoming corporate. Scale matters: a tiny floral pin disappears on a wide lapel, while a medium abstract piece holds its own. If the jacket already has strong buttons, choose a brooch with a different shape so the two details do not compete.</p><p class="brooch-formula"><strong>Outfit formula</strong><br>Oversized charcoal blazer + white T-shirt + straight denim + sculptural gold brooch.</p>
<h3><span class="number">02</span>High on a shirt collar</h3><p>A small brooch between or just beside the collar points gives an oversized shirt a centre of gravity. Use a lightweight piece so the collar remains crisp. A brushed-silver shape on pale blue poplin feels cleaner than a crystal cluster. Fasten through two layers if possible, and check that the pin does not touch the throat when you sit.</p><p class="brooch-formula"><strong>Outfit formula</strong><br>Pale-blue shirt + dark tailored trousers + miniature silver brooch.</p>
{picture("brooch-shirt-collar", "Small brushed-silver brooch pinned between the collar points of an oversized pale-blue shirt", "A small collar piece gives an oversized shirt a precise centre.")}
<h3><span class="number">03</span>At the knot of a necktie</h3><p>Place a compact square brooch just below the knot, not through the knot itself. The tie should remain narrow enough that the piece does not float inside a large expanse of silk. Black tie, cream shirt and brown tailoring keep the effect graphic. For valuable or delicate ties, use a purpose-made tie pin or converter rather than forcing a thick vintage needle through silk.</p><p class="brooch-formula"><strong>Outfit formula</strong><br>Cream shirt + narrow black tie + relaxed brown suit + square onyx brooch.</p>
{picture("brooch-tie-knot", "Square onyx brooch secured below a narrow black tie knot on a relaxed brown suit", "A geometric pin makes a tie feel personal rather than ceremonial.")}
<h3><span class="number">04</span>Clustered across a denim jacket</h3><p>Denim can support more weight than silk or fine knitwear, which makes it the best place to learn multiple-brooch styling. Start with five pieces in one metal family. Vary the scale and leave enough dark fabric between them for each silhouette to register. Follow the yoke or pocket seam rather than scattering them across the entire chest. The shared antique-gold tone makes a leaf, bird, dark stone and enamel dot look collected rather than random.</p><p class="brooch-formula"><strong>Outfit formula</strong><br>Dark denim jacket + white T-shirt + five antique-gold brooches with different motifs.</p>
{picture("multiple-brooch-denim", "Five different antique-gold brooches clustered across a dark indigo denim jacket", "A shared metal finish keeps five different motifs in conversation.")}
<h3><span class="number">05</span>On the shoulder of a plain knit</h3><p>A shoulder placement works particularly well on a dense crew neck because it shifts attention away from the usual lapel zone. Pin near the shoulder seam, where the knit has support, rather than in the soft centre of the chest. Avoid loosely woven cashmere and open stitches. If the jumper sags after ten minutes, the brooch is too heavy, however good the first photograph looked.</p><p class="brooch-formula"><strong>Outfit formula</strong><br>Charcoal crew neck + pleated dark trouser + one brushed-gold abstract brooch.</p>
{picture("brooch-knit-shoulder", "Brushed-gold sculptural brooch pinned high on the shoulder of a dense charcoal jumper", "Dense knitwear can carry a medium brooch without losing its line.")}
<h3><span class="number">06</span>Holding a silk scarf</h3><p>Let the scarf cross naturally, then pin the brooch where the two layers meet slightly off-centre. A lightweight leaf or bar is safer than a heavy crystal piece. The scarf should still drape, not bunch into a rigid knot. Cream silk with an oxblood edge, a black knit and antique gold creates enough contrast without looking like a uniform.</p><p class="brooch-formula"><strong>Outfit formula</strong><br>Cream silk scarf + fitted black knit + lightweight antique-gold brooch.</p>
{picture("brooch-silk-scarf", "Lightweight antique-gold leaf brooch securing a cream silk scarf with an oxblood border", "Pin the scarf where it crosses, not directly in the middle of the chest.")}
<h3><span class="number">07</span>On the pocket of a white shirt</h3><p>This is the quiet option for readers who dislike maximalism. Choose one small brooch and pin it to the pocket edge or just above it. The seam gives fine cotton more support and makes the placement look intentional. Leave necklaces out of the equation. A pocket brooch works because it is the only decorative interruption.</p>
<h3><span class="number">08</span>At the waist of a dress</h3><p>On a simple column dress, a brooch can mark the waist visually without pretending to hold the garment together. Place it at one side, where the line remains asymmetrical. Do not gather substantial fabric unless the fastening was designed for that load. An Art Deco fan or geometric spray brings structure to matte black cloth, while the absence of other jewellery lets the object remain the focus.</p><p class="brooch-formula"><strong>Outfit formula</strong><br>Matte black column dress + Art Deco brooch at the side waist + plain black shoes.</p>
{picture("brooch-black-dress-waist", "Art Deco-inspired silver and dark-crystal brooch placed asymmetrically at the waist of a black column dress", "At the waist, the brooch should add focus rather than carry fabric.")}
<h3><span class="number">09</span>On a belt or belt loop</h3><p>Fasten a small metal brooch to a fabric keeper, removable ribbon or belt loop rather than puncturing good leather. It can sit beside the buckle or replace the visual weight of one on a tie belt. Keep the buckle simple. Two ornate metal objects at the same point create congestion.</p>
<h3><span class="number">10</span>Along the waistband of trousers</h3><p>High-waisted tailoring gives a small brooch an architectural position. Place it slightly off-centre with a tucked fine knit or shirt. The piece should sit beside the fastening, never over it, and should not interfere with a pocket opening. A dark-red enamel leaf against charcoal is enough colour to make the placement readable.</p><p class="brooch-formula"><strong>Outfit formula</strong><br>Ivory fine knit + charcoal pleated trousers + dark-red enamel brooch.</p>
{picture("brooch-trouser-waistband", "Small dark-red enamel brooch placed beside the waistband fastening of charcoal tailored trousers", "A waistband brooch works best when the rest of the line stays clean.")}
<h3><span class="number">11</span>On a trench coat</h3><p>A trench offers two useful positions: high near the collar or on the storm flap. The latter feels less traditional and gives a small object a defined panel. Use a brooch large enough to compete with buttons and epaulettes, but avoid pinning through taped waterproof seams. On fine technical outerwear, leave the pin off entirely.</p>
<h3><span class="number">12</span>On a handbag</h3><p>Do not push a sharp pin through valuable leather. Tie a silk scarf around the handle and fasten the brooch to the scarf, or use a removable strap with woven fabric. Canvas panels may tolerate a pin, but test an inconspicuous area first. An animal brooch on an oxblood-and-cream scarf brings personality to a plain brown bag without making it look decorated at the factory.</p>
{picture("brooch-handbag-scarf", "Antique-gold animal brooch fastened to an oxblood-and-cream scarf tied around a brown handbag handle", "A handle scarf gives the brooch a safe surface and the bag a removable detail.")}
<h3><span class="number">13</span>On a beret or structured hat</h3><p>A medium brooch placed off-centre on felt or dense wool reads clearly from a distance. One piece is usually enough because the hat already frames the face. Match weight to structure: a soft, unlined beret will collapse under a heavy cluster. Check the pin tip from inside before wearing it.</p>
{picture("brooch-beret", "Abstract antique-gold brooch placed off-centre on an oxblood wool beret", "One sculptural piece is enough when the hat already carries colour and shape.")}
<h3><span class="number">14</span>On ballet flats, loafers or boots</h3><p>Use purpose-made shoe clips or brooch converters, not an ordinary open pin. The hardware should sit flat, stay clear of the foot and survive a few firm steps indoors before leaving home. Matching clips look controlled on black loafers; deliberately different pieces can work on boots if they share metal and scale. Never pierce expensive leather merely for a photograph.</p><p class="brooch-formula"><strong>Outfit formula</strong><br>Cream trousers + black loafers + removable antique-silver geometric clips.</p>
{picture("brooch-shoe-clips", "Removable antique-silver geometric shoe clips attached to black leather loafers", "Purpose-made clips give the look of brooches without puncturing leather.")}
<h3><span class="number">15</span>On a simple black dress</h3><p>The brooch should provide the main visual interest. Choose shoulder, neckline, waist or hip, then remove one other accessory. A floral piece at the shoulder softens a strict dress; geometric silver at the hip sharpens it. The mistake is filling every empty zone. Black cloth gives a brooch space precisely because it is quiet.</p>
<h3><span class="number">16</span>On a ribbon or velvet choker</h3><p>A small antique brooch can become a necklace centrepiece when secured to a broad velvet ribbon. Use a proper backing, cover the pin point completely and keep sharp edges away from skin. The ribbon should be wide enough to support the piece without twisting. This works best with an open neckline and no earrings competing nearby.</p>
<h3><span class="number">17</span>Mixed into masculine tailoring</h3><p>Treat brooches for men&rsquo;s suits as part of the same visual language, not a novelty subsection. A floral, animal or geometric piece high on a relaxed lapel adds softness or wit to tailoring. Leave the shirt open or use a plain tie, depending on the brooch. The current effect comes from ease: broad navy suit, ivory shirt, one silver botanical pin and nothing that resembles a wedding boutonni&egrave;re.</p><p class="brooch-formula"><strong>Outfit formula</strong><br>Relaxed navy double-breasted suit + open ivory shirt + single silver floral brooch.</p>
{picture("brooch-mens-suit", "Single silver floral brooch worn high on the lapel of a relaxed navy double-breasted suit", "A floral pin gives masculine tailoring specificity without turning it into occasionwear.")}</section>

<section class="brooch-placement-map" id="placement-map" data-reveal><header><h2>The by.foro placement map</h2><p>Begin with the garment&rsquo;s structure. Seams, collars, yokes and bands support weight better than unsupported fabric. The unexpected position makes the look current; the supported position keeps it wearable.</p></header><div class="brooch-placement-map__grid"><div><span>01</span><strong>Collar</strong></div><div><span>02</span><strong>Shoulder</strong></div><div><span>03</span><strong>Lapel</strong></div><div><span>04</span><strong>Tie</strong></div><div><span>05</span><strong>Cuff</strong></div><div><span>06</span><strong>Waist</strong></div><div><span>07</span><strong>Pocket</strong></div><div><span>08</span><strong>Scarf</strong></div><div><span>09</span><strong>Bag</strong></div><div><span>10</span><strong>Hat</strong></div><div><span>11</span><strong>Shoe clip</strong></div></div></section>

<section id="choose" data-reveal><h2>How to choose the right brooch for your outfit</h2>
<div class="article-table-wrap" role="region" aria-label="Brooch selection guide" tabindex="0"><table class="article-visual-table"><thead><tr><th>Outfit</th><th>Best brooch direction</th><th>Why it works</th></tr></thead><tbody><tr><td>Minimal black outfit</td><td>Large sculptural metal</td><td>One clear silhouette replaces several accessories</td></tr><tr><td>Dark denim</td><td>Colourful enamel or a coherent cluster</td><td>Dense fabric supports weight and reduces formality</td></tr><tr><td>Masculine tailoring</td><td>Geometric, animal or botanical</td><td>A specific motif interrupts the suit&rsquo;s order</td></tr><tr><td>Romantic dress</td><td>Abstract metal or restrained pearl</td><td>Contrast avoids over-sweetening the outfit</td></tr><tr><td>Patterned outfit</td><td>One simple metal brooch</td><td>A clean shape remains legible against print</td></tr><tr><td>Silk scarf</td><td>Lightweight vintage brooch</td><td>Low weight protects drape and fibre</td></tr><tr><td>Thick winter coat</td><td>Large secure statement piece</td><td>Scale holds its own beside buttons and lapels</td></tr></tbody></table></div>
<h3>Vintage, heirloom or new?</h3><p><strong>Vintage</strong> offers character and designs that are unlikely to appear twice, but the clasp needs inspection. <strong>Heirloom jewellery</strong> brings personal meaning and may be financially or emotionally valuable, so use a safety chain or professional converter when appropriate. <strong>New designer pieces</strong> often have stronger mechanisms and shapes made for current placement. <strong>Costume jewellery</strong> is ideal for testing scale without anxiety. <strong>Shoe and scarf clips</strong> are engineered for their surfaces and are often the sensible choice.</p>
<div class="brooch-notes"><div><strong>Before buying vintage</strong><p>Open and close the clasp, check that the pin is straight, inspect missing stones under daylight and ask whether repairs are visible.</p></div><div><strong>Before wearing an heirloom</strong><p>Photograph the piece, confirm insurance if relevant, test the catch and avoid bags or coats that will rub directly against it.</p></div></div></section>

<section id="mistakes" data-reveal><h2>Five mistakes that make brooches look dated</h2>
<h3>1. Matching every accessory exactly</h3><p>A coordinated set can be beautiful, but wearing every part at once removes tension. Let the brooch disagree slightly in age, shape or finish. Mixed gold and silver can work when one metal appears twice and the other acts as the interruption.</p>
<h3>2. Combining too many formal signals</h3><p>Pearls, a fitted blazer, a formal blouse and a small floral lapel pin reproduce a familiar code. Change one major element. Use the brooch with denim, loosen the shirt, choose a broad jacket or replace the pumps with loafers.</p>
<h3>3. Choosing a piece too small for the garment</h3><p>A miniature pin can vanish on an oversized coat. Step back two metres before deciding. If the object disappears, enlarge it or move it to a smaller field such as a collar, pocket or cuff.</p>
<h3>4. Defaulting to the same lapel position</h3><p>The left lapel remains useful, especially on strong tailoring. It becomes dated only when every other decision is equally expected. Raise the placement, turn the piece, cluster it or move it to the storm flap.</p>
<h3>5. Ignoring weight and movement</h3><p>A brooch that looks perfect while standing may swing, pull or scratch when walking. Wear it at home for twenty minutes. Sit, put on a coat, carry your usual bag and check the fabric afterwards. Practical failure is never made elegant by trend status.</p></section>

<section id="care" data-reveal><h2>How to protect clothes from brooch damage</h2><p>Match the pin to the fabric before considering colour. Dense wool, denim, canvas and reinforced seams tolerate more weight. Fine silk, loose knits, technical membranes and valuable leather require a clip, converter or a different idea. A small felt backing patch behind the garment spreads pressure and can stop a heavy piece from tipping forward.</p>
<p>Push the pin through gently and in a straight line. Never force a blunt or corroded needle. Pin through seams, yokes or two fabric layers when the design allows, then close the catch fully. Magnetic converters can be useful, but keep strong magnets away from pacemakers and check whether they mark delicate finishes. Purpose-made scarf rings and shoe clips remain safer than improvisation.</p>
<p>Vintage mechanisms deserve particular attention. The Smithsonian&rsquo;s collection records historic pieces with simple C-clasps, and those open catches can loosen with age. A jewellery repairer can assess a valuable pin before wear. For practical fabric guidance, specialist Juliet Cuerden&rsquo;s <a href="https://www.broochella.com/blogs/news/how-to-wear-a-brooch-without-damaging-your-fabric">May 2026 care guide</a> similarly stresses matching brooch weight to fabric and checking vintage mechanisms rather than forcing them.</p></section>

<section id="faq" class="article-faq" data-reveal><h2>Brooch styling questions, answered</h2>
<h3>Which side should a brooch be worn on?</h3><p>There is no modern requirement. The left lapel is traditional, but collar, shoulder, right lapel, pocket and waist placements are equally valid. Choose the side that balances the garment, hairstyle and bag strap.</p>
<h3>Can you wear a brooch on a T-shirt?</h3><p>Yes, if the brooch is light. Pin through a folded sleeve edge, pocket seam or a small felt backing patch. Heavy pieces can drag jersey out of shape.</p>
<h3>How do you wear several brooches together?</h3><p>Use three to seven pieces and repeat one feature such as antique gold, botanical motifs or dark stones. Vary the scale, arrange them before pinning and keep the cluster within a clear boundary such as a denim yoke.</p>
<h3>Can men wear brooches?</h3><p>Of course. Current runway and search interest treats brooches as part of menswear&rsquo;s broader return to decorated tailoring. A geometric or botanical piece can sit on a lapel, tie, collar or coat without being framed as novelty.</p>
<h3>How do you wear a brooch without damaging clothes?</h3><p>Match weight to fabric, use seams or backing patches, close the clasp fully and choose converters for silk, leather, shoes or technical cloth. Test the placement at home before a full day.</p>
<h3>Are vintage brooches valuable?</h3><p>Some are, many are not. Value depends on maker, material, condition, rarity and documented provenance. Do not infer value from age or sparkle alone. Ask a qualified specialist before cleaning, altering or insuring a piece.</p>
<h3>Can you wear gold and silver brooches together?</h3><p>Yes. Mixed metal looks deliberate when the cluster shares another feature, such as scale or motif. Repeat one metal elsewhere in the outfit, then let the other provide contrast.</p></section>

<section class="source-note" data-reveal><h2>Sources and editorial notes</h2><p>Trend figures were checked on 1 August 2026 against <a href="https://business.pinterest.com/en-gb/pinterest-predicts/">Pinterest Predicts 2026</a>. Runway and placement context comes from British Vogue&rsquo;s <a href="https://www.vogue.co.uk/gallery/jewellery-trend-brooches-aw26">autumn/winter 2026 brooch report</a>, its <a href="https://www.vogue.co.uk/article/styling-tips-spring-2025">27 January 2026 styling edit</a> and its longer <a href="https://www.vogue.co.uk/article/brooches-trend">placement feature</a>. Broader jewellery scale was cross-checked with <a href="https://www.marieclaire.com/fashion/jewelry-trends-2026/">Marie Claire&rsquo;s 2026 jewellery report</a>. The styling analysis and all 12 article images are original to by.foro. Images are visual studies, not documentary runway photographs.</p></section>
<section data-reveal><h2>The final edit</h2><p>How to wear brooches now comes down to interruption. Put the precious object on the ordinary garment. Move it away from the position it inherited. Match its weight to the cloth, then let one shape carry the outfit. The brooch does not need to make a plain wardrobe louder. It needs to make it more particular.</p></section>
<!-- FURTHER-READING:START --><aside class="article-further" aria-label="Further reading"><p class="kicker">Continue the idea</p><p>Pair the brooch with <a href="/blogs/fashion/glamoratti-style-2026/">the return of expressive 1980s accessories</a>, <a href="/blogs/fashion/european-summer-style-2026/">the new European summer wardrobe</a>, <a href="/blogs/fashion/dressing-with-intention/">a more intentional wardrobe</a>, <a href="/blogs/fashion/how-to-wear-colour-again/">a controlled approach to colour</a>, <a href="/blogs/fashion/literary-chic-without-the-costume/">literary style without costume</a> and <a href="/blogs/culture/how-taste-is-built/">the practice of building taste</a>.</p></aside><!-- FURTHER-READING:END -->
<div class="article-end"><span>End</span><p>Research checked 1 August 2026. Published by by.foro Editorial. For corrections, contact <a href="mailto:hello@byforo.com">hello@byforo.com</a>.</p></div></div></div>
<section class="next-story"></section></article></main>'''


head = f'''<!DOCTYPE html><html lang="en-GB"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover"><meta name="theme-color" content="#f2eee7"><meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1, max-video-preview:-1"><title>{SEO_TITLE}</title><meta name="description" content="{DESCRIPTION}"><link rel="canonical" href="{CANONICAL}"><link rel="icon" href="/assets/icons/favicon.svg" type="image/svg+xml"><link rel="manifest" href="/site.webmanifest"><meta property="og:type" content="article"><meta property="og:locale" content="en_GB"><meta property="og:site_name" content="by.foro"><meta property="og:title" content="{SEO_TITLE}"><meta property="og:description" content="{DESCRIPTION}"><meta property="og:url" content="{CANONICAL}"><meta property="og:image" content="https://byforo.com{HERO}.jpg"><meta property="og:image:alt" content="Three antique-style brooches arranged on an oversized charcoal blazer with an oxblood scarf"><meta property="og:image:width" content="1536"><meta property="og:image:height" content="1024"><meta property="og:image:type" content="image/jpeg"><meta name="twitter:card" content="summary_large_image"><meta name="twitter:title" content="{SEO_TITLE}"><meta name="twitter:description" content="{DESCRIPTION}"><meta name="twitter:image" content="https://byforo.com{HERO}.jpg"><meta property="article:section" content="Fashion"><meta property="article:published_time" content="2026-08-01T13:15:00+02:00"><meta property="article:modified_time" content="2026-08-01T13:15:00+02:00"><meta name="author" content="by.foro Editorial"><link rel="preload" as="style" href="/styles.css"><link rel="stylesheet" href="/styles.css"><link rel="alternate" type="application/rss+xml" title="by.foro Journal" href="https://byforo.com/rss.xml"><link rel="apple-touch-icon" sizes="180x180" href="/assets/icons/icon-180.png"><script id="article-schema" type="application/ld+json">{json.dumps(article_schema, ensure_ascii=False, separators=(',', ':'))}</script><script id="article-breadcrumb-schema" type="application/ld+json">{json.dumps(breadcrumb_schema, ensure_ascii=False, separators=(',', ':'))}</script></head><body><a class="skip-link" href="#main">Skip to content</a><div class="edition-bar"><span>Independent editorial</span><span>Edition 01 &middot; 2026</span><span>Fashion &middot; Home &middot; Beauty &middot; Culture</span></div>{site_header(URL)}'''

page = head + body + site_footer() + '<script defer src="/script.js"></script></body></html>\n'
destination = ROOT / URL.strip("/") / "index.html"
destination.parent.mkdir(parents=True, exist_ok=True)
destination.write_text(page, encoding="utf-8", newline="\n")
print(f"Built {destination.relative_to(ROOT)}")
