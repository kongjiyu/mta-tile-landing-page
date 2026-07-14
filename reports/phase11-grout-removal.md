# Phase 11 — Remove MTA Grout from the public catalogue

**Date:** 2026-07-14

## Reason

MTA Grout is not an approved public product and must not appear in the website catalogue.

## Changes

- Removed MTA Grout from the canonical `PRODUCTS` data in `static-redesign.py`.
- Removed its homepage product card, navigation entries, footer link, related-product links, metadata, and product page.
- Updated the homepage description so the public range is described as tile adhesives and admixtures.
- Added a targeted cPanel deployment cleanup for the obsolete `/mta-grout/` directory. Other production files are not deleted.

## Verification

- Regenerated the complete static site with `python3 static-redesign.py`.
- Confirmed the homepage contains exactly three product cards.
- Confirmed no generated HTML, sitemap, or robots file contains `mta-grout` or `MTA GROUT`.
- Confirmed `/mta-grout/` returns HTTP 404 in the local preview after removal; production uses the shipped `.htaccess` to route missing paths to the branded 404 page.
- Browser-checked the homepage at 1440×900 and 390×844.
- Opened the mobile product menu and confirmed it contains only MTA 991, MTA 993, and MTA ADMIX 123.

## Screenshots

- Before: `phase11-grout-removal-before-desktop.png`
- After, desktop: `phase11-grout-removal-after-desktop.png`
- After, mobile menu: `phase11-grout-removal-after-mobile.png`
