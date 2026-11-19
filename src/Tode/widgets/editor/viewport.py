from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from Tode.drivers._driver import Driver
    from os import terminal_size


class Viewport:

    def __init__(self, bottom: int = 1, left: int = 0):
        self.width, self.height = 80, 24
        self.bottom = bottom
        self.left = left
        self.offset = 0

    @property
    def visible_height(self) -> int:
        return max(1, self.height - self.bottom)

    @property
    def visible_width(self) -> int:
        return max(1, self.width - self.left)

    def resize(self, size: terminal_size) -> bool:
        if size == (self.width, self.height):
            return False

        self.width, self.height = size
        return True

    def scroll_to(self, row: int) -> None:
        if row - 1 < self.offset:
            self.offset = row - 1

        elif row > self.offset + self.visible_height:
            self.offset = row - self.visible_height
