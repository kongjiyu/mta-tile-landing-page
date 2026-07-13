#!/usr/bin/env python3
"""
Playwright-based static site generator for MTA Tiles.

Crawls localhost:8080, downloads all pages and assets, rewrites paths
to relative, outputs a fully static site ready for deployment.
"""

import asyncio
import hashlib
import os
import re
import sys
from pathlib import Path
from urllib.parse import urlparse, urljoin, unquote
from playwright.async_api import async_playwright

SOURCE = "http://localhost:8080"
DEST = "/Users/kongjy/Documents/Work/mta-tile/static"
PAGES_TO_CRAWL = [
    ("/", "index.html"),
    ("/about-us/", "about-us/index.html"),
    ("/contact-us/", "contact-us/index.html"),
    ("/mta991/", "mta991/index.html"),
    ("/mta993/", "mta993/index.html"),
    ("/mta_admix_123/", "mta_admix_123/index.html"),
    ("/mta-grout/", "mta-grout/index.html"),
]

# Stats
stats = {
    "pages": 0,
    "assets_downloaded": 0,
    "assets_skipped": 0,
    "bytes_downloaded": 0,
    "errors": [],
}


def url_to_local_path(url: str) -> str:
    """Convert a URL on the source domain to a local file path.
    Preserves the URL path so that relative references work after deploy.
    """
    parsed = urlparse(url)
    path = unquote(parsed.path)
    # strip query string / fragment (already done by urlparse)
    if not path or path == "/":
        return "index.html"
    # remove leading slash
    if path.startswith("/"):
        path = path[1:]
    # If path ends with /, treat as index.html in that dir
    if path.endswith("/"):
        path = path + "index.html"
    # Don't add an extension if it already has one
    return path


async def scroll_to_load(page):
    """Scroll to bottom then top to trigger lazy-load / animations."""
    await page.evaluate("""
    async () => {
        const h = document.body.scrollHeight;
        for (let y = 0; y <= h; y += 400) {
            window.scrollTo(0, y);
            await new Promise(r => setTimeout(r, 200));
        }
        window.scrollTo(0, 0);
        await new Promise(r => setTimeout(r, 800));
    }
    """)


def normalize_for_static(html: str) -> str:
    """Final HTML cleanups for static deployment:
    - Remove WP admin / login links
    - Remove WordPress-specific meta tags
    - Remove any script tags that try to call WordPress REST API
    - Remove edit-link / preview links
    """
    # Remove edit-link (admin toolbar)
    html = re.sub(
        r'<link[^>]*rel=["\']https://api\.w\.org/["\'][^>]*>',
        '',
        html,
    )
    # Remove EditURI, WLWManifest, wp-json rels that point to localhost
    html = re.sub(r'<link[^>]*rel=["\']EditURI["\'][^>]*>', '', html)
    html = re.sub(r'<link[^>]*rel=["\']wlwmanifest["\'][^>]*>', '', html)
    html = re.sub(r'<link[^>]*type=["\']application/json\+oembed["\'][^>]*>', '', html)
    html = re.sub(r'<link[^>]*type=["\']text/xml\+oembed["\'][^>]*>', '', html)
    # Remove generator meta
    html = re.sub(r'<meta[^>]*name=["\']generator["\'][^>]*>', '', html)
    # Remove rsd_link, wlwmanifest_link options from head (already removed by link tags above)
    # Remove WordPress block library script for /wp/v2/ etc that won't work statically
    # But keep view.min.js etc that don't need backend
    # Remove <link rel='shortlink' />
    html = re.sub(r'<link[^>]*rel=["\']shortlink["\'][^>]*>', '', html)
    # Add helpful noindex for previews
    return html


def rewrite_html_for_static(html: str, current_page_url: str) -> str:
    """Rewrite asset paths from absolute http://localhost:8080/... to relative paths.

    We want the static HTML to work both:
    1. When opened directly (file:// or http://) — relative paths
    2. When deployed at the root of mtatileadhesive.com — relative paths from each page dir

    Strategy:
    - Compute the "depth" of the current page (how many /.. we need to go up)
    - Convert /wp-content/... and /wp-includes/... to {depth}/wp-content/... etc
    - Keep the URL of the page as-is for internal links (but rewrite to .html)
    """
    current_path = urlparse(current_page_url).path
    # depth = number of non-empty segments
    parts = [p for p in current_path.split("/") if p]
    depth = len(parts)
    if current_path.endswith("/") or current_path == "":
        # /about-us/ -> depth 1, ..
        if current_path == "" or current_path == "/":
            prefix = ""
        else:
            prefix = "../" * depth
    else:
        # /about-us (no trailing) - same
        prefix = "../" * depth

    def repl_absolute(match):
        url = match.group(1)
        if url.startswith("http://localhost:8080"):
            path = url[len("http://localhost:8080"):]
            if path.startswith("/"):
                return f'"{prefix[:-3] if prefix else ""}{path[1:]}"' if prefix == "" else f'"{prefix}{path[1:]}"'
        return match.group(0)

    # Simpler: just do string replacement
    html = html.replace('http://localhost:8080/', prefix if prefix else '')
    # Now if depth=0 (homepage), path is e.g. "wp-content/...". If depth=1 (about-us/), path is "../wp-content/...".
    # Need to also fix internal links that point to other pages:
    # /about-us/ -> ../about-us/index.html (so user clicking works)
    # /mta991/ -> ../mta991/index.html
    # But also rewrite the .html suffix

    return html


