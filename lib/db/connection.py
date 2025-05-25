import psycopg2
from psycopg2.extras import RealDictCursor
def get_connection():
 conn = psycopg2.connect(
"dbname=articles_challenge user=your_username password=your_password"
)
 conn.cursor_factory = RealDictCursor # This enables column access by name
 return conn