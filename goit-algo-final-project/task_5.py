from collections import deque

from tree_visualization import (
    Node,
    build_tree_from_heap,
    draw_tree,
)


def dfs(root: Node | None) -> list[Node]:
    """Виконує обхід дерева в глибину через стек."""
    if root is None:
        return []

    order = []
    stack = [root]

    while stack:
        node = stack.pop()
        order.append(node)

        if node.right is not None:
            stack.append(node.right)

        if node.left is not None:
            stack.append(node.left)

    return order


def bfs(root: Node | None) -> list[Node]:
    """Виконує обхід дерева в ширину через чергу."""
    if root is None:
        return []

    order = []
    queue = deque([root])

    while queue:
        node = queue.popleft()
        order.append(node)

        if node.left is not None:
            queue.append(node.left)

        if node.right is not None:
            queue.append(node.right)

    return order


def generate_colors(count: int) -> list[str]:
    """Створює градацію від темного до світлого."""
    if count == 0:
        return []

    start_color = (18, 80, 130)
    end_color = (180, 230, 250)
    colors = []

    for index in range(count):
        ratio = index / max(count - 1, 1)

        red = int(
            start_color[0]
            + (end_color[0] - start_color[0]) * ratio
        )

        green = int(
            start_color[1]
            + (end_color[1] - start_color[1]) * ratio
        )

        blue = int(
            start_color[2]
            + (end_color[2] - start_color[2]) * ratio
        )

        colors.append(
            f"#{red:02X}{green:02X}{blue:02X}"
        )

    return colors


def create_color_map(
    order: list[Node],
) -> dict[Node, str]:
    """Призначає кольори за порядком обходу."""
    colors = generate_colors(len(order))

    return dict(zip(order, colors))


def main() -> None:
    heap = [
        0,
        4,
        1,
        5,
        10,
        3,
        7,
    ]

    root = build_tree_from_heap(heap)

    if root is None:
        print("Дерево порожнє.")
        return

    dfs_order = dfs(root)
    bfs_order = bfs(root)

    print(
        f"DFS: {[node.value for node in dfs_order]}"
    )

    print(
        f"BFS: {[node.value for node in bfs_order]}"
    )

    draw_tree(
        root,
        "Обхід дерева в глибину DFS",
        "dfs_traversal.png",
        create_color_map(dfs_order),
    )

    draw_tree(
        root,
        "Обхід дерева в ширину BFS",
        "bfs_traversal.png",
        create_color_map(bfs_order),
    )


if __name__ == "__main__":
    main()