from lib.models.author import Author
from lib.models.magazine import Magazine
from lib.models.article import Article
from lib.db.connection import get_connection

def run_queries():
    conn = get_connection()
    cursor = conn.cursor()

    print("--- Authors ---")
    authors = cursor.execute("SELECT * FROM authors").fetchall()
    for author_data in authors:
        author = Author(id=author_data['id'], name=author_data['name'])
        print(f"Author: {author.name}")
        print(f"  Articles: {[a.title for a in author.articles()]}")
        print(f"  Magazines: {[m.name for m in author.magazines()]}")
        print(f"  Topic Areas: {author.topic_areas()}")
    print("\n")

    print("--- Magazines ---")
    magazines = cursor.execute("SELECT * FROM magazines").fetchall()
    for magazine_data in magazines:
        magazine = Magazine(id=magazine_data['id'], name=magazine_data['name'], category=magazine_data['category'])
        print(f"Magazine: {magazine.name} ({magazine.category})")
        print(f"  Articles: {[a.title for a in magazine.articles()]}")
        print(f"  Contributors: {[c.name for c in magazine.contributors()]}")
        print(f"  Article Titles: {magazine.article_titles()}")
        print(f"  Contributing Authors (more than 2 articles): {[a.name for a in magazine.contributing_authors()]}")
    print("\n")

    print("--- Articles ---")
    articles = cursor.execute("SELECT * FROM articles").fetchall()
    for article_data in articles:
        article = Article(id=article_data['id'], title=article_data['title'], author_id=article_data['author_id'], magazine_id=article_data['magazine_id'])
        print(f"Article: {article.title}")
        print(f"  Author: {article.author().name}")
        print(f"  Magazine: {article.magazine().name}")
    print("\n")

    print("--- Additional Queries ---")
    # Find magazines with articles by at least 2 different authors
    cursor.execute("""
        SELECT m.name
        FROM magazines m
        JOIN articles a ON m.id = a.magazine_id
        GROUP BY m.id, m.name
        HAVING COUNT(DISTINCT a.author_id) >= 2
    """)
    magazines_with_multiple_authors = [row['name'] for row in cursor.fetchall()]
    print(f"Magazines with articles by at least 2 different authors: {magazines_with_multiple_authors}")

    # Count the number of articles in each magazine
    cursor.execute("""
        SELECT m.name, COUNT(a.id) AS article_count
        FROM magazines m
        LEFT JOIN articles a ON m.id = a.magazine_id
        GROUP BY m.name
    """)
    article_counts_by_magazine = cursor.fetchall()
    print("Article counts by magazine:")
    for row in article_counts_by_magazine:
        print(f"  {row['name']}: {row['article_count']}")

    # Find the author who has written the most articles
    cursor.execute("""
        SELECT au.name, COUNT(ar.id) AS article_count
        FROM authors au
        JOIN articles ar ON au.id = ar.author_id
        GROUP BY au.name
        ORDER BY article_count DESC
        LIMIT 1
    """)
    top_author = cursor.fetchone()
    if top_author:
        print(f"Author with the most articles: {top_author['name']} ({top_author['article_count']} articles)")
    else:
        print("No authors found with articles.")

    conn.close()

if __name__ == "__main__":
    run_queries()