"""Prepare responsive image sets for the 2 August 2026 features."""

from __future__ import annotations

import shutil
from pathlib import Path

from PIL import Image, ImageOps


ROOT = Path(__file__).resolve().parents[1]
GENERATED = Path(r"C:\Users\Filip\.codex\generated_images\019f7c7a-91be-7b23-a310-81bba61e867c")


def save_set(
    image: Image.Image,
    stem: Path,
    width: int,
    height: int,
    jpeg_quality: int = 84,
    webp_quality: int = 79,
) -> None:
    image = ImageOps.exif_transpose(image).convert("RGB")
    image = ImageOps.fit(image, (width, height), method=Image.Resampling.LANCZOS)
    stem.parent.mkdir(parents=True, exist_ok=True)
    image.save(stem.with_suffix(".jpg"), "JPEG", quality=jpeg_quality, optimize=True, progressive=True)
    image.save(stem.with_suffix(".webp"), "WEBP", quality=webp_quality, method=6)
    for variant in (960, 640):
        variant_height = round(height * variant / width)
        resized = image.resize((variant, variant_height), Image.Resampling.LANCZOS)
        resized.save(stem.parent / f"{stem.name}-{variant}.webp", "WEBP", quality=max(60, webp_quality - 2), method=6)


def main() -> None:
    home_root = ROOT / "assets" / "images" / "blogs" / "home" / "how-to-keep-your-space-clean"
    generated = {
        "how-to-keep-your-space-clean-hero": GENERATED / "exec-800b9697-4b0b-4516-a882-775e73789167.png",
        "clean-entry-transfer-route": GENERATED / "exec-df1bc39f-a277-46d3-a586-f81a495d1021.png",
        "oblique-light-cleaning-check": GENERATED / "exec-2acb7ec8-e754-4900-bb3b-01e6914e6b16.png",
    }
    for name, source in generated.items():
        with Image.open(source) as image:
            size = (1536, 1024) if name.endswith("hero") else (1200, 1500)
            save_set(image, home_root / name, *size)

    culture_root = ROOT / "assets" / "images" / "blogs" / "culture" / "ariana-grande-petal-streams-rankings"
    official_root = ROOT / "assets" / "images" / "blogs" / "culture" / "ariana-grande-petal-meaning"
    culture_sources = {
        "ariana-petal-streams-hero": "ariana-grande-petal-hero",
        "ariana-petal-chart-impact": "petal-video-flower",
        "ariana-petal-next-week": "petal-video-audition",
    }
    for destination_name, source_name in culture_sources.items():
        for suffix in (".jpg", ".webp", "-640.webp", "-960.webp"):
            shutil.copy2(official_root / f"{source_name}{suffix}", culture_root / f"{destination_name}{suffix}")


if __name__ == "__main__":
    main()
