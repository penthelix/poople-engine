from typing import cast

import numpy as np
import numpy.typing as npt


class Graph:
    def __init__(self, dims: tuple[int, int]) -> None:
        self.dims: tuple[int, int] = dims
        self.matrix: npt.NDArray[np.bool_] = np.zeros(dims, dtype=bool)

    def _validate_indices(self, x: int, y: int) -> bool:
        if x > self.dims[0] or y > self.dims[1]:
            raise IndexError("Index out of bounds.")
        if x < 0 or y < 0:
            raise IndexError("Index cannot be negative.")
        return True

    def _check_symmetry(self) -> bool:
        if self.dims[0] != self.dims[1]:
            raise ValueError("Matrix is not square.")
        return np.array_equal(self.matrix, self.matrix.T)

    def are_connected(self, x: int, y: int) -> bool:
        _ = self._validate_indices(x, y)
        return cast(bool, self.matrix[x, y])

    def get_connected(self, x: int) -> list[int]:
        _ = self._validate_indices(x, 0)
        row = cast(npt.NDArray[np.bool_], self.matrix[x])
        return np.where(row)[0].tolist()

    def add_edge(self, x: int, y: int):
        _ = self._validate_indices(x, y)
        self.matrix[x, y] = 1
        self.matrix[y, x] = 1

    def remove_edge(self, x: int, y: int) -> None:
        _ = self._validate_indices(x, y)
        if not self.are_connected(x, y):
            raise ValueError("Edge does not exist.")
        self.matrix[x, y] = 0
        self.matrix[y, x] = 0
