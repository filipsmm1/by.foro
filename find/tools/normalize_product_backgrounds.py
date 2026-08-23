"""Place every local Finder product photograph on a clean white field.

The routine changes only edge-connected studio background pixels. It does not
redraw labels, bottles or packaging, and it keeps both WebP and JPEG outputs.
"""

from __future__ import annotations

import json
from pathlib import Path

from PIL import Image, ImageDraw, ImageOps


FIND_DIR = Path(__file__).resolve().parents[1]
PRODUCTS_PATH = FIND_DIR / "products.json"
IMAGE_DIR = FIND_DIR / "assets" / "products"
SIZE = 900
WHITE = (255, 255, 255)


def white_field(source: Image.Image) -> Image.Image:
    image = ImageOps.exif_transpose(source).convert("RGB")
    image.thumbnail((SIZE, SIZE), Image.Resampling.LANCZOS)
    canvas = Image.new("RGB", (SIZE, SIZE), WHITE)
    canvas.paste(image, ((SIZE - image.width) // 2, (SIZE - image.height) // 2))

    # Retail packshots use a connected neutral or solid studio field. Flooding
    # inward from several edge points removes that field while preserving the
    # enclosed product and its internal white or black details.
    points: list[tuple[int, int]] = []
    for offset in range(0, SIZE, 45):
        points.extend(((offset, 0), (offset, SIZE - 1), (0, offset), (SIZE - 1, offset)))
    for point in points:
        pixel = canvas.getpixel(point)
        spread = max(pixel) - min(pixel)
        brightness = sum(pixel) / 3
        if spread < 24 or brightness < 25 or brightness > 225:
            ImageDraw.floodfill(canvas, point, WHITE, thresh=42)

    # A guaranteed white outer edge prevents a coloured hairline when cards are
    # resized by the browser.
    draw = ImageDraw.Draw(canvas)
    draw.rectangle((0, 0, SIZE - 1, SIZE - 1), outline=WHITE, width=8)
    return canvas


def main() -> None:
    products = json.loads(PRODUCTS_PATH.read_text(encoding="utf-8"))
    stems = sorted({item["image"] for item in products if item.get("image")})
    for index, stem in enumerate(stems, start=1):
        jpeg = IMAGE_DIR / f"{stem}.jpg"
        webp = IMAGE_DIR / f"{stem}.webp"
        source = jpeg if jpeg.exists() else webp
        if not source.exists():
            raise FileNotFoundError(f"Missing local product image: {stem}")
        with Image.open(source) as opened:
            prepared = white_field(opened)
        prepared.save(jpeg, "JPEG", quality=84, optimize=True, progressive=True)
        prepared.save(webp, "WEBP", quality=78, method=6)
        if index % 25 == 0 or index == len(stems):
            print(f"white backgrounds {index}/{len(stems)}", flush=True)


if __name__ == "__main__":
    main()
