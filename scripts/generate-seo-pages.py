#!/usr/bin/env python3
"""Generate SEO landing pages for westsummerlinhomes.com"""

from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
FOOTER = (ROOT / "seo-footer-snippet.html").read_text()

NAP = {
    "phone": "702-222-1964",
    "phone_tel": "7022221964",
    "email": "janet@westsummerlinhomes.com",
    "street": "12446 Weather Ridge Pl",
    "city": "Las Vegas",
    "state": "NV",
    "zip": "89138",
    "license": "S.0197614.LLC",
}

AGENT_ID = "QWdlbnQtMjI1MDUw"
BASE = "https://www.westsummerlinhomes.com"

NAV = """            <ul class="nav-links">
                <li><a href="index.html">Home</a></li>
                <li><a href="buyers.html"{buy_active}>Buy</a></li>
                <li><a href="sellers.html"{sell_active}>Sell</a></li>
                <li><a href="properties.html"{props_active}>Properties</a></li>
                <li><a href="neighborhoods.html"{hood_active}>Neighborhoods</a></li>
                <li><a href="about.html"{about_active}>About</a></li>
                <li><a href="contact.html"{contact_active}>Contact</a></li>
                <li><a href="#" class="calendly-popup">Schedule</a></li>
            </ul>"""

REALSCOUT_HUB = """
    <section id="search" class="search-section">
        <div class="container">
            <div class="search-container">
                <h3>Search Summerlin Homes</h3>
                <div class="realscout-search-container">
                    <realscout-advanced-search agent-encoded-id="{agent_id}"></realscout-advanced-search>
                </div>
            </div>
        </div>
    </section>

    <section class="realscout-listings">
        <div class="container">
            <h2 class="section-title">{listings_title}</h2>
            <realscout-office-listings agent-encoded-id="{agent_id}" sort-order="STATUS_AND_SIGNIFICANT_CHANGE" listing-status="For Sale" property-types="SFR,MF" price-min="{price_min}" price-max="{price_max}"></realscout-office-listings>
        </div>
    </section>
"""

NAP_BLOCK = """
    <section class="nap-block">
        <div class="container">
            <div class="nap-grid">
                <div>
                    <h3>Call</h3>
                    <p><a href="tel:{phone_tel}">{phone}</a></p>
                </div>
                <div>
                    <h3>Email</h3>
                    <p><a href="mailto:{email}">{email}</a></p>
                </div>
                <div>
                    <h3>Office</h3>
                    <p>{street}<br>{city}, {state} {zip}</p>
                </div>
                <div>
                    <h3>License</h3>
                    <p>Nevada #{license}</p>
                </div>
            </div>
        </div>
    </section>
""".format(**NAP)

CTA = """
    <section class="cta">
        <div class="container">
            <h2>{cta_title}</h2>
            <p>{cta_body}</p>
            <a href="#" class="cta-button calendly-popup">Schedule time with me</a>
        </div>
    </section>
"""

SCHEMA_AGENT = """{{
      "@context": "https://schema.org",
      "@type": "RealEstateAgent",
      "name": "Dr. Janet Duffy",
      "url": "{base}",
      "telephone": "+1-702-222-1964",
      "email": "{email}",
      "address": {{
        "@type": "PostalAddress",
        "streetAddress": "{street}",
        "addressLocality": "{city}",
        "addressRegion": "{state}",
        "postalCode": "{zip}",
        "addressCountry": "US"
      }},
      "areaServed": ["Summerlin West", "Las Vegas", "Nevada"]
    }}""".format(base=BASE, **NAP)


def nav(active: str = "") -> str:
    keys = ["buy", "sell", "props", "hood", "about", "contact"]
    mapping = {
        "buy": "buyers.html",
        "sell": "sellers.html",
        "props": "properties.html",
        "hood": "neighborhoods.html",
        "about": "about.html",
        "contact": "contact.html",
    }
    replacements = {}
    for k in keys:
        replacements[f"{k}_active"] = ' class="active"' if mapping[k] == active else ""
    return NAV.format(**replacements)


def breadcrumb(*crumbs: tuple[str, str]) -> str:
    items = []
    for i, (label, href) in enumerate(crumbs):
        if i == len(crumbs) - 1:
            items.append(f'<li class="breadcrumb-item" aria-current="page">{label}</li>')
        else:
            items.append(f'<li class="breadcrumb-item"><a href="{href}">{label}</a></li>')
    return f"""
    <nav class="breadcrumb-nav" aria-label="Breadcrumb">
        <div class="container">
            <ol class="breadcrumb-list">{''.join(items)}</ol>
        </div>
    </nav>"""


