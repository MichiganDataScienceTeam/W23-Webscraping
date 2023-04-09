from threading import Condition, Lock


class RWLock:
    def __init__(self):
        self.num_readers = 0
        self.num_writers = 0
        self.lock = Lock()
        self.read_cv = Condition(self.lock)
        self.writer_cv = Condition(self.lock)

    def rlock(self):
        with self.lock:
            while self.num_writers > 0:
                self.read_cv.wait()
            self.num_readers += 1

    def rrelease(self):
        with self.lock:
            self.num_readers -= 1
            if self.num_readers == 0:
                self.writer_cv.notify_all()

    def wlock(self):
        with self.lock:
            while self.num_writers > 0 or self.num_readers > 0:
                self.writer_cv.wait()
            self.num_writers += 1

    def wrelease(self):
        with self.lock:
            self.num_writers -= 1
            if self.num_writers == 0:
                self.writer_cv.notify()  # tell writers to go first to avoid starvation
                self.read_cv.notify_all()
