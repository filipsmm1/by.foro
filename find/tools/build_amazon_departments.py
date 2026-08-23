"""Build every Amazon-backed department for the by.foro Finder.

The script keeps the existing editorial perfume catalogue, changes its shopping
destinations to Amazon searches, supplements it to the requested size, and
builds five further departments from current Amazon category and search pages.
It stores Amazon-hosted image URLs rather than copying Amazon product images.
That keeps the catalogue light and leaves product graphics on Amazon's servers.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Any

from lxml import html


FIND_DIR = Path(__file__).resolve().parents[1]
PRODUCTS_PATH = FIND_DIR / "products.json"
CHECKED_DATE = "2026-08-23"
DEFAULT_PER_DEPARTMENT = 200
USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140 Safari/537.36"
)

SOURCES = {
    "makeup": ["https://www.amazon.com/gp/bestsellers/beauty/11058281"],
    "skincare": ["https://www.amazon.com/gp/bestsellers/beauty/11060451"],
    "kitchen": ["https://www.amazon.com/gp/bestsellers/kitchen/289913"],
    "home": [
        "https://www.amazon.com/gp/bestsellers/home-garden/1063278",
        "https://www.amazon.com/gp/bestsellers/home-garden/3610841",
    ],
    "accessories": [
        "https://www.amazon.com/gp/bestsellers/fashion/2474936011",
        "https://www.amazon.com/gp/bestsellers/fashion/7192394011",
    ],
}

# Targeted searches provide enough breadth for a 200-item department while also
# supplying a reliable type hint when a concise Amazon title omits category
# language. Searches stop as soon as the requested unique-item target is met.
SEARCHES: dict[str, list[tuple[str, str]]] = {
    "perfume": [
        ("women's perfume", "floral-powdery"),
        ("men's cologne", "green-woody"),
        ("unisex fragrance", "skin-musk"),
        ("vanilla perfume", "gourmand-vanilla"),
        ("musk perfume", "skin-musk"),
        ("fresh citrus perfume", "fresh-citrus"),
        ("oud perfume", "green-woody"),
        ("amber perfume", "amber-spicy"),
    ],
    "makeup": [
        ("mascara", "eyes"), ("eyeshadow palette", "eyes"),
        ("eyeliner makeup", "eyes"), ("foundation makeup", "complexion"),
        ("concealer makeup", "complexion"), ("face primer makeup", "complexion"),
        ("face powder makeup", "complexion"), ("lipstick", "lips"),
        ("lip gloss", "lips"), ("blush makeup", "cheeks"),
        ("bronzer highlighter", "cheeks"), ("eyebrow pencil", "brows"),
    ],
    "skincare": [
        ("facial cleanser", "cleanser"), ("face moisturizer", "moisturizer"),
        ("face sunscreen", "sunscreen"), ("face serum", "serum"),
        ("vitamin c serum", "serum"), ("retinol serum", "serum"),
        ("face toner", "exfoliant"), ("face exfoliant", "exfoliant"),
        ("acne treatment", "mask"), ("pimple patches", "mask"),
        ("face mask skincare", "mask"), ("body lotion", "body"),
    ],
    "kitchen": [
        ("air fryer", "air-frying"), ("coffee maker", "coffee"),
        ("espresso machine", "coffee"), ("personal blender", "blending"),
        ("countertop blender", "blending"), ("food processor", "blending"),
        ("two slice toaster", "breakfast"), ("electric kettle", "breakfast"),
        ("waffle maker", "baking"), ("stand mixer", "baking"),
        ("rice cooker", "meal-prep"), ("slow cooker", "meal-prep"),
        ("indoor grill", "meal-prep"), ("juicer machine", "blending"),
    ],
    "home": [
        ("table lamp home decor", "lighting"), ("floor lamp home", "lighting"),
        ("throw pillow home decor", "textiles"), ("area rug home", "textiles"),
        ("throw blanket", "textiles"), ("curtains living room", "textiles"),
        ("storage basket home", "storage"), ("drawer organizer home", "storage"),
        ("home storage shelves", "storage"), ("decorative tray", "tabletop"),
        ("decorative vase", "tabletop"), ("picture frame home", "wall-decor"),
        ("wall mirror home decor", "wall-decor"), ("wall art home decor", "wall-decor"),
        ("candle warmer lamp", "scent"), ("reed diffuser home", "scent"),
    ],
    "accessories": [
        ("women's earrings", "jewelry"), ("women's necklace", "jewelry"),
        ("women's bracelet", "jewelry"), ("women's rings", "jewelry"),
        ("brooch pin women", "jewelry"), ("women's handbag", "handbags"),
        ("women's wallet", "handbags"), ("women's tote bag", "handbags"),
        ("women's hair accessories", "hair"), ("women's belt", "belts"),
        ("women's scarf", "scarves"), ("women's sunglasses", "eyewear"),
        ("women's sun hat", "hats"),
    ],
}

ALLOW = {
    "perfume": re.compile(
        r"perfume|parfum|fragrance|cologne|eau de toilette|eau de parfum|body spray",
        re.I,
    ),
    "makeup": re.compile(
        r"mascara|lip|foundation|concealer|blush|bronzer|liner|shadow|brow|powder|primer|makeup|gloss|highlighter",
        re.I,
    ),
    "skincare": re.compile(
        r"cleanser|wash|moist|cream|lotion|serum|sunscreen|spf|patch|mask|toner|exfol|retinol|balm|essence|mist|oil|body",
        re.I,
    ),
    "kitchen": re.compile(
        r"air fryer|toaster|blender|coffee|espresso|kettle|mixer|processor|cooker|griddle|waffle|juicer|chopper|oven|maker|steamer",
        re.I,
    ),
    "home": re.compile(
        r"frame|pillow|rug|curtain|diffuser|candle|lamp|light|vase|mirror|blanket|throw|basket|tray|clock|wall art|artwork|decor|holder|storage|organizer|shelf|drawer|hanger|bin",
        re.I,
    ),
    "accessories": re.compile(
        r"headband|sunglass|scarf|belt|wallet|bag|earring|necklace|bracelet|ring|clip|scrunch|hat|watch|brooch|pin|hair",
        re.I,
    ),
}

BLOCK = re.compile(
    r"\brefill\b|\breplacement\b|\bliner\b|filter only|gift card|subscription|\bbook\b|costume|cleaning cloth|makeup remover|wipes",
    re.I,
)

DEPARTMENT_BLOCK = {
    "perfume": re.compile(r"empty bottle|atomizer only|perfume tray|perfume organizer|deodorant", re.I),
    "makeup": re.compile(r"remover|wipe|cleaner|case|bag|mirror", re.I),
    "skincare": re.compile(r"setting spray|towel|cloth|tool|brush|massager|razor|supplement", re.I),
    "kitchen": re.compile(r"replacement|accessor|liner|filter|recipe|cover only", re.I),
    "home": re.compile(r"rug tape|rug gripper|curtain rod|draft stopper|window film|tumbler|moving bag", re.I),
    "accessories": re.compile(r"organizer insert|holder strap|costume|ring sizer|grabber tool|piercing|nose ring|for sports", re.I),
}

KNOWN_BRANDS = sorted(
    {
        "The Ordinary", "La Roche-Posay", "NYX Professional Makeup", "L'Oreal Paris",
        "L’Oreal Paris", "L’Oreal", "LAURA GELLER", "Mighty Patch Hero Cosmetics",
        "Maybelline New York", "e.l.f.", "Wet n Wild", "Physicians Formula",
        "Hero Cosmetics", "Clean Skin Club", "Beauty of Joseon", "COSRX", "CeraVe",
        "Paula's Choice", "Neutrogena", "PanOxyl", "Medicube", "BIODANCE", "Good Molecules",
        "Instant Pot", "Hamilton Beach", "BLACK+DECKER", "KitchenAid", "Nespresso",
        "Ninja", "Keurig", "Cuisinart", "DASH", "bella", "Magic Bullet", "Vitamix",
        "Utopia Bedding", "Amazon Basics", "Americanflat", "Gorilla Grip", "H.VERSAILTEX",
        "OLANLY", "NICETOWN", "GODONLIF", "LaVie Home", "RELEANY", "ChrisDowa",
        "Rubbermaid", "HOMESURE", "Kitsure", "Veken", "Vtopmart", "TICONN",
        "Kitsch", "PAVOI", "SOJOS", "Fossil", "Michael Kors", "Coach", "TOPACC",
        "Tipmile", "FURTALK", "Airkit", "GUVIVI", "JASGOOD", "XZQTIVE", "Gokeey",
        "LILIE&WHITE", "Jewlpire", "LOLIAS", "Fesciory", "ORANGELOVE", "Wonderskin",
        "Julep", "Revlon", "Clinique", "Vanicream", "EltaMD", "Naturium", "Dr.Althea",
        "Turelar", "Cosori", "Nutribullet", "CHICHAUS", "Crock-Pot", "AROMA", "Elite Gourmet",
        "Chefman", "OVENTE", "upsimples",
        "Yves Saint Laurent", "Victoria's Secret", "Swiss Arabian", "Giorgio Armani",
        "Dolce & Gabbana", "Carolina Herrera", "Jean Paul Gaultier", "Ariana Grande",
        "Billie Eilish", "Sabrina Carpenter", "Calvin Klein", "Ralph Lauren", "Britney Spears",
        "Elizabeth Arden", "Maison Alhambra", "Al Haramain", "Fragrance World", "Sol de Janeiro",
        "Maison Margiela", "Juliette Has a Gun", "Marc Jacobs", "Viktor & Rolf", "Tom Ford",
        "Paco Rabanne", "Lucky Brand", "Ed Hardy", "Kate Spade", "Paris Hilton", "Perry Ellis",
        "Lattafa", "Afnan", "Rasasi", "Armaf", "Pacifica", "Dossier", "Nemat", "Mugler",
        "Versace", "Gucci", "Burberry", "Prada", "Dior", "Chanel", "Valentino", "Givenchy",
        "Lancôme", "Clinique", "Coach", "Nautica", "Davidoff", "Montblanc", "Rabanne",
        "Azzaro", "Guess", "Jimmy Choo", "Issey Miyake", "Tommy Hilfiger", "Vera Wang",
        "Jovan", "Curve", "Cuba",
    },
    key=len,
    reverse=True,
)

TYPE_RULES = {
    "perfume": {
        "skin-musk": r"musk|skin scent|clean|cotton|cashmere|ambrette",
        "fresh-citrus": r"fresh|citrus|bergamot|lemon|orange|aqua|marine|ocean|blue",
        "floral-powdery": r"floral|rose|jasmine|iris|violet|gardenia|blossom|powder",
        "green-woody": r"wood|woody|oud|cedar|sandal|vetiver|green|forest|tobacco",
        "gourmand-vanilla": r"vanilla|gourmand|caramel|candy|chocolate|coffee|sweet|coconut",
        "amber-spicy": r"amber|spice|spicy|intense|elixir|oriental|warm",
    },
    "makeup": {
        "complexion": r"foundation|concealer|powder|primer|setting spray",
        "lips": r"lip|gloss",
        "eyes": r"mascara|liner|shadow",
        "cheeks": r"blush|bronzer|highlighter",
        "brows": r"brow",
        "tools": r"brush|sponge|puff|curler",
    },
    "skincare": {
        "cleanser": r"cleanser|wash|cleansing|balm",
        "moisturizer": r"moist|cream|lotion",
        "sunscreen": r"sunscreen|spf",
        "serum": r"serum|essence|ampoule|oil",
        "exfoliant": r"exfol|acid|peel|toner|retinol",
        "mask": r"mask|patch",
        "body": r"body|hand|foot",
    },
    "kitchen": {
        "coffee": r"coffee|espresso",
        "air-frying": r"air fryer|airfryer",
        "blending": r"blend|processor|chopper|juicer",
        "baking": r"mixer|waffle|baker|oven",
        "meal-prep": r"cooker|pot|steamer|griddle",
        "breakfast": r"toaster|kettle|egg|breakfast",
    },
    "home": {
        "lighting": r"lamp|light|candle",
        "textiles": r"pillow|rug|curtain|blanket|throw",
        "storage": r"basket|storage|organizer|holder",
        "tabletop": r"tray|vase|coaster|table",
        "wall-decor": r"frame|mirror|clock|art|wall",
        "scent": r"diffuser|candle|fragrance",
    },
        "accessories": {
        "jewelry": r"earring|necklace|bracelet|ring|brooch|pin|jewel",
        "handbags": r"bag|purse|wallet|tote|clutch",
        "hair": r"headband|clip|scrunch|hair",
        "belts": r"belt",
        "scarves": r"scarf|shawl|wrap",
        "eyewear": r"sunglass|eyewear|glasses",
        "hats": r"hat|cap|beanie",
    },
}

PRIORITY_RULES = {
    "perfume": {
        "longevity": r"long.?lasting|intense|elixir|parfum|extrait",
        "subtlety": r"skin|clean|soft|light|fresh",
        "uniqueness": r"niche|unisex|oud|artisan|rare",
        "versatility": r"everyday|daily|classic|signature",
        "compliments": r"bold|seductive|sexy|statement",
        "layering": r"layer|musk|oil",
        "comfort": r"vanilla|cashmere|warm|cozy|coconut",
    },
    "makeup": {
        "natural": r"natural|sheer|tinted|skin tint",
        "long-wear": r"long.?wear|24.?hour|waterproof|stay",
        "sensitive": r"sensitive|hypoallergenic|fragrance.?free",
        "travel": r"mini|compact|travel|stick",
        "beginner": r"easy|pencil|crayon|one step",
        "bold": r"bold|vivid|intense|volume|dramatic",
    },
    "skincare": {
        "hydration": r"hydrat|moist|hyaluronic|plump",
        "sensitive": r"sensitive|gentle|soothing|calm",
        "acne": r"acne|pimple|blemish|benzoyl|salicylic",
        "brightening": r"bright|vitamin c|glow|tone",
        "barrier": r"barrier|ceramide|repair",
        "anti-aging": r"retinol|peptide|firm|wrinkle|elastic",
    },
    "kitchen": {
        "compact": r"compact|mini|slim|personal|space",
        "easy-clean": r"dishwasher|easy.?clean|nonstick|removable",
        "speed": r"rapid|quick|fast|express|instant",
        "quiet": r"quiet|silent",
        "family-size": r"large|family|quart|12.?cup|14.?cup",
        "multi-use": r"multi|combo|[0-9]+.?in.?1|versatile",
    },
    "home": {
        "small-space": r"small|compact|slim|apartment",
        "washable": r"washable|machine wash|easy.?clean",
        "neutral": r"white|cream|beige|linen|neutral|black",
        "statement": r"gold|velvet|sculpt|decorative|bold",
        "durable": r"heavy.?duty|shatter|metal|solid|durable",
        "renter-friendly": r"adhesive|removable|no drill|hanging",
    },
    "accessories": {
        "everyday": r"everyday|classic|simple|basic",
        "statement": r"chunky|statement|oversized|bold",
        "travel": r"travel|fold|pack|case",
        "adjustable": r"adjustable|stretch|elastic",
        "giftable": r"gift|box|set",
        "minimal": r"minimal|slim|delicate|small|tiny",
    },
}

AVOID_RULES = {
    "perfume": {"sweet": r"sweet|candy|caramel|gourmand", "powdery": r"powder|iris|violet", "floral": r"floral|rose|jasmine|flower", "citrus": r"citrus|lemon|bergamot|orange", "musk": r"musk", "vanilla": r"vanilla", "woody": r"wood|oud|cedar|sandal", "smoky": r"smok|tobacco|incense", "strong": r"intense|elixir|extrait|powerful"},
    "makeup": {"fragrance": r"fragrance|scented", "shimmer": r"shimmer|glitter|sparkle", "full-coverage": r"full coverage", "waterproof": r"waterproof", "cream": r"cream|liquid", "powder": r"powder"},
    "skincare": {"fragrance": r"fragrance|scented|perfume", "active-heavy": r"retinol|acid|peel|benzoyl", "rich": r"rich|butter|balm", "oil": r"oil", "exfoliating": r"exfol|scrub|peel|acid"},
    "kitchen": {"plastic": r"plastic", "hand-wash": r"hand wash", "large": r"large|family|12.?cup|14.?cup", "single-use": r"single.?serve|one function", "noisy": r"powerful|high.?speed"},
    "home": {"glass": r"glass|mirror", "scented": r"scent|fragrance|candle|diffuser", "synthetic": r"polyester|microfiber|plastic", "assembly": r"assembly|install|mount", "oversized": r"large|oversized|[6-9]x[6-9]"},
    "accessories": {"gold-tone": r"gold", "silver-tone": r"silver", "logo": r"logo|branded", "synthetic": r"polyester|plastic|faux|pu leather", "delicate": r"delicate|thin|tiny"},
}


def request_text(url: str) -> str:
    request = urllib.request.Request(
        url,
        headers={"User-Agent": USER_AGENT, "Accept-Language": "en-US,en;q=0.9"},
    )
    for attempt in range(3):
        try:
            with urllib.request.urlopen(request, timeout=30) as response:
                return response.read().decode("utf-8", errors="replace")
        except (urllib.error.URLError, TimeoutError):
            if attempt == 2:
                raise
            time.sleep(1.5 * (attempt + 1))
    raise RuntimeError("Amazon request did not complete")


def search_document(query: str, page: int) -> Any:
    """Fetch a populated Amazon search page, retrying empty throttle pages."""
    last_count = 0
    for attempt in range(4):
        params = urllib.parse.urlencode(
            {"k": query, "page": page, "qid": int(time.time()) + attempt}
        )
        document = html.fromstring(request_text(f"https://www.amazon.com/s?{params}"))
        last_count = len(
            document.xpath("//*[@data-component-type='s-search-result' and @data-asin]")
        )
        if last_count >= 8:
            time.sleep(0.7)
            return document
        time.sleep(2.0 * (attempt + 1))
    raise RuntimeError(
        f"Amazon returned an incomplete search page for {query!r} page {page} ({last_count} items)"
    )


def clean_spaces(value: str) -> str:
    return re.sub(r"\s+", " ", value).strip()


def brand_and_name(title: str) -> tuple[str, str]:
    cleaned = clean_spaces(title).replace("\ufffd", "")
    cleaned = re.sub(r"^Sponsored Ad\s*[-:]\s*", "", cleaned, flags=re.I)
    brand = next((name for name in KNOWN_BRANDS if cleaned.lower().startswith(name.lower())), "")
    if not brand:
        brand = re.split(r"\s+", cleaned, maxsplit=1)[0].strip("-–—|,")
    if re.fullmatch(r"\d+(?:mm|x\d+)?", brand, re.I) or brand.lower() in {
        "candle", "chunky", "headbands", "hypoallergenic", "linen", "vacuum", "womengifts"
    }:
        brand = "Amazon Find"
    if brand == "Mighty Patch Hero Cosmetics":
        brand = "Hero Cosmetics"
        cleaned = cleaned.replace("Mighty Patch Hero Cosmetics", "Hero Cosmetics Mighty Patch", 1)
    remaining = cleaned if brand == "Amazon Find" else cleaned[len(brand):].lstrip(" -–—|,")
    name = re.split(r"\s*\|\s*|\s+-\s+|\s+with\s+", remaining, maxsplit=1, flags=re.I)[0]
    name = re.sub(r"\s+\(?Pack of.*$|\s+\d+\s*(?:Count|Ct)\b.*$", "", name, flags=re.I)
    name = clean_spaces(name)[:82].rstrip(" -–—|,")
    return brand[:42], name or cleaned[:82]


def price_tier(card: Any) -> int:
    prices = card.xpath(
        ".//span[contains(@class,'p13n-sc-price')]/text() | "
        ".//span[contains(@class,'a-price')]//span[contains(@class,'a-offscreen')]/text()"
    )
    if not prices:
        return 0
    match = re.search(r"([0-9]+(?:[.,][0-9]+)?)", clean_spaces(prices[0]).replace(",", ""))
    if not match:
        return 0
    value = float(match.group(1))
    return 1 if value < 30 else 2 if value < 100 else 3 if value < 250 else 4


def classify(title: str, rules: dict[str, str], fallback: str) -> list[str]:
    matches = [key for key, pattern in rules.items() if re.search(pattern, title, re.I)]
    return matches[:3] or [fallback]


def image_url(image: Any) -> str:
    srcset = clean_spaces(image.get("srcset", ""))
    choices = [part.strip().split(" ", 1)[0] for part in srcset.split(",") if part.strip()]
    source = choices[-1] if choices else image.get("src", "")
    return source.replace("http://", "https://")


def duplicate_key(brand: str, name: str) -> str:
    value = clean_spaces(f"{brand} {name}").lower()
    value = re.sub(r"\b(?:pack|set) of \d+\b|\b\d+\s*(?:count|ct)\b", "", value)
    return re.sub(r"[^a-z0-9]+", " ", value).strip()


def entry_from_card(department: str, card: Any, fallback_type: str) -> dict[str, Any] | None:
    asin = card.get("data-asin", "").strip()
    images = card.xpath(".//img[@src]")
    if not asin or not images:
        return None
    title = clean_spaces(images[0].get("alt", ""))
    if not title:
        title = clean_spaces(" ".join(card.xpath(".//h2//text()")))
    if (
        not title
        or BLOCK.search(title)
        or DEPARTMENT_BLOCK[department].search(title)
        or not ALLOW[department].search(title)
    ):
        return None
    brand, name = brand_and_name(title)
    types = classify(title, TYPE_RULES[department], fallback_type)
    if fallback_type not in types:
        types = [fallback_type, *types][:3]
    priorities = classify(title, PRIORITY_RULES[department], next(iter(PRIORITY_RULES[department])))
    avoid = [key for key, pattern in AVOID_RULES[department].items() if re.search(pattern, title, re.I)][:3]
    return {
        "id": f"{department}-{asin.lower()}",
        "department": department,
        "brand": brand,
        "name": name,
        "priceTier": price_tier(card),
        "priceLabel": "See current price on Amazon",
        "productUrl": f"https://www.amazon.com/dp/{asin}",
        "affiliateUrl": "",
        "imageUrl": image_url(images[0]),
        "imageCredit": "Amazon product photography",
        "types": types,
        "priorities": priorities,
        "avoid": avoid,
        "tags": list(dict.fromkeys(types + priorities))[:4],
        "summary": f"A {types[0].replace('-', ' ')} option from {brand}, found in Amazon's current catalogue.",
        "amazonAsin": asin,
        "catalogueChecked": CHECKED_DATE,
    }


def scrape_department(
    department: str,
    target: int,
    excluded_titles: set[str] | None = None,
) -> list[dict[str, Any]]:
    candidates: list[dict[str, Any]] = []
    seen_asins: set[str] = set()
    seen_titles = set(excluded_titles or set())

    def collect(document: Any, fallback_type: str, max_add: int | None = None) -> int:
        added = 0
        cards = document.xpath("//*[@data-component-type='s-search-result' and @data-asin]")
        if not cards:
            cards = document.xpath("//*[@data-asin and string-length(@data-asin)>0]")
        for card in cards:
            entry = entry_from_card(department, card, fallback_type)
            if not entry:
                continue
            asin = entry["amazonAsin"]
            title_key = duplicate_key(entry["brand"], entry["name"])
            if asin in seen_asins or title_key in seen_titles:
                continue
            candidates.append(entry)
            seen_asins.add(asin)
            seen_titles.add(title_key)
            added += 1
            if len(candidates) == target or (max_add is not None and added == max_add):
                break
        return added

    # The concise Best Sellers pages are useful for small editorial refreshes.
    # At 100+ items, targeted searches provide much better type diversity.
    for source in SOURCES.get(department, []) if target < 100 else []:
        for page in (1, 2):
            joiner = "&" if "?" in source else "?"
            document = html.fromstring(request_text(f"{source}{joiner}pg={page}"))
            collect(document, next(iter(TYPE_RULES[department])))
            print(f"{department}: {len(candidates)}/{target}", flush=True)
            if len(candidates) == target:
                return candidates

    searches = SEARCHES[department]
    type_totals = {
        type_name: target // len(TYPE_RULES[department])
        + (index < target % len(TYPE_RULES[department]))
        for index, type_name in enumerate(TYPE_RULES[department])
    }
    type_occurrences = {
        type_name: sum(fallback == type_name for _, fallback in searches)
        for type_name in TYPE_RULES[department]
    }
    used_per_type = {type_name: 0 for type_name in TYPE_RULES[department]}
    query_limits: list[int] = []
    for _, fallback_type in searches:
        occurrence = used_per_type[fallback_type]
        count = type_occurrences[fallback_type]
        total = type_totals[fallback_type]
        query_limits.append(total // count + (occurrence < total % count))
        used_per_type[fallback_type] += 1
    query_counts = [0] * len(searches)

    for page in (1, 2):
        for query_index, (query, fallback_type) in enumerate(searches):
            remaining = query_limits[query_index] - query_counts[query_index]
            if remaining <= 0:
                continue
            document = search_document(query, page)
            query_counts[query_index] += collect(document, fallback_type, remaining)
            print(f"{department}: {len(candidates)}/{target}", flush=True)
            if len(candidates) == target:
                return candidates

    # If a narrow query could not fill its share, reuse the unselected results
    # from every query before declaring the department incomplete.
    for page in (1, 2):
        for query, fallback_type in searches:
            document = search_document(query, page)
            collect(document, fallback_type)
            if len(candidates) == target:
                return candidates
    raise RuntimeError(f"Only {len(candidates)} usable {department} products were found; {target} required")


def amazon_search(brand: str, name: str) -> str:
    query = urllib.parse.quote_plus(clean_spaces(f"{brand} {name}"))
    return f"https://www.amazon.com/s?k={query}"


def perfume_catalogue(existing: list[dict[str, Any]]) -> list[dict[str, Any]]:
    perfumes = [
        item
        for item in existing
        if item.get("department", "perfume") == "perfume"
        and (
            not item.get("amazonAsin")
            or not DEPARTMENT_BLOCK["perfume"].search(f"{item.get('brand', '')} {item.get('name', '')}")
        )
    ]
    for item in perfumes:
        item["department"] = "perfume"
        item["types"] = item.get("families") or item.get("types") or ["skin-musk"]
        item["tags"] = item.get("notes", [])[:4]
        if not item["tags"]:
            item["tags"] = list(dict.fromkeys(item["types"] + item.get("priorities", [])))[:4]
        item["avoid"] = item.get("traits") or item.get("avoid") or []
        item["productUrl"] = (
            f"https://www.amazon.com/dp/{item['amazonAsin']}"
            if item.get("amazonAsin")
            else amazon_search(item["brand"], item["name"])
        )
        item["affiliateUrl"] = ""
        item["priceLabel"] = "See current price on Amazon"
        item["imageCredit"] = f"{item['brand']} product photography"
        item["catalogueChecked"] = CHECKED_DATE
        item.pop("sourceImageUrl", None)
    return perfumes


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--per-department", type=int, default=DEFAULT_PER_DEPARTMENT)
    parser.add_argument(
        "--refresh",
        action="store_true",
        help="Re-fetch departments that already meet the requested size.",
    )
    args = parser.parse_args()
    existing = json.loads(PRODUCTS_PATH.read_text(encoding="utf-8"))
    perfumes = perfume_catalogue(existing)[: args.per_department]
    if len(perfumes) < args.per_department:
        existing_titles = {duplicate_key(item["brand"], item["name"]) for item in perfumes}
        perfumes.extend(
            scrape_department(
                "perfume",
                args.per_department - len(perfumes),
                excluded_titles=existing_titles,
            )
        )
    catalogue = perfumes
    print(f"perfume: {len(perfumes)}", flush=True)
    for department in SOURCES:
        current = [item for item in existing if item.get("department") == department]
        products = (
            current[: args.per_department]
            if not args.refresh and len(current) >= args.per_department
            else scrape_department(department, args.per_department)
        )
        catalogue.extend(products)
        print(f"{department}: {len(products)}", flush=True)
    PRODUCTS_PATH.write_text(
        json.dumps(catalogue, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    print(f"Wrote {len(catalogue)} products to {PRODUCTS_PATH}")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as error:  # noqa: BLE001 - give a concise build failure
        print(f"Catalogue build failed: {error}", file=sys.stderr)
        raise
