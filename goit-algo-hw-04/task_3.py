import random
import timeit


def insertion_sort(values):
    items = values.copy()

    for i in range(1, len(items)):
        key = items[i]
        j = i - 1

        while j >= 0 and items[j] > key:
            items[j + 1] = items[j]
            j -= 1

        items[j + 1] = key

    return items


def merge_sort(values):
    if len(values) <= 1:
        return values.copy()

    middle = len(values) // 2
    left = merge_sort(values[:middle])
    right = merge_sort(values[middle:])

    result = []
    i = 0
    j = 0

    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1

    return result + left[i:] + right[j:]


def create_datasets(size):
    random_data = [
        random.randint(0, 100_000)
        for _ in range(size)
    ]

    return {
        "random": random_data,
        "sorted": sorted(random_data),
        "reversed": sorted(random_data, reverse=True),
        "few_unique": [
            random.randint(0, 10)
            for _ in range(size)
        ],
    }


def main():
    random.seed(42)

    algorithms = {
        "Insertion sort": insertion_sort,
        "Merge sort": merge_sort,
        "Timsort": sorted,
    }

    sizes = {
        100: 100,
        1000: 10,
        5000: 1,
    }

    for size, repeats in sizes.items():
        print(f"\nArray size: {size}")

        for dataset_name, data in create_datasets(size).items():
            print(f"  {dataset_name}:")

            correct_result = sorted(data)

            for name, algorithm in algorithms.items():
                if algorithm(data) != correct_result:
                    raise ValueError(f"{name} works incorrectly")

                time_result = timeit.timeit(
                    lambda: algorithm(data),
                    number=repeats,
                ) / repeats

                print(
                    f"    {name:<15} "
                    f"{time_result:.6f} sec/run"
                )

    print("\nConclusion:")
    print("Insertion sort is slow on large unsorted arrays: O(n^2).")
    print("Merge sort works faster on large arrays: O(n log n).")
    print("Timsort is usually the fastest built-in solution.")


if __name__ == "__main__":
    main()