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
                 "INSERT INTO authors (name) VALUES (%s) RETURNING id",
            )
            self.id = cursor.fetchone()[0]
        else:
            cursor.execute(
                "UPDATE authors SET name = %s WHERE id = %s",
                (self.name, self.id)
            )
            conn.commit()
            conn.close()
            
    @classmethod
    def find_by_id(cls,author_id):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT * FROM authors WHERE id = %s",
            (author_id,)
        )
        row = cursor.fetchone()
        conn.close()
        if row:
            
            return cls(id = row[0], name = row[1])
        return None 
    
    @classmethod
    def find_by_id(cls, author_id):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT * FROM authors WHERE id = %s",
            (author_id,)
        )
        row = cursor.fetchone()
        conn.close()
        if row:
            return cls(id = row[0], name = row[1])
        return None
    
    @classmethod
    def find_by_name(cls, name):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT * FROM authors WHERE name = %s",
            (name,)
        )
        row = cursor.fetchone()
        conn.close()
        
        if row:
            return cls(id = row[0], name = row[1])
        return None
    
    def articles(self):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT * FROM articles WHERE author_id = %s",
            (self.id,)
        )
        articles = cursor.fetchall()
        conn.close()
        return articles