def breadcrumb_schema(crumbs: list[tuple[str, str]]) -> str:
    items = []
    for i, (label, href) in enumerate(crumbs, start=1):
        url = BASE if href == "index.html" else f"{BASE}/{href}"
        items.append(
            f'{{"@type": "ListItem", "position": {i}, "name": "{label}", "item": "{url}"}}'
        )
    return ",\n          ".join(items)


def page(
    *,
    filename: str,
    title: str,
    description: str,
    h1: str,
    subtitle: str,
    active_nav: str,
    breadcrumb_crumbs: list[tuple[str, str]],
    body: str,
    extra_schema: str = "",
    listings_title: str = "Current Listings",
    price_min: str = "400000",
    price_max: str = "3000000",
    cta_title: str = "Ready to Get Started?",
    cta_body: str = "Schedule an in-person consultation with Dr. Janet Duffy.",
) -> str:
    crumbs = [("Home", "index.html")] + breadcrumb_crumbs
    schema_extra_block = f",\n      {extra_schema}" if extra_schema else ""
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <meta name="description" content="{description}">
    <link rel="canonical" href="{BASE}/{filename}">
    <link rel="icon" href="https://cdn.jsdelivr.net/gh/LetMeHelpYouREALTY/westsummerlinhomes.com@main/images/logo.png" type="image/png">
    <script src="https://em.realscout.com/widgets/realscout-web-components.umd.js" type="module"></script>
    <link rel="stylesheet" href="/realscout-hub.css">
    <link rel="stylesheet" href="/seo-page.css">
    <link href="https://assets.calendly.com/assets/external/widget.css" rel="stylesheet">
    <script type="application/ld+json">
    [
      {SCHEMA_AGENT},
      {{
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
          {breadcrumb_schema(crumbs)}
        ]
      }}{schema_extra_block}
    ]
    </script>
</head>
<body>
    <header>
        <nav class="container">
            <a href="index.html" class="logo">
                <img src="https://cdn.jsdelivr.net/gh/LetMeHelpYouREALTY/westsummerlinhomes.com@main/images/logo.png" alt="Dr. Janet Duffy Real Estate" width="42" height="42" loading="eager">
                <span>Dr. Janet Duffy</span>
            </a>
{nav(active_nav)}
        </nav>
    </header>
{breadcrumb(*crumbs)}
    <section class="page-header">
        <div class="container">
            <h1>{h1}</h1>
            <p>{subtitle}</p>
        </div>
    </section>
{REALSCOUT_HUB.format(agent_id=AGENT_ID, listings_title=listings_title, price_min=price_min, price_max=price_max)}
{body}
{NAP_BLOCK}
{CTA.format(cta_title=cta_title, cta_body=cta_body)}
{FOOTER}
    <script src="https://assets.calendly.com/assets/external/widget.js" async></script>
    <script src="/calendly.js"></script>
