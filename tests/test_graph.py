from pathlib import Path

from pytest import raises

from src.graph import Graph, is_one_char_away, word

# pyright: reportPrivateUsage=false


class TestGraph:
    def test_validate_indices(self):
        graph = Graph(dims=2)
        with raises(IndexError):
            _ = graph._validate_indices(2, 2)
        with raises(IndexError):
            _ = graph._validate_indices(2, 4)
        with raises(IndexError):
            _ = graph._validate_indices(3, 3)

    def test_check_symmetry(self):
        graph = Graph(dims=3)
        graph.matrix[0][1] = 1
        graph.matrix[1][0] = 1
        assert graph._check_symmetry() == True

        graph.matrix[0][2] = 1
        assert graph._check_symmetry() == False

    def test_are_connected(self):
        graph = Graph(dims=3)
        graph.matrix[0][1] = 1
        graph.matrix[1][0] = 1

        assert graph.are_connected(0, 1) == True
        assert graph.are_connected(0, 2) == False
        with raises(IndexError):
            _ = graph.are_connected(3, 4)

    def test_get_connected(self):
        graph = Graph(dims=3)
        graph.matrix[0][1] = 1
        graph.matrix[1][0] = 1
        graph.matrix[0][2] = 1
        graph.matrix[2][0] = 1

        assert graph.get_connected(0) == [1, 2]
        assert graph.get_connected(1) == [0]
        assert graph.get_connected(2) == [0]
        with raises(IndexError):
            assert graph.get_connected(3) == []

    def test_add_edge(self):
        graph = Graph(dims=3)
        graph.add_edge(0, 1)

        assert graph.matrix[0][1] == 1
        assert graph.matrix[1][0] == 1

    def test_remove_edge(self):
        graph = Graph(dims=3)
        graph.matrix[0][1] = 1
        graph.matrix[1][0] = 1
        graph.remove_edge(0, 1)

        assert graph.matrix[0][1] == 0
        assert graph.matrix[1][0] == 0


def test_is_one_char_away():
    with raises(ValueError):
        _ = is_one_char_away("abc", "abcd")

    assert is_one_char_away("abc", "abd") == True
    assert is_one_char_away("abc", "aac") == True
    assert is_one_char_away("abc", "abc") == False


def test_word(tmp_path: Path):
    with raises(FileNotFoundError):
        tmp_word_file: Path = tmp_path / "not_found.txt"
        _ = list(word(tmp_word_file))

    with raises(FileNotFoundError):
        _ = list(word(tmp_path))

    with open(tmp_path / "word.txt", "w+") as f:
        _ = f.write("hello\nworld\n")
        _ = f.seek(0)
        assert list(word(Path(f.name))) == ["hello", "world"]
