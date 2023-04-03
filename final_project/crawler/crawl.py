import os
import pathlib
import time

import bs4
import numpy as np
import requests

from crawler.storage import WebsiteStorage
from crawler.utils import RE_BASE, RE_HTML, RE_STRIPBASE, normalize_url


def download_webpage(url: str) -> str:
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers)
    if response.status_code >= 400:
        raise RuntimeError("Request failed")
    return response.text


def parse_links(content: str, prefix_url: str):
    prefix_url = RE_STRIPBASE.sub("/", prefix_url)
    parsed_content = bs4.BeautifulSoup(content, "html.parser")
    links = set([link.get("href") for link in parsed_content.find_all("a")])
    links.update(frame.get("src") for frame in parsed_content.find_all("frame"))

    filtered = []
    for link in links:
        if link.startswith(".."):
            # ignore relative links
            continue
        if RE_HTML.search(link) and not RE_BASE.search(link):
            filtered.append(prefix_url + link)
    return list(set(filtered))


def crawl(url: str, storage_directory: pathlib.Path):
    webpath = storage_directory / pathlib.Path(normalize_url(url))
    webpath.mkdir(parents=True, exist_ok=True)

    stack = [url]
    storage = WebsiteStorage(storage_directory)
    visited = set()

    rng = np.random.default_rng()

    while len(stack) > 0:
        delay = rng.integers(2, 15)
        current_url = stack[-1]
        if current_url in visited:
            continue
        print(f"Downloading {current_url}...", end="")
        stack.pop()

        webpage = download_webpage(current_url)
        storage.insert(current_url, webpage)
        visited.add(current_url)

        stack.extend(parse_links(webpage, current_url))
        print(f"DONE, sleeping for {delay} seconds")
        time.sleep(delay)

    storage.write()
