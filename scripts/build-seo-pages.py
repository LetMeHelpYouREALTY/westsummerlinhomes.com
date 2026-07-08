#!/usr/bin/env python3
"""Generate SEO/geo pages and sync shared site chrome across all HTML pages."""

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

NAP = {
    "business": "West Summerlin Homes by Dr. Jan Duffy",
    "agent": "Dr. Jan Duffy",
    "brokerage": "BHHS Nevada Properties",
    "phone": "702-222-1964",
    "phone_tel": "tel:7022221964",
    "email": "janet@westsummerlinhomes.com",
    "street": "1234 Summerlin Parkway",
    "city": "Las Vegas",
    "region": "NV",
    "postal": "89134",
    "license": "S.0197614.LLC",
    "url": "https://westsummerlinhomes.com",
}

REALSCOUT_AGENT_ID = "QWdlbnQtMjI1MDUw"
REALSCOUT_PORTAL_URL = "https://drjanduffy.realscout.com/"

NAV_LINKS = [
    ("index.html", "Home", "index.html"),
    ("about.html", "About", "about.html"),
    ("buyers.html", "Buy", "buyers.html"),
    ("sellers.html", "Sell", "sellers.html"),
    ("properties.html", "Properties", "properties.html"),
    (REALSCOUT_PORTAL_URL, "MLS Search", "_external"),
    ("neighborhoods.html", "Neighborhoods", "neighborhoods.html"),
    ("faq.html", "FAQ", "faq.html"),
    ("contact.html", "Contact", "contact.html"),
]

FOOTER_EXPLORE = [
    ("index.html", "Home"),
    ("buyers.html", "Buyers Guide"),
    ("sellers.html", "Sellers Guide"),
    ("properties.html", "Properties"),
    (REALSCOUT_PORTAL_URL, "MLS Search Portal"),
    ("neighborhoods.html", "Neighborhoods"),
    ("luxury-homes.html", "Luxury Homes"),
    ("market-update.html", "Market Update"),
    ("home-valuation.html", "Home Valuation"),
    ("faq.html", "FAQ"),
    ("testimonials.html", "Testimonials"),
    ("about.html", "About"),
    ("contact.html", "Contact"),
]

NEIGHBORHOOD_PAGES = [
    {
        "slug": "red-rock-country-club",
        "name": "Red Rock Country Club",
        "title": "Red Rock Country Club Homes for Sale | West Summerlin",
        "description": "Golf-course estate homes in Red Rock Country Club, West Summerlin. Current listings, pricing trends, and private tours with Dr. Jan Duffy.",
        "price_range": "$1.2M – $5M+",
        "highlights": ["Golf course living", "Guard-gated", "Mountain views", "Custom estates"],
        "summary": "Red Rock Country Club is one of West Summerlin's premier guard-gated communities, known for championship golf, custom estates, and Red Rock Canyon views.",
    },
    {
        "slug": "the-ridges-summerlin",
        "name": "The Ridges",
        "title": "The Ridges Summerlin Homes for Sale | Luxury Real Estate",
        "description": "Luxury homes in The Ridges, Summerlin West. Explore current inventory, village amenities, and schedule a private tour with Dr. Jan Duffy.",
        "price_range": "$1.5M – $8M+",
        "highlights": ["Ultra-luxury custom homes", "Strip views", "Private enclaves", "Resort amenities"],
        "summary": "The Ridges offers ultra-luxury custom homes perched above the Las Vegas valley with dramatic views and exclusive village settings.",
    },
    {
        "slug": "summerlin-centre",
        "name": "Summerlin Centre",
        "title": "Summerlin Centre Homes for Sale | West Summerlin Real Estate",
        "description": "Homes for sale in Summerlin Centre — parks, trails, and walkable amenities in the heart of West Summerlin. Expert guidance from Dr. Jan Duffy.",
        "price_range": "$550K – $1.2M",
        "highlights": ["Parks and trails", "Downtown Summerlin access", "Newer construction", "Walkable amenities"],
        "summary": "Summerlin Centre blends newer construction with parks, trails, and convenient access to Downtown Summerlin shopping and dining.",
    },
    {
        "slug": "the-trails-summerlin",
        "name": "The Trails",
        "title": "The Trails Summerlin Homes for Sale | Established West Summerlin",
        "description": "Established homes in The Trails, Summerlin West. Mature landscaping, larger lots, and strong resale values. Listings and tours with Dr. Jan Duffy.",
        "price_range": "$650K – $1.5M",
        "highlights": ["Mature trees", "Larger lots", "Established community", "Strong resale demand"],
        "summary": "The Trails is an established Summerlin village prized for mature landscaping, generous lot sizes, and consistent buyer demand.",
    },
    {
        "slug": "regency-at-summerlin",
        "name": "Regency at Summerlin",
        "title": "Regency at Summerlin Homes for Sale | 55+ West Summerlin",
        "description": "Homes for sale in Regency at Summerlin — active-adult living with clubhouse, fitness, and low-maintenance homes in West Summerlin.",
        "price_range": "$450K – $850K",
        "highlights": ["55+ community", "Clubhouse", "Fitness center", "Low-maintenance living"],
        "summary": "Regency at Summerlin is an active-adult village offering clubhouse amenities, fitness facilities, and low-maintenance residences in West Summerlin.",
    },
    {
        "slug": "stonebridge-summerlin",
        "name": "Stonebridge",
        "title": "Stonebridge Summerlin Homes for Sale | Golf Community",
        "description": "Homes for sale in Stonebridge, Summerlin West near Angel Park. Golf-side residences with pool access and strong resale demand.",
        "price_range": "$600K – $1.4M",
        "highlights": ["Golf community", "Pool access", "Angel Park proximity", "Summerlin West"],
        "summary": "Stonebridge is a golf-side Summerlin village near Angel Park, known for resort-style amenities, pool access, and steady resale demand.",
    },
]


