import contextlib

def start_database():
    pass
def stop_database():
    pass
def db_backup():
    pass

@contextlib.contextmanager
def db_handler():
    try:
        stop_database()
        yield
    finally:
        start_database()

with db_handler():
    db_backup()
