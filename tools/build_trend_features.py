"""Build the five July 2026 by.foro trend features from reviewed copy."""

from __future__ import annotations

import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PUBLISHED = "2026-07-30"


FEATURES = [
    {
        "title": "The Anti-Algorithm Home: Why Perfect Interiors Are Starting to Feel Outdated",
        "seoTitle": "Lived-In Interior Design: Imperfect Homes in 2026 | by.foro",
        "department": "home",
        "topic": "lived-in-interiors",
        "url": "/blogs/home/lived-in-interior-design-2026/",
        "excerpt": "Lived-in interior design replaces showroom perfection with aged wood, useful objects, mixed materials and the beautiful evidence of daily life.",
        "metaDescription": "Discover why lived-in interior design is replacing showroom perfection in 2026, with practical ways to add patina, personality and everyday ease at home.",
        "deck": "The most interesting rooms now contain evidence: a softened armchair, a marked table, books left within reach and objects that could only belong to one household.",
        "kicker": "Home · The 2026 mood",
        "hero": "lived-in-interior-design-hero",
        "hero_alt": "Collected living room with a rumpled linen sofa, aged oak table, worn rug and personal objects",
        "images": [
            (
                "lived-in-interior-design-objects",
                "Aged oak console with old frames, books, keys, a handmade bowl and garden flowers",
            ),
            (
                "lived-in-interior-design-dining",
                "Lived-in dining room after lunch with mismatched chairs, rumpled linen and a worn timber table",
            ),
        ],
        "keywords": [
            "lived-in interior design",
            "interior design trends 2026",
            "collected home decor",
            "characterful interiors",
        ],
        "toc": [
            ("answer", "What lived-in design means"),
            ("why-now", "Why perfection lost its appeal"),
            ("patina", "Patina, not damage"),
            ("mix", "Mixing periods and materials"),
            ("objects", "Objects with a job"),
            ("textiles", "Textiles that can relax"),
            ("room-plan", "A room-by-room plan"),
            ("edit", "The line between life and clutter"),
        ],
        "body": """
<p class="article-opening">Lived-in interior design is a way of making rooms feel specific, useful and gently changed by time. Instead of hiding every cord, crease and personal object, it builds beauty from aged materials, mixed periods, comfortable textiles and the visible rituals of ordinary life. The result should not look messy. It should look impossible to reproduce with one shopping list.</p>
<p>That distinction matters in 2026. On 9 July, <a href="https://www.vogue.com/article/interior-design-trends-2026">Vogue named lived-in interiors</a> among the year&rsquo;s defining design movements, reporting a shift toward rooms shown as they are actually used. Its designers described layered stone, living wood finishes and dining chairs valued for the gatherings that happen around them. A June survey from <a href="https://www.homesandgardens.com/interior-design/interior-design-trends-2026">Homes &amp; Gardens</a> found the same larger turn from stark minimalism toward warmth, character and individuality. These are editorial trend reports, not rules. Their useful observation is that polish without personality has begun to feel strangely anonymous.</p>
<section id="answer" data-reveal><h2>What makes a home feel lived in?</h2>
<p>A lived-in home contains three kinds of evidence. The first is material: timber that has deepened, metal that has dulled, linen that no longer holds a shop-floor fold. The second is biographical: a chair inherited from somebody, a bowl bought on a particular trip, a drawing made by a child, a stack of books that reflects an actual obsession. The third is behavioural: a lamp beside the place where someone reads, a tray where keys genuinely land, hooks at the height that works for the household.</p>
<p>None of this requires an old building or an antique budget. New rooms acquire character when decisions begin with use instead of a reference image. Ask where coffee is placed, which seat catches the morning sun, where wet coats go and what people reach for at night. Those answers create a plan more personal than choosing between named aesthetics.</p></section>
<section id="why-now" data-reveal><h2>Why perfect interiors are starting to feel dated</h2>
<p>The immaculate neutral room once offered visual relief from a noisy internet. Then it became one of the internet&rsquo;s most repeatable products. The same pale sofa, boucle chair, arched mirror and fluted cabinet could be arranged in almost any postcode. Algorithms rewarded immediate recognition, shops shortened the route from image to purchase and homes began to resemble the content made about them.</p>
<p>A room can be beautiful and still feel thin if every object arrived at once. What is missing is not colour or ornament but time. Time introduces incompatibility, and incompatibility is often where character starts: a severe modern lamp on a scarred country table, a stainless-steel kitchen beside an old rush chair, a formal portrait above a sofa designed for afternoon sleep.</p>
<p>This is not an argument for performative disorder. A deliberately spilled cup and an artfully unmade bed are simply another kind of styling. The more convincing move is to stop removing the evidence of habits that make a room work.</p></section>
<section id="patina" data-reveal><h2>Patina is not the same as damage</h2>
<p>Patina is the surface record of good use. It is the darkening of an oak arm where hands have rested, the fine scratches on silver, the softened colour of vegetable-tanned leather and the slight variation in handmade glaze. Damage makes an object unsafe or prevents it from doing its job. A loose chair joint is damage. A rubbed edge is information.</p>
<p>Learn to maintain materials without resetting them. Oil a dry timber top, but do not sand away every mark. Condition leather before it cracks, while accepting the creases produced by sitting. Polish brass selectively if you prefer a little brightness, leaving depth around handles and joints. Wash linen well and let it retain movement. The aim is stewardship, not artificial ageing.</p>
<p>When buying new, choose materials capable of becoming better. Solid or thickly veneered timber can usually be repaired. Wool develops a settled surface; linen softens; unlacquered brass changes tone. A plastic film printed to resemble oak has no second life once its surface fails. The value of a living finish is not nostalgia. It is that maintenance remains possible.</p></section>
<figure class="media article-inline-image"><picture><source type="image/webp" srcset="/assets/images/blogs/home/lived-in-interior-design-2026/lived-in-interior-design-objects-640.webp 640w, /assets/images/blogs/home/lived-in-interior-design-2026/lived-in-interior-design-objects-960.webp 960w, /assets/images/blogs/home/lived-in-interior-design-2026/lived-in-interior-design-objects.webp 1536w" sizes="(max-width: 760px) 90vw, 760px"><img src="/assets/images/blogs/home/lived-in-interior-design-2026/lived-in-interior-design-objects.jpg" width="1536" height="1024" loading="lazy" decoding="async" alt="Aged oak console with old frames, books, keys, a handmade bowl and garden flowers"></picture></figure>
<section id="mix" data-reveal><h2>Mix periods by finding a point of agreement</h2>
<p>&ldquo;Collected&rdquo; does not mean indiscriminate. Successful mixed rooms usually contain a quiet agreement between unlike pieces. It might be line, colour, scale or material. A curving 1930s chair can sit beside a square contemporary sofa if both are low and generous. A glossy chrome lamp can sharpen a rustic table because its small footprint respects the larger form. Three woods can coexist when their undertones belong to the same warm or cool family.</p>
<p>Begin with one anchor that has enough presence to make the room feel intentional: a long table, a substantial rug, a deep sofa or a cabinet with history. Add a second piece from another period, then let smaller objects mediate between them. Repeating one note twice is usually enough. The black line of a modern lamp might answer a black frame across the room. The rust in an old rug can reappear in one cushion.</p>
<p>Scale is more important than provenance. Tiny vintage pieces scattered around a large new-build room read as accessories. Give old furniture real responsibility. Let the chest hold dining linen, the desk become a dressing table and the sideboard carry the television. Function keeps nostalgia from turning into theatre.</p></section>
<section id="objects" data-reveal><h2>Personal objects need a job or a reason</h2>
<p>The quickest way to make a room less generic is not to buy decor. It is to bring forward what already belongs to your life. A stone from a familiar beach can hold letters. A shallow bowl can collect keys. Children&rsquo;s drawings can be framed with the seriousness given to any work on paper. Cookbooks should live close to the kitchen, not be colour-sorted in a room where nobody reads them.</p>
<p>Use surfaces according to rhythm. A hall console may contain the daily layer: lamp, key bowl, post and perhaps one photograph. A high shelf can hold the slower layer: objects that matter but are handled rarely. A coffee table needs enough clear space for a cup, even when it carries books and flowers. Our guide to <a href="/blogs/home/coffee-table-styling-that-looks-collected/">coffee table styling that looks collected</a> applies the same test: leave room for the life the object is meant to support.</p>
<p>Rotate rather than accumulate. A home feels alive when its small landscape changes with attention: a new branch, a recently read book, the bowl brought back from storage because its colour suddenly suits the season. Rotation gives objects presence and makes dusting possible.</p></section>
<section id="textiles" data-reveal><h2>Choose textiles that are allowed to relax</h2>
<p>Perfectly arranged cushions are the punctuation of the showroom. In a home, textiles should invite contact. Washed linen, brushed cotton, wool, mohair and robust velvet look convincing when compressed, folded and slightly uneven. They hold light differently, which gives a mostly neutral room depth without requiring five shades of beige paint.</p>
<p>Mix textile weights before patterns. Put a dry linen cushion beside dense wool, a smooth cotton sheet under a nubbly blanket, a flatwoven rug beneath a plush chair. If pattern is wanted, let it come from one or two sources with different scales. A narrow stripe and a blurred floral can coexist because they do not compete for the same visual frequency.</p>
<p>Buy for laundering and repair. Removable covers, generous hems and fabrics that can tolerate ordinary cleaning are more luxurious than precious surfaces everyone is afraid to touch. In a <a href="/blogs/home/warm-minimalist-bedroom/">warm minimalist bedroom</a>, a creased duvet and softened wool throw do more for atmosphere than a row of decorative pillows that has to be removed every night.</p></section>
<section id="room-plan" data-reveal><h2>A practical room-by-room plan</h2>
<h3>Living room</h3><p>Move seating close enough for conversation before adding anything. Put a table beside every seat that is genuinely used. Replace one matching side table with a piece of different age or material. Gather remote controls in a box rather than pretending they do not exist. Keep the current book visible.</p>
<h3>Kitchen</h3><p>Let the durable tools stay out: a wood board, pepper mill, fruit bowl or earthenware jug. Hide packaging and duplicates, not evidence of cooking. If every surface is new, one freestanding timber piece can interrupt the fitted quality. The best <a href="/blogs/home/most-beautiful-kitchen-colour-combinations/">kitchen colour combinations</a> gain depth from timber, stone and metal as much as paint.</p>
<h3>Bedroom</h3><p>Give each side of the bed what its sleeper needs, even if the tables do not match. Use lamps related by scale or shade rather than identical bases. Allow a chair to carry tomorrow&rsquo;s clothes, but provide a hook or valet so it does not become a permanent pile.</p>
<h3>Bathroom</h3><p>Mix one warm material into the hard shell: timber stool, woven basket, linen blind or framed work on paper placed safely away from water. Keep daily bottles on a washable tray and store backups. A used bar of soap is not visual failure.</p></section>
<figure class="media article-inline-image"><picture><source type="image/webp" srcset="/assets/images/blogs/home/lived-in-interior-design-2026/lived-in-interior-design-dining-640.webp 640w, /assets/images/blogs/home/lived-in-interior-design-2026/lived-in-interior-design-dining-960.webp 960w, /assets/images/blogs/home/lived-in-interior-design-2026/lived-in-interior-design-dining.webp 1536w" sizes="(max-width: 760px) 90vw, 760px"><img src="/assets/images/blogs/home/lived-in-interior-design-2026/lived-in-interior-design-dining.jpg" width="1536" height="1024" loading="lazy" decoding="async" alt="Lived-in dining room after lunch with mismatched chairs, rumpled linen and a worn timber table"></picture></figure>
<section id="edit" data-reveal><h2>The line between life and clutter</h2>
<p>Useful evidence becomes clutter when it blocks the action a surface or room is meant to support. The dining table must still host dinner. The hall must allow a bag to be put down. A bedside table must leave room for water. This functional definition is kinder and clearer than a fixed limit on objects.</p>
<p>Give every active category a boundary: magazines in one low stack, post in one tray, blankets in one basket, chargers in one drawer. When the boundary fills, edit the category rather than buying a larger container. Empty space remains important, but it should feel like a pause around things that matter, not proof that nobody lives there.</p>
<p>The anti-algorithm home is not an aesthetic package. It is a refusal to let recognisable styling replace knowledge of the people in the room. A good house can be photographed, but the photograph should never explain all of it. Something should remain off-frame: a habit, a history, the reason that particular chair always sits there.</p></section>
<section data-reveal><h2>Let light and sound show that the room is used</h2><p>Uniform ceiling light makes even a characterful room feel like a display. Build a small landscape of light around activity: a shaded lamp beside the reading chair, a low pool across the dining table and a practical light where keys are found. Bulbs do not need to match perfectly, but their colour should belong to the same warm or neutral family.</p><p>Sound is another overlooked layer. Curtains, rugs, books and upholstered furniture reduce the hard echo that makes a minimally furnished room tiring. A lived-in room often sounds calmer because its useful softness absorbs noise. This is not a call to cover every surface. Add softness where voices, footsteps or dishes create the most reflection, then leave some hard material visible for contrast.</p></section>
<section data-reveal><h2>Sources and date notes</h2><p>Current trend reporting was checked on 30 July 2026. Read the July 2026 <a href="https://www.vogue.com/article/interior-design-trends-2026">Vogue interiors report</a> and the June 2026 <a href="https://www.homesandgardens.com/interior-design/interior-design-trends-2026">Homes &amp; Gardens trend review</a>. Their trend observations are credited; the practical guidance and opinions in this feature are by by.foro Editorial.</p></section>
""",
    },
    {
        "title": "The New European Summer Wardrobe",
        "seoTitle": "European Summer Style 2026: 10 Pieces That Define the Look",
        "department": "fashion",
        "topic": "summer-style",
        "url": "/blogs/fashion/european-summer-style-2026/",
        "excerpt": "European summer style for 2026, translated into ten useful pieces that feel polished and relaxed without becoming a holiday costume.",
        "metaDescription": "Build a European summer wardrobe for 2026 with ten useful pieces, practical outfit formulas and styling advice that avoids the social-media costume effect.",
        "deck": "The useful version of European summer style is less about dressing for a fantasy coastline and more about fabric, proportion and clothes that survive a real hot day.",
        "kicker": "Fashion · Summer 2026",
        "hero": "european-summer-style-hero",
        "hero_alt": "European summer wardrobe with Breton knit, Bermuda shorts, pajama trousers, raffia bag and wedges",
        "images": [
            (
                "european-summer-style-bermuda",
                "Faceless summer outfit with linen shirt, tailored navy Bermuda shorts, raffia bag and black wedges",
            ),
            (
                "european-summer-style-evening",
                "Striped pajama trousers, black knit, beaded bag and wedge sandals in a Mediterranean room at dusk",
            ),
        ],
        "keywords": [
            "European summer style 2026",
            "European summer wardrobe",
            "summer capsule wardrobe",
            "Euro summer outfits",
        ],
        "toc": [
            ("answer", "The look without the costume"),
            ("fabric", "Start with fabric"),
            ("ten", "The ten useful pieces"),
            ("formulas", "Four outfit formulas"),
            ("city-coast", "City, coast and evening"),
            ("packing", "A realistic packing edit"),
            ("avoid", "What makes it feel forced"),
        ],
        "body": """
<p class="article-opening">European summer style in 2026 is defined by relaxed tailoring, breathable fabric and one tactile accessory, not by dressing as a postcard. The wardrobe works because Breton stripes, pajama trousers, tailored Bermuda shorts, raffia, scarves, beads and low wedges can move between a hot city, a train, lunch and evening without requiring a costume change.</p>
<p>The repetition is visible across current coverage. On 15 July 2026, <a href="https://www.vogue.com/article/summer-trends-editor-picks-2026">Vogue&rsquo;s summer edit</a> brought together Breton tees, raffia totes, pajama trousers, tailored Bermudas, wedge mules, patterned scarves and beaded accessories. A 30 May report from <a href="https://www.vogue.es/articulos/euro-summer-tendencias-verano-2026-mediterraneo-italia-mallorca">Vogue Spain</a> tracked raffia, scarves, midi dresses and espadrille wedges around the Mediterranean. This does not prove that Europe has one wardrobe. Lisbon, Copenhagen, Naples and Warsaw clearly do not dress alike. It does show a shared summer logic: ease sharpened by one deliberate line.</p>
<section id="answer" data-reveal><h2>How to get the look without appearing dressed for a trend</h2>
<p>Choose two recognisable summer signals at most. Striped knit with tailored shorts is enough. Pajama trousers with a small beaded bag are enough. When raffia, scarf, stripe, crochet, wedge and sailor collar appear together, the clothes stop describing a person and start describing a mood board.</p>
<p>Keep one part of the outfit ordinary to you. If you always wear a white shirt, use it over Bermudas. If your wardrobe is mostly black, put the raffia bag beside a black dress. If flat shoes are your reality, ignore the wedge and wear a clean loafer or leather sandal. The most convincing holiday style retains the wearer&rsquo;s normal grammar.</p></section>
<section id="fabric" data-reveal><h2>Begin with fabric, not a destination</h2>
<p>Hot-weather polish is largely a fabric problem. Light does not automatically mean cool. A thin synthetic blouse can trap heat, turn translucent and hold odour faster than a slightly heavier cotton. Look for linen that is not too open, cotton poplin with movement, silk blends reserved for lower-friction pieces and fine knits that recover after stretching.</p>
<p>Wrinkles are acceptable; collapse is not. A good summer trouser can crease at the lap yet retain a clear waistband and side seam. Bermuda shorts need enough body to skim the thigh. A Breton top should hold the shoulder rather than cling across the torso. These structural details keep relaxed clothes from reading as sleepwear or beach cover-ups.</p></section>
<section id="ten" data-reveal><h2>The ten pieces that define the 2026 look</h2>
<h3>1. A Breton stripe with some weight</h3><p>Choose a cream ground rather than optic white if most of your wardrobe is warm. Navy is the classic, but tobacco, black or red can integrate more easily. A slightly boxy shoulder and bracelet sleeve feel more modern than a tight sailor tee. Wear it with dark denim, ivory trousers or Bermudas, not with every nautical object you own.</p>
<h3>2. The useful raffia bag</h3><p>Raffia gives a plain outfit texture and sunlight. The useful version has a secure closure, a reinforced base and handles that do not scratch the shoulder. A leather trim helps it work in a city. Consider a smaller raffia shoulder bag if a large open basket would spend the day knocking into café chairs.</p>
<h3>3. Pajama trousers that are clearly trousers</h3><p>Look for an opaque cloth, deliberate waistband and controlled width. A fine stripe or piped edge can nod to sleepwear, but the top should be crisp: black knit, fitted shirt or compact vest. The trouser works best when one other piece supplies structure.</p>
<h3>4. Tailored Bermuda shorts</h3><p>The strongest length finishes near the knee and leaves a little air around the thigh. Front pleats need to fall closed. A navy, cream or tobacco pair can replace a skirt in the city and works with the same loafers discussed in our <a href="/blogs/fashion/summer-loafers-outfit-guide/">summer loafers guide</a>. Vogue&rsquo;s June 2026 overview connected the style to spring collections by Dries Van Noten, Khaite and TWP, but fit matters more than label.</p>
<h3>5. A patterned silk scarf</h3><p>Use a scarf where the outfit actually needs it: over hair in wind, at the neck when an air-conditioned train is cold, around a bag handle that rubs or as a narrow belt through one loop. A small geometric print is easier to combine than a large souvenir motif. Let the knot be loose enough to look handled.</p>
<figure class="media article-inline-image"><picture><source type="image/webp" srcset="/assets/images/blogs/fashion/european-summer-style-2026/european-summer-style-bermuda-640.webp 640w, /assets/images/blogs/fashion/european-summer-style-2026/european-summer-style-bermuda-960.webp 960w, /assets/images/blogs/fashion/european-summer-style-2026/european-summer-style-bermuda.webp 1536w" sizes="(max-width: 760px) 90vw, 760px"><img src="/assets/images/blogs/fashion/european-summer-style-2026/european-summer-style-bermuda.jpg" width="1536" height="1024" loading="lazy" decoding="async" alt="Faceless summer outfit with linen shirt, tailored navy Bermuda shorts, raffia bag and black wedges"></picture></figure>
<h3>6. The minimalist wedge</h3><p>The 2026 wedge is cleaner than the platform espadrille: modest height, narrow upper, little decoration. It provides lift under long pajama trousers and balances the horizontal line of a Bermuda short. Check that the sole bends at the ball of the foot and that the heel does not separate from your foot when walking.</p>
<h3>7. A beaded evening accessory</h3><p>Glass or wooden beads catch low light without the formality of a satin clutch. Keep the shape compact and the rest of the look quiet. Beading is most elegant when it feels like craft, not a festival instruction. One bag or necklace is the entire point.</p>
<h3>8. An oversized linen or poplin shirt</h3><p>The shoulder can drop, but the collar should retain shape. Wear it buttoned into a wide trouser, open over a swimsuit or tucked loosely into shorts. Long sleeves are useful protection from sun and overenthusiastic air conditioning. Pale blue often looks fresher than white after several days of travel.</p>
<h3>9. A simple column dress</h3><p>A straight midi dress in cotton, linen blend or compact jersey creates a calm base for scarf, raffia or beads. Side slits make movement possible. Avoid a dress that depends on a particular undergarment you would not normally pack. The elegant option is the one you can sit in for two hours.</p>
<h3>10. A flat leather shoe</h3><p>Not every day can support a wedge. A backless loafer, slim sandal or soft ballet flat gives the wardrobe a practical floor. Choose a sole appropriate to the streets you will walk. The fashionable fantasy ends quickly on hot cobbles with no grip.</p></section>
<section id="formulas" data-reveal><h2>Four formulas that do not look pre-packaged</h2>
<p><strong>For a hot workday:</strong> blue poplin shirt, cream Bermuda shorts, dark belt, flat loafer, medium raffia shoulder bag. Roll the sleeves unevenly and keep jewellery small.</p>
<p><strong>For travel:</strong> Breton knit, navy pajama trousers, leather sandal, large closed tote. Carry the scarf for the train rather than tying it on before dawn.</p>
<p><strong>For lunch near water:</strong> column dress, raffia bag, low wedge and one cuff. The straight dress prevents the natural accessories from becoming pastoral.</p>
<p><strong>For evening:</strong> black sleeveless knit, striped pajama trouser, beaded pouch and minimalist wedge. This is relaxed but not careless because the dark upper half gives the eye a firm place to land.</p>
<p>Each formula changes only one or two signals from a normal outfit. That is the secret. Our broader guide to <a href="/blogs/fashion/dressing-with-intention/">dressing with intention</a> uses the same principle: repeat a reliable silhouette, then alter fabric or mood.</p></section>
<figure class="media article-inline-image"><picture><source type="image/webp" srcset="/assets/images/blogs/fashion/european-summer-style-2026/european-summer-style-evening-640.webp 640w, /assets/images/blogs/fashion/european-summer-style-2026/european-summer-style-evening-960.webp 960w, /assets/images/blogs/fashion/european-summer-style-2026/european-summer-style-evening.webp 1536w" sizes="(max-width: 760px) 90vw, 760px"><img src="/assets/images/blogs/fashion/european-summer-style-2026/european-summer-style-evening.jpg" width="1536" height="1024" loading="lazy" decoding="async" alt="Striped pajama trousers, black knit, beaded bag and wedge sandals in a Mediterranean room at dusk"></picture></figure>
<section id="city-coast" data-reveal><h2>Adjust for the city, coast and evening</h2>
<p>In a city, increase structure and coverage: closed bag, proper waistband, shirt collar, shoe with a real sole. Near the coast, relax one construction point: drawstring trouser, open weave bag or unlined dress. At night, add depth instead of more skin. Black, ink, tobacco and dark red make raffia and pale linen look deliberate after sunset.</p>
<p>Climate also decides. Northern evenings may require a cotton knit or light jacket. Southern midday heat rewards a loose sleeve and covered shoulder. The phrase &ldquo;European summer&rdquo; hides a great deal of weather, so pack for the forecast rather than the fantasy.</p></section>
<section id="packing" data-reveal><h2>A realistic seven-day packing edit</h2>
<p>Start with three bottoms: pajama trouser, tailored Bermuda and one skirt or simple dress. Add four tops: shirt, Breton knit, compact sleeveless knit and plain tee. Take two shoes, one flat and one slightly elevated, plus one practical bag and one small evening bag. The scarf and jewellery should fit inside the smaller bag.</p>
<p>Before packing, make every top work with two bottoms and both shoes work with every hem. Photograph the combinations if mornings are rushed. Wear the bulkiest knit and flat shoe in transit. Leave room for laundry and do not count a swimsuit as a top unless you have tested it under the actual shirt.</p></section>
<section data-reveal><h2>Build a palette that survives repetition</h2><p>A compact summer wardrobe needs contrast without requiring a new accessory for every outfit. Start with two base colours, such as navy and ivory, black and tobacco, or chocolate and pale blue. Add one accent that appears in a scarf, bead or knit stripe. The accent should work beside both bases. This turns six garments into combinations rather than separate looks.</p><p>White is beautiful but demanding in transit. Cream, stone and pale blue conceal the small evidence of a long day more gracefully. Dark bottoms are practical on trains and city benches; lighter bottoms feel cooler and more relaxed near water. Put the colour most flattering near your face in tops and scarves, then let bags and shoes repeat the quieter base.</p></section>
<section data-reveal><h2>Care for summer fabric while travelling</h2><p>Hang linen and poplin as soon as you arrive. Steam from a shower may release light creases, but do not leave clothes in a wet bathroom. A small spray bottle of water and clean hands can smooth a collar or trouser front. Roll knitwear and beaded pieces rather than hanging them from points that may stretch.</p><p>Pack a stain cloth, a small amount of gentle detergent and a breathable laundry bag. Rinse salt and chlorine from swimwear promptly. Let leather shoes dry away from direct heat and alternate pairs so insoles release moisture. Raffia should not be crushed under a suitcase; fill the bag with light clothing and protect projecting handles.</p><p>The wardrobe looks more expensive when it is maintained, not when it is larger. A brushed shoe, unrolled hem and shirt that has been allowed to dry fully will do more than a fifth novelty accessory.</p></section>
<section id="avoid" data-reveal><h2>What makes the look feel forced</h2>
<p>Too many regional clichés are the first warning. A beret does not belong to every French summer; a head scarf, basket and espadrille do not automatically create Italian ease. The second warning is newness. When every piece has been bought for one trip, the outfit lacks the friction of personal style.</p>
<p>The solution is editing, not understatement. You can wear a red scarf, beaded bag or sculptural wedge with confidence if the rest of the outfit belongs to your existing wardrobe. Summer style should make movement simpler and evenings more pleasurable. If it requires constant adjustment or a particular backdrop, it is wardrobe scenery.</p></section>
<section data-reveal><h2>Sources and date notes</h2><p>Trend references were checked on 30 July 2026 using <a href="https://www.vogue.com/article/summer-trends-editor-picks-2026">Vogue&rsquo;s 15 July summer edit</a>, <a href="https://www.vogue.es/articulos/euro-summer-tendencias-verano-2026-mediterraneo-italia-mallorca">Vogue Spain&rsquo;s 30 May Mediterranean report</a> and <a href="https://www.vogue.com/article/bermuda-shorts-summer-outfits">Vogue&rsquo;s June Bermuda-shorts report</a>. Specific styling recommendations are by by.foro Editorial.</p></section>
""",
    },
]


