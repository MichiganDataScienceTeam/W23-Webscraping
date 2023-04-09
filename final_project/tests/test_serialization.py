import json
import tempfile
import unittest
from pathlib import Path

from crawler.storage import WebsiteStorage
from crawler.website_node import WebsiteNodeDecoder, WebsiteNodeEncoder


class StructureGenTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tempdir = tempfile.TemporaryDirectory()
        self.tempdir_fpath = Path(self.tempdir.name)
        print(f"Created {str(self.tempdir_fpath)}")
        return super().setUp()

    def tearDown(self) -> None:
        print(f"Deleted {str(self.tempdir_fpath)}")
        self.tempdir.cleanup()
        return super().tearDown()

    def test_encode(self):
        writer = WebsiteStorage(self.tempdir_fpath)
        writer.insert("test.com/my-url", "EEE")
        writer.insert("test.com/my-url-2", "EEE")
        writer.insert("test.com/my-url/hi.html", "EEE")
        writer.insert("test.com/my-url-3/hi/hi.html", "EEE")
        writer.pprint()
        encoder = WebsiteNodeEncoder()
        serialized = encoder.default(writer["test.com"])
        print(json.dumps(serialized))

    def test_decode(self):
        writer = WebsiteStorage(self.tempdir_fpath)
        writer.insert("test.com/my-url", "EEE")
        writer.insert("test.com/my-url-2", "EEE")
        writer.insert("test.com/my-url/hi.html", "EEE")
        writer.insert("test.com/my-url-3/hi/hi.html", "EEE")
        writer.pprint()
        string = json.dumps(writer["test.com"], cls=WebsiteNodeEncoder)
        writer.root = json.loads(string, cls=WebsiteNodeDecoder)
        writer.pprint()
