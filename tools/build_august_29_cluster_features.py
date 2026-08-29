"""Build two low-competition cluster features for 29 August 2026."""

from __future__ import annotations

import html
import json
import re
from pathlib import Path

import build_august_two_features as base


ROOT = Path(__file__).resolve().parents[1]
PUBLISHED = "2026-08-29"
PUBLISHED_LABEL = "29 August 2026"
PUBLISHED_ISO = "2026-08-29T09:00:00+02:00"
base.PUBLISHED = PUBLISHED
base.PUBLISHED_LABEL = PUBLISHED_LABEL
base.PUBLISHED_ISO = PUBLISHED_ISO


def picture(root: str, name: str, alt: str) -> str:
    return f'''<figure class="media article-inline-image"><picture><source type="image/webp" srcset="{root}/{name}-640.webp 640w, {root}/{name}-960.webp 960w, {root}/{name}.webp 1536w" sizes="(max-width: 760px) calc(100vw - 2rem), 760px"><img src="{root}/{name}.jpg" width="1536" height="1024" loading="lazy" decoding="async" alt="{html.escape(alt)}"></picture></figure>'''


CARROT_URL = "/blogs/beauty/carrot-seed-perfume-guide/"
CARROT_ROOT = "/assets/images/blogs/beauty/carrot-seed-perfume-guide"
CARROT_TITLE = "Carrot Seed Perfume Smells More Like Iris Than Dinner"
CARROT_SEO = "Carrot Seed Perfume: What the Earthy Note Smells Like"
CARROT_DESCRIPTION = "Discover what carrot seed perfume smells like, how it differs from carrot blossom, which notes suit it and how to test the emerging vegetal fragrance trend."
CARROT_DECK = "It smells less like lunch than iris dusted with soil: dry, powdery, softly sweet and unexpectedly elegant."
CARROT_BODY = f'''<div class="article-layout"><aside class="article-aside"><p class="kicker">The scent file</p><ol><li><a href="#answer">The short answer</a></li><li><a href="#smell">What it smells like</a></li><li><a href="#different">Seed, root or blossom</a></li><li><a href="#styles">Five scent styles</a></li><li><a href="#test">How to test it</a></li><li><a href="#layer">How to layer it</a></li><li><a href="#choose">Choose the right bottle</a></li></ol><button class="copy-link" data-copy-link type="button">Copy link</button></aside><div class="article-body">
<p class="article-opening">Carrot seed perfume smells dry, earthy, powdery and softly sweet. The effect is closer to iris, violet, warm roots and clean soil than raw carrot or carrot cake. In a fragrance, it may add a grainy green texture to musk, woods, amber, apricot or floral notes without making the composition smell obviously like food.</p>
<p>The name creates a comic first picture: orange juice, grated salad, perhaps cream-cheese icing. The material itself is quieter and stranger. It can feel like opening a wooden drawer where a paper packet of seeds has been kept beside face powder. There is earth, but no mud; sweetness, but very little sugar.</p>
<p>That ambiguity gives carrot seed a useful place in 2026. Marie Claire reported in July that vegetable notes had moved from niche gardens into mainstream fragrance launches, including carrot, beetroot and butternut. At the same time, fragrance communities were asking for grown-up carrot scents that did not become gourmand. The interest is visible; the practical language for choosing one is still catching up.</p>
<div class="summary-box" id="answer"><p class="kicker">The concise answer</p><h2>Expect powder, roots and a dry green warmth</h2><p>Choose carrot seed with orris, iris or violet for a powdery finish; with vetiver, cedar or amber for something drier; with apricot, peach or musk for gentle sweetness; and with herbs or citrus for a brighter garden effect. Test it for at least four hours. The opening may suggest fresh roots, while the heart becomes cosmetic and the base settles into musk or wood.</p></div>
<section id="smell"><h2>What carrot seed perfume actually smells like</h2><p>The Fragrance Foundation UK describes carrot seed oil as a multifaceted material with green, earthy, softly fruity and powdery, almost orris-like facets. Perfumer Nathalie Rouquet also notes its grainy texture and terpenic lift. That combination explains why descriptions seem contradictory. One person notices dry soil. Another finds iris face powder. A third smells apricot skin or pale wood.</p><p>On paper, the green edge may arrive first: slightly bitter, dry and root-like. On warm skin, a softer floral powder can appear. Musk makes the material feel creamy; amber emphasises warmth; vetiver pulls it back toward roots. The same carrot seed note can therefore sit inside a close skin scent, an earthy floral or a dry autumn wood.</p><h3>It is not automatically a vegetal novelty</h3><p>Carrot seed has existed inside perfumes long before bottles advertised the vegetable garden. It often works as support rather than headline, adding natural texture to iris, violet, musk or amber. A note list can place it near the bottom while its powdery dryness quietly changes the whole composition.</p><h3>Why it can smell familiar without being identifiable</h3><p>Iris effects already sit between flower, root, paper, suede and powder. Carrot seed shares part of that territory but keeps more green grain and earthy sweetness. If a perfume smells like expensive face powder left beside a root cellar, the carrot may be doing more work than the label suggests.</p></section>
{picture(CARROT_ROOT, "carrot-seed-perfume-notes", "Carrot seeds, pale orris root, violet petals, apricot skin, cedar shavings and a glass sample vial arranged on worn limestone")}
<section id="different"><h2>Carrot seed, carrot root and carrot blossom are different ideas</h2><p>Fragrance names are creative directions, not laboratory inventories. A perfume called carrot blossom may build a fresh floral impression around orange blossom, herbs and musk. A root-focused composition may emphasise soil, vetiver and damp wood. Carrot seed oil is a real aromatic material, usually obtained by steam distillation or carbon-dioxide extraction, but a finished carrot accord can combine natural and synthetic materials.</p><div class="article-table-wrap" role="region" aria-label="Carrot fragrance style comparison" tabindex="0"><table class="article-visual-table"><thead><tr><th>Label</th><th>Likely direction</th><th>Useful pairings</th></tr></thead><tbody><tr><td>Carrot seed</td><td>Earthy, powdery, grainy, softly sweet</td><td>Orris, violet, musk, amber, cedar</td></tr><tr><td>Carrot root</td><td>Cool soil, damp wood, green bitterness</td><td>Vetiver, patchouli, moss, herbs</td></tr><tr><td>Carrot blossom</td><td>Airy floral with a garden edge</td><td>Orange blossom, fennel, neroli, white musk</td></tr><tr><td>Carrot accord</td><td>A perfumer's interpretation of the whole plant</td><td>Leaf, seed, fruit, earth or spice effects</td></tr></tbody></table></div><p>Do not treat those labels as guarantees. Read the surrounding notes and test the late drydown. A bottle covered in illustrated carrots can still become a conventional white musk after twenty minutes. A perfume with no vegetable in its name may reveal a convincing rooty iris on skin.</p><p>The distinction is similar to the one in our <a href="/blogs/beauty/tomato-leaf-perfume-guide/">tomato leaf perfume guide</a>: the recognisable object may be a mood assembled from several materials rather than a literal extraction of everything pictured on the box.</p></section>
<section id="styles"><h2>Five kinds of carrot seed perfume worth knowing</h2><h3>1. Powdery orris</h3><p>This is the easiest entry point. Iris, violet and ionone-like floral effects amplify the cosmetic side of carrot seed. Look for a finish that feels dry and translucent rather than chalky. It suits tailored clothes, cool weather and anyone who likes powder but dislikes overt sweetness.</p><h3>2. Clean skin musk</h3><p>Soft musk rounds the grain and brings the note closer to skin. The result can suggest warm paper, clean cotton and a faint trace of roots. It belongs naturally beside the quieter bottles in our <a href="/blogs/beauty/skin-scent-perfume-guide/">skin scent guide</a>, especially when the wearer wants intimacy with more texture than a simple white musk.</p><h3>3. Earthy amber</h3><p>Amber, cistus, balsamic notes and dry woods make carrot seed warmer and darker. The best versions preserve a green edge so the perfume does not collapse into generic sweetness. This style works in early autumn, when the air is cool but a dense vanilla still feels premature.</p><h3>4. Apricot and pale fruit</h3><p>The softly fruity side can make apricot, peach or raspberry feel less glossy. Carrot seed gives fruit a dry skin and a little soil beneath it. Choose this direction if you enjoy fruity perfume but want less syrup and more grain.</p><h3>5. Herb garden</h3><p>Fennel, parsley leaf, citrus, geranium or vetiver can pull the note toward the whole plant. The effect feels brighter than an earthy amber and softer than sharp tomato vine. It is the vegetable-fragrance option for someone who wants a garden, not a greenhouse.</p></section>
<section id="test"><h2>How to test carrot seed without mistaking powder for performance</h2><p>Begin with one spray on a labelled blotter. Smell at five minutes, thirty minutes, two hours and the following morning. Powdery notes can seem dense in the first cloud and then settle very close; musk can do the opposite, disappearing from your own attention while remaining clear to someone nearby.</p><ol><li><strong>At five minutes:</strong> name the first texture. Is it green, terpenic, rooty, peppery or fruity?</li><li><strong>At thirty minutes:</strong> look for the bridge into iris, violet, fruit or herbs.</li><li><strong>At two hours:</strong> decide whether the powder feels papery, creamy, dusty or suede-like.</li><li><strong>The next morning:</strong> judge the base without the bottle or packaging nearby.</li></ol><p>Move only one option to skin, then wear it on two ordinary days. Avoid scented hand cream during the first test. A cosmetic iris accord beside vanilla lotion may become much sweeter than the perfume is on its own.</p><h3>Test beside an iris, not another vegetable perfume</h3><p>A side-by-side comparison with an iris or violet fragrance reveals what carrot seed contributes: extra grain, roots, green lift or fruit. Comparing it only with tomato leaf turns the exercise into a contest for the most obvious vegetable. The quieter material loses for the wrong reason.</p></section>
{picture(CARROT_ROOT, "carrot-seed-perfume-testing", "Unbranded amber perfume bottle with three paper scent strips, a muslin pouch of carrot seeds and one freshly lifted carrot on a sunlit wooden table")}
<section id="layer"><h2>How to layer carrot seed without turning it into carrot cake</h2><p>Wear the perfume alone several times before layering. If the note feels too powdery, add something dry or bright rather than immediately reaching for vanilla. Keep each fragrance on a separate point of skin and reduce the total number of sprays.</p><ul><li><strong>For a cleaner finish:</strong> add quiet musk or pale cedar.</li><li><strong>For more roots:</strong> use vetiver, moss or a restrained patchouli.</li><li><strong>For brightness:</strong> choose bergamot, petitgrain or dry ginger.</li><li><strong>For softness:</strong> try iris, violet or a sheer rose.</li><li><strong>For gentle fruit:</strong> use apricot or peach without caramel notes.</li></ul><p>Cinnamon, dense vanilla and sugary lactones can push the association toward baking. That may be enjoyable, but it erases the material's unusual dry texture. If you bought carrot seed for its strangeness, allow some of the root to remain visible.</p><p>Within a <a href="/blogs/beauty/perfume-wardrobe-by-mood/">perfume wardrobe organised by mood</a>, carrot seed can sit between clean and green: calmer than tomato leaf, earthier than laundry musk and easier to wear when a bright citrus feels too thin.</p></section>
<section id="choose"><h2>How to choose a carrot perfume you will still wear after the surprise</h2><p>Ask which part you want after the name stops being funny. If the answer is iris powder, compare it with the iris perfumes already in your collection. If it is earth, make sure the drydown does not become a plain musk. If it is the current vegetable trend, buy a sample first and let novelty cool.</p><p>Then consider projection. A dry powder can feel elegant close to skin and oppressive when oversprayed onto a scarf. A herb-garden cologne may be vivid for twenty minutes and almost gone by lunch. Neither is a defect if it serves the role you intended.</p><h3>Do not buy a note when you dislike the base</h3><p>The opening explains the story; the base occupies the day. Smell the sample after four hours and on fabric the next morning. If the carrot has vanished, would you still choose the remaining musk, amber or wood? A full bottle should survive that question.</p><p>Keep the final fragrance away from direct sun, heat and bathroom steam. The beautiful still life belongs in a photograph; stable shade is kinder to the bottle. Our <a href="/blogs/beauty/the-vanity-table-as-still-life/">vanity table guide</a> shows how to keep useful objects visible without giving them the worst conditions in the room.</p></section>
<section class="article-faq"><h2>Carrot seed perfume questions</h2><h3>Does carrot seed perfume smell like carrots?</h3><p>It can suggest fresh roots and a little green sweetness, but it usually smells more powdery, woody and orris-like than a raw orange carrot.</p><h3>Is carrot seed perfume a gourmand?</h3><p>Not automatically. Vanilla, spice and lactonic notes can make it gourmand, while iris, vetiver, musk or cedar keep it dry and earthy.</p><h3>What is the difference between carrot seed and orris?</h3><p>They can share a powdery root-like effect. Carrot seed usually brings more green grain, earthy sweetness and terpenic lift; orris can feel cooler, smoother and more suede-like.</p><h3>Can carrot seed perfume work in warm weather?</h3><p>Yes. Choose a version with citrus, herbs, sheer musk or vetiver and apply lightly. Dense amber-and-powder styles are usually easier in cooler air.</p></section>
<section class="source-note"><h2>Sources and image note</h2><p>Current trend context was reviewed in <a href="https://www.marieclaire.co.uk/beauty/fragrance/vegetable-notes-perfume-trend">Marie Claire's July 2026 vegetable-fragrance report</a>. Material, extraction and formulation guidance was checked against <a href="https://static1.squarespace.com/static/633d57596b4dca58ec18a9a7/t/66ed549e17d936569ddd8b68/1726829734736/TFF_UK_Carrot_Seed_Special_2_compressed.pdf">The Fragrance Foundation UK's carrot seed special</a>, including its interview with perfumer Nathalie Rouquet. Community demand was reviewed in a July 2026 <a href="https://www.reddit.com/r/FemFragLab/comments/1v2i9o7/looking_for_a_grownup_nongourmand_carrot_or/">non-gourmand carrot fragrance discussion</a>. Testing, layering and wardrobe guidance is by.foro editorial analysis. The photographs show fictional unbranded fragrance scenes created for this article.</p></section>
<section><h2>The best carrot perfume keeps a little soil in the powder</h2><p>It should not need to shout vegetable. A dry green edge beneath iris, musk or amber is enough. When the joke of the name disappears and the texture remains interesting, carrot seed stops being a novelty and becomes a genuinely useful note.</p></section><div class="article-end"><span>End</span><p>Published by by.foro Editorial on 29 August 2026. For corrections, contact <a href="mailto:hello@byforo.com">hello@byforo.com</a>.</p></div></div></div>'''


