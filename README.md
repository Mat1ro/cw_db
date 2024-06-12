# Coursework db

This is a description of the project.

## Dependencies

- Python 3.11
- PostgreSQL
- poetry

## Installation

First, clone the repository:

```bash
git clone https://github.com/mat1ro/coursework_db.git
```

Install dependencies using poetry:

```
poetry install
```

## Configuration

Update the database connection string in db_manager.py with your PostgreSQL database credentials:

```
f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{db_name}"
```

## For starting project you should run 'main.py' file