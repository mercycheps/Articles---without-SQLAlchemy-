from lib.db.connection import get_connection

class Magazine:
    def __init__(self, id=None, name=None, category=None):
        self.id = id
        self.name = name
        self.category = category
        
    @classmethod
    def top_publisher(cls):
        conn = get_connection()
        cursor = conn.cursor()
        query = """
            SELECT magazines.*, COUNT(articles.id) AS article_count
            FROM magazines
            JOIN articles ON articles.magazine_id = magazines.id
            GROUP BY magazines.id
            ORDER BY article_count DESC
            LIMIT 1;
        """
        cursor.execute(query)
        row = cursor.fetchone()
        conn.close()
        if row:
            return cls(id=row['id'], name=row['name'], category=row['category'])
        return None    
    
    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        if not isinstance(value, str) or not (1 <= len(value) <= 255):
            raise ValueError("Name must be a string between 1 and 255 characters.")
        self._name = value

    @property
    def category(self):
        return self._category

    @category.setter
    def category(self, value):
        if not isinstance(value, str) or not (1 <= len(value) <= 255):
            raise ValueError("Category must be a string between 1 and 255 characters.")
        self._category = value
        
    def save(self):
        conn = get_connection()
        cursor = conn.cursor()
        if self.id is None:
            cursor.execute(
                "INSERT INTO magazines (name, category) VALUES (?, ?)",
                (self.name, self.category)
            )
            self.id = cursor.lastrowid
        else:
            cursor.execute(
                "UPDATE magazines SET name=?, category=? WHERE id=?",
                (self.name, self.category, self.id)
            )
        conn.commit()
        conn.close()
        
    @classmethod
    def find_by_id(cls, mag_id):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT * FROM magazines WHERE id = ?",
            (mag_id,)
        )
        row = cursor.fetchone()
        conn.close()
        if row:
             return cls(id = row['id'], name = row['name'], category = row['category'])
        return None

    @classmethod
    def find_by_name(cls, name):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT * FROM magazines WHERE name = ?",
            (name,)
        )
        row = cursor.fetchone()
        conn.close()
        if row:
            return cls(id = row['id'], name = row['name'], category = row['category'])
        return None
    
    @classmethod
    def find_by_category(cls, category):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT * FROM magazines WHERE category=?",
            (category,)
        )
        rows = cursor.fetchall()
        conn.close()
        return [cls(id=row['id'], name=row['name'], category=row['category']) for row in rows]
    
    def articles(self):
        from lib.models.article import Article
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT * FROM articles WHERE magazine_id=?",
            (self.id,)
        )
        articles_data = cursor.fetchall()
        conn.close()
        return [Article(id=article['id'], title=article['title'], author_id=article['author_id'], magazine_id=article['magazine_id']) for article in articles_data]

    def contributors(self):
        from lib.models.author import Author
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT DISTINCT a.* FROM authors a
            JOIN articles ar ON a.id = ar.author_id
            WHERE ar.magazine_id = ?
            """,
            (self.id,)
        )
        contributors_data = cursor.fetchall()
        conn.close()
        return [Author(id=c['id'], name=c['name']) for c in contributors_data]

    def article_titles(self):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT title FROM articles WHERE magazine_id = ?",
            (self.id,)
        )
        titles = [row['title'] for row in cursor.fetchall()]
        conn.close()
        return titles

    def contributing_authors(self):
        from lib.models.author import Author
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT a.id, a.name, COUNT(ar.id) AS article_count
            FROM authors a
            JOIN articles ar ON a.id = ar.author_id
            WHERE ar.magazine_id = ?
            GROUP BY a.id, a.name
            HAVING COUNT(ar.id) >= 2
        """, (self.id,))
        authors_data = cursor.fetchall()
        conn.close()
        return [Author(id=a['id'], name=a['name']) for a in authors_data]
    @classmethod
    def count_articles_by_magazine(cls):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT m.name, COUNT(a.id) AS article_count
            FROM magazines m
            LEFT JOIN articles a ON m.id = a.magazine_id
            GROUP BY m.name
        """)
        counts = cursor.fetchall()
        conn.close()
        return counts

    @classmethod
    def top_publishing_magazines(cls):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT m.name, COUNT(a.id) AS article_count
            FROM magazines m
            JOIN articles a ON m.id = a.magazine_id
            GROUP BY m.id, m.name
            ORDER BY article_count DESC
        """)
        magazines_data = cursor.fetchall()
        conn.close()
        return magazines_data

    @classmethod
    def get_all(cls):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM magazines")
        magazines_data = cursor.fetchall()
        conn.close()
        return [cls(id=row['id'], name=row['name'], category=row['category']) for row in magazines_data]