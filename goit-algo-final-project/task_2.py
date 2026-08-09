import math

import matplotlib.pyplot as plt


def draw_branch(
    ax,
    x: float,
    y: float,
    length: float,
    angle: float,
    level: int,
) -> None:
    """Рекурсивно малює гілки дерева Піфагора."""
    if level == 0:
        return

    end_x = x + length * math.cos(angle)
    end_y = y + length * math.sin(angle)

    branch_color = "#5D4037" if level > 3 else "#2E7D32"
    branch_width = max(level * 0.7, 1)

    ax.plot(
        [x, end_x],
        [y, end_y],
        color=branch_color,
        linewidth=branch_width,
    )

    next_length = length * 0.72
    angle_offset = math.radians(35)

    draw_branch(
        ax,
        end_x,
        end_y,
        next_length,
        angle + angle_offset,
        level - 1,
    )

    draw_branch(
        ax,
        end_x,
        end_y,
        next_length,
        angle - angle_offset,
        level - 1,
    )


def draw_pythagoras_tree(level: int) -> None:
    """Створює та зберігає зображення фрактального дерева."""
    figure, ax = plt.subplots(figsize=(8, 8))

    draw_branch(
        ax=ax,
        x=0,
        y=0,
        length=1.5,
        angle=math.pi / 2,
        level=level,
    )

    ax.set_aspect("equal")
    ax.axis("off")
    ax.set_title(
        f"Дерево Піфагора. Рівень рекурсії: {level}"
    )

    output_file = "pythagoras_tree.png"

    plt.tight_layout()
    plt.savefig(output_file, dpi=150)

    print(f"Фрактал збережено у файл: {output_file}")

    plt.show()


def main() -> None:
    try:
        level = int(
            input("Введіть рівень рекурсії від 1 до 12: ")
        )

        if not 1 <= level <= 12:
            raise ValueError

    except ValueError:
        print(
            "Помилка: потрібно ввести ціле число від 1 до 12."
        )
        return

    draw_pythagoras_tree(level)


if __name__ == "__main__":
    main()