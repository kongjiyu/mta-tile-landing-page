#!/usr/bin/env python3
"""Build the redesigned, deployment-ready MTA static website.

This is deliberately dependency-free so the post-crawl enhancement step remains
repeatable on any machine with Python 3.
"""

from __future__ import annotations

import html
import json
from pathlib import Path
from urllib.parse import quote


ROOT = Path(__file__).resolve().parent
STATIC = ROOT / "static"
BASE_URL = "https://mtatileadhesive.com"
PHONE = "60124148562"
EMAIL = "mtaspecialist99@gmail.com"
ADDRESS = "No. 27, Jalan Sungai Merbau 32/98, Kemuning Greenville, 40460 Shah Alam, Selangor Darul Ehsan"
LOGO = "wp-content/uploads/2025/03/Screenshot_2024-11-22_093257-removebg-preview.png"


PRODUCTS = {
    "mta991": {
        "code": "MTA 991",
        "type": "Normal Cementitious Tile Adhesive",
        "short": "C1 cementitious adhesive for general wall and floor tiling.",
        "description": "MTA 991 complies with the C1 classification requirements in accordance with EN 12004 standards.",
        "image": "wp-content/uploads/2025/04/MTA_packaging-991-transparent.png",
        "package": "25 kg / bag",
        "class": "C1",
        "use": "Interior + exterior",
        "pdf": "wp-content/uploads/2025/06/MTA-991_Catalogue.pdf",
        "features": [
            "Suitable for installing ceramic wall and floor tiles and natural stone material which are not sensitive to discoloration or translucence.",
            "For conventional cement-based substrate, concrete render, brickwork, and cementitious screeds provided they are sufficiently dry and cured.",
            "Use on walls and floors in both interior and exterior applications.",
            "Where extra strength is required for dense tiles such as vitrified porcelain with water absorption ≤ 0.5%, marble, or granite, mix with MTA Admix 123.",
        ],
        "limitations": [
            "Do not use on wood.",
            "Do not use on metal, PVC, rubber, or linoleum surfaces.",
            "Do not use on surfaces subject to strong movement.",
        ],
        "technical_intro": "In compliance with EN 12004 under laboratory conditions.",
        "technical": [
            ("Appearance", "White / grey powder"),
            ("Specific gravity", "1.5 ± 0.1 kg / litre"),
            ("Pot life at 25°C", "1–2 hours"),
            ("Open time at 25°C", "Approx. 20 minutes"),
            ("Trafficable", "After 24 hours"),
            ("Tensile adhesion strength, 28 days", "≥ 0.5 N / mm²"),
            ("Tensile adhesion after water immersion", "≥ 0.5 N / mm²"),
            ("Tensile adhesion after heat ageing", "≥ 0.5 N / mm²"),
            ("Open time", "≥ 0.5 N / mm²"),
        ],
        "coverage": [
            ("3 × 3 mm notched trowel", "2.0–3.0 kg/m²"),
            ("6 × 3 mm notched trowel", "5.0–5.5 kg/m²"),
            ("12 × 12 mm notched trowel", "10.0–11.0 kg/m²"),
        ],
    },
    "mta993": {
        "code": "MTA 993",
        "type": "Polymer Modified Flexible Tile Adhesive",
        "short": "C2TE flexible adhesive for demanding tile installations.",
        "description": "MTA 993 complies with the C2TE classification requirements in accordance with EN 12004 standards.",
        "image": "wp-content/uploads/2025/04/MTA-Packaging-993-transparent.png",
        "package": "25 kg / bag",
        "class": "C2TE",
        "use": "Interior + exterior",
        "pdf": "wp-content/uploads/2025/06/MTA-993_Catalogue.pdf",
        "features": [
            "Suitable for ceramic wall and floor tiles, homogeneous vitrified tiles, porcelain, monocottura, and natural stone not sensitive to discolouration or translucence.",
            "Tiles do not need to be soaked before installation.",
            "For conventional cement-based substrate, concrete render, brickwork, cured cementitious screeds, and lightweight concrete blocks primed with MTA Bonding Agent.",
            "Use on walls and floors in both interior and exterior applications.",
        ],
        "limitations": [
            "Do not use on metal, PVC, rubber, or linoleum surfaces.",
            "Do not use where subject to extreme flexing or vibration, including wood and fibre-cement.",
        ],
        "technical_intro": "In compliance with EN 12004 under laboratory conditions.",
        "technical": [
            ("Appearance", "Grey powder"),
            ("Specific gravity", "1.5 ± 0.1 kg / litre"),
            ("Pot life at 25°C", "1–2 hours"),
            ("Open time at 25°C", "Approx. 30 minutes"),
            ("Trafficable", "After 24 hours"),
            ("Tensile adhesion strength, 28 days", "≥ 1.0 N / mm²"),
            ("Tensile adhesion after water immersion", "≥ 1.0 N / mm²"),
            ("Tensile adhesion after heat ageing", "≥ 1.0 N / mm²"),
            ("Open time", "≥ 0.5 N / mm²"),
            ("Slip resistance", "< 0.5 mm"),
        ],
        "coverage": [
            ("3 × 3 mm notched trowel", "2.0–3.0 kg/m²"),
            ("6 × 3 mm notched trowel", "5.0–5.5 kg/m²"),
            ("12 × 12 mm notched trowel", "10.0–11.0 kg/m²"),
        ],
    },
    "mta_admix_123": {
        "code": "MTA ADMIX 123",
        "type": "Multipurpose Latex Admixture for Mortar",
        "short": "Latex admixture for stronger, more flexible cement mixes.",
        "description": "A multipurpose latex admixture designed to improve the adhesion strength of cement mixes, enhance flexibility, and reduce efflorescence.",
        "image": "wp-content/uploads/2025/04/MTA_packagingAdmix123_20litres-transparent.png",
        "package": "4 L + 20 L pails",
        "class": "Admixture",
        "use": "Wet + dry areas",
        "pdf": "wp-content/uploads/2025/06/MTA-Admix-123_Catalogue.pdf",
        "features": [
            "Admixture for tile adhesive: use with the MTA range of cement-based tile adhesive for ceramic tiles, marble, granite, and other installations on walls or floors, in dry or wet, internal or external areas including swimming pools.",
            "Admixture for tile grout: use with the MTA range of coloured grout for filling joints.",
            "Admixture for cement-sand mortar: add to cement and mortar for screed or render, improved adhesion, or a slurry bond coat.",
        ],
        "limitations": ["Do not use MTA Admix 123 as a primer; always add cement and sand."],
        "technical_intro": "All stated data is based on laboratory tests. Actual measured data may vary due to circumstances beyond our control.",
        "technical": [
            ("Appearance", "Milky white liquid"),
            ("Specific gravity", "1.01 ± 0.1 kg / litre"),
            ("Application temperature", "5°C to 40°C"),
            ("pH", "1 ± 9"),
        ],
        "coverage": [],
    },
}