def schema_graph(page_type: str, title: str, description: str, url: str, breadcrumb: list, extra: list | None = None) -> str:
    graph = [
        {
            "@type": "WebPage",
            "@id": f"{url}#webpage",
            "url": url,
            "name": title,
            "description": description,
            "isPartOf": {"@id": f"{NAP['url']}/#website"},
            "about": {"@id": f"{NAP['url']}/#agent"},
        },
        {
            "@type": "BreadcrumbList",
            "itemListElement": [
                {
                    "@type": "ListItem",
                    "position": i + 1,
                    "name": item["name"],
                    "item": item.get("item", url if i == len(breadcrumb) - 1 else NAP["url"]),
                }
                for i, item in enumerate(breadcrumb)
            ],
        },
        {
            "@type": "RealEstateAgent",
            "@id": f"{NAP['url']}/#agent",
            "name": NAP["agent"],
            "url": NAP["url"],
            "telephone": format_phone_e164(NAP["phone"]),
            "email": NAP["email"],
            "address": {
                "@type": "PostalAddress",
                "streetAddress": NAP["street"],
                "addressLocality": NAP["city"],
                "addressRegion": NAP["region"],
                "postalCode": NAP["postal"],
                "addressCountry": "US",
            },
            "areaServed": ["Las Vegas", "Summerlin", "West Summerlin"],
            "memberOf": {"@type": "Organization", "name": NAP["brokerage"]},
            "identifier": NAP["license"],
        },
        {
            "@type": ["LocalBusiness", "RealEstateAgent"],
            "@id": f"{NAP['url']}/#localbusiness",
            "name": NAP["business"],
            "url": NAP["url"],
            "telephone": format_phone_e164(NAP["phone"]),
            "email": NAP["email"],
            "address": {
                "@type": "PostalAddress",
                "streetAddress": NAP["street"],
                "addressLocality": NAP["city"],
                "addressRegion": NAP["region"],
                "postalCode": NAP["postal"],
                "addressCountry": "US",
            },
            "geo": {
                "@type": "GeoCoordinates",
                "latitude": 36.1699,
                "longitude": -115.3338,
            },
            "openingHoursSpecification": [
                {
                    "@type": "OpeningHoursSpecification",
                    "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"],
                    "opens": "08:00",
                    "closes": "20:00",
                }
            ],
            "priceRange": "$$$",
        },
    ]
    if extra:
        graph.extend(extra)
    payload = {"@context": "https://schema.org", "@graph": graph}
    return json.dumps(payload, indent=2)


