from pathlib import Path
import timeit


def read_text(filename):
    data = (Path(__file__).parent / filename).read_bytes()

    for encoding in ("utf-8-sig", "cp1251"):
        try:
            return data.decode(encoding).lower()
        except UnicodeDecodeError:
            pass

    return data.decode("cp1251", errors="ignore").lower()


def boyer_moore(text, pattern):
    if not pattern:
        return 0

    length = len(pattern)
    shifts = {
        char: length - index - 1
        for index, char in enumerate(pattern[:-1])
    }
    position = 0

    while position <= len(text) - length:
        index = length - 1

        while index >= 0 and text[position + index] == pattern[index]:
            index -= 1

        if index < 0:
            return position

        char = text[position + length - 1]
        position += shifts.get(char, length)

    return -1


def compute_lps(pattern):
    lps = [0] * len(pattern)
    length = 0
    index = 1

    while index < len(pattern):
        if pattern[index] == pattern[length]:
            length += 1
            lps[index] = length
            index += 1
        elif length:
            length = lps[length - 1]
        else:
            index += 1

    return lps


def kmp_search(text, pattern):
    if not pattern:
        return 0

    lps = compute_lps(pattern)
    text_index = 0
    pattern_index = 0

    while text_index < len(text):
        if text[text_index] == pattern[pattern_index]:
            text_index += 1
            pattern_index += 1

            if pattern_index == len(pattern):
                return text_index - pattern_index

        elif pattern_index:
            pattern_index = lps[pattern_index - 1]
        else:
            text_index += 1

    return -1


def rabin_karp(text, pattern):
    if not pattern:
        return 0

    pattern_length = len(pattern)

    if pattern_length > len(text):
        return -1

    base = 256
    modulus = 101
    high_order = pow(base, pattern_length - 1, modulus)

    pattern_hash = 0
    window_hash = 0

    for index in range(pattern_length):
        pattern_hash = (
            pattern_hash * base + ord(pattern[index])
        ) % modulus
        window_hash = (
            window_hash * base + ord(text[index])
        ) % modulus

    for index in range(len(text) - pattern_length + 1):
        if (
            pattern_hash == window_hash
            and text[index:index + pattern_length] == pattern
        ):
            return index

        if index < len(text) - pattern_length:
            window_hash = (
                (
                    window_hash
                    - ord(text[index]) * high_order
                )
                * base
                + ord(text[index + pattern_length])
            ) % modulus

    return -1


def choose_pattern(text, preferred):
    if preferred in text:
        return preferred

    for pattern in ("алгоритм", "даних", "пошук", "система"):
        if pattern in text:
            return pattern


def main():
    algorithms = {
        "Boyer-Moore": boyer_moore,
        "KMP": kmp_search,
        "Rabin-Karp": rabin_karp,
    }

    articles = [
        (
            "Стаття 1",
            read_text("стаття_1.txt"),
            "алгоритми – це послідовність",
        ),
        (
            "Стаття 2",
            read_text("стаття_2.txt"),
            "метою даної роботи є дослідження",
        ),
    ]

    fake_pattern = "вигаданий_підрядок_якого_немає"
    total_times = {name: 0 for name in algorithms}

    for title, text, preferred_pattern in articles:
        existing_pattern = choose_pattern(text, preferred_pattern)
        article_times = {name: 0 for name in algorithms}

        print(f"\n{title}")

        for label, pattern in (
            ("Існуючий", existing_pattern),
            ("Вигаданий", fake_pattern),
        ):
            print(f"\n{label}: {pattern}")

            for name, algorithm in algorithms.items():
                assert algorithm(text, pattern) == text.find(pattern)

                elapsed = timeit.timeit(
                    lambda: algorithm(text, pattern),
                    number=20,
                ) / 20

                article_times[name] += elapsed
                total_times[name] += elapsed

                print(f"{name:<12} {elapsed:.8f} с")

        fastest = min(article_times, key=article_times.get)
        print(f"\nНайшвидший: {fastest}")

    fastest_overall = min(total_times, key=total_times.get)
    print(f"\nНайшвидший загалом: {fastest_overall}")


if __name__ == "__main__":
    main()