from lib.db.connection import get_connection
from lib.models.author import Author
from lib.models.magazine import Magazine

class Article:
    def __init__(self, id = None, title = None, author_id = None, magazine_id = None):
        self.id = id
        self.title = title
        self.author_id = author_id
        self.magazine_id = magazine_id

    def save(self):
        conn = get_connection()
        cursor = conn.cursor()
        if self.id is None:
            cursor.execute(
                "INSERT INTO articles (title, author_id, magazine_id) VALUES (%s, %s, %s) RETURNING id",
                (self.title, self.author_id, self.magazine_id)
            )
            self.id = cursor.fetchone()[0]
        else:
            cursor.execute(
                "UPDATE articles SET title=%s, author_id=%s, magazine_id=%s WHERE id=%s",
                (self.title, self.author_id, self.magazine_id, self.id)
            )
        conn.commit()
        conn.close()
   
   
    @classmethod
    def find_by_id(cls, article_id):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT * FROM articles WHERE id=%s",
            (article_id,)
        )
        row = cursor.fetchone()
        conn.close()
        if row:
            return cls(id=row[0], title=row[1], author_id=row[2], magazine_id=row[3])
        return None
    
    @classmethod
    def find_by_title(cls, title):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT * FROM articles WHERE title=%s",
            (title,)
        )
        rows = cursor.fetchall()
        conn.close()
        return [cls(id=row[0], title=row[1], author_id=row[2], magazine_id=row[3]) for row in rows]
    
    @classmethod
    def find_by_author(cls, author_id):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT * FROM articles WHERE author_id=%s",
            (author_id,)
        )
        rows = cursor.fetchall()
        conn.close()
        return [cls(id=row[0], title=row[1], author_id=row[2], magazine_id=row[3]) for row in rows]
    
    
    @classmethod
    def find_by_magazine(cls, magazine_id):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT * FROM articles WHERE magazine_id=%s",
            (magazine_id,)
        )
        rows = cursor.fetchall()
        conn.close()
        return [cls(id=row[0], title=row[1], author_id=row[2], magazine_id=row[3]) for row in rows]

    def author(self):
        return Author.find_by_id(self.author_id)

    def magazine(self):
        return Magazine.find_by_id(self.magazine_id)