ITEMS = {
    "red-bull": {"cost": 55, "calories": 300},
    "chips": {"cost": 70, "calories": 250},
    "apple": {"cost": 50, "calories": 200},
    "oatmeal": {"cost": 30, "calories": 100},
    "spaghetti": {"cost": 45, "calories": 220},
    "cheddar": {"cost": 150, "calories": 350},
}


def greedy_algorithm(items, budget):
    """Обирає продукти за співвідношенням калорій до вартості."""
    sorted_items = sorted(
        items,
        key=lambda name: items[name]["calories"] / items[name]["cost"],
        reverse=True,
    )

    chosen_items = []
    total_cost = 0
    total_calories = 0

    for name in sorted_items:
        cost = items[name]["cost"]

        if total_cost + cost <= budget:
            chosen_items.append(name)
            total_cost += cost
            total_calories += items[name]["calories"]

    return chosen_items, total_cost, total_calories


def dynamic_programming(items, budget):
    """Знаходить оптимальний набір продуктів методом ДП."""
    table = [(0, []) for _ in range(budget + 1)]

    for name, data in items.items():
        cost = data["cost"]
        calories = data["calories"]

        for current_budget in range(budget, cost - 1, -1):
            previous_calories, previous_items = table[
                current_budget - cost
            ]

            candidate = previous_calories + calories

            if candidate > table[current_budget][0]:
                table[current_budget] = (
                    candidate,
                    previous_items + [name],
                )

    total_calories, chosen_items = table[budget]

    total_cost = sum(
        items[name]["cost"]
        for name in chosen_items
    )

    return chosen_items, total_cost, total_calories


def print_result(algorithm_name, result):
    """Виводить результат роботи алгоритму."""
    chosen_items, total_cost, total_calories = result

    print(f"\n{algorithm_name}:")
    print(f"Обрані продукти: {chosen_items}")
    print(f"Загальна вартість: {total_cost}")
    print(f"Загальна калорійність: {total_calories}")


def main():
    budget = 1000

    print(f"Бюджет: {budget}")

    greedy_result = greedy_algorithm(
        ITEMS,
        budget,
    )

    dynamic_result = dynamic_programming(
        ITEMS,
        budget,
    )

    print_result(
        "Жадібний алгоритм",
        greedy_result,
    )

    print_result(
        "Динамічне програмування",
        dynamic_result,
    )


if __name__ == "__main__":
    main()