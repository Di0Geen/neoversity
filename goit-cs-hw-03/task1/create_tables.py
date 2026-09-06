import os

import psycopg2
from psycopg2 import Error


# Параметри підключення до PostgreSQL
DB_CONFIG = {
    "dbname": os.getenv("POSTGRES_DB", "task_manager"),
    "user": os.getenv("POSTGRES_USER", "postgres"),
    "password": os.getenv("POSTGRES_PASSWORD", "postgres"),
    "host": os.getenv("POSTGRES_HOST", "localhost"),
    "port": os.getenv("POSTGRES_PORT", "5432"),
}


# Команди для створення структури бази даних SQL
TABLES_SQL = """
DROP TABLE IF EXISTS tasks;
DROP TABLE IF EXISTS status;
DROP TABLE IF EXISTS users;

CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    fullname VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE
);

CREATE TABLE status (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) NOT NULL UNIQUE
);

CREATE TABLE tasks (
    id SERIAL PRIMARY KEY,
    title VARCHAR(100) NOT NULL,
    description TEXT,
    status_id INTEGER NOT NULL,
    user_id INTEGER NOT NULL,
    CONSTRAINT fk_task_status
        FOREIGN KEY (status_id)
        REFERENCES status(id),
    CONSTRAINT fk_task_user
        FOREIGN KEY (user_id)
        REFERENCES users(id)
        ON DELETE CASCADE
);
"""


def create_tables():
    """Створює таблиці users, status і tasks у PostgreSQL."""

    try:
        # Підєднання до бази даних
        with psycopg2.connect(**DB_CONFIG) as connection:
            with connection.cursor() as cursor:
                cursor.execute(TABLES_SQL)

        print("Таблиці users, status і tasks успішно створено.")

    except Error as error:
        print(f"Помилка під час створення таблиць: {error}")


if __name__ == "__main__":
    create_tables()