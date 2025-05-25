from lib.db.connection import get_connection

def add_author_with_articles(author_name, articles_data):
    """
    Add an author and their articles in a single transaction.
    
    articles_data: list of dicts with keys 'title' and 'magazine_id'
    
    Returns True if successful, False otherwise.
    """
    
    conn = get_connection()
    try:
        with conn:
            with conn.cursor() as cursor:
                
                cursor.execute(
                    "INSERT INTO authors (name) VALUES (%s) RETURNING id;",
                    (author_name,)
                )
                author_id = cursor.fetchone()[0]

                
                for article in articles_data:
                    cursor.execute(
                        "INSERT INTO articles (title, author_id, magazine_id) VALUES (%s, %s, %s);",
                        (article['title'], author_id, article['magazine_id'])
                    )
       
        return True
    

    except Exception as e:
       
        print(f"Transaction failed: {e}")
        return False


    finally:
        conn.close()
