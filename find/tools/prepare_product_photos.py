"""Prepare compact, real product photographs for the by.foro Finder.

Inputs are official brand photography downloaded to a temporary folder. The
script keeps the photographed background, trims only excessive studio margins,
and exports opaque WebP/JPEG files. It never generates or redraws a product.
"""

from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np
from PIL import Image


PRODUCTS = (
    "nemat-amber",
    "glossier-you",
    "not-a-perfume",
    "burberry-goddess",
    "fleur-de-peau",
    "bal-d-afrique",
    "ellis-brooklyn-myth",
    "bois-de-balincourt",
    "i-dont-know-what",
    "dedcool-milk",
)


def edge_colour(image: Image.Image) -> tuple[int, int, int]:
    rgb = image.convert("RGB")
    width, height = rgb.size
    span = max(5, min(width, height) // 60)
    samples: list[tuple[int, int, int]] = []
    for box in (
        (0, 0, span, span),
        (width - span, 0, width, span),
        (0, height - span, span, height),
        (width - span, height - span, width, height),
    ):
        samples.extend(list(rgb.crop(box).getdata()))
    channels = np.asarray(samples, dtype=np.uint8)
    return tuple(int(value) for value in np.median(channels, axis=0))


def subject_bbox(image: Image.Image, slug: str) -> tuple[int, int, int, int]:
    width, height = image.size
    if slug == "nemat-amber":
        return (0, 0, width, height)

    if image.getchannel("A").getextrema()[0] < 255:
        bbox = image.getchannel("A").point(lambda value: 255 if value > 16 else 0).getbbox()
    else:
        rgb = np.asarray(image.convert("RGB"), dtype=np.int16)
        key = np.asarray(edge_colour(image), dtype=np.int16)
        difference = np.max(np.abs(rgb - key), axis=2)
        mask = difference > 20
        points = np.argwhere(mask)
        if not points.size:
            return (0, 0, width, height)
        y0, x0 = points.min(axis=0)
        y1, x1 = points.max(axis=0) + 1
        bbox = (int(x0), int(y0), int(x1), int(y1))

    if not bbox:
        return (0, 0, width, height)
    left, top, right, bottom = bbox
    padding = int(max(right - left, bottom - top) * 0.08)
    return (
        max(0, left - padding),
        max(0, top - padding),
        min(width, right + padding),
        min(height, bottom + padding),
    )


def prepare(source: Path, output_dir: Path, slug: str) -> None:
    original = Image.open(source).convert("RGBA")
    background = edge_colour(original)
    if original.getchannel("A").getextrema()[0] < 255:
        matte = Image.new("RGBA", original.size, (242, 237, 229, 255))
        matte.alpha_composite(original)
        original = matte

    crop = original.crop(subject_bbox(original, slug)).convert("RGB")
    crop.thumbnail((860, 860), Image.Resampling.LANCZOS)
    canvas = Image.new("RGB", (900, 900), background if slug != "dedcool-milk" else (242, 237, 229))
    canvas.paste(crop, ((900 - crop.width) // 2, (900 - crop.height) // 2))

    output_dir.mkdir(parents=True, exist_ok=True)
    canvas.save(output_dir / f"{slug}.jpg", format="JPEG", quality=88, optimize=True, progressive=True)
    canvas.save(output_dir / f"{slug}.webp", format="WEBP", quality=82, method=4)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("source_dir", type=Path)
    parser.add_argument("output_dir", type=Path)
    args = parser.parse_args()
    for slug in PRODUCTS:
        prepare(args.source_dir / f"{slug}.source", args.output_dir, slug)
        print(slug)


if __name__ == "__main__":
    main()
