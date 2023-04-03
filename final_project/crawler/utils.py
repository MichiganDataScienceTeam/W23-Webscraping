import re
from enum import Enum

RE_HTML = re.compile(r"\.html$")
RE_BASE = re.compile(r"^https?\:\/\/")
RE_NORM = re.compile(r"[^\w\d\/\_\-]")
RE_NORM_HTML = re.compile(r"[^\w\d\/\_\-\.]")
RE_STRIPBASE = re.compile(r"\/\w+\.\w+$")
RE_TRAILING_SLASH = re.compile("\/$")


class NodeType(int, Enum):
    INTERNAL = 0
    WEBPAGE = 1


def normalize_url(url: str):
    # want to strip all dots except for .html
    url = RE_TRAILING_SLASH.sub("", url)
    url = RE_BASE.sub("", url)  # remove https
    if RE_HTML.search(url):
        filter = RE_NORM_HTML
    else:
        filter = RE_NORM
    url = filter.sub("_", url)
    return url
