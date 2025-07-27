import contextlib

class dbhandler_decorator(contextlib.ContextDecorator):
    def __enter__(self):
        stop_database()
        return self
    
    def __exit__(self, exc_type, exc_value, traceback):
        start_database()

#dbhandler() 装饰器
@dbhandler_decorator()
def db_backup():
    pass