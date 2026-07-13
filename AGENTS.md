# AGENTS.md

Static site for **mtatileadhesive.com** — a WordPress-to-static recovery and redesign project. The deliverable is a 70+ MB pure-HTML/CSS site ready to upload to Shinjiru.

## Setup

```bash
# Local preview
cd static && python3 -m http.server 8000   # http://localhost:8000

# Local WordPress (only needed if re-running the crawler)
php -S localhost:8080 -t recovered/
mariadb --socket=/tmp/mariadb.sock -uwpuser -pwppass_local_2026 mta_tile_local < recovered/wp-content/database-utf8mb4.sql
```

## Build pipeline

Run in this order, top to bottom. Each step is independent.

| Step | Script | When to run | Output |
| --- | --- | --- | --- |
| 1. Extract `.wpress` | `npx wpress-extract original/*.wpress -o extracted/ -f` | If `extracted/` is missing or stale | `extracted/` (DB + wp-content) |
| 2. Restore WordPress | (manual: copy core, set up DB, replace prefix) | If `recovered/` is missing | `recovered/` (running WP) |
| 3. Crawl to static | `python3 static-crawler.py` | After recovered WP is up at :8080 | `static/<pages>/index.html` |
| 4. Cleanup paths | `python3 static-cleanup.py` | After crawl | rewrites `localhost:8080` → relative, adds `/index.html` to internal links |
| 5. Enhance (legacy) | `python3 static-enhance.py` | Optional, pre-redesign | adds WhatsApp button, sticky header, animations, OG, JSON-LD |
| 6. **Redesign (current)** | `python3 static-redesign.py` | After cleanup, **the canonical step** | fully rebuilds `static/` from a hand-written design |
| 7. Package | `zip -r mta-tile-static.zip static/ -x "*/.DS_Store"` | After step 6 | deployable zip |

Steps 5 and 6 both produce a complete `static/`. **Step 6 supersedes step 5** — its output is what gets deployed. Step 5 is kept for reference / comparison.

## Project layout

```
original/           immutable .wpress backup (read-only evidence). DO NOT modify.
extracted/          unpacked wp-content + database.sql. Recovery input.
recovered/          runnable WordPress 6.9.1 (PHP 8.5 + MariaDB 12.3). Recovery input.
static/             deployable site. THE deliverable. Hand-built by step 6.
mta-tile-static.zip deployment package (~71 MB). Upload to Shinjiru.
.impeccable.md      design spec / context. Read this before any visual change.
static-redesign.py  canonical site generator (step 6). 451 lines, dependency-free.
static-crawler.py   crawl WordPress to raw HTML (step 3).
static-cleanup.py   rewrite paths for static hosting (step 4).
static-enhance.py   legacy enhancement (step 5, superseded).
output/             scratch — AI-generated images, Playwright runs, debug. Not shipped.
reports/            phase notes + verification screenshots. Reference only.
MAINTENANCE.md      operator guide for the deployed site.
```

## Design rules

The visual design is governed by **`.impeccable.md`**. Read it before any UI change. Key constraints:

- Light industrial catalogue aesthetic. Warm cement neutrals, charcoal ink, MTA red.
- No decorative animations, no glassmorphism, no glossy gradients, no invented claims.
- Every product journey ends in a **model-specific WhatsApp enquiry** (wa.me/60124148562?text=…).
- Mobile is a sales catalogue with thumb-reachable actions, not a shrunken desktop page.
- **Never invent** pricing, stock, MOQ, certification, dealer policy. All such data must come from the recovered backup or be flagged TODO.

## Coding style

- **Python**: PEP 8, 4-space indent, `snake_case`. `pathlib.Path` for filesystem. `static-redesign.py` is dependency-free by design.
- **HTML/CSS**: lowercase, hyphenated class names. Preserve existing page slugs (`mta_admix_123` is intentional, not a typo). Avoid editing vendored plugin/theme/core files unless recovery requires it.
- **JavaScript**: keep inline if < 2 KB; extract to a shared file only if reused across pages.
- No linters or formatters are configured. Match the surrounding code.

## Workflow conventions

- Preserve page slugs (URL paths). Renaming a slug changes the public URL.
- The active theme is **Yuga by Automattic** (free, no license). It is a Full Site Editing (FSE) block theme; do not introduce page-builder HTML.
- Static-crawler follows only `http://localhost:8080` links. Hand-edit product pages if a CTA should point to a static URL.
- WhatsApp pre-fill messages must be product-specific. Reuse `wa_url()` from `static-redesign.py`.
- All product images are in `static/wp-content/uploads/2025/04/`. AI-generated variants live in `output/imagegen/` and must be promoted into `static/wp-content/uploads/...` only after a design pass.
- PDFs: `static/wp-content/uploads/2025/06/` is the canonical location. Do not move.

## Testing

No automated test framework. Manual smoke checklist before packaging:

1. Preview every page at desktop (1440×900) and mobile (390×844): `/`, `/about-us/`, `/contact-us/`, `/mta991/`, `/mta993/`, `/mta_admix_123/`, `/mta-grout/`, `/404.html`, `/sitemap.xml`, `/robots.txt`.
2. Click every internal link — they should resolve to a real `<page>/index.html`.
3. Click every "Download PDF" link — should return `application/pdf` 200, not 404.
4. Click every WhatsApp CTA — should open `wa.me/60124148562?text=…` with product-specific text.
5. View source: confirm `<link rel="canonical">`, `og:*`, JSON-LD `<script type="application/ld+json">` are present and correct.
6. Save a screenshot per page into `reports/` for the change log.

## Commit & change log

No remote / no PR conventions. The change log lives in `reports/` — one Markdown per phase (`phase1-integrity.md` through `phase9-enhancements.md`). On any new visual or structural change, add a fresh `phaseN-*.md` and put before/after screenshots in the same folder.

Short imperative commit messages with an optional scope, e.g. `fix(contact): correct form validation`. Keep generated archives (`mta-tile-static.zip`) out of the diff — they are produced by the build, not edited.

## Security & configuration

- **Never commit** hosting credentials, database passwords, email SMTP secrets, or Formspree form IDs. The Formspree ID is injected at deploy time, not in source.
- The local WordPress DB user is `wpuser` / `wppass_local_2026` (dev only). The DB socket is `/tmp/mariadb.sock`. Production DB lives on Shinjiru, separate credentials.
- `original/*.wpress` is **read-only by convention**; `chmod 444` is set but do not rely on it. Always treat it as immutable evidence.
- Back up the current production package before replacing it on Shinjiru.
- Review `MAINTENANCE.md` before any rebuild or deploy.

## Common pitfalls

- **wpcomsh mu-plugin** (`recovered/wp-content/mu-plugins/wpcomsh*`) is WordPress.com specific and crashes the local site. Keep `wpcomsh-loader.php` renamed to `.php.disabled`. Same for the `wpcomsh/` directory.
- **Database charset**: the original dump is `latin1`. Convert to `utf8mb4` before import; 4-byte UTF-8 (e.g. emoji) must be stripped or the column errors out.
- **AI1WM placeholder**: the SQL dump uses `SERVMASK_PREFIX_` instead of `wp_`. Substitute before importing.
- **404 page**: Shinjiru's default 404 is unbranded. The static site ships its own `404.html`; ensure the deployed `.htaccess` has `ErrorDocument 404 /404.html`.
- **Hidden files**: `cPanel File Manager` hides dotfiles by default. Toggle "Show Hidden Files" before uploading so `.htaccess` actually lands.
