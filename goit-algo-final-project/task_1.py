class Node:
    """Вузол однозв'язного списку."""

    def __init__(self, data: int) -> None:
        self.data = data
        self.next: Node | None = None


class LinkedList:
    """Однозв'язний список."""

    def __init__(self) -> None:
        self.head: Node | None = None

    def insert_at_end(self, data: int) -> None:
        """Додає новий вузол у кінець списку."""
        new_node = Node(data)

        if self.head is None:
            self.head = new_node
            return

        current = self.head

        while current.next is not None:
            current = current.next

        current.next = new_node

    def print_list(self) -> None:
        """Виводить елементи списку."""
        current = self.head

        while current is not None:
            print(current.data, end=" -> ")
            current = current.next

        print("None")

    def reverse(self) -> None:
        """Реверсує список, змінюючи посилання між вузлами."""
        previous = None
        current = self.head

        while current is not None:
            next_node = current.next
            current.next = previous
            previous = current
            current = next_node

        self.head = previous

    @staticmethod
    def get_middle(head: Node) -> Node:
        """Знаходить середній вузол списку."""
        slow = head
        fast = head.next

        while fast is not None and fast.next is not None:
            slow = slow.next
            fast = fast.next.next

        return slow

    @staticmethod
    def sorted_merge(
        left: Node | None,
        right: Node | None,
    ) -> Node | None:
        """Об'єднує дві відсортовані частини списку."""
        dummy = Node(0)
        tail = dummy

        while left is not None and right is not None:
            if left.data <= right.data:
                tail.next = left
                left = left.next
            else:
                tail.next = right
                right = right.next

            tail = tail.next

        tail.next = left if left is not None else right
        return dummy.next

    def merge_sort(self, head: Node | None) -> Node | None:
        """Сортує однозв'язний список методом злиття."""
        if head is None or head.next is None:
            return head

        middle = self.get_middle(head)
        right_head = middle.next
        middle.next = None

        left_part = self.merge_sort(head)
        right_part = self.merge_sort(right_head)

        return self.sorted_merge(left_part, right_part)

    def sort(self) -> None:
        """Оновлює список після сортування."""
        self.head = self.merge_sort(self.head)

    @staticmethod
    def merge_sorted_lists(
        first: "LinkedList",
        second: "LinkedList",
    ) -> "LinkedList":
        """Об'єднує два відсортовані списки в один."""
        merged_list = LinkedList()

        merged_list.head = LinkedList.sorted_merge(
            first.head,
            second.head,
        )

        return merged_list


def create_list(values: list[int]) -> LinkedList:
    """Створює однозв'язний список із переданих значень."""
    linked_list = LinkedList()

    for value in values:
        linked_list.insert_at_end(value)

    return linked_list


def main() -> None:
    first_list = create_list([18, 7, 12, 3, 25, 10])

    print("Початковий список:")
    first_list.print_list()

    first_list.reverse()
    print("\nСписок після реверсування:")
    first_list.print_list()

    first_list.sort()
    print("\nВідсортований список:")
    first_list.print_list()

    second_list = create_list([1, 6, 14, 30])
    print("\nДругий відсортований список:")
    second_list.print_list()

    merged_list = LinkedList.merge_sorted_lists(
        first_list,
        second_list,
    )

    print("\nОб'єднаний відсортований список:")
    merged_list.print_list()


if __name__ == "__main__":
    main()