async def download_asset(context, url: str, dest_root: str) -> bool:
    """Download a single asset to dest_root. Returns True on success."""
    if not url.startswith("http://localhost:8080"):
        return False
    parsed = urlparse(url)
    local = url_to_local_path(url)
    local_path = os.path.join(dest_root, local)
    os.makedirs(os.path.dirname(local_path), exist_ok=True)
    if os.path.exists(local_path) and os.path.getsize(local_path) > 0:
        stats["assets_skipped"] += 1
        return True
    try:
        response = await context.request.get(url, timeout=20000)
        if response.status != 200:
            stats["errors"].append(f"HTTP {response.status} for {url}")
            return False
        data = await response.body()
        with open(local_path, "wb") as f:
            f.write(data)
        stats["assets_downloaded"] += 1
        stats["bytes_downloaded"] += len(data)
        return True
    except Exception as e:
        stats["errors"].append(f"Failed {url}: {e}")
        return False


async def crawl_and_save():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(
            viewport={"width": 1440, "height": 900},
            user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36",
        )
        # Block external (Jetpack, s.w.org, etc) to speed up
        await context.route("**/*", lambda route: (
            route.abort() if any(
                host in route.request.url for host in [
                    "s0.wordpress.com", "pixel.wp.com", "s.w.org", "i0.wp.com",
                    "wordpress.com", "jetpack.com", "googleapis.com",
                ]
            ) and "i0.wp.com" not in route.request.url  # allow if user uploaded there
            else route.continue_()
        ))

        for path, dest_rel in PAGES_TO_CRAWL:
            url = SOURCE + path
            print(f"\n=== {url} ===")
            page = await context.new_page()
            try:
                await page.goto(url, wait_until="domcontentloaded", timeout=30000)
                await scroll_to_load(page)
                # Wait for any pending network requests
                try:
                    await page.wait_for_load_state("networkidle", timeout=10000)
                except Exception:
                    pass
                # Get the HTML
                html = await page.content()
                # Extract all asset URLs from HTML before rewriting
                asset_urls = set()
                # img src / srcset
                for m in re.finditer(r'<img[^>]*src=["\']([^"\']+)["\']', html):
                    asset_urls.add(m.group(1))
                for m in re.finditer(r'srcset=["\']([^"\']+)["\']', html):
                    for part in m.group(1).split(','):
                        u = part.strip().split(' ')[0]
                        if u:
                            asset_urls.add(u)
                # link href (CSS)
                for m in re.finditer(r'<link[^>]*href=["\']([^"\']+)["\']', html):
                    asset_urls.add(m.group(1))
                # script src
                for m in re.finditer(r'<script[^>]*src=["\']([^"\']+)["\']', html):
                    asset_urls.add(m.group(1))
                # source srcset (for video/picture)
                for m in re.finditer(r'<source[^>]*srcset=["\']([^"\']+)["\']', html):
                    for part in m.group(1).split(','):
                        u = part.strip().split(' ')[0]
                        if u:
                            asset_urls.add(u)
                # Resolve relative URLs
                resolved = set()
                for u in asset_urls:
                    if u.startswith("http://localhost:8080") or u.startswith("https://localhost:8080"):
                        resolved.add(u)
                    elif u.startswith("/"):
                        resolved.add(SOURCE + u)
                    elif u.startswith("data:") or u.startswith("blob:"):
                        continue
                    # else: relative, skip
                # Filter to only download from our domain
                resolved = {u for u in resolved if u.startswith(SOURCE)}
                # Download all
                print(f"  Found {len(resolved)} assets")
                for u in resolved:
                    await download_asset(context, u, DEST)
                # Also fetch CSS and download @import / url() references
                # Find CSS file URLs
                css_urls = [u for u in resolved if u.endswith('.css') or '.css?' in u]
                for css_url in css_urls:
                    local_css = os.path.join(DEST, url_to_local_path(css_url))
                    if os.path.exists(local_css):
                        with open(local_css) as f:
                            css_text = f.read()
                        # Find url(...) references
                        for m in re.finditer(r'url\(([^)]+)\)', css_text):
                            ref = m.group(1).strip().strip('"\'')
                            if ref.startswith("data:") or ref.startswith("#"):
                                continue
                            if ref.startswith("/"):
                                ref = SOURCE + ref
                            if ref.startswith(SOURCE):
                                await download_asset(context, ref, DEST)
                # Save the HTML
                html = normalize_for_static(html)
                html = rewrite_html_for_static(html, url)
                dest_path = os.path.join(DEST, dest_rel)
                os.makedirs(os.path.dirname(dest_path), exist_ok=True)
                with open(dest_path, "w") as f:
                    f.write(html)
                stats["pages"] += 1
                print(f"  Saved: {dest_path} ({len(html)} bytes)")
            except Exception as e:
                stats["errors"].append(f"Page {url}: {e}")
                print(f"  ERROR: {e}")
            finally:
                await page.close()

        await browser.close()


async def main():
    print(f"Crawling {SOURCE} -> {DEST}")
    print(f"Pages: {len(PAGES_TO_CRAWL)}")
    print()
    await crawl_and_save()
    print()
    print("=== Stats ===")
    for k, v in stats.items():
        if k != "errors":
            print(f"  {k}: {v}")
    if stats["errors"]:
        print(f"\n  errors ({len(stats['errors'])}):")
        for e in stats["errors"][:20]:
            print(f"    - {e}")
        if len(stats["errors"]) > 20:
            print(f"    ... and {len(stats['errors']) - 20} more")


if __name__ == "__main__":
    asyncio.run(main())
