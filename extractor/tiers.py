import re

# Words that strongly indicate tiers
TIER_KEYWORDS_STRONG = [
    "title sponsor",
    "associate sponsor",
    "platinum sponsor",
    "gold sponsor",
    "silver sponsor",
    "bronze sponsor",
    "powered by",
    "official partner",
    "sponsored by",
    "Alumini sponsor",
    "diamond sponsor" 
]

PORTFOLIO_KEYWORDS = [
    "official",
    "partner",
    "powered by",
    "bulk sms",
    "technology partner",
    "media partner",
    "banking partner",
    "travel partner",
    "education partner",
]


def contains_tier_word(text: str) -> bool:
    """Return True if text contains a strong tier keyword."""
    text = text.lower()
    for kw in TIER_KEYWORDS_STRONG:
        if kw in text:
            return True
    return False


def find_closest_tier_header(container) -> str | None:
    """
    Search near the container for a tier-like heading.
    Checks:
     - previous sibling headers
     - parent headers
    """
    # 1) Check previous siblings
    for sib in container.find_previous_siblings(limit=3):
        if sib.name in ["h1", "h2", "h3", "h4"]:
            txt = sib.get_text(" ", strip=True)
            if contains_tier_word(txt):
                return txt

    # 2) Check parent header
    parent = container.find_parent()
    if parent:
        for header in parent.find_all(["h1", "h2", "h3", "h4"]):
            txt = header.get_text(" ", strip=True)
            if contains_tier_word(txt):
                return txt

    return None

def find_logo_local_tier(img):
    """
    Look for descriptive tier text near a logo.
    Priority:
      1. Previous sibling text
      2. Parent container text
    """

    # 1️⃣ Previous siblings (most common case)
    for sib in img.find_previous_siblings(limit=3):
        text = sib.get_text(" ", strip=True)
        if text and any(k in text.lower() for k in PORTFOLIO_KEYWORDS):
            return text

    # 2️⃣ Parent container (fallback)
    parent = img.find_parent(["div", "td", "section"])
    if parent:
        for child in parent.find_all(["p", "span", "div"], recursive=False):
            text = child.get_text(" ", strip=True)
            if text and any(k in text.lower() for k in PORTFOLIO_KEYWORDS):
                return text

    return None

def determine_tier(img, group_tier):
    # Highest priority: logo-local tier
    local_tier = find_logo_local_tier(img)
    if local_tier:
        return local_tier

    # Fallback: group-level tier
    return group_tier
