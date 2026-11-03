from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from Tode.app import Tode
    from Tode.buffer._buffer import Buffer

from enum import Enum, auto

from .cursor import Cursor
from .viewport import Viewport
from .gutter import Gutter
from .status_bar import StatusBar

from Tode.widgets._widget import Widget

from Tode.utils import ANSI
from Tode.utils import KEY
from Tode.utils import Keybind
from Tode.utils import Color


class Direction(Enum):
    UP    = auto()
    DOWN  = auto()
    LEFT  = auto()
    RIGHT = auto()


_DELTAS = {
    Direction.UP:    (-1, 0),
    Direction.DOWN:  (1, 0),
    Direction.LEFT:  (0, -1),
    Direction.RIGHT: (0, 1),
}


class Editor(Widget):

    def __init__(self, app: Tode, buffer: Buffer):
        super().__init__(app=app)

        self.buffer = buffer

        self.cursor     = Cursor(1, 1)
        self.viewport   = Viewport(self.terminal, 1)
        self.gutter     = Gutter()
        self.status_bar = StatusBar("MAIN", self.buffer.path.name)

        self.to_draw = True
        self.is_active = True

        self.left = 24

        self.bg_color = Color("#292d34").to_ansi(background=True)

        self._setup_keybinds()

    def _setup_keybinds(self):
        # Arrow binds
        self.bind(ANSI.ARROW_UP,    self._move, Direction.UP)
        self.bind(ANSI.ARROW_DOWN,  self._move, Direction.DOWN)
        self.bind(ANSI.ARROW_LEFT,  self._move, Direction.LEFT)
        self.bind(ANSI.ARROW_RIGHT, self._move, Direction.RIGHT)

        # Char/Enter/Backspace
        self.bind(KEY.CHAR,          self._insert_char)
        self.bind(KEY.BACKSPACE,     self._delete_char)
        self.bind(KEY.ENTER,         self._insert_newline)

        self.bind(Keybind("CTRL+S"), self.buffer.save)

    def _move(self, direction: Direction):
        lines = self.buffer.get_lines()
        old_row, old_offset = self.cursor.row, self.viewport.offset

        d_row, d_col = _DELTAS[direction]
        row = max(1, min(self.cursor.row + d_row, max(1, len(lines))))
        line = lines[row - 1] if lines else ""

        self.cursor.row = row
        self.cursor.col = max(1, min(self.cursor.col + d_col, len(line) + 1))

        height = self.viewport.visible_height

        if self.cursor.row - 1 < self.viewport.offset:
            self.viewport.offset = self.cursor.row - 1

        elif self.cursor.row > self.viewport.offset + height:
            self.viewport.offset = self.cursor.row - height

        if self.cursor.row != old_row or self.viewport.offset != old_offset:
            self.to_draw = True

    def _insert_char(self, char: str) -> None:
        offset = self.buffer.get_offset(self.cursor)
        self.buffer.insert(offset, char)
        self.cursor.col += 1

        self.to_draw = True

    def _insert_newline(self) -> None:
        offset = self.buffer.get_offset(self.cursor)
        self.buffer.insert(offset, "\n")

        self.cursor.row += 1
        self.cursor.col = 1
        self.viewport.scroll_to(self.cursor.row)

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

    def _draw_lines(self, lines: list[str]):
        visible = lines[self.viewport.offset : self.viewport.offset + self.viewport.visible_height]

        self.terminal.write(self.bg_color)

        for row, line in enumerate(visible, 1):
            abs_row = self.viewport.offset + row
            is_current = abs_row == self.cursor.row
            number = self.cursor.row if is_current else abs(abs_row - self.cursor.row)

            self.terminal.move_to(1 + self.left, row)
            self.terminal.write(
                f"{self.gutter.format(number, len(lines), is_current)}"
                f"{line}{ANSI.ERASE_LINE}"
            )

        for row in range(len(visible) + 1, self.viewport.visible_height + 1):
            self.terminal.move_to(1 + self.left, row)
            self.terminal.write(f"▍{ANSI.ERASE_LINE}")

        self.terminal.write(ANSI.CLEAR_BACKGROUND)
        self.to_draw = False

    def render(self):
        if self.viewport.resize():
            self.viewport.scroll_to(self.cursor.row)
            self.to_draw = True

        lines = self.buffer.get_lines()

        self.terminal.write(ANSI.HIDE_CURSOR)

        if self.to_draw:
            self._draw_lines(lines)

        self.terminal.move_to(1 + self.left, self.viewport.visible_height + 1)
        self.terminal.write(
            self.status_bar.format(
                self.viewport.width - self.left,
                self.cursor,
                self.buffer.edited
            )
        )

        self.terminal.write(ANSI.SHOW_CURSOR)
        self.terminal.move_to(
            self.cursor.col + self.left + self.gutter.width(len(lines)),
            self.cursor.row - self.viewport.offset,
        )