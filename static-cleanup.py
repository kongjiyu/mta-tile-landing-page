#!/usr/bin/env python3
"""
Static site post-processing for MTA Tiles.
- Rewrite internal page links to include /index.html
- Remove broken feed/comments/wp-json links
- Set canonical URL to https://mtatileadhesive.com
- Add sitemap.xml, robots.txt, 404.html
"""

import os
import re
from pathlib import Path
from datetime import datetime

STATIC = Path("/Users/kongjy/Documents/Work/mta-tile/static")
PROD_URL = "https://mtatileadhesive.com"

# All page paths
PAGES = [
    ("/", "Homepage", "2026-02-24"),
    ("/about-us/", "About Us", "2025-07-09"),
    ("/contact-us/", "Contact Us", "2025-07-09"),
    ("/mta991/", "MTA 991 - Normal Cementitious Tile Adhesive", "2025-04-01"),
    ("/mta993/", "MTA 993 - Single Component Polymer Modified Flexible Tile Adhesive", "2025-04-01"),
    ("/mta_admix_123/", "MTA ADMIX 123 - Multipurpose Latex Admixture for Mortar", "2025-04-01"),
    ("/mta-grout/", "MTA Grout (Coming Soon) - Floor & Wall Grout Joint Filler", "2025-04-01"),
]


def rewrite_html(html: str, current_page_path: str) -> str:
    """Rewrite HTML for static deployment."""
    # Compute prefix
    parts = [p for p in current_page_path.split("/") if p]
    depth = len(parts)
    if depth == 0:
        prefix = ""
    else:
        prefix = "../" * depth

    # Remove broken feed/comment/wp-json references in head
    html = re.sub(r'<link[^>]*href="[^"]*feed/?"[^>]*>', '', html)
    html = re.sub(r'<link[^>]*href="[^"]*comments/feed/?"[^>]*>', '', html)
    html = re.sub(r'<link[^>]*rel=["\']https://api\.w\.org/["\'][^>]*>', '', html)
    html = re.sub(r'<link[^>]*rel=["\']EditURI["\'][^>]*>', '', html)
    html = re.sub(r'<link[^>]*rel=["\']wlwmanifest["\'][^>]*>', '', html)
    html = re.sub(r'<link[^>]*rel=["\']shortlink["\'][^>]*>', '', html)
    html = re.sub(r'<link[^>]*type=["\']application/json\+oembed["\'][^>]*>', '', html)
    html = re.sub(r'<link[^>]*type=["\']text/xml\+oembed["\'][^>]*>', '', html)
    # Remove canonical pointing to localhost
    html = re.sub(r'<link[^>]*rel=["\']canonical["\'][^>]*>', '', html)
    # Remove WordPress REST API link
    html = re.sub(r'<link[^>]*rel=["\']alternate["\'][^>]*type=["\']application/json\+oembed["\'][^>]*>', '', html)
    # Remove generator meta
    html = re.sub(r'<meta[^>]*name=["\']generator["\'][^>]*>', '', html)
    # Remove xmlrpc
    html = re.sub(r'<link[^>]*rel=["\']pingback["\'][^>]*>', '', html)

    # Rewrite internal page links (about-us/, mta991/, etc) to include /index.html
    # But NOT external or already-relative-with-file links
    page_slugs = ["about-us", "contact-us", "mta991", "mta993", "mta_admix_123", "mta-grout"]
    for slug in page_slugs:
        # href="about-us/" or href="../about-us/" (from depth 1)
        # We want href="about-us/index.html" or href="../about-us/index.html"
        html = re.sub(
            rf'href="(/?(?:[^"/]+/)*){re.escape(slug)}/?(?:#[^"]*)?"',
            rf'href="\1{slug}/index.html"',
            html,
        )
    # Also rewrite href="/" to index.html
    html = re.sub(r'href="/(?:#[^"]*)?"', f'href="{prefix}index.html"', html)
    html = re.sub(r'href="/#', f'href="{prefix}index.html#', html)

    # Remove WordPress REST API script (it tries to fetch from /wp-json/)
    html = re.sub(
        r'<script[^>]*src=["\'][^"\']*wp-json[^"\']*["\'][^>]*></script>',
        '',
        html,
    )
    # Remove links to /wp-json/ or wp-json in href
    html = re.sub(r'<link[^>]*href="[^"]*wp-json[^"]*"[^>]*>', '', html)
    html = re.sub(r'<a[^>]*href="[^"]*wp-json[^"]*"[^>]*>.*?</a>', '', html, flags=re.DOTALL)

    # Add canonical link to production
    canonical = f'<link rel="canonical" href="{PROD_URL}{current_page_path}" />'
    html = html.replace('<head>', f'<head>\n\t{canonical}', 1)

    # Add favicon (just use a 1x1 transparent placeholder, or skip)
    # Replace <html lang="en-US"> if needed (kept as is, fine)

    # Remove href="http://localhost:8080"
    html = re.sub(r'href="http://localhost:8080[^"]*"', f'href="{PROD_URL}/"', html)
    # Remove src="http://localhost:8080..." (just in case)
    html = re.sub(r'src="http://localhost:8080[^"]*"', '', html)

    # Add noindex robots if the page is internal (homepage shouldn't be noindex)
    # but it's fine to leave them as-is since they're public pages

    return html


