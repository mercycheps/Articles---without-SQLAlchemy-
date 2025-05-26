import pytest
from lib.models.magazine import Magazine
from lib.models.author import Author
from lib.models.article import Article
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

def test_magazine_creation():
    magazine = Magazine(name="Tech Weekly", category="Technology")
    assert magazine.name == "Tech Weekly"
    assert magazine.category == "Technology"

def test_magazine_save():
    magazine = Magazine(name="Fashion Monthly", category="Fashion")
    magazine.save()
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM magazines WHERE name = 'Fashion Monthly'")
    result = cursor.fetchone()
    conn.close()
    assert result is not None
    assert result['name'] == "Fashion Monthly"
    assert result['category'] == "Fashion"
    assert magazine.id is not None

def test_magazine_find_by_id():
    magazine = Magazine(name="Traveler", category="Travel")
    magazine.save()
    found_magazine = Magazine.find_by_id(magazine.id)
    assert found_magazine.name == "Traveler"
    assert found_magazine.category == "Travel"

def test_magazine_find_by_name():
    magazine = Magazine(name="Science Today", category="Science")
    magazine.save()
    found_magazine = Magazine.find_by_name("Science Today")
    assert found_magazine.name == "Science Today"
    assert found_magazine.category == "Science"

def test_magazine_articles():
    author = Author(name="John Doe")
    author.save()
    magazine = Magazine(name="Nature", category="Science")
    magazine.save()
    article1 = Article(title="The Wonders of Nature", author_id=author.id, magazine_id=magazine.id)
    article1.save()
    article2 = Article(title="Exploring the Amazon", author_id=author.id, magazine_id=magazine.id)
    article2.save()
    articles = magazine.articles()
    assert len(articles) == 2
    assert articles[0].title == "The Wonders of Nature"
    assert articles[1].title == "Exploring the Amazon"

def test_magazine_contributors():
    author1 = Author(name="Jane Smith")
    author1.save()
    author2 = Author(name="Peter Jones")
    author2.save()
    magazine = Magazine(name="Art Review", category="Art")
    magazine.save()
    article1 = Article(title="Modern Art Trends", author_id=author1.id, magazine_id=magazine.id)
    article1.save()
    article2 = Article(title="Impressionism Revisited", author_id=author2.id, magazine_id=magazine.id)
    article2.save()
    contributors = magazine.contributors()
    assert len(contributors) == 2
    assert contributors[0].name == "Jane Smith"
    assert contributors[1].name == "Peter Jones"

def test_magazine_article_titles():
    author = Author(name="Alice Brown")
    author.save()
    magazine = Magazine(name="Foodie", category="Cooking")
    magazine.save()
    article1 = Article(title="Best Pasta Recipes", author_id=author.id, magazine_id=magazine.id)
    article1.save()
    article2 = Article(title="Quick Desserts", author_id=author.id, magazine_id=magazine.id)
    article2.save()
    titles = magazine.article_titles()
    assert len(titles) == 2
    assert "Best Pasta Recipes" in titles
    assert "Quick Desserts" in titles

def test_magazine_contributing_authors():
    author1 = Author(name="Author A")
    author1.save()
    author2 = Author(name="Author B")
    author2.save()
    author3 = Author(name="Author C")
    author3.save()
    magazine = Magazine(name="Tech Innovate", category="Technology")
    magazine.save()

    Article(title="Article 1", author_id=author1.id, magazine_id=magazine.id).save()
    Article(title="Article 2", author_id=author1.id, magazine_id=magazine.id).save()
    Article(title="Article 3", author_id=author1.id, magazine_id=magazine.id).save()
    Article(title="Article 4", author_id=author2.id, magazine_id=magazine.id).save()
    Article(title="Article 5", author_id=author2.id, magazine_id=magazine.id).save()
    Article(title="Article 6", author_id=author3.id, magazine_id=magazine.id).save()

    contributing_authors = magazine.contributing_authors()
    assert len(contributing_authors) == 2
    assert contributing_authors[0].name == "Author A"
    assert contributing_authors[1].name == "Author B"