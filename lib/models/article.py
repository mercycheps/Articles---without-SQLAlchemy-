from lib.db.connection import get_connection

class Article:
    def __init__(self, id = None, title = None, author_id = None, magazine_id = None):
        self.id = id
        self.title = title
        self.author_id = author_id
        self.magazine_id = magazine_id
    
    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, value):
        if not isinstance(value, str) or not (1 <= len(value) <= 255):
            raise ValueError("Title must be a string between 1 and 255 characters.")
        self._title = value

    @property
    def author_id(self):
        return self._author_id

    @author_id.setter
    def author_id(self, value):
        if not isinstance(value, int):
            raise ValueError("Author ID must be an integer.")
        self._author_id = value

    @property
    def magazine_id(self):
        return self._magazine_id

    @magazine_id.setter
    def magazine_id(self, value):
        if not isinstance(value, int):
            raise ValueError("Magazine ID must be an integer.")
        self._magazine_id = value

    def save(self):
        conn = get_connection()
        cursor = conn.cursor()
        if self.id is None:
            cursor.execute(
                "INSERT INTO articles (title, author_id, magazine_id) VALUES (?, ?, ?)",
                (self.title, self.author_id, self.magazine_id)
            )
            self.id = cursor.lastrowid
        else:
            cursor.execute(
                "UPDATE articles SET title=?, author_id=?, magazine_id=? WHERE id=?",
                (self.title, self.author_id, self.magazine_id, self.id)
            )
        conn.commit()
        conn.close()
   
   
    @classmethod
    def find_by_id(cls, article_id):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT * FROM articles WHERE id=?",
            (article_id,)
        )
        row = cursor.fetchone()
        conn.close()
        if row:
            return cls(id=row['id'], title=row['title'], author_id=row['author_id'], magazine_id=row['magazine_id'])
        return None
    
    @classmethod
    def find_by_title(cls, title):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT * FROM articles WHERE title=?",
            (title,)
        )
        row = cursor.fetchone()
        conn.close()
        if row:
            return cls(id=row['id'], title=row['title'], author_id=row['author_id'], magazine_id=row['magazine_id'])
        return None
    
    @classmethod
    def find_by_author(cls, author_id):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT * FROM articles WHERE author_id=?",
            (author_id,)
        )
        rows = cursor.fetchall()
        conn.close()
        return [cls(id=row['id'], title=row['title'], author_id=row['author_id'], magazine_id=row['magazine_id']) for row in rows]
    
    
    @classmethod
    def find_by_magazine(cls, magazine_id):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT * FROM articles WHERE magazine_id=?",
            (magazine_id,)
        )
        rows = cursor.fetchall()
        conn.close()
        return [cls(id=row['id'], title=row['title'], author_id=row['author_id'], magazine_id=row['magazine_id']) for row in rows]

    def author(self):
        from lib.models.author import Author
        return Author.find_by_id(self.author_id)

    def magazine(self):
        from lib.models.magazine import Magazine
        return Magazine.find_by_id(self.magazine_id)

    @classmethod
    def get_all(cls):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM articles")
        articles_data = cursor.fetchall()
        conn.close()
        return [cls(id=row['id'], title=row['title'], author_id=row['author_id'], magazine_id=row['magazine_id']) for row in articles_data]
