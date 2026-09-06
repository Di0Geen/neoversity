import os

from pymongo import MongoClient
from pymongo.errors import PyMongoError


MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")

client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)
database = client["cats_database"]
cats = database["cats"]


def print_cat(cat):
    """Виводить інформацію про кота."""

    if cat:
        print(
            f"Ім'я: {cat['name']}, "
            f"вік: {cat['age']}, "
            f"характеристики: {', '.join(cat['features'])}"
        )
    else:
        print("Кота не знайдено.")


def create_cat():
    """Додає нового кота до колекції."""

    name = input("Введіть ім'я кота: ").strip()
    age = int(input("Введіть вік кота: "))
    features = input("Введіть характеристики через кому: ").split(",")
    features = [item.strip() for item in features if item.strip()]

    cats.insert_one({"name": name, "age": age, "features": features})
    print(f"Кота {name} додано.")


def show_all_cats():
    """Виводить усіх котів із колекції."""

    all_cats = list(cats.find())

    if not all_cats:
        print("Колекція котів порожня.")
        return

    for cat in all_cats:
        print_cat(cat)


def find_cat():
    """Знаходить кота за ім'ям."""

    name = input("Введіть ім'я кота: ").strip()
    print_cat(cats.find_one({"name": name}))


def update_cat_age():
    """Оновлює вік кота за його ім'ям."""

    name = input("Введіть ім'я кота: ").strip()
    age = int(input("Введіть новий вік: "))

    result = cats.update_one({"name": name}, {"$set": {"age": age}})
    print("Вік оновлено." if result.matched_count else "Кота не знайдено.")


def add_cat_feature():
    """Додає нову характеристику коту."""

    name = input("Введіть ім'я кота: ").strip()
    feature = input("Введіть нову характеристику: ").strip()

    result = cats.update_one(
        {"name": name},
        {"$addToSet": {"features": feature}},
    )
    print(
        "Характеристику додано."
        if result.matched_count
        else "Кота не знайдено."
    )


def delete_cat():
    """Видаляє кота за ім'ям."""

    name = input("Введіть ім'я кота: ").strip()
    result = cats.delete_one({"name": name})

    print("Кота видалено." if result.deleted_count else "Кота не знайдено.")


def delete_all_cats():
    """Видаляє всі записи з колекції."""

    confirmation = input("Видалити всіх котів? (так/ні): ").lower()

    if confirmation == "так":
        result = cats.delete_many({})
        print(f"Видалено записів: {result.deleted_count}")
    else:
        print("Видалення скасовано.")


def show_menu():
    """Показує меню доступних операцій."""

    print(
        "\n1 — додати кота"
        "\n2 — показати всіх котів"
        "\n3 — знайти кота за ім'ям"
        "\n4 — оновити вік кота"
        "\n5 — додати характеристику"
        "\n6 — видалити кота"
        "\n7 — видалити всіх котів"
        "\n0 — завершити роботу"
    )


def main():
    actions = {
        "1": create_cat,
        "2": show_all_cats,
        "3": find_cat,
        "4": update_cat_age,
        "5": add_cat_feature,
        "6": delete_cat,
        "7": delete_all_cats,
    }

    try:
        client.admin.command("ping")
        print("Підключення до MongoDB успішне.")

        while True:
            show_menu()
            choice = input("Оберіть дію: ").strip()

            if choice == "0":
                print("Роботу завершено.")
                break

            action = actions.get(choice)

            if not action:
                print("Оберіть пункт від 0 до 7.")
                continue

            try:
                action()
            except ValueError:
                print("Вік потрібно вводити цілим числом.")

    except PyMongoError as error:
        print(f"Помилка MongoDB: {error}")

    finally:
        client.close()


if __name__ == "__main__":
    main()