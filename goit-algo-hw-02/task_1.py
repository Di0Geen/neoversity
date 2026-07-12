from dataclasses import dataclass
from queue import Queue
from itertools import count
import random


@dataclass
class Request:
    """Клас для збереження даних про одну заявку."""

    request_id: int
    customer_name: str
    issue: str


# Черга, у якій будуть зберігатися всі заявки
request_queue = Queue()

# Лічильник для створення унікального номера заявки
request_counter = count(1)


CUSTOMERS = [
    "Анна",
    "Богдан",
    "Ірина",
    "Максим",
    "Олена",
    "Тарас",
]


ISSUES = [
    "Скидання пароля",
    "Встановлення програмного забезпечення",
    "Проблема з інтернетом",
    "Налаштування принтера",
    "Відновлення облікового запису",
    "Діагностика пристрою",
]


def generate_request() -> None:
    """Створює нову заявку та додає її до черги."""

    new_request = Request(
        request_id=next(request_counter),
        customer_name=random.choice(CUSTOMERS),
        issue=random.choice(ISSUES),
    )

    request_queue.put(new_request)

    print(
        f"Створено заявку №{new_request.request_id}: "
        f"{new_request.customer_name} — {new_request.issue}"
    )
    print("Заявку додано до черги.")


def process_request() -> None:
    """Дістає заявку з черги та імітує її обробку."""

    if not request_queue.empty():
        current_request = request_queue.get()

        print(
            f"Обробляється заявка №{current_request.request_id}: "
            f"{current_request.customer_name} — {current_request.issue}"
        )
        print("Заявку успішно оброблено.")

        request_queue.task_done()
    else:
        print("Черга порожня. Немає заявок для обробки.")


def main() -> None:
    """Головна функція програми для демонстрації роботи черги."""

    print("Система обробки заявок сервісного центру запущена.")

    while True:
        print("\nОберіть дію:")
        print("1 - Створити нову заявку")
        print("2 - Обробити заявку")
        print("3 - Створити та одразу обробити заявку")
        print("4 - Вийти з програми")

        user_choice = input("Ваш вибір: ")

        if user_choice == "1":
            generate_request()
        elif user_choice == "2":
            process_request()
        elif user_choice == "3":
            generate_request()
            process_request()
        elif user_choice == "4":
            print("Програму завершено.")
            break
        else:
            print("Невірний вибір. Спробуйте ще раз.")


if __name__ == "__main__":
    main()