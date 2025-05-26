import pytest
from lib.models.article import Article
from lib.models.author import Author
from lib.models.magazine import Magazine
from lib.db.connection import get_connection

@pytest.fixture(autouse=True)
def setup_and_teardown_db():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DROP TABLE IF EXISTS articles")
    cursor.execute("DROP TABLE IF EXISTS authors")
    cursor.execute("DROP TABLE IF EXISTS magazines")
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS authors (
            id INTEGER PRIMARY KEY,
            name VARCHAR(255) NOT NULL
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS magazines (
            id INTEGER PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            category VARCHAR(255) NOT NULL
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS articles (
            id INTEGER PRIMARY KEY,
            title VARCHAR(255) NOT NULL,
            author_id INTEGER,
            magazine_id INTEGER,
            FOREIGN KEY (author_id) REFERENCES authors(id),
            FOREIGN KEY (magazine_id) REFERENCES magazines(id)
        )
    """)
    conn.commit()
    conn.close()
    yield
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DROP TABLE IF EXISTS articles")
    cursor.execute("DROP TABLE IF EXISTS authors")
    cursor.execute("DROP TABLE IF EXISTS magazines")
    conn.commit()
    conn.close()

def test_article_creation():
    article = Article(title="New Article", author_id=1, magazine_id=1)
    assert article.title == "New Article"
    assert article.author_id == 1
    assert article.magazine_id == 1

def test_article_save():
    author = Author(name="Test Author")
    author.save()
    magazine = Magazine(name="Test Magazine", category="Test Category")
    magazine.save()
    article = Article(title="Saved Article", author_id=author.id, magazine_id=magazine.id)
    article.save()
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM articles WHERE title = 'Saved Article'")
    result = cursor.fetchone()
    conn.close()
    assert result is not None
    assert result['title'] == "Saved Article"
    assert article.id is not None

def test_article_find_by_id():
    author = Author(name="Author A")
    author.save()
    magazine = Magazine(name="Magazine A", category="Category A")
    magazine.save()
    article = Article(title="Find Me", author_id=author.id, magazine_id=magazine.id)
    article.save()
    found_article = Article.find_by_id(article.id)
    assert found_article.title == "Find Me"

def test_article_find_by_title():
    author = Author(name="Author B")
    author.save()
    magazine = Magazine(name="Magazine B", category="Category B")
    magazine.save()
    article = Article(title="Unique Title", author_id=author.id, magazine_id=magazine.id)
    article.save()
    found_article = Article.find_by_title("Unique Title")
    assert found_article.title == "Unique Title"

def test_article_author():
    author = Author(name="Author C")
    author.save()
    magazine = Magazine(name="Magazine C", category="Category C")
    magazine.save()
    article = Article(title="Article by Author C", author_id=author.id, magazine_id=magazine.id)
    article.save()
    retrieved_author = article.author()
    assert retrieved_author.name == "Author C"

def test_article_magazine():
    author = Author(name="Author D")
    author.save()
    magazine = Magazine(name="Magazine D", category="Category D")
    magazine.save()
    article = Article(title="Article in Magazine D", author_id=author.id, magazine_id=magazine.id)
    article.save()
    retrieved_magazine = article.magazine()
    assert retrieved_magazine.name == "Magazine D"