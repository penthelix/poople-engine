from pathlib import Path

from pytest import raises

from src.utils import (
    PROJECT_ROOT,
    WORD_LEN,
    filter_words_by_length,
    get_words,
    is_one_char_away,
)


def test_main():
    assert isinstance(PROJECT_ROOT, Path)
    assert isinstance(WORD_LEN, int)
    assert WORD_LEN > 0


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


def test_is_one_char_away():
    with raises(ValueError):
        _ = is_one_char_away("abc", "abcd")

    assert is_one_char_away("abc", "abd") == True
    assert is_one_char_away("abc", "aac") == True
    assert is_one_char_away("abc", "abc") == False


def test_word(tmp_path: Path):
    with raises(FileNotFoundError):
        tmp_word_file: Path = tmp_path / "not_found.txt"
        _ = get_words(tmp_word_file)

    with raises(FileNotFoundError):
        _ = get_words(tmp_path)

    with open(tmp_path / "word.txt", "w+") as f:
        _ = f.write("hello\nworld\n")
        _ = f.seek(0)
        assert get_words(Path(f.name)) == ["hello", "world"]
