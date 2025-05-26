from lib.db.connection import get_connection
from lib.db.seed import seed_db

def setup_db():
    conn = get_connection()
    cursor = conn.cursor()
    
    with open("lib/db/schema.sql") as f:
        cursor.executescript(f.read())
        
    conn.commit()
    conn.close()
    
    seed_db()

if __name__ == "__main__":
    setup_db()
    print("Database setup complete and seeded.")