BROOCH_URL = "/blogs/fashion/textured-brooch-trend/"
BROOCH_ROOT = "/assets/images/blogs/fashion/textured-brooch-trend"
BROOCH_TITLE = "The Textured Brooch Makes One Outfit Feel New"
BROOCH_SEO = "Textured Brooch Trend 2026: How to Wear Oversized Pins"
BROOCH_DESCRIPTION = "Learn how to wear oversized textured brooches in 2026, choose feather, fabric or sculptural styles and protect jackets, knits and simple tops from damage."
BROOCH_DECK = "Feather, felt, silk and brushed metal turn a flat pin into a small piece of architecture. Give it plain cloth and enough room."
BROOCH_BODY = f'''<div class="article-layout"><aside class="article-aside"><p class="kicker">The placement guide</p><ol><li><a href="#answer">The short answer</a></li><li><a href="#why">Why it is rising</a></li><li><a href="#choose">Choose the texture</a></li><li><a href="#place">Where to pin it</a></li><li><a href="#outfits">Seven outfit formulas</a></li><li><a href="#protect">Protect the garment</a></li><li><a href="#buy">Buy for repeat wear</a></li></ol><button class="copy-link" data-copy-link type="button">Copy link</button></aside><div class="article-body">
<p class="article-opening">A textured brooch is a dimensional pin made with feathers, silk, felt, yarn, beads, brushed metal or layered fabric. The easiest way to wear one is high on a plain blazer, knit or tank, with no competing necklace and enough empty cloth around it. Match the weight to the garment and keep the rest of the outfit ordinary.</p>
<p>The point is not to make a jacket look decorated. It is to change its surface. A flat gold pin adds shine; a textured brooch adds shadow, softness and movement. That small difference explains why an ivory organza flower can make a charcoal blazer feel new while a conventional crystal cluster may simply make it feel more formal.</p>
<p>The timing is unusually good. Pinterest placed brooches among its 2026 emerging trends, and late-August street-style coverage from Copenhagen focused specifically on oversized feathery pins. ABC's fall jewellery report, published on 28 August, described a wider move toward expressive scale, sculptural brooches and wearable-art materials. The exact idea is arriving quickly, but the search results are still thin enough for a practical guide to be useful.</p>
<div class="summary-box" id="answer"><p class="kicker">The concise answer</p><h2>Use one soft object against one firm line</h2><p>Pin a palm-sized textured brooch high on a blazer lapel, coat collar, dense knit or sturdy tank strap. Choose one clear colour, remove the necklace and repeat the brooch's texture nowhere else. Use a felt backing patch or converter when weight requires it, and never force a sharp pin through silk, fine jersey, technical fabric or valuable leather.</p></div>
<section id="why"><h2>Why the textured brooch feels right now</h2><p>Several fashion currents meet inside one small object. Minimal basics remain common, which gives a dramatic pin a calm background. At the same time, fall 2026 jewellery is becoming larger and more expressive. A brooch can satisfy both instincts: keep the jacket, change the focal point.</p><p>Texture also photographs well without depending on a logo. Feathers move, organza catches side light and felt creates a clear silhouette. The object remains recognisable in a close crop and can be moved from knit to coat between photographs. That portability gives it strong social potential without requiring a whole new outfit.</p><p>Who What Wear reported textured brooches on Copenhagen Fashion Week attendees in August, including feathery versions pinned to blazers, knits, T-shirts and tanks. The useful observation is not that every one of those combinations must be copied. It is that the pin has escaped the jewellery box and entered ordinary daytime clothes.</p><h3>The trend extends the brooch revival rather than replacing it</h3><p>Metal, enamel and antique pins are still relevant. Texture simply changes the scale and mood. Our broader guide to <a href="/blogs/fashion/how-to-wear-brooches/">17 modern ways to wear brooches</a> covers collars, scarves, bags, shoes and clusters. This article narrows the question to one large dimensional piece and the fabric required to support it.</p></section>
{picture(BROOCH_ROOT, "textured-brooch-materials", "Ivory silk organza, burgundy felt, black feathers and a brushed-gold sculptural brooch arranged with pins and tailor's chalk on a dark worktable")}
<section id="choose"><h2>Choose the texture by the clothes you already own</h2><div class="article-table-wrap" role="region" aria-label="Textured brooch material guide" tabindex="0"><table class="article-visual-table"><thead><tr><th>Material</th><th>Visual effect</th><th>Best background</th></tr></thead><tbody><tr><td>Silk or organza</td><td>Airy volume and translucent edges</td><td>Wool blazer, dense cotton, evening column</td></tr><tr><td>Felt or boiled wool</td><td>Graphic softness and clear colour</td><td>Denim, coat wool, compact knit</td></tr><tr><td>Feather</td><td>Movement, irregular shadow, lightness</td><td>Plain lapel, tank strap, simple crew neck</td></tr><tr><td>Yarn or crochet</td><td>Handmade grain and visible loops</td><td>Canvas, denim, smooth tailoring</td></tr><tr><td>Layered metal</td><td>Architectural depth with sharper edges</td><td>Coat, blazer, structured dress</td></tr><tr><td>Bead and textile</td><td>Colour, sparkle and surface density</td><td>Matte cloth with little pattern</td></tr></tbody></table></div><h3>Contrast is easier than matching</h3><p>A fuzzy brooch on a fuzzy jumper can disappear into one busy surface. Place softness against a cleaner line: feather on flannel, organza on wool, felt on denim, hammered metal on compact jersey. The difference lets both materials register.</p><h3>Scale should be judged from two metres away</h3><p>A palm-sized flower may look enormous in the hand and perfectly proportioned on an oversized blazer. Pin it temporarily, step back and take a plain phone photograph. If the object vanishes, enlarge it or move it to a smaller field such as a collar. If it consumes the shoulder, reduce the size or lower the contrast.</p><p>Do not confuse volume with weight. A feather piece may be visually large and physically light. A compact beaded brooch may be small and heavy. The garment responds to grams, while the outfit responds to silhouette. Both tests matter.</p></section>
<section id="place"><h2>Where to pin an oversized textured brooch</h2><h3>High on a blazer lapel</h3><p>This is the most reliable position because the lapel provides structure and the face supplies natural visual balance. Place the brooch above the chest line, then check whether the coat can still close. A large flower sitting too low can look like an improvised fastening.</p><h3>At the shoulder of a crew-neck knit</h3><p>Use a dense knit and a lightweight brooch. Let part of the shape cross the shoulder seam so the placement follows the garment's construction. Avoid loose loops that can be pulled by the pin or catch.</p><h3>On a substantial tank strap</h3><p>A textured pin can carry a summer tank into early autumn beneath a blazer. The strap must be wide and doubled enough to support the mechanism. Keep the opposite shoulder bare and choose simple trousers or denim.</p><h3>At the collar of a coat</h3><p>Coat wool can hold scale, but the piece must survive movement and a shoulder bag. Pin it on the side opposite the bag strap and check the position while sitting. A brooch that brushes the jaw or seat belt will not remain elegant for long.</p><h3>At the side waist of a plain dress</h3><p>Use the brooch as visual focus, not as a device to gather heavy fabric. Place it over a seam or supported band and keep the silhouette otherwise clean. This position suits layered metal or compact felt better than long feathers that collapse against the arm.</p></section>
{picture(BROOCH_ROOT, "textured-brooch-knit", "Large oxblood silk-and-feather brooch pinned high on a dense oatmeal crew-neck knit, cropped from neck to waist in soft window light")}
<section id="outfits"><h2>Seven textured brooch outfits that stay polished</h2><ol><li><strong>Charcoal blazer, white T-shirt, straight denim, ivory organza brooch.</strong> Use a black loafer and no necklace.</li><li><strong>Oatmeal crew neck, dark tailored trouser, oxblood feather brooch.</strong> Repeat oxblood only in a small lip or bag lining, not another accessory.</li><li><strong>Black tank, camel trousers, chartreuse felt flower.</strong> Keep the shoe dark and the earring small.</li><li><strong>Indigo denim jacket, cream skirt, brushed-gold sculptural pin.</strong> Place it near the yoke rather than the soft pocket edge.</li><li><strong>Navy coat, grey knit, pale-blue silk corsage.</strong> Pin opposite the bag strap.</li><li><strong>Matte black column dress, black feather brooch.</strong> Let texture, not colour contrast, create the evening effect.</li><li><strong>Brown suede jacket, white shirt, rust crochet brooch.</strong> Use smooth leather shoes so the handmade texture has one clear role.</li></ol><p>Each formula has one visual hierarchy. The brooch provides softness or scale, the garment supplies structure and the other accessories stay quiet. Trying to repeat feather at the shoe, bag and hair turns a removable detail into a theme.</p><h3>Colour can be bold when the shape is simple</h3><p>Chartreuse, violet and tomato red work because the surrounding outfit is familiar. If the brooch contains several colours, pull the wardrobe back to charcoal, navy, cream or denim. A monochrome textured piece can tolerate a richer outfit, especially when the material remains matte.</p><p>The strategy belongs to the same expressive family as <a href="/blogs/fashion/glamoratti-style-2026/">Glamoratti style</a>, but it requires far less commitment. One tactile object can bring theatre to a grey knit without asking the whole wardrobe to become opulent.</p></section>
<section id="protect"><h2>How to protect clothes from a large brooch</h2><p>Support is more important than placement originality. Dense wool, denim, canvas, coat cloth and reinforced seams handle weight best. Fine silk, open knits, delicate jersey, leather and waterproof technical fabrics should not be pierced casually.</p><p>Place a small felt patch behind the garment to spread pressure and stop a heavy brooch tipping forward. Fasten through two layers or close to a seam when the design allows it. A magnetic converter may avoid a hole, but strong magnets are not suitable for everybody or every electronic device; follow the maker's warnings and test whether the plates mark the fabric.</p><h3>Test the outfit in motion</h3><p>Wear the brooch at home for twenty minutes. Put on the coat, lift a bag, sit, reach across a table and fasten the seat belt. Check whether the object rotates, sheds, catches hair or scratches the garment. A beautiful still photograph is not evidence that the placement works through a day.</p><h3>Feathers and loose fibres need their own care</h3><p>Store dimensional brooches in a rigid box with enough room for the silhouette. Do not flatten organza or feathers beneath heavier jewellery. Remove surface dust with a very soft brush, working in the direction of the fibres. Follow the maker's instructions for dyed, glued or vintage materials and take valuable pieces to a specialist rather than applying steam or household cleaner.</p><p>If animal-derived feathers matter to you, ask the seller for origin and material disclosure. Vintage, reclaimed, plant-fibre and synthetic options can create movement without pretending every feathery object has the same source. Accuracy is more useful than a vague ethical label.</p></section>
<section id="buy"><h2>How to buy one that will outlast the autumn photographs</h2><p>Begin with the jacket or knit that needs a focal point. Measure the available lapel or shoulder area, then compare that field with the brooch dimensions. Online product photographs often hide scale by cropping close.</p><p>Turn the object over. The back should show a secure mechanism, neat attachment points and no dried glue or sharp wire. On fabric flowers, check whether the centre is stitched, wired or only glued. On feather pieces, look for a stable base and controlled shedding. On layered metal, run a finger near the edges before bringing it close to good cloth.</p><h3>Choose a removable colour, not an imaginary personality</h3><p>A brooch should improve at least three outfits you already wear. Photograph those outfits and test a paper shape of the same size before buying. If the object makes sense only with a future coat, future party and future confidence, it is an image rather than a wardrobe tool.</p><p>Textured brooches are especially suitable for vintage and handmade shopping because small differences improve the object. Search by material and mechanism rather than trend name: organza corsage pin, felt flower brooch, feather clip, textile pin, sculptural brooch. The better question is not whether it is the exact viral piece. It is whether the back is sound and the front still interests you when the feed moves on.</p><p>For smaller figurative pins, our <a href="/blogs/fashion/bug-jewellery-trend/">bug jewellery guide</a> offers a different route into expressive jewellery: less volume, more motif and a sharper relationship with metal.</p></section>
<section class="article-faq"><h2>Textured brooch questions</h2><h3>Where should an oversized brooch be placed?</h3><p>High on a blazer lapel, coat collar or dense knit shoulder is easiest. Use a supported area, leave space around the object and place it opposite the bag strap.</p><h3>Can a large brooch damage clothing?</h3><p>Yes. Weight, a blunt pin and repeated movement can stretch or puncture fabric. Use dense cloth, seams, backing patches or suitable converters and test the placement at home.</p><h3>Can textured brooches be worn in summer?</h3><p>Yes. Choose a lightweight organza, feather or fabric piece on a wide tank strap, cotton jacket or linen blazer with enough internal structure.</p><h3>Should a textured brooch match the bag or shoes?</h3><p>No. It usually looks more current as the only tactile focal point. Let the bag and shoes support the outfit with simpler leather, suede or canvas.</p></section>
<section class="source-note"><h2>Sources and image note</h2><p>Demand context was checked against <a href="https://business.pinterest.com/en-gb/blog/pinterest-predicts-2026-turn-trends-into-unlimited-possibilities/">Pinterest Predicts 2026</a>, <a href="https://www.whowhatwear.com/fashion/trends/oversized-textured-brooch-trend-2026">Who What Wear's 22 August textured-brooch report</a> and <a href="https://abcnews.com/GMA/Shop/avant-garde-jewelry-trend-fall-2026/story?id=136010401">ABC News' 28 August fall jewellery report</a>. Styling, garment-protection and buying guidance is by.foro editorial analysis; individual makers' care instructions take priority for specialist materials. The photographs show fictional unbranded accessories created for this article.</p></section>
<section><h2>The brooch works when the jacket still looks like yours</h2><p>Pin one soft object against one firm line, step back and remove the necklace. The outfit should not become a costume for the trend. It should simply reveal a new surface on a piece you already knew how to wear.</p></section><div class="article-end"><span>End</span><p>Published by by.foro Editorial on 29 August 2026. For corrections, contact <a href="mailto:hello@byforo.com">hello@byforo.com</a>.</p></div></div></div>'''


