import pytest
from lib.models.author import Author
from lib.models.article import Article
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

def test_author_creation():
    author = Author(name="Stephen King")
    assert author.name == "Stephen King"

def test_author_save():
    author = Author(name="J.K. Rowling")
    author.save()
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM authors WHERE name = 'J.K. Rowling'")
    result = cursor.fetchone()
    conn.close()
    assert result is not None
    assert result['name'] == "J.K. Rowling"
    assert author.id is not None

def test_author_find_by_id():
    author = Author(name="Agatha Christie")
    author.save()
    found_author = Author.find_by_id(author.id)
    assert found_author.name == "Agatha Christie"

def test_author_find_by_name():
    author = Author(name="George Orwell")
    author.save()
    found_author = Author.find_by_name("George Orwell")
    assert found_author.name == "George Orwell"

def test_author_articles():
    author = Author(name="Ernest Hemingway")
    author.save()
    magazine = Magazine(name="Literary Review", category="Literature")
    magazine.save()
    article1 = Article(title="The Old Man and the Sea", author_id=author.id, magazine_id=magazine.id)
    article1.save()
    article2 = Article(title="A Farewell to Arms", author_id=author.id, magazine_id=magazine.id)
    article2.save()
    articles = author.articles()
    assert len(articles) == 2
    assert articles[0].title == "The Old Man and the Sea"
    assert articles[1].title == "A Farewell to Arms"

def test_author_magazines():
    author = Author(name="Virginia Woolf")
    author.save()
    magazine1 = Magazine(name="Modern Fiction", category="Fiction")
    magazine1.save()
    magazine2 = Magazine(name="Literary Quarterly", category="Literature")
    magazine2.save()
    Article(title="Mrs Dalloway", author_id=author.id, magazine_id=magazine1.id).save()
    Article(title="To the Lighthouse", author_id=author.id, magazine_id=magazine2.id).save()
    magazines = author.magazines()
    assert len(magazines) == 2
    assert magazines[0].name == "Modern Fiction"
    assert magazines[1].name == "Literary Quarterly"

def test_author_add_article():
    author = Author(name="F. Scott Fitzgerald")
    author.save()
    magazine = Magazine(name="The Great American Novel", category="Fiction")
    magazine.save()
    author.add_article(magazine, "The Great Gatsby")
    articles = author.articles()
    assert len(articles) == 1
    assert articles[0].title == "The Great Gatsby"
    assert articles[0].magazine_id == magazine.id

def test_author_topic_areas():
    author = Author(name="Jane Austen")
    author.save()
    magazine1 = Magazine(name="Romance Reads", category="Romance")
    magazine1.save()
    magazine2 = Magazine(name="Classic Novels", category="Literature")
    magazine2.save()
    Article(title="Pride and Prejudice", author_id=author.id, magazine_id=magazine1.id).save()
    Article(title="Sense and Sensibility", author_id=author.id, magazine_id=magazine2.id).save()
    topic_areas = author.topic_areas()
    assert len(topic_areas) == 2
    assert "Romance" in topic_areas
    assert "Literature" in topic_areas