FEATURES.extend(
    [
        {
            "title": "Glamoratti: The Return of Decadent 1980s Style",
            "seoTitle": "Glamoratti Style: Maximalist 1980s Fashion in 2026",
            "department": "fashion",
            "topic": "trends",
            "url": "/blogs/fashion/glamoratti-style-2026/",
            "excerpt": "Glamoratti style brings sculpted shoulders, baggy suits, funnel necks, bold belts and serious gold jewellery back to fashion in 2026.",
            "metaDescription": "Understand the Glamoratti fashion trend of 2026 and wear sculpted tailoring, funnel necks, bold belts and gold jewellery without looking like a costume.",
            "deck": "Quiet luxury has not disappeared. It has acquired a stronger shoulder, a darker lipstick case and enough gold to catch the light from across the room.",
            "kicker": "Fashion · Pinterest Predicts 2026",
            "hero": "glamoratti-style-hero",
            "hero_alt": "Faceless woman in a charcoal sculpted-shoulder suit, funnel neck, wide belt and gold cuff",
            "images": [
                (
                    "glamoratti-style-accessories",
                    "Hammered gold cuff, chunky chain, black belt, oxblood gloves and angular sunglasses",
                ),
                (
                    "glamoratti-style-evening",
                    "Faceless evening look with a cream funnel-neck jacket, long black skirt and gold cuff",
                ),
            ],
            "keywords": [
                "Glamoratti style",
                "1980s fashion trend 2026",
                "power dressing",
                "maximalist fashion",
            ],
            "toc": [
                ("answer", "What Glamoratti means"),
                ("evidence", "Why it is happening now"),
                ("shoulder", "The new strong shoulder"),
                ("suit", "The baggy suit"),
                ("funnel", "Funnel necks"),
                ("gold", "Belts and gold jewellery"),
                ("formulas", "How to wear it"),
                ("buy", "What is worth buying"),
            ],
            "body": """
<p class="article-opening">Glamoratti is Pinterest&rsquo;s name for a 2026 revival of decadent 1980s power dressing: baggier suits, sculpted shoulders, high funnel necks, chunky belts and bold gold jewellery. The modern version is not a full period reconstruction. It works when one emphatic shape or accessory is placed against clothes that remain clean, current and easy to move in.</p>
<p>Pinterest released its 2026 forecast in December 2025. The company&rsquo;s <a href="https://create.pinterest.com/en-us/blog/2026-pinterest-predicts-trends-and-content-ideas/">official creator report</a> recorded increases in searches for &ldquo;80s luxury&rdquo; by 225%, &ldquo;baggy suit&rdquo; by 90%, &ldquo;chunky belt&rdquo; by 65%, &ldquo;high collar jacket&rdquo; by 60% and &ldquo;gold cuff&rdquo; by 50%. Those figures describe activity on Pinterest during its stated analysis period, not the whole population. Still, the cluster is unusually coherent: people are looking for scale, authority and visible pleasure after years of discreet beige.</p>
<section id="answer" data-reveal><h2>What Glamoratti style looks like in real clothes</h2>
<p>Imagine a charcoal suit cut wide through the leg, but controlled by a clean waist. Add a fine black funnel neck and one broad cuff. Or place a sculpted cream jacket over a plain column skirt with an oxblood clutch. The message comes from outline and finish, not from piling on references.</p>
<p>Three principles keep it contemporary. First, exaggerate one zone: shoulder, collar, waist or wrist. Second, keep the palette concentrated. Third, let the fabric carry some of the drama. Dense wool, polished leather, velvet and substantial metal look luxurious because they hold light and shape. Thin synthetic cloth with oversized proportions often looks like fancy dress.</p></section>
<section id="evidence" data-reveal><h2>Why quiet luxury is getting louder</h2>
<p>The restrained wardrobe of the early 2020s offered useful corrections: better fabric, fewer logos, a focus on cut. Its visual language then became easy to imitate. Once every feed contained a camel coat, cream knit and unmarked black bag, discretion itself started to look uniform.</p>
<p>Glamoratti keeps the attention to material but restores tension. A stronger shoulder changes posture. A wide belt makes the act of getting dressed visible. Gold jewellery acknowledges decoration instead of pretending a watch is purely functional. It is not a rejection of good basics. It is a reminder that good basics can support theatre.</p>
<p>The revival also fits a wider 2026 appetite for specificity. Pinterest&rsquo;s <a href="https://newsroom.pinterest.com/en-gb/news/pinterest-predicts-nonconformity-self-preservation-and-escapism-drive-21-trends-for-2026/">official newsroom summary</a> framed its forecast around nonconformity, self-preservation and escapism. That is marketing language, but the fashion implication is clear: generic polish has less emotional charge than a recognisable gesture.</p></section>
<section id="shoulder" data-reveal><h2>The new strong shoulder is sculpted, not padded at random</h2>
<p>A good strong shoulder extends the line cleanly and then lets the sleeve fall. It should not rise toward the ear or collapse into a dent above the arm. On a jacket, inspect the seam from the back. The cloth should remain smooth across the upper body, even if the shoulder projects beyond it.</p>
<p>Balance matters. A long, broad jacket works with a wide trouser when the inner layer is narrow and the shoe has a defined toe. A cropped sculpted jacket can sit over a straight skirt or high-waisted jean. If the shoulder and lower half are both voluminous, show a precise wrist, waist or ankle so the body does not disappear.</p>
<p>Tailoring is the category where vintage can be especially useful, but alterations have limits. Sleeve length and waist suppression are often possible. Rebuilding an oversized shoulder is expensive and can disturb the whole jacket. Buy for the shoulder first.</p></section>
<section id="suit" data-reveal><h2>The baggy suit needs a point of control</h2>
<p>&ldquo;Baggy&rdquo; in the trend report should not mean badly fitted. The modern suit is generous through jacket and trouser, with enough length to create a continuous line. Control can come from a high waistband, a belt over the jacket, a close funnel-neck layer or sleeves pushed to reveal the forearm.</p>
<p>Charcoal, espresso and ink are easier than black because their surface remains visible in low light. Pinstripe adds an unmistakable 1980s note, so use it with a plain knit and minimal shoe. A double-breasted closure increases presence; wear it closed only if the buttons sit without pulling.</p>
<p>Separate the suit after its first outing. The jacket can give a white tee and straight denim more authority. The trouser can take a small cardigan or soft silk shirt. This test distinguishes useful tailoring from an event outfit.</p></section>
<figure class="media article-inline-image"><picture><source type="image/webp" srcset="/assets/images/blogs/fashion/glamoratti-style-2026/glamoratti-style-accessories-640.webp 640w, /assets/images/blogs/fashion/glamoratti-style-2026/glamoratti-style-accessories-960.webp 960w, /assets/images/blogs/fashion/glamoratti-style-2026/glamoratti-style-accessories.webp 1536w" sizes="(max-width: 760px) 90vw, 760px"><img src="/assets/images/blogs/fashion/glamoratti-style-2026/glamoratti-style-accessories.jpg" width="1536" height="1024" loading="lazy" decoding="async" alt="Hammered gold cuff, chunky chain, black belt, oxblood gloves and angular sunglasses"></picture></figure>
<section id="funnel" data-reveal><h2>Funnel necks give drama without exposure</h2>
<p>The funnel neck rises away from the neck rather than clinging like a turtleneck. In compact knitwear it frames the jaw; in a jacket it can create an architectural line from shoulder to face. This makes it particularly effective with simple hair and little jewellery near the neckline.</p>
<p>Check movement before buying. Turn your head, sit down and lift your arms. A rigid collar that touches makeup or prevents normal movement will not become more charming at dinner. Fine wool and structured jersey are useful for inner layers; bonded wool or suede can hold the shape in outerwear.</p>
<p>If a high collar feels severe, soften the surrounding colour. Cream, tobacco and deep red feel less corporate than black. A narrow earring or bare ear is enough. The collar has already done the accessorising.</p></section>
<section id="gold" data-reveal><h2>Belts and gold jewellery are punctuation</h2>
<p>A wide belt over tailoring creates the shortest route to the trend. Choose leather with a firm edge and a buckle that belongs to the scale of the strap. Position it at the point where the jacket naturally narrows, not necessarily at the smallest part of the body. If the jacket bunches above and below, the belt is too tight or the cloth too soft.</p>
<p>Gold works best as a solid visual mass: one cuff, broad hoops, a chunky chain or a sculptural ring. Mixing all four turns impact into noise. The metal does not need to be precious, but weight, closure and finish matter. Look for smooth edges, a secure hinge and a tone that does not become green under indoor light.</p>
<p>This is one of the rare trends where one accessory can update an entire existing wardrobe. A broad cuff against a rolled white shirt, a black knit or the sleeve of an old coat gives more return than a head-to-toe revival.</p></section>
<section id="formulas" data-reveal><h2>Four ways to wear Glamoratti now</h2>
<p><strong>Day:</strong> oversized charcoal blazer, fine cream knit, straight blue jeans, black pointed flat, one gold cuff. The denim removes the boardroom reference.</p>
<p><strong>Work:</strong> wide navy trouser, black funnel neck, matching belt, compact leather bag. Add the sculpted jacket only if the workplace and temperature allow it.</p>
<p><strong>Dinner:</strong> cream high-collar jacket, long black skirt, oxblood clutch and a single cuff. Our guide to <a href="/blogs/fashion/how-to-wear-colour-again/">wearing colour without feeling overdressed</a> explains why one dark red accent can act almost like a neutral.</p>
<p><strong>Weekend:</strong> broad leather belt over a long cardigan, narrow trouser and loafer. This is the least literal version and often the most wearable.</p>
<p>Notice that none of these outfits combines a large shoulder, bright colour, wide belt, chunky chain and dramatic shoe. The trend becomes sophisticated when the eye can identify the decision.</p></section>
<section data-reveal><h2>Colour and fabric decide whether the trend feels expensive</h2><p>The original decade loved saturated colour, but a modern interpretation does not need electric brights. Oxblood, aubergine, petrol blue, tobacco and deep emerald have intensity with enough darkness to behave like wardrobe colours. Cream and stone make gold look deliberate. Charcoal gives broad tailoring more surface than flat black.</p><p>Use sheen selectively. A polished leather belt can sit against dry wool. A velvet evening piece works with matte hosiery and a plain shoe. Satin beside bright metal and glossy patent can overwhelm the silhouette. When shape is already emphatic, texture should alternate between light-catching and quiet.</p><p>Pinstripe deserves special care because it carries both financial and 1980s associations. Choose a stripe fine enough to read as texture from a distance. Break the suit with denim, a compact knit or a soft bag if you do not want the corporate reference to dominate.</p></section>
<section data-reveal><h2>Outerwear is the most convincing place to try the scale</h2><p>A coat or jacket can hold a sculpted shoulder without asking every layer beneath it to participate. Look for a clean armhole, enough room through the upper back and a sleeve that narrows slightly toward the cuff. A strong shoulder with a wide, shapeless sleeve can make the whole garment feel heavy.</p><p>Length changes the message. A hip-length jacket feels direct and works over long skirts. A longer double-breasted coat creates authority with simple trousers and boots. If the garment has both strong shoulder and dramatic lapel, keep fastenings and pockets quiet.</p><p>Try it over the thickest knit you plan to wear. Cross your arms, sit and carry your normal bag. Power dressing that prevents movement is only an image of power.</p></section>
<section data-reveal><h2>Beauty should support the architecture, not compete with it</h2><p>Hair can be sleek, natural or tied back, but it helps to keep the outline clear around a funnel neck or enlarged shoulder. A precise side part provides period tension without requiring a period set. Makeup can focus on one dense element, such as a deep lip or strong brow, while skin and eyes remain current.</p><p>The same editing rule applies to nails and scent. A dark short nail can echo oxblood leather; a warm resinous fragrance can extend the mood. None of these is required. The clothes already speak loudly, so grooming should make the decision look intentional rather than adding another theme.</p></section>
<figure class="media article-inline-image"><picture><source type="image/webp" srcset="/assets/images/blogs/fashion/glamoratti-style-2026/glamoratti-style-evening-640.webp 640w, /assets/images/blogs/fashion/glamoratti-style-2026/glamoratti-style-evening-960.webp 960w, /assets/images/blogs/fashion/glamoratti-style-2026/glamoratti-style-evening.webp 1536w" sizes="(max-width: 760px) 90vw, 760px"><img src="/assets/images/blogs/fashion/glamoratti-style-2026/glamoratti-style-evening.jpg" width="1536" height="1024" loading="lazy" decoding="async" alt="Faceless evening look with a cream funnel-neck jacket, long black skirt and gold cuff"></picture></figure>
<section id="buy" data-reveal><h2>What is worth buying, and what to borrow from the wardrobe</h2>
<p>Borrow the belt, dark palette and gold from what you already own. Test a strong shoulder with a coat or old blazer before investing. If the proportion makes three ordinary outfits better, a well-made jacket may deserve tailoring. If it only works with the full fantasy, enjoy the image and leave the purchase.</p>
<p>Vintage belts, cuffs and evening bags often carry the scale this look needs. Inspect plating, hinges, linings and leather around buckle holes. For jackets, prioritise shoulder and cloth. For a funnel neck, prioritise comfort. A dramatic item worn often is more rational than a quiet item that never feels quite right.</p>
<p>The most interesting part of Glamoratti is not nostalgia. It is permission to use clothes as architecture again. After years of trying to appear effortlessly correct, a visible decision can feel unexpectedly modern. Photograph the outfit from the side as well as the front: a strong silhouette has to remain coherent from every angle, not only in the mirror&rsquo;s first view.</p></section>
<section data-reveal><h2>Sources and date notes</h2><p>Pinterest search figures and forecast language were checked on 30 July 2026 against the <a href="https://create.pinterest.com/en-us/blog/2026-pinterest-predicts-trends-and-content-ideas/">official Pinterest Predicts creator report</a> and <a href="https://newsroom.pinterest.com/en-gb/news/pinterest-predicts-nonconformity-self-preservation-and-escapism-drive-21-trends-for-2026/">Pinterest Newsroom</a>. For wider runway context, see <a href="/blogs/fashion/fall-2026-fashion-trends-worth-wearing/">the by.foro Fall 2026 edit</a>. Styling analysis is by by.foro Editorial.</p></section>
""",
        },
        {
            "title": "The Bob Haircut Boom: Japanese Bob vs Scandi Bob",
            "seoTitle": "Japanese Bob vs Scandi Bob: Short Haircuts for 2026",
            "department": "beauty",
            "topic": "hair",
            "url": "/blogs/beauty/japanese-bob-vs-scandi-bob/",
            "excerpt": "Japanese bob versus Scandi bob, explained through length, perimeter, texture, styling, maintenance and the questions to ask before a short haircut.",
            "metaDescription": "Compare the Japanese bob and Scandi bob haircuts for 2026, including shape, length, texture, styling, maintenance and what to ask for at the salon.",
            "deck": "Both cuts are short, clean and current. One relies on precision and a controlled curve; the other leaves more room for air, bend and natural texture.",
            "kicker": "Beauty · Hair 2026",
            "hero": "japanese-bob-vs-scandi-bob-hero",
            "hero_alt": "Rear view comparing a sleek dark Japanese bob and a softly textured dark blonde Scandi bob",
            "images": [
                (
                    "japanese-bob-reference",
                    "Rear three-quarter reference of a precise dark brown Japanese bob with a blunt jaw-length perimeter",
                ),
                (
                    "scandi-bob-reference",
                    "Rear three-quarter reference of a softly textured dark blonde Scandi bob with natural movement",
                ),
            ],
            "keywords": [
                "Japanese bob vs Scandi bob",
                "Japanese bob haircut",
                "Scandi bob haircut",
                "bob haircut 2026",
            ],
            "toc": [
                ("answer", "The difference in one minute"),
                ("japanese", "The Japanese bob"),
                ("scandi", "The Scandi bob"),
                ("compare", "Shape and length compared"),
                ("texture", "Choosing for hair texture"),
                ("face", "Face-framing choices"),
                ("salon", "What to ask the stylist"),
                ("care", "Styling and maintenance"),
            ],
            "body": """
<p class="article-opening">The Japanese bob is usually the more precise cut: jaw-skimming, compact, blunt at the perimeter and styled smooth with a subtle inward curve. The Scandi bob keeps a strong outline but feels airier, often sitting from the jaw to just below the chin with natural bend, minimal invisible layering and less insistence on a polished finish. The better choice depends on hair behaviour and maintenance, not nationality or face-shape rules.</p>
<p>Interest is measurable. Google&rsquo;s <a href="https://trends.withgoogle.com/trends/summergeist/">Summergeist 2026 report</a> says search interest in &ldquo;Japanese bob&rdquo; rose 2,500% over the preceding month, while &ldquo;Scandi bob&rdquo; was a breakout search. The report also identifies peekaboo hair as the top trending summer colouring technique and ashy brown as the top trending colour during its measurement window. These are search signals, not evidence that either cut is universally flattering. They are a good reason to define the terms before taking a screenshot to a salon.</p>
<section id="answer" data-reveal><h2>Japanese bob vs Scandi bob at a glance</h2>
<p><strong>Japanese bob:</strong> a dense, graphic outline; commonly at jaw level; little visible layering; polished surface; ends may turn gently inward. It asks for accuracy and usually shows growth sooner.</p>
<p><strong>Scandi bob:</strong> a clean but less severe outline; jaw to below-chin length; subtle internal weight removal; natural straight, wavy or curly texture; ends may bend, flick or separate. It tolerates a little more irregularity between appointments.</p>
<p>Neither label describes one regulated technique. Salons and editors use the names with some variation. Treat them as visual shorthand, then discuss the actual perimeter, weight, length and styling routine you want.</p></section>
<section id="japanese" data-reveal><h2>The Japanese bob: precision, weight and a controlled curve</h2>
<p>The defining quality is compactness. The perimeter reads as one continuous, deliberate line, often landing between the lower cheek and jaw. Hair is kept dense enough for the edge to look substantial. Internal work may remove bulk, but obvious external layers would weaken the graphic shape.</p>
<p>A slight inward bevel can make the cut hug the jaw without resembling a round helmet. The curve should come from careful graduation or styling at the ends, not from excessive volume through the mid-length. A centre or quiet side part keeps the geometry visible. A fringe is optional and changes the composition considerably, so decide on it separately.</p>
<p>This bob looks especially clear on straight or softly bending hair, but it is not limited to one texture. Dense wavy hair may need invisible internal weight removal to prevent a triangular outline. Fine hair may benefit from the blunt edge, provided the length does not expose sparse areas at the nape. A good stylist assesses growth patterns before deciding the exact line.</p></section>
<figure class="media article-inline-image"><picture><source type="image/webp" srcset="/assets/images/blogs/beauty/japanese-bob-vs-scandi-bob/japanese-bob-reference-640.webp 640w, /assets/images/blogs/beauty/japanese-bob-vs-scandi-bob/japanese-bob-reference-960.webp 960w, /assets/images/blogs/beauty/japanese-bob-vs-scandi-bob/japanese-bob-reference.webp 1536w" sizes="(max-width: 760px) 90vw, 760px"><img src="/assets/images/blogs/beauty/japanese-bob-vs-scandi-bob/japanese-bob-reference.jpg" width="1536" height="1024" loading="lazy" decoding="async" alt="Rear three-quarter reference of a precise dark brown Japanese bob with a blunt jaw-length perimeter"></picture></figure>
<section id="scandi" data-reveal><h2>The Scandi bob: a strong line with room for movement</h2>
<p>The Scandi bob has structure, but the finish is less controlled. In a 15 July 2026 feature, <a href="https://www.vogue.com/article/what-is-the-scandi-bob">Vogue described it</a> as sitting between jawline and collarbone with a strong perimeter that is not too harsh, styled to respect natural texture. That length range is broad. The version currently circulating most often sits around the jaw or just below it, short enough to expose the neck and long enough to tuck.</p>
<p>Minimal invisible layers can release wave or prevent thick hair from becoming a solid block. The outside still reads as a bob. Ends may turn out, separate into soft bends or dry almost straight. This tolerance is what gives the cut its easy reputation, though &ldquo;easy&rdquo; depends entirely on whether the stylist cuts for the wearer&rsquo;s natural pattern.</p>
<p>Fine hair can look fuller when the perimeter remains dense and the crown is not over-layered. Wavy hair often needs less styling if the cut allows its bends to sit at different points. Curly and coily versions require a curl-by-curl conversation about shrinkage and shape; a reference photographed on straight hair does not predict the result.</p></section>
<figure class="media article-inline-image"><picture><source type="image/webp" srcset="/assets/images/blogs/beauty/japanese-bob-vs-scandi-bob/scandi-bob-reference-640.webp 640w, /assets/images/blogs/beauty/japanese-bob-vs-scandi-bob/scandi-bob-reference-960.webp 960w, /assets/images/blogs/beauty/japanese-bob-vs-scandi-bob/scandi-bob-reference.webp 1536w" sizes="(max-width: 760px) 90vw, 760px"><img src="/assets/images/blogs/beauty/japanese-bob-vs-scandi-bob/scandi-bob-reference.jpg" width="1536" height="1024" loading="lazy" decoding="async" alt="Rear three-quarter reference of a softly textured dark blonde Scandi bob with natural movement"></picture></figure>
<section id="compare" data-reveal><h2>Shape, length and finish compared</h2>
<h3>Perimeter</h3><p>The Japanese bob usually has the sharper, more continuous perimeter. The Scandi bob retains a visible line but may be softly point-cut or allowed to separate with texture. If you want the ends to look almost drawn, move Japanese. If you want the outline to survive air-drying, move Scandi.</p>
<h3>Length</h3><p>A jaw-level cut is visually strongest but leaves less room to tie hair back. Below-chin length offers more tucking and a softer grow-out. Ask the stylist to mark the proposed dry length while you are sitting upright. Wet hair, curls and a tilted head can all make the finished line shorter than expected.</p>
<h3>Volume</h3><p>The Japanese version concentrates weight at the edge and uses polish to keep the silhouette compact. The Scandi version allows air through the mid-length and crown. Neither should rely on aggressive thinning shears. Removing too much internal hair can make the surface frizz and the perimeter transparent.</p>
<h3>Finish</h3><p>Smoothness is part of the Japanese bob&rsquo;s visual identity, though it need not be glassy. The Scandi bob can be smooth too, but its signature is a less managed surface. A few flyaways and irregular bends belong to the look.</p></section>
<section id="texture" data-reveal><h2>Choose according to what your hair does after washing</h2>
<p>Wash and air-dry your hair before the consultation if possible. Show the stylist photographs of it on an ordinary day, not only after a blowout. Note where it expands, flips and separates. A cowlick at the nape may dictate a slightly shorter or longer line. Hair that swells in humidity needs a different internal structure from hair that falls flat.</p>
<p>For straight, medium-density hair, both cuts are realistic. Choose based on willingness to style and trim. For fine hair, protect the perimeter and avoid excessive layers. For thick straight hair, request hidden weight removal, not a shredded edge. For waves, the Scandi route usually gives more room to work with the pattern. For curls or coils, prioritise a stylist experienced in that texture and judge the shape dry.</p>
<p>Colour affects the reading of the cut. A single dark tone makes a blunt line look especially graphic. Fine highlights reveal bend and separation. Google&rsquo;s 2026 data may make ashy brown and peekaboo colour tempting, but colour should support the haircut and hair condition. Bleached internal panels can behave differently from the rest of a precise bob.</p></section>
<section id="face" data-reveal><h2>Face framing is more useful than face-shape rules</h2>
<p>Claims that one bob &ldquo;suits round faces&rdquo; or another &ldquo;elongates square faces&rdquo; reduce a three-dimensional decision to a diagram. More useful questions are where you want the eye to land and which features you prefer to reveal. A line at the jaw emphasises the jaw. A line below it can create a longer vertical. A side part changes asymmetry; a centre part makes the cut read more graphic.</p>
<p>Consider glasses, earrings, neckline and the way you tuck hair. If you tuck one side daily, ask the stylist to check how the line behaves behind the ear. If you wear a fringe, discuss its density with the bob&rsquo;s perimeter. Two strong horizontal lines can look intentional, but they need space between them.</p></section>
<section id="salon" data-reveal><h2>What to ask for at the salon</h2>
<p>Bring three reference images: front or three-quarter, side and back. Choose hair with a texture and density reasonably similar to yours. Then translate the image into decisions.</p>
<p>For a Japanese bob, ask about a jaw-skimming blunt perimeter, minimal visible layering, compact weight and a subtle inward bevel. Specify whether you want the ear covered, whether the nape should be exposed and how much daily smoothing you will do.</p>
<p>For a Scandi bob, ask for a strong but soft perimeter, jaw-to-below-chin length, minimal internal layering tailored to natural texture and enough length to tuck if that matters. Say explicitly that you want movement without a shag shape.</p>
<p>Ask the stylist to explain maintenance before cutting. If the desired line requires heat every morning or a six-week appointment you will not keep, adjust the design now.</p></section>
<section data-reveal><h2>A consultation checklist before the first cut</h2><p>Tell the stylist about chemical colour, keratin services and previous undercuts, even when they have grown out. These change density and movement. Show where you normally part the hair and whether you switch sides. Mention headphones, glasses, work uniforms and exercise routines that affect how often the hair is tucked or tied.</p><p>Agree on the shortest point and the back line. A bob that clears the jaw at the front may rise at the nape. Ask whether the cut will be established wet, refined dry or cut mainly in its natural texture. There is no single correct method, but the stylist should be able to explain why the method suits your hair.</p><p>If you are unsure, leave an extra centimetre. A slightly longer bob can be shortened after the shape settles; a line cut above your comfort cannot be negotiated with.</p></section>
<section id="care" data-reveal><h2>Styling and maintenance</h2>
<p>A precise short bob commonly needs reshaping every six to eight weeks, a timeframe also noted in <a href="https://www.vogue.fr/article/carre-japonais-japanese-bob-coupe-minimaliste-2026">Vogue France&rsquo;s 2026 Japanese-bob guide</a>. Growth rate, neckline and tolerance for change vary. A Scandi bob can often travel a little longer because a softer edge and extra length absorb growth, but the back may still become heavy.</p>
<p>For the Japanese finish, use heat protection, direct a dryer downward with a flat or round brush, then bend only the final centimetres. Finish with a small amount of light serum at the ends. For the Scandi finish, apply light leave-in conditioner or air-dry cream, encourage natural bends with hands and avoid coating the roots. A diffuser on low air can preserve wave without producing a salon curl set.</p>
<p>Sleep, weather and water will alter either cut. That is not failure. The useful haircut is the one whose second-day version you also like. Decide between precision and movement by imagining Tuesday morning, not the photograph taken five minutes after the cape comes off.</p></section>
<section data-reveal><h2>Plan the grow-out before committing</h2><p>A jaw-length bob usually passes through a heavier below-chin stage before reaching the shoulders. The back can feel long before the front catches up because of head shape and the original line. Small perimeter trims can keep it deliberate without resetting all the length.</p><p>If the goal is to grow, ask the stylist to remove only what distorts the shape. Avoid repeatedly thinning the interior, which may create short pieces that take longer to rejoin the edge. Fringe growth follows a separate schedule and may need face-framing adjustments.</p><p>Photograph the cut from the back on day one. The image gives future appointments a reliable reference and helps you notice whether the part, texture or styling preference has changed rather than assuming the cut itself was wrong.</p></section>
<section data-reveal><h2>Sources and date notes</h2><p>Search data and haircut descriptions were checked on 30 July 2026 using <a href="https://trends.withgoogle.com/trends/summergeist/">Google Summergeist 2026</a>, <a href="https://www.vogue.com/article/what-is-the-scandi-bob">Vogue&rsquo;s 15 July Scandi-bob feature</a> and <a href="https://www.vogue.fr/article/carre-japonais-japanese-bob-coupe-minimaliste-2026">Vogue France&rsquo;s Japanese-bob guide</a>. This article offers editorial guidance, not personalised hair or scalp advice.</p></section>
""",
        },
        {
            "title": "The Art Deco Revival: Why 1920s Glamour Is Returning",
            "seoTitle": "The Art Deco Revival: Fashion and Interiors in 2026",
            "department": "culture",
            "topic": "design",
            "url": "/blogs/culture/art-deco-revival/",
            "excerpt": "The Art Deco revival connects Fall 2026 fashion with geometric jewellery, velvet rooms, frosted lighting, marquetry and modern cocktail culture.",
            "metaDescription": "Explore the Art Deco revival across Fall 2026 fashion, jewellery, lighting, furniture, hotels and cocktail culture, with advice for using it today.",
            "deck": "A century after the Paris exhibition that fixed Deco in the public imagination, its geometry and glamour are moving through wardrobes, rooms and objects again.",
            "kicker": "Culture · Design history",
            "hero": "art-deco-revival-hero",
            "hero_alt": "Contemporary Art Deco lounge with oxblood velvet, walnut panels, frosted glass and black lacquer",
            "images": [
                (
                    "art-deco-revival-fashion",
                    "Plum velvet evening dress with linear beadwork, black gloves, embellished bag and geometric cuff",
                ),
                (
                    "art-deco-revival-objects",
                    "Stepped frosted-glass lamp, walnut box, geometric jewellery and coupe glass on a stone console",
                ),
            ],
            "keywords": [
                "Art Deco revival",
                "Art Deco fashion 2026",
                "Neo Deco interiors",
                "Art Deco interior design",
            ],
            "toc": [
                ("answer", "Why Deco is returning"),
                ("history", "What Art Deco actually was"),
                ("fashion", "Fall 2026 fashion"),
                ("jewellery", "Jewellery and bags"),
                ("interiors", "Lighting and furniture"),
                ("hotels", "Hotels and cocktails"),
                ("use", "How to use Deco now"),
                ("avoid", "Avoiding the theme-room effect"),
            ],
            "body": """
<p class="article-opening">The Art Deco revival is returning through geometry, shine and controlled luxury rather than literal 1920s costume. In fashion, it appears as velvet, linear embellishment, fringe, gloves and compact evening bags. In interiors, it is visible in stepped lighting, lacquer, marquetry, curved seating, fluted glass and richer colour. The successful modern version uses one strong Deco language at a time.</p>
<p>The timing is unusually clear. <a href="https://www.vogue.com/article/fall-winter-2026-fashion-trends">Vogue&rsquo;s Fall 2026 trend report</a>, published in July, identified the Art Deco dress across collections by Khaite, Colleen Allen and others, noting glamorous shapes, fringe, gloves, velvet and opulent evening bags. Pinterest separately forecast <a href="https://newsroom.pinterest.com/en-gb/news/pinterest-predicts-nonconformity-self-preservation-and-escapism-drive-21-trends-for-2026/">Neo Deco for 2026</a>, describing a sleek contemporary twist on the style. Fashion and interiors are responding to the same appetite: decoration with structure.</p>
<section id="answer" data-reveal><h2>Why does Art Deco feel current again?</h2>
<p>Deco offers an alternative to both blank minimalism and uncontrolled maximalism. Its rooms can be rich, but the richness is organised by repeated lines, symmetry and clearly framed materials. Its clothes can shimmer, but embellishment follows the body or garment construction. Luxury is visible, yet edited.</p>
<p>That balance suits the present mood. After years of pale, soft-edged interiors, a stepped lamp or black lacquer table brings clarity. After seasons of deliberately ordinary dressing, a velvet column or geometric cuff restores occasion. The style also photographs powerfully, which helps explain its digital visibility, but its best qualities are physical: the weight of a brass handle, the depth of velvet, the exact meeting of different veneers.</p></section>
<section id="history" data-reveal><h2>What Art Deco actually was</h2>
<p>Art Deco was never limited to flapper dresses and fan motifs. The <a href="https://www.vam.ac.uk/collections/art-deco">Victoria and Albert Museum&rsquo;s collection</a> spans furniture, ceramics, glass, metalwork, textiles, prints, fashion and jewellery. The 1925 Exposition internationale des arts décoratifs et industriels modernes in Paris became a defining public moment for the style, though its ideas developed before and continued through the 1930s.</p>
<p>Deco absorbed geometry, modern machinery, ancient and global references, expensive craft and new industrial materials. That breadth explains why a tubular chrome chair and an intricate lacquer cabinet can both belong to its story. There is no single Deco palette or motif. The connective tissue is a fascination with modern life expressed through controlled ornament, luxurious surface and decisive form.</p>
<p>The history also includes unequal access to materials, colonial collecting and the appropriation of motifs from cultures presented as exotic. A contemporary revival should understand that context rather than treating every zigzag as neutral decoration. Looking closely at museum collections, dates and makers is more useful than copying a generic &ldquo;Gatsby&rdquo; board.</p></section>
<section id="fashion" data-reveal><h2>How Fall 2026 fashion translates Deco</h2>
<p>The strongest current clothes do not reconstruct a drop-waist flapper dress. They borrow the verticality, surface and evening discipline of the period. A long velvet column creates a dark field for linear beadwork. Fringe follows a seam or hem instead of covering the entire body. Gloves extend a clean line. A geometric neckline gives the dress architecture before any embellishment is added.</p>
<p>Velvet is particularly effective because its pile changes with movement, creating richness without a print. Deep plum, black, bottle green and oxblood feel connected to Deco while remaining compatible with modern wardrobes. Wear one velvet piece against a dry surface such as wool, poplin or matte leather.</p>
<p>Fringe needs weight and purpose. On a bag or the edge of a skirt, it can animate walking. Cheap, sparse fringe twists and catches. If movement is the reason to buy it, walk several lengths of the fitting room and sit down before deciding.</p>
<p>Gloves are the most theatrical reference and should be treated accordingly. Elbow length works with a sleeveless column or short evening sleeve; a wrist glove can sharpen a coat. Keep shoes current and hair simple. The period clue is more persuasive when the entire beauty look does not repeat it.</p></section>
<figure class="media article-inline-image"><picture><source type="image/webp" srcset="/assets/images/blogs/culture/art-deco-revival/art-deco-revival-fashion-640.webp 640w, /assets/images/blogs/culture/art-deco-revival/art-deco-revival-fashion-960.webp 960w, /assets/images/blogs/culture/art-deco-revival/art-deco-revival-fashion.webp 1536w" sizes="(max-width: 760px) 90vw, 760px"><img src="/assets/images/blogs/culture/art-deco-revival/art-deco-revival-fashion.jpg" width="1536" height="1024" loading="lazy" decoding="async" alt="Plum velvet evening dress with linear beadwork, black gloves, embellished bag and geometric cuff"></picture></figure>
<section id="jewellery" data-reveal><h2>Jewellery and bags carry the geometry best</h2>
<p>Deco jewellery uses line, contrast and repeated shape. A stepped cuff in gold and onyx, long linear earrings or a compact ring with a strong rectangular setting can introduce the style without changing the rest of the outfit. Look for clean joins and stones held securely. The design depends on precision, so weak plating and crooked settings are especially visible.</p>
<p>Evening bags offer more room for pattern. Fan shapes, radiating beadwork, black satin, metallic frames and hard geometric clasps all make sense. Pair an embellished bag with an unembellished dress, or a plain lacquer clutch with a beaded garment. Two competing surfaces flatten each other.</p>
<p>Vintage examples deserve careful inspection. Open and close the frame, check bead loss along folds and examine fabric where a chain attaches. A beautiful bag that cannot hold a phone, key and card may still be collectible, but it is not a practical evening purchase.</p></section>
<section id="interiors" data-reveal><h2>In interiors, begin with lighting and furniture</h2>
<p>Lighting is the easiest route because Deco fixtures combine sculpture and function. Look for stepped or fluted glass, opaline shades, chrome, nickel, aged brass and compact geometric bases. One table lamp can change a room after dark without forcing the architecture to participate. Place it against a simple wall and let the silhouette read.</p>
<p>Furniture can move in two directions. The first is architectural: a marquetry cabinet, black lacquer table or screen with strong geometry. The second is sensuous: a curved velvet banquette, tub chair or rounded sofa. Combining one from each direction creates the tension at the heart of Deco. Repeating five angular objects turns a room into a set.</p>
<p>Material quality matters more than literal motif. Walnut veneer laid beautifully, a honed stone top and a substantial metal pull can suggest the period without a single sunburst. Our feature on <a href="/blogs/home/quietly-dramatic-home-decor/">quietly dramatic interiors</a> follows a compatible rule: one confident gesture per room, supported by calmer materials.</p>
<p>Colour should be deep but not relentlessly dark. Oxblood, plum, bottle green, cream, pale peach, walnut and black all belong. A cream wall or pale rug allows lacquer and velvet to remain legible. Mirrors can expand low light, but smoked or antiqued glass is often more forgiving than a wall of perfect reflection.</p></section>
<section id="hotels" data-reveal><h2>Why hotels and cocktail culture keep Deco alive</h2>
<p>Hotels are natural carriers of the style because they turn arrival, lighting and service into sequence. A geometric lobby floor establishes rhythm; a low banquette changes posture; a shaded lamp creates a private pool in a public room. These devices can make even a recently built hotel feel ceremonious.</p>
<p>Cocktail culture shares the same attention to frame. A coupe glass, silver tray, linen napkin and small pool of light make a drink feel like an event. At home, the lesson is not to build a themed bar. It is to make one small ritual complete. Keep good ice, use a glass that suits the drink and provide somewhere to set it down.</p>
<p>One illuminated lamp beside a tray is more convincing than a trolley crowded with decanters nobody opens. The glamour comes from readiness and proportion. An empty seat, a clean glass and flattering light suggest hospitality before any ornament is added.</p></section>
<section data-reveal><h2>Originals, reproductions and the quality question</h2><p>An original period object can carry history and exceptional craft, but age alone does not guarantee quality. Check veneer lifting, loose joints, rewired lamps and replaced hardware. Electrical pieces should be assessed by a qualified professional before use. Ask dealers for dimensions, condition reports and clear photographs of backs, bases and repairs.</p><p>A good reproduction is preferable to a compromised original when the object must work hard. Look for honest materials, balanced proportions and construction that can be repaired. A lamp inspired by Deco does not need a false patina or invented provenance. Contemporary designers can quote stepped glass, curved timber or geometric marquetry without pretending the piece was made in 1928.</p><p>For smaller budgets, focus on one precise category. Vintage chrome frames, glass dishes, bookends and compact lamps can carry the line without dominating a room. Reupholstering a simple curved chair in dense velvet may produce a better result than buying a whole themed furniture set.</p></section>
<figure class="media article-inline-image"><picture><source type="image/webp" srcset="/assets/images/blogs/culture/art-deco-revival/art-deco-revival-objects-640.webp 640w, /assets/images/blogs/culture/art-deco-revival/art-deco-revival-objects-960.webp 960w, /assets/images/blogs/culture/art-deco-revival/art-deco-revival-objects.webp 1536w" sizes="(max-width: 760px) 90vw, 760px"><img src="/assets/images/blogs/culture/art-deco-revival/art-deco-revival-objects.jpg" width="1536" height="1024" loading="lazy" decoding="async" alt="Stepped frosted-glass lamp, walnut box, geometric jewellery and coupe glass on a stone console"></picture></figure>
<section id="use" data-reveal><h2>How to use Art Deco now</h2>
<h3>In a wardrobe</h3><p>Choose one category: velvet, geometric jewellery, gloves or an embellished bag. Build the rest of the outfit from present-day tailoring and shoes. If the item only works with a themed event, it is costume rather than wardrobe.</p>
<h3>In a living room</h3><p>Add a fluted-glass lamp or small lacquer table beside furniture you already own. Repeat its metal finish once across the room, perhaps in a frame or handle. Stop there and observe it after dark before adding more.</p>
<h3>In a bedroom</h3><p>A curved headboard, pair of geometric sconces or narrow marquetry bedside cabinet can provide structure. Use plain bedding and one rich textile. Deco needs calm fields around its edges.</p>
<h3>At a dinner</h3><p>Use low light, simple glassware, cloth napkins and one linear arrangement of flowers or candlesticks. The period prized total design, but contemporary hospitality should still allow people to see their food and move their elbows.</p></section>
<section data-reveal><h2>A measured plan for one room</h2><p>Start with an inventory, not a shopping trip. Photograph the room at night, when Deco lighting and reflective surfaces matter most. Identify one missing function: reading light, side table, enclosed storage or comfortable occasional seating. Let the new object solve it.</p><p>Next, choose a material already present that can connect to the addition. A walnut lamp base can answer an existing table. A nickel sconce can repeat a door handle. An oxblood cushion can find a small colour in a rug. This point of agreement makes a historically inspired piece feel native to the room.</p><p>Live with the change for two weeks. If the room still needs more structure, add a second element from a different category, such as a textile after a lamp. Do not add another object with the same fan or zigzag motif. Repetition of material is quieter and more durable than repetition of symbol.</p></section>
<section id="avoid" data-reveal><h2>Avoiding the theme-room effect</h2>
<p>The quickest route to parody is repeating the same motif on wallpaper, rug, mirror, lamp and glassware. A style becomes convincing when its principles move between forms rather than its symbol being stamped everywhere. Use geometry in the furniture and softness in the textile, or pattern in the bag and simplicity in the dress.</p>
<p>A second mistake is confusing luxury with shine. Deco includes polished surfaces, but they gain depth from velvet, wood, parchment, wool and frosted glass. A room made entirely from mirror, bright brass and black gloss feels commercial. A wardrobe made entirely from satin and sequins loses the strong line that gives the trend authority.</p>
<p>The revival matters because it restores a relationship between decoration and discipline. Its geometry can make glamour feel intelligent, and its sensual materials can keep geometry from becoming cold. A century later, that exchange still looks modern.</p></section>
<section data-reveal><h2>Sources and date notes</h2><p>Current reporting was checked on 30 July 2026 against <a href="https://www.vogue.com/article/fall-winter-2026-fashion-trends">Vogue&rsquo;s Fall 2026 trend report</a> and <a href="https://newsroom.pinterest.com/en-gb/news/pinterest-predicts-nonconformity-self-preservation-and-escapism-drive-21-trends-for-2026/">Pinterest Predicts 2026</a>. Historical context comes from the <a href="https://www.vam.ac.uk/collections/art-deco">V&amp;A Art Deco collection</a>. Interpretation and practical advice are by by.foro Editorial.</p></section>
""",
        },
    ]
)


