# by.foro article system

Every article has one canonical folder, one catalogue entry and one image folder.

```text
blogs/<department>/<article-slug>/index.html
assets/images/blogs/<department>/<article-slug>/<article-slug>-hero.webp
assets/images/blogs/<department>/<article-slug>/<article-slug>-hero.jpg
content/articles.json
```

Departments are `fashion`, `home`, `beauty` and `culture`. Topics are narrower and use lowercase hyphenated names such as `personal-style`, `kitchens`, `living-rooms`, `fragrance`, `music` and `essays`.

## Image rule

Use a `<picture>` element with WebP first and an optimised JPEG fallback:

```html
<picture>
  <source type="image/webp" srcset="/assets/images/blogs/home/example/example-hero.webp">
  <img src="/assets/images/blogs/home/example/example-hero.jpg"
       alt="Specific description of the image"
       width="1536" height="1024" loading="lazy" decoding="async">
</picture>
```

JPEG is the fallback instead of PNG because photographs are dramatically smaller in JPEG and every browser that can display the site supports it. Keep hero images near 3:2, normally 1536 × 1024. Aim for WebP below 150 KB and fallback JPEG below 350 KB.

## Publish checklist

1. Copy `blogs/_template/article-template.html` into `blogs/<department>/<slug>/index.html`.
2. Put the WebP and JPEG image pair in the matching `assets/images/blogs/<department>/<slug>/` folder.
3. Add one record to `content/articles.json` with department, topic, date, URL and both image paths.
4. Add the story card to `journal/index.html` with matching `data-department`, `data-topic` and `data-search` values.
5. Add the URL to `sitemap.xml` and the item to `rss.xml`.
6. Point the relevant department’s latest-story feature at the new article when appropriate.
7. Check search, filters, image fallback and mobile layout locally before publishing.

Legacy `.html` redirect files remain beside newer article folders only to preserve old inbound links. New canonical content always lives in the folder URL ending with `/`.