ARTICLES = [
    {
        "url": CARROT_URL,
        "seo": CARROT_SEO,
        "title": CARROT_TITLE,
        "description": CARROT_DESCRIPTION,
        "deck": CARROT_DECK,
        "department": "Beauty",
        "topic": "Fragrance",
        "hero": f"{CARROT_ROOT}/carrot-seed-perfume-hero",
        "alt": "Unbranded amber perfume bottle beside freshly lifted carrots, carrot seeds, orris root and cream linen on worn limestone",
        "body": CARROT_BODY,
        "words": 2200,
        "keywords": ["carrot seed perfume", "what does carrot seed smell like", "carrot perfume", "vegetable perfume trend"],
    },
    {
        "url": BROOCH_URL,
        "seo": BROOCH_SEO,
        "title": BROOCH_TITLE,
        "description": BROOCH_DESCRIPTION,
        "deck": BROOCH_DECK,
        "department": "Fashion",
        "topic": "Accessories",
        "hero": f"{BROOCH_ROOT}/textured-brooch-hero",
        "alt": "Large oxblood silk-and-feather brooch pinned high on a charcoal wool blazer, photographed from neck to waist on an overcast city street",
        "body": BROOCH_BODY,
        "words": 2100,
        "keywords": ["textured brooch trend 2026", "oversized brooch", "feather brooch outfit", "how to wear a statement brooch"],
    },
]


