from lib.db.connection import get_connection

class Magazine:
    def __init__(self, id=None, name=None, category=None):
        self.id = id
        self.name = name
        self.category = category
        
    def save(self):
        conn = get_connection()
        cursor = conn.cursor()
        if self.id is None:
            cursor.execute(
                "INSERT INTO magazines (name, category) VALUES (%s, %s) RETURNING id",
                (self.name, self.category)
            )
            self.id = cursor.fetchone()[0]
        else:
            cursor.execute(
                "UPDATE magazines SET name=%s, category=%s WHERE id=%s",
                (self.name, self.category, self.id)
            )
        conn.commit()
        conn.close() 
        
    @classmethod
    def find_by_id(cls, mag_id):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT * FROM magazines WHERE id = %s",
            (mag_id,)
        )
        row = cursor.fetchone()
        conn.close()
        if row:
             return cls(id = row[0], name = row[1], category = row[2])
        return None

    @classmethod
    def find_by_name(cls, name):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT * FROM magazines WHERE name = %s",
            (name,)
        )
        row = cursor.fetchone()
        conn.close()
        if row:
            return cls(id = row[0], name = row[1], category = row[2])
        return None
    
    @classmethod
    def find_by_category(cls, category):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT * FROM magazines WHERE category=%s",
            (category,)
        )
        rows = cursor.fetchall()
        conn.close()
        return [cls(id=row[0], name=row[1], category=row[2]) for row in rows]
    
    def articles(self):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT * FROM articles WHERE magazine_id=%s",
            (self.id,)
        )
        articles = cursor.fetchall()
        conn.close()
        return articles

    def contributors(self):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT DISTINCT a.* FROM authors a
            JOIN articles ar ON a.id = ar.author_id
            WHERE ar.magazine_id = %s
            """,
            (self.id,)
        )
        contributors = cursor.fetchall()
        conn.close()
        return contributors

    def article_titles(self):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT title FROM articles WHERE magazine_id = %s",
            (self.id,)
        )
        titles = [row[0] for row in cursor.fetchall()]
        conn.close()
        return titles
    