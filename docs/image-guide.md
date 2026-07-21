# by.foro image guide

Source photography lives in `assets/images/`; article media is grouped by department
and slug under `assets/images/blogs/`.

## Editorial direction

- Prefer natural light, believable materials and lived-in detail.
- Avoid visible faces unless a story genuinely requires a portrait and permission is clear.
- Avoid synthetic-looking skin, impossible reflections, repeated objects and illegible labels.
- Keep frames straight and let proportion create variety; do not use arbitrary crooked crops.
- Write alt text from what is actually visible.

## Output

- Keep the optimized JPEG as the universal fallback.
- Generate responsive WebP files at 640 px, 960 px and full source width with
  `python tools/optimize_images.py`.
- Aim for full WebP files below 150 KB and smaller derivatives below 100 KB.
- Use PNG only for transparency or lossless artwork, not photography.

## Primary image slots

- Homepage: `homepage-hero`, `homepage-fashion`, `homepage-home`,
  `homepage-beauty`, `homepage-culture`, `homepage-studio`.
- Departments: `<department>-hero` and `<department>-secondary`.
- Company: `studio-hero`, `studio-process`, `about-byforo`.
- Articles: `<slug>-hero` plus any named inline images in the article folder.
