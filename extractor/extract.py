from bs4 import BeautifulSoup
import requests
import re
import os
from urllib.parse import urlparse, urljoin 
from extractor.tiers import contains_tier_word, find_closest_tier_header, determine_tier

def find_sponsor_groups(html):
    """
    Find repeating DOM blocks that likely represent sponsor groups.
    """
    soup = BeautifulSoup(html, "lxml")
    groups = []

    # Look for containers with multiple images (logos)
    for container in soup.find_all(["div", "section"]):
        images = container.find_all("img") 
        if len(images)<1:
            continue

        # Ignore very large containers (entire page) -> might be reason if more text, less images 
        text_len = len(container.get_text(strip=True))
        if text_len > 2000:
            continue

        groups.append(container)

    return groups

#optional if we find out the closest tier header
def extract_group_label(container):
    """
    Extract portfolio/category name near a sponsor group.
    """
    # Check headers inside container
    for tag in container.find_all(["h1", "h2", "h3", "h4", "h5", "h6"]):
        text = tag.get_text(strip=True)
        if 2 <= len(text.split()) <= 6:
            return text

    # Check immediate previous siblings
    prev = container.find_previous_sibling()
    if prev:
        text = prev.get_text(strip=True)
        if 2 <= len(text.split()) <= 6:
            return text

    return None  # group exists, label unclear

def resolve_brand_name(img, base_url):
    """
    Resolve brand name using multiple weak signals.
    Priority:
    alt > link domain > filename
    """
    # 1. alt text
    alt = img.get("alt")
    if alt and len(alt.strip()) > 2:
        return alt.strip(), 0.9

    # 2. parent link domain
    parent_link = img.find_parent("a")
    if parent_link and parent_link.get("href"):
        domain = urlparse(parent_link["href"]).netloc
        if domain:
            return domain.replace("www.", "").split(".")[0], 0.75

    # 3. image filename
    src = img.get("src")
    if src:
        filename = os.path.basename(src)
        name = re.sub(r"[-_].*", "", filename)
        name = os.path.splitext(name)[0]
        if len(name) > 2:
            return name, 0.7

    return None, 0.0

#main extraction - tier detection
def extract_sponsors_from_group(container, base_url, group_name=None):
    sponsors = []
    imgs = container.find_all("img")

    # Find a strong tier label first
    tier = determine_tier(container, group_name)

    # Only treat the raw group label as tier if it *really looks like* one
    if not tier and group_name and contains_tier_word(group_name):
        tier = group_name

    for img in imgs:
        name, confidence = resolve_brand_name(img, base_url)
        
        if confidence >= 0.9 and name: extraction_mtd = "alt"
        elif confidence >= 0.75: extraction_mtd = "link_domain"
        elif confidence >= 0.7: extraction_mtd = "filename"
        else: extraction_mtd = "unknown"

        if name:
            sponsors.append({
                "name": name,
                "confidence": confidence,
                "group": tier,
                "extraction_method": extraction_mtd,
                "raw_text": img.get("alt") or name,
            })

    return sponsors

#full extraction function
def extract_sponsors_advanced(html, base_url):
    groups = find_sponsor_groups(html)
    all_sponsors = []

    for group in groups:
        group_name = extract_group_label(group)

        sponsors = extract_sponsors_from_group(group, base_url, group_name) 

        all_sponsors.extend(sponsors)

    return deduplicate(all_sponsors)


def deduplicate(items):
    seen = {}
    for item in items:
        key = item["name"].lower()
        if key not in seen or seen[key]["confidence"] < item["confidence"]:
            seen[key] = item
    return list(seen.values())

