#!/usr/bin/env python

import click
import re
import requests
import pathlib
import os
import bs4
from collections import deque
from json import load, dump

import re

from crawler.website_node import WebsiteNode, WebsiteNodeDecoder, WebsiteNodeEncoder
from crawler.crawler_types import NodeType


class WebsiteStorage:
    """
    Track structure of website when crawling.

    Assumption is that the urls are well-formatted
    (the crawler needs to go ahead and track this structure properly)
    """

    def __init__(self):
        self.root = WebsiteNode("", "", NodeType.INTERNAL, -1)

    def __get_node_type(self, url: str):
        if re.match(r".html$", url):
            return NodeType.WEBPAGE
        return NodeType.INTERNAL

    def __insert(self, node: WebsiteNode, url_parts: list[str], level: int):
        """Helper function for recursively building a tree structure"""
        folder = url_parts[level + 1]
        children = node.children
        if len(url_parts[level:]) == 2:
            url = "/".join(url_parts[1:])
            target_type = self.__get_node_type(folder)
            children[folder] = WebsiteNode(folder, url, target_type, level)
        else:
            url = "/".join(url_parts[1 : level + 2])
            if folder not in children:
                children[folder] = WebsiteNode(folder, url, NodeType.INTERNAL, level)
            self.__insert(children[folder], url_parts, level + 1)

    def __bfs(self):
        """Breadth-first iteration through tree structure."""
        bfs_queue = deque(self.root.children.values())
        while len(bfs_queue) > 0:
            node = bfs_queue.popleft()
            yield node
            bfs_queue.extend(node.children.values())

    def __dfs(self):
        """Depth-first iteration through tree structure."""
        stack = list(self.root.children.values())
        while len(stack) > 0:
            node = stack.pop()
            yield node
            stack.extend(node.children.values())

    def __iter__(self):
        yield from self.__dfs()

    def read(self, dirpath):
        config_file = dirpath / "config.yml"
        with config_file.open("r") as ifstream:
            self.root = load(ifstream, cls=WebsiteNodeDecoder)
        self.pprint()

    def write(self, dirpath: pathlib.Path):
        config_file = dirpath / "structure.json"
        with config_file.open("w") as ofstream:
            dump(self.root, ofstream, cls=WebsiteNodeEncoder)

    def __getitem__(self, url: str):
        return self.find(url)

    def find(self, url: str):
        for node in self.__bfs():
            if node.url == url:
                return node
        return None

    def get_subpages(self, url: str):
        node = self.find(url)
        return list(node.children.values())

    def pprint(self):
        iterator = iter(self)
        for node in iterator:
            if node.level > 0:
                print("  " * (node.level - 1), end="")
            print("┗━ " + node.url)

    def insert(self, url: str):
        """Insert a webpage url into the tree structure."""
        self.__insert(self.root, [""] + url.split("/"), 0)


def get_folder_name(url: str):
    url = url.strip()[:-1]
    url = re.sub(r"https?:\/\/", "", url)  # remove https
    url = re.sub(r"[^a-zA-Z]", "_", url)  # remove nonstandard chars
    return url


def download_webpage(url: str) -> str:
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers)
    if response.status_code >= 400:
        raise RuntimeError("Request failed")
    return response.text


def parse_links(content: str):
    parsed_content = bs4.BeautifulSoup(content, "html.parser")
    links = [link.get("href") for link in parsed_content.find_all("a")]
    # check all frames because that's a thing lol
    frames = [frame.get("src") for frame in parsed_content.find_all("frame")]
    return links + frames


def filter_links(links: list[str], prefix: str):
    filtered_links = []
    for link in links:
        if re.match(r".\.html$", link):
            filtered_links.append(link)
    return filtered_links


def write_webpage(url: str, content: str, basedir: pathlib.Path) -> None:
    name = os.path.basename(url)
    if name == "":
        name = "index.html"
    file = basedir / pathlib.Path(name)
    with file.open("w") as ofstream:
        ofstream.write(content)


def crawl(url: str, storage_directory: pathlib.Path):
    webpath = storage_directory / pathlib.Path(get_folder_name(url))
    webpath.mkdir(parents=True, exist_ok=True)
    stack = [url]
    while len(stack) > 0:
        webpage = download_webpage(url)
        write_webpage(url, webpage, webpath)
        links = parse_links(webpage)
        stack.extend(filter_links(links, url))
        print(stack)
        break


@click.command("Crawler")
@click.argument("url")
@click.argument("storage_directory")
def main(url: str, storage_directory: str):
    crawl(url, pathlib.Path(storage_directory))


if __name__ == "__main__":
    main()
