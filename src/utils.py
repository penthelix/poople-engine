import re
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent
DATA_FOLDER: Path = PROJECT_ROOT / "data"
CORPUS_FILE: Path = PROJECT_ROOT / "data" / "all_words.txt"

# Edit these directly.
MAX_WORD_LEN: int = 10
MIN_WORD_LEN: int = 3

# Use setters.
WORD_LEN: int = 4
CORPUS_LEN: int = -1


def set_word_length(len: int) -> None:
    """
    Set the word length for the game. This will also reset the corpus length.

    Raises:
        ValueError: If the word length is not between MIN_WORD_LENGTH and MAX_WORD_LENGTH.
    """
    if len < MIN_WORD_LEN or len > MAX_WORD_LEN:
        raise ValueError(
            f"Word length must be between {MIN_WORD_LEN} and {MAX_WORD_LEN}"
        )
    global WORD_LEN
    WORD_LEN = len
    set_corpus_length(-1)


def set_corpus_length(len: int) -> None:
    global CORPUS_LEN
    CORPUS_LEN = len


def filter_words_by_length(
    in_path: Path,
    out_dir: Path,
    word_length: int = WORD_LEN,
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
    if not in_path.is_file():
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


def is_one_char_away(w1: str, w2: str) -> bool:
    """
    Check if two words are one character apart.

    Raises:
        ValueError: If the words are of different lengths.
    """
    if len(w1) != len(w2):
        raise ValueError("Words must be of same length.")

    if w1 == w2:
        return False

    diff = 0
    for c1, c2 in zip(w1, w2):
        if c1 != c2:
            diff += 1
        if diff > 1:
            return False
    return True


def id_to_word(id: int) -> str:
    """
    Convert word ID i.e. its line number in CORPUS_FILE to the word itself.

    Raises:
        ValueError: If the word ID is not found.
    """
    with open(CORPUS_FILE, "r") as f:
        for i, line in enumerate(f):
            if i == id:
                return line.strip()
    raise ValueError(f"Word ID {id} not found.")


def get_words(file: Path, sort: bool = False) -> list[str]:
    """
    Returns a list of words from a file without duplicates.
    """
    if not file.is_file():
        raise FileNotFoundError(f"{file} was not found.")

    with open(file, "r") as f:
        words = [line.strip() for line in f]
    if sort:
        return sorted(words)
    return words


def sanitize_word(word: str) -> str:
    """
    Sanitize a word by removing non-alphabetic characters and converting to lowercase.
    """
    word = word.lower()
    word = re.sub(r"[^a-z]", "", word)
    return word


if __name__ == "__main__":
    lines = filter_words_by_length(
        in_path=CORPUS_FILE,
        out_dir=DATA_FOLDER,
    )
    set_corpus_length(lines)
