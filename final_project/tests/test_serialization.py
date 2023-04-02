import unittest
from crawler.storage import WebsiteStorage
from crawler.website_node import WebsiteNodeEncoder, WebsiteNodeDecoder
import json


class StructureGenTests(unittest.TestCase):
    def test_encode(self):
        writer = WebsiteStorage()
        writer.insert("test.com/my-url")
        writer.insert("test.com/my-url-2")
        writer.insert("test.com/my-url/hi.html")
        writer.insert("test.com/my-url-3/hi/hi.html")
        writer.pprint()
        encoder = WebsiteNodeEncoder()
        serialized = encoder.default(writer["test.com"])
        print(json.dumps(serialized))

    def test_decode(self):
        writer = WebsiteStorage()
        writer.insert("test.com/my-url")
        writer.insert("test.com/my-url-2")
        writer.insert("test.com/my-url/hi.html")
        writer.insert("test.com/my-url-3/hi/hi.html")
        writer.pprint()
        string = json.dumps(writer["test.com"], cls=WebsiteNodeEncoder)
        writer.root = json.loads(string, cls=WebsiteNodeDecoder)
        writer.pprint()
