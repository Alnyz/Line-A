# -*- coding: utf-8 -*-
import random
import re
import string
import sys
import threading
import traceback

import six
from six import string_types

# Python3 queue support.

try:
    import Queue
except ImportError:
    import queue as Queue
import logging

logger = logging.getLogger(__name__)

thread_local = threading.local()


class WorkerThread(threading.Thread):
        count = 0

        def __init__(self, exception_callback=None, queue=None, name=None):
            if not name:
                name = "WorkerThread{0}".format(self.__class__.count + 1)
                self.__class__.count += 1
            if not queue:
                queue = Queue.Queue()

            threading.Thread.__init__(self, name=name)
            self.queue = queue
            self.daemon = True

            self.received_task_event = threading.Event()
            self.done_event = threading.Event()
            self.exception_event = threading.Event()
            self.continue_event = threading.Event()

            self.exception_callback = exception_callback
            self.exc_info = None
            self._running = True
            self.start()

        def run(self):
            while self._running:
                try:
                    task, args, kwargs = self.queue.get(block=True, timeout=.5)
                    self.continue_event.clear()
                    self.received_task_event.clear()
                    self.done_event.clear()
                    self.exception_event.clear()
                    logger.debug("Received task")
                    self.received_task_event.set()

                    task(*args, **kwargs)
                    logger.debug("Task complete")
                    self.done_event.set()
                except Queue.Empty:
                    pass
                except Exception as e:
                    logger.error(type(e).__name__ + " occurred, args=" + str(e.args) + "\n" + traceback.format_exc())
                    self.exc_info = sys.exc_info()
                    self.exception_event.set()

                    if self.exception_callback:
                        self.exception_callback(self, self.exc_info)
                    self.continue_event.wait()

        def put(self, task, *args, **kwargs):
            self.queue.put((task, args, kwargs))

        def raise_exceptions(self):
            if self.exception_event.is_set():
                six.reraise(self.exc_info[0], self.exc_info[1], self.exc_info[2])

        def clear_exceptions(self):
            self.exception_event.clear()
            self.continue_event.set()

        def stop(self):
            self._running = False


class ThreadPool:

    def __init__(self, num_threads=2):
        self.tasks = Queue.Queue()
        self.workers = [WorkerThread(self.on_exception, self.tasks) for _ in range(num_threads)]
        self.num_threads = num_threads

        self.exception_event = threading.Event()
        self.exc_info = None

    def put(self, func, *args, **kwargs):
        self.tasks.put((func, args, kwargs))

    def on_exception(self, worker_thread, exc_info):
        self.exc_info = exc_info
        self.exception_event.set()
        worker_thread.continue_event.set()

    def raise_exceptions(self):
        if self.exception_event.is_set():
            six.reraise(self.exc_info[0], self.exc_info[1], self.exc_info[2])

    def clear_exceptions(self):
        self.exception_event.clear()

    def close(self):
        for worker in self.workers:
            worker.stop()
        for worker in self.workers:
            worker.join()

def split_string(text, chars_per_string):
    """
    Splits one string into multiple strings, with a maximum amount of `chars_per_string` characters per string.
    This is very useful for splitting one giant message into multiples.

    :param text: The text to split
    :param chars_per_string: The number of characters per line the text is split into.
    :return: The splitted text as a list of strings.
    """
    return [text[i:i + chars_per_string] for i in range(0, len(text), chars_per_string)]