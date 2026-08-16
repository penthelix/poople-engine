from pytest import raises

from src.graph import Graph

# pyright: reportPrivateUsage=false


class TestGraph:
    def test_validate_indices(self):
        graph = Graph(dims=(2, 3))
        assert graph._validate_indices(2, 3) == True
        with raises(IndexError):
            _ = graph._validate_indices(2, 4)
        with raises(IndexError):
            _ = graph._validate_indices(3, 3)

    def test_check_symmetry(self):
        graph = Graph(dims=(3, 4))
        with raises(ValueError):
            _ = graph._check_symmetry()

        graph = Graph(dims=(3, 3))
        graph.matrix[0][1] = 1
        graph.matrix[1][0] = 1
        assert graph._check_symmetry() == True

        graph.matrix[0][2] = 1
        assert graph._check_symmetry() == False

    def test_are_connected(self):
        graph = Graph(dims=(3, 4))
        graph.matrix[0][1] = 1
        graph.matrix[1][0] = 1

        assert graph.are_connected(0, 1) == True
        assert graph.are_connected(0, 2) == False
        with raises(IndexError):
            _ = graph.are_connected(3, 4)

    def test_get_connected(self):
        graph = Graph(dims=(3, 4))
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
        graph = Graph(dims=(3, 4))
        graph.add_edge(0, 1)

        assert graph.matrix[0][1] == 1
        assert graph.matrix[1][0] == 1

    def test_remove_edge(self):
        graph = Graph(dims=(3, 4))
        graph.matrix[0][1] = 1
        graph.matrix[1][0] = 1
        graph.remove_edge(0, 1)

        assert graph.matrix[0][1] == 0
        assert graph.matrix[1][0] == 0
