import threading
from functools import wraps

import pytest


class MyThread(threading.Thread):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.exc = None

    def run(self):
        self.exc = None

        try:
            super().run()
        except BaseException as e:
            self.exc = e

    def join(self, timeout_: float | None = None):
        threading.Thread.join(self, timeout_)
        # Since join() returns in caller thread
        # we re-raise the caught exception
        # if any was caught
        if self.exc:
            raise self.exc


def timeout(timer):
    def decorator(func):
        @wraps(func)
        def new_func(*args):
            # Create a thread to run the test
            test_thread = MyThread(target=lambda: func(*args))
            test_thread.daemon = True
            test_thread.start()

            # Wait for the thread to complete with a timeout
            test_thread.join(timeout_=timer)

            if test_thread.is_alive():
                pytest.fail(f"Test exceeded time limit of {timer} seconds")

        return new_func

    return decorator
