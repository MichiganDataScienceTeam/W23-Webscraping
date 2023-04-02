from dataclasses import dataclass, field
from typing import Dict
from crawler.crawler_types import NodeType


@dataclass
class WebsiteNode:
    folder: str
    url: str
    type: NodeType
    level: int
    children: Dict[str, "WebsiteNode"] = field(default_factory=lambda: {})

    def __repr__(self):
        return f"{self.url}: {self.level}"
