from lib.db.connection import get_connection

def run_schema():
    conn = get_connection()
    cursor = conn.cursor()

    with open('lib/db/schema.sql', 'r') as f:
        schema_sql = f.read()

    cursor.execute(schema_sql)
    conn.commit()
    conn.close()
    print("✅ Schema applied successfully.")

if __name__ == '__main__':
    run_schema()
