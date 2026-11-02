from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from Tode.drivers._driver import Driver


class Viewport:

    def __init__(self, terminal: Driver, bottom: int = 1):
        self._terminal = terminal

        self.width, self.height = self._terminal.get_terminal_size()
        self.bottom = bottom
        self.offset = 0

    @property
    def visible_height(self) -> int:
        return max(1, self.height - self.bottom)

    def resize(self) -> bool:
        size = self._terminal.get_terminal_size()

        if size == (self.width, self.height):
            return False

        self.width, self.height = size
        return True

    def scroll_to(self, row: int) -> None:
        if row - 1 < self.offset:
            self.offset = row - 1

        elif row > self.offset + self.visible_height:
            self.offset = row - self.visible_height
