from __future__ import annotations

from timeit import repeat


COINS = (50, 25, 10, 5, 2, 1)


def validate_amount(amount: int) -> None:
    """Перевіряє, чи можна використовувати передану суму."""
    if not isinstance(amount, int) or isinstance(amount, bool):
        raise TypeError("Сума повинна бути цілим числом")
    if amount < 0:
        raise ValueError("Сума не може бути від'ємною")


def find_coins_greedy(amount: int) -> dict[int, int]:
    """Формує решту, послідовно обираючи найбільші монети."""
    validate_amount(amount)

    result = {}
    remainder = amount

    for coin in COINS:
        count, remainder = divmod(remainder, coin)
        if count:
            result[coin] = count

    return result


def find_min_coins(amount: int) -> dict[int, int]:
    """Знаходить мінімальну кількість монет методом динамічного програмування."""
    validate_amount(amount)

    if amount == 0:
        return {}

    min_count = [0] + [amount + 1] * amount
    last_coin = [0] * (amount + 1)

    # Знаходимо оптимальне рішення для кожної суми від 1 до amount.
    for current_amount in range(1, amount + 1):
        for coin in COINS:
            if coin > current_amount:
                continue

            candidate = min_count[current_amount - coin] + 1
            if candidate < min_count[current_amount]:
                min_count[current_amount] = candidate
                last_coin[current_amount] = coin

    # Відновлюємо набір монет за збереженими значеннями.
    result = {}
    remainder = amount

    while remainder > 0:
        coin = last_coin[remainder]
        result[coin] = result.get(coin, 0) + 1
        remainder -= coin

    return result


def measure_average_time(function, amount: int, launches: int = 5) -> float:
    """Повертає найкращий середній час одного запуску функції."""
    measurements = repeat(
        lambda: function(amount),
        repeat=3,
        number=launches,
    )
    return min(measurements) / launches


def main() -> None:
    test_amount = 113
    large_amount = 100_000

    print(f"Сума для перевірки: {test_amount}")
    print(f"Жадібний алгоритм: {find_coins_greedy(test_amount)}")
    print(f"Динамічне програмування: {find_min_coins(test_amount)}")

    greedy_time = measure_average_time(find_coins_greedy, large_amount)
    dynamic_time = measure_average_time(find_min_coins, large_amount)

    print(f"\nПорівняння для суми {large_amount}:")
    print(f"Жадібний алгоритм: {greedy_time:.9f} с")
    print(f"Динамічне програмування: {dynamic_time:.9f} с")


if __name__ == "__main__":
    main()
