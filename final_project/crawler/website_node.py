from json import JSONDecoder, JSONEncoder
from pathlib import Path
from typing import Any

from crawler.rw_lock import RWLock
from crawler.utils import NodeType


class WebsiteNode:
    def __init__(self, folder: str, url: str, type: NodeType, level: int, path: Path):
        self.folder = folder
        self.url = url
        self.type = type
        self.level = level
        self.path = path

        self.lock = RWLock()
        self.children = {}
        self.__create()

    def __create(self):
        if self.type == NodeType.WEBPAGE:
            self.path.parent.mkdir(parents=True, exist_ok=True)
            self.path.touch(exist_ok=True)

        elif self.type == NodeType.INTERNAL:
            self.path.mkdir(parents=True, exist_ok=True)
        assert self.path.exists()

    def write(self, data: str):
        if self.type == NodeType.WEBPAGE:
            with self.path.open("w") as ofstream:
                ofstream.write(data)

    def __repr__(self):
        return f"{self.url}: {self.level}"


class WebsiteNodeEncoder(JSONEncoder):
    def default(self, o: Any) -> Any:
        if isinstance(o, WebsiteNode):
            serialized = {
                "folder": o.folder,
                "url": o.url,
                "type": o.type,
                "level": o.level,
                "obj": "website_node",
                "path": str(o.path),
            }
            if len(o.children) != 0:
                children = [self.default(child) for child in o.children.values()]
            else:
                children = []
            serialized["children"] = children
            return serialized
        return super().default(o)


class WebsiteNodeDecoder(JSONDecoder):
    def __init__(self, *args, **kwargs):
        JSONDecoder.__init__(self, object_hook=self.object_hook, *args, **kwargs)

    def object_hook(self, object):
        if not isinstance(object, dict):
            return object
        if "obj" not in object and object["obj"] != "website_node":
            return object

        node = WebsiteNode(
            object["folder"],
            object["url"],
            object["type"],
            object["level"],
            Path(object["path"]),
        )
        if len(object["children"]) > 0:
            parsed_children = {}
            for child_object in object["children"]:
                child = self.object_hook(child_object)
                parsed_children[child.folder] = child
            node.children = parsed_children
        return node
