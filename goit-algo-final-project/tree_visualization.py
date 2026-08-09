from collections import deque

import matplotlib.pyplot as plt


class Node:
    """Вузол бінарного дерева."""

    def __init__(self, value: int) -> None:
        self.value = value
        self.left: Node | None = None
        self.right: Node | None = None


def build_tree_from_heap(
    heap: list[int],
    index: int = 0,
) -> Node | None:
    """Будує бінарне дерево з масиву купи."""
    if index >= len(heap):
        return None

    node = Node(heap[index])

    node.left = build_tree_from_heap(
        heap,
        2 * index + 1,
    )

    node.right = build_tree_from_heap(
        heap,
        2 * index + 2,
    )

    return node


def collect_nodes(root: Node) -> list[Node]:
    """Збирає вузли дерева в ширину."""
    nodes = []
    queue = deque([root])

    while queue:
        node = queue.popleft()
        nodes.append(node)

        if node.left is not None:
            queue.append(node.left)

        if node.right is not None:
            queue.append(node.right)

    return nodes


def get_positions(
    root: Node,
) -> dict[Node, tuple[float, float]]:
    """Обчислює координати вузлів дерева."""
    positions = {
        root: (0.0, 0.0),
    }

    queue = deque([
        (root, 0.0, 0.0, 1),
    ])

    while queue:
        node, x, y, level = queue.popleft()
        offset = 1 / (2 ** level)

        children = (
            (node.left, x - offset),
            (node.right, x + offset),
        )

        for child, child_x in children:
            if child is not None:
                positions[child] = (
                    child_x,
                    y - 1,
                )

                queue.append(
                    (
                        child,
                        child_x,
                        y - 1,
                        level + 1,
                    )
                )

    return positions


def draw_tree(
    root: Node,
    title: str,
    output_file: str,
    colors: dict[Node, str] | None = None,
) -> None:
    """Візуалізує дерево та зберігає зображення."""
    nodes = collect_nodes(root)
    positions = get_positions(root)

    figure, ax = plt.subplots(figsize=(10, 7))

    # Малюємо ребра дерева.
    for node in nodes:
        x, y = positions[node]

        for child in (node.left, node.right):
            if child is not None:
                child_x, child_y = positions[child]

                ax.plot(
                    [x, child_x],
                    [y, child_y],
                    color="#616161",
                )

    # Малюємо вузли дерева.
    for node in nodes:
        x, y = positions[node]

        color = (
            colors.get(node, "#90CAF9")
            if colors
            else "#90CAF9"
        )

        ax.scatter(
            x,
            y,
            s=1800,
            color=color,
            edgecolors="#263238",
            zorder=2,
        )

        ax.text(
            x,
            y,
            str(node.value),
            ha="center",
            va="center",
            fontsize=12,
            zorder=3,
        )

    ax.set_title(title, fontsize=16)
    ax.margins(x=0.15, y=0.20)
    ax.axis("off")

    figure.tight_layout()

    figure.savefig(
        output_file,
        dpi=150,
        bbox_inches="tight",
    )

    print(f"Зображення збережено у файл: {output_file}")

    plt.show()
    plt.close(figure)