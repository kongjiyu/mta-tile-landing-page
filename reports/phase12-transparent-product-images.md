# Phase 12 — Restore transparent product images

**Date:** 2026-07-14

## Problem

The redesigned site referenced the original JPG or non-transparent PNG product photos, which displayed visible white rectangles around the packaging.

## Changes

- Restored the existing transparent PNG for MTA 991.
- Restored the existing transparent PNG for MTA 993.
- Restored the existing transparent PNG for MTA ADMIX 123 20 L.
- Updated the canonical generator so hero images, product cards, navigation thumbnails, related products, metadata, and product pages stay consistent on future rebuilds.
- No CSS or layout changes were required.

## Verification

- Confirmed all three source assets are RGBA PNG files.
- Regenerated the full static site with `python3 static-redesign.py`.
- Confirmed generated HTML references only the transparent product assets.
- Browser-checked the homepage at 1440×900 and 390×844.
- Visually confirmed that the white image rectangles are gone while the intended card backgrounds remain unchanged.

## Screenshots

- Before: `phase12-transparent-products-before-desktop.png`
- After, desktop: `phase12-transparent-products-after-desktop.png`
- After, mobile: `phase12-transparent-products-after-mobile.png`
