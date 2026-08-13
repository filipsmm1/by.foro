"""Prepare responsive image sets for the 13 August 2026 features."""
from pathlib import Path
from PIL import Image, ImageOps

ROOT = Path(__file__).resolve().parents[1]
GENERATED = Path(r"C:\Users\Filip\.codex\generated_images\019f7c7a-91be-7b23-a310-81bba61e867c")
IMAGES = {
 "beauty/matcha-perfume-guide/matcha-perfume-hero":"exec-3ef388ac-7278-4652-98b3-c000daafc054.png",
 "beauty/matcha-perfume-guide/matcha-perfume-notes":"exec-1f01181a-6c86-49e4-90b9-4fcc9e6fe0df.png",
 "beauty/matcha-perfume-guide/matcha-perfume-evening":"exec-38f29449-5aa2-4655-b872-cd4d4a56b015.png",
 "fashion/how-to-wear-peplum-tops/peplum-top-hero":"exec-9f006d71-b6e4-42a3-97ef-a2a090f616e7.png",
 "fashion/how-to-wear-peplum-tops/peplum-top-construction":"exec-e9ad54dc-d14b-4558-a039-c4b83d54896f.png",
 "fashion/how-to-wear-peplum-tops/peplum-top-evening":"exec-aa0dc578-6a5b-4733-9f49-2055fa9edbd1.png",
 "beauty/ceramide-ampoule-guide/ceramide-ampoule-hero":"exec-5755783b-3321-4880-967c-2aa29424cf7e.png",
 "beauty/ceramide-ampoule-guide/ceramide-ampoule-textures":"exec-d87f70ed-1194-4b99-8f2b-2c9f54b0c60b.png",
 "beauty/ceramide-ampoule-guide/ceramide-ampoule-routine":"exec-fa185853-ba5c-41e1-9b6b-5d7bd0bb186b.png",
}
def save_set(source, stem):
    with Image.open(source) as opened:
        image=ImageOps.fit(ImageOps.exif_transpose(opened).convert("RGB"),(1536,1024),method=Image.Resampling.LANCZOS)
    stem.parent.mkdir(parents=True,exist_ok=True)
    image.save(stem.with_suffix('.jpg'),'JPEG',quality=79,optimize=True,progressive=True)
    image.save(stem.with_suffix('.webp'),'WEBP',quality=78,method=6)
    for width in (960,640):
        resized=image.resize((width,round(1024*width/1536)),Image.Resampling.LANCZOS)
        resized.save(stem.parent/f'{stem.name}-{width}.webp','WEBP',quality=76,method=6)
def main():
    for destination,source in IMAGES.items():
        save_set(GENERATED/source,ROOT/'assets/images/blogs'/destination)
        print('Prepared',destination)
if __name__=='__main__': main()