def rel(prefix: str, path: str) -> str:
    return f"{prefix}{path}"


def wa_url(message: str) -> str:
    return f"https://wa.me/{PHONE}?text={quote(message)}"


ICON_PATHS = {
    "arrow-down": '<path d="M12 5v14"/><path d="m19 12-7 7-7-7"/>',
    "arrow-right": '<path d="M5 12h14"/><path d="m12 5 7 7-7 7"/>',
    "arrow-up-right": '<path d="M7 17 17 7"/><path d="M7 7h10v10"/>',
    "close": '<path d="M18 6 6 18"/><path d="m6 6 12 12"/>',
    "menu": '<path d="M4 6h16"/><path d="M4 12h16"/><path d="M4 18h16"/>',
}


def icon(name: str, extra_class: str = "") -> str:
    """Return a dependency-free Lucide-style interface icon."""
    classes = f"icon {extra_class}".strip()
    return (
        f'<svg class="{classes}" aria-hidden="true" focusable="false" '
        'viewBox="0 0 24 24" fill="none" stroke="currentColor" '
        'stroke-width="2" stroke-linecap="round" stroke-linejoin="round">'
        f'{ICON_PATHS[name]}</svg>'
    )


def header(prefix: str) -> str:
    product_links = "".join(
        f'''<a href="{rel(prefix, slug + '/index.html')}">
          <img src="{rel(prefix, product['image'])}" alt="" width="64" height="64">
          <span><strong>{html.escape(product['code'])}</strong><small>{html.escape(product['type'])}</small></span>
        </a>'''
        for slug, product in PRODUCTS.items()
    )
    mobile_products = "".join(
        f'<a href="{rel(prefix, slug + "/index.html")}">{html.escape(product["code"])} {icon("arrow-right")}</a>'
        for slug, product in PRODUCTS.items()
    )
    return f'''<a class="skip-link" href="#main">Skip to content</a>
<header class="site-header">
  <div class="wrap header-inner">
    <a class="brand" href="{rel(prefix, 'index.html')}" aria-label="MTA Tiles Adhesive Specialist home">
      <img src="{rel(prefix, LOGO)}" alt="MTA" width="120" height="78">
      <span>MTA Tiles Adhesive Specialist</span>
    </a>
    <nav class="desktop-nav" aria-label="Main navigation">
      <details class="nav-products">
        <summary>Products</summary>
        <div class="nav-panel">{product_links}</div>
      </details>
      <a href="{rel(prefix, 'about-us/index.html')}">About</a>
      <a href="{rel(prefix, 'contact-us/index.html')}">Contact</a>
    </nav>
    <a class="button button-red header-cta" href="{wa_url('Hello MTA, I would like to enquire about your products for wholesale or distribution.')}" target="_blank" rel="noopener">WhatsApp enquiry {icon('arrow-up-right', 'arrow')}</a>
    <button class="menu-toggle" type="button" aria-expanded="false" aria-controls="mobile-navigation" aria-label="Open menu">{icon('menu', 'menu-icon menu-icon-open')}{icon('close', 'menu-icon menu-icon-close')}</button>
  </div>
  <nav class="mobile-nav" id="mobile-navigation" aria-label="Mobile navigation">
    <span class="mobile-label">Products</span>
    {mobile_products}
    <span class="mobile-label">Company</span>
    <a href="{rel(prefix, 'about-us/index.html')}">About MTA {icon('arrow-right')}</a>
    <a href="{rel(prefix, 'contact-us/index.html')}">Contact {icon('arrow-right')}</a>
  </nav>
</header>'''


