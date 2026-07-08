#!/usr/bin/env python3
"""Generate SEO/geo pages and sync shared site chrome across all HTML pages."""

import json
import os
import re
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
GSC_VERIFICATION = os.environ.get("GSC_VERIFICATION", "").strip()
SITEMAP_URL = "https://www.westsummerlinhomes.com/sitemap.xml"
TODAY = date.today().isoformat()

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
    "url": "https://www.westsummerlinhomes.com",
}

REALSCOUT_AGENT_ID = "QWdlbnQtMjI1MDUw"
REALSCOUT_PORTAL_URL = "https://drjanduffy.realscout.com/"

NAV_LINKS = [
    ("/", "Home", "/"),
    ("about.html", "About", "about.html"),
    ("buyers.html", "Buy", "buyers.html"),
    ("sellers.html", "Sell", "sellers.html"),
    ("services.html", "Services", "services.html"),
    ("properties.html", "Properties", "properties.html"),
    (REALSCOUT_PORTAL_URL, "MLS Search", "_external"),
    ("neighborhoods.html", "Neighborhoods", "neighborhoods.html"),
    ("faq.html", "FAQ", "faq.html"),
    ("contact.html", "Contact", "contact.html"),
]

FOOTER_EXPLORE = [
    ("/", "Home"),
    ("buyers.html", "Buyers Guide"),
    ("sellers.html", "Sellers Guide"),
    ("services.html", "Services"),
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


def format_phone_e164(phone: str) -> str:
    digits = "".join(ch for ch in phone if ch.isdigit())
    if len(digits) == 10:
        return f"+1-{digits[:3]}-{digits[3:6]}-{digits[6:]}"
    return phone


def postal_address() -> dict:
    return {
        "@type": "PostalAddress",
        "streetAddress": NAP["street"],
        "addressLocality": NAP["city"],
        "addressRegion": NAP["region"],
        "postalCode": NAP["postal"],
        "addressCountry": "US",
    }


def website_entity() -> dict:
    return {
        "@type": "WebSite",
        "@id": f"{NAP['url']}/#website",
        "url": NAP["url"],
        "name": NAP["business"],
        "description": "Premium real estate services in West Summerlin and Las Vegas",
        "publisher": {"@id": f"{NAP['url']}/#organization"},
        "potentialAction": {
            "@type": "SearchAction",
            "target": {
                "@type": "EntryPoint",
                "urlTemplate": REALSCOUT_PORTAL_URL,
            },
            "query-input": "required name=search_term_string",
        },
    }


def organization_entity() -> dict:
    return {
        "@type": "Organization",
        "@id": f"{NAP['url']}/#organization",
        "name": NAP["business"],
        "url": NAP["url"],
        "logo": "https://cdn.jsdelivr.net/gh/LetMeHelpYouREALTY/westsummerlinhomes.com@main/images/logo.png",
        "description": "Premium real estate services in West Summerlin and Las Vegas",
        "address": postal_address(),
        "contactPoint": {
            "@type": "ContactPoint",
            "telephone": format_phone_e164(NAP["phone"]),
            "contactType": "customer service",
            "areaServed": "US-NV",
            "availableLanguage": "English",
        },
    }


def agent_entity() -> dict:
    return {
        "@type": "RealEstateAgent",
        "@id": f"{NAP['url']}/#agent",
        "name": NAP["agent"],
        "url": NAP["url"],
        "telephone": format_phone_e164(NAP["phone"]),
        "email": NAP["email"],
        "image": "https://cdn.westsummerlinhomes.com/images/dr-janet-duffy.jpg",
        "address": postal_address(),
        "areaServed": [
            {"@type": "City", "name": "Las Vegas"},
            {"@type": "City", "name": "Summerlin"},
            "West Summerlin",
        ],
        "memberOf": {"@type": "Organization", "name": NAP["brokerage"]},
        "identifier": NAP["license"],
        "hasOfferCatalog": services_catalog(),
    }


def local_business_entity() -> dict:
    return {
        "@type": ["LocalBusiness", "RealEstateAgent"],
        "@id": f"{NAP['url']}/#localbusiness",
        "name": NAP["business"],
        "url": NAP["url"],
        "telephone": format_phone_e164(NAP["phone"]),
        "email": NAP["email"],
        "address": postal_address(),
        "geo": {"@type": "GeoCoordinates", "latitude": 36.1699, "longitude": -115.3338},
        "openingHoursSpecification": [
            {
                "@type": "OpeningHoursSpecification",
                "dayOfWeek": [
                    "Monday",
                    "Tuesday",
                    "Wednesday",
                    "Thursday",
                    "Friday",
                    "Saturday",
                    "Sunday",
                ],
                "opens": "08:00",
                "closes": "20:00",
            }
        ],
        "priceRange": "$$$",
    }


def services_catalog() -> dict:
    return {
        "@type": "OfferCatalog",
        "name": "Real Estate Services",
        "itemListElement": [
            {
                "@type": "Offer",
                "itemOffered": {
                    "@type": "Service",
                    "name": "Home Buying Services",
                    "description": "Expert guidance through the West Summerlin home buying process",
                    "provider": {"@id": f"{NAP['url']}/#agent"},
                    "areaServed": "West Summerlin, Las Vegas",
                },
            },
            {
                "@type": "Offer",
                "itemOffered": {
                    "@type": "Service",
                    "name": "Home Selling Services",
                    "description": "Professional home selling and marketing in Summerlin",
                    "provider": {"@id": f"{NAP['url']}/#agent"},
                    "areaServed": "West Summerlin, Las Vegas",
                },
            },
            {
                "@type": "Offer",
                "itemOffered": {
                    "@type": "Service",
                    "name": "Investment Property Services",
                    "description": "Real estate investment consultation in Las Vegas",
                    "provider": {"@id": f"{NAP['url']}/#agent"},
                    "areaServed": "Las Vegas",
                },
            },
        ],
    }


def breadcrumb_entity(breadcrumb: list, url: str) -> dict:
    return {
        "@type": "BreadcrumbList",
        "@id": f"{url}#breadcrumb",
        "itemListElement": [
            {
                "@type": "ListItem",
                "position": i + 1,
                "name": item["name"],
                "item": item.get("item", url if i == len(breadcrumb) - 1 else NAP["url"]),
            }
            for i, item in enumerate(breadcrumb)
        ],
    }


def homepage_faq_entity() -> dict:
    faqs = [
        (
            "What areas does Dr. Jan Duffy serve for real estate?",
            "Dr. Jan Duffy specializes in West Summerlin, Summerlin West, and the greater Las Vegas valley, including Red Rock Country Club, The Ridges, Summerlin Centre, and The Trails.",
        ),
        (
            "How do I search MLS listings in West Summerlin?",
            f"Search live MLS inventory on {REALSCOUT_PORTAL_URL} or call {NAP['phone']} for a curated list from Dr. Jan Duffy.",
        ),
        (
            "What services does Dr. Jan Duffy offer?",
            "Home buying, home selling, luxury estates, investment properties, market analysis, and private showings seven days a week.",
        ),
        (
            "How do I schedule a consultation?",
            f"Call {NAP['phone']} or use the Schedule Consultation button to book an in-person meeting with Dr. Jan Duffy.",
        ),
        (
            "Does Dr. Jan Duffy handle luxury properties?",
            "Yes — Dr. Jan Duffy specializes in luxury homes throughout West Summerlin, including guard-gated golf communities and custom estates.",
        ),
    ]
    return {
        "@type": "FAQPage",
        "@id": f"{NAP['url']}/#faq",
        "mainEntity": [
            {
                "@type": "Question",
                "name": q,
                "acceptedAnswer": {"@type": "Answer", "text": a},
            }
            for q, a in faqs
        ],
    }


def testimonials_schema() -> list:
    reviews = [
        (
            "Sarah & Mike Johnson",
            "Dr. Duffy made our home buying experience seamless and stress-free. Her expertise and dedication are unmatched — we closed on our Red Rock home in 21 days.",
        ),
        (
            "Robert Chen",
            "Sold our home in two weeks at asking price. Dr. Duffy's marketing strategy and negotiation skills are exceptional.",
        ),
        (
            "Maria Rodriguez",
            "Professional, knowledgeable, and truly cares about her clients. We couldn't have asked for a better realtor.",
        ),
        (
            "David Park",
            "As an investor, I appreciate agents who understand cap rates and rental demand. Dr. Duffy delivered on both.",
        ),
        (
            "Jennifer & Tom Walsh",
            "First-time buyers with a lot of questions. She explained every step clearly and never rushed us.",
        ),
    ]
    entities = [
        {
            "@type": "AggregateRating",
            "@id": f"{NAP['url']}/testimonials.html#aggregate",
            "ratingValue": "4.9",
            "bestRating": "5",
            "ratingCount": str(len(reviews)),
            "itemReviewed": {"@id": f"{NAP['url']}/#agent"},
        }
    ]
    for author, text in reviews:
        entities.append(
            {
                "@type": "Review",
                "author": {"@type": "Person", "name": author},
                "reviewBody": text,
                "reviewRating": {"@type": "Rating", "ratingValue": "5", "bestRating": "5"},
                "itemReviewed": {"@id": f"{NAP['url']}/#agent"},
            }
        )
    return entities


def neighborhoods_item_list() -> dict:
    return {
        "@type": "ItemList",
        "@id": f"{NAP['url']}/neighborhoods.html#neighborhoods",
        "name": "West Summerlin Neighborhoods",
        "itemListElement": [
            {
                "@type": "ListItem",
                "position": i + 1,
                "name": page["name"],
                "url": f"{NAP['url']}/{page['slug']}.html",
            }
            for i, page in enumerate(NEIGHBORHOOD_PAGES)
        ],
    }


def schema_graph(
    page_type: str,
    title: str,
    description: str,
    url: str,
    breadcrumb: list,
    extra: list | None = None,
) -> str:
    webpage_types = ["WebPage"] if page_type == "WebPage" else [page_type, "WebPage"]
    graph = [
        website_entity(),
        organization_entity(),
        agent_entity(),
        local_business_entity(),
        {
            "@type": webpage_types,
            "@id": f"{url}#webpage",
            "url": url,
            "name": title,
            "description": description,
            "isPartOf": {"@id": f"{NAP['url']}/#website"},
            "about": {"@id": f"{NAP['url']}/#agent"},
            "breadcrumb": {"@id": f"{url}#breadcrumb"},
        },
        breadcrumb_entity(breadcrumb, url),
    ]
    if extra:
        graph.extend(extra)
    payload = {"@context": "https://schema.org", "@graph": graph}
    return json.dumps(payload, indent=2)


def schema_for_homepage() -> str:
    url = f"{NAP['url']}/"
    title = "West Summerlin Homes by Dr. Jan Duffy | Las Vegas & Summerlin Real Estate"
    description = (
        "Expert real estate services in West Summerlin and Las Vegas. "
        "Dr. Jan Duffy provides personalized home buying, selling, and investment guidance."
    )
    breadcrumb = [{"name": "Home", "item": NAP["url"]}]
    return schema_graph("WebPage", title, description, url, breadcrumb, [homepage_faq_entity()])


MANUAL_PAGE_SEO = {
    "about.html": {
        "title": "About Dr. Jan Duffy | West Summerlin Real Estate Agent",
        "description": "Meet Dr. Jan Duffy, licensed West Summerlin real estate agent with BHHS Nevada Properties. Local expertise in Las Vegas and Summerlin.",
        "page_type": "AboutPage",
        "breadcrumb": [
            {"name": "Home", "item": NAP["url"]},
            {"name": "About", "item": f"{NAP['url']}/about.html"},
        ],
        "extra": [
            {
                "@type": "Person",
                "@id": f"{NAP['url']}/about.html#person",
                "name": NAP["agent"],
                "jobTitle": "Real Estate Agent",
                "worksFor": {"@id": f"{NAP['url']}/#organization"},
                "url": f"{NAP['url']}/about.html",
                "image": "https://cdn.westsummerlinhomes.com/images/dr-janet-duffy.jpg",
            }
        ],
    },
    "contact.html": {
        "title": "Contact Dr. Jan Duffy | West Summerlin Real Estate",
        "description": "Contact Dr. Jan Duffy for West Summerlin real estate. Call 702-222-1964 or schedule an in-person consultation seven days a week.",
        "page_type": "ContactPage",
        "breadcrumb": [
            {"name": "Home", "item": NAP["url"]},
            {"name": "Contact", "item": f"{NAP['url']}/contact.html"},
        ],
        "extra": [],
    },
    "services.html": {
        "title": "Real Estate Services | West Summerlin Homes by Dr. Jan Duffy",
        "description": "Home buying, selling, investment, and relocation services in West Summerlin and Las Vegas from Dr. Jan Duffy.",
        "page_type": "WebPage",
        "breadcrumb": [
            {"name": "Home", "item": NAP["url"]},
            {"name": "Services", "item": f"{NAP['url']}/services.html"},
        ],
        "extra": [services_catalog()],
    },
    "properties.html": {
        "title": "Homes for Sale in West Summerlin | MLS Listings | Dr. Jan Duffy",
        "description": "Browse live MLS homes for sale in West Summerlin and Las Vegas. Luxury estates, modern builds, and investment properties with Dr. Jan Duffy.",
        "page_type": "CollectionPage",
        "breadcrumb": [
            {"name": "Home", "item": NAP["url"]},
            {"name": "Properties", "item": f"{NAP['url']}/properties.html"},
        ],
        "extra": [
            {
                "@type": "SearchAction",
                "@id": f"{NAP['url']}/properties.html#search",
                "target": REALSCOUT_PORTAL_URL,
                "query-input": "required name=search_term_string",
            }
        ],
    },
    "neighborhoods.html": {
        "title": "West Summerlin Neighborhoods | Dr. Jan Duffy",
        "description": "Explore West Summerlin neighborhoods including Red Rock Country Club, The Ridges, Summerlin Centre, and more with Dr. Jan Duffy.",
        "page_type": "CollectionPage",
        "breadcrumb": [
            {"name": "Home", "item": NAP["url"]},
            {"name": "Neighborhoods", "item": f"{NAP['url']}/neighborhoods.html"},
        ],
        "extra": [neighborhoods_item_list()],
    },
    "testimonials.html": {
        "title": "Client Testimonials | Dr. Jan Duffy | West Summerlin Real Estate",
        "description": "Read client reviews for Dr. Jan Duffy, West Summerlin real estate agent. 4.9-star service across buying, selling, and investment transactions.",
        "page_type": "WebPage",
        "breadcrumb": [
            {"name": "Home", "item": NAP["url"]},
            {"name": "Testimonials", "item": f"{NAP['url']}/testimonials.html"},
        ],
        "extra": testimonials_schema(),
    },
}

LD_JSON_RE = re.compile(r"\s*<script type=\"application/ld\+json\">.*?</script>", re.DOTALL)
BODY_LD_JSON_RE = re.compile(
    r"\s*<!--[^>]*Structured Data[^>]*-->\s*<script type=\"application/ld\+json\">.*?</script>",
    re.DOTALL,
)


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
            <a href="/" class="logo">
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


def gsc_meta_block() -> str:
    if GSC_VERIFICATION:
        return f'    <meta name="google-site-verification" content="{GSC_VERIFICATION}">'
    return "    <!-- google-site-verification: set GSC_VERIFICATION env var at deploy time -->"


def seo_meta_block(title: str, description: str, canonical: str) -> str:
    return f"""    <meta name="description" content="{description}">
    <meta name="robots" content="index, follow">
    <link rel="canonical" href="{canonical}">
    <link rel="sitemap" type="application/xml" title="Sitemap" href="{SITEMAP_URL}">
    {gsc_meta_block()}
    <meta name="geo.region" content="US-NV">
    <meta name="geo.placename" content="Las Vegas, Summerlin">
    <meta property="og:title" content="{title}">
    <meta property="og:description" content="{description}">
    <meta property="og:url" content="{canonical}">
    <meta property="og:type" content="website">"""


def head_block(title: str, description: str, canonical: str, schema: str) -> str:
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
{seo_meta_block(title, description, canonical)}
    <link rel="icon" href="https://cdn.jsdelivr.net/gh/LetMeHelpYouREALTY/westsummerlinhomes.com@main/images/logo.png" type="image/png">
    <link rel="stylesheet" href="/site.css">
    <script src="https://em.realscout.com/widgets/realscout-web-components.umd.js" type="module"></script>
    <link href="https://assets.calendly.com/assets/external/widget.css" rel="stylesheet">
    <script type="application/ld+json">
{schema}
    </script>
</head>
<body>"""


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
            href = "/" if not path else path

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


def write_page(
    filename: str,
    active: str,
    title: str,
    description: str,
    breadcrumb: list,
    body: str,
    schema_extra: list | None = None,
    page_type: str = "WebPage",
):
    url = f"{NAP['url']}/{filename}" if filename != "index.html" else f"{NAP['url']}/"
    schema = schema_graph(page_type, title, description, url, breadcrumb, schema_extra)
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


def faq_schema_entity(faqs: list[tuple[str, str]], page_id: str) -> dict:
    return {
        "@type": "FAQPage",
        "@id": page_id,
        "mainEntity": [
            {
                "@type": "Question",
                "name": q,
                "acceptedAnswer": {"@type": "Answer", "text": a},
            }
            for q, a in faqs
        ],
    }


def faq_section_html(faqs: list[tuple[str, str]], title: str = "Frequently Asked Questions") -> str:
    items = "\n".join(
        f"""                <article class="faq-item">
                    <h3>{q}</h3>
                    <p>{a}</p>
                </article>"""
        for q, a in faqs
    )
    return f"""    <section class="faq-section content-page">
        <div class="container">
            <h2 class="section-title">{title}</h2>
            <div class="faq-list">
{items}
            </div>
        </div>
    </section>"""


def related_links_section(links: list[tuple[str, str]]) -> str:
    anchors = "\n".join(f'                <a href="{href}">{label}</a>' for href, label in links)
    return f"""    <section class="content-page">
        <div class="container">
            <h2 class="section-title">Related Pages</h2>
            <div class="related-links">
{anchors}
            </div>
        </div>
    </section>"""


def neighborhood_card_html(page: dict) -> str:
    tags = "".join(f'<span class="neighborhood-tag">{tag}</span>' for tag in page["highlights"][:3])
    slug = page["slug"]
    return f"""                <article class="neighborhood-card">
                    <div class="neighborhood-image">{page["name"]}</div>
                    <div class="neighborhood-info">
                        <h2 class="neighborhood-name">{page["name"]}</h2>
                        <p class="neighborhood-description">{page["summary"]}</p>
                        <p class="neighborhood-price">{page["price_range"]}</p>
                        <div>{tags}</div>
                        <p class="neighborhood-actions">
                            <a href="{slug}.html" class="btn-primary">Learn More</a>
                            <a href="properties.html" class="btn-secondary">Listings</a>
                        </p>
                    </div>
                </article>"""


def neighborhoods_grid_section() -> str:
    cards = "\n".join(neighborhood_card_html(page) for page in NEIGHBORHOOD_PAGES)
    return f"""    <section class="neighborhoods">
        <div class="container">
            <p class="section-subtitle">Each West Summerlin village offers distinct architecture, amenities, and price points across the Summerlin master plan.</p>
            <div class="neighborhoods-grid fade-in">
{cards}
            </div>
        </div>
    </section>"""


def map_embed_section() -> str:
    return f"""    <section class="content-page">
        <div class="container">
            <h2 class="section-title">Office Location</h2>
            <p class="section-subtitle">{NAP["business"]} · {NAP["street"]}, {NAP["city"]}, {NAP["region"]} {NAP["postal"]}</p>
            <div class="map-embed">
                <iframe title="Map to {NAP["business"]}" src="https://maps.google.com/maps?q={NAP['street']},+{NAP['city']},+{NAP['region']}+{NAP['postal']}&amp;output=embed" width="100%" height="360" style="border:0;" loading="lazy" referrerpolicy="no-referrer-when-downgrade"></iframe>
            </div>
            <div class="contact-actions" style="margin-top:1rem;">
                <a href="tel:7022221964">Call {NAP["phone"]}</a>
                <a href="https://maps.google.com/?q={NAP['street']},+{NAP['city']},+{NAP['region']}" class="outline" target="_blank" rel="noopener noreferrer">Directions</a>
            </div>
        </div>
    </section>"""


def generate_about():
    faqs = [
        (
            "How long has Dr. Jan Duffy served West Summerlin?",
            "Dr. Jan Duffy has focused on West Summerlin and Summerlin West since 2009, with deep knowledge of village-level pricing, HOA structures, and resale trends.",
        ),
        (
            "What license does Dr. Jan Duffy hold?",
            f"Nevada real estate license #{NAP['license']} with {NAP['brokerage']}.",
        ),
        (
            "Does Dr. Jan Duffy work with luxury buyers and sellers?",
            "Yes. Dr. Duffy represents clients in guard-gated golf communities, custom estates, and $1M+ transactions across Summerlin West.",
        ),
    ]
    body = f"""    <section class="page-header">
        <div class="container fade-in">
            <p class="section-eyebrow">Meet Your Agent</p>
            <h1>About Dr. Jan Duffy</h1>
            <p>Licensed Nevada real estate professional serving West Summerlin buyers, sellers, and investors since 2009.</p>
        </div>
    </section>

    <section class="about">
        <div class="container">
            <div class="about-content">
                <div class="about-image">
                    <img src="https://cdn.westsummerlinhomes.com/images/dr-janet-duffy.jpg" onerror="this.onerror=null;this.src='/images/dr-janet-duffy.jpg';" alt="Dr. Jan Duffy, West Summerlin real estate agent" width="300" height="300" loading="lazy">
                </div>
                <div class="about-text">
                    <h2>West Summerlin Real Estate Expert</h2>
                    <p>Dr. Jan Duffy combines local market data, negotiation discipline, and seven-day-a-week availability for clients across the Summerlin master plan. From first-time buyers in Summerlin Centre to estate sellers in Red Rock Country Club, every transaction gets the same direct access and preparation.</p>
                    <p>Based with {NAP["brokerage"]}, Dr. Duffy provides private neighborhood tours, listing strategy, and MLS search support through RealScout — updated every five minutes with GLVAR inventory.</p>
                    {nap_block()}
                    <div class="credentials">
                        <span class="credential">Licensed Realtor</span>
                        <span class="credential">License #{NAP["license"]}</span>
                        <span class="credential">West Summerlin Specialist</span>
                        <span class="credential">BHHS Nevada Properties</span>
                    </div>
                </div>
            </div>
        </div>
    </section>

    <section class="experience">
        <div class="container">
            <h2 class="section-title">Why Clients Choose Dr. Jan Duffy</h2>
            <div class="experience-grid">
                <div class="experience-card">
                    <div class="experience-icon">🏘️</div>
                    <h3>Village-Level Knowledge</h3>
                    <p>Red Rock, The Ridges, Summerlin Centre, The Trails, Regency, and Stonebridge — pricing, amenities, and resale patterns by community.</p>
                </div>
                <div class="experience-card">
                    <div class="experience-icon">📊</div>
                    <h3>Data-Driven Strategy</h3>
                    <p>MLS-backed valuations, comp analysis, and offer strategy built on current West Summerlin inventory — not national averages.</p>
                </div>
                <div class="experience-card">
                    <div class="experience-icon">🤝</div>
                    <h3>Direct Access</h3>
                    <p>Call {NAP["phone"]} seven days a week. Private showings, contract review, and closing coordination with one point of contact.</p>
                </div>
            </div>
        </div>
    </section>

    <section class="content-page">
        <div class="container content-body">
            <h2>Communities Served in Summerlin West</h2>
            <p>Dr. Jan Duffy tours and transacts across these West Summerlin villages and surrounding Las Vegas markets:</p>
            <ul>
                <li><a href="red-rock-country-club.html">Red Rock Country Club</a> — guard-gated golf estates</li>
                <li><a href="the-ridges-summerlin.html">The Ridges</a> — ultra-luxury custom homes</li>
                <li><a href="summerlin-centre.html">Summerlin Centre</a> — walkable urban village living</li>
                <li><a href="the-trails-summerlin.html">The Trails</a> — established lots and mature landscaping</li>
                <li><a href="regency-at-summerlin.html">Regency at Summerlin</a> — active-adult community</li>
                <li><a href="stonebridge-summerlin.html">Stonebridge</a> — golf-side residences near Angel Park</li>
            </ul>
        </div>
    </section>

{faq_section_html(faqs, "About Dr. Jan Duffy — FAQ")}

{listings_section()}

{related_links_section([
    ("services.html", "Real Estate Services"),
    ("testimonials.html", "Client Reviews"),
    ("buyers.html", "Buyers Guide"),
    ("contact.html", "Contact Dr. Jan Duffy"),
])}"""
    schema_extra = [
        {
            "@type": "Person",
            "@id": f"{NAP['url']}/about.html#person",
            "name": NAP["agent"],
            "jobTitle": "Real Estate Agent",
            "worksFor": {"@id": f"{NAP['url']}/#organization"},
            "url": f"{NAP['url']}/about.html",
            "image": "https://cdn.westsummerlinhomes.com/images/dr-janet-duffy.jpg",
        },
        faq_schema_entity(faqs, f"{NAP['url']}/about.html#faq"),
    ]
    write_page(
        "about.html",
        "about.html",
        "About Dr. Jan Duffy | West Summerlin Real Estate Agent",
        "Meet Dr. Jan Duffy — licensed West Summerlin real estate agent with BHHS Nevada Properties. Village-level expertise in Red Rock, The Ridges, and Summerlin West since 2009.",
        [{"name": "Home", "item": NAP["url"]}, {"name": "About", "item": f"{NAP['url']}/about.html"}],
        body,
        schema_extra,
        "AboutPage",
    )


def generate_services():
    faqs = [
        (
            "What real estate services does Dr. Jan Duffy offer?",
            "Home buying, home selling, luxury listings, investment property analysis, relocation support, and free home valuations across West Summerlin.",
        ),
        (
            "Do you provide market analysis before listing?",
            "Yes. Every listing and purchase strategy starts with current MLS comps and village-specific demand data.",
        ),
        (
            "Can I schedule a consultation before committing?",
            f"Absolutely. Call {NAP['phone']} or book an in-person consultation online — no obligation.",
        ),
    ]
    body = f"""    <section class="page-header">
        <div class="container fade-in">
            <p class="section-eyebrow">Full-Service Real Estate</p>
            <h1>Real Estate Services in West Summerlin</h1>
            <p>Buying, selling, investing, and relocation — tailored to Summerlin West and the greater Las Vegas valley.</p>
        </div>
    </section>

    <section class="services">
        <div class="container">
            <p class="section-subtitle">Every service includes direct access to Dr. Jan Duffy, live MLS search on RealScout, and seven-day-a-week showing availability.</p>
            <div class="services-grid">
                <div class="service-card">
                    <div class="service-icon">🏠</div>
                    <h2>Home Buying</h2>
                    <p>From pre-approval through closing — neighborhood tours, offer strategy, and inspection negotiation across West Summerlin.</p>
                    <ul class="service-features">
                        <li>MLS search and saved listing alerts</li>
                        <li>Private showings seven days a week</li>
                        <li>Offer and counter-offer strategy</li>
                    </ul>
                    <a href="buyers.html" class="service-cta">Buyers Guide</a>
                </div>
                <div class="service-card">
                    <div class="service-icon">💰</div>
                    <h2>Home Selling</h2>
                    <p>Pricing, staging guidance, professional marketing, and multiple-offer management for West Summerlin sellers.</p>
                    <ul class="service-features">
                        <li>Comparative market analysis</li>
                        <li>Listing prep and launch strategy</li>
                        <li>Contract-to-close coordination</li>
                    </ul>
                    <a href="sellers.html" class="service-cta">Sellers Guide</a>
                </div>
                <div class="service-card">
                    <div class="service-icon">📊</div>
                    <h2>Home Valuation</h2>
                    <p>Instant RealScout estimates plus in-person pricing review for accurate West Summerlin list prices.</p>
                    <ul class="service-features">
                        <li>MLS-backed valuation widget</li>
                        <li>Village-level comp review</li>
                        <li>Seller net sheet guidance</li>
                    </ul>
                    <a href="home-valuation.html" class="service-cta">Get Valuation</a>
                </div>
                <div class="service-card">
                    <div class="service-icon">🏢</div>
                    <h2>Luxury &amp; Investment</h2>
                    <p>Estate transactions, guard-gated communities, and rental-demand analysis for investors relocating to Las Vegas.</p>
                    <ul class="service-features">
                        <li>$1M+ estate marketing</li>
                        <li>Cap rate and ROI review</li>
                        <li>Portfolio acquisition support</li>
                    </ul>
                    <a href="luxury-homes.html" class="service-cta">Luxury Homes</a>
                </div>
            </div>
        </div>
    </section>

    <section class="content-page">
        <div class="container content-body">
            <h2>How Dr. Jan Duffy Works With Clients</h2>
            <p>Unlike large teams where leads get passed around, you work directly with Dr. Duffy from first call to closing. Listings go live on the GLVAR MLS and Dr. Jan Duffy's <a href="{REALSCOUT_PORTAL_URL}" target="_blank" rel="noopener noreferrer">RealScout portal</a> simultaneously. Buyers receive curated searches by village, price, and property type — not generic auto-blasts.</p>
            <p>Ready to start? <a href="contact.html">Contact Dr. Jan Duffy</a> or read <a href="testimonials.html">client reviews</a> from recent West Summerlin transactions.</p>
        </div>
    </section>

{faq_section_html(faqs, "Services FAQ")}

{realscout_advanced_search_section("Search West Summerlin MLS", "Live inventory across every Summerlin West village.")}

{related_links_section([
    ("about.html", "About Dr. Jan Duffy"),
    ("properties.html", "MLS Listings"),
    ("market-update.html", "Market Update"),
    ("faq.html", "FAQ"),
])}"""
    schema_extra = [services_catalog(), faq_schema_entity(faqs, f"{NAP['url']}/services.html#faq")]
    write_page(
        "services.html",
        "services.html",
        "Real Estate Services | West Summerlin Homes by Dr. Jan Duffy",
        "Home buying, selling, luxury estates, valuations, and investment services in West Summerlin. Direct access to Dr. Jan Duffy — call 702-222-1964.",
        [{"name": "Home", "item": NAP["url"]}, {"name": "Services", "item": f"{NAP['url']}/services.html"}],
        body,
        schema_extra,
    )


def generate_contact():
    faqs = [
        (
            "What is the best way to reach Dr. Jan Duffy?",
            f"Call {NAP['phone']} for the fastest response, or schedule an in-person consultation through the Calendly link on this page.",
        ),
        (
            "What are Dr. Jan Duffy's office hours?",
            "Available seven days a week, 8:00 AM – 8:00 PM. Evening and weekend showings are available by appointment.",
        ),
        (
            "Where is the office located?",
            f"{NAP['brokerage']}, {NAP['street']}, {NAP['city']}, {NAP['region']} {NAP['postal']}.",
        ),
    ]
    body = f"""    <section class="page-header">
        <div class="container fade-in">
            <p class="section-eyebrow">Let's Connect</p>
            <h1>Contact Dr. Jan Duffy</h1>
            <p>West Summerlin real estate questions? Call {NAP['phone']} or book an in-person consultation.</p>
            <div class="cta-actions">
                <a href="{NAP['phone_tel']}" class="cta-button">Call {NAP['phone']}</a>
                <a href="#" class="cta-button cta-button-outline calendly-popup">Schedule Consultation</a>
            </div>
        </div>
    </section>

    <section class="contact">
        <div class="container">
            <h2 class="section-title">Contact Information</h2>
            <div class="contact-content">
                <div class="contact-info">
                    <h3>{NAP['business']}</h3>
                    {nap_block()}
                    <div class="contact-item">
                        <span>📞</span>
                        <span><a href="{NAP['phone_tel']}">{NAP['phone']}</a></span>
                    </div>
                    <div class="contact-item">
                        <span>✉️</span>
                        <span><a href="mailto:{NAP['email']}">{NAP['email']}</a></span>
                    </div>
                    <div class="contact-item">
                        <span>🕒</span>
                        <span>Available 7 days a week · 8:00 AM – 8:00 PM</span>
                    </div>
                    <div class="contact-actions">
                        <a href="{NAP['phone_tel']}">Call Now</a>
                        <a href="https://maps.google.com/?q={NAP['street']},+{NAP['city']},+{NAP['region']}" class="outline" target="_blank" rel="noopener noreferrer">Directions</a>
                    </div>
                </div>
                <div class="contact-form calendly-embed">
                    <h3>Schedule a Consultation</h3>
                    <p><a href="#" class="calendly-popup calendly-link-btn">Schedule time with me</a></p>
                    <div class="calendly-inline-widget" data-url="https://calendly.com/drjanduffy/in-person-real-estate-consultation" style="min-width:320px;height:700px;"></div>
                </div>
            </div>
        </div>
    </section>

{map_embed_section()}

    <section class="office-hours">
        <div class="container">
            <h2 class="section-title">Office Hours &amp; Response Times</h2>
            <div class="hours-grid">
                <div class="hours-card">
                    <h3>Regular Hours</h3>
                    <ul class="hours-list">
                        <li><span>Monday – Friday</span> <span>8:00 AM – 8:00 PM</span></li>
                        <li><span>Saturday – Sunday</span> <span>8:00 AM – 8:00 PM</span></li>
                    </ul>
                </div>
                <div class="hours-card">
                    <h3>Showings</h3>
                    <ul class="hours-list">
                        <li><span>Private Tours</span> <span>7 days a week</span></li>
                        <li><span>Evening Appointments</span> <span>Available</span></li>
                    </ul>
                </div>
                <div class="hours-card">
                    <h3>Response Time</h3>
                    <ul class="hours-list">
                        <li><span>Phone</span> <span>Within 1 hour</span></li>
                        <li><span>Email</span> <span>Within 4 hours</span></li>
                    </ul>
                </div>
            </div>
        </div>
    </section>

{faq_section_html(faqs, "Contact FAQ")}

{listings_section()}

{related_links_section([
    ("about.html", "About Dr. Jan Duffy"),
    ("services.html", "Services"),
    ("buyers.html", "Buyers Guide"),
    ("neighborhoods.html", "Neighborhoods"),
])}"""
    schema_extra = [faq_schema_entity(faqs, f"{NAP['url']}/contact.html#faq")]
    write_page(
        "contact.html",
        "contact.html",
        "Contact Dr. Jan Duffy | West Summerlin Real Estate",
        f"Contact Dr. Jan Duffy for West Summerlin real estate. Call {NAP['phone']} or schedule an in-person consultation at {NAP['brokerage']}, Summerlin.",
        [{"name": "Home", "item": NAP["url"]}, {"name": "Contact", "item": f"{NAP['url']}/contact.html"}],
        body,
        schema_extra,
        "ContactPage",
    )


def generate_testimonials():
    faqs = [
        (
            "What do clients say about Dr. Jan Duffy?",
            "Buyers, sellers, and investors cite responsive communication, local market knowledge, and strong negotiation results across West Summerlin.",
        ),
        (
            "How do I leave a review after closing?",
            f"After your transaction, you will receive a link to share feedback on Google. You can also call {NAP['phone']} with a testimonial.",
        ),
    ]
    body = f"""    <section class="page-header">
        <div class="container fade-in">
            <p class="section-eyebrow">Client Success</p>
            <h1>Client Testimonials</h1>
            <p>4.9★ average rating from buyers, sellers, and investors across West Summerlin and Las Vegas.</p>
        </div>
    </section>

    <section class="content-page">
        <div class="container content-body">
            <p>These reviews come from recent transactions in Red Rock Country Club, The Trails, Summerlin Centre, and investment purchases across the Las Vegas valley. Every client works directly with Dr. Jan Duffy — not an assistant team.</p>
            <p>Considering a move to West Summerlin? Read <a href="about.html">about Dr. Jan Duffy</a> or explore <a href="services.html">available services</a>.</p>
        </div>
    </section>

    <section class="testimonials">
        <div class="container">
            <div class="testimonials-grid fade-in">
                <article class="testimonial testimonial-featured">
                    <div class="testimonial-stars">★★★★★</div>
                    <p class="testimonial-text">"Dr. Duffy made our home buying experience seamless and stress-free. Her expertise and dedication are unmatched — we closed on our Red Rock home in 21 days."</p>
                    <p class="testimonial-author">— Sarah &amp; Mike Johnson, Red Rock Country Club</p>
                </article>
                <article class="testimonial">
                    <div class="testimonial-stars">★★★★★</div>
                    <p class="testimonial-text">"Sold our home in two weeks at asking price. Dr. Duffy's marketing strategy and negotiation skills are exceptional."</p>
                    <p class="testimonial-author">— Robert Chen, The Trails</p>
                </article>
                <article class="testimonial">
                    <div class="testimonial-stars">★★★★★</div>
                    <p class="testimonial-text">"Professional, knowledgeable, and truly cares about her clients. We couldn't have asked for a better realtor."</p>
                    <p class="testimonial-author">— Maria Rodriguez, Summerlin Centre</p>
                </article>
                <article class="testimonial">
                    <div class="testimonial-stars">★★★★★</div>
                    <p class="testimonial-text">"As an investor, I appreciate agents who understand cap rates and rental demand. Dr. Duffy delivered on both."</p>
                    <p class="testimonial-author">— David Park, Investment Buyer</p>
                </article>
                <article class="testimonial">
                    <div class="testimonial-stars">★★★★★</div>
                    <p class="testimonial-text">"First-time buyers with a lot of questions. She explained every step clearly and never rushed us."</p>
                    <p class="testimonial-author">— Jennifer &amp; Tom Walsh</p>
                </article>
                <article class="testimonial">
                    <div class="testimonial-stars">★★★★★</div>
                    <p class="testimonial-text">"Relocated from Chicago — Dr. Duffy knew every Summerlin village and matched us to the right community in one weekend."</p>
                    <p class="testimonial-author">— The Morrison Family</p>
                </article>
            </div>
            <div class="cta-actions fade-in">
                <a href="#" class="cta-button calendly-popup">Schedule Your Consultation</a>
                <a href="{NAP['phone_tel']}" class="cta-button cta-button-outline">Call {NAP['phone']}</a>
            </div>
        </div>
    </section>

{faq_section_html(faqs, "Reviews FAQ")}

{related_links_section([
    ("about.html", "About Dr. Jan Duffy"),
    ("services.html", "Services"),
    ("neighborhoods.html", "Neighborhoods"),
    ("contact.html", "Contact"),
])}"""
    schema_extra = testimonials_schema() + [faq_schema_entity(faqs, f"{NAP['url']}/testimonials.html#faq")]
    write_page(
        "testimonials.html",
        "testimonials.html",
        "Client Testimonials | Dr. Jan Duffy | West Summerlin Real Estate",
        "Read client reviews for Dr. Jan Duffy, West Summerlin real estate agent. 4.9-star service for buying, selling, and investment transactions in Summerlin.",
        [{"name": "Home", "item": NAP["url"]}, {"name": "Testimonials", "item": f"{NAP['url']}/testimonials.html"}],
        body,
        schema_extra,
    )


def generate_neighborhoods_hub():
    faqs = [
        (
            "What are the best neighborhoods in West Summerlin?",
            "Top villages include Red Rock Country Club for golf estates, The Ridges for ultra-luxury homes, Summerlin Centre for walkable amenities, and The Trails for established lots.",
        ),
        (
            "How do I choose the right Summerlin village?",
            "Dr. Jan Duffy provides private driving tours comparing price point, HOA, commute, and amenities before you write an offer.",
        ),
        (
            "Can I search MLS listings by neighborhood?",
            f"Yes — use the RealScout MLS portal or call {NAP['phone']} for a curated list by village.",
        ),
    ]
    body = f"""    <section class="page-header">
        <div class="container fade-in">
            <p class="section-eyebrow">Las Vegas · Summerlin West</p>
            <h1>West Summerlin Neighborhoods</h1>
            <p>From championship golf communities to walkable urban villages — compare every major Summerlin West neighborhood.</p>
            <div class="cta-actions">
                <a href="#" class="cta-button calendly-popup">Schedule Neighborhood Tour</a>
                <a href="properties.html" class="cta-button cta-button-outline">View MLS Listings</a>
            </div>
        </div>
    </section>

    <section class="content-page">
        <div class="container content-body">
            <h2>Find Your West Summerlin Community</h2>
            <p>The Summerlin master plan spans dozens of villages. Dr. Jan Duffy specializes in Summerlin West — including guard-gated golf communities, luxury custom enclaves, and newer urban villages near Downtown Summerlin.</p>
            <p>Select a neighborhood below for village-specific pricing, amenities, and current MLS inventory. Not sure where to start? <a href="contact.html">Book a consultation</a> for a private driving tour.</p>
        </div>
    </section>

{neighborhoods_grid_section()}

{faq_section_html(faqs, "Neighborhood FAQ")}

{realscout_advanced_search_section("Search by Neighborhood", "Filter MLS listings by price, beds, and area across West Summerlin.")}

{related_links_section([
    ("buyers.html", "Buyers Guide"),
    ("luxury-homes.html", "Luxury Homes"),
    ("market-update.html", "Market Update"),
    ("about.html", "About Dr. Jan Duffy"),
])}"""
    schema_extra = [neighborhoods_item_list(), faq_schema_entity(faqs, f"{NAP['url']}/neighborhoods.html#faq")]
    write_page(
        "neighborhoods.html",
        "neighborhoods.html",
        "West Summerlin Neighborhoods | Dr. Jan Duffy",
        "Compare West Summerlin neighborhoods — Red Rock Country Club, The Ridges, Summerlin Centre, The Trails, Regency, and Stonebridge. Tours and MLS listings with Dr. Jan Duffy.",
        [{"name": "Home", "item": NAP["url"]}, {"name": "Neighborhoods", "item": f"{NAP['url']}/neighborhoods.html"}],
        body,
        schema_extra,
        "CollectionPage",
    )


def patch_index_internal_links():
    path = ROOT / "index.html"
    if not path.exists():
        return
    html = path.read_text(encoding="utf-8")
    patches = [
        (
            '                    </div>\n                </div>\n            </div>\n        </div>\n    </section>\n\n    <section id="services" class="services">',
            '                    </div>\n                    <p class="section-cta fade-in"><a href="about.html" class="btn-primary">Read full bio &amp; credentials</a></p>\n                </div>\n            </div>\n        </div>\n    </section>\n\n    <section id="services" class="services">',
        ),
        (
            '            </div>\n        </div>\n    </section>\n\n    <!-- Enhanced Author Credentials Section',
            '            </div>\n            <p class="section-cta fade-in"><a href="services.html" class="btn-primary">View all real estate services</a></p>\n        </div>\n    </section>\n\n    <!-- Enhanced Author Credentials Section',
        ),
        (
            '            </div>\n        </div>\n    </section>\n\n    <section id="testimonials" class="testimonials">',
            '            </div>\n            <p class="section-cta fade-in"><a href="neighborhoods.html" class="btn-primary">Explore all West Summerlin neighborhoods</a></p>\n        </div>\n    </section>\n\n    <section id="testimonials" class="testimonials">',
        ),
        (
            '            </div>\n        </div>\n    </section>\n\n    <section id="contact" class="contact">',
            '            </div>\n            <p class="section-cta fade-in"><a href="testimonials.html" class="btn-primary">Read all client reviews</a></p>\n        </div>\n    </section>\n\n    <section id="contact" class="contact">',
        ),
        (
            '            <h2 class="section-title fade-in">Get In Touch</h2>\n            <div class="contact-content fade-in">',
            '            <h2 class="section-title fade-in">Get In Touch</h2>\n            <p class="section-subtitle fade-in"><a href="contact.html">Visit the full contact page</a> for office hours, map, and scheduling.</p>\n            <div class="contact-content fade-in">',
        ),
    ]
    for old, new in patches:
        if old in html and new not in html:
            html = html.replace(old, new, 1)
    path.write_text(html, encoding="utf-8")
    print("Patched index.html internal links")


def extract_title_description(html: str) -> tuple[str, str]:
    title_match = re.search(r"<title>(.*?)</title>", html, re.DOTALL)
    desc_match = re.search(
        r'<meta name="description" content="([^"]*)"',
        html,
    )
    title = title_match.group(1).strip() if title_match else NAP["business"]
    description = desc_match.group(1).strip() if desc_match else NAP["business"]
    return title, description


def ensure_seo_head_tags(html: str, title: str, description: str, canonical: str) -> str:
    head_match = re.search(r"<head>(.*?)</head>", html, re.DOTALL)
    if not head_match:
        return html
    head = head_match.group(1)

    if 'name="description"' not in head:
        head = head.replace(
            "</title>",
            f"</title>\n    <meta name=\"description\" content=\"{description}\">",
            1,
        )
    if 'name="robots"' not in head:
        head = head.replace(
            '<meta name="description"',
            '    <meta name="robots" content="index, follow">\n    <meta name="description"',
            1,
        )
    if 'rel="canonical"' not in head:
        head = head.replace(
            '<meta name="robots"',
            f'    <link rel="canonical" href="{canonical}">\n    <meta name="robots"',
            1,
        )
    if 'rel="sitemap"' not in head:
        head = head.replace(
            '<link rel="canonical"',
            f'    <link rel="sitemap" type="application/xml" title="Sitemap" href="{SITEMAP_URL}">\n    <link rel="canonical"',
            1,
        )
    if "google-site-verification" not in head and "google-site-verification:" not in head:
        head = head.replace(
            '<link rel="sitemap"',
            f"{gsc_meta_block()}\n    <link rel=\"sitemap\"",
            1,
        )
    if 'property="og:title"' not in head:
        og_block = f"""
    <meta name="geo.region" content="US-NV">
    <meta name="geo.placename" content="Las Vegas, Summerlin">
    <meta property="og:title" content="{title}">
    <meta property="og:description" content="{description}">
    <meta property="og:url" content="{canonical}">
    <meta property="og:type" content="website">"""
        head = head.replace(
            '<link rel="icon"',
            f"{og_block}\n    <link rel=\"icon\"",
            1,
        )

    head = re.sub(
        r'<link rel="canonical" href="[^"]*"',
        f'<link rel="canonical" href="{canonical}"',
        head,
        count=1,
    )
    head = re.sub(
        r'<meta property="og:url" content="[^"]*"',
        f'<meta property="og:url" content="{canonical}"',
        head,
        count=1,
    )
    head = re.sub(
        r'<meta property="twitter:url" content="[^"]*"',
        f'<meta property="twitter:url" content="{canonical}"',
        head,
        count=1,
    )
    head = re.sub(
        r'<link rel="sitemap"[^>]*href="[^"]*"',
        f'<link rel="sitemap" type="application/xml" title="Sitemap" href="{SITEMAP_URL}"',
        head,
        count=1,
    )

    html = html[: head_match.start(1)] + head + html[head_match.end(1) :]
    return html


def normalize_site_urls(html: str) -> str:
    """Ensure apex domain URLs use www to match the live primary host."""
    return re.sub(
        r"https://westsummerlinhomes\.com",
        "https://www.westsummerlinhomes.com",
        html,
    )


def inject_schema_script(html: str, schema_json: str) -> str:
    script = f"\n    <script type=\"application/ld+json\">\n{schema_json}\n    </script>"
    html = LD_JSON_RE.sub("", html)
    html = BODY_LD_JSON_RE.sub("", html)
    # Remove remaining body ld+json blocks (index.html legacy)
    body_match = re.search(r"<body>(.*)</body>", html, re.DOTALL)
    if body_match:
        body = body_match.group(1)
        cleaned_body = LD_JSON_RE.sub("", body)
        if cleaned_body != body:
            html = html.replace(body, cleaned_body, 1)
    return html.replace("</head>", f"{script}\n</head>", 1)


def canonical_for(filename: str) -> str:
    if filename == "index.html":
        return f"{NAP['url']}/"
    return f"{NAP['url']}/{filename}"


def inject_manual_pages_schema():
    inject_only = {"properties.html"}
    for filename, meta in MANUAL_PAGE_SEO.items():
        if filename not in inject_only:
            continue
        path = ROOT / filename
        if not path.exists():
            continue
        url = canonical_for(filename)
        schema = schema_graph(
            meta["page_type"],
            meta["title"],
            meta["description"],
            url,
            meta["breadcrumb"],
            meta.get("extra"),
        )
        html = path.read_text(encoding="utf-8")
        html = html.replace("Dr. Janet Duffy", "Dr. Jan Duffy")
        html = ensure_seo_head_tags(html, meta["title"], meta["description"], url)
        if re.search(r"<title>.*?</title>", html):
            html = re.sub(r"<title>.*?</title>", f"<title>{meta['title']}</title>", html, count=1)
        html = inject_schema_script(html, schema)
        html = normalize_site_urls(html)
        path.write_text(html, encoding="utf-8")
        print(f"Injected schema for {filename}")


def inject_index_schema():
    path = ROOT / "index.html"
    if not path.exists():
        return
    title = "West Summerlin Homes by Dr. Jan Duffy | Las Vegas & Summerlin Real Estate"
    description = (
        "Expert real estate services in West Summerlin and Las Vegas. "
        "Dr. Jan Duffy provides personalized home buying, selling, and investment guidance."
    )
    canonical = f"{NAP['url']}/"
    schema = schema_for_homepage()
    html = path.read_text(encoding="utf-8")
    html = html.replace("Dr. Janet Duffy", "Dr. Jan Duffy")
    html = ensure_seo_head_tags(html, title, description, canonical)
    html = inject_schema_script(html, schema)
    html = re.sub(
        r"\s*<!-- Structured Data[^>]*-->\s*",
        "\n",
        html,
    )
    html = re.sub(
        r"\s*<!-- FAQ Schema[^>]*-->\s*",
        "\n",
        html,
    )
    html = re.sub(
        r"\s*<!-- Breadcrumb Schema[^>]*-->\s*",
        "\n",
        html,
    )
    html = normalize_site_urls(html)
    path.write_text(html, encoding="utf-8")
    print("Injected unified schema for index.html")


def inject_gsc_sitemap_all_pages():
    for path in sorted(ROOT.glob("*.html")):
        html = path.read_text(encoding="utf-8")
        title, description = extract_title_description(html)
        canonical = canonical_for(path.name)
        updated = ensure_seo_head_tags(html, title, description, canonical)
        updated = normalize_site_urls(updated)
        if updated != html:
            path.write_text(updated, encoding="utf-8")
            print(f"Updated SEO head tags for {path.name}")


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
        "index.html": "/",
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
        if page.name in (
            "about.html",
            "contact.html",
            "services.html",
            "testimonials.html",
            "neighborhoods.html",
            "properties.html",
            "luxury-homes.html",
        ):
            priority = "0.95"
        if page.name.startswith(("red-rock", "the-ridges", "summerlin-centre", "the-trails", "regency-at", "stonebridge")):
            priority = "0.85"
        urls.append(f"""  <url>
    <loc>{loc}</loc>
    <lastmod>{TODAY}</lastmod>
    <changefreq>weekly</changefreq>
    <priority>{priority}</priority>
  </url>""")
    xml = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + "\n".join(urls) + "\n</urlset>\n"
    (ROOT / "sitemap.xml").write_text(xml, encoding="utf-8")
    print("Updated sitemap.xml")


def main():
    generate_about()
    generate_services()
    generate_contact()
    generate_testimonials()
    generate_neighborhoods_hub()
    generate_buyers()
    generate_sellers()
    generate_faq()
    generate_market()
    generate_luxury()
    generate_valuation()
    for nbh in NEIGHBORHOOD_PAGES:
        generate_neighborhood(nbh)
    patch_existing_pages()
    patch_index_internal_links()
    inject_gsc_sitemap_all_pages()
    inject_manual_pages_schema()
    inject_index_schema()
    write_sitemap()


if __name__ == "__main__":
    main()