def header_html(active: str) -> str:
    nav_items = []
    for href, label, match in NAV_LINKS:
        if match == "_external":
            nav_items.append(
                f'                <li><a href="{href}" target="_blank" rel="noopener noreferrer">{label}</a></li>'
            )
            continue
        cls = ' class="active"' if match == active else ""
        nav_items.append(f'                <li><a href="{href}"{cls}>{label}</a></li>')
    nav_items.append('                <li><a href="#" class="calendly-popup nav-schedule">Schedule</a></li>')
    return f"""    <header>
        <nav class="container">
            <a href="index.html" class="logo">
                <img src="https://cdn.jsdelivr.net/gh/LetMeHelpYouREALTY/westsummerlinhomes.com@main/images/logo.png" alt="West Summerlin Homes by Dr. Jan Duffy" width="42" height="42" loading="eager">
                <span class="logo-text">
                    <span class="logo-title">West Summerlin Homes</span>
                    <span class="logo-subtitle">by Dr. Jan Duffy</span>
                </span>
            </a>
            <a href="{NAP['phone_tel']}" class="nav-call">📞 {NAP['phone']}</a>
            <button type="button" class="nav-toggle" aria-label="Open menu" aria-expanded="false" aria-controls="site-nav">
                <span class="nav-toggle-bar"></span>
                <span class="nav-toggle-bar"></span>
                <span class="nav-toggle-bar"></span>
            </button>
            <ul class="nav-links" id="site-nav">
{chr(10).join(nav_items)}
            </ul>
        </nav>
    </header>"""


def footer_html() -> str:
    explore = []
    for href, label in FOOTER_EXPLORE:
        if href.startswith("http"):
            explore.append(
                f'                    <li><a href="{href}" target="_blank" rel="noopener noreferrer">{label}</a></li>'
            )
        else:
            explore.append(f'                    <li><a href="{href}">{label}</a></li>')
    explore_html = "\n".join(explore)
    return f"""    <footer class="site-footer">
        <div class="container footer-grid">
            <div class="footer-brand">
                <strong>West Summerlin Homes</strong>
                <span>by Dr. Jan Duffy</span>
                <p>Luxury real estate in West Summerlin and the greater Las Vegas valley.</p>
            </div>
            <div class="footer-nav">
                <h4>Explore</h4>
                <ul>
{explore_html}
                </ul>
            </div>
            <div class="footer-contact">
                <h4>Contact</h4>
                <p>{NAP['agent']}<br>{NAP['brokerage']}</p>
                <p><a href="{NAP['phone_tel']}">{NAP['phone']}</a></p>
                <p>License #{NAP['license']}</p>
            </div>
        </div>
        <div class="footer-bottom container">
            <p>&copy; 2026 {NAP['business']}. All rights reserved. <a href="#" class="calendly-popup calendly-link-btn">Schedule time with me</a></p>
        </div>
    </footer>

    <div class="sticky-call-bar">
        <a href="{NAP['phone_tel']}">Call {NAP['phone']}</a>
        <a href="#" class="calendly-popup">Schedule</a>
    </div>

    <script src="https://assets.calendly.com/assets/external/widget.js" async></script>
    <script src="/site.js"></script>
    <script src="/calendly.js"></script>
</body>
</html>"""


def head_block(title: str, description: str, canonical: str, schema: str) -> str:
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <meta name="description" content="{description}">
    <meta name="robots" content="index, follow">
    <link rel="canonical" href="{canonical}">
    <meta name="geo.region" content="US-NV">
    <meta name="geo.placename" content="Las Vegas, Summerlin">
    <meta property="og:title" content="{title}">
    <meta property="og:description" content="{description}">
    <meta property="og:url" content="{canonical}">
    <meta property="og:type" content="website">
    <link rel="icon" href="https://cdn.jsdelivr.net/gh/LetMeHelpYouREALTY/westsummerlinhomes.com@main/images/logo.png" type="image/png">
    <link rel="stylesheet" href="/site.css">
    <script src="https://em.realscout.com/widgets/realscout-web-components.umd.js" type="module"></script>
    <link href="https://assets.calendly.com/assets/external/widget.css" rel="stylesheet">
    <script type="application/ld+json">
{schema}
    </script>
