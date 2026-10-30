from dataclasses import dataclass


@dataclass(slots=True)
class Cursor:

    col: int
    row: int

    def __post_init__(self):
        self.col = max(self.col, 1)
        self.row = max(self.row, 1)
