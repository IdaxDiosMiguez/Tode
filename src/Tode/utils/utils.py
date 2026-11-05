from dataclasses import dataclass


@dataclass(slots=True)
class Coord:

    col: int
    row: int

    def __post_init__(self):
        self.col = max(self.col, 1)
        self.row = max(self.row, 1)


@dataclass(slots=True)
class Size:

    width: int
    height: int

    def __post_init__(self):
        self.width = max(self.width, 1)
        self.height = max(self.height, 1)
