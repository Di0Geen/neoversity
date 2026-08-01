from task_1 import BinarySearchTree, TreeNode


def sum_tree_values(root: TreeNode | None) -> int:
    """Обчислює суму всіх значень у двійковому дереві."""
    if root is None:
        return 0

    # Додаємо значення вузла та суми його піддерев.
    return (
        root.data
        + sum_tree_values(root.left)
        + sum_tree_values(root.right)
    )


def main() -> None:
    tree = BinarySearchTree()
    values = [25, 15, 40, 8, 18, 30, 50, 2]

    for value in values:
        tree.add(value)

    total = sum_tree_values(tree.root)

    print(f"Значення у дереві: {values}")
    print(f"Сума всіх значень: {total}")


if __name__ == "__main__":
    main()