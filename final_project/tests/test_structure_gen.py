import tempfile
import unittest
from pathlib import Path
from threading import Thread

from crawler.storage import WebsiteStorage


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

    def test_insertion(self):
        writer = WebsiteStorage(self.tempdir_fpath)
        writer.insert("test.com/my-url-3/hi2.html", "EEEE")
        writer.insert("test.com/index.html", "EEEE")
        writer.insert("test.com/my-url/hi.html", "EEEEE")
        writer.insert("test.com/my-url-3/hi/hi.html", "EEEEEE")
        writer.pprint()

    def test_find(self):
        writer = WebsiteStorage(self.tempdir_fpath)
        writer.insert("test.com/my-url-3/hi2.html", "EEEE")
        writer.insert("test.com/index.html", "EEEE")
        writer.insert("test.com/my-url/hi.html", "EEEEE")
        writer.insert("test.com/my-url-3/hi/hi.html", "EEEEEE")

        print(writer.find("test.com"))
        print(writer.find("test.com/my-url"))
        print(writer.find("test.com/my-url-2"))
        print(writer.find("test.com/my-url/hi2.html"))
        print(writer.find("test.com/my-url/hi.html"))

    def test_get_subpages(self):
        writer = WebsiteStorage(self.tempdir_fpath)
        writer.insert("test.com/my-url-3/hi2.html", "EEEE")
        writer.insert("test.com/index.html", "EEEE")
        writer.insert("test.com/my-url/hi.html", "EEEEE")
        writer.insert("test.com/my-url-3/hi/hi.html", "EEEEEE")

        print(writer.get_subpages("test.com"))
        print(writer.get_subpages("test.com/my-url"))
        print(writer.get_subpages("test.com/my-url/hi.html"))

    @unittest.expectedFailure
    def test_get_subpage_failure(self):
        writer = WebsiteStorage(self.tempdir_fpath)
        writer.insert("test.com/my-url-3/hi2.html", "EEEE")
        writer.insert("test.com/index.html", "EEEE")
        writer.insert("test.com/my-url/hi.html", "EEEEE")
        writer.insert("test.com/my-url-3/hi/hi.html", "EEEEEE")
        print(writer.get_subpages("test.com/my-url/hi2.html"))

    def test_depth_first_traversal(self):
        writer = WebsiteStorage(self.tempdir_fpath)
        writer.insert("test.com/my-url-3/hi2.html", "EEEE")
        writer.insert("test.com/index.html", "EEEE")
        writer.insert("test.com/my-url/hi.html", "EEEEE")
        writer.insert("test.com/my-url-3/hi/hi.html", "EEEEEE")

    def test_get_filenames(self):
        writer = WebsiteStorage(self.tempdir_fpath)
        writer.insert("test.com/my-url-3/hi2.html", "EEEE")
        writer.insert("test.com/index.html", "EEEE")
        writer.insert("test.com/my-url/hi.html", "EEEEE")
        writer.insert("test.com/my-url-3/hi/hi.html", "EEEEEE")

        for page in writer:
            print(str(page.path))

        assert (self.tempdir_fpath / "test_com/my-url").exists()
        assert (self.tempdir_fpath / "test_com/my-url").is_dir()

        assert (self.tempdir_fpath / "test_com/my-url-3/hi").exists()
        assert (self.tempdir_fpath / "test_com/my-url-3/hi").is_dir()
        assert (self.tempdir_fpath / "test_com/my-url-3/hi/hi.html").exists()
        assert (self.tempdir_fpath / "test_com/my-url-3/hi/hi.html").is_file()

    def test_multi_thread(self):
        writer = WebsiteStorage(self.tempdir_fpath)

        def load():
            writer.insert("test.com/my-url-3/hi2.html", "EEEE")
            writer.insert("test.com/my-url-3/hi/2.html", "EEEE")
            writer.insert("test.com/index.html", "EEEE")

        def load2():
            writer.insert("test.com/my-url/hi.html", "EEEEE")
            writer.insert("test.com/my-url-3/hi.html", "EEEEE")
            writer.insert("test.com/my-url-3/hi/hi.html", "EEEEEE")

        t1 = Thread(target=load)
        t2 = Thread(target=load2)
        t1.start()
        t2.start()
        t1.join()
        t2.join()

        assert (self.tempdir_fpath / "test_com/my-url").exists()
        assert (self.tempdir_fpath / "test_com/my-url").is_dir()
        assert (self.tempdir_fpath / "test_com/my-url-3/hi").exists()
        assert (self.tempdir_fpath / "test_com/my-url-3/hi").is_dir()
        assert (self.tempdir_fpath / "test_com/my-url-3/hi.html").exists()
        assert (self.tempdir_fpath / "test_com/my-url-3/hi.html").is_file()
        assert (self.tempdir_fpath / "test_com/my-url-3/hi/hi.html").exists()
        assert (self.tempdir_fpath / "test_com/my-url-3/hi/2.html").exists()
        assert (self.tempdir_fpath / "test_com/my-url-3/hi/hi.html").is_file()
        assert (self.tempdir_fpath / "test_com/my-url-3/hi/2.html").is_file()
