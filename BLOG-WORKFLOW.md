# by.foro blog workflow

The site now uses category folders inside `blogs/`:

```text
blogs/
├── fashion/
├── home/
├── beauty/
├── culture/
└── _template/
    └── article-template.html
```

## Publish a new blog

1. Duplicate `blogs/_template/article-template.html`.
2. Put the copy inside the correct category folder.
3. Rename it with a lowercase URL slug, for example:
   `blogs/home/how-to-style-open-kitchen-shelves.html`
4. Put its images in:
   `assets/images/blogs/home/how-to-style-open-kitchen-shelves/`
5. Because an article sits two folders below the site root, use `../../` for root files. Examples:
   - `../../styles.css`
   - `../../home.html`
   - `../../assets/images/...`
6. Add the article URL to `sitemap.xml`.
7. Add a card only to the page where you want the article promoted.

## Add a card to a category page

For a Home article, open `home.html` and paste this block inside the `<section class="stories">` element:

```html
<article class="story-card">
  <a href="blogs/home/ARTICLE-SLUG.html">
    <img src="assets/images/blogs/home/ARTICLE-SLUG/card.jpg"
         alt="DESCRIPTIVE IMAGE ALT TEXT"
         width="1200" height="1500" loading="lazy" decoding="async">
    <p class="category">Home · SUBCATEGORY</p>
    <h2>ARTICLE TITLE</h2>
    <p class="story-description">ONE-SENTENCE ARTICLE DESCRIPTION.</p>
  </a>
</article>
```

Use the same pattern in:

- `fashion.html` for files in `blogs/fashion/`
- `home.html` for files in `blogs/home/`
- `beauty.html` for files in `blogs/beauty/`
- `culture.html` for files in `blogs/culture/`
- `index.html` only when you also want a story featured on the homepage

## Important limitation

This is a static GitHub Pages website. Merely placing an HTML file inside `blogs/home/` does not automatically create a card on `home.html`. You must add the card block to the listing page, or later move the site to a generator such as Eleventy, Astro or Jekyll.

## Current example

The first article is stored at:

`blogs/home/most-beautiful-kitchen-colour-combinations.html`

Its card is already added to `home.html`, and its URL is already added to `sitemap.xml`.
