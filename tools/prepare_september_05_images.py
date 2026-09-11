"""Prepare responsive image sets for the 5 September 2026 cluster features."""

from __future__ import annotations

from io import BytesIO
from pathlib import Path

from PIL import Image, ImageOps


ROOT = Path(__file__).resolve().parents[1]
GENERATED = Path(r"C:\Users\filip\.codex\generated_images\01a04c89-6bb5-70b1-876a-51dbf29647c7")


def save_webp(image: Image.Image, destination: Path, quality: int, max_bytes: int | None = None) -> None:
    candidate = b""
    while quality >= 54:
        output = BytesIO()
        image.save(output, "WEBP", quality=quality, method=6)
        candidate = output.getvalue()
        if max_bytes is None or len(candidate) <= max_bytes:
            break
        quality -= 2
    destination.write_bytes(candidate)


def save_set(source: Path, destination: Path) -> None:
    with Image.open(source) as opened:
        image = ImageOps.exif_transpose(opened).convert("RGB")
        image = ImageOps.fit(image, (1536, 1024), method=Image.Resampling.LANCZOS)
        destination.parent.mkdir(parents=True, exist_ok=True)
        image.save(destination.with_suffix(".jpg"), "JPEG", quality=86, optimize=True, progressive=True)
        save_webp(image, destination.with_suffix(".webp"), quality=76, max_bytes=150 * 1024)
        for width in (960, 640):
            height = round(image.height * width / image.width)
            resized = image.resize((width, height), Image.Resampling.LANCZOS)
            save_webp(
                resized,
                destination.parent / f"{destination.name}-{width}.webp",
                quality=75 if width == 960 else 72,
            )


def main() -> None:
    jobs = {
        ROOT / "assets/images/blogs/fashion/kitchen-sink-necklace/kitchen-sink-necklace-hero": GENERATED / "exec-855dfae9-8997-49a8-9a98-a7ae558576d3.png",
        ROOT / "assets/images/blogs/fashion/kitchen-sink-necklace/kitchen-sink-necklace-charms": GENERATED / "exec-f9c1e933-8ffe-41d3-886c-875a1126fafb.png",
        ROOT / "assets/images/blogs/fashion/kitchen-sink-necklace/kitchen-sink-necklace-outfit": GENERATED / "exec-71055008-6caa-478f-9357-650d6106e5aa.png",
        ROOT / "assets/images/blogs/home/greek-chic-interiors/greek-chic-interiors-hero": GENERATED / "exec-ba885f58-872d-470d-ab53-a8d3ab816779.png",
        ROOT / "assets/images/blogs/home/greek-chic-interiors/greek-chic-materials": GENERATED / "exec-604cff49-8537-43d1-b926-bca1b5fc90cd.png",
        ROOT / "assets/images/blogs/home/greek-chic-interiors/greek-chic-entryway": GENERATED / "exec-930d4634-9d7f-427e-a01a-69d9e724c351.png",
        ROOT / "assets/images/blogs/beauty/rice-perfume-guide/rice-perfume-hero": GENERATED / "exec-7d67c215-5956-41ed-880c-324eb58f2945.png",
        ROOT / "assets/images/blogs/beauty/rice-perfume-guide/rice-perfume-notes": GENERATED / "exec-7e0794b9-98ce-49ad-8002-c4f104be94bb.png",
        ROOT / "assets/images/blogs/beauty/rice-perfume-guide/rice-perfume-testing": GENERATED / "exec-233b3768-3d93-49d4-af67-b6d6e4b4ebd9.png",
    }
    for destination, source in jobs.items():
        if not source.exists():
            raise FileNotFoundError(source)
        save_set(source, destination)
        print("Prepared", destination.relative_to(ROOT))


if __name__ == "__main__":
    main()
