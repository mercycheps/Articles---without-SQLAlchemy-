from lib.db.connection import get_connection
from lib.models.author import Author
from lib.models.magazine import Magazine
from lib.models.article import Article

def seed_db():
    conn = get_connection()
    cursor = conn.cursor()

    # Clear existing data
    cursor.execute("DELETE FROM articles")
    cursor.execute("DELETE FROM authors")
    cursor.execute("DELETE FROM magazines")
    conn.commit()

    # Create authors
    author1 = Author(name="John Doe")
    author1.save()
    author2 = Author(name="Jane Smith")
    author2.save()

    # Create magazines
    magazine1 = Magazine(name="Tech Weekly", category="Technology")
    magazine1.save()
    magazine2 = Magazine(name="Fashion Monthly", category="Fashion")
    magazine2.save()
    magazine3 = Magazine(name="Science Today", category="Science")
    magazine3.save()

    # Create articles
    article1 = Article(title="The Future of AI", author_id=author1.id, magazine_id=magazine1.id)
    article1.save()
    article2 = Article(title="Sustainable Fashion Trends", author_id=author2.id, magazine_id=magazine2.id)
    article2.save()
    article3 = Article(title="Quantum Computing Explained", author_id=author1.id, magazine_id=magazine3.id)
    article3.save()
    article4 = Article(title="AI in Healthcare", author_id=author1.id, magazine_id=magazine1.id)
    article4.save()
    article5 = Article(title="New Discoveries in Space", author_id=author2.id, magazine_id=magazine3.id)
    article5.save()

    conn.close()
    print("Database seeded successfully!")

if __name__ == "__main__":
    seed_db()