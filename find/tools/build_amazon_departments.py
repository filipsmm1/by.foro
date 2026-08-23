"""Build the non-fragrance departments for the by.foro Finder.

The script keeps the existing editorial perfume catalogue, changes its shopping
destinations to Amazon searches, and adds five current Amazon departments. It
stores Amazon-hosted thumbnail URLs rather than copying Amazon product images.
That keeps the catalogue light and leaves product graphics on Amazon's servers.
"""

from __future__ import annotations

import argparse
import json
import math
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

ALLOW = {
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
    r"refill|replacement|liner|filter only|gift card|subscription|book|costume|cleaning cloth|makeup remover|wipes",
    re.I,
)

DEPARTMENT_BLOCK = {
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
    },
    key=len,
    reverse=True,
)

TYPE_RULES = {
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


def clean_spaces(value: str) -> str:
    return re.sub(r"\s+", " ", value).strip()


def brand_and_name(title: str) -> tuple[str, str]:
    cleaned = clean_spaces(title).replace("�", "")
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
    name = re.split(r"\s*[|,]\s*|\s+-\s+|\s+with\s+", remaining, maxsplit=1, flags=re.I)[0]
    name = re.sub(r"\s+\(?Pack of.*$|\s+\d+\s*(?:Count|Ct)\b.*$", "", name, flags=re.I)
    name = clean_spaces(name)[:82].rstrip(" -–—|,")
    return brand[:42], name or cleaned[:82]


def price_tier(card: Any) -> int:
    prices = card.xpath(".//span[contains(@class,'p13n-sc-price')]/text()")
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


def scrape_department(department: str, target: int) -> list[dict[str, Any]]:
    candidates: list[dict[str, Any]] = []
    seen: set[str] = set()
    source_quota = math.ceil(target / len(SOURCES[department]))
    for source in SOURCES[department]:
        source_start = len(candidates)
        for page in (1, 2):
            joiner = "&" if "?" in source else "?"
            document = html.fromstring(request_text(f"{source}{joiner}pg={page}"))
            for card in document.xpath("//*[@data-asin and string-length(@data-asin)>0]"):
                asin = card.get("data-asin", "").strip()
                if not asin or asin in seen:
                    continue
                image = card.xpath(".//img[@src]")
                if not image:
                    continue
                title = clean_spaces(image[0].get("alt", ""))
                if not title or BLOCK.search(title) or DEPARTMENT_BLOCK[department].search(title) or not ALLOW[department].search(title):
                    continue
                brand, name = brand_and_name(title)
                types = classify(title, TYPE_RULES[department], next(iter(TYPE_RULES[department])))
                priorities = classify(title, PRIORITY_RULES[department], next(iter(PRIORITY_RULES[department])))
                avoid = [key for key, pattern in AVOID_RULES[department].items() if re.search(pattern, title, re.I)][:3]
                image_url = image[0].get("src", "").replace("http://", "https://")
                candidates.append(
                    {
                        "id": f"{department}-{asin.lower()}",
                        "department": department,
                        "brand": brand,
                        "name": name,
                        "priceTier": price_tier(card),
                        "priceLabel": "See current price on Amazon",
                        "productUrl": f"https://www.amazon.com/dp/{asin}",
                        "affiliateUrl": "",
                        "imageUrl": image_url,
                        "imageCredit": "Amazon product photography",
                        "types": types,
                        "priorities": priorities,
                        "avoid": avoid,
                        "tags": list(dict.fromkeys(types + priorities))[:4],
                        "summary": f"A {types[0].replace('-', ' ')} option from {brand}, selected from Amazon's current category listings.",
                        "amazonAsin": asin,
                        "catalogueChecked": CHECKED_DATE,
                    }
                )
                seen.add(asin)
                if len(candidates) - source_start >= source_quota or len(candidates) == target:
                    break
            if len(candidates) - source_start >= source_quota or len(candidates) == target:
                break
        if len(candidates) == target:
            return candidates
    raise RuntimeError(f"Only {len(candidates)} usable {department} products were found; {target} required")


def amazon_search(brand: str, name: str) -> str:
    query = urllib.parse.quote_plus(clean_spaces(f"{brand} {name}"))
    return f"https://www.amazon.com/s?k={query}"


def perfume_catalogue(existing: list[dict[str, Any]]) -> list[dict[str, Any]]:
    perfumes = [item for item in existing if item.get("department", "perfume") == "perfume"]
    for item in perfumes:
        item["department"] = "perfume"
        item["types"] = item.get("families", ["skin-musk"])
        item["tags"] = item.get("notes", [])[:4]
        item["avoid"] = item.get("traits", [])
        item["productUrl"] = amazon_search(item["brand"], item["name"])
        item["affiliateUrl"] = ""
        item["priceLabel"] = "See current price on Amazon"
        item["imageCredit"] = f"{item['brand']} product photography"
        item["catalogueChecked"] = CHECKED_DATE
        item.pop("sourceImageUrl", None)
    return perfumes


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--per-department", type=int, default=24)
    args = parser.parse_args()
    existing = json.loads(PRODUCTS_PATH.read_text(encoding="utf-8"))
    catalogue = perfume_catalogue(existing)
    for department in SOURCES:
        products = scrape_department(department, args.per_department)
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
