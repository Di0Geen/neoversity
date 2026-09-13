from multiprocessing import Process, Queue, freeze_support
from pathlib import Path
from time import perf_counter

BASE_DIR = Path(__file__).resolve().parent
TEXT_FILES_DIR = BASE_DIR / "text_files"

KEYWORDS = [
    "Python", "Docker", "Kubernetes", "Git",
    "DevOps", "Threading", "Multiprocessing",
]


def divide_files(files: list[Path], workers: int) -> list[list[Path]]:
    """Розподіляє файли між процесами."""
    return [files[index::workers] for index in range(workers)]


def search_files(file_names: list[str], result_queue: Queue) -> None:
    """Шукає слова та передає результат через Queue."""
    result = {word: [] for word in KEYWORDS}

    for file_name in file_names:
        file_path = Path(file_name)

        try:
            text = file_path.read_text(encoding="utf-8").casefold()

            for word in KEYWORDS:
                if word.casefold() in text:
                    path = file_path.relative_to(BASE_DIR)
                    result[word].append(str(path))

        except (OSError, UnicodeError) as error:
            print(f"Помилка читання {file_path}: {error}")

    result_queue.put(result)


def run_multiprocessing(files: list[Path]) -> dict[str, list[str]]:
    """Запускає процеси та повертає спільний результат."""
    result = {word: [] for word in KEYWORDS}
    groups = divide_files(files, min(4, len(files)))
    result_queue = Queue()

    processes = [
        Process(
            target=search_files,
            args=(
                [str(path) for path in group],
                result_queue,
            ),
        )
        for group in groups
    ]

    for process in processes:
        process.start()

    for _ in processes:
        partial_result = result_queue.get()

        for word, paths in partial_result.items():
            result[word].extend(paths)

    for process in processes:
        process.join()

    result_queue.close()

    return {
        word: sorted(paths)
        for word, paths in result.items()
    }


def print_table(results: dict[str, list[str]]) -> None:
    """Виводить результати у вигляді таблиці."""
    headers = ("Ключове слово", "Кількість", "Знайдені файли")

    rows = [
        (
            word,
            str(len(paths)),
            ", ".join(paths) or "не знайдено",
        )
        for word, paths in results.items()
    ]

    widths = [
        max(map(len, column))
        for column in zip(headers, *rows)
    ]

    border = (
        "+"
        + "+".join("-" * (width + 2) for width in widths)
        + "+"
    )

    print(border)

    for number, row in enumerate((headers, *rows)):
        cells = (
            value.ljust(width)
            for value, width in zip(row, widths)
        )
        print(f"| {' | '.join(cells)} |")

        if number == 0:
            print(border)

    print(border)


def get_text_files() -> list[Path]:
    """Отримує список текстових файлів."""
    try:
        return sorted(
            path
            for path in TEXT_FILES_DIR.glob("*.txt")
            if path.is_file()
        )

    except OSError as error:
        print(f"Помилка файлової системи: {error}")
        return []


def main() -> None:
    files = get_text_files()

    if not files:
        print("Текстові файли не знайдено.")
        return

    start_time = perf_counter()
    results = run_multiprocessing(files)

    print("Багатопроцесорна версія (multiprocessing)")
    print_table(results)
    print(f"Час виконання: {perf_counter() - start_time:.6f} секунд")


if __name__ == "__main__":
    freeze_support()
    main()