</head>
<body>"""


def format_phone_e164(phone: str) -> str:
    digits = "".join(ch for ch in phone if ch.isdigit())
    if len(digits) == 10:
        return f"+1-{digits[:3]}-{digits[3:6]}-{digits[6:]}"
    return phone


def breadcrumb_html(items: list) -> str:
    crumbs = []
    for i, item in enumerate(items):
        if isinstance(item, dict):
            label = item["name"]
            href = item.get("item", "#")
        else:
            href, label = item

        if href.startswith(NAP["url"]):
            path = href[len(NAP["url"]) :].lstrip("/")
            href = "index.html" if not path else path

        if i == len(items) - 1:
            crumbs.append(f'                <li class="breadcrumb-item" aria-current="page">{label}</li>')
        else:
            crumbs.append(f'                <li class="breadcrumb-item"><a href="{href}">{label}</a></li>')
    return f"""    <nav class="breadcrumb-nav" aria-label="Breadcrumb">
        <div class="container">
            <ol class="breadcrumb-list">
{chr(10).join(crumbs)}
            </ol>
        </div>
    </nav>"""


def contact_section(title: str = "Get In Touch") -> str:
    return f"""    <section class="contact">
        <div class="container">
            <h2 class="section-title">{title}</h2>
            <p class="section-subtitle">Call {NAP['phone']} or book an in-person consultation with Dr. Jan Duffy.</p>
            <div class="contact-cta-group">
                <a href="#" class="cta-button calendly-popup">Schedule Consultation</a>
                <a href="{NAP['phone_tel']}" class="cta-button cta-button-outline">Call {NAP['phone']}</a>
            </div>
        </div>
    </section>"""


def realscout_portal_banner(
    title: str = "Search Live MLS Listings",
    text: str = "Browse every active listing on Dr. Jan Duffy's RealScout portal — updated every 5 minutes.",
) -> str:
    return f"""            <div class="realscout-portal-banner">
                <div>
                    <h3>{title}</h3>
                    <p>{text}</p>
                </div>
                <a href="{REALSCOUT_PORTAL_URL}" class="btn-primary" target="_blank" rel="noopener noreferrer">Open MLS Search Portal</a>
            </div>"""


def realscout_advanced_search_section(
    title: str = "Find Your Perfect Home",
    subtitle: str = "Filter by price, beds, baths, and neighborhood across West Summerlin.",
) -> str:
    return f"""    <section class="search-section">
        <div class="container">
            <h2 class="section-title">{title}</h2>
            <p class="section-subtitle">{subtitle}</p>
            <div class="search-container">
                <realscout-advanced-search agent-encoded-id="{REALSCOUT_AGENT_ID}"></realscout-advanced-search>
                {realscout_portal_banner("Want the full map experience?", "Save searches, favorite homes, and get alerts on drjanduffy.realscout.com.")}
            </div>
        </div>
    </section>"""


def realscout_listings_section(
    title: str = "Current Listings",
    sort_order: str = "STATUS_AND_SIGNIFICANT_CHANGE",
    price_min: str = "600000",
    price_max: str = "750000",
    property_types: str = "SFR,MF",
    listing_status: str = "For Sale",
) -> str:
    return f"""    <section class="realscout-listings">
        <div class="container">
            <h2 class="section-title">{title}</h2>
            <realscout-office-listings agent-encoded-id="{REALSCOUT_AGENT_ID}" sort-order="{sort_order}" listing-status="{listing_status}" property-types="{property_types}" price-min="{price_min}" price-max="{price_max}"></realscout-office-listings>
            <p class="realscout-portal-note">Data courtesy of GLVAR · <a href="{REALSCOUT_PORTAL_URL}" target="_blank" rel="noopener noreferrer">Search all listings on RealScout</a></p>
        </div>
    </section>"""


def realscout_home_value_section(
    title: str = "What's Your Home Worth?",
    subtitle: str = "Get an instant estimate powered by RealScout MLS data.",
) -> str:
    return f"""    <section class="realscout-home-value-section">
        <div class="container">
            <h2 class="section-title">{title}</h2>
            <p class="section-subtitle">{subtitle}</p>
            <div class="realscout-home-value-wrap fade-in">
                <realscout-home-value agent-encoded-id="{REALSCOUT_AGENT_ID}"></realscout-home-value>
            </div>
            <p class="realscout-portal-note"><a href="home-valuation.html">Full valuation page</a> · <a href="{REALSCOUT_PORTAL_URL}" target="_blank" rel="noopener noreferrer">Browse MLS on RealScout</a></p>
        </div>
    </section>"""


def listings_section() -> str:
    return realscout_listings_section()


def nap_block() -> str:
    return f"""            <div class="nap-block">
                <strong>{NAP['business']}</strong>
                <p>{NAP['brokerage']}<br>{NAP['street']}, {NAP['city']}, {NAP['region']} {NAP['postal']}</p>
                <p><a href="{NAP['phone_tel']}">{NAP['phone']}</a> · License #{NAP['license']}</p>
            </div>"""


def write_page(filename: str, active: str, title: str, description: str, breadcrumb: list, body: str, schema_extra: list | None = None):
    url = f"{NAP['url']}/{filename}"
    schema = schema_graph("WebPage", title, description, url, breadcrumb, schema_extra)
    content = "\n".join([
        head_block(title, description, url, schema),
        header_html(active),
        breadcrumb_html(breadcrumb),
        body,
        contact_section(),
        footer_html(),
    ])
    (ROOT / filename).write_text(content, encoding="utf-8")
    print(f"Wrote {filename}")


def generate_buyers():
    body = f"""    <section class="page-header">
        <div class="container fade-in">
            <p class="section-eyebrow">Buyers Guide</p>
            <h1>Buying a Home in West Summerlin</h1>
            <p>Step-by-step guidance from pre-approval to closing — with local market data and private showings seven days a week.</p>
            <div class="cta-actions">
                <a href="{REALSCOUT_PORTAL_URL}" class="cta-button" target="_blank" rel="noopener noreferrer">Search MLS Listings</a>
                <a href="#" class="cta-button cta-button-outline calendly-popup">Schedule Consultation</a>
            </div>
        </div>
    </section>

