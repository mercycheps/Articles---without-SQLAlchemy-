import sys
from lib.models.author import Author
from lib.models.magazine import Magazine
from lib.models.article import Article
from lib.db.connection import get_connection

def display_author(author):
    print(f"ID: {author.id}, Name: {author.name}")
    print(f"  Articles: {[a.title for a in author.articles()]}")
    print(f"  Magazines: {[m.name for m in author.magazines()]}")
    print(f"  Topic Areas: {author.topic_areas()}")

def display_magazine(magazine):
    print(f"ID: {magazine.id}, Name: {magazine.name}, Category: {magazine.category}")
    print(f"  Articles: {[a.title for a in magazine.articles()]}")
    print(f"  Contributors: {[c.name for c in magazine.contributors()]}")
    print(f"  Article Titles: {magazine.article_titles()}")
    print(f"  Contributing Authors (more than 2 articles): {[a.name for a in magazine.contributing_authors()]}")

def display_article(article):
    print(f"ID: {article.id}, Title: {article.title}")
    print(f"  Author: {article.author().name}")
    print(f"  Magazine: {article.magazine().name}")

def main_menu():
    while True:
        print("\n--- Database CLI Tool ---")
        print("1. Query Authors")
        print("2. Query Magazines")
        print("3. Query Articles")
        print("4. Find Top Publisher Magazine")
        print("5. Exit")

        choice = input("Enter your choice: ")

        if choice == '1':
            query_authors_menu()
        elif choice == '2':
            query_magazines_menu()
        elif choice == '3':
            query_articles_menu()
        elif choice == '4':
            top_publisher = Magazine.top_publisher()
            if top_publisher:
                print("\n--- Top Publisher Magazine ---")
                display_magazine(top_publisher)
            else:
                print("No top publisher found.")
        elif choice == '5':
            print("Exiting CLI tool. Goodbye!")
            sys.exit(0)
        else:
            print("Invalid choice. Please try again.")

def query_authors_menu():
    while True:
        print("\n--- Query Authors ---")
        print("1. List all authors")
        print("2. Find author by ID")
        print("3. Find author by name")
        print("4. Back to Main Menu")

        choice = input("Enter your choice: ")

        if choice == '1':
            authors = Author.get_all()
            if authors:
                for author in authors:
                    display_author(author)
            else:
                print("No authors found.")
        elif choice == '2':
            try:
                author_id = int(input("Enter author ID: "))
                author = Author.find_by_id(author_id)
                if author:
                    display_author(author)
                else:
                    print(f"Author with ID {author_id} not found.")
            except ValueError:
                print("Invalid ID. Please enter a number.")
        elif choice == '3':
            author_name = input("Enter author name: ")
            author = Author.find_by_name(author_name)
            if author:
                display_author(author)
            else:
                print(f"Author with name '{author_name}' not found.")
        elif choice == '4':
            break
        else:
            print("Invalid choice. Please try again.")

def query_magazines_menu():
    while True:
        print("\n--- Query Magazines ---")
        print("1. List all magazines")
        print("2. Find magazine by ID")
        print("3. Find magazine by name")
        print("4. Find magazines by category")
        print("5. Back to Main Menu")

        choice = input("Enter your choice: ")

        if choice == '1':
            magazines = Magazine.get_all()
            if magazines:
                for magazine in magazines:
                    display_magazine(magazine)
            else:
                print("No magazines found.")
        elif choice == '2':
            try:
                magazine_id = int(input("Enter magazine ID: "))
                magazine = Magazine.find_by_id(magazine_id)
                if magazine:
                    display_magazine(magazine)
                else:
                    print(f"Magazine with ID {magazine_id} not found.")
            except ValueError:
                print("Invalid ID. Please enter a number.")
        elif choice == '3':
            magazine_name = input("Enter magazine name: ")
            magazine = Magazine.find_by_name(magazine_name)
            if magazine:
                display_magazine(magazine)
            else:
                print(f"Magazine with name '{magazine_name}' not found.")
        elif choice == '4':
            magazine_category = input("Enter magazine category: ")
            magazines = Magazine.find_by_category(magazine_category)
            if magazines:
                for magazine in magazines:
                    display_magazine(magazine)
            else:
                print(f"No magazines found in category '{magazine_category}'.")
        elif choice == '5':
            break
        else:
            print("Invalid choice. Please try again.")

def query_articles_menu():
    while True:
        print("\n--- Query Articles ---")
        print("1. List all articles")
        print("2. Find article by ID")
        print("3. Find article by title")
        print("4. Back to Main Menu")

        choice = input("Enter your choice: ")

        if choice == '1':
            articles = Article.get_all()
            if articles:
                for article in articles:
                    display_article(article)
            else:
                print("No articles found.")
        elif choice == '2':
            try:
                article_id = int(input("Enter article ID: "))
                article = Article.find_by_id(article_id)
                if article:
                    display_article(article)
                else:
                    print(f"Article with ID {article_id} not found.")
            except ValueError:
                print("Invalid ID. Please enter a number.")
        elif choice == '3':
            article_title = input("Enter article title: ")
            article = Article.find_by_title(article_title)
            if article:
                display_article(article)
            else:
                print(f"Article with title '{article_title}' not found.")
        elif choice == '4':
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main_menu()