def footer(prefix: str) -> str:
    return f'''<footer class="site-footer">
  <div class="wrap">
    <div class="footer-grid">
      <div class="footer-brand">
        <a class="brand" href="{rel(prefix, 'index.html')}"><img src="{rel(prefix, LOGO)}" alt="MTA" width="120" height="78"><span>MTA Tiles Adhesive Specialist</span></a>
        <p>Reliable tile adhesive systems and construction materials for real-world applications across Malaysia.</p>
      </div>
      <div class="footer-col"><h3>Products</h3>
        <a href="{rel(prefix, 'mta991/index.html')}">MTA 991</a><a href="{rel(prefix, 'mta993/index.html')}">MTA 993</a><a href="{rel(prefix, 'mta_admix_123/index.html')}">MTA Admix 123</a>
      </div>
      <div class="footer-col"><h3>Contact</h3>
        <a href="tel:+60124148562">+60 12-414 8562</a><a href="mailto:{EMAIL}">{EMAIL}</a><a href="{rel(prefix, 'contact-us/index.html')}">Shah Alam, Selangor</a>
      </div>
    </div>
    <div class="footer-bottom"><span>© 2026 MTA Tile Adhesive Specialist Sdn Bhd</span><span>Monday–Friday · 9:00am–6:00pm</span></div>
  </div>
</footer>'''


def mobile_wa(message: str) -> str:
    return f'<a class="mobile-wa" href="{wa_url(message)}" target="_blank" rel="noopener">WhatsApp enquiry {icon("arrow-up-right", "arrow")}</a>'


