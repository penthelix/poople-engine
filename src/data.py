from pathlib import Path

from src.utils import (
    ALL_WORDS_FILE,
    DATA_FOLDER,
    WORD_LENGTH,
    set_corpus_length,
)


def filter_words_by_length(
    in_path: Path,
    out_dir: Path,
    word_length: int = WORD_LENGTH,
) -> int:
    """
    Gets words from a file, filters them by length, and writes them to a new file.

    Args:
        in_path: Path to the input file.
        out_dir: Path to the output directory.
        word_length: Length of the words to filter.

     Raises:
        FileNotFoundError: If the input file does not exist.
        NotADirectoryError: If out_dir is not a directory.

    Returns:
        The number of words written to the output file.
    """
    if not in_path.exists() or not in_path.is_file():
        raise FileNotFoundError(f"{in_path} was not found.")
    if not out_dir.is_dir():
        raise NotADirectoryError(f"{out_dir} must be a directory.")

    out_path = out_dir / f"{word_length}_letter_words.txt"
    out_path.touch()

    out_line_count: int = 0

    with open(in_path, "r") as fin, open(out_path, "w") as fout:
        for line in fin:
            if word_length == len(line.strip()):
                out_line_count += 1
                _ = fout.write(line)
    return out_line_count


if __name__ == "__main__":
    lines = filter_words_by_length(
        in_path=ALL_WORDS_FILE,
        out_dir=DATA_FOLDER,
    )
    set_corpus_length(lines)
