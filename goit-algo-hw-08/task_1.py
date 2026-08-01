from __future__ import annotations


class TreeNode:
    """Вузол двійкового дерева пошуку."""

    def __init__(self, data: int) -> None:
        self.data = data
        self.left: TreeNode | None = None
        self.right: TreeNode | None = None


class BinarySearchTree:
    """Двійкове дерево пошуку."""

    def __init__(self) -> None:
        self.root: TreeNode | None = None

    def add(self, data: int) -> None:
        """Додає нове значення до дерева."""
        new_node = TreeNode(data)

        if self.root is None:
            self.root = new_node
            return

        current_node = self.root

        while True:
            if data < current_node.data:
                if current_node.left is None:
                    current_node.left = new_node
                    return

                current_node = current_node.left
            else:
                if current_node.right is None:
                    current_node.right = new_node
                    return

                current_node = current_node.right


def find_minimum(root: TreeNode | None) -> int | None:
    """Повертає найменше значення у двійковому дереві пошуку."""
    if root is None:
        return None

    current_node = root

    # Найменше значення розташоване у крайньому лівому вузлі.
    while current_node.left is not None:
        current_node = current_node.left

    return current_node.data


def main() -> None:
    tree = BinarySearchTree()
    values = [25, 15, 40, 8, 18, 30, 50, 2]

    for value in values:
        tree.add(value)

    minimum = find_minimum(tree.root)

    print(f"Значення у дереві: {values}")
    print(f"Найменше значення: {minimum}")


if __name__ == "__main__":
    main()