def add_reciprocal_link(path: Path, url: str, sentence: str) -> None:
    text = path.read_text(encoding="utf-8")
    if url in text:
        return
    match = re.search(r'(<p class="article-opening">.*?</p>)', text, flags=re.S)
    if not match:
        raise RuntimeError(f"Could not find opening paragraph in {path}")
    text = text[: match.end()] + sentence + text[match.end() :]
    path.write_text(text, encoding="utf-8", newline="\n")


def main() -> None:
    for item in ARTICLES:
        document = base.page(
            item["url"], item["seo"], item["title"], item["description"],
            item["deck"], item["department"], item["topic"], item["hero"],
            item["alt"], item["body"], "BlogPosting", item["words"], item["keywords"],
        )
        destination = ROOT / item["url"].strip("/") / "index.html"
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_text(document, encoding="utf-8", newline="\n")
        print("Built", destination.relative_to(ROOT))

    catalogue_path = ROOT / "content" / "articles.json"
    current = json.loads(catalogue_path.read_text(encoding="utf-8"))
    additions = []
    for item in ARTICLES:
        additions.append({
            "title": item["title"],
            "seoTitle": item["seo"],
            "department": item["department"].lower(),
            "topic": item["topic"].lower(),
            "published": PUBLISHED,
            "readingMinutes": round(item["words"] / 195),
            "readingWordsPerMinute": 195,
            "url": item["url"],
            "excerpt": item["deck"],
            "metaDescription": item["description"],
            "image": {
                "webp": f'{item["hero"]}.webp',
                "fallback": f'{item["hero"]}.jpg',
                "alt": item["alt"],
                "width": 1536,
                "height": 1024,
            },
            "articleSection": item["topic"],
            "breadcrumbTopic": True,
        })
    new_urls = {item["url"] for item in additions}
    catalogue_path.write_text(
        json.dumps(additions + [item for item in current if item["url"] not in new_urls], ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
        newline="\n",
    )

    add_reciprocal_link(
        ROOT / "blogs/beauty/tomato-leaf-perfume-guide/index.html",
        CARROT_URL,
        '<p>For the softer, powderier edge of the same vegetal shift, our <a href="/blogs/beauty/carrot-seed-perfume-guide/">carrot seed perfume guide</a> explains its orris-like texture, testing and layering.</p>',
    )
    add_reciprocal_link(
        ROOT / "blogs/beauty/perfume-wardrobe-by-mood/index.html",
        CARROT_URL,
        '<p>Between the clean and green moods, our <a href="/blogs/beauty/carrot-seed-perfume-guide/">carrot seed perfume guide</a> explores a dry, powdery note that feels earthier than musk and softer than tomato leaf.</p>',
    )
    add_reciprocal_link(
        ROOT / "blogs/fashion/how-to-wear-brooches/index.html",
        BROOCH_URL,
        '<p>For the newest oversized variation, our <a href="/blogs/fashion/textured-brooch-trend/">textured brooch guide</a> covers feather, silk, felt and sculptural pins, including the support each garment needs.</p>',
    )
    add_reciprocal_link(
        ROOT / "blogs/fashion/glamoratti-style-2026/index.html",
        BROOCH_URL,
        '<p>For a smaller route into the same expressive mood, our <a href="/blogs/fashion/textured-brooch-trend/">textured brooch guide</a> shows how one tactile pin can change a plain blazer, knit or tank.</p>',
    )


if __name__ == "__main__":
    main()