def seo_head(*, prefix: str, title: str, description: str, path: str, image: str, schema_type: str = "WebPage", product: dict | None = None) -> str:
    canonical = f"{BASE_URL}{path}"
    image_url = f"{BASE_URL}/{image}"
    if product:
        schema = {
            "@context": "https://schema.org",
            "@type": "Product",
            "name": product["code"],
            "description": product["description"],
            "image": image_url,
            "brand": {"@type": "Brand", "name": "MTA"},
            "manufacturer": {"@type": "Organization", "name": "MTA Tile Adhesive Specialist Sdn Bhd"},
        }
    else:
        schema = {
            "@context": "https://schema.org",
            "@type": schema_type,
            "name": title,
            "description": description,
            "url": canonical,
        }
        if schema_type == "LocalBusiness":
            schema.update({"telephone": "+60124148562", "email": EMAIL, "address": {"@type": "PostalAddress", "streetAddress": "No. 27, Jalan Sungai Merbau 32/98, Kemuning Greenville", "addressLocality": "Shah Alam", "addressRegion": "Selangor", "postalCode": "40460", "addressCountry": "MY"}})
    return f'''<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(title)}</title>
<meta name="description" content="{html.escape(description, quote=True)}">
<link rel="canonical" href="{canonical}">
<meta property="og:type" content="{'product' if product else 'website'}">
<meta property="og:title" content="{html.escape(title, quote=True)}">
<meta property="og:description" content="{html.escape(description, quote=True)}">
<meta property="og:url" content="{canonical}">
<meta property="og:image" content="{image_url}">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="/favicon.ico" sizes="32x32">
<link rel="icon" href="{rel(prefix, 'wp-content/uploads/2025/05/cropped-SCR-2025-05-19-150x150.png')}" sizes="150x150" type="image/png">
<link rel="apple-touch-icon" href="/apple-touch-icon.png" sizes="180x180">
<link rel="stylesheet" href="{rel(prefix, 'mta-site.css')}">
<script type="application/ld+json">{json.dumps(schema, ensure_ascii=False)}</script>'''


def page(*, title: str, description: str, path: str, prefix: str, image: str, main: str, wa_message: str, schema_type: str = "WebPage", product: dict | None = None) -> str:
    return f'''<!doctype html>
<html lang="en">
<head>
{seo_head(prefix=prefix, title=title, description=description, path=path, image=image, schema_type=schema_type, product=product)}
</head>
<body>
{header(prefix)}
<main id="main">{main}</main>
{footer(prefix)}
{mobile_wa(wa_message)}
<script src="{rel(prefix, 'mta-site.js')}" defer></script>
</body>
</html>
'''


def product_card(prefix: str, slug: str, index: str) -> str:
    product = PRODUCTS[slug]
    badge = '<span class="coming-badge">Coming soon</span>' if product.get("coming") else ""
    return f'''<a class="product-card reveal" href="{rel(prefix, slug + '/index.html')}">
      <span class="index">{index}</span>
      <img src="{rel(prefix, product['image'])}" alt="{html.escape(product['code'])} product packaging" loading="lazy">
      <div class="product-meta"><div>{badge}<h3>{html.escape(product['code'])}</h3><p>{html.escape(product['type'])}</p></div><span class="circle-arrow" aria-hidden="true">{icon('arrow-up-right')}</span></div>
    </a>'''


