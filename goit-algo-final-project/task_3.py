import heapq


Graph = dict[str, list[tuple[str, int]]]


def dijkstra(
    graph: Graph,
    start: str,
) -> tuple[dict[str, float], dict[str, str | None]]:
    """Обчислює найкоротші відстані від початкової вершини."""
    if start not in graph:
        raise ValueError(
            "Початкова вершина відсутня у графі."
        )

    distances = {
        vertex: float("inf")
        for vertex in graph
    }

    previous = {
        vertex: None
        for vertex in graph
    }

    distances[start] = 0
    priority_queue = [(0, start)]

    while priority_queue:
        current_distance, current_vertex = heapq.heappop(
            priority_queue
        )

        if current_distance > distances[current_vertex]:
            continue

        for neighbor, weight in graph[current_vertex]:
            if weight < 0:
                raise ValueError(
                    "Алгоритм Дейкстри не підтримує "
                    "від'ємні ваги."
                )

            new_distance = current_distance + weight

            if new_distance < distances[neighbor]:
                distances[neighbor] = new_distance
                previous[neighbor] = current_vertex

                heapq.heappush(
                    priority_queue,
                    (new_distance, neighbor),
                )

    return distances, previous


def restore_path(
    previous: dict[str, str | None],
    start: str,
    target: str,
) -> list[str]:
    """Відновлює найкоротший шлях до заданої вершини."""
    path = []
    current: str | None = target

    while current is not None:
        path.append(current)

        if current == start:
            return path[::-1]

        current = previous[current]

    return []


def main() -> None:
    graph: Graph = {
        "A": [
            ("B", 6),
            ("C", 2),
        ],
        "B": [
            ("A", 6),
            ("C", 3),
            ("D", 1),
        ],
        "C": [
            ("A", 2),
            ("B", 3),
            ("D", 5),
            ("E", 8),
        ],
        "D": [
            ("B", 1),
            ("C", 5),
            ("E", 4),
            ("F", 7),
        ],
        "E": [
            ("C", 8),
            ("D", 4),
            ("F", 2),
        ],
        "F": [
            ("D", 7),
            ("E", 2),
        ],
    }

    start_vertex = "A"

    distances, previous = dijkstra(
        graph,
        start_vertex,
    )

    print(f"Початкова вершина: {start_vertex}\n")
    print("Найкоротші шляхи:")

    for vertex in graph:
        path = restore_path(
            previous,
            start_vertex,
            vertex,
        )

        path_text = " -> ".join(path)

        print(
            f"{start_vertex} -> {vertex}: "
            f"відстань {distances[vertex]}, "
            f"шлях {path_text}"
        )


if __name__ == "__main__":
    main()