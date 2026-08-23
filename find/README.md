# by.foro Product Finder

The live catalogue is stored in `products.json`. It contains 1,200 products across six departments: 200 each for perfume, makeup, skincare, kitchen appliances, home essentials and fashion accessories.

The interface asks four short questions about budget, product type, priorities and dealbreakers. The searchable library and recommendations read the same product fields, so catalogue updates do not require layout changes.

## Amazon shopping links

Every shopping destination in the Finder points to Amazon. Current non-perfume products use direct ASIN links. Perfumes use exact Amazon search links where a stable ASIN has not been verified.

`affiliateUrl` must stay empty until a real Amazon Associates tracking link is available. Do not invent a tracking ID. When a verified affiliate destination is added, the interface automatically uses it instead of `productUrl`.

## Product images

The original 150 perfume images have white backgrounds and are stored locally as compact `.webp` files with `.jpg` fallbacks in `assets/products/`. The 50 additional perfumes and all other departments use Amazon-hosted product images inside white, `object-fit: contain` image fields. Amazon-hosted images are not copied into the repository.

## Refresh the catalogue

- `tools/build_amazon_departments.py` maintains at least 200 Amazon-linked products in every department. Completed departments are preserved by default; pass `--refresh` for a deliberate full source refresh.
- `tools/build_perfume_catalogue.py` refreshes the 150-perfume source set, prepares white-background image files and writes Amazon shopping destinations.
- `tools/normalize_product_backgrounds.py` converts the edge-connected studio backgrounds of existing local perfume images to white without redrawing branded packaging.

Review product names, images and destinations before publishing because availability and Amazon listings can change.
