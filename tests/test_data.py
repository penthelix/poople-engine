from pathlib import Path

from pytest import raises

from src.data import filter_words_by_length
from src.utils import WORD_LENGTH


def test_main():
    assert isinstance(WORD_LENGTH, int)
    assert WORD_LENGTH > 0


def test_filter_words_by_length(tmp_path: Path):
    # Test validation checks
    test_in: Path = tmp_path / "test_in.md"
    with raises(FileNotFoundError):
        _ = filter_words_by_length(test_in, out_dir=tmp_path)
    with raises(NotADirectoryError):
        test_in.touch()
        _ = filter_words_by_length(test_in, out_dir=tmp_path / "test_file.md")

    # 1 word of length 3: "six"
    # 4 words of length 4: "test", "word", "four", "five"
    # 1 word of length 7: "bananas"
    sample_text: str = "test\nword\nfour\nfive\nsix\nbananas\n"
    input_file: Path = tmp_path / "input.txt"
    with open(input_file, "w") as f:
        _ = f.write(sample_text)

    assert (
        filter_words_by_length(input_file, word_length=4, out_dir=tmp_path)
        == filter_words_by_length(input_file, out_dir=tmp_path)
        == 4
    )
    assert filter_words_by_length(input_file, word_length=3, out_dir=tmp_path) == 1
    assert filter_words_by_length(input_file, word_length=7, out_dir=tmp_path) == 1
    assert filter_words_by_length(input_file, word_length=2, out_dir=tmp_path) == 0
