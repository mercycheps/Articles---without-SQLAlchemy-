import psycopg2
from psycopg2.extras import RealDictCursor

def get_connection():
    conn = psycopg2.connect(
        dbname="articles_challenge",
        user="planet",
        password="postgres",
        host="localhost",
        port="5432",
        cursor_factory=RealDictCursor
    )
    return conn
