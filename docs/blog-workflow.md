# by.foro article system

Every article has one canonical folder, one catalogue record and one image folder.

```text
blogs/<department>/<article-slug>/index.html
assets/images/blogs/<department>/<article-slug>/<article-slug>-hero.jpg
content/articles.json
```

Departments are `fashion`, `home`, `beauty` and `culture`. Topics are narrower,
lowercase and hyphenated, such as `personal-style`, `kitchens`, `fragrance`,
`music` and `essays`.

## Publishing a story

1. Copy `blogs/_template/article-template.html` to the canonical article folder.
2. Add the optimized JPEG source to the matching image folder.
3. Add the complete record to `content/articles.json`, including excerpt and alt text.
4. Add the story card to `journal/index.html` and the URL to `sitemap.xml` and `rss.xml`.
5. Run `python tools/optimize_images.py` to create the 640 px, 960 px and full WebP files.
6. Run `python tools/refresh_site.py` to rebuild related stories, department archives,
   structured data, word counts and responsive image markup.
7. Test search, filters, image fallback, keyboard navigation and mobile layout locally.

The catalogue is the source of truth for related stories and department archive
cards. Empty future topics should not appear in navigation until a story exists.

## Image rule

Use a photographic JPEG as the fallback source. The optimization tool creates
responsive WebP derivatives and keeps full-size WebPs below 150 KB where possible.
PNG is reserved for graphics that genuinely require lossless pixels or transparency.

Always write descriptive alt text that describes the visible scene rather than
repeating the article title. Decorative images should use an empty alt attribute.

## Content and SEO checklist

- One H1 and one canonical URL.
- A useful, specific description; do not write a search-engine summary that the
  article cannot fulfil.
- Original publication and modification dates must be visibly distinguished.
- `BlogPosting.wordCount` must match the visible article body.
- Add contextual links where another by.foro story genuinely continues the idea.
- Credit sources next to factual claims and trend reporting.
- Never create an empty crawlable topic page.

Legacy top-level `.html` redirect files remain only to preserve old inbound links.
New canonical content always uses the folder URL ending in `/`.
