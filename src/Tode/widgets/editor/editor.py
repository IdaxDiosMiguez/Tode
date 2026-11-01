from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from Tode.app import Tode
    from Tode.buffer._buffer import Buffer

from enum import Enum

from .cursor import Cursor

from Tode.widgets._widget import Widget

from Tode.utils import ANSI
from Tode.utils import KEY
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
        self.cursor = Cursor(1, 1)
        self.offset = 0
        self._width, self._height = self.terminal.get_terminal_size()

        self.background_color = Color("#292d34").to_ansi()
        self.line_number_color = Color("#7d956d").to_ansi(background=False)

        self._setup_keybinds()

    def _setup_keybinds(self):
        # Arrow binds
        self.bind(ANSI.ARROW_UP,    self._move, Direction.UP)
        self.bind(ANSI.ARROW_DOWN,  self._move, Direction.DOWN)
        self.bind(ANSI.ARROW_LEFT,  self._move, Direction.LEFT)
        self.bind(ANSI.ARROW_RIGHT, self._move, Direction.RIGHT)

        # Char/Enter/Backspace
        self.bind(KEY.CHAR,         self.insert_char)
        self.bind(KEY.BACKSPACE,    self._delete_char)

    def _move(self, direction: Direction):
        buffer_lines = self.buffer.get_lines()
        buffer_length = len(buffer_lines)

        if buffer_length == 0:
            self.cursor.row = 1
            self.cursor.col = 1
            self.to_draw = True
            return

        match direction:
            case Direction.UP:
                if self.cursor.row > 1:
                    self.cursor.row -= 1
                    if (self.cursor.row - 1) < self.offset:
                        self.offset = max(0, self.offset - 1)

            case Direction.DOWN:
                if self.cursor.row < buffer_length:
                    self.cursor.row += 1
                    if self.cursor.row > self.offset + self._height:
                        self.offset += 1

            case Direction.LEFT:
                self.cursor.col -= 1

            case Direction.RIGHT:
                self.cursor.col += 1

        current_line = buffer_lines[self.cursor.row - 1]

        self.cursor.row = max(1, min(self.cursor.row, buffer_length))
        self.cursor.col = max(1, min(self.cursor.col, max(1, len(current_line) + 1)))

        self.to_draw = True

    def insert_char(self, char: str) -> None:
        offset = self.buffer.get_offset(self.cursor)
        self.buffer.insert(offset, char)
        self.cursor.col += 1

        self.to_draw = True

    def _delete_char(self):

        if (self.cursor.row == 1) and (self.cursor.col == 1):
            return

        offset = self.buffer.get_offset(self.cursor)

        if offset <= 0:
            return

        buffer_lines = self.buffer.get_lines()

        if self.cursor.col > 1:
            self.buffer.delete(offset - 1, 1)
            self.cursor.col -= 1

        elif self.cursor.row > 1:
            prev_row_idx = self.cursor.row - 2
            prev_line_len = len(buffer_lines[prev_row_idx])

            self.buffer.delete(offset - 1, 1)

            self.cursor.row -= 1
            self.cursor.col = prev_line_len + 1

        self.to_draw = True

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

    def _check_terminal_resize(self):
        width, height = self.terminal.get_terminal_size()

        if (self._width != width) or (self._height != height):
            self._width = width
            self._height = height
            self.to_draw = True

    def render(self):
        self._check_terminal_resize()

        buffer_lines = self.buffer.get_lines()
        buffer_length = len(buffer_lines)
        line_num_padding = max(len(str(buffer_length)) + 1, 1)

        if self.to_draw:
            visible_lines = buffer_lines[self.offset : self.offset + self._height]

            self.terminal.write(ANSI.HIDE_CURSOR)
            self.terminal.write(self.background_color)

            for row, line in enumerate(visible_lines, 1):
                abs_line_num = self.offset + row
                is_current = (abs_line_num == self.cursor.row)
                line_num = self.cursor.row if is_current else abs(abs_line_num - self.cursor.row)

                number = self._format_line_number(line_num, line_num_padding, is_current)
                line = self._format_buffer_line(line_num, line)

                self.terminal.move_to(1, row)
                self.terminal.write(f"{number}{line}")

            rendered_count = len(visible_lines)
            for row in range(rendered_count + 1, self._height + 1):
                self.terminal.move_to(1, row)
                self.terminal.write(ANSI.ERASE_LINE)

            self.terminal.write(ANSI.CLEAR_BACKGROUND)
            self.terminal.write(ANSI.SHOW_CURSOR)

            self.to_draw = False

        self.terminal.move_to(
            self.cursor.col + line_num_padding + 3,
            self.cursor.row - self.offset
        )