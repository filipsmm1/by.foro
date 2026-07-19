# by.foro website

Production-ready static website for GitHub Pages and the custom domain `byforo.com`.

## Publish

1. Upload every file in this folder to the root of the GitHub Pages repository.
2. Keep `CNAME` in the repository root.
3. In GitHub Pages settings, confirm the custom domain is `byforo.com` and enable HTTPS.
4. Submit `https://byforo.com/sitemap.xml` in Google Search Console.

## Forms

Contact and newsletter requests are sent through FormSubmit to `hello@byforo.com`. On the first live submission, FormSubmit sends an activation email to that address. Open it and approve the form endpoint. If the brand uses another inbox, replace `hello@byforo.com` in `contact.html`, all newsletter forms, `script.js`, and the policy pages.

## Image system

Original JPEG files are retained for social previews. Responsive WebP variants are used in-page through `<picture>` and `srcset`. Add future images to `assets/images`, export a high-quality JPEG, and create 640, 960 and 1280 pixel WebP variants.

## Publishing

Add new stories under `blogs/<department>/`, then update `journal.html`, the relevant department page, `sitemap.xml` and `rss.xml`. Every story should include a unique title, description, canonical URL, Open Graph image, publication date, BlogPosting schema, breadcrumbs, alt text and a visible update date when materially revised.

## Blog image behavior

Blog article hero and inline images are intentionally static and rectangular. Dynamic cursor zoom and sculpted crops remain on landing, category, studio and journal pages only.
