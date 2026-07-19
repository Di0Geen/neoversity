import argparse
import shutil
from pathlib import Path


def get_extension(file_path: Path) -> str:
    return file_path.suffix[1:].lower() if file_path.suffix else "no_extension"


def get_unique_path(file_path: Path) -> Path:
    if not file_path.exists():
        return file_path

    counter = 1

    while True:
        new_name = f"{file_path.stem}_{counter}{file_path.suffix}"
        new_path = file_path.parent / new_name

        if not new_path.exists():
            return new_path

        counter += 1


def copy_files(source: Path, destination: Path) -> None:
    try:
        for item in source.iterdir():
            if item.resolve() == destination:
                continue

            if item.is_dir():
                copy_files(item, destination)

            elif item.is_file():
                folder = destination / get_extension(item)
                folder.mkdir(parents=True, exist_ok=True)

                target = get_unique_path(folder / item.name)
                shutil.copy2(item, target)

    except PermissionError as error:
        print(f"Permission denied: {error}")

    except OSError as error:
        print(f"Error while processing {source}: {error}")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Copy and sort files by extension."
    )
    parser.add_argument("source", help="Source directory")
    parser.add_argument(
        "destination",
        nargs="?",
        default="dist",
        help="Destination directory",
    )

    args = parser.parse_args()

    source = Path(args.source).resolve()
    destination = Path(args.destination).resolve()

    if not source.exists() or not source.is_dir():
        print("Source directory does not exist.")
        return

    if source == destination:
        print("Source and destination must be different.")
        return

    if destination.exists() and not destination.is_dir():
        print("Destination path is not a directory.")
        return

    try:
        destination.mkdir(parents=True, exist_ok=True)
    except OSError as error:
        print(f"Cannot create destination directory: {error}")
        return

    copy_files(source, destination)
    print("Done")


if __name__ == "__main__":
    main()