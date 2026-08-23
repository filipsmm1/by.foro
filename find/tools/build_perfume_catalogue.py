#!/usr/bin/env python3
"""Build the static by.foro perfume catalogue from sourced product listings.

The script keeps the hand-edited products already in ``products.json`` and adds
current products from retailer listing pages. Product detail copy supplies the
fragrance family and key notes. Images are saved locally on white backgrounds
as compact WebP files with JPEG fallbacks. Shopping links point to Amazon.

This is an editorial data preparation tool, not a live price feed. Re-run it
before a major catalogue update and review the resulting diff before publishing.
"""

from __future__ import annotations

import argparse
import io
import json
import re
import sys
import unicodedata
import urllib.error
import urllib.parse
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from typing import Any, Iterable

from PIL import Image, ImageOps


ROOT = Path(__file__).resolve().parents[2]
FINDER = ROOT / "find"
PRODUCTS_PATH = FINDER / "products.json"
IMAGE_DIR = FINDER / "assets" / "products"
LISTING_URL = "https://www.ulta.com/shop/fragrance/all?fragrance+type=eau_de_parfum&page={page}"
USER_AGENT = "byforo.com perfume-finder/1.0 (editorial catalogue; contact@byforo.com)"
TARGET_COUNT = 150

BLOCKED_PRODUCT_WORDS = re.compile(
    r"\b(set|duo|trio|discovery|rollerball|travel spray|refill|body mist|"
    r"hair mist|lotion|deodorant)\b",
    re.I,
)

FAMILY_RULES = {
    "skin-musk": (
        "musk", "musky", "ambrette", "skin scent", "cashmere", "cashmeran",
        "aldehyd", "clean cotton",
    ),
    "fresh-citrus": (
        "citrus", "bergamot", "lemon", "lime", "mandarin", "orange", "grapefruit",
        "aquatic", "marine", "sea salt", "ozonic", "fresh", "water accord", "ginger",
    ),
    "floral-powdery": (
        "floral", "rose", "jasmine", "tuberose", "iris", "violet", "lavender",
        "orange blossom", "peony", "gardenia", "magnolia", "ylang", "orchid",
        "lily", "freesia", "geranium", "neroli", "hibiscus",
    ),
    "green-woody": (
        "wood", "woody", "sandalwood", "cedar", "vetiver", "patchouli", "moss",
        "green", "herbal", "oak", "pine", "cypress", "fig leaf", "earthy",
    ),
    "gourmand-vanilla": (
        "vanilla", "gourmand", "caramel", "chocolate", "coffee", "praline", "coconut",
        "tonka", "almond", "marshmallow", "sugar", "honey", "cream", "milk", "cacao",
        "pistachio", "pastry", "cake",
    ),
    "amber-spicy": (
        "amber", "spicy", "spice", "incense", "leather", "tobacco", "saffron",
        "pepper", "cardamom", "cinnamon", "resin", "oud", "labdanum", "rum",
        "bourbon", "smoky",
    ),
}

FAMILY_LABELS = {
    "skin-musk": "soft musk",
    "fresh-citrus": "fresh citrus",
    "floral-powdery": "floral",
    "green-woody": "green woods",
    "gourmand-vanilla": "gourmand warmth",
    "amber-spicy": "amber and spice",
}


def request_bytes(url: str, timeout: int = 45) -> bytes:
    request = urllib.request.Request(
        url,
        headers={
            "User-Agent": USER_AGENT,
            "Accept": "text/html,application/xhtml+xml,application/json,image/avif,image/webp,image/*,*/*;q=0.8",
        },
    )
    with urllib.request.urlopen(request, timeout=timeout) as response:
        return response.read()


def apollo_state(page: str) -> dict[str, Any]:
    marker = "window.__APOLLO_STATE__ = "
    position = page.index(marker) + len(marker)
    state, _ = json.JSONDecoder().raw_decode(page[position:])
    return state


def walk(value: Any) -> Iterable[Any]:
    yield value
    if isinstance(value, dict):
        for child in value.values():
            yield from walk(child)
    elif isinstance(value, list):
        for child in value:
            yield from walk(child)


