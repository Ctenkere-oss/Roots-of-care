#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Roots of Care — static site builder.

It wraps the shared shell (<head> tags, header, footer, cookie banner,
structured data) around the page content files found in
src/pages/<lang>/<key>.html and writes the finished, 100% static site
into the site/ folder.

    python3 tools/build.py

The site is English only. The builder is still language-aware so a
French version can be added later without rewriting anything:
see "ADDING A SECOND LANGUAGE" at the bottom of README.md.

WARNING: site/ is REGENERATED on every run. If you edit the files in
site/ directly, stop running this script (or carry your edits back
into src/).
"""

import os
import posixpath
import re
import sys
from datetime import date

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "src", "pages")
OUT = os.path.join(ROOT, "site")

# ---------------------------------------------------------------------------
# GENERAL SETTINGS — set these once
# ---------------------------------------------------------------------------
BASE_URL = "https://www.rootsofcare.ca"          # final domain
INSTAGRAM = "https://www.instagram.com/roots.of.care/"
INSTAGRAM_HANDLE = "@roots.of.care"
SNAPCHAT = "https://www.snapchat.com/add/aeilmyy"
SNAPCHAT_HANDLE = "aeilmyy"
LAST_UPDATED = "September 14, 2026"
STUDIO = "Alpha Marketing Studio"

LANGS = ["en"]                                   # add "fr" here for bilingual

# Page order = order of the sitemap
PAGE_ORDER = ["home", "hair", "henna", "services", "booking", "about",
              "contact", "policies", "privacy", "terms"]

# Address of every page, per language
SLUGS = {
    "home":     {"en": "index.html"},
    "hair":     {"en": "hair.html"},
    "henna":    {"en": "henna.html"},
    "services": {"en": "services.html"},
    "booking":  {"en": "booking.html"},
    "about":    {"en": "about.html"},
    "contact":  {"en": "contact.html"},
    "policies": {"en": "booking-policies.html"},
    "privacy":  {"en": "privacy-policy.html"},
    "terms":    {"en": "terms.html"},
}

# Sitemap priority
PRIORITY = {"home": "1.0", "booking": "0.9", "services": "0.9", "hair": "0.9",
            "henna": "0.9", "about": "0.7", "contact": "0.7", "policies": "0.6",
            "privacy": "0.3", "terms": "0.3"}

NAV = ["home", "hair", "henna", "services", "about", "contact"]

LABELS = {
    "en": {
        "home": "Home", "hair": "Hair &amp; Locs", "henna": "Henna",
        "services": "Services", "about": "About", "contact": "Contact",
        "booking": "Book", "policies": "Booking policies",
        "privacy": "Privacy policy", "terms": "Terms of use",
    },
}

UI = {
    "en": {
        "skip": "Skip to main content",
        "menu": "Open menu",
        "book_now": "Book",
        "nav_label": "Main navigation",
        "footer_tagline": "Loc care, natural hair styling, and henna and jagua body art, in Montréal.",
        "footer_nav": "Navigation",
        "footer_info": "Information",
        "footer_policy_title": "Booking",
        "footer_policy": "A non-refundable <strong>$20 deposit</strong> is required in order to book, by e-transfer within 3&nbsp;hours.<br>Cancellations must be made <strong>24&nbsp;hours in advance</strong>.",
        "footer_policy_link": "Read the full policies",
        "rights": "All rights reserved.",
        "credit": "Website by",
        "cookie_title": "Cookies",
        "cookie_text": "This site only uses the cookies it needs in order to work. With your consent we would also like to measure page visits so we can improve it. You can decline with no consequence — nothing is measured before you choose.",
        "cookie_accept": "Accept",
        "cookie_refuse": "Decline",
        "cookie_more": "Learn more",
    },
}


# ---------------------------------------------------------------------------
# LOGO — inline SVG placeholder (replace with the owner's real logo file)
# ---------------------------------------------------------------------------
def logo_full(variant="default", classname="hero__logo",
              title="Roots of Care — Beauty Services"):
    """Full logo: RC monogram watermark + script signature + sub-line."""
    if variant == "light":
        mark, script, sub, mark_op = "#FBF9F5", "#FBF9F5", "#E6DCD3", ".12"
    else:
        mark, script, sub, mark_op = "#FBF9F5", "#7A5647", "#AD9686", "1"
    return f'''<svg class="{classname}" viewBox="0 0 460 172" role="img" aria-label="{title}" xmlns="http://www.w3.org/2000/svg">
      <title>{title}</title>
      <text x="232" y="122" text-anchor="middle" font-family="Georgia, 'Times New Roman', serif" font-size="146" fill="{mark}" opacity="{mark_op}" letter-spacing="6">RC</text>
      <text x="230" y="104" text-anchor="middle" font-family="Parisienne, 'Snell Roundhand', cursive" font-size="62" fill="{script}">Roots of Care</text>
      <text x="234" y="148" text-anchor="middle" font-family="'Josefin Sans', 'Century Gothic', sans-serif" font-weight="300" font-size="21" fill="{sub}" letter-spacing="8.5">BEAUTY SERVICES</text>
    </svg>'''


def logo_compact(title="Roots of Care — Beauty Services"):
    """Reduced version used in the sticky header."""
    return f'''<svg class="logo-lockup" viewBox="0 0 300 80" role="img" aria-label="{title}" xmlns="http://www.w3.org/2000/svg">
      <title>{title}</title>
      <text x="150" y="46" text-anchor="middle" font-family="Parisienne, 'Snell Roundhand', cursive" font-size="42" fill="#7A5647">Roots of Care</text>
      <text x="152" y="68" text-anchor="middle" font-family="'Josefin Sans', 'Century Gothic', sans-serif" font-weight="300" font-size="12" fill="#AD9686" letter-spacing="5.2">BEAUTY SERVICES</text>
    </svg>'''


ICON_INSTAGRAM = ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.3" '
                  'aria-hidden="true" focusable="false"><rect x="3" y="3" width="18" height="18" rx="5"/>'
                  '<circle cx="12" cy="12" r="4"/><circle cx="17.4" cy="6.6" r="1" fill="currentColor" stroke="none"/></svg>')

ICON_SNAPCHAT = ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.3" '
                 'stroke-linejoin="round" aria-hidden="true" focusable="false">'
                 '<path d="M6 11.5V8a6 6 0 0 1 12 0v3.5c0 1.7 1.3 2.4 2.7 2.8.6.2.6 1 0 1.2-1.3.4-2.4 1'
                 '-2.8 2-.2.5-.7.7-1.2.6-.8-.2-1.6 0-2.2.5-1.4 1.1-3 1.1-4.4 0-.6-.5-1.4-.7-2.2-.5-.5.1'
                 '-1-.1-1.2-.6-.4-1-1.5-1.6-2.8-2-.6-.2-.6-1 0-1.2C4.7 13.9 6 13.2 6 11.5Z"/></svg>')


def social_links(light=False):
    """Instagram and Snapchat, side by side."""
    return f'''<ul class="social-list">
          <li><a class="social" href="{INSTAGRAM}" target="_blank" rel="noopener">
            {ICON_INSTAGRAM}<span>{INSTAGRAM_HANDLE}</span>
          </a></li>
          <li><a class="social" href="{SNAPCHAT}" target="_blank" rel="noopener">
            {ICON_SNAPCHAT}<span>{SNAPCHAT_HANDLE}</span>
          </a></li>
        </ul>'''


# ---------------------------------------------------------------------------
# HELPERS
# ---------------------------------------------------------------------------
def rel(from_path, to_path):
    """Relative path between two pages (also works when opened from disk)."""
    return posixpath.relpath(to_path, posixpath.dirname(from_path) or ".")


def parse_page(path):
    """Read a content file and split the metadata header from the body."""
    with open(path, encoding="utf-8") as fh:
        raw = fh.read()
    meta, body = {}, raw
    match = re.match(r"\s*<!--META\s*(.*?)-->\s*", raw, re.S)
    if match:
        for line in match.group(1).strip().splitlines():
            line = line.strip()
            if line and ":" in line:
                key, value = line.split(":", 1)
                meta[key.strip()] = value.strip()
        body = raw[match.end():]
    return meta, body


# ---------------------------------------------------------------------------
# TEMPLATE
# ---------------------------------------------------------------------------
def head(lang, key, meta, self_path, noindex=False):
    a = lambda p: rel(self_path, p)
    canonical = f"{BASE_URL}/{SLUGS[key][lang]}".replace("/index.html", "/") if key in SLUGS else None
    title, desc = meta["title"], meta["description"]

    alternates = "\n".join(
        '<link rel="alternate" hreflang="%s-CA" href="%s">' % (
            l, f"{BASE_URL}/{SLUGS[key][l]}".replace("/index.html", "/"))
        for l in LANGS if key in SLUGS and l in SLUGS[key])
    if key in SLUGS:
        alternates += '\n<link rel="alternate" hreflang="x-default" href="%s">' % (
            f"{BASE_URL}/{SLUGS[key][LANGS[0]]}".replace("/index.html", "/"))

    index_tag = ('<meta name="robots" content="noindex, follow">' if noindex
                 else f'<link rel="canonical" href="{canonical}">')
    og_url = canonical or f"{BASE_URL}/"

    return f'''<!DOCTYPE html>
<html lang="{lang}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
{index_tag}
{alternates}

<!-- Social sharing -->
<meta property="og:type" content="website">
<meta property="og:site_name" content="Roots of Care — Beauty Services">
<meta property="og:locale" content="en_CA">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{og_url}">
<meta property="og:image" content="{BASE_URL}/assets/img/og-roots-of-care.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="Roots of Care — Beauty Services, Montréal">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{title}">
<meta name="twitter:description" content="{desc}">
<meta name="twitter:image" content="{BASE_URL}/assets/img/og-roots-of-care.png">
<meta name="theme-color" content="#E9E5DC">

<!-- Icons -->
<link rel="icon" href="{a('assets/img/favicon.svg')}" type="image/svg+xml">
<link rel="alternate icon" href="{a('assets/img/favicon-32.png')}" sizes="32x32">
<link rel="apple-touch-icon" href="{a('assets/img/apple-touch-icon.png')}">

<!-- Google Fonts (font-display: swap, so text shows immediately) -->
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="preload" as="style" href="https://fonts.googleapis.com/css2?family=Josefin+Sans:wght@300;400&family=Lato:wght@300;400;700&family=Parisienne&display=swap">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Josefin+Sans:wght@300;400&family=Lato:wght@300;400;700&family=Parisienne&display=swap">

<link rel="stylesheet" href="{a('assets/css/styles.css')}">

<!-- Marks the page as JavaScript-capable. Without it, the scroll fade-ins
     stay switched off and every section is visible from the start. -->
<script>document.documentElement.className += " js";</script>
<script src="{a('assets/js/main.js')}" defer></script>
{json_ld(lang, key)}
</head>'''


def json_ld(lang, key):
    """LocalBusiness / HairSalon structured data.
    STILL TO ADD: telephone, email and opening hours (see README.md)."""
    catalogue = [
        ("Loc starting", "Starting locs on natural hair."),
        ("Loc retwist and maintenance", "Regular root maintenance and retwist."),
        ("Loc repair", "Repair, combining and reconstruction of damaged locs."),
        ("No retwist styles", "Styling in between retwists, from $25."),
        ("Men's twists on natural hair", "Small and medium twists, from $65."),
        ("Braids and twists", "Knotless braids, box braids, twists, cornrows."),
        ("Henna body art", "Natural henna, hand designs from $15 and arm sleeves from $45."),
        ("Jagua body art", "Natural jagua gel, hand designs from $20 and arm sleeves from $60."),
        ("Hair treatments", "Deep conditioning and scalp care."),
    ]
    items = ",\n        ".join(
        '{"@type":"Offer","itemOffered":{"@type":"Service","name":"%s","description":"%s"}}' % (n, d)
        for n, d in catalogue)
    booking_url = f"{BASE_URL}/{SLUGS['booking'][lang]}"
    return f'''
<!-- Structured data for Google. STILL TO ADD once known:
     "telephone", "email" and "openingHoursSpecification" (see README.md). -->
<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@type": "HairSalon",
  "@id": "{BASE_URL}/#business",
  "name": "Roots of Care — Beauty Services",
  "alternateName": "Roots of Care",
  "description": "Independent studio in Montréal specialising in locs — starting, retwisting, repair and styling — natural hair care, and henna and jagua body art.",
  "url": "{BASE_URL}/",
  "image": "{BASE_URL}/assets/img/og-roots-of-care.png",
  "logo": "{BASE_URL}/assets/img/logo-roots-of-care.svg",
  "email": "rootsofcare.vv@gmail.com",
  "priceRange": "$$",
  "currenciesAccepted": "CAD",
  "address": {{
    "@type": "PostalAddress",
    "addressLocality": "Montréal",
    "addressRegion": "QC",
    "addressCountry": "CA"
  }},
  "areaServed": {{ "@type": "City", "name": "Montréal" }},
  "knowsLanguage": ["en-CA", "fr-CA"],
  "sameAs": ["{INSTAGRAM}", "{SNAPCHAT}"],
  "potentialAction": {{
    "@type": "ReserveAction",
    "target": {{
      "@type": "EntryPoint",
      "urlTemplate": "{booking_url}",
      "inLanguage": "en-CA",
      "actionPlatform": [
        "http://schema.org/DesktopWebPlatform",
        "http://schema.org/MobileWebPlatform"
      ]
    }},
    "result": {{ "@type": "Reservation", "name": "Appointment at Roots of Care" }}
  }},
  "hasOfferCatalog": {{
    "@type": "OfferCatalog",
    "name": "Services",
    "itemListElement": [
        {items}
    ]
  }}
}}
</script>'''


def header(lang, key, self_path):
    """key = None for a page that is not in the main plan (e.g. 404)."""
    ui, lab = UI[lang], LABELS[lang]
    link = lambda k: rel(self_path, SLUGS[k][lang])

    nav_items = mobile_items = ""
    for k in NAV:
        current = ' aria-current="page"' if k == key else ""
        nav_items += f'          <li><a href="{link(k)}"{current}>{lab[k]}</a></li>\n'
        mobile_items += f'        <li><a href="{link(k)}"{current}>{lab[k]}</a></li>\n'

    return f'''<body>
<a class="skip-link" href="#main">{ui['skip']}</a>

<!-- ========================= HEADER ========================= -->
<header class="site-header">
  <div class="wrap header-inner">

    <!-- LOGO — to use the real logo file, replace the inline <svg> below with:
         <img src="{rel(self_path, 'assets/img/logo-roots-of-care.svg')}"
              alt="Roots of Care — Beauty Services" class="logo-lockup"
              width="300" height="80"> -->
    <a class="brand" href="{link('home')}" aria-label="Roots of Care — {lab['home']}">
      {logo_compact()}
    </a>

    <nav class="nav-desktop" aria-label="{ui['nav_label']}">
      <ul class="nav-list">
{nav_items}      </ul>
    </nav>

    <div class="header-actions">
      <!-- A FR/EN language switcher goes here if a French version is added
           later — see "ADDING A SECOND LANGUAGE" in README.md. -->
      <a class="btn btn--sm" href="{link('booking')}">{ui['book_now']}</a>
      <button class="nav-toggle" type="button" aria-expanded="false"
              aria-controls="nav-mobile" aria-label="{ui['menu']}">
        <span></span><span></span><span></span>
      </button>
    </div>
  </div>
</header>

<!-- Full-screen mobile menu -->
<nav class="nav-mobile" id="nav-mobile" aria-label="{ui['nav_label']}">
  <div class="wrap">
    <ul>
{mobile_items}      <li><a href="{link('policies')}">{lab['policies']}</a></li>
    </ul>
    <a class="btn" href="{link('booking')}">{ui['book_now']}</a>
    <p class="mobile-meta">
      <a href="{INSTAGRAM}" target="_blank" rel="noopener">{INSTAGRAM_HANDLE}</a>
      &nbsp;·&nbsp;
      <a href="{SNAPCHAT}" target="_blank" rel="noopener">Snapchat</a>
    </p>
  </div>
</nav>
'''


def footer(lang, key, self_path):
    """key = None for a page that is not in the main plan (e.g. 404)."""
    ui, lab = UI[lang], LABELS[lang]
    link = lambda k: rel(self_path, SLUGS[k][lang])
    year = date.today().year

    nav_links = "".join(f'          <li><a href="{link(k)}">{lab[k]}</a></li>\n' for k in NAV)
    info_links = "".join(f'          <li><a href="{link(k)}">{lab[k]}</a></li>\n'
                         for k in ["booking", "services", "policies", "privacy", "terms"])

    return f'''
<!-- ======================== FOOTER ========================= -->
<footer class="site-footer">
  <div class="wrap footer-inner">
    <div class="footer-grid">

      <div>
        {logo_full(variant="light", classname="footer-logo")}
        <p>{ui['footer_tagline']}</p>
        {social_links(light=True)}
        <!-- CONTACT DETAILS — the phone number is still to be added -->
        <p class="small" style="color:var(--on-brown-muted);margin-top:.9rem">
          <a href="mailto:rootsofcare.vv@gmail.com">rootsofcare.vv@gmail.com</a><br>
          <span class="fill">[[PHONE]]</span>
        </p>
      </div>

      <div>
        <h4>{ui['footer_nav']}</h4>
        <ul class="footer-links">
{nav_links}        </ul>
      </div>

      <div>
        <h4>{ui['footer_info']}</h4>
        <ul class="footer-links">
{info_links}        </ul>
      </div>

      <div>
        <h4>{ui['footer_policy_title']}</h4>
        <div class="footer-policy">
          <p>{ui['footer_policy']}</p>
          <p style="margin-top:1rem"><a href="{link('policies')}">{ui['footer_policy_link']}</a></p>
        </div>
      </div>

    </div>

    <div class="footer-bottom">
      <p>© <span data-year>{year}</span> Roots of Care — Beauty Services. {ui['rights']}</p>
      <p>{ui['credit']} {STUDIO}</p>
    </div>
  </div>
</footer>

<!-- ================== COOKIE BANNER (Law 25) ==================
     Declining is exactly as easy as accepting, and no measurement
     cookie is dropped before the visitor has chosen. -->
<aside class="cookie-banner" id="cookie-banner" role="dialog"
       aria-live="polite" aria-label="{ui['cookie_title']}">
  <p>{ui['cookie_text']} <a href="{link('privacy')}">{ui['cookie_more']}</a></p>
  <div class="btn-row">
    <button class="btn btn--sm" type="button" data-consent="accepted">{ui['cookie_accept']}</button>
    <button class="btn btn--sm btn--ghost" type="button" data-consent="refused">{ui['cookie_refuse']}</button>
  </div>
</aside>

</body>
</html>
'''


def expand(body, lang, self_path):
    """Replace the {{...}} tokens used inside the content files."""
    prefix = "../" * self_path.count("/")
    body = body.replace("{{P}}", prefix)
    for k, slug in SLUGS.items():
        body = body.replace("{{%s}}" % k.upper(), rel(self_path, slug[lang]))
    body = body.replace("{{LOGO_FULL}}", logo_full())
    body = body.replace("{{INSTAGRAM}}", INSTAGRAM)
    body = body.replace("{{INSTAGRAM_HANDLE}}", INSTAGRAM_HANDLE)
    body = body.replace("{{SNAPCHAT}}", SNAPCHAT)
    body = body.replace("{{SNAPCHAT_HANDLE}}", SNAPCHAT_HANDLE)
    body = body.replace("{{UPDATED}}", LAST_UPDATED)
    body = body.replace("{{BASE_URL}}", BASE_URL)
    return body


def render(lang, key, meta, body, self_path=None, noindex=False):
    self_path = self_path or SLUGS[key][lang]
    out = head(lang, key, meta, self_path, noindex=noindex)
    out += header(lang, key, self_path)
    out += '\n<main id="main">\n'
    out += expand(body, lang, self_path).rstrip() + "\n"
    out += "</main>\n"
    out += footer(lang, key, self_path)
    return out


# ---------------------------------------------------------------------------
# EXTRA FILES
# ---------------------------------------------------------------------------
def write(path, content):
    full = os.path.join(OUT, path)
    os.makedirs(os.path.dirname(full) or OUT, exist_ok=True)
    with open(full, "w", encoding="utf-8") as fh:
        fh.write(content)


def build_sitemap():
    today = date.today().isoformat()
    entries = []
    for key in PAGE_ORDER:
        for lang in LANGS:
            loc = f"{BASE_URL}/{SLUGS[key][lang]}".replace("/index.html", "/")
            entries.append(
                f"  <url>\n    <loc>{loc}</loc>\n"
                f"    <lastmod>{today}</lastmod>\n"
                f"    <changefreq>monthly</changefreq>\n"
                f"    <priority>{PRIORITY[key]}</priority>\n  </url>")
    write("sitemap.xml", '<?xml version="1.0" encoding="UTF-8"?>\n'
          '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
          + "\n".join(entries) + "\n</urlset>\n")


def build_robots():
    write("robots.txt", f"""# robots.txt — Roots of Care
