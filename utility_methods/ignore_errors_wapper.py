from contextlib import contextmanager


@contextmanager
def ignore_errors_wrapper():
    try:
        yield
    except Exception:
        pass
