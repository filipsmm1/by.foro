# by.foro static website

GitHub Pages-ready editorial website for by.foro.

## Current content state

- Fabricated/demo article pages have been removed.
- Real articles are organised under `blogs/<category>/`.
- The first Home article is published and listed on `home.html`.
- Typography has been reduced across desktop and mobile layouts.
- Image placeholders are included throughout the homepage, category pages, About page and Studio page.
- All future image files belong in `assets/images/`.
- See `IMAGE-SLOTS.md` for general page images.
- See `BLOG-WORKFLOW.md` for the article folder structure, card template and publishing steps.

## Before launch

1. Add real images to `assets/images/` and replace each placeholder with its matching `<img>` element.
2. Publish researched articles inside `blogs/<category>/`, then add their cards to the relevant category page and their URLs to `sitemap.xml`.
3. Replace `hello@byforo.com`, `studio@byforo.com`, and `corrections@byforo.com` if those inboxes do not exist.
4. Replace `https://byforo.com/` in `robots.txt` and `sitemap.xml` if the final domain differs.
5. Connect a real newsletter provider before collecting subscriptions.
6. Review legal pages for the final business entity, country, analytics, advertising, affiliate and email tools.

Open `index.html` locally or deploy the folder to GitHub Pages.
