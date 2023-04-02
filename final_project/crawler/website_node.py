from dataclasses import dataclass, field
from typing import Any, Dict
from crawler.crawler_types import NodeType
from json import JSONEncoder, JSONDecoder


@dataclass
class WebsiteNode:
    folder: str
    url: str
    type: NodeType
    level: int
    children: Dict[str, "WebsiteNode"] = field(default_factory=lambda: {})

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
            object["folder"], object["url"], object["type"], object["level"]
        )
        if len(object["children"]) > 0:
            parsed_children = {}
            for child_object in object["children"]:
                child = self.object_hook(child_object)
                parsed_children[child.folder] = child
            node.children = parsed_children
        return node