def esc(value: str) -> str:
    return (
        value.replace("&", "&amp;")
        .replace('"', "&quot;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
    )


def catalogue_entry(feature: dict) -> dict:
    base = f'/assets/images/blogs/{feature["department"]}/{feature["url"].strip("/").split("/")[-1]}/{feature["hero"]}'
    return {
        "title": feature["title"],
        "department": feature["department"],
        "topic": feature["topic"],
        "published": PUBLISHED,
        "readingMinutes": 11,
        "url": feature["url"],
        "excerpt": feature["excerpt"],
        "image": {
            "webp": f"{base}.webp",
            "fallback": f"{base}.jpg",
            "alt": feature["hero_alt"],
            "width": 1536,
            "height": 1024,
        },
        "metaDescription": feature["metaDescription"],
        "seoTitle": feature["seoTitle"],
    }


def page_head(feature: dict) -> str:
    entry = catalogue_entry(feature)
    page_url = f'https://byforo.com{feature["url"]}'
    image_url = f'https://byforo.com{entry["image"]["fallback"]}'
    schema = {
        "@context": "https://schema.org",
        "@type": "BlogPosting",
        "mainEntityOfPage": {"@type": "WebPage", "@id": page_url},
        "headline": feature["title"],
        "description": feature["metaDescription"],
        "image": [image_url],
        "datePublished": f"{PUBLISHED}T12:00:00+02:00",
        "dateModified": f"{PUBLISHED}T12:00:00+02:00",
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
        "articleSection": feature["department"].title(),
        "keywords": feature["keywords"],
        "inLanguage": "en-GB",
        "wordCount": 0,
    }
    breadcrumbs = {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {
                "@type": "ListItem",
                "position": 1,
                "name": "by.foro",
                "item": "https://byforo.com/",
            },
            {
                "@type": "ListItem",
                "position": 2,
                "name": feature["department"].title(),
                "item": f'https://byforo.com/{feature["department"]}/',
            },
            {
                "@type": "ListItem",
                "position": 3,
                "name": feature["title"],
                "item": page_url,
            },
        ],
    }
    return f"""<!DOCTYPE html>
<html lang="en-GB">
<head>
  <meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover"><meta name="theme-color" content="#f2eee7"><meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1, max-video-preview:-1">
  <title>{esc(feature["seoTitle"])}</title>
  <meta name="description" content="{esc(feature["metaDescription"])}">
  <link rel="canonical" href="{page_url}"><link rel="icon" href="/assets/icons/favicon.svg" type="image/svg+xml"><link rel="manifest" href="/site.webmanifest">
  <meta property="og:type" content="article"><meta property="og:locale" content="en_GB"><meta property="og:site_name" content="by.foro"><meta property="og:title" content="{esc(feature["seoTitle"])}"><meta property="og:description" content="{esc(feature["metaDescription"])}"><meta property="og:url" content="{page_url}"><meta property="og:image" content="{image_url}"><meta property="og:image:alt" content="{esc(feature["hero_alt"])}"><meta property="og:image:width" content="1536"><meta property="og:image:height" content="1024"><meta property="og:image:type" content="image/jpeg">
  <meta name="twitter:card" content="summary_large_image"><meta name="twitter:title" content="{esc(feature["seoTitle"])}"><meta name="twitter:description" content="{esc(feature["metaDescription"])}"><meta name="twitter:image" content="{image_url}">
  <meta property="article:section" content="{feature["department"].title()}"><meta property="article:published_time" content="{PUBLISHED}T12:00:00+02:00"><meta property="article:modified_time" content="{PUBLISHED}T12:00:00+02:00"><meta name="author" content="by.foro Editorial"><link rel="preload" as="style" href="/styles.css"><link rel="stylesheet" href="/styles.css"><link rel="alternate" type="application/rss+xml" title="by.foro Journal" href="https://byforo.com/rss.xml"><link rel="apple-touch-icon" sizes="180x180" href="/assets/icons/icon-180.png">
  <script id="article-schema" type="application/ld+json">{json.dumps(schema, ensure_ascii=False, separators=(",", ":"))}</script>
  <script id="article-breadcrumb-schema" type="application/ld+json">{json.dumps(breadcrumbs, ensure_ascii=False, separators=(",", ":"))}</script>
</head>"""


