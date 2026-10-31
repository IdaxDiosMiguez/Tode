from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from Tode.app import Tode
    from Tode.buffer._buffer import Buffer

from enum import Enum

from .cursor import Cursor

from Tode.widgets._widget import Widget

from Tode.utils import ANSI
from Tode.utils import Color


class Direction(Enum):
    UP    = 1
    DOWN  = 2
    LEFT  = 3
    RIGHT = 4


class Editor(Widget):

    def __init__(self, app: Tode, buffer: Buffer):
        super().__init__(app=app)

        self.to_draw = True
        self.is_active = True

        self.buffer = buffer
        self._width, self._height = self.terminal.get_terminal_size()
        self.cursor = Cursor(1, 1)
        self.viewport_offset = 0

        self.background_color = Color("#292d34").to_ansi()
        self.line_number_color = Color("#7d956d").to_ansi(background=False)

        self.bind(ANSI.ARROW_UP,   self._move, Direction.UP)
        self.bind(ANSI.ARROW_DOWN, self._move, Direction.DOWN)
        self.bind(ANSI.ARROW_LEFT, self._move, Direction.LEFT)
        self.bind(ANSI.ARROW_RIGHT, self._move, Direction.RIGHT)

    def _move(self, direction: Direction):
        match direction:
            case Direction.UP:
                self.cursor.row = max(1, self.cursor.row - 1)

            case Direction.DOWN:
                self.cursor.row = min(self._height, self.cursor.row + 1)

            case Direction.LEFT:
                self.cursor.col = max(1, self.cursor.col - 1)

            case Direction.RIGHT:
                self.cursor.col = min(self._width, self.cursor.col + 1)

    def _format_line_number(self, row: int, padding: int, is_current: bool) -> str:

        space_start = "" if is_current else " "
        space_after = " " if is_current else ""

        return (
            f"{space_start}"
            f"{self.line_number_color}"
            f"{ANSI.BOLD_FONT}"
            f"{row:>{padding}}"
            f"{ANSI.UNSET_BOLD_FONT}"
            f"{ANSI.CLEAR_FOREGROUND}"
            f"  {space_after}"
        )

    def _format_buffer_line(self, row: int, line) -> str:
        return (
            f"{line}"
            f"{ANSI.ERASE_LINE}"
        )

    def render(self):

        buffer_lines = self.buffer.get_lines()[ : self._height]
        buffer_length = len(buffer_lines)
        line_num_padding = max(len(str(buffer_length)) + 1, 1)

        if self.to_draw:
            self.terminal.write(ANSI.HIDE_CURSOR)
            self.terminal.write(self.background_color)

            for row, line in enumerate(buffer_lines, 1):
                is_current = (row == self.cursor.row)
                line_num = self.cursor.row if is_current else abs(row - self.cursor.row)

                number = self._format_line_number(line_num, line_num_padding, is_current)
                line = self._format_buffer_line(row, line)

                self.terminal.move_to(1, row)
                self.terminal.write(f"{number}{line}")

            for row in range(buffer_length + 1, self._height + 1):
                self.terminal.move_to(1, row)
                self.terminal.write(ANSI.ERASE_LINE)

            self.terminal.write(ANSI.CLEAR_BACKGROUND)
            self.terminal.write(ANSI.SHOW_CURSOR)

        self.terminal.move_to(
            self.cursor.col + line_num_padding + 3,
            self.cursor.row
        )
