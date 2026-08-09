import random
from collections import Counter

import matplotlib.pyplot as plt


ROLLS = 500_000

ANALYTICAL = {
    value: (6 - abs(7 - value)) / 36
    for value in range(2, 13)
}


def simulate_dice_rolls(rolls):
    """Імітує кидання двох кубиків."""
    return Counter(
        random.randint(1, 6)
        + random.randint(1, 6)
        for _ in range(rolls)
    )


def print_table(counts, rolls):
    """Виводить таблицю результатів."""
    print(
        "Сума | Кількість | "
        "Монте-Карло | Аналітично"
    )

    print("-" * 52)

    for value in range(2, 13):
        probability = counts[value] / rolls

        print(
            f"{value:>4} | "
            f"{counts[value]:>9} | "
            f"{probability * 100:>10.2f}% | "
            f"{ANALYTICAL[value] * 100:>9.2f}%"
        )


def draw_chart(counts, rolls):
    """Будує графік імовірностей."""
    sums = list(range(2, 13))

    monte_carlo = [
        counts[value] / rolls * 100
        for value in sums
    ]

    analytical = [
        ANALYTICAL[value] * 100
        for value in sums
    ]

    figure, ax = plt.subplots(
        figsize=(10, 6)
    )

    ax.bar(
        [value - 0.2 for value in sums],
        monte_carlo,
        0.4,
        label="Монте-Карло",
    )

    ax.bar(
        [value + 0.2 for value in sums],
        analytical,
        0.4,
        label="Аналітично",
    )

    ax.set(
        title="Ймовірності сум двох кубиків",
        xlabel="Сума",
        ylabel="Імовірність, %",
    )

    ax.set_xticks(sums)
    ax.legend()

    ax.grid(
        axis="y",
        linestyle="--",
        alpha=0.4,
    )

    figure.tight_layout()

    plt.savefig(
        "dice_probabilities.png",
        dpi=150,
    )

    print(
        "Графік збережено у файл: "
        "dice_probabilities.png"
    )

    plt.show()
    plt.close(figure)


def main():
    random.seed(42)

    counts = simulate_dice_rolls(ROLLS)

    print(f"Кількість кидків: {ROLLS}\n")

    print_table(
        counts,
        ROLLS,
    )

    draw_chart(
        counts,
        ROLLS,
    )


if __name__ == "__main__":
    main()