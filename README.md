# MTA Tiles Static Site

Static site for [mtatileadhesive.com](https://mtatileadhesive.com) — a WordPress-to-static recovery and redesign project.

The deliverable is a 70+ MB pure-HTML/CSS site (no PHP, no database) deployed to Shinjiru shared hosting.

## Live site

- Production: <https://mtatileadhesive.com>
- Local preview: `cd static && python3 -m http.server 8000` → <http://localhost:8000>

## Deployment

Every push to `main` that touches `static/**` or `static-redesign.py` triggers a CI/CD pipeline that:

1. Runs `python3 static-redesign.py` to regenerate `static/` from the source-of-truth data
2. Sanity-checks the output
3. Uploads `static/` to Shinjiru via FTP

To deploy manually: **Actions** tab → **Deploy to Shinjiru via FTP** → **Run workflow**.

### Required secrets (set in repo Settings → Secrets → Actions)

| Name | Value |
|---|---|
| `FTP_SERVER` | Shinjiru FTP host (usually `mtatileadhesive.com`) |
| `FTP_USERNAME` | cPanel / FTP username (usually `mtatilea`) |
| `FTP_PASSWORD` | cPanel / FTP password |

## Local development

```bash
# Regenerate static site from source
python3 static-redesign.py

# Preview locally
cd static && python3 -m http.server 8000
# Open http://localhost:8000
```

## Project layout

```
static/                  # Deployable site (what gets uploaded to Shinjiru)
├── index.html           # Homepage
├── about-us/index.html
├── contact-us/index.html
├── mta991/index.html    # Product pages
├── mta993/index.html
├── mta_admix_123/index.html
├── mta-grout/index.html
├── 404.html
├── sitemap.xml
├── robots.txt
├── favicon.ico
├── apple-touch-icon.png
├── mta-site.css
├── mta-site.js
└── wp-content/, wp-includes/   # Images, fonts, legacy WP assets

static-redesign.py       # Source-of-truth site generator
static-crawler.py        # WordPress → raw HTML (recovery only)
static-cleanup.py        # Path rewriter (recovery only)
static-enhance.py        # Legacy enhancement (superseded)

.github/workflows/deploy.yml   # This CI/CD pipeline
.gitignore                       # Excludes backup artifacts, generated files
AGENTS.md                        # Full project documentation for AI agents
.impeccable.md                   # Design spec
MAINTENANCE.md                   # Operator guide for the deployed site
```

## What is NOT in this repo

These are gitignored because they are large, sensitive, or build artifacts:

- `original/` — the original `.wpress` backup (579 MB, immutable evidence)
- `extracted/` — unpacked backup contents (546 MB)
- `recovered/` — full WordPress recovery copy (684 MB, has local DB credentials)
- `working/` — intermediate scratch
- `output/` — AI-generated images, Playwright runs (scratch)
- `mta-tile-static.zip` — generated deployment package (built by GitHub Actions or locally)

To restore from backup artifacts, see `AGENTS.md` § "Build pipeline".

## Manual deployment fallback

If CI/CD is down and you need to deploy right now:

```bash
# From this repo
python3 static-redesign.py
zip -r mta-tile-static.zip static/ -x "*/.DS_Store"
# Upload mta-tile-static.zip to Shinjiru cPanel File Manager
# Extract to public_html/ (overwrite)
```

## SEO

- `sitemap.xml` is hand-written and committed
- `robots.txt` allows all + references sitemap
- All pages have `meta description`, canonical URL, Open Graph, Twitter Card, JSON-LD
- See `AGENTS.md` § "SEO" for the full checklist before requesting Google indexing

## Maintenance

For day-to-day operations (updating copy, replacing images, adding pages), see `MAINTENANCE.md`.
