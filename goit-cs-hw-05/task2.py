import argparse
import re
from collections import Counter
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import matplotlib.pyplot as plt
import requests

DEFAULT_URL = "https://www.gutenberg.org/files/1342/1342-0.txt"
WORD_PATTERN = re.compile(
    r"[^\W\d_]+(?:['’-][^\W\d_]+)*",
    re.UNICODE,
)


def positive_int(value: str) -> int:
    number = int(value)

    if number < 1:
        raise argparse.ArgumentTypeError(
            "значення має бути більшим за нуль"
        )

    return number


def download_text(url: str, timeout: int = 30) -> str:
    response = requests.get(
        url,
        timeout=timeout,
        headers={"User-Agent": "GoIT MapReduce homework"},
    )
    response.raise_for_status()

    return response.text


def tokenize(text: str) -> list[str]:
    return [
        word.casefold()
        for word in WORD_PATTERN.findall(text)
    ]


def count_chunk(words: list[str]) -> Counter[str]:
    return Counter(words)


def map_reduce(
    text: str,
    workers: int = 4,
) -> Counter[str]:
    words = tokenize(text)

    if not words:
        return Counter()

    chunk_size = max(
        1,
        (len(words) + workers - 1) // workers,
    )

    chunks = [
        words[index:index + chunk_size]
        for index in range(0, len(words), chunk_size)
    ]

    with ThreadPoolExecutor(
        max_workers=workers
    ) as executor:
        partial_results = executor.map(
            count_chunk,
            chunks,
        )

    frequencies: Counter[str] = Counter()

    for result in partial_results:
        frequencies.update(result)

    return frequencies


def visualize_top_words(
    frequencies: Counter[str],
    top_n: int,
    output: Path,
) -> None:
    top_words = frequencies.most_common(top_n)

    if not top_words:
        raise ValueError("У тексті не знайдено слів")

    if output.is_dir():
        raise ValueError(
            "Для output потрібно вказати ім'я файлу"
        )

    words, counts = zip(
        *reversed(top_words),
        strict=True,
    )

    output.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    figure, axis = plt.subplots(
        figsize=(10, 6)
    )

    bars = axis.barh(
        words,
        counts,
        color="skyblue",
    )

    axis.bar_label(bars, padding=3)
    axis.set_title(
        f"Топ-{len(top_words)} найчастіших слів"
    )
    axis.set_xlabel("Кількість")
    axis.set_ylabel("Слова")

    figure.tight_layout()
    figure.savefig(output, dpi=150)
    plt.close(figure)


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Аналіз частоти слів "
            "за допомогою MapReduce."
        )
    )

    parser.add_argument(
        "url",
        nargs="?",
        default=DEFAULT_URL,
    )
    parser.add_argument(
        "--top",
        type=positive_int,
        default=10,
    )
    parser.add_argument(
        "--workers",
        type=positive_int,
        default=4,
    )
    parser.add_argument(
        "--timeout",
        type=positive_int,
        default=30,
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("top_words.png"),
    )

    return parser.parse_args()


def main() -> int:
    args = parse_arguments()

    try:
        text = download_text(
            args.url,
            args.timeout,
        )

        frequencies = map_reduce(
            text,
            args.workers,
        )

        visualize_top_words(
            frequencies,
            args.top,
            args.output,
        )

    except (
        requests.RequestException,
        OSError,
        ValueError,
    ) as error:
        print(f"Помилка: {error}")
        return 1

    print(f"Графік збережено: {args.output}")
    print("Найчастіші слова:")

    for word, count in frequencies.most_common(
        args.top
    ):
        print(f"{word}: {count}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())