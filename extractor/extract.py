from bs4 import BeautifulSoup
import re
import os
from urllib.parse import urlparse, urljoin

from extractor.tiers import sanitize_tier  

GENERIC_NAMES = {
    "logo", "sponsor", "sponsor logo",
    "partner", "image", "img",
    "mood indigo logo"
}


# ----------------------------
# 1️⃣ BRAND NAME RESOLUTION
# ----------------------------

def resolve_brand_name(img, base_url):
    # 1. alt text
    alt = img.get("alt")
    if alt:
        alt_clean = alt.strip().lower()
        if alt_clean not in GENERIC_NAMES and len(alt_clean) > 3:
            return alt.strip(), 0.9

    # 2. parent link domain
    parent_link = img.find_parent("a")
    if parent_link and parent_link.get("href"):
        domain = urlparse(parent_link["href"]).netloc
        if domain:
            brand = domain.replace("www.", "").split(".")[0]
            if len(brand) > 2:
                return brand, 0.85

    # 3. image filename
    src = img.get("src")
    if src:
        filename = os.path.basename(src)
        name = re.sub(r"[-_].*", "", filename)
        name = os.path.splitext(name)[0]
        if len(name) > 2:
            return name, 0.7

    return None, 0.0


# ----------------------------
# 2️⃣ LOGO EXTRACTION (GLOBAL)
# ----------------------------

def extract_all_logos(soup, base_url):
    logos = []

    for img in soup.find_all("img"):
        src = img.get("src")
        if not src:
            continue

        src = urljoin(base_url, src)

        # filter obvious non-logo images
        if any(x in src.lower() for x in [
            "icon", "sprite", "arrow", "loader",
            "background", "banner", "decor"
        ]):
            continue

        logos.append(img)

    return logos


# ----------------------------
# 3️⃣ TIER DETECTION (LOGO-CENTRIC)
# ----------------------------

def find_tier_for_logo(img):
    texts = []

    # previous siblings
    for sib in img.find_previous_siblings(limit=5):
        texts.append(sib.get_text(" ", strip=True))

    # next siblings
    for sib in img.find_next_siblings(limit=5):
        texts.append(sib.get_text(" ", strip=True))

    # parent context
    parent = img.parent
    if parent:
        texts.append(parent.get_text(" ", strip=True))

        for sib in parent.find_previous_siblings(limit=3):
            texts.append(sib.get_text(" ", strip=True))

        for sib in parent.find_next_siblings(limit=3):
            texts.append(sib.get_text(" ", strip=True))

    for t in texts:
        tier = sanitize_tier(t)
        if tier:
            return tier

    return None


# ----------------------------
# 4️⃣ GROUP-BASED FALLBACK
# ----------------------------

def extract_group_based(soup, base_url):
    sponsors = []

    for container in soup.find_all(["div", "section"]):
        imgs = container.find_all("img")
        if len(imgs) < 2:
            continue

        group_text = container.get_text(" ", strip=True)
        group_tier = sanitize_tier(group_text)

        for img in imgs:
            name, confidence = resolve_brand_name(img, base_url)
            if not name:
                continue

            sponsors.append({
                "name": name,
                "confidence": confidence,
                "tier": group_tier,
                "raw_text": img.get("alt") or name,
                "source": "group",
            })

    return sponsors


# ----------------------------
# 5️⃣ MAIN ROBUST EXTRACTOR
# ----------------------------

def extract_sponsors_advanced(html, base_url):
    soup = BeautifulSoup(html, "lxml")
    sponsors = []

    # 🔹 Strategy A: Logo-centric (primary, robust)
    logos = extract_all_logos(soup, base_url)

    for img in logos:
        name, confidence = resolve_brand_name(img, base_url)
        if not name:
            continue

        tier = find_tier_for_logo(img)

        sponsors.append({
            "name": name,
            "confidence": confidence,
            "tier": tier,
            "raw_text": img.get("alt") or name,
            "source": "logo",
        })

    # 🔹 Strategy B: Group-based fallback (older simple sites)
    if len(sponsors) < 5:
        sponsors.extend(extract_group_based(soup, base_url))

    return deduplicate(sponsors)


# ----------------------------
# 6️⃣ SAFE DEDUPLICATION
# ----------------------------

def deduplicate(items):
    seen = {}

    for item in items:
        key = (
            item["name"].lower(),
            item.get("tier"),
        )

        if key not in seen or seen[key]["confidence"] < item["confidence"]:
            seen[key] = item

    return list(seen.values())
