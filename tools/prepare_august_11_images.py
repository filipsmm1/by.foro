"""Prepare responsive image sets for the 11 August 2026 features."""

from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageOps


ROOT = Path(__file__).resolve().parents[1]
GENERATED = Path(r"C:\Users\Filip\.codex\generated_images\019f7c7a-91be-7b23-a310-81bba61e867c")

IMAGES = {
    "fashion/how-to-wear-a-scarf-belt/scarf-belt-hero": "exec-3ce3aa27-eeef-4dc6-9270-09a7899548b3.png",
    "fashion/how-to-wear-a-scarf-belt/scarf-belt-bias-fold": "exec-0fa79e53-c064-40d7-9d3d-8a15416ac2c5.png",
    "fashion/how-to-wear-a-scarf-belt/scarf-belt-tailoring": "exec-5fef8ab5-7514-4449-987f-854f1127f728.png",
    "beauty/birkin-bangs-guide/birkin-bangs-hero": "exec-e0af130c-e9a9-4209-b387-34ae7e91e22e.png",
    "beauty/birkin-bangs-guide/birkin-bangs-salon": "exec-bbcc0001-8391-4b4c-8517-6b5ea03fc202.png",
    "beauty/birkin-bangs-guide/birkin-bangs-wavy": "exec-c5671c18-1a88-43cf-af0f-74a5da610aa7.png",
    "fashion/mahjong-necklace-meaning/mahjong-necklace-hero": "exec-d53731f4-5dd7-4759-9cbe-6d7e2a8697aa.png",
    "fashion/mahjong-necklace-meaning/mahjong-necklace-layering": "exec-34c88d35-d896-418a-8feb-bbdf128e9e4d.png",
    "fashion/mahjong-necklace-meaning/mahjong-necklace-game-table": "exec-9c633793-efee-4690-9d82-696b140cf4e3.png",
}


def save_set(source: Path, stem: Path) -> None:
    with Image.open(source) as opened:
        image = ImageOps.fit(
            ImageOps.exif_transpose(opened).convert("RGB"),
            (1536, 1024),
            method=Image.Resampling.LANCZOS,
        )
    stem.parent.mkdir(parents=True, exist_ok=True)
    image.save(stem.with_suffix(".jpg"), "JPEG", quality=80, optimize=True, progressive=True)
    image.save(stem.with_suffix(".webp"), "WEBP", quality=79, method=6)
    for width in (960, 640):
        resized = image.resize((width, round(1024 * width / 1536)), Image.Resampling.LANCZOS)
        resized.save(stem.parent / f"{stem.name}-{width}.webp", "WEBP", quality=77, method=6)


def main() -> None:
    for destination, source_name in IMAGES.items():
        save_set(GENERATED / source_name, ROOT / "assets/images/blogs" / destination)
        print(f"Prepared {destination}")


if __name__ == "__main__":
    main()
