 Object Relations Code Challenge - Articles

This project models the relationships between Authors, Articles, and Magazines, with data persisted in a SQLite database.

Problem Statement

The core relationships are:
- An `Author` can write many `Articles`.
- A `Magazine` can publish many `Articles`.
- An `Article` belongs to both an `Author` and a `Magazine`.
- The `Author`-`Magazine` relationship is many-to-many.

Setup Instructions

1.  Clone the repository (if not already cloned):**
    ```bash
    git clone <repository_url>
    cd Articles---without-SQLAlchemy-
    ```

2.  Create and activate a virtual environment:**
    ```bash
    python3 -m venv env
    source env/bin/activate
    ```

3.  nstall dependencies:
    ```bash
    pip install pytest
    ```

4.  Database Setup:
    The project uses SQLite. The database schema is defined in `lib/db/schema.sql`, and initial data is seeded via `lib/db/seed.py`.
    To set up the database and populate it with sample data, run:
    ```bash
    PYTHONPATH=. python3 scripts/setup_db.py
    ```

 Project Structure

```
code-challenge/
├── lib/ # Main code directory
│ ├── models/ # Model classes
│ │ ├── __init__.py
│ │ ├── author.py # Author class with SQL methods
│ │ ├── article.py # Article class with SQL methods
│ │ └── magazine.py # Magazine class with SQL methods
│ ├── db/ # Database components
│ │ ├── __init__.py
│ │ ├── connection.py # Database connection setup (SQLite)
│ │ ├── seed.py # Seed data for testing
│ │ └── schema.sql # SQL schema definitions
│ ├── controllers/ # Optional: Business logic
│ │ └── __init__.py
│ └── __init__.py
├── tests/ # Test directory
│ ├── __init__.py
│ ├── test_author.py # Tests for Author class
│ ├── test_article.py # Tests for Article class
│ └── test_magazine.py # Tests for Magazine class
├── scripts/ # Helper scripts
│ ├── setup_db.py # Script to set up the database and seed data
│ └── run_queries.py # Script to run example queries
└── README.md # Project documentation
```

 Running Tests

To run the unit tests and verify the implementation, use `pytest`:

```bash
PYTHONPATH=. python3 -m pytest
```

## Running Example Queries

To see the implemented SQL query methods and relationships in action, run the `run_queries.py` script:

```bash
PYTHONPATH=. python3 scripts/run_queries.py
```

## Running the CLI Tool

An interactive command-line interface (CLI) tool has been implemented to allow users to query the database.

```bash
PYTHONPATH=. python3 scripts/cli.py
```

## Database Indexes

Database indexes have been added to `lib/db/schema.sql` to improve query performance on frequently accessed columns such as `articles.magazine_id`, `articles.author_id`, `magazines.name`, `magazines.category`, and `authors.name`.