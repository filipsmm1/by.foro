# by.foro Finder

The live 150-perfume catalogue is stored in `products.json`. The questionnaire and searchable library use those fields directly, so new products and affiliate destinations do not require layout changes.

## Add an affiliate link

For the relevant product, paste the complete tracked destination into `affiliateUrl`:

```json
"productUrl": "https://brand.example/product",
"affiliateUrl": "https://affiliate-network.example/tracked-destination"
```

When `affiliateUrl` is empty, the button says **View official product** and opens `productUrl`. When it is filled, the button says **Shop via partner**, uses the affiliate destination, and receives `rel="sponsored nofollow noopener"` automatically.

## Product images

Every catalogue image has a `.webp` file and `.jpg` fallback in `assets/products/`. Images are sourced brand or retailer product photography with the original background preserved. `sourceImageUrl`, `productUrl` and `imageCredit` record where each image and listing came from.

## Refresh the sourced catalogue

`tools/build_perfume_catalogue.py` reads three current Ulta Beauty eau de parfum listing pages, checks individual product pages for fragrance family and key notes, excludes sets and refills, then prepares compact local images. The first 10 products remain the hand-edited by.foro selection; the script fills the library to exactly 150 distinct perfumes.

Review the JSON and image diff before publishing because product names, prices and retailer availability can change.
