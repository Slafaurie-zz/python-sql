import os
from contextlib import contextmanager
from psycopg2.pool import SimpleConnectionPool
from dotenv import load_dotenv

db_url = input('Enter a custom URL to DB or leave blank for default: ')

if not db_url:
    load_dotenv()
    db_url = os.environ["DATABASE_URL"]


pool = SimpleConnectionPool(minconn = 1, maxconn= 10, dsn = db_url)


@contextmanager
def get_connection():
    connection = pool.getconn()
    try:
        
        yield connection

    finally:
        pool.putconn(connection)
