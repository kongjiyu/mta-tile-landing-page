# Product images and lightbox verification — 2026-07-12

## Image work

- Created transparent product cutouts for MTA 991, MTA 993, and MTA ADMIX 123.
- Used the built-in image generation edit workflow to replace only the exterior white background with a chroma-key color, followed by local alpha extraction.
- Preserved packaging colors, logos, text, proportions, and white areas inside each product.
- Saved the final project assets as:
  - `static/wp-content/uploads/2025/04/MTA_packaging-991-transparent.png`
  - `static/wp-content/uploads/2025/04/MTA-Packaging-993-transparent.png`
  - `static/wp-content/uploads/2025/04/MTA_packagingAdmix123_20litres-transparent.png`

## Background assessment

The existing backgrounds remain appropriate. Warm cement neutrals give the red, blue, black, and white packaging clear contrast without making the catalogue feel glossy. The dark home hero also suits the industrial brand; the issue was image scale and positioning rather than the background color. The hero products were reduced and moved into a dedicated safe area so they no longer overlap the note or sales copy.

## UX review

- Anti-pattern verdict: pass. The result retains the industrial editorial direction and avoids generic glass, neon, or decorative card treatments.
- Cognitive load: low. Three product choices stay within the four-item working-memory guideline.
- Mobile sales flow: the fixed WhatsApp action remains thumb reachable.
- Accessibility: content images have alt text, visible keyboard focus, Enter/Space activation, a labelled close control, and Escape dismissal.

## MTA GROUT visibility

- Removed from the home product range.
- Removed from desktop navigation, mobile navigation, related products, and footers.
- Removed from `sitemap.xml`.
- Retained the source page with `noindex, nofollow` so recovery evidence is not deleted.

## Browser checks

- Desktop: 1440 × 900.
- Mobile: 390 × 844.
- Checked `/`, `/about-us/`, `/mta991/`, `/mta993/`, and `/mta_admix_123/`.
- All content images loaded successfully.
- Every content image initialized as zoomable.
- No JavaScript console errors or document-level horizontal overflow.
- No MTA GROUT link or visible text remained outside the retained source page.

## Visual artifacts

- `output/playwright/home-transparent-products.png`
- `output/playwright/admix-transparent-product.png`
- `output/playwright/photo-lightbox-desktop.png`
- `output/playwright/home-mobile-transparent-products.png`
- `output/playwright/photo-lightbox-mobile.png`
- `output/playwright/mobile-menu-three-products.png`