User-agent: *
Allow: /

Sitemap: {BASE_URL}/sitemap.xml
""")


def build_404():
    meta = {"title": "Page not found — Roots of Care",
            "description": "This page does not exist or has been moved."}
    body = '''
<section class="error-page wrap">
  <p class="code">404</p>
  <h1>This page doesn&rsquo;t exist</h1>
  <p class="lead measure" style="margin-inline:auto">
    The link may be out of date or slightly mistyped. Everything else is still
    exactly where you left it.
  </p>
  <div class="btn-row">
    <a class="btn" href="{{HOME}}">Back to home</a>
    <a class="btn btn--ghost" href="{{BOOKING}}">Book an appointment</a>
  </div>
</section>
'''
    write("404.html", render("en", "home", meta, body, self_path="404.html", noindex=True))


# ---------------------------------------------------------------------------
# MAIN
# ---------------------------------------------------------------------------
def main():
    count = 0
    for lang in LANGS:
        for key in PAGE_ORDER:
            path = os.path.join(SRC, lang, key + ".html")
            if not os.path.exists(path):
                print(f"  !  missing: src/pages/{lang}/{key}.html")
                continue
            meta, body = parse_page(path)
            if "title" not in meta or "description" not in meta:
                sys.exit(f"ERROR: title/description missing in {path}")
            write(SLUGS[key][lang], render(lang, key, meta, body))
            count += 1
    build_404()
    build_sitemap()
    build_robots()
    print(f"OK — {count} pages written to site/ (plus 404, sitemap, robots)")


if __name__ == "__main__":
    main()
