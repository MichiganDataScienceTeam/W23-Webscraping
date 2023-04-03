#!/usr/bin/env python

import pathlib
from collections import deque
from json import dump, load
from os import getcwd
from typing import Union

from crawler.utils import RE_BASE, RE_HTML, NodeType, normalize_url
from crawler.website_node import WebsiteNode, WebsiteNodeDecoder, WebsiteNodeEncoder


class WebsiteStorage:
    """
    Track structure of website when crawling.

    Creates folder structure on disk to mirror website format. Assumption is that
    the urls are well-formatted.
    """

    def __init__(self, storage_directory: Union[str, pathlib.Path] = None):
        if not storage_directory:
            storage_directory = getcwd()
        self.workdir = pathlib.Path(storage_directory)
        if not self.workdir.exists():
            self.workdir.mkdir(parents=True)
        self.root = WebsiteNode("", "", NodeType.INTERNAL, -1, self.workdir)

    def __get_node_type(self, url: str):
        if RE_HTML.search(url):
            return NodeType.WEBPAGE
        return NodeType.INTERNAL

    def __insert(self, node: WebsiteNode, url_parts: list[str], level: int, data: str):
        """Helper function for recursively building a tree structure"""
        folder = url_parts[level + 1]
        children = node.children
        fpath = node.path / normalize_url(folder)
        if len(url_parts[level:]) == 2:
            url = "/".join(url_parts[1:])
            target_type = self.__get_node_type(folder)
            node = WebsiteNode(folder, url, target_type, level, fpath)
            node.write(data)
            children[folder] = node
        else:
            url = "/".join(url_parts[1 : level + 2])
            if folder not in children:
                children[folder] = WebsiteNode(
                    folder, url, NodeType.INTERNAL, level, fpath
                )
            self.__insert(children[folder], url_parts, level + 1, data)

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

    def read(self):
        config_file = self.workdir / "config.yml"
        with config_file.open("r") as ifstream:
            self.root = load(ifstream, cls=WebsiteNodeDecoder)
        self.pprint()

    def write(self):
        config_file = self.workdir / "structure.json"
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

    def insert(self, url: str, data: str):
        """Insert a webpage url into the tree structure."""
        url = RE_BASE.sub("", url)
        self.__insert(self.root, [""] + url.split("/"), 0, data)
