import unittest
from crawler.storage import WebsiteStorage


class StructureGenTests(unittest.TestCase):
    def test_insertion(self):
        writer = WebsiteStorage()
        writer.insert("test.com/my-url")
        writer.insert("test.com/my-url-2")
        writer.insert("test.com/my-url/hi.html")
        writer.insert("test.com/my-url-3/hi/hi.html")
        writer.pprint()

    def test_find(self):
        writer = WebsiteStorage()
        writer.insert("test.com/my-url")
        writer.insert("test.com/my-url-2")
        writer.insert("test.com/my-url/hi.html")
        writer.insert("test.com/my-url-3/hi/hi.html")

        print(writer.find("test.com"))
        print(writer.find("test.com/my-url"))
        print(writer.find("test.com/my-url-2"))
        print(writer.find("test.com/my-url/hi2.html"))
        print(writer.find("test.com/my-url/hi.html"))

    def test_get_subpages(self):
        writer = WebsiteStorage()
        writer.insert("test.com/my-url")
        writer.insert("test.com/my-url-2")
        writer.insert("test.com/my-url/hi.html")
        writer.insert("test.com/my-url-3/hi/hi.html")

        print(writer.get_subpages("test.com"))
        print(writer.get_subpages("test.com/my-url"))
        print(writer.get_subpages("test.com/my-url-2"))
        print(writer.get_subpages("test.com/my-url/hi.html"))

    @unittest.expectedFailure
    def test_get_subpage_failure(self):
        writer = WebsiteStorage()
        writer.insert("test.com/my-url")
        writer.insert("test.com/my-url-2")
        writer.insert("test.com/my-url/hi.html")
        writer.insert("test.com/my-url-3/hi/hi.html")
        print(writer.get_subpages("test.com/my-url/hi2.html"))

    def test_depth_first_traversal(self):
        writer = WebsiteStorage()
        writer.insert("test.com/my-url")
        writer.insert("test.com/my-url-2")
        writer.insert("test.com/my-url/hi.html")
        writer.insert("test.com/my-url-3/hi/hi.html")