</body>
</html>
"""


PAGES = [
    page(
        filename="buyers.html",
        title="Buy a Home in Summerlin West | Dr. Janet Duffy Real Estate",
        description="Buy a home in Summerlin West and Las Vegas with Dr. Janet Duffy. MLS search, private showings, and expert negotiation. Call 702-222-1964.",
        h1="Buy a Home in Summerlin West",
        subtitle="Search live MLS inventory, tour homes seven days a week, and close with a licensed Summerlin specialist.",
        active_nav="buyers.html",
        breadcrumb_crumbs=[("Buy a Home", "buyers.html")],
        listings_title="Homes for Sale in Summerlin West",
        cta_title="Start Your Home Search",
        cta_body="Book a buyer consultation to define your budget, neighborhoods, and timeline.",
        body="""
    <section class="content-section">
        <div class="container">
            <h2 class="section-title">Buyer Services in West Summerlin</h2>
            <div class="content-grid">
                <article class="content-card">
                    <h3>MLS Access &amp; Saved Searches</h3>
                    <p>Search every active listing in Summerlin West with RealScout. Dr. Duffy sets up alerts so you see new homes within hours of hitting the market.</p>
                </article>
                <article class="content-card">
                    <h3>Private Showings</h3>
                    <p>Tour homes on your schedule — evenings and weekends included. One call to <a href="tel:7022221964">702-222-1964</a> coordinates access across villages.</p>
                </article>
                <article class="content-card">
                    <h3>Offer Strategy</h3>
                    <p>Comparable sales analysis, inspection negotiation, and contract review backed by 15+ years of Las Vegas transaction experience.</p>
                </article>
            </div>
            <div class="prose" style="margin-top:2rem;">
                <h2>Popular Summerlin West Villages for Buyers</h2>
                <p>Explore village guides for price ranges, amenities, and current inventory:</p>
                <div class="link-grid">
                    <a href="the-ridges.html">The Ridges</a>
                    <a href="red-rock-country-club.html">Red Rock Country Club</a>
                    <a href="summerlin-centre.html">Summerlin Centre</a>
                    <a href="neighborhoods.html">All Neighborhoods</a>
                    <a href="luxury-homes.html">Luxury Homes</a>
                    <a href="relocating-to-summerlin.html">Relocating to Summerlin</a>
                </div>
            </div>
        </div>
    </section>""",
    ),
    page(
        filename="sellers.html",
        title="Sell Your Summerlin Home | Dr. Janet Duffy Real Estate",
        description="Sell your Summerlin West home with Dr. Janet Duffy. Pricing strategy, staging guidance, and full marketing. Free consultation — 702-222-1964.",
        h1="Sell Your Summerlin Home",
        subtitle="Maximize net proceeds with data-driven pricing, professional marketing, and negotiation that protects your timeline.",
        active_nav="sellers.html",
        breadcrumb_crumbs=[("Sell Your Home", "sellers.html")],
        listings_title="Recent Summerlin Listings",
        cta_title="Get Your Home Valuation",
        cta_body="Request a comparative market analysis for your Summerlin West address.",
        body="""
    <section class="content-section">
        <div class="container">
            <h2 class="section-title">Listing Strategy That Sells</h2>
            <div class="content-grid">
                <article class="content-card">
                    <h3>Pricing &amp; CMA</h3>
                    <p>Accurate pricing based on recent comps in your village — not national averages. <a href="home-valuation.html">Request a home valuation</a>.</p>
                </article>
                <article class="content-card">
                    <h3>Marketing Package</h3>
                    <p>Professional photography, MLS syndication, social promotion, and open-house coordination across the Summerlin market.</p>
                </article>
                <article class="content-card">
                    <h3>From Contract to Close</h3>
                    <p>Inspection repairs, appraisal support, and title coordination handled start to finish. License #{license}.</p>
                </article>
            </div>
            <div class="prose" style="margin-top:2rem;">
                <h2>Seller Resources</h2>
                <div class="link-grid">
                    <a href="home-valuation.html">Free Home Valuation</a>
                    <a href="market-update.html">Summerlin Market Update</a>
                    <a href="faq.html">Seller FAQ</a>
                    <a href="testimonials.html">Client Reviews</a>
                </div>
            </div>
        </div>
    </section>""".format(**NAP),
    ),
    page(
        filename="market-update.html",
        title="Summerlin West Real Estate Market Update | Dr. Janet Duffy",
        description="Summerlin West and Las Vegas real estate market insights from Dr. Janet Duffy. Inventory trends, buyer demand, and village-level analysis.",
        h1="Summerlin West Market Update",
        subtitle="Local market context for buyers and sellers — updated regularly by a licensed Summerlin specialist.",
        active_nav="",
        breadcrumb_crumbs=[("Market Update", "market-update.html")],
        cta_title="Get a Custom Market Report",
        cta_body="Request village-specific comps and current inventory for your Summerlin address.",
        body="""
    <section class="content-section">
        <div class="container prose">
            <p>West Summerlin remains one of the most active master-planned markets in the Las Vegas valley. Inventory, days on market, and list-to-sale ratios vary significantly by village — from golf-course estates in <a href="red-rock-country-club.html">Red Rock Country Club</a> to walkable condos near <a href="summerlin-centre.html">Summerlin Centre</a>.</p>
            <h2>What Buyers Should Watch</h2>
            <p>New listings in The Ridges, The Trails, and Reverence move quickly when priced to recent comps. Use the live MLS search above to filter by price, beds, and property type. Dr. Duffy sends same-day alerts when homes match your criteria.</p>
            <h2>What Sellers Should Watch</h2>
            <p>Homes that show well online — professional photos, accurate sq ft, and clear pricing — generate more showings in the first two weeks. Overpriced listings sit while correctly priced homes in the same village receive multiple offers.</p>
            <h2>Get Current Numbers for Your Address</h2>
            <p>Published averages lag the market. For a current comparative market analysis on your home or target neighborhood, call <a href="tel:7022221964">702-222-1964</a> or <a href="home-valuation.html">request a valuation</a>.</p>
            <div class="link-grid">
                <a href="buyers.html">Buyer Guide</a>
                <a href="sellers.html">Seller Guide</a>
                <a href="properties.html">All Listings</a>
                <a href="neighborhoods.html">Neighborhood Comparison</a>
            </div>
        </div>
    </section>""",
    ),
    page(
        filename="faq.html",
        title="Summerlin Real Estate FAQ | Dr. Janet Duffy",
        description="Frequently asked questions about buying and selling in Summerlin West and Las Vegas. HOA, closing costs, inspections, and timelines answered by Dr. Janet Duffy.",
        h1="Summerlin Real Estate FAQ",
        subtitle="Answers to common buyer and seller questions in West Summerlin and the greater Las Vegas market.",
        active_nav="",
        breadcrumb_crumbs=[("FAQ", "faq.html")],
        extra_schema="""{
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
          {"@type": "Question", "name": "How much do I need for a down payment in Summerlin?", "acceptedAnswer": {"@type": "Answer", "text": "Down payment requirements depend on your loan type — conventional, FHA, and VA programs each have different minimums. Dr. Duffy connects buyers with local lenders who specialize in Nevada purchases."}},
          {"@type": "Question", "name": "How long does it take to close on a home in Las Vegas?", "acceptedAnswer": {"@type": "Answer", "text": "A typical purchase closes in 30–45 days after contract acceptance, depending on loan type, HOA document delivery, and inspection timelines."}},
          {"@type": "Question", "name": "What are HOA fees in Summerlin villages?", "acceptedAnswer": {"@type": "Answer", "text": "HOA fees vary by village and sub-association. Fees cover landscaping, amenities, and master-planned community services. Dr. Duffy provides exact figures for each property before you write an offer."}},
          {"@type": "Question", "name": "How do I get a home valuation in Summerlin West?", "acceptedAnswer": {"@type": "Answer", "text": "Request a comparative market analysis through the home valuation page or call 702-222-1964. Valuations use recent closed sales in your specific village."}}
        ]
      }""",
        body="""
    <section class="content-section alt">
        <div class="container">
            <div class="faq-list">
                <article class="faq-item">
                    <h3>How much do I need for a down payment in Summerlin?</h3>
                    <p>Requirements depend on your loan type. Conventional, FHA, and VA programs each have different minimums. Dr. Duffy connects buyers with local lenders who specialize in Nevada purchases.</p>
                </article>
                <article class="faq-item">
                    <h3>How long does it take to close on a home in Las Vegas?</h3>
                    <p>Most purchases close in 30–45 days after contract acceptance, depending on financing, HOA document delivery, and inspection timelines.</p>
                </article>
                <article class="faq-item">
                    <h3>What are HOA fees in Summerlin villages?</h3>
                    <p>HOA fees vary by village and sub-association. Dr. Duffy provides exact figures for each property before you write an offer.</p>
                </article>
                <article class="faq-item">
                    <h3>Should I sell before I buy?</h3>
                    <p>It depends on your equity, financing, and timeline. Dr. Duffy maps contingent and bridge strategies so you are not carrying two mortgages longer than necessary.</p>
                </article>
                <article class="faq-item">
                    <h3>How do I get a home valuation?</h3>
                    <p><a href="home-valuation.html">Request a CMA online</a> or call <a href="tel:7022221964">702-222-1964</a>. Valuations use recent closed sales in your village.</p>
                </article>
                <article class="faq-item">
                    <h3>Do you work with out-of-state buyers?</h3>
                    <p>Yes. Dr. Duffy coordinates virtual tours, video walk-throughs, and remote closings for relocations to Summerlin. See the <a href="relocating-to-summerlin.html">relocating guide</a>.</p>
                </article>
            </div>
        </div>
    </section>""",
    ),
    page(
        filename="home-valuation.html",
        title="Free Summerlin Home Valuation | Dr. Janet Duffy",
        description="Request a free comparative market analysis for your Summerlin West home. Accurate pricing from Dr. Janet Duffy — 702-222-1964.",
        h1="Free Summerlin Home Valuation",
        subtitle="Get a comparative market analysis based on recent sales in your village — not a generic online estimate.",
        active_nav="sellers.html",
        breadcrumb_crumbs=[("Home Valuation", "home-valuation.html")],
        cta_title="Book Your Valuation Consultation",
        cta_body="Schedule an in-person walk-through or desk review with Dr. Janet Duffy.",
        body="""
    <section class="content-section">
        <div class="container">
            <div class="content-grid">
                <article class="content-card">
                    <h3>What You Receive</h3>
                    <ul>
                        <li>Recent closed sales in your village</li>
                        <li>Active competition analysis</li>
                        <li>Suggested list price range</li>
                        <li>Net proceeds estimate</li>
                    </ul>
                </article>
                <article class="content-card">
                    <h3>Why Village-Level Data Matters</h3>
                    <p>A home in The Trails comps differently than one in The Ridges. Dr. Duffy pulls MLS data specific to your sub-association and lot characteristics.</p>
                </article>
                <article class="content-card">
                    <h3>Next Step</h3>
                    <p>Call <a href="tel:7022221964">702-222-1964</a> or schedule a consultation below. Include your address, beds, baths, and any recent upgrades.</p>
                </article>
            </div>
            <div class="calendly-inline-widget" data-url="https://calendly.com/drjanduffy/in-person-real-estate-consultation" style="min-width:320px;height:700px;margin-top:2rem;"></div>
        </div>
    </section>""",
    ),
    page(
        filename="luxury-homes.html",
        title="Luxury Homes in Summerlin West | Dr. Janet Duffy",
        description="Luxury homes for sale in Summerlin West — The Ridges, Red Rock Country Club, and custom estates. Dr. Janet Duffy, Las Vegas luxury specialist. 702-222-1964.",
        h1="Luxury Homes in Summerlin West",
        subtitle="Custom estates, golf-course properties, and mountain-view residences across Summerlin's premier villages.",
        active_nav="properties.html",
        breadcrumb_crumbs=[("Luxury Homes", "luxury-homes.html")],
        listings_title="Luxury Listings",
        price_min="800000",
        price_max="10000000",
        cta_title="Tour Luxury Listings Privately",
        cta_body="Off-market and pre-market inventory available to qualified buyers.",
        body="""
    <section class="content-section">
        <div class="container">
            <div class="content-grid">
                <article class="content-card">
                    <h3>The Ridges</h3>
                    <p>Custom homes on elevated lots with Strip and mountain views. <a href="the-ridges.html">Explore The Ridges</a>.</p>
                </article>
                <article class="content-card">
                    <h3>Red Rock Country Club</h3>
                    <p>Golf-course estates with resort amenities. <a href="red-rock-country-club.html">Explore Red Rock</a>.</p>
                </article>
                <article class="content-card">
                    <h3>Private Showings</h3>
                    <p>Discreet tours for high-net-worth buyers. Direct line: <a href="tel:7022221964">702-222-1964</a>.</p>
                </article>
            </div>
        </div>
    </section>""",
    ),
    page(
        filename="relocating-to-summerlin.html",
        title="Relocating to Summerlin Las Vegas | Dr. Janet Duffy",
        description="Relocating to Summerlin West or Las Vegas? Dr. Janet Duffy helps out-of-state buyers with virtual tours, neighborhood tours, and remote closings.",
        h1="Relocating to Summerlin",
        subtitle="Move to Las Vegas with a local guide — virtual tours, village comparisons, and remote closing support.",
        active_nav="buyers.html",
        breadcrumb_crumbs=[("Relocating to Summerlin", "relocating-to-summerlin.html")],
        body="""
    <section class="content-section">
        <div class="container prose">
            <h2>Your Relocation Timeline</h2>
            <p>Most out-of-state buyers start with a video consultation, narrow villages by commute and budget, then tour in person over a long weekend. Dr. Duffy pre-screens listings so you only walk homes that fit.</p>
            <h2>Compare Villages Before You Fly</h2>
            <div class="link-grid">
                <a href="summerlin-centre.html">Summerlin Centre — urban walkability</a>
                <a href="the-ridges.html">The Ridges — custom luxury</a>
                <a href="red-rock-country-club.html">Red Rock — golf course living</a>
                <a href="neighborhoods.html">Full neighborhood guide</a>
            </div>
            <h2>Remote Closing Support</h2>
            <p>Power of attorney, mobile notary, and digital signing options are available for buyers who cannot attend closing in person.</p>
        </div>
    </section>""",
    ),
    page(
        filename="the-ridges.html",
        title="The Ridges Summerlin Homes for Sale | Dr. Janet Duffy",
        description="Homes for sale in The Ridges, Summerlin West. Luxury custom homes with mountain views. Search MLS listings with Dr. Janet Duffy — 702-222-1964.",
        h1="The Ridges, Summerlin West",
        subtitle="Custom luxury homes on elevated lots with Red Rock Canyon and Strip views.",
        active_nav="neighborhoods.html",
        breadcrumb_crumbs=[("Neighborhoods", "neighborhoods.html"), ("The Ridges", "the-ridges.html")],
        listings_title="Homes for Sale in The Ridges",
        price_min="900000",
        price_max="10000000",
        body="""
    <section class="content-section">
        <div class="container prose">
            <p>The Ridges is one of Summerlin West's most exclusive villages, known for custom architecture, large lots, and panoramic views. Price points typically start above $1.2M for established homes and extend to multi-million-dollar new construction.</p>
            <h2>Amenities &amp; Lifestyle</h2>
            <p>Residents enjoy private streets, proximity to Downtown Summerlin, and quick access to Red Rock Canyon National Conservation Area. Many homes feature pools, outdoor kitchens, and multi-car garages.</p>
            <h2>Buying in The Ridges</h2>
            <p>Inventory is limited and moves quickly when priced to recent comps. Use the MLS search above or call <a href="tel:7022221964">702-222-1964</a> for private showings.</p>
            <div class="link-grid">
                <a href="luxury-homes.html">All Luxury Homes</a>
                <a href="red-rock-country-club.html">Red Rock Country Club</a>
                <a href="buyers.html">Buyer Services</a>
            </div>
        </div>
    </section>""",
    ),
    page(
        filename="red-rock-country-club.html",
        title="Red Rock Country Club Homes for Sale | Dr. Janet Duffy",
        description="Homes for sale at Red Rock Country Club, Summerlin West. Golf-course living with resort amenities. MLS search with Dr. Janet Duffy.",
        h1="Red Rock Country Club",
        subtitle="Golf-course estates and resort-style living at the base of Red Rock Canyon.",
        active_nav="neighborhoods.html",
        breadcrumb_crumbs=[("Neighborhoods", "neighborhoods.html"), ("Red Rock Country Club", "red-rock-country-club.html")],
        listings_title="Red Rock Country Club Listings",
        price_min="700000",
        price_max="5000000",
        body="""
    <section class="content-section">
        <div class="container prose">
            <p>Red Rock Country Club combines championship golf, tennis, dining, and guard-gated security minutes from Summerlin Parkway. Homes range from patio homes near the course to expansive custom estates.</p>
            <h2>Who Buys Here</h2>
            <p>Golf enthusiasts, empty-nesters, and executives who want resort amenities without leaving the valley. Many properties offer mountain and course views.</p>
            <div class="link-grid">
                <a href="the-ridges.html">The Ridges</a>
                <a href="luxury-homes.html">Luxury Homes</a>
                <a href="neighborhoods.html">All Neighborhoods</a>
            </div>
        </div>
    </section>""",
    ),
    page(
        filename="summerlin-centre.html",
        title="Summerlin Centre Homes for Sale | Dr. Janet Duffy",
        description="Homes for sale in Summerlin Centre near Downtown Summerlin. Walk to shopping, dining, and entertainment. MLS listings with Dr. Janet Duffy.",
        h1="Summerlin Centre",
        subtitle="Urban-style living steps from Downtown Summerlin shopping, dining, and entertainment.",
        active_nav="neighborhoods.html",
        breadcrumb_crumbs=[("Neighborhoods", "neighborhoods.html"), ("Summerlin Centre", "summerlin-centre.html")],
        listings_title="Summerlin Centre Listings",
        price_min="350000",
        price_max="1500000",
        body="""
    <section class="content-section">
        <div class="container prose">
            <p>Summerlin Centre offers condos, townhomes, and single-family homes within walking distance of Downtown Summerlin's retail, restaurants, and office space. Popular with professionals and buyers who want a lock-and-leave lifestyle.</p>
            <h2>Commute &amp; Access</h2>
            <p>Quick access to Summerlin Parkway and the 215 beltway. Most daily errands are within a 10-minute walk or short drive.</p>
            <div class="link-grid">
                <a href="buyers.html">First-Time Buyer Guide</a>
                <a href="relocating-to-summerlin.html">Relocating to Summerlin</a>
                <a href="neighborhoods.html">Compare Villages</a>
            </div>
        </div>
    </section>""",
    ),
]

for html in PAGES:
    # Extract filename from canonical
    import re
    m = re.search(r'href="[^"]+/([^"]+)"', html)
    if m:
        fname = m.group(1)
        (ROOT / fname).write_text(html)
        print(f"Wrote {fname}")

print("Done.")
