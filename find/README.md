# by.foro Finder

The live perfume catalogue is stored in `products.json`. The questionnaire uses those fields directly, so new products and affiliate destinations do not require layout changes.

## Add an affiliate link

For the relevant product, paste the complete tracked destination into `affiliateUrl`:

```json
"productUrl": "https://brand.example/product",
"affiliateUrl": "https://affiliate-network.example/tracked-destination"
```

When `affiliateUrl` is empty, the button says **View official product** and opens `productUrl`. When it is filled, the button says **Shop via partner**, uses the affiliate destination, and receives `rel="sponsored nofollow noopener"` automatically.

## Product images

Every catalogue image has a `.webp` file and `.jpg` fallback in `assets/products/`. Images are official brand photography, and `sourceImageUrl` plus `imageCredit` provide the visible credit on each result card.
