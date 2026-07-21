"""Create responsive WebP derivatives for by.foro photography.

Run from the repository root:
    python tools/optimize_images.py

The original JPEG remains the universal fallback. Existing source photographs are
never overwritten; the script only creates or refreshes WebP derivatives.
"""

from __future__ import annotations

from io import BytesIO
from pathlib import Path
from PIL import Image, ImageOps


ROOT = Path(__file__).resolve().parents[1]
IMAGE_ROOT = ROOT / "assets" / "images"
WIDTHS = (640, 960)


def save_webp(
    image: Image.Image,
    destination: Path,
    *,
    quality: int,
    max_bytes: int | None = None,
) -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)
    candidate = b""
    current_quality = quality
    while current_quality >= 56:
        output = BytesIO()
        image.save(output, "WEBP", quality=current_quality, method=6, optimize=True)
        candidate = output.getvalue()
        if max_bytes is None or len(candidate) <= max_bytes:
            break
        current_quality -= 2
    if destination.exists() and destination.stat().st_size <= len(candidate):
        return
    destination.write_bytes(candidate)


def optimize(source: Path) -> list[Path]:
    created: list[Path] = []
    with Image.open(source) as opened:
        image = ImageOps.exif_transpose(opened).convert("RGB")
        for width in WIDTHS:
            if image.width <= width:
                continue
            height = round(image.height * width / image.width)
            resized = image.resize((width, height), Image.Resampling.LANCZOS)
            destination = source.with_name(f"{source.stem}-{width}.webp")
            save_webp(resized, destination, quality=70 if width == 640 else 72)
            created.append(destination)

        full_destination = source.with_suffix(".webp")
        save_webp(image, full_destination, quality=68, max_bytes=150 * 1024)
        created.append(full_destination)
    return created


def main() -> None:
    sources = sorted(IMAGE_ROOT.rglob("*.jpg"))
    generated: list[Path] = []
    for source in sources:
        generated.extend(optimize(source))

    total_bytes = sum(path.stat().st_size for path in generated)
    print(
        f"Optimized {len(sources)} JPEG sources into {len(generated)} WebP files "
        f"({total_bytes / 1024 / 1024:.2f} MB)."
    )


if __name__ == "__main__":
    main()
