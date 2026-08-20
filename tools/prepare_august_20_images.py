"""Prepare responsive image sets for the 20 August 2026 features."""
from pathlib import Path

from PIL import Image, ImageOps


ROOT = Path(__file__).resolve().parents[1]
GENERATED = Path(r"C:\Users\Filip\.codex\generated_images\019f7c7a-91be-7b23-a310-81bba61e867c")

GENERATED_IMAGES = {
    "home/dorm-desk-hutch-ideas/dorm-desk-hutch-hero": "exec-8e2e4d39-9774-4931-96c7-e452f481646a.png",
    "home/dorm-desk-hutch-ideas/dorm-desk-work-zone": "exec-b0160398-c3d4-4530-96e0-f66f83d3d560.png",
    "home/dorm-desk-hutch-ideas/dorm-desk-lighting": "exec-d222f26e-1d55-4f8d-b228-7f41b5041790.png",
    "beauty/dragonfly-nails/dragonfly-nails-hero": "exec-ae2101ca-f198-40ad-a128-cbfb6cdec080.png",
    "beauty/dragonfly-nails/dragonfly-nails-minimal": "exec-7130300a-bc57-4dc5-b6cf-a37d6b4cf5b0.png",
    "beauty/dragonfly-nails/dragonfly-nails-iridescent": "exec-f71c60aa-afd1-4593-b8ee-c204036f87df.png",
    "fashion/khaki-coded-style/khaki-coded-hero": "exec-ffe32cc9-ccac-43fa-8cdb-5264bb7bbaa6.png",
    "fashion/khaki-coded-style/khaki-coded-palette": "exec-7477eca5-b855-4fd2-9309-53d5d699b65a.png",
    "fashion/khaki-coded-style/khaki-coded-tailoring": "exec-f974dad7-0856-4a40-a3b2-2886aaeb5a57.png",
    "fashion/bug-jewellery-trend/bug-jewellery-hero": "exec-dacdb08e-1856-4fd6-8217-045dbb397dcc.png",
    "fashion/bug-jewellery-trend/bug-jewellery-motifs": "exec-45644fb5-fbe8-4366-978f-49038db7e2df.png",
    "fashion/bug-jewellery-trend/bug-jewellery-styling": "exec-9e60b84e-eeb7-49bb-a9b0-efd377c18413.png",
}


def flatten(opened: Image.Image) -> Image.Image:
    image = ImageOps.exif_transpose(opened)
    if image.mode in {"RGBA", "LA"} or "transparency" in image.info:
        rgba = image.convert("RGBA")
        backdrop = Image.new("RGBA", rgba.size, (226, 214, 196, 255))
        backdrop.alpha_composite(rgba)
        return backdrop.convert("RGB")
    return image.convert("RGB")


def save_set(opened: Image.Image, stem: Path) -> None:
    image = ImageOps.fit(flatten(opened), (1536, 1024), Image.Resampling.LANCZOS)
    stem.parent.mkdir(parents=True, exist_ok=True)
    image.save(stem.with_suffix(".jpg"), "JPEG", quality=79, optimize=True, progressive=True)
    image.save(stem.with_suffix(".webp"), "WEBP", quality=78, method=6)
    for width in (960, 640):
        resized = image.resize((width, round(1024 * width / 1536)), Image.Resampling.LANCZOS)
        resized.save(stem.parent / f"{stem.name}-{width}.webp", "WEBP", quality=76, method=6)


def main() -> None:
    for destination, source in GENERATED_IMAGES.items():
        with Image.open(GENERATED / source) as opened:
            save_set(opened, ROOT / "assets/images/blogs" / destination)
        print("Prepared original", destination)


if __name__ == "__main__":
    main()