{realscout_advanced_search_section("Search West Summerlin Homes", "Live MLS filters for buyers across Summerlin West and Las Vegas.")}

    <section class="content-page">
        <div class="container content-body">
            <h2>Your West Summerlin Buying Roadmap</h2>
            <p>Dr. Jan Duffy guides buyers through every stage — financing, neighborhood selection, offer strategy, inspections, and closing — with data-backed advice tailored to the Las Vegas market.</p>
            <ol>
                <li><strong>Get pre-approved</strong> — Know your budget before you tour.</li>
                <li><strong>Choose your village</strong> — Compare <a href="neighborhoods.html">West Summerlin neighborhoods</a> by price, amenities, and commute.</li>
                <li><strong>Tour strategically</strong> — Private showings scheduled around your calendar.</li>
                <li><strong>Make a competitive offer</strong> — Pricing and terms based on current MLS data.</li>
                <li><strong>Close with confidence</strong> — Inspection, appraisal, and escrow managed start to finish.</li>
            </ol>
            {nap_block()}
            <div class="related-links">
                <a href="neighborhoods.html">Neighborhoods</a>
                <a href="luxury-homes.html">Luxury Homes</a>
                <a href="market-update.html">Market Update</a>
                <a href="faq.html">FAQ</a>
            </div>
        </div>
    </section>

{listings_section()}"""
    write_page("buyers.html", "buyers.html", "Buy a Home in West Summerlin | Buyers Guide | Dr. Jan Duffy",
               "Complete home buying guide for West Summerlin and Las Vegas. Pre-approval, neighborhood tours, offers, and closing with Dr. Jan Duffy.",
               [{"name": "Home", "item": NAP["url"]}, {"name": "Buyers Guide", "item": f"{NAP['url']}/buyers.html"}], body)


def generate_sellers():
    body = f"""    <section class="page-header">
        <div class="container fade-in">
            <p class="section-eyebrow">Sellers Guide</p>
            <h1>Sell Your West Summerlin Home</h1>
            <p>Pricing strategy, staging guidance, and marketing that puts your listing in front of qualified buyers.</p>
            <div class="cta-actions">
                <a href="home-valuation.html" class="cta-button">Home Value Estimate</a>
                <a href="#" class="cta-button cta-button-outline calendly-popup">Schedule Listing Consult</a>
            </div>
        </div>
    </section>

