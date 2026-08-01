import heapq


def calculate_minimum_cost(cable_lengths: list[int]) -> int:
    """Обчислює мінімальні загальні витрати на з'єднання кабелів."""
    if len(cable_lengths) < 2:
        return 0

    cables_heap = cable_lengths.copy()
    heapq.heapify(cables_heap)

    total_cost = 0

    while len(cables_heap) > 1:
        shortest_cable = heapq.heappop(cables_heap)
        next_shortest_cable = heapq.heappop(cables_heap)

        connected_length = shortest_cable + next_shortest_cable
        total_cost += connected_length

        heapq.heappush(cables_heap, connected_length)

    return total_cost


def get_connection_order(
    cable_lengths: list[int],
) -> list[tuple[int, int, int]]:
    """Повертає порядок з'єднання кабелів."""
    if len(cable_lengths) < 2:
        return []

    cables_heap = cable_lengths.copy()
    heapq.heapify(cables_heap)

    connection_order = []

    while len(cables_heap) > 1:
        shortest_cable = heapq.heappop(cables_heap)
        next_shortest_cable = heapq.heappop(cables_heap)

        connected_length = shortest_cable + next_shortest_cable

        connection_order.append(
            (shortest_cable, next_shortest_cable, connected_length)
        )

        heapq.heappush(cables_heap, connected_length)

    return connection_order


def main() -> None:
    cable_lengths = [5, 2, 8, 3, 7]

    minimum_cost = calculate_minimum_cost(cable_lengths)
    connection_order = get_connection_order(cable_lengths)

    print(f"Довжини кабелів: {cable_lengths}")
    print("Порядок з'єднання:")

    for first, second, result in connection_order:
        print(f"{first} + {second} = {result}")

    print(f"Мінімальні загальні витрати: {minimum_cost}")


if __name__ == "__main__":
    main()