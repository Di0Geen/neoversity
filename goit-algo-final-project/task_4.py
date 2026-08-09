import heapq

from tree_visualization import (
    build_tree_from_heap,
    draw_tree,
)


def visualize_heap(values: list[int]) -> None:
    """Створює та візуалізує мінімальну купу."""
    heap = values.copy()
    heapq.heapify(heap)

    print(f"Початкові значення: {values}")
    print(f"Мінімальна купа: {heap}")

    root = build_tree_from_heap(heap)

    if root is None:
        print("Купа порожня.")
        return

    draw_tree(
        root,
        "Візуалізація мінімальної бінарної купи",
        "heap_visualization.png",
    )


if __name__ == "__main__":
    numbers = [
        16,
        4,
        11,
        2,
        9,
        7,
        14,
        1,
        5,
    ]

    visualize_heap(numbers)