def home_page() -> str:
    prefix = ""
    main = f'''
<section class="home-hero">
  <div class="wrap hero-inner">
    <div class="hero-copy reveal">
      <p class="eyebrow">Tile installation systems · Malaysia</p>
      <h1>Strength beneath <span class="accent">every surface.</span></h1>
      <p class="lede">High-performance tile adhesives and admixtures engineered for consistent application, durable results, and professional supply.</p>
      <div class="button-row"><a class="button button-red" href="#products">Explore products {icon('arrow-down', 'arrow')}</a><a class="button" href="{wa_url('Hello MTA, I would like to enquire about your products for wholesale or distribution.')}" target="_blank" rel="noopener">WhatsApp enquiry {icon('arrow-up-right', 'arrow')}</a></div>
    </div>
    <div class="hero-products" aria-label="MTA product range">
      <p class="hero-note">Made for the demands of walls, floors, façades, wet areas, and pools.</p>
      <img class="bag" src="{PRODUCTS['mta991']['image']}" alt="MTA 991 tile adhesive bag">
      <img class="pail" src="{PRODUCTS['mta_admix_123']['image']}" alt="MTA Admix 123 pail">
    </div>
  </div>
</section>
<section class="section" id="products">
  <div class="wrap">
    <div class="intro-grid reveal"><p class="eyebrow">Product range</p><div class="intro-copy"><h2>Built around the way professionals install.</h2><p class="lede">Choose a general cementitious adhesive, step up to flexible performance, or reinforce cement mixes with a latex admixture. Each product page keeps packaging, applications, technical data, and the catalogue together.</p></div></div>
    <div class="product-grid">
      {product_card(prefix, 'mta991', '01')}
      {product_card(prefix, 'mta993', '02')}
      {product_card(prefix, 'mta_admix_123', '03')}
    </div>
  </div>
</section>
<section class="applications section">
  <div class="wrap">
    <div class="section-heading reveal"><div><p class="eyebrow">Application systems</p><h2>Specify by environment.</h2></div><p class="lede">MTA installation diagrams show the recommended system build-up for homogeneous porcelain tiles across three common application areas.</p></div>
    <div class="application-grid">
      <article class="application reveal"><span>01</span><img src="wp-content/uploads/2025/05/MTA_Installation_System_IGA_Full_56.png" alt="MTA installation system diagram for an internal general area" loading="lazy"><h3>Internal General Area</h3></article>
      <article class="application reveal"><span>02</span><img src="wp-content/uploads/2025/05/MTA_Installation_System_EGA_Full_56.png" alt="MTA installation system diagram for an external general area" loading="lazy"><h3>External General Area</h3></article>
      <article class="application reveal"><span>03</span><img src="wp-content/uploads/2025/05/MTA_Installation_System_SP_Full_56.png" alt="MTA installation system diagram for a swimming pool" loading="lazy"><h3>Swimming Pool</h3></article>
    </div>
  </div>
</section>
<section class="section">
  <div class="wrap proof-grid">
    <div class="proof-image reveal"><img src="wp-content/uploads/2025/04/ChatGPT-Image-Apr-10-2025-03_42_38-PM.png" alt="Installer applying tile adhesive with a notched trowel" loading="lazy"></div>
    <div class="reveal"><p class="eyebrow">Why MTA</p><h2>Precision in the mix. Confidence on site.</h2><div class="proof-list">
      <div class="proof-item"><b>01</b><div><h3>Quality</h3><p>Formulated for consistent application and long-term durability in real construction conditions.</p></div></div>
      <div class="proof-item"><b>02</b><div><h3>Versatility</h3><p>Solutions for bathrooms, façades, commercial floors, wet areas, and multiple substrate conditions.</p></div></div>
      <div class="proof-item"><b>03</b><div><h3>Expertise</h3><p>Product knowledge shaped by more than 15 years of tile-adhesive industry experience.</p></div></div>
    </div>
  </div>
</section>
<section class="cta-band section-tight"><div class="wrap cta-inner reveal"><div><p class="eyebrow">Product enquiry</p><h2>Tell us which MTA product you need.</h2></div><a class="button" href="{wa_url('Hello MTA, I would like product information for a wholesale or distribution enquiry.')}" target="_blank" rel="noopener">Start on WhatsApp {icon('arrow-up-right', 'arrow')}</a></div></section>'''
    return page(title="MTA Tiles Adhesive Specialist | Professional Tile Installation Systems", description="Explore MTA tile adhesives and admixtures for professional installation systems in Malaysia. View technical data, download catalogues and enquire on WhatsApp.", path="/", prefix="", image="wp-content/uploads/2025/04/banner_background-1024x683.png", main=main, wa_message="Hello MTA, I would like to enquire about your products for wholesale or distribution.", schema_type="LocalBusiness")


def detail_block(number: str, title: str, content: str, open_by_default: bool = False) -> str:
    return f'''<details{' open' if open_by_default else ''}><summary><span class="num">{number}</span><span>{html.escape(title)}</span></summary><div class="detail-content">{content}</div></details>'''


