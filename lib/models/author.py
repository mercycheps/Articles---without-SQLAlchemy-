from lib.db.connection import get_connection

class Author:
    def __init__(self, id = None, name = None):
        self.id = id
        self.name = name
        
    def save(self):
        conn = get_connection()
        cursor = conn.cursor()
        if self.id is None:
            cursor.execute(
                 "INSERT INTO authors (name) VALUES (?)",
                 (self.name,)
            )
            self.id = cursor.lastrowid
        else:
            cursor.execute(
                "UPDATE authors SET name = ? WHERE id = ?",
                (self.name, self.id)
            )
        conn.commit()
        conn.close()
    
    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        if not isinstance(value, str) or not (1 <= len(value) <= 50):
            raise ValueError("Name must be a string between 1 and 50 characters.")
        self._name = value
            
    @classmethod
    def find_by_id(cls,author_id):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT * FROM authors WHERE id = ?",
            (author_id,)
        )
        row = cursor.fetchone()
        conn.close()
        if row:
            
            return cls(id = row['id'], name = row['name'])
        return None
    
    @classmethod
    def find_by_name(cls, name):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT * FROM authors WHERE name = ?",
            (name,)
        )
        row = cursor.fetchone()
        conn.close()
        
        if row:
            return cls(id = row['id'], name = row['name'])
        return None
    
    def articles(self):
        from lib.models.article import Article
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT * FROM articles WHERE author_id = ?",
            (self.id,)
        )
        articles = cursor.fetchall()
        conn.close()
        return [Article(id=article['id'], title=article['title'], author_id=article['author_id'], magazine_id=article['magazine_id']) for article in articles]

    def magazines(self):
        from lib.models.magazine import Magazine
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT DISTINCT m.* FROM magazines m
            JOIN articles a ON m.id = a.magazine_id
            WHERE a.author_id = ?
        """, (self.id,))
        magazines_data = cursor.fetchall()
        conn.close()
        return [Magazine(id=m['id'], name=m['name'], category=m['category']) for m in magazines_data]

    def add_article(self, magazine, title):
        from lib.models.article import Article
        article = Article(title=title, author_id=self.id, magazine_id=magazine.id)
        article.save()
        return article

    def topic_areas(self):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT DISTINCT m.category FROM magazines m
            JOIN articles a ON m.id = a.magazine_id
            WHERE a.author_id = ?
        """, (self.id,))
        topic_areas = [row['category'] for row in cursor.fetchall()]
        conn.close()
        return topic_areas

    @classmethod
    def get_all(cls):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM authors")
        authors_data = cursor.fetchall()
        conn.close()
        return [cls(id=row['id'], name=row['name']) for row in authors_data]