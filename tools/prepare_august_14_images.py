"""Prepare responsive image sets for the 14 August 2026 features."""
from pathlib import Path
from PIL import Image, ImageOps

ROOT = Path(__file__).resolve().parents[1]
GENERATED = Path(r"C:\Users\Filip\.codex\generated_images\019f7c7a-91be-7b23-a310-81bba61e867c")
IMAGES = {
    "fashion/how-to-wear-a-bib-necklace/bib-necklace-hero": "exec-38c035cd-af6e-4148-af9e-32b4cd004e15.png",
    "fashion/how-to-wear-a-bib-necklace/bib-necklace-shirt": "exec-4c0abe52-89ee-47fd-b760-2a878a248d94.png",
    "fashion/how-to-wear-a-bib-necklace/bib-necklace-evening": "exec-c9fa242a-2fe6-4adb-b031-a0a4851f00ee.png",
    "culture/pen-pal-letter-ideas-for-adults/pen-pal-letter-hero": "exec-a7c12101-f80b-49ba-9583-7c3041ce294e.png",
    "culture/pen-pal-letter-ideas-for-adults/pen-pal-letter-archive": "exec-a405465f-32e5-4398-a0ee-e3c5f80a6760.png",
    "culture/pen-pal-letter-ideas-for-adults/pen-pal-letter-inclusions": "exec-48570b62-cab5-40ff-badf-3cb9b8b738af.png",
    "home/circus-interior-design/circus-interior-hero": "exec-4c631e44-b908-4e32-aad7-e749dcd17f9a.png",
    "home/circus-interior-design/circus-interior-dining": "exec-366fa819-6ad4-487d-a9d8-a158d337c86b.png",
    "home/circus-interior-design/circus-interior-entry": "exec-6035d83e-697c-466a-b3d2-b24e4ce73f0e.png",
    "beauty/niche-perfume-collection/niche-perfume-hero": "exec-ec2e0e7a-17b4-4881-8739-c1f83cfe35e9.png",
    "beauty/niche-perfume-collection/niche-perfume-sampling": "exec-07ab7d81-2cad-4ed7-a7f6-6324a22b9e21.png",
    "beauty/niche-perfume-collection/niche-perfume-storage": "exec-a27b1e4a-559f-4e3f-87a9-b7d1507cc682.png",
    "home/red-marble-bathroom-ideas/red-marble-bathroom-hero": "exec-8a4627ac-881c-4cb1-a478-490550d52a77.png",
    "home/red-marble-bathroom-ideas/red-marble-materials": "exec-ea00fbc8-35a0-4104-9465-da5b6167549f.png",
    "home/red-marble-bathroom-ideas/red-marble-shower": "exec-0c262ecb-ebff-4448-8f72-b55992d9efb2.png",
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
    for destination, source in IMAGES.items():
        save_set(GENERATED / source, ROOT / "assets/images/blogs" / destination)
        print("Prepared", destination)

if __name__ == "__main__":
    main()
