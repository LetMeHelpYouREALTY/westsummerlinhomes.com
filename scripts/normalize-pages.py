#!/usr/bin/env python3
"""Normalize HTML heads, footers, and duplicate scripts across site pages."""

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

FOOTER = """
    <footer class="site-footer">
        <div class="container footer-grid">
            <div class="footer-brand">
                <strong>West Summerlin Homes</strong>
                <span>by Dr. Jan Duffy</span>
                <p>Luxury real estate in West Summerlin and the greater Las Vegas valley.</p>
            </div>
            <div class="footer-nav">
                <h4>Explore</h4>
                <ul>
                    <li><a href="index.html">Home</a></li>
                    <li><a href="buyers.html">Buyers Guide</a></li>
                    <li><a href="sellers.html">Sellers Guide</a></li>
                    <li><a href="properties.html">Properties</a></li>
                    <li><a href="https://drjanduffy.realscout.com/" target="_blank" rel="noopener noreferrer">MLS Search Portal</a></li>
                    <li><a href="neighborhoods.html">Neighborhoods</a></li>
                    <li><a href="luxury-homes.html">Luxury Homes</a></li>
                    <li><a href="market-update.html">Market Update</a></li>
                    <li><a href="home-valuation.html">Home Valuation</a></li>
                    <li><a href="faq.html">FAQ</a></li>
                    <li><a href="testimonials.html">Testimonials</a></li>
                    <li><a href="about.html">About</a></li>
                    <li><a href="contact.html">Contact</a></li>
                </ul>
            </div>
            <div class="footer-contact">
                <h4>Contact</h4>
                <p>Dr. Jan Duffy<br>BHHS Nevada Properties</p>
                <p><a href="tel:7022221964">702-222-1964</a></p>
                <p>License #S.0197614.LLC</p>
            </div>
        </div>
        <div class="footer-bottom container">
            <p>&copy; 2026 West Summerlin Homes by Dr. Jan Duffy. All rights reserved. <a href="#" class="calendly-popup calendly-link-btn">Schedule time with me</a></p>
        </div>
    </footer>

    <div class="sticky-call-bar">
        <a href="tel:7022221964">Call 702-222-1964</a>
        <a href="#" class="calendly-popup">Schedule</a>
    </div>

    <script src="https://assets.calendly.com/assets/external/widget.js" async></script>
    <script src="/site.js"></script>
    <script src="/calendly.js"></script>
</body>
</html>
"""

HEAD_TEMPLATE = """    <link rel="icon" href="https://cdn.jsdelivr.net/gh/LetMeHelpYouREALTY/westsummerlinhomes.com@main/images/logo.png" type="image/png">
    <link rel="stylesheet" href="/site.css">
    <script src="https://em.realscout.com/widgets/realscout-web-components.umd.js" type="module"></script>
    <link href="https://assets.calendly.com/assets/external/widget.css" rel="stylesheet">
</head>"""


def clean_head(content: str) -> str:
    content = re.sub(
        r'<link rel="icon"[^>]*>.*?<link href="https://assets\.calendly\.com/assets/external/widget\.css" rel="stylesheet">\s*</head>',
        HEAD_TEMPLATE,
        content,
        flags=re.DOTALL,
    )
    content = re.sub(
        r'(<script src="https://em\.realscout\.com/widgets/realscout-web-components\.umd\.js" type="module"></script>\s*)+',
        '<script src="https://em.realscout.com/widgets/realscout-web-components.umd.js" type="module"></script>\n',
        content,
    )
    content = re.sub(
        r'(<link href="https://assets\.calendly\.com/assets/external/widget\.css" rel="stylesheet">\s*)+',
        '<link href="https://assets.calendly.com/assets/external/widget.css" rel="stylesheet">\n',
        content,
    )
    return content


def clean_footer(content: str) -> str:
    if 'class="site-footer"' in content:
        content = re.sub(
            r'<footer class="site-footer">.*?</html>',
            FOOTER.strip(),
            content,
            flags=re.DOTALL,
        )
        return content
    content = re.sub(
        r'<footer>.*?</html>',
        FOOTER.strip(),
        content,
        flags=re.DOTALL,
    )
    return content


def clean_scripts(content: str) -> str:
    content = re.sub(r'(<script src="/calendly\.js"></script>\s*)+', '<script src="/calendly.js"></script>\n', content)
    return content


for page in sorted(ROOT.glob("*.html")):
    text = page.read_text(encoding="utf-8")
    text = clean_head(text)
    text = clean_footer(text)
    text = clean_scripts(text)
    page.write_text(text, encoding="utf-8")
    print(page.name)
