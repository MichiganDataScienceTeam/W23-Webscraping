import threading
import unittest
from typing import List

from crawler.rw_lock import RWLock


class RWLockTests(unittest.TestCase):
    def test_basic(self):
        value = [0]
        lock = RWLock()

        def increment():
            for index in range(10000):
                if index % 5 == 0:
                    lock.wlock()
                    value[0] += 1
                    lock.wrelease()
                else:
                    lock.rlock()
                    print(value[0])
                    lock.rrelease()

        pool: List[threading.Thread] = []
        for _ in range(10):
            tdx = threading.Thread(target=increment)
            tdx.start()
            pool.append(tdx)

        for thread in pool:
            thread.join()

        assert value[0] == 20000
