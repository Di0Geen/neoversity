import argparse
import asyncio
import logging
import shutil
from pathlib import Path

LOGGER = logging.getLogger(__name__)


def unique_destination(
    file_path: Path,
    output_folder: Path,
    reserved: set[str],
) -> Path:
    """Build a unique destination path for a file."""
    extension = file_path.suffix.lower().lstrip(".") or "no_extension"
    folder = output_folder / extension
    destination = folder / file_path.name
    counter = 1

    while str(destination).casefold() in reserved or destination.exists():
        destination = folder / (
            f"{file_path.stem}_{counter}{file_path.suffix}"
        )
        counter += 1

    reserved.add(str(destination).casefold())
    return destination


async def copy_file(
    source: Path,
    destination: Path,
    semaphore: asyncio.Semaphore,
) -> bool:
    """Copy one file without blocking the event loop."""
    try:
        async with semaphore:
            await asyncio.to_thread(
                destination.parent.mkdir,
                parents=True,
                exist_ok=True,
            )
            await asyncio.to_thread(
                shutil.copy2,
                source,
                destination,
            )

        LOGGER.info("Скопійовано: %s -> %s", source, destination)
        return True

    except (OSError, shutil.Error) as error:
        LOGGER.error("Не вдалося скопіювати %s: %s", source, error)
        return False


async def read_folder(
    source: Path,
    output: Path,
    concurrency: int,
) -> tuple[int, int]:
    """Find files recursively and copy them concurrently."""
    files = await asyncio.to_thread(
        lambda: [
            path
            for path in source.rglob("*")
            if path.is_file()
        ]
    )

    reserved: set[str] = set()
    destinations = [
        unique_destination(file, output, reserved)
        for file in files
    ]

    semaphore = asyncio.Semaphore(concurrency)

    results = await asyncio.gather(
        *(
            copy_file(file, destination, semaphore)
            for file, destination in zip(
                files,
                destinations,
                strict=True,
            )
        )
    )

    successful = sum(results)
    return successful, len(results) - successful


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Асинхронне сортування файлів за розширеннями."
    )

    parser.add_argument(
        "source",
        type=Path,
        help="Вихідна папка",
    )
    parser.add_argument(
        "output",
        type=Path,
        help="Цільова папка",
    )
    parser.add_argument(
        "--concurrency",
        type=int,
        default=10,
    )

    return parser.parse_args()


async def main() -> int:
    args = parse_arguments()

    source = args.source.expanduser().resolve()
    output = args.output.expanduser().resolve()

    if not source.is_dir():
        LOGGER.error("Вихідна папка не існує: %s", source)
        return 1

    if output == source or source in output.parents:
        LOGGER.error(
            "Цільова папка не може бути всередині вихідної"
        )
        return 1

    if args.concurrency < 1:
        LOGGER.error(
            "Параметр concurrency має бути більшим за нуль"
        )
        return 1

    try:
        await asyncio.to_thread(
            output.mkdir,
            parents=True,
            exist_ok=True,
        )

        successful, failed = await read_folder(
            source,
            output,
            args.concurrency,
        )

    except OSError as error:
        LOGGER.error("Помилка обробки папок: %s", error)
        return 1

    LOGGER.info(
        "Завершено: %d скопійовано, %d помилок",
        successful,
        failed,
    )

    return 0 if failed == 0 else 1


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format="%(levelname)s: %(message)s",
    )

    raise SystemExit(asyncio.run(main()))