def list_html(items: list[str], empty: str = "Details will be published when confirmed.") -> str:
    if not items:
        return f"<p>{html.escape(empty)}</p>"
    return "<ul>" + "".join(f"<li>{html.escape(item)}</li>" for item in items) + "</ul>"


def table_html(rows: list[tuple[str, str]], intro: str = "") -> str:
    if not rows:
        return f"<p>{html.escape(intro or 'Details will be published when confirmed.')}</p>"
    body = "".join(f"<tr><td>{html.escape(a)}</td><td>{html.escape(b)}</td></tr>" for a, b in rows)
    intro_html = f'<p class="muted" style="margin-bottom:1rem">{html.escape(intro)}</p>' if intro else ""
    return f'''{intro_html}<div class="table-scroll"><table class="data-table"><thead><tr><th>Property</th><th>Value</th></tr></thead><tbody>{body}</tbody></table></div>'''


def product_page(slug: str) -> str:
    p = PRODUCTS[slug]
    prefix = "../"
    message = f"Hello MTA, I would like to enquire about {p['code']} for wholesale or distribution. Product page: {BASE_URL}/{slug}/"
    badge = '<span class="coming-badge">Coming soon</span>' if p.get("coming") else ""
    pdf_button = f'<a class="button button-light" href="{rel(prefix, p["pdf"])}" target="_blank" rel="noopener">Download technical PDF {icon("arrow-down", "arrow")}</a>' if p.get("pdf") else ""
    coverage = table_html(p["coverage"], "Coverage may vary depending on the nature and flatness of the substrate.") if p["coverage"] else "<p>Coverage data will be published when confirmed.</p>"
    related = "".join(
        f'''<a class="related-card" href="{rel(prefix, other_slug + '/index.html')}"><img src="{rel(prefix, other['image'])}" alt="{html.escape(other['code'])} packaging" loading="lazy"><h3>{html.escape(other['code'])}</h3><span>{html.escape(other['type'])}</span></a>'''
        for other_slug, other in PRODUCTS.items() if other_slug != slug
    )
    main = f'''
<section class="product-hero">
  <div class="wrap breadcrumb"><a href="../index.html">Home</a><span>/</span><a href="../index.html#products">Products</a><span>/</span><span aria-current="page">{html.escape(p['code'])}</span></div>
  <div class="wrap product-hero-grid">
    <div class="product-visual" data-code="{html.escape(p['code'])}"><img src="{rel(prefix, p['image'])}" alt="{html.escape(p['code'])} product packaging"></div>
    <div class="product-summary reveal">{badge}<p class="eyebrow">MTA product system</p><h1>{html.escape(p['code'])}</h1><p class="product-type">{html.escape(p['type'])}</p><p class="product-description">{html.escape(p['description'])}</p>
      <div class="spec-strip"><div><small>Pack size</small><strong>{html.escape(p['package'])}</strong></div><div><small>Classification</small><strong>{html.escape(p['class'])}</strong></div><div><small>Application</small><strong>{html.escape(p['use'])}</strong></div></div>
      <div class="button-row"><a class="button button-red" href="{wa_url(message)}" target="_blank" rel="noopener">Enquire on WhatsApp {icon('arrow-up-right', 'arrow')}</a>{pdf_button}</div>
    </div>
  </div>
</section>
<section class="section">
  <div class="wrap details-layout">
    <aside class="details-aside reveal"><p class="eyebrow">Product detail</p><h2>Everything needed to assess the product.</h2><p>Review applications and limitations before referring to the laboratory technical data. Download the official catalogue for the complete source document.</p></aside>
    <div class="tech-details reveal">
      {detail_block('01', 'Features & applications', list_html(p['features']), True)}
      {detail_block('02', 'Limitations', list_html(p['limitations']))}
      {detail_block('03', 'Technical data', table_html(p['technical'], p['technical_intro']))}
      {detail_block('04', 'Approximate coverage', coverage)}
    </div>
  </div>
</section>
<section class="section-tight"><div class="wrap"><div class="section-heading"><div><p class="eyebrow">Continue browsing</p><h2>Other MTA products.</h2></div><p class="lede">Compare the rest of the range or ask our team which system matches your application.</p></div><div class="related-grid">{related}</div></div></section>
<section class="cta-band section-tight"><div class="wrap cta-inner"><div><p class="eyebrow">Wholesale enquiry</p><h2>Ask about {html.escape(p['code'])}.</h2></div><a class="button" href="{wa_url(message)}" target="_blank" rel="noopener">WhatsApp MTA {icon('arrow-up-right', 'arrow')}</a></div></section>'''
    return page(title=f"{p['code']} | {p['type']} | MTA", description=p["description"], path=f"/{slug}/", prefix=prefix, image=p["image"], main=main, wa_message=message, product=p)