def process_html_files():
    """Walk all index.html files and rewrite them."""
    for page_path, page_title, _ in PAGES:
        if page_path == "/":
            html_file = STATIC / "index.html"
        else:
            slug = page_path.strip("/").rstrip("/")
            html_file = STATIC / slug / "index.html"
        if not html_file.exists():
            print(f"  MISSING: {html_file}")
            continue
        html = html_file.read_text(encoding="utf-8", errors="replace")
        new_html = rewrite_html(html, page_path)
        if new_html != html:
            html_file.write_text(new_html, encoding="utf-8")
            print(f"  Rewrote: {html_file.relative_to(STATIC)}")
        else:
            print(f"  No change: {html_file.relative_to(STATIC)}")


def write_sitemap():
    """Generate sitemap.xml."""
    content = ['<?xml version="1.0" encoding="UTF-8"?>']
    content.append('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">')
    for path, _, lastmod in PAGES:
        content.append("  <url>")
        content.append(f"    <loc>{PROD_URL}{path}</loc>")
        content.append(f"    <lastmod>{lastmod}</lastmod>")
        content.append("    <changefreq>monthly</changefreq>")
        content.append("    <priority>0.8</priority>")
        content.append("  </url>")
    content.append("</urlset>")
    (STATIC / "sitemap.xml").write_text("\n".join(content), encoding="utf-8")
    print("  Wrote: sitemap.xml")


def write_robots():
    """Generate robots.txt."""
    content = f"""User-agent: *
Allow: /

Sitemap: {PROD_URL}/sitemap.xml
"""
    (STATIC / "robots.txt").write_text(content, encoding="utf-8")
    print("  Wrote: robots.txt")


def write_404():
    """Generate a simple 404.html that matches the site style."""
    content = """<!DOCTYPE html>
<html lang="en-US">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Page Not Found | MTA Tiles Adhesive Specialist</title>
<link rel="canonical" href="https://mtatileadhesive.com/404.html" />
<style>
  body {
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
    background: #f6f4ed;
    color: #002a32;
    margin: 0;
    padding: 0;
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
  }
  .container {
    max-width: 600px;
    text-align: center;
    padding: 40px 20px;
  }
  .logo {
    width: 64px;
    height: auto;
    margin-bottom: 24px;
  }
  h1 {
    font-size: 96px;
    margin: 0 0 16px;
    color: #002a32;
    font-weight: 800;
    line-height: 1;
  }
  h2 {
    font-size: 24px;
    margin: 0 0 16px;
    color: #002a32;
    font-weight: 600;
  }
  p {
    font-size: 16px;
    color: #555;
    line-height: 1.6;
    margin: 0 0 32px;
  }
  .actions {
    display: flex;
    gap: 12px;
    justify-content: center;
    flex-wrap: wrap;
  }
  .btn {
    display: inline-block;
    padding: 12px 24px;
    background: #002a32;
    color: #f6f4ed;
    text-decoration: none;
    border-radius: 4px;
    font-weight: 500;
    transition: background 0.2s;
  }
  .btn:hover { background: #001a1f; }
  .btn-outline {
    background: transparent;
    color: #002a32;
    border: 2px solid #002a32;
  }
  .btn-outline:hover { background: #002a32; color: #f6f4ed; }
</style>
</head>
<body>
  <div class="container">
    <h1>404</h1>
    <h2>Page Not Found</h2>
    <p>The page you're looking for doesn't exist or has been moved. Let's get you back to where you need to be.</p>
    <div class="actions">
      <a href="/" class="btn">Back to Homepage</a>
      <a href="/contact-us/" class="btn btn-outline">Contact Us</a>
    </div>
  </div>
</body>
</html>
"""
    (STATIC / "404.html").write_text(content, encoding="utf-8")
    print("  Wrote: 404.html")


def write_readme():
    """Write a README for the static site."""
    content = f"""# MTA Tiles Static Site

Generated from a `.wpress` backup on 2026-07-12.

## Structure

```
static/
├── index.html              # Homepage
├── about-us/index.html
├── contact-us/index.html
├── mta991/index.html
├── mta993/index.html
├── mta_admix_123/index.html
├── mta-grout/index.html
├── 404.html                # Not found
├── sitemap.xml             # SEO
├── robots.txt              # Crawler rules
├── wp-content/             # Uploaded files, themes, plugins
└── wp-includes/            # WordPress core assets (CSS, JS, fonts)
```

## Deploy

Upload the entire `static/` directory to your web server's document root
(typically `public_html/`). All paths are relative.

## URLs

- Homepage: https://{PROD_URL}/
- About: https://{PROD_URL}/about-us/
- Contact: https://{PROD_URL}/contact-us/
- MTA 991: https://{PROD_URL}/mta991/
- MTA 993: https://{PROD_URL}/mta993/
- MTA ADMIX 123: https://{PROD_URL}/mta_admix_123/
- MTA Grout: https://{PROD_URL}/mta-grout/

## Source

Backup: `original/MTA Tiles Adhesive Export 2026-02-24.wpress` (579MB)
WordPress version: 6.9.1
Theme: Yuga (Automattic, free)
"""
    (STATIC / "README.md").write_text(content, encoding="utf-8")
    print("  Wrote: README.md")


if __name__ == "__main__":
    print("Processing HTML files...")
    process_html_files()
    print()
    print("Writing extra files...")
    write_sitemap()
    write_robots()
    write_404()
    write_readme()
    print()
    print("Done.")
