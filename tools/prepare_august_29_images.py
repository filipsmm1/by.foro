"""Prepare responsive image sets for the 29 August 2026 cluster features."""

from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageOps


ROOT = Path(__file__).resolve().parents[1]
GENERATED = Path(r"C:\Users\filip\.codex\generated_images\01a04c89-6bb5-70b1-876a-51dbf29647c7")


def save_set(source: Path, destination: Path) -> None:
    with Image.open(source) as opened:
        image = ImageOps.exif_transpose(opened).convert("RGB")
        image = ImageOps.fit(image, (1536, 1024), method=Image.Resampling.LANCZOS)
        destination.parent.mkdir(parents=True, exist_ok=True)
        image.save(
            destination.with_suffix(".jpg"),
            "JPEG",
            quality=86,
            optimize=True,
            progressive=True,
        )
        image.save(
            destination.with_suffix(".webp"),
            "WEBP",
            quality=78,
            method=6,
        )
        for width in (960, 640):
            height = round(image.height * width / image.width)
            resized = image.resize((width, height), Image.Resampling.LANCZOS)
            resized.save(
                destination.parent / f"{destination.name}-{width}.webp",
                "WEBP",
                quality=75 if width == 960 else 72,
                method=6,
            )


def main() -> None:
    jobs = {
        ROOT / "assets/images/blogs/beauty/carrot-seed-perfume-guide/carrot-seed-perfume-hero": GENERATED / "exec-e40a2264-272b-4d88-ba81-25503d02bd96.png",
        ROOT / "assets/images/blogs/beauty/carrot-seed-perfume-guide/carrot-seed-perfume-notes": GENERATED / "exec-d27eed61-3690-4e3f-98c3-76f6b5ce5acc.png",
        ROOT / "assets/images/blogs/beauty/carrot-seed-perfume-guide/carrot-seed-perfume-testing": GENERATED / "exec-4a58f1dc-d924-4d35-8996-3e0bf1effad8.png",
        ROOT / "assets/images/blogs/fashion/textured-brooch-trend/textured-brooch-hero": GENERATED / "exec-ae51f31e-3322-43bb-9aae-70b540e0a048.png",
        ROOT / "assets/images/blogs/fashion/textured-brooch-trend/textured-brooch-materials": GENERATED / "exec-21f1c334-f417-488f-a8c1-8daacf9af7c6.png",
        ROOT / "assets/images/blogs/fashion/textured-brooch-trend/textured-brooch-knit": GENERATED / "exec-0ca7a156-2f91-410a-9f19-1f0588592cd5.png",
    }
    for destination, source in jobs.items():
        if not source.exists():
            raise FileNotFoundError(source)
        save_set(source, destination)
        print("Prepared", destination.relative_to(ROOT))


if __name__ == "__main__":
    main()
