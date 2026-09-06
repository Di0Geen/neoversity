import os

import psycopg2
from faker import Faker
from psycopg2 import Error


DB_CONFIG = {
    "dbname": os.getenv("POSTGRES_DB", "task_manager"),
    "user": os.getenv("POSTGRES_USER", "postgres"),
    "password": os.getenv("POSTGRES_PASSWORD", "postgres"),
    "host": os.getenv("POSTGRES_HOST", "localhost"),
    "port": os.getenv("POSTGRES_PORT", "5432"),
}

STATUSES = ["new", "in progress", "completed"]

TASK_TITLES = [
    "Підготувати щотижневий звіт",
    "Перевірити базу даних",
    "Оновити документацію проєкту",
    "Протестувати застосунок",
    "Виправити знайдені помилки",
    "Перевірити роботу сервера",
    "Оновити залежності проєкту",
    "Налаштувати резервне копіювання",
    "Підготувати презентацію",
    "Провести командну зустріч",
]

TASK_DESCRIPTIONS = [
    "Зібрати результати роботи та оформити звіт.",
    "Перевірити правильність збережених даних.",
    "Додати до документації актуальну інформацію.",
    "Перевірити основні функції застосунку.",
    "Знайти причину помилки та виправити її.",
    "Перевірити доступність сервера і журнал подій.",
    "Встановити та протестувати нові залежності.",
    "Створити резервну копію важливих даних.",
    "Підготувати матеріали для демонстрації проєкту.",
    "Обговорити з командою поточні завдання.",
]

fake = Faker("uk_UA")


def seed_database():
    """Заповнює таблиці тестовими даними."""

    try:
        with psycopg2.connect(**DB_CONFIG) as connection:
            with connection.cursor() as cursor:
                # Очищає таблиці перед повторним запуском
                cursor.execute(
                    "TRUNCATE tasks, status, users "
                    "RESTART IDENTITY CASCADE;"
                )

                cursor.executemany(
                    "INSERT INTO status (name) VALUES (%s);",
                    [(name,) for name in STATUSES],
                )

                users = []
                for number in range(1, 11):
                    domain = "example.com" if number <= 5 else "mail.com"
                    email = f"{fake.unique.user_name()}@{domain}"

                    users.append((fake.name()[:100], email[:100]))

                cursor.executemany(
                    """
                    INSERT INTO users (fullname, email)
                    VALUES (%s, %s);
                    """,
                    users,
                )

                cursor.execute("SELECT id FROM users ORDER BY id;")
                user_ids = [row[0] for row in cursor.fetchall()]

                cursor.execute("SELECT id FROM status ORDER BY id;")
                status_ids = [row[0] for row in cursor.fetchall()]

                tasks = []

                for number in range(30):
                    title = f"{fake.random_element(TASK_TITLES)} №{number + 1}"

                    description = (
                        None
                        if number % 5 == 0
                        else fake.random_element(TASK_DESCRIPTIONS)
                    )

                    tasks.append(
                        (
                            title,
                            description,
                            status_ids[number % len(status_ids)],
                            user_ids[number % len(user_ids[:-2])],
                        )
                    )

                cursor.executemany(
                    """
                    INSERT INTO tasks
                        (title, description, status_id, user_id)
                    VALUES (%s, %s, %s, %s);
                    """,
                    tasks,
                )

        print("Базу успішно заповнено: 3 статуси, 10 користувачів, 30 завдань.")

    except Error as error:
        print(f"Помилка PostgreSQL: {error}")


if __name__ == "__main__":
    seed_database()