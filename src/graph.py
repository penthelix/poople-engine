from typing import cast

import numpy as np
import numpy.typing as npt


class Graph:
    def __init__(self, dims: tuple[int, int]) -> None:
        self.matrix: npt.NDArray[np.bool_] = np.zeros(dims, dtype=bool)
        self.dims: tuple[int, int] = dims

    def _validate_indices(self, x: int, y: int) -> None:
        if x > self.dims[0] or y > self.dims[1]:
            raise IndexError("Index out of bounds.")
        if x < 0 or y < 0:
            raise IndexError("Index cannot be negative.")

    def _check_symmetry(self) -> bool:
        return np.array_equal(self.matrix, self.matrix.T)

    def are_connected(self, x: int, y: int) -> bool | np.bool_:
        self._validate_indices(x, y)
        return cast(bool, self.matrix[x, y])

    def get_connected(self, x: int) -> list[int]:
        row = cast(npt.NDArray[np.bool_], self.matrix[x])
        return np.where(row)[0].tolist()

    def add_edge(self, x: int, y: int):
        self._validate_indices(x, y)
        self.matrix[x, y] = True
        self.matrix[y, x] = True

    def remove_edge(self, x: int, y: int) -> None:
        self._validate_indices(x, y)
        if not self.are_connected(x, y):
            raise ValueError("Edge does not exist.")
        self.matrix[x, y] = False
        self.matrix[y, x] = False