def about_page() -> str:
    prefix = "../"
    main = f'''
<section class="page-hero" data-index="01"><div class="wrap"><div class="breadcrumb"><a href="../index.html">Home</a><span>/</span><span aria-current="page">About</span></div><p class="eyebrow">About MTA</p><h1>Material knowledge, built into every solution.</h1><p class="lede">MTA Tile Adhesive Specialist Sdn Bhd supplies high-performance tile installation and construction materials for residential, commercial, and industrial projects across Malaysia.</p></div></section>
<section class="section"><div class="wrap about-lead"><img class="reveal" src="{rel(prefix, 'wp-content/uploads/2025/04/mix_mortars_image-e1744421499931.png')}" alt="Preparing a cement-based construction mix" loading="lazy"><div class="about-copy reveal"><p class="eyebrow">Company overview</p><h2>A focused specialist for tiling and construction needs.</h2><p>MTA Tile Adhesive Specialist Sdn Bhd is a distributor of the MTA brand and a provider of tile adhesive solutions. Since 2021, the company has focused on dependable building materials and practical product support.</p><div class="history-line"><strong>Since 2021</strong><p>Operating as MTA Tile Adhesive Specialist Sdn Bhd.</p></div><div class="history-line"><strong>15+ years</strong><p>Tile-adhesive industry expertise across manufacturing, product development, and market requirements.</p></div></div></div></section>
<section class="mission-band section"><div class="wrap mission-grid"><div class="reveal"><p class="eyebrow">Vision</p><h2>Raise confidence in tile installation.</h2><p>To lead the market in tile adhesive solutions through reliable products that improve construction project quality across Malaysia.</p></div><div class="reveal"><p class="eyebrow">Mission</p><h2>Be the partner professionals can rely on.</h2><p>To provide high-quality tile adhesives, responsive customer service, and solutions suited to the evolving building and construction industry.</p></div></div></section>
<section class="section"><div class="wrap"><div class="section-heading reveal"><div><p class="eyebrow">Products & services</p><h2>Focused construction capability.</h2></div><p class="lede">The MTA range centres on tile installation while supporting adjacent building-material requirements.</p></div><div class="capability-grid">
  <article class="capability"><p class="eyebrow">01</p><h3>Tile adhesives</h3><p>High-performance adhesives for ceramic, porcelain, and natural stone tiles.</p></article>
  <article class="capability"><p class="eyebrow">02</p><h3>Dry mix mortars</h3><p>Mortar products for masonry and supporting construction applications.</p></article>
  <article class="capability"><p class="eyebrow">03</p><h3>Waterproofing, stone treatment & construction materials</h3><p>Supporting products for water protection, surface maintenance, and residential, commercial, or industrial work.</p></article>
</div></div></section>
<section class="cta-band section-tight"><div class="wrap cta-inner"><div><p class="eyebrow">Talk to MTA</p><h2>Discuss your product requirements.</h2></div><a class="button" href="{wa_url('Hello MTA, I would like to discuss your products for wholesale or distribution.')}" target="_blank" rel="noopener">Start on WhatsApp {icon('arrow-up-right', 'arrow')}</a></div></section>'''
    return page(title="About MTA Tile Adhesive Specialist Sdn Bhd", description="Learn about MTA Tile Adhesive Specialist Sdn Bhd, its tile-adhesive expertise, mission, and construction product capabilities in Malaysia.", path="/about-us/", prefix=prefix, image="wp-content/uploads/2025/04/mix_mortars_image-e1744421499931-1024x577.png", main=main, wa_message="Hello MTA, I would like to discuss your products for wholesale or distribution.")


