def stop_database():
    print("stopping database")

def start_database():
    print("starting database")

class DBHandler:
    def __enter__(self):
        stop_database()
        return self
    
    def __exit__(self, exc_type, exc_value, traceback):
        start_database()

def db_backup():
    run("pg_dump database")

def main():
    with DBHandler():
        db_backup()