def article_html(feature: dict) -> str:
    slug = feature["url"].strip("/").split("/")[-1]
    department = feature["department"]
    department_label = department.title()
    base = f"/assets/images/blogs/{department}/{slug}/{feature['hero']}"
    toc = "".join(
        f'<li><a href="#{anchor}">{esc(label)}</a></li>'
        for anchor, label in feature["toc"]
    )
    return f"""<article class="article"><header class="article-hero"><nav class="breadcrumbs" aria-label="Breadcrumb"><a href="/">by.foro</a><span>/</span><a href="/{department}/">{department_label}</a><span>/</span><span aria-current="page">{esc(feature["topic"].replace("-", " ").title())}</span></nav><p class="kicker">{esc(feature["kicker"])}</p><h1>{esc(feature["title"])}</h1><p class="article-deck">{esc(feature["deck"])}</p><div class="article-meta"><a class="article-byline" href="/about/" rel="author">by.foro Editorial</a><time datetime="{PUBLISHED}">30 July 2026</time><span>11 min read</span></div></header>
<figure class="media article-hero-image"><picture><source type="image/webp" srcset="{base}-640.webp 640w, {base}-960.webp 960w, {base}.webp 1536w" sizes="(max-width: 760px) 90vw, 93vw"><img src="{base}.jpg" width="1536" height="1024" loading="eager" fetchpriority="high" decoding="async" alt="{esc(feature["hero_alt"])}"></picture></figure>
<div class="article-layout"><aside class="article-aside"><p class="kicker">The edit</p><ol>{toc}</ol><button class="copy-link" data-copy-link type="button">Copy link</button></aside>
<div class="article-body">{feature["body"].strip()}<div class="article-end"><span>End</span><p>Research checked 30 July 2026. Published by by.foro Editorial. For corrections, contact <a href="mailto:hello@byforo.com">hello@byforo.com</a>.</p></div></div></div>
<section class="next-story"></section></article>"""


