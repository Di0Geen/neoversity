from collections import deque


def is_palindrome(text: str) -> bool:
    """Перевіряє, чи є рядок паліндромом."""

    # Робимо рядок зручним для перевірки:
    # переводимо в нижній регістр і прибираємо пробіли.
    normalized_text = "".join(text.lower().split())

    # Записуємо символи у двосторонню чергу.
    chars = deque(normalized_text)

    # Порівнюємо символи зліва і справа.
    while len(chars) > 1:
        if chars.popleft() != chars.pop():
            return False

    return True


def main() -> None:
    """Головна функція програми."""

    samples = [
        "Привіт світ",
        "Гарні рози в Гришка",
        "Море пляж",
        "А на чемпіонаті світу",
        "Око",
    ]

    for sample in samples:
        result = is_palindrome(sample)

        if result:
            print(f'"{sample}" -> паліндром')
        else:
            print(f'"{sample}" -> не паліндром')


if __name__ == "__main__":
    main()