{realscout_home_value_section("Instant Home Value", "Start with RealScout, then book a full MLS pricing consult with Dr. Jan Duffy.")}

    <section class="content-page">
        <div class="container content-body">
            <h2>How Dr. Jan Duffy Sells West Summerlin Homes</h2>
            <p>From pricing analysis to closing, sellers receive a clear plan backed by current MLS comps and proven marketing across digital, print, and agent networks.</p>
            <ul>
                <li>Comparative market analysis with recent sold data</li>
                <li>Professional photography and listing syndication</li>
                <li>Targeted outreach to relocation and investor buyers</li>
                <li>Negotiation and contract management through escrow</li>
            </ul>
            {nap_block()}
            <div class="related-links">
                <a href="home-valuation.html">Home Valuation</a>
                <a href="market-update.html">Market Update</a>
                <a href="testimonials.html">Client Reviews</a>
            </div>
        </div>
    </section>"""
    write_page("sellers.html", "sellers.html", "Sell Your West Summerlin Home | Sellers Guide | Dr. Jan Duffy",
               "Sell your West Summerlin home with expert pricing, marketing, and negotiation. Free valuation and listing consultation with Dr. Jan Duffy.",
               [{"name": "Home", "item": NAP["url"]}, {"name": "Sellers Guide", "item": f"{NAP['url']}/sellers.html"}], body)


def generate_faq():
    faqs = [
        ("What areas does Dr. Jan Duffy serve?", "West Summerlin, Summerlin West, and the greater Las Vegas valley including Red Rock Country Club, The Ridges, Summerlin Centre, and The Trails."),
        ("How do I schedule a private showing?", f"Call {NAP['phone']} or use the Schedule Consultation button to book an in-person consultation. Showings are available seven days a week."),
        ("What is the median home price in West Summerlin?", "Pricing varies by village and property type. Contact Dr. Jan Duffy for a current market snapshot based on active MLS data."),
        ("Do you work with first-time buyers?", "Yes. Dr. Duffy walks first-time buyers through financing, offers, inspections, and closing with clear step-by-step guidance."),
        ("How long do homes stay on the market in Summerlin?", "Days on market shift with inventory and rates. Dr. Duffy provides current averages during your consultation."),
        ("What license does Dr. Jan Duffy hold?", f"Nevada real estate license #{NAP['license']} with BHHS Nevada Properties."),
    ]
    faq_items = "\n".join(
        f"""                <article class="faq-item">
                    <h3>{q}</h3>
                    <p>{a}</p>
                </article>""" for q, a in faqs
    )
    faq_schema = {
        "@type": "FAQPage",
        "mainEntity": [
            {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}}
            for q, a in faqs
        ],
    }
    body = f"""    <section class="page-header">
        <div class="container fade-in">
            <p class="section-eyebrow">FAQ</p>
            <h1>Frequently Asked Questions</h1>
            <p>Answers about buying, selling, and touring homes in West Summerlin and Las Vegas.</p>
        </div>
    </section>

    <section class="content-page">
        <div class="container">
            <div class="faq-list fade-in">
{faq_items}
            </div>
            {nap_block()}
        </div>
    </section>"""
    write_page("faq.html", "faq.html", "FAQ | West Summerlin Real Estate | Dr. Jan Duffy",
               "Frequently asked questions about buying and selling homes in West Summerlin, Las Vegas. Scheduling, pricing, areas served, and more.",
               [{"name": "Home", "item": NAP["url"]}, {"name": "FAQ", "item": f"{NAP['url']}/faq.html"}], body, [faq_schema])


def generate_market():
    body = f"""    <section class="page-header">
        <div class="container fade-in">
            <p class="section-eyebrow">Market Data</p>
            <h1>West Summerlin Market Update</h1>
            <p>Current trends for buyers and sellers in Summerlin West and the greater Las Vegas valley.</p>
        </div>
    </section>

    <section class="content-page">
        <div class="container content-body">
            <p>Live MLS data updates every 5 minutes on Dr. Jan Duffy's RealScout portal. Use the search and listing tools below, or open the full map experience for saved searches and alerts.</p>
            {realscout_portal_banner()}
            {nap_block()}
        </div>
    </section>

{realscout_advanced_search_section("Search the West Summerlin Market", "Filter active listings by price, beds, baths, and area.")}