def contact_page() -> str:
    prefix = "../"
    message = "Hello MTA, I would like to make a wholesale or distribution enquiry."
    main = f'''
<section class="page-hero" data-index="02"><div class="wrap"><div class="breadcrumb"><a href="../index.html">Home</a><span>/</span><span aria-current="page">Contact</span></div><p class="eyebrow">Contact MTA</p><h1>Tell us what product you are looking for.</h1><p class="lede">For product information, availability discussions, or a wholesale enquiry, reach the MTA team directly during business hours.</p></div></section>
<section class="section"><div class="wrap contact-grid">
  <div class="contact-panel reveal"><p class="eyebrow">Company details</p><h2>Direct lines to our team.</h2><dl class="contact-list">
    <div class="contact-item"><dt>Company</dt><dd>MTA Tile Adhesive Specialist Sdn Bhd</dd></div>
    <div class="contact-item"><dt>Telephone</dt><dd><a href="tel:+60124148562">+60 12-414 8562</a></dd></div>
    <div class="contact-item"><dt>Email</dt><dd><a href="mailto:{EMAIL}">{EMAIL}</a></dd></div>
    <div class="contact-item"><dt>Address</dt><dd>{ADDRESS}</dd></div>
    <div class="contact-item"><dt>Hours</dt><dd>Monday–Friday<br>9:00am–6:00pm</dd></div>
  </dl><p class="map-note">Include the product model, required quantity, and delivery location in your enquiry where possible.</p></div>
  <div class="whatsapp-panel reveal"><div class="wa-mark">WA</div><div><p class="eyebrow">Fastest response</p><h2>Start with WhatsApp.</h2><p>Send the product model and a short note about your requirement. The pre-filled message can be edited before sending.</p></div><a class="button" href="{wa_url(message)}" target="_blank" rel="noopener">Open WhatsApp {icon('arrow-up-right', 'arrow')}</a></div>
</div></section>
<section class="section-tight"><div class="wrap"><div class="section-heading"><div><p class="eyebrow">Before you enquire</p><h2>Useful details to include.</h2></div><p class="lede">Product model, estimated quantity, project or resale use, and delivery location help the team understand the request more quickly.</p></div></div></section>'''
    return page(title="Contact MTA Tiles Adhesive Specialist", description=f"Contact MTA Tile Adhesive Specialist Sdn Bhd in Shah Alam by WhatsApp, phone or email for product and wholesale enquiries.", path="/contact-us/", prefix=prefix, image=LOGO, main=main, wa_message=message, schema_type="ContactPage")


def error_page() -> str:
    return f'''<!doctype html><html lang="en"><head>{seo_head(prefix='', title='Page Not Found | MTA', description='The requested MTA page could not be found.', path='/404.html', image=LOGO)}</head><body>{header('')}<main id="main"><section class="page-hero" data-index="404"><div class="wrap"><p class="eyebrow">404 · Page not found</p><h1>This surface has not been prepared.</h1><p class="lede">The page may have moved. Return to the product range or contact MTA for help.</p><div class="button-row" style="margin-top:2rem"><a class="button button-red" href="index.html">View products {icon('arrow-right', 'arrow')}</a><a class="button button-light" href="contact-us/index.html">Contact MTA {icon('arrow-right', 'arrow')}</a></div></div></section></main>{footer('')}<script src="mta-site.js" defer></script></body></html>'''


def write(relative_path: str, content: str) -> None:
    target = STATIC / relative_path
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(content, encoding="utf-8")
    print(f"Built {target.relative_to(ROOT)}")


def build() -> None:
    write("index.html", home_page())
    write("about-us/index.html", about_page())
    write("contact-us/index.html", contact_page())
    for slug in PRODUCTS:
        write(f"{slug}/index.html", product_page(slug))
    write("404.html", error_page())


if __name__ == "__main__":
    build()
