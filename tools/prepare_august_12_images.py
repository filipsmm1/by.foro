"""Prepare responsive image sets for the 12 August 2026 fashion features."""

from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageOps


ROOT = Path(__file__).resolve().parents[1]
GENERATED = Path(r"C:\Users\Filip\.codex\generated_images\019f7c7a-91be-7b23-a310-81bba61e867c")

IMAGES = {
    "fashion/jelly-kitten-heels/jelly-kitten-heels-hero": "exec-b2a2da4a-e738-453d-8ec5-3548234e0b5a.png",
    "fashion/jelly-kitten-heels/jelly-kitten-heels-construction": "exec-b78376c9-25a0-4384-92c4-a24a39d0ce74.png",
    "fashion/jelly-kitten-heels/jelly-kitten-heels-evening": "exec-2a7481bc-fefe-4c9f-ae48-5a085a9b22ad.png",
    "fashion/subtle-cat-eye-sunglasses/subtle-cat-eye-sunglasses-hero": "exec-bd24bba4-c819-4f96-be88-90b393aec0fb.png",
    "fashion/subtle-cat-eye-sunglasses/subtle-cat-eye-sunglasses-fit": "exec-292bde9c-fc05-4dbc-b53d-9977ee5680d4.png",
    "fashion/subtle-cat-eye-sunglasses/subtle-cat-eye-sunglasses-shapes": "exec-464063a6-a1c1-4650-afda-d4416739f9fb.png",
}


def save_set(source: Path, stem: Path) -> None:
    with Image.open(source) as opened:
        image = ImageOps.fit(
            ImageOps.exif_transpose(opened).convert("RGB"),
            (1536, 1024),
            method=Image.Resampling.LANCZOS,
        )
    stem.parent.mkdir(parents=True, exist_ok=True)
    image.save(stem.with_suffix(".jpg"), "JPEG", quality=79, optimize=True, progressive=True)
    image.save(stem.with_suffix(".webp"), "WEBP", quality=78, method=6)
    for width in (960, 640):
        resized = image.resize((width, round(1024 * width / 1536)), Image.Resampling.LANCZOS)
        resized.save(stem.parent / f"{stem.name}-{width}.webp", "WEBP", quality=76, method=6)


def main() -> None:
    for destination, source_name in IMAGES.items():
        save_set(GENERATED / source_name, ROOT / "assets/images/blogs" / destination)
        print(f"Prepared {destination}")


if __name__ == "__main__":
    main()
