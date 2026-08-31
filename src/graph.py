from collections.abc import Iterator
from pathlib import Path
from typing import cast

import numpy as np
import numpy.typing as npt

from src.config import WORD_LENGTH
from src.utils import PROJECT_ROOT


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


def word(file: Path) -> Iterator[str]:
    """
    Generator to read words from a file.
    """
    if not file.exists():
        raise FileNotFoundError(f"File {file} does not exist.")
    if not file.is_file():
        raise FileNotFoundError(f"{file} is not a file.")

    with open(file, "r") as f:
        for line in f:
            yield line.strip()


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
    np.savetxt(fname=out_path, X=graph.matrix)


def main() -> None:
    try:
        graph = build_graph(PROJECT_ROOT / "data" / f"{WORD_LENGTH}_letter_words.txt")
    except FileNotFoundError as e:
        print(e)
        return
    save_graph(
        graph=graph,
        out_path=PROJECT_ROOT / "data" / f"{WORD_LENGTH}_letter",
    )


if __name__ == "__main__":
    main()