def main() -> None:
    template = (
        ROOT / "blogs" / "fashion" / "fall-2026-fashion-trends-worth-wearing" / "index.html"
    ).read_text(encoding="utf-8")
    body_prefix = re.search(r"<body>.*?<main id=\"main\">", template, flags=re.S)
    footer = re.search(r"<footer class=\"site-footer\">.*$", template, flags=re.S)
    if body_prefix is None or footer is None:
        raise RuntimeError("Could not read the shared article shell")

    catalogue_path = ROOT / "content" / "articles.json"
    catalogue = json.loads(catalogue_path.read_text(encoding="utf-8"))
    feature_urls = {feature["url"] for feature in FEATURES}
    catalogue = [item for item in catalogue if item["url"] not in feature_urls]
    catalogue = [catalogue_entry(feature) for feature in FEATURES] + catalogue
    catalogue_path.write_text(
        json.dumps(catalogue, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
        newline="\n",
    )

    for feature in FEATURES:
        destination = ROOT / feature["url"].strip("/") / "index.html"
        destination.parent.mkdir(parents=True, exist_ok=True)
        page = (
            page_head(feature)
            + "\n"
            + body_prefix.group(0)
            + article_html(feature)
            + "</main>\n"
            + footer.group(0)
        )
        destination.write_text(page, encoding="utf-8", newline="\n")
    print(f"Built {len(FEATURES)} trend features.")


if __name__ == "__main__":
    main()
