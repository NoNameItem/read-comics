"""Pure helpers for ComicVine text. Must not import anything from the project (circular-import risk)."""

import re

from bs4 import BeautifulSoup

_LINK_TAGS = re.compile(r"<(a|/a).*?>")
_COVERS_LIST = re.compile(r"<h4>List of covers and their creators:<\/h4><table[^>]*>.*?<\/table>")
_LEADING_NUMBER = re.compile(r"^\d+(\.\d+)?")


def strip_links(text):
    """Remove <a> and </a> tags; empty input gives None."""
    if text:
        return _LINK_TAGS.sub("", text)
    return None


def strip_issue_description(text):
    """Remove links and the covers table from an issue description; empty input is returned as is."""
    if not text:
        return text
    return _COVERS_LIST.sub("", strip_links(text))


def set_lazy_image_sources(html, img_class=None):
    """Point lazy images at their real source; optionally add img_class to every img."""
    soup = BeautifulSoup(html, "html.parser")
    for image in soup.select("img.js-lazy-load-image"):
        image["src"] = image.get("data-src")
    if img_class:
        for image in soup.select("img"):
            classes = image.get("class", [])
            classes.append(img_class)
            image["class"] = classes
    return str(soup)


def numerical_issue_number(number):
    """Sortable float for an issue number string; None for an empty one."""
    if not number:
        return None
    if number == "½":
        return 0.5
    match = _LEADING_NUMBER.match(number)
    return float(match.group(0)) if match else 0.0


def split_aliases(text):
    """Split a newline-separated aliases field into stripped non-empty names."""
    if not text:
        return []
    return [line.strip() for line in text.splitlines() if line.strip()]