{realscout_listings_section("Active Listings Snapshot", price_min="400000", price_max="2000000")}"""
    write_page("market-update.html", "market-update.html", "West Summerlin Market Update | Las Vegas Real Estate",
               "West Summerlin and Las Vegas real estate market trends. Current pricing, inventory, and days on market with Dr. Jan Duffy.",
               [{"name": "Home", "item": NAP["url"]}, {"name": "Market Update", "item": f"{NAP['url']}/market-update.html"}], body)


def generate_luxury():
    body = f"""    <section class="page-header">
        <div class="container fade-in">
            <p class="section-eyebrow">Luxury Homes</p>
            <h1>Luxury Homes in West Summerlin</h1>
            <p>Estate properties, golf-course residences, and custom builds from $1M+ across Summerlin's premier villages.</p>
            <div class="cta-actions">
                <a href="{REALSCOUT_PORTAL_URL}" class="cta-button" target="_blank" rel="noopener noreferrer">Search Luxury MLS</a>
                <a href="#" class="cta-button cta-button-outline calendly-popup">Private Tour</a>
            </div>
        </div>
    </section>

    <section class="content-page">
        <div class="container content-body">
            <h2>Featured Luxury Villages</h2>
            <div class="related-links">
                <a href="red-rock-country-club.html">Red Rock Country Club</a>
                <a href="the-ridges-summerlin.html">The Ridges</a>
                <a href="the-trails-summerlin.html">The Trails</a>
            </div>
            <p>Dr. Jan Duffy specializes in luxury transactions — discreet showings, off-market opportunities, and negotiation for high-value properties.</p>
            {nap_block()}
        </div>
    </section>

{realscout_listings_section("Luxury Listings $800K – $1M+", sort_order="SOLD_DATE_NEWEST", price_min="800000", price_max="1000000", property_types=",SFR,MOBILE")}"""
    write_page("luxury-homes.html", "properties.html", "Luxury Homes West Summerlin | $1M+ Estates | Dr. Jan Duffy",
               "Luxury homes and estates for sale in West Summerlin — Red Rock Country Club, The Ridges, and premier Summerlin villages.",
               [{"name": "Home", "item": NAP["url"]}, {"name": "Luxury Homes", "item": f"{NAP['url']}/luxury-homes.html"}], body)


def generate_valuation():
    body = f"""    <section class="page-header">
        <div class="container fade-in">
            <p class="section-eyebrow">Home Valuation</p>
            <h1>What's Your Home Worth?</h1>
            <p>Enter your address below for an instant home value estimate powered by RealScout.</p>
        </div>
    </section>

    <section class="realscout-home-value-section">
        <div class="container">
            <div class="realscout-home-value-wrap fade-in">
                <realscout-home-value agent-encoded-id="{REALSCOUT_AGENT_ID}"></realscout-home-value>
            </div>
            <p class="section-subtitle" style="margin-top:2rem;">Want a detailed MLS analysis? <a href="#" class="calendly-popup calendly-link-btn-dark">Schedule a consultation</a> with Dr. Jan Duffy, call <a href="tel:7022221964">702-222-1964</a>, or <a href="{REALSCOUT_PORTAL_URL}" target="_blank" rel="noopener noreferrer">search on RealScout</a>.</p>
            {nap_block()}
        </div>
    </section>"""
    write_page("home-valuation.html", "sellers.html", "Free Home Valuation West Summerlin | Dr. Jan Duffy",
               "Get an instant home value estimate for your West Summerlin property. RealScout-powered valuation with follow-up from Dr. Jan Duffy.",
               [{"name": "Home", "item": NAP["url"]}, {"name": "Home Valuation", "item": f"{NAP['url']}/home-valuation.html"}], body)


def generate_neighborhood(page: dict):
    tags = "".join(f'<span class="neighborhood-tag">{h}</span>' for h in page["highlights"])
    place_schema = {
        "@type": "Place",
        "name": page["name"],
        "description": page["summary"],
        "address": {
            "@type": "PostalAddress",
            "addressLocality": "Las Vegas",
            "addressRegion": "NV",
            "addressCountry": "US",
        },
        "containedInPlace": {"@type": "City", "name": "Summerlin"},
    }
    body = f"""    <section class="page-header">
        <div class="container fade-in">
            <p class="section-eyebrow">West Summerlin Neighborhood</p>
            <h1>{page['name']}</h1>
            <p>{page['summary']}</p>
            <div class="cta-actions">
                <a href="properties.html" class="cta-button">View Listings</a>
                <a href="#" class="cta-button cta-button-outline calendly-popup">Schedule Tour</a>
            </div>
        </div>
    </section>

    <section class="content-page">
        <div class="container">
            <div class="neighborhood-hero-card">
                <h2>{page['name']} at a Glance</h2>
                <p>Typical price range: <strong>{page['price_range']}</strong></p>
                <div style="margin-top:1rem;">{tags}</div>
            </div>
            <div class="content-body">
                <h2>Living in {page['name']}</h2>
                <p>{page['summary']} Dr. Jan Duffy provides private driving tours and current MLS listings for this village.</p>
                {nap_block()}
                <div class="related-links">
                    <a href="neighborhoods.html">All Neighborhoods</a>
                    <a href="buyers.html">Buyers Guide</a>
                    <a href="luxury-homes.html">Luxury Homes</a>
                </div>
            </div>
        </div>
    </section>

