from collections.abc import Iterator
from pathlib import Path
from typing import cast

import numpy as np
import numpy.typing as npt


class Graph:
    """
    A graph represented as an adjacency matrix.
    """
    def __init__(self, dims: tuple[int, int]) -> None:
        self.dims: tuple[int, int] = dims
        self.matrix: npt.NDArray[np.bool_] = np.zeros(dims, dtype=bool)

    def _validate_indices(self, x: int, y: int) -> bool:
        """
        Check if the indices are valid.

        Raises:
            IndexError: If the indices are out of bounds or negative.
        """
        if x > self.dims[0] or y > self.dims[1]:
            raise IndexError("Index out of bounds.")
        if x < 0 or y < 0:
            raise IndexError("Index cannot be negative.")
        return True

    def _check_symmetry(self) -> bool:
        """
        Check if the matrix is symmetric.

        Raises:
            ValueError: If the matrix is not square.
        """
        if self.dims[0] != self.dims[1]:
            raise ValueError("Matrix is not square.")
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
    """
    if len(w1) != len(w2):
        raise ValueError("Words must be of same length.")
    if w1 == w2:
        raise ValueError("Words must be different.")

    diff = 0
    for c1, c2 in w1, w2:
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
    with open(file, "r") as f:
        for line in f:
            yield line.strip()
