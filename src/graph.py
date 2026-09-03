from pathlib import Path
from typing import cast

import numpy as np
import numpy.typing as npt
from scipy.sparse.csgraph import shortest_path

from src.utils import PROJECT_ROOT, WORD_LENGTH, id_to_word, is_one_char_away, word


class Graph:
    """
    A graph represented as an adjacency matrix.
    """

    def __init__(self, dims: int) -> None:
        """
        Creates a square adjaceny matrix of shape (dims, dims) filled with zeros.

        Args:
            dims: The number of dimensions of the matrix.

        Raises:
            ValueError: If the dimensions are less than 1.
        """
        if dims < 1:
            raise ValueError("Dimensions must be positive.")
        self.dims: int = dims
        self.matrix: npt.NDArray[np.bool_] = np.zeros((dims, dims), dtype=bool)

        self.shortest_paths: npt.NDArray[np.float64] | None = None
        self.predecessors: npt.NDArray[np.int32] | None = None

    def _validate_indices(self, x: int, y: int) -> bool:
        """
        Check if the indices are valid when accessing the matrix.

        Raises:
            IndexError: If the indices are out of bounds or negative.
        """
        if x >= self.dims or y >= self.dims:
            raise IndexError("Index out of bounds.")
        if x < 0 or y < 0:
            raise IndexError("Index cannot be negative.")
        return True

    def _check_symmetry(self) -> bool:
        """
        Check if the matrix is symmetric.
        """
        return np.array_equal(self.matrix, self.matrix.T)

    def are_connected(self, x: int, y: int) -> bool:
        """
        Check if two nodes are connected.

        Args:
            x: The first node.
            y: The second node.

        Returns:
            bool: True if the nodes are connected, False otherwise.
        """
        _ = self._validate_indices(x, y)
        return cast(bool, self.matrix[x, y])

    def get_connected(self, x: int) -> list[int]:
        """
        Get the nodes connected to a given node.

        Args:
            x: The node to get the connected nodes for.

        Returns:
            list[int]: The nodes connected to the given node.
        """
        _ = self._validate_indices(x, 0)
        row = cast(npt.NDArray[np.bool_], self.matrix[x])
        return np.where(row)[0].tolist()

    def add_edge(self, x: int, y: int):
        """
        Add an edge between two nodes.

        Args:
            x: The first node.
            y: The second node.
        """
        _ = self._validate_indices(x, y)
        self.matrix[x, y] = 1
        self.matrix[y, x] = 1

    def remove_edge(self, x: int, y: int) -> None:
        """
        Remove an edge between two nodes.

        Args:
            x: The first node.
            y: The second node.

        Raises:
            ValueError: If the edge does not exist.
        """
        _ = self._validate_indices(x, y)
        if not self.are_connected(x, y):
            raise ValueError("Edge does not exist.")
        self.matrix[x, y] = 0
        self.matrix[y, x] = 0

    def calculate_shortest_paths(self):
        self.shortest_paths, self.predecessors = shortest_path(
            self.matrix, return_predecessors=True
        )


def build_graph(in_path: Path) -> Graph:
    with open(in_path, "rb") as f:
        line_count = sum([1 for _ in f])

    graph = Graph(dims=line_count)
    words = list(word(in_path))

    for i, w1 in enumerate(words):
        for j, w2 in enumerate(words[i + 1 :]):
            if is_one_char_away(w1, w2):
                graph.add_edge(i, j)

    return graph


def save_graph(graph: Graph, out_path: Path) -> None:
    np.savetxt(fname=out_path.with_suffix(".matrix"), X=graph.matrix)

    if graph.shortest_paths is None or graph.predecessors is None:
        return
    np.savetxt(fname=out_path.with_suffix(".paths"), X=graph.shortest_paths)
    np.savetxt(fname=out_path.with_suffix(".predecessors"), X=graph.predecessors)


def get_shortest_path(graph: Graph, start: int, end: int) -> list[str]:
    if graph.shortest_paths is None or graph.predecessors is None:
        raise ValueError("Graph has not been calculated yet.")

    if graph.shortest_paths[start][end] == float("inf"):
        raise ValueError("No path exists between the two words.")

    path: list[int] = []
    current: int = end
    while current != start:
        path.append(current)
        current = cast(int, graph.predecessors[start][current])
    path.append(start)
    path.reverse()
    return [id_to_word(i) for i in path]


def main() -> None:
    try:
        graph = build_graph(PROJECT_ROOT / "data" / f"{WORD_LENGTH}_letter_words.txt")
    except FileNotFoundError as e:
        print(e)
        return
    graph.calculate_shortest_paths()
    save_graph(
        graph=graph,
        out_path=PROJECT_ROOT / "data" / f"{WORD_LENGTH}_letter",
    )


if __name__ == "__main__":
    main()
