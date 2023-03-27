#!/usr/bin/env python

import click
import re
import requests
import pathlib
import os
import bs4

from dataclasses import dataclass, field
import enum
import re

from typing import Dict


class NodeType(enum.Enum):
    INTERNAL = 0
    WEBPAGE = 1


@dataclass
class StructureNode:
    folder: str
    url: str
    type: NodeType
    level: int
    children: Dict[str, "StructureNode"] = field(default_factory=lambda: {})


class SiteTreeParser:
    """
    Track structure of website when crawling.

    Assumption is that the urls are well-formatted
    (the crawler needs to go ahead and track this structure properly)
    """

    def __init__(self):
        self.root = StructureNode("", "", NodeType.INTERNAL, -1)

    @classmethod
    def from_file(cls, filename):
        pass

    def __get_node_type(self, url: str):
        if re.match(r".html$", url):
            return NodeType.WEBPAGE
        return NodeType.INTERNAL

    def __insert(self, node: StructureNode, url_parts: list[str], level: int):
        """Helper function for recursively building a tree structure"""
        folder = url_parts[level + 1]
        children = node.children
        if len(url_parts[level:]) == 2:
            url = "/".join(url_parts[1:])
            target_type = self.__get_node_type(folder)
            children[folder] = StructureNode(folder, url, target_type, level)
        else:
            url = "/".join(url_parts[1 : level + 2])
            if folder not in children:
                children[folder] = StructureNode(folder, url, NodeType.INTERNAL, level)
            self.__insert(children[folder], url_parts, level + 1)

    def __iter__(self):
        """Depth-first iteration through tree structure"""
        stack = list(self.root.children.values())
        while len(stack) > 0:
            node = stack.pop()
            yield node
            stack.extend(node.children.values())

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
        if link.startswith(prefix):
            filtered_links.append(link)
    return filtered_links


def write_webpage(url: str, content: str, basedir: pathlib.Path) -> None:
    name = os.path.basename(url)
    if name == "":
        name = "index.html"
    file = basedir / pathlib.Path(name)
    with file.open("w") as ofstream:
        ofstream.write(content)


@click.command("Crawler")
@click.argument("url")
@click.argument("storage_directory")
def main(url: str, storage_directory: str):
    storage_directory = pathlib.Path(storage_directory)
    webpath = storage_directory / pathlib.Path(get_folder_name(url))
    webpath.mkdir(parents=True, exist_ok=True)
    num_docs = len([item for item in webpath.iterdir()])
    # if num_docs == 0:
    webpage = download_webpage(url)
    write_webpage(url, webpage, webpath)
    # else:
    #     with (storage_directory / webpage / "index.html").open("r") as ifstream:
    #         webpage = ifstream.read()
    links = parse_links(webpage)
    print(links)
    # print(filter_links(links, url))


if __name__ == "__main__":
    main()
