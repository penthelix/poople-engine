from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent
DATA_FOLDER: Path = PROJECT_ROOT / "data"
ALL_WORDS_FILE: Path = PROJECT_ROOT / "data" / "all_words.txt"

# Edit these directly.
MAX_WORD_LENGTH: int = 10
MIN_WORD_LENGTH: int = 3

# Use setters.
WORD_LENGTH: int = 4
CORPUS_LENGTH: int = -1


def set_word_length(len: int):
    """
    Set the word length for the game. This will also reset the corpus length.

    Raises:
        ValueError: If the word length is not between MIN_WORD_LENGTH and MAX_WORD_LENGTH.
    """
    if len < MIN_WORD_LENGTH or len > MAX_WORD_LENGTH:
        raise ValueError(
            f"Word length must be between {MIN_WORD_LENGTH} and {MAX_WORD_LENGTH}"
        )
    global WORD_LENGTH
    WORD_LENGTH = len
    set_corpus_length(-1)


def set_corpus_length(len: int):
    global CORPUS_LENGTH
    CORPUS_LENGTH = len
