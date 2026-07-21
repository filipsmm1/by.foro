# by.foro

This build uses directory-based clean URLs that work on GitHub Pages with the `byforo.com` custom domain.

Examples:

- Homepage: `https://byforo.com/`
- Journal: `https://byforo.com/journal/`
- Fashion: `https://byforo.com/fashion/`
- Article: `https://byforo.com/blogs/home/most-beautiful-kitchen-colour-combinations/`

Each clean route contains its own `index.html`. Internal links never expose `.html` or `index.html`.
Legacy `.html` files remain only as automatic redirects, protecting old bookmarks and search-engine history.

## Deployment

Upload the complete contents of this folder to the root of the GitHub Pages repository. Do not flatten or rename the route folders. Keep `CNAME`, `assets`, `blogs`, `styles.css`, and `script.js` in place.

The site keeps optimized JPEG fallbacks and responsive WebP derivatives in
`assets/images`. Dynamic image interactions remain on the main editorial pages;
article imagery stays calm and static.

## Editorial maintenance

- Article catalogue: `content/articles.json`
- Publishing workflow: `docs/blog-workflow.md`
- Image direction: `docs/image-guide.md`
- Rebuild repeated modules: `python tools/refresh_site.py`
- Rebuild responsive images: `python tools/optimize_images.py`

Run both tools after adding an article, then test the Journal filters and the changed
pages locally before deployment.