def listing_products(page: str) -> list[dict[str, Any]]:
    found: dict[str, dict[str, Any]] = {}
    for value in walk(apollo_state(page)):
        if not isinstance(value, dict):
            continue
        if not value.get("productName") or not value.get("brandName"):
            continue
        if not isinstance(value.get("image"), dict) or not value["image"].get("imageUrl"):
            continue
        if not value.get("productId") or not value.get("action", {}).get("url"):
            continue
        found.setdefault(value["productId"], value)
    return list(found.values())


def normalise(value: str) -> str:
    value = unicodedata.normalize("NFKD", value)
    value = "".join(character for character in value if not unicodedata.combining(character))
    return re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")


def product_key(brand: str, name: str) -> str:
    cleaned = re.sub(
        r"\b(eau de parfum|eau de toilette|parfum|spray|limited edition)\b",
        " ",
        name,
        flags=re.I,
    )
    return normalise(f"{brand} {cleaned}")


def markdown_section(markdown: str, heading: str) -> list[str]:
    match = re.search(
        rf"####\s+{re.escape(heading)}\s*(.*?)(?=\n####|\nItem\s+\d+|\Z)",
        markdown,
        flags=re.I | re.S,
    )
    if not match:
        return []
    values = []
    for line in match.group(1).splitlines():
        line = re.sub(r"^\s*[-*]\s*", "", line).strip()
        if line:
            values.append(line)
    return values


def clean_notes(lines: list[str]) -> list[str]:
    notes: list[str] = []
    for line in lines:
        line = re.sub(
            r"^(top(?:\s+notes?)?|middle(?:\s+notes?)?|mid(?:\s+notes?)?|"
            r"heart(?:\s+notes?)?|base(?:\s+notes?)?|dry(?:\s+notes?)?|"
            r"key notes?|notes?)\s*(?:[-:–]|\bof\b)?\s*",
            "",
            line,
            flags=re.I,
        )
        for part in re.split(r",|\s+[&+]\s+|\s+and\s+|\s+are amplified by\s+|\s+is enveloped in\s+", line):
            part = re.sub(r"^(intertwined with|wrapped in|blended with|built around)\s+", "", part, flags=re.I)
            part = re.sub(r"\([^)]*\)", "", part).strip(" .;:-–")
            if (
                part
                and len(part) <= 60
                and not any(fragment in part.lower() for fragment in ("open the fragrance", "heightening the scent", "the fragrance opens"))
                and part.lower() not in {item.lower() for item in notes}
            ):
                notes.append(part)
    return notes[:8]


def product_detail(url: str) -> dict[str, Any]:
    page = request_bytes(url).decode("utf-8", errors="replace")
    state = apollo_state(page)
    descriptions = [
        value["description"]
        for value in walk(state)
        if isinstance(value, dict)
        and isinstance(value.get("description"), str)
        and ("Fragrance Family" in value["description"] or "Key Notes" in value["description"])
    ]
    markdown = max(descriptions, key=len) if descriptions else ""
    families = markdown_section(markdown, "Fragrance Family")
    notes = clean_notes(markdown_section(markdown, "Key Notes"))
    features = markdown_section(markdown, "Features")
    return {
        "officialFamily": "; ".join(families[:3]),
        "notes": notes,
        "features": features[:3],
    }


def parse_max_price(label: str) -> float:
    prices = [float(value.replace(",", "")) for value in re.findall(r"\$([\d,.]+)", label or "")]
    return max(prices, default=0)


def price_tier(label: str) -> int:
    price = parse_max_price(label)
    if price <= 75:
        return 1
    if price <= 150:
        return 2
    if price <= 250:
        return 3
    return 4


def classify_families(name: str, official_family: str, notes: list[str], features: list[str]) -> list[str]:
    haystack = " ".join([name, official_family, *notes, *features]).lower()
    scores = {
        family: sum(1 for keyword in keywords if keyword in haystack)
        for family, keywords in FAMILY_RULES.items()
    }
    ranked = sorted(scores, key=lambda family: (-scores[family], family))
    selected = [family for family in ranked if scores[family] > 0][:2]
    if not selected:
        selected = ["floral-powdery"]
    return selected


