import logging
import pathlib
import time
from concurrent.futures.thread import ThreadPoolExecutor
from dataclasses import dataclass
from enum import Enum
from queue import Empty, Queue
from threading import Lock
from typing import Union

import bs4
import numpy as np
import requests

from crawler.storage import WebsiteStorage
from crawler.utils import RE_BASE, RE_HTML, RE_STRIPBASE, normalize_url

NUM_WORKERS = 10
JOB_TIMEOUT_WAIT = 10


logger = logging.getLogger(__name__)
logging.basicConfig(level="INFO", format="%(levelname)s: %(message)s")

job_queue = Queue()
visited = set()
visited_lock = Lock()


def crawl_page(worker_id: int, url: str, storage: WebsiteStorage) -> bool:
    with visited_lock:
        if url in visited:
            return False

    with visited_lock:
        visited.add(url)

    logger.info(f"Worker %d | Downloading %s...", worker_id, url)
    if (webpage := download_webpage(worker_id, url)) is None:
        return False

    storage.insert(url, webpage)
    links = parse_links(webpage, url)
    for link in links:
        with visited_lock:
            if link not in visited:
                job_queue.put(link)
    return True


def worker(worker_id: int, storage: WebsiteStorage) -> None:
    logger.info("Worker %d | Started crawl, waiting for requests", worker_id)
    shutdown = False
    rng = np.random.default_rng()
    while not shutdown:
        try:
            url = job_queue.get(timeout=JOB_TIMEOUT_WAIT)
            if crawl_page(worker_id, url, storage):
                delay = rng.uniform(10, 20)
                logger.info("Worker %d | Sleeping for %f seconds", worker_id, delay)
                time.sleep(delay)
        except Empty:
            logger.info("Worker %d | Wait for job timed out, shutting down", worker_id)
            shutdown = True


def download_webpage(worker_id: int, url: str) -> str:
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers)
    if response.status_code >= 400:
        logger.warn(
            "Worker %d | Request failed with error code %d, skipping",
            worker_id,
            response.status_code,
        )
        return None
    return response.text


def parse_links(content: str, prefix_url: str):
    prefix_url = RE_STRIPBASE.sub("/", prefix_url)
    parsed_content = bs4.BeautifulSoup(content, "html.parser")
    links = set([link.get("href") for link in parsed_content.find_all("a")])
    links.update(frame.get("src") for frame in parsed_content.find_all("frame"))

    filtered = []
    for link in links:
        if not link:
            continue
        if link.startswith(".."):
            # ignore relative links
            continue
        if not RE_BASE.search(link):
            if RE_HTML.search(link):
                filtered.append(prefix_url + link)
            if link.endswith("/"):
                filtered.append(prefix_url + link)  # this is also a link to check out
    return list(set(filtered))


def load(filepath: Union[str, pathlib.Path]) -> WebsiteStorage:
    filepath = pathlib.Path(filepath)
    storage =  WebsiteStorage(filepath)
    storage.read()
    return storage


def crawl(url: str, storage_directory: pathlib.Path):
    structure_path = storage_directory / pathlib.Path("structure.json")
    if structure_path.exists():
        print(
            f"Existing crawl data found at {str(storage_directory)}, would you like to recrawl?"
        )
        response = input("> [y/n]: ")
        while response != "y" and response != "n":
            print(f"Invalid response: {response}")
            response = input("> [y/n]: ")
        if response == "n":
            print("Exiting crawler")
            return

    webpath = storage_directory / pathlib.Path(normalize_url(url))
    webpath.mkdir(parents=True, exist_ok=True)

    storage = WebsiteStorage(storage_directory)
    job_queue.put(url)
    with ThreadPoolExecutor(NUM_WORKERS) as executor:
        for index in range(NUM_WORKERS):
            executor.submit(worker, index, storage)
            time.sleep(1)  # this is done to offset the wait times
    storage.write()
