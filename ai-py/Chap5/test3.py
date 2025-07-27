import time
from functools import wraps


def log_args(func):
    def wrapper(*args, **kwargs):
        print(f"Arguments: {args}, {kwargs}")
        return func(*args, **kwargs)

    return wrapper


def log_time(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        print(f"Execute time: {time.time()}")
        func(*args, **kwargs)

    return wrapper


@log_args
@log_time
def a(p):
    print("a")


a(3)
