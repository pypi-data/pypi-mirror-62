from threading import Thread, Lock, Semaphore, Event
from queue import Queue


ONE_YEAR = 365 * 24 * 60 * 60

THREAD_DONE = object()

class ExceptionBox(object):
    def __init__(self, exc):
        self.exc = exc

class LazyThreadPoolExecutor(object):
    def __init__(self, num_workers=1):
        self.num_workers = num_workers
        self.result_queue = Queue()
        self.thread_sem = Semaphore(num_workers)
        self._shutdown = Event()
        self.threads = []

    def map(self, predicate, iterable):
        self._shutdown.clear()
        self.iterable = ThreadSafeIterator(iterable)
        self._start_threads(predicate)
        return self._result_iterator()

    def shutdown(self, wait=True):
        self._shutdown.set()
        if wait:
            for t in self.threads:
                t.join()

    def _start_threads(self, predicate):
        for i in range(self.num_workers):
            t = Thread(
                name="LazyChild #{0}".format(i),
                target=self._make_worker(predicate)
            )
            t.daemon = True
            self.threads.append(t)
            t.start()

    def _make_worker(self, predicate):
        def _w():
            with self.thread_sem:
                for thing in self.iterable:
                    try:
                        self.result_queue.put(predicate(thing))
                    except Exception as e:
                        self.result_queue.put(ExceptionBox(e))
                    if self._shutdown.is_set():
                        break
            self.result_queue.put(THREAD_DONE)
        return _w

    def _result_iterator(self):
        while 1:
            # Queue.get is not interruptable w/ ^C unless you specify a
            # timeout.
            # Hopefully one year is long enough...
            # See http://bugs.python.org/issue1360
            result = self.result_queue.get(True, ONE_YEAR)
            if result is not THREAD_DONE:
                if isinstance(result, ExceptionBox):
                    raise result.exc
                else:
                    yield result
            else:
                # if all threads have exited
                # sorry, this is kind of a gross way to use semaphores
                # break
                if self.thread_sem._value == self.num_workers:
                    break
                else:
                    continue



class ThreadSafeIterator(object):
    def __init__(self, it):
        self._it = iter(it)
        self.lock = Lock()

    def __iter__(self):
        return self

    def __next__(self):
        with self.lock:
            return self._it.__next__()
