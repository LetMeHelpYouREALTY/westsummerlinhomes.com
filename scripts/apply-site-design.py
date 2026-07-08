#!/usr/bin/env python3
"""Strip inline layout CSS and wire site.css + site.js on HTML pages."""

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ASSET_VERSION = "20260708"
SITE_CSS = f"/site.css?v={ASSET_VERSION}"

HEAD_ASSETS = f"""    <link rel="stylesheet" href="{SITE_CSS}">
    <script src="https://em.realscout.com/widgets/realscout-web-components.umd.js" type="module"></script>
    <link href="https://assets.calendly.com/assets/external/widget.css" rel="stylesheet">"""

SCRIPT_TAGS = f"""    <script src="https://assets.calendly.com/assets/external/widget.js" async></script>
    <script src="/site.js?v={ASSET_VERSION}"></script>
    <script src="/calendly.js?v={ASSET_VERSION}"></script>"""

PAGES = [
    "index.html",
    "about.html",
    "contact.html",
    "services.html",
    "properties.html",
]


def strip_layout_styles(content: str) -> str:
    content = re.sub(
        r"\s*<style>\s*realscout-office-listings.*?</style>\s*",
        "\n",
        content,
        flags=re.DOTALL,
    )
    content = re.sub(
        r"\s*<style>\s*\* \{.*?</style>\s*",
        "\n",
        content,
        flags=re.DOTALL,
    )
    return content


def normalize_head(content: str) -> str:
    content = strip_layout_styles(content)
    content = re.sub(r'\s*<link rel="stylesheet" href="/header\.css">\s*', "\n", content)
    if "/site.css" not in content:
        content = content.replace(
            '<link rel="icon"',
            HEAD_ASSETS + "\n    <link rel=\"icon\"",
            1,
        )
    content = re.sub(r'<script src="/header\.js"></script>\s*', "", content)
    if '<script src="/site.js"></script>' not in content:
        content = re.sub(
            r'(<script src="https://assets\.calendly\.com/assets/external/widget\.js" async></script>\s*)',
            SCRIPT_TAGS + "\n",
            content,
            count=1,
        )
    return content


def add_nav_call(content: str) -> str:
    if 'class="nav-call"' in content:
        return content
    return content.replace(
        '            </a>\n            <button type="button" class="nav-toggle"',
        '            </a>\n            <a href="tel:7022221964" class="nav-call">📞 702-222-1964</a>\n            <button type="button" class="nav-toggle"',
    )


def fix_scripts(content: str) -> str:
    return re.sub(
        r"\s*<script>\s*// Smooth scrolling for navigation links.*?</script>\s*",
        "\n",
        content,
        flags=re.DOTALL,
    )


for page in PAGES:
    path = ROOT / page
    if not path.exists():
        continue
    text = path.read_text(encoding="utf-8")
    text = normalize_head(text)
    text = add_nav_call(text)
    text = fix_scripts(text)
    path.write_text(text, encoding="utf-8")
    print(f"Updated {page}")
