"""Prepare responsive image sets for the 16 August 2026 features."""
from io import BytesIO
from pathlib import Path
from urllib.request import Request, urlopen

from PIL import Image, ImageOps

ROOT = Path(__file__).resolve().parents[1]
GENERATED = Path(r"C:\Users\Filip\.codex\generated_images\019f7c7a-91be-7b23-a310-81bba61e867c")

GENERATED_IMAGES = {
    "home/elegant-summerween-decor/summerween-hero": "exec-7dbd185e-4cf3-4be9-9fc1-58b3e4ab33d2.png",
    "home/elegant-summerween-decor/summerween-table": "exec-44626b14-519f-4418-94d0-a3d958692bcc.png",
    "home/elegant-summerween-decor/summerween-film-night": "exec-f1fffe80-3ed9-41e2-b695-ec484cc650e8.png",
    "culture/how-to-serve-chilled-red-wine/chilled-red-hero": "exec-cd6f408e-eda7-4f35-919b-1959088bb739.png",
    "culture/how-to-serve-chilled-red-wine/chilled-red-temperature": "exec-5b4e4845-1746-47c7-8e7d-ad8839244e4e.png",
    "culture/how-to-serve-chilled-red-wine/chilled-red-dinner": "exec-301eed2e-2e3a-46bd-860f-2acf91eb51c5.png",
}

OFFICIAL_IMAGES = {
    "culture/the-last-house-ending-explained/last-house-hero": "https://dnm.nflximg.net/api/v6/2DuQlx0fM4wd1nzqm5BFBi6ILa8/AAAAQW-n0QodhaoucdY327Lh2H9dYo6AR2kKe-MBgpuiOEUcYZ9450yJ37Xp7uiG2dQWAhb7Z68p4IN4DBqeliCutAxn4CmILoXZNt1HI3u9-ch8g8Y95lSR7_yI842CGbmUIajp4HouKA_DKUQ-_ihVVzXZ.jpg?r=5c3",
    "culture/the-last-house-ending-explained/last-house-ann": "https://dnm.nflximg.net/api/v6/2DuQlx0fM4wd1nzqm5BFBi6ILa8/AAAAQbOuxQkvfEO-hUTcFPk6TN6lE6RJUARJC-rkeMBq1ArlLXH9_jQsdBbThkxq-_ZhjkQypGXlxc5dPCEnJs8iZg-DwMSY0JJJA58q88Ur6F_ky-MQO8wtVNSPECcW8LP6P-vmKHJ1Y0OuGVCJds8iDqi1.jpg?r=a81",
    "culture/the-last-house-ending-explained/last-house-garden": "https://dnm.nflximg.net/api/v6/2DuQlx0fM4wd1nzqm5BFBi6ILa8/AAAAQV2n39Nfl42W8JMXQLI-tMTiNNBcaQZvXA4f8MNF1F0NqZefJ1j0JZf6vGFoslg-aPkDtOJ5dpzvr0itdFo-tq-TfLgaE8kY4t2X7nXtHvYxwR7MKY1Dk802pPrZoZQuxXHDbO64fynKzEKMsdiE01Hj.jpg?r=5a4",
    "culture/sam-smith-hazel-eyes-meaning/hazel-eyes-hero": "https://i.ytimg.com/vi/K0G7jODNtEo/maxresdefault.jpg",
    "culture/sam-smith-hazel-eyes-meaning/hazel-eyes-album-art": "https://store.samsmithworld.com/cdn/shop/files/Sam_Smith_CD_9b5e5104-104a-4fd5-bfa5-e5c1ab46ecc0.png?v=1782216307&width=1500",
    "culture/sam-smith-hazel-eyes-meaning/hazel-eyes-to-be-free": "https://www.samsmithworld.com/wp-content/uploads/sites/11248/2025/07/sam-smith-to-be-free-compressed.jpg",
    "fashion/jennifer-lopez-green-versace-dress/jlo-green-dress-hero": "https://storage.googleapis.com/gweb-uniblog-publish-prod/images/VERSACE_W_SS_20_4K00055733_1.width-2200.format-webp.webp",
    "fashion/jennifer-lopez-green-versace-dress/jlo-green-dress-search-wall": "https://storage.googleapis.com/gweb-uniblog-publish-prod/images/jlo--dv-2.width-2000.format-webp.webp",
    "fashion/jennifer-lopez-green-versace-dress/jlo-green-dress-cast": "https://i.ytimg.com/vi_webp/FhrV7KSgIH4/maxresdefault.webp",
}


def fetch(url: str) -> Image.Image:
    request = Request(url, headers={"User-Agent": "Mozilla/5.0 by.foro editorial image preparation"})
    with urlopen(request, timeout=45) as response:
        return Image.open(BytesIO(response.read()))


def flatten(opened: Image.Image) -> Image.Image:
    image = ImageOps.exif_transpose(opened)
    if image.mode in {"RGBA", "LA"} or "transparency" in image.info:
        rgba = image.convert("RGBA")
        backdrop = Image.new("RGBA", rgba.size, (226, 214, 196, 255))
        backdrop.alpha_composite(rgba)
        return backdrop.convert("RGB")
    return image.convert("RGB")


def save_set(opened: Image.Image, stem: Path, centering=(0.5, 0.5)) -> None:
    image = ImageOps.fit(flatten(opened), (1536, 1024), Image.Resampling.LANCZOS, centering=centering)
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
    for destination, url in OFFICIAL_IMAGES.items():
        opened = fetch(url)
        centering = (0.5, 0.28) if destination.endswith("jlo-green-dress-hero") else (0.5, 0.5)
        save_set(opened, ROOT / "assets/images/blogs" / destination, centering=centering)
        print("Prepared credited", destination)


if __name__ == "__main__":
    main()
