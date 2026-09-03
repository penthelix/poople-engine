from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent
ALL_WORDS_FILE: Path = PROJECT_ROOT / "data" / "all_words.txt"

WORD_LENGTH: int = 4
MAX_WORD_LENGTH: int = 10
MIN_WORD_LENGTH: int = 3


def set_word_length(len: int):
    global WORD_LENGTH
    WORD_LENGTH = len