def classify_intensity(name: str, families: list[str]) -> str:
    lower = name.lower()
    if any(word in lower for word in ("intense", "intensely", "elixir", "absolu", "extreme", "black", "night")):
        return "noticeable"
    if any(word in lower for word in ("light", "fresh", "aqua", "eau tendre", "11 11", "skin")):
        return "intimate"
    if any(word in lower for word in ("opium", "alien", "spicebomb", "flowerbomb", "most wanted", "stronger with you")):
        return "noticeable"
    return "balanced"


def traits_for(families: list[str], intensity: str, text: str) -> list[str]:
    lower = text.lower()
    traits = []
    keyword_traits = {
        "sweet": ("sweet", "sugar", "caramel", "praline", "honey", "gourmand"),
        "powdery": ("powder", "iris", "violet"),
        "floral": ("floral", "rose", "jasmine", "tuberose", "flower", "peony", "gardenia"),
        "citrus": ("citrus", "bergamot", "lemon", "lime", "mandarin", "grapefruit"),
        "musk": ("musk", "ambrette"),
        "vanilla": ("vanilla",),
        "woody": ("wood", "cedar", "vetiver", "sandalwood", "patchouli", "oak"),
        "smoky": ("smok", "incense", "tobacco", "leather"),
    }
    for trait, keywords in keyword_traits.items():
        if any(keyword in lower for keyword in keywords):
            traits.append(trait)
    if not traits:
        fallback_traits = {
            "skin-musk": "musk",
            "floral-powdery": "floral",
            "green-woody": "woody",
            "gourmand-vanilla": "sweet",
        }
        for family in families:
            if family in fallback_traits:
                traits.append(fallback_traits[family])
                break
    if intensity == "noticeable":
        traits.append("strong")
    return list(dict.fromkeys(traits))


def profile_for(name: str, official_family: str, notes: list[str], features: list[str]) -> dict[str, Any]:
    families = classify_families(name, official_family, notes, features)
    intensity = classify_intensity(name, families)

    occasions = []
    textures = []
    priorities = []
    for family in families:
        if family == "skin-musk":
            occasions += ["everyday", "office", "date", "versatile"]
            textures += ["clean", "creamy", "powdery"]
            priorities += ["subtlety", "layering", "comfort", "versatility"]
        elif family == "fresh-citrus":
            occasions += ["everyday", "office", "warm-weather", "versatile"]
            textures += ["clean", "juicy"]
            priorities += ["versatility", "comfort", "layering"]
        elif family == "floral-powdery":
            occasions += ["everyday", "date", "evening", "warm-weather", "versatile"]
            textures += ["powdery", "juicy"]
            priorities += ["versatility", "compliments", "comfort"]
        elif family == "green-woody":
            occasions += ["office", "evening", "cold-weather", "versatile"]
            textures += ["dry", "clean"]
            priorities += ["longevity", "uniqueness", "versatility"]
        elif family == "gourmand-vanilla":
            occasions += ["date", "evening", "cold-weather"]
            textures += ["creamy", "powdery"]
            priorities += ["longevity", "compliments", "comfort"]
        elif family == "amber-spicy":
            occasions += ["date", "evening", "cold-weather"]
            textures += ["dry", "smoky"]
            priorities += ["longevity", "compliments", "uniqueness"]

    if intensity == "intimate":
        priorities += ["subtlety", "layering"]
    elif intensity == "noticeable":
        priorities += ["longevity", "compliments"]

    text = " ".join([name, official_family, *notes, *features])
    return {
        "families": list(dict.fromkeys(families)),
        "intensity": intensity,
        "occasions": list(dict.fromkeys(occasions)),
        "textures": list(dict.fromkeys(textures))[:3],
        "traits": traits_for(families, intensity, text),
        "priorities": list(dict.fromkeys(priorities))[:4],
    }


def editorial_summary(product: dict[str, Any], profile: dict[str, Any]) -> str:
    notes = product["notes"][:3]
    note_phrase = ", ".join(notes[:-1]) + (f" and {notes[-1]}" if len(notes) > 1 else notes[0] if notes else "")
    directions = [FAMILY_LABELS[family] for family in profile["families"][:2]]
    direction = directions[0] if len(directions) == 1 else f"{directions[0]} and {directions[1]}"
    if note_phrase:
        return (
            f"An eau de parfum combining {direction}, built around {note_phrase}. "
            f"It suits a {profile['intensity']} scent brief and is best treated as a skin test, not a blind buy."
        )
    return (
        f"An eau de parfum in the {direction} direction with a {profile['intensity']} presence. "
        "Check the current note list at the retailer and sample it on skin before choosing a full bottle."
    )


