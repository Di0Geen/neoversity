from __future__ import annotations

import random
from collections.abc import Callable


def function(x: float) -> float:
    """Функція, визначений інтеграл якої потрібно обчислити."""
    return (x + 1) ** 2


def monte_carlo_integral(
    func: Callable[[float], float],
    lower_bound: float,
    upper_bound: float,
    max_value: float,
    samples: int = 1_000_000,
    seed: int | None = None,
) -> float:
    """Обчислює площу під графіком методом випадкових точок."""
    if lower_bound >= upper_bound:
        raise ValueError("Нижня межа повинна бути меншою за верхню")
    if max_value <= 0:
        raise ValueError("Висота прямокутника повинна бути додатною")
    if samples <= 0:
        raise ValueError("Кількість випадкових точок повинна бути додатною")

    random_generator = random.Random(seed)
    points_under_curve = 0

    for _ in range(samples):
        x = random_generator.uniform(lower_bound, upper_bound)
        y = random_generator.uniform(0, max_value)

        if y <= func(x):
            points_under_curve += 1

    rectangle_area = (upper_bound - lower_bound) * max_value
    return rectangle_area * points_under_curve / samples


def analytical_integral(lower_bound: float, upper_bound: float) -> float:
    """Повертає точне значення інтеграла для f(x) = (x + 1)^2."""
    return ((upper_bound + 1) ** 3 - (lower_bound + 1) ** 3) / 3


def main() -> None:
    lower_bound = 0
    upper_bound = 2
    samples = 1_000_000
    max_value = function(upper_bound)

    monte_carlo_result = monte_carlo_integral(
        function,
        lower_bound,
        upper_bound,
        max_value,
        samples,
        seed=42,
    )
    analytical_result = analytical_integral(lower_bound, upper_bound)

    absolute_error = abs(monte_carlo_result - analytical_result)
    relative_error = absolute_error / abs(analytical_result) * 100

    print("Інтеграл функції f(x) = (x + 1)^2 на відрізку [0; 2]")
    print(f"Метод Монте-Карло: {monte_carlo_result:.6f}")
    print(f"Аналітичний результат: {analytical_result:.6f}")
    print(f"Абсолютна похибка: {absolute_error:.6f}")
    print(f"Відносна похибка: {relative_error:.4f}%")


if __name__ == "__main__":
    main()