{listings_section()}"""
    filename = f"{page['slug']}.html"
    write_page(filename, "neighborhoods.html", page["title"], page["description"],
               [{"name": "Home", "item": NAP["url"]}, {"name": "Neighborhoods", "item": f"{NAP['url']}/neighborhoods.html"}, {"name": page["name"], "item": f"{NAP['url']}/{filename}"}],
               body, [place_schema])


def patch_existing_pages():
    calendly_replacements = [
        (r'<p><a href="#" class="calendly-popup">Schedule time with me</a></p>',
         '<p><a href="#" class="calendly-popup calendly-link-btn">Schedule time with me</a></p>'),
        (r'<a href="#" class="calendly-popup">Schedule time with me</a>',
         '<a href="#" class="calendly-popup calendly-link-btn">Schedule time with me</a>'),
    ]
    nav_pattern = re.compile(r'<header>.*?</header>', re.DOTALL)
    footer_pattern = re.compile(r'<footer class="site-footer">.*?</html>', re.DOTALL)

    active_map = {
        "index.html": "index.html",
        "about.html": "about.html",
        "services.html": "services.html",
        "properties.html": "properties.html",
        "neighborhoods.html": "neighborhoods.html",
        "testimonials.html": "testimonials.html",
        "contact.html": "contact.html",
        "buyers.html": "buyers.html",
        "sellers.html": "sellers.html",
        "faq.html": "faq.html",
    }

    for page in sorted(ROOT.glob("*.html")):
        text = page.read_text(encoding="utf-8")
        active = active_map.get(page.name, "")
        if nav_pattern.search(text):
            text = nav_pattern.sub(header_html(active), text, count=1)
        if footer_pattern.search(text):
            text = footer_pattern.sub(footer_html(), text, count=1)
        for old, new in calendly_replacements:
            text = text.replace(old, new)
        page.write_text(text, encoding="utf-8")
        print(f"Patched {page.name}")


def write_sitemap():
    pages = sorted(ROOT.glob("*.html"))
    urls = []
    for page in pages:
        loc = NAP["url"] + ("/" if page.name == "index.html" else f"/{page.name}")
        priority = "1.0" if page.name == "index.html" else "0.8"
        if page.name in ("properties.html", "luxury-homes.html"):
            priority = "0.9"
        if page.name.startswith(("red-rock", "the-ridges", "summerlin-centre", "the-trails", "regency-at", "stonebridge")):
            priority = "0.85"
        urls.append(f"""  <url>
    <loc>{loc}</loc>
    <lastmod>2026-07-08</lastmod>
    <changefreq>weekly</changefreq>
    <priority>{priority}</priority>
  </url>""")
    xml = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + "\n".join(urls) + "\n</urlset>\n"
    (ROOT / "sitemap.xml").write_text(xml, encoding="utf-8")
    print("Updated sitemap.xml")


def main():
    generate_buyers()
    generate_sellers()
    generate_faq()
    generate_market()
    generate_luxury()
    generate_valuation()
    for nbh in NEIGHBORHOOD_PAGES:
        generate_neighborhood(nbh)
    patch_existing_pages()
    write_sitemap()


if __name__ == "__main__":
    main()
