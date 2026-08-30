from pathlib import Path

from src.config import WORD_LENGTH
from src.utils import PROJECT_ROOT


def filter_words_by_length(
    in_path: Path,
    word_length: int = WORD_LENGTH,
    out_dir: Path | None = None,
) -> int:
    # Validate paths
    if not in_path.exists() or not in_path.is_file():
        raise FileNotFoundError(f"{in_path} was not found.")
    if out_dir and not out_dir.is_dir():
        raise NotADirectoryError(f"{out_dir} must be a directory.")

    out_filename = f"{word_length}_letter_words.txt"
    out_path = Path()

    if out_dir:
        out_path = out_dir / out_filename
    else:
        out_path = Path(".").parent.parent.absolute() / "data" / out_filename
    out_path.touch()

    out_line_count: int = 0

    with open(in_path, "r") as fin, open(out_path, "w") as fout:
        for line in fin:
            if word_length == len(line.strip()):
                out_line_count += 1
                _ = fout.write(line)
    return out_line_count


if __name__ == "__main__":
    _ = filter_words_by_length(PROJECT_ROOT / "data" / "all_words.txt")