def sample_advice(profile: dict[str, Any]) -> str:
    if profile["intensity"] == "noticeable":
        return "Begin with one spray and wear it for a full afternoon; projection and sweetness can build after the opening."
    if "fresh-citrus" in profile["families"]:
        return "Test the dry-down after the bright opening fades, then compare longevity in the weather where you will wear it."
    if "floral-powdery" in profile["families"]:
        return "Give the floral heart at least an hour on skin, especially if powder or white flowers can become dominant for you."
    return "Wear it on skin for several hours before buying a full bottle; fabric and a paper blotter can hide the true dry-down."


def image_slug(brand: str, name: str, product_id: str) -> str:
    cleaned = re.sub(r"\b(eau de parfum|eau de toilette|parfum|spray)\b", " ", name, flags=re.I)
    base = normalise(f"{brand}-{cleaned}")[:68].strip("-")
    return f"{base}-{normalise(product_id).removeprefix('pimprod')}"


def prepare_image(source_url: str, slug: str) -> None:
    IMAGE_DIR.mkdir(parents=True, exist_ok=True)
    raw = request_bytes(f"{source_url}?w=900&h=900&fmt=jpeg", timeout=60)
    with Image.open(io.BytesIO(raw)) as source:
        image = ImageOps.exif_transpose(source).convert("RGBA")
        image.thumbnail((900, 900), Image.Resampling.LANCZOS)
        background = Image.new("RGB", (900, 900), "#ffffff")
        background.paste(
            image,
            ((900 - image.width) // 2, (900 - image.height) // 2),
            image.getchannel("A"),
        )
        background.save(IMAGE_DIR / f"{slug}.webp", "WEBP", quality=76, method=6)
        background.save(IMAGE_DIR / f"{slug}.jpg", "JPEG", quality=82, optimize=True, progressive=True)


def build_entry(listing: dict[str, Any], detail: dict[str, Any]) -> dict[str, Any]:
    brand = listing["brandName"].strip()
    name = listing["productName"].strip()
    notes = detail["notes"]
    profile = profile_for(name, detail["officialFamily"], notes, detail["features"])
    slug = image_slug(brand, name, listing["productId"])
    price = listing.get("salePrice") or listing.get("listPrice") or "See current price"
    amazon_query = urllib.parse.quote_plus(f"{brand} {name}")
    return {
        "id": slug,
        "brand": brand,
        "name": name,
        "concentration": "Eau de parfum",
        "priceTier": price_tier(price),
        "priceLabel": "See current price on Amazon",
        "productUrl": f"https://www.amazon.com/s?k={amazon_query}",
        "affiliateUrl": "",
        "image": slug,
        "imageCredit": f"{brand} product photography",
        "sourceImageUrl": listing["image"]["imageUrl"],
        **profile,
        "notes": notes[:6],
        "summary": "",
        "sampleAdvice": sample_advice(profile),
        "officialFamily": detail["officialFamily"],
        "rating": listing.get("rating"),
        "reviewCount": listing.get("reviewCount", 0),
        "sourceChecked": "2026-08-23",
    }


def load_listing_pages(cache_paths: list[Path] | None) -> list[dict[str, Any]]:
    products: list[dict[str, Any]] = []
    seen = set()
    for page_number in range(1, 4):
        if cache_paths:
            path = cache_paths[page_number - 1]
            text = path.read_text(encoding="utf-8")
        else:
            text = request_bytes(LISTING_URL.format(page=page_number)).decode("utf-8", errors="replace")
        for product in listing_products(text):
            if product["productId"] not in seen:
                seen.add(product["productId"])
                products.append(product)
    return products


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--listing-cache", nargs=3, type=Path)
    parser.add_argument("--workers", type=int, default=12)
    parser.add_argument("--target", type=int, default=TARGET_COUNT)
    parser.add_argument("--reclassify-only", action="store_true")
    args = parser.parse_args()

    existing = json.loads(PRODUCTS_PATH.read_text(encoding="utf-8"))
    if args.reclassify_only:
        for item in existing:
            if not item.get("sourceChecked"):
                continue
            item["notes"] = clean_notes(item["notes"]) or [item.get("officialFamily", "Fragrance profile")]
            profile = profile_for(item["name"], item["officialFamily"], item["notes"], [])
            item.update(profile)
            item["summary"] = editorial_summary(item, item)
            item["sampleAdvice"] = sample_advice(item)
        PRODUCTS_PATH.write_text(
            json.dumps(existing, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
            newline="\n",
        )
        print(f"Reclassified {sum(bool(item.get('sourceChecked')) for item in existing)} sourced perfumes.")
        return 0

    # Preserve the hand-edited core catalogue and replace the sourced portion on
    # every full refresh. This keeps the command idempotent after the database
    # has already reached its target size.
    editorial = [item for item in existing if not item.get("sourceChecked")]
    if args.target < len(editorial):
        print(
            f"Target {args.target} is smaller than the {len(editorial)} editorial entries.",
            file=sys.stderr,
        )
        return 1

    existing_keys = {product_key(item["brand"], item["name"]) for item in editorial}
    listings = load_listing_pages(args.listing_cache)

    candidates = []
    for item in listings:
        if BLOCKED_PRODUCT_WORDS.search(item["productName"]):
            continue
        key = product_key(item["brandName"], item["productName"])
        if key in existing_keys:
            continue
        # The original editorial database already contains these base scents
        # under shorter names. Flankers such as Intense remain distinct.
        if item["brandName"].lower() == "burberry" and item["productName"].lower() == "burberry goddess eau de parfum":
            continue
        if item["brandName"].lower() == "nemat" and item["productName"].lower() == "amber eau de parfum":
            continue
        candidates.append(item)

    needed = args.target - len(editorial)
    if needed == 0:
        PRODUCTS_PATH.write_text(
            json.dumps(editorial, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
            newline="\n",
        )
        print(f"Wrote {len(editorial)} perfumes to {PRODUCTS_PATH}")
        return 0
    candidates = candidates[: needed + 20]
    details: dict[str, dict[str, Any]] = {}
    failures: list[tuple[str, str]] = []
    with ThreadPoolExecutor(max_workers=args.workers) as pool:
        futures = {
            pool.submit(product_detail, item["action"]["url"]): item
            for item in candidates
        }
        complete = 0
        for future in as_completed(futures):
            item = futures[future]
            try:
                detail = future.result()
                if not detail["notes"]:
                    raise ValueError("official key notes were not found")
                details[item["productId"]] = detail
            except Exception as error:  # noqa: BLE001 - report every failed source cleanly
                failures.append((item["productName"], str(error)))
            complete += 1
            if complete % 20 == 0 or complete == len(futures):
                print(f"details {complete}/{len(futures)}", flush=True)

    added: list[dict[str, Any]] = []
    for listing in candidates:
        detail = details.get(listing["productId"])
        if not detail:
            continue
        entry = build_entry(listing, detail)
        entry["summary"] = editorial_summary(entry, entry)
        added.append(entry)
        if len(added) == needed:
            break

    if len(added) != needed:
        print(f"Only {len(added)} sourced entries were usable; {needed} are required.", file=sys.stderr)
        for name, error in failures[:20]:
            print(f"  {name}: {error}", file=sys.stderr)
        return 1

    with ThreadPoolExecutor(max_workers=args.workers) as pool:
        futures = {
            pool.submit(prepare_image, item["sourceImageUrl"], item["image"]): item
            for item in added
        }
        complete = 0
        for future in as_completed(futures):
            item = futures[future]
            try:
                future.result()
            except (urllib.error.URLError, OSError) as error:
                print(f"Image failed for {item['brand']} {item['name']}: {error}", file=sys.stderr)
                return 1
            complete += 1
            if complete % 20 == 0 or complete == len(futures):
                print(f"images {complete}/{len(futures)}", flush=True)

    catalogue = editorial + added
    for item in catalogue:
        item.pop("sourceImageUrl", None)
    PRODUCTS_PATH.write_text(
        json.dumps(catalogue, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    print(f"Wrote {len(catalogue)} perfumes to {PRODUCTS_PATH}")
    if failures:
        print(f"Skipped {len(failures)} products whose official detail data was incomplete.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
