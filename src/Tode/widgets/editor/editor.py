from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pathlib import Path

from Tode.widgets._widget import Widget, View

from Tode.utils import KEY
from Tode.utils import ANSI
from Tode.utils import Coord
from Tode.utils import Color
from Tode.utils import Keybind
from Tode.utils import Keybinds

from Tode.core import Focus
from Tode.core import Resize, OpenFile

from .piece_table import PieceTable

from .viewport import Viewport
from .gutter import Gutter
from .status_bar import StatusBar
from .actions import *


_DELTAS = {
    Direction.UP:    (-1, 0),
    Direction.DOWN:  (1, 0),
    Direction.LEFT:  (0, -1),
    Direction.RIGHT: (0, 1),
}

class Editor(Widget):

    KEYBINDS: Keybinds = {
        ANSI.ARROW_UP: Move(Direction.UP),
        ANSI.ARROW_DOWN:  Move(Direction.DOWN),
        ANSI.ARROW_LEFT: Move(Direction.LEFT),
        ANSI.ARROW_RIGHT: Move(Direction.RIGHT),

        KEY.ENTER: InsertNewLine(),
        KEY.BACKSPACE: DeleteChar(),

        Keybind("CTRL+S"): Save(),
    }

    def __init__(self, path: Path, cursor: Coord | None = None) -> None:
        self.buffer = PieceTable(path)
        self.scroll = Viewport()
        self.cursor = cursor or Coord(1, 1)

        self.focus  = Focus.EDITOR

        self.gutter     = Gutter()
        self.status_bar = StatusBar("MAIN", self.buffer.path.name)

        self.bg_color = Color("#282828").to_ansi(background=True)
        self.fg_color = Color("#e5e7eb").to_ansi(background=False)

    def keymap(self, key):
        if (action := super().keymap(key)) is not None:
            return action

        if len(key) == 1 and key.isprintable():
            return InsertChar(key)

        return None

    # --- update -----------------------------------------------------------

    def _move(self, direction):
        lines = self.buffer.get_lines()

        d_row, d_col = _DELTAS[direction]
        row = max(1, min(self.cursor.row + d_row, max(1, len(lines))))
        line = lines[row - 1] if lines else ""

        self.cursor.row = row
        self.cursor.col = max(1, min(self.cursor.col + d_col, len(line) + 1))

        self.scroll.scroll_to(self.cursor.row)

    def _insert_newline(self):
        self.buffer.insert(self.buffer.get_offset(self.cursor), "\n")

        self.cursor.row += 1
        self.cursor.col = 1
        self.scroll.scroll_to(self.cursor.row)

    def _delete_char(self):
        offset = self.buffer.get_offset(self.cursor)

        if offset <= 0:
            return

        lines = self.buffer.get_lines()

        if self.cursor.col > 1:
            self.cursor.col -= 1

        elif self.cursor.row > 1:
            self.cursor.row -= 1
            self.cursor.col = len(lines[self.cursor.row - 1]) + 1

        self.buffer.delete(offset - 1, 1)
        self.scroll.scroll_to(self.cursor.row)

    def _open_file(self, path):
        self.buffer = PieceTable(path)
        self.cursor = Coord(1, 1)
        self.scroll.offset = 0

    def update(self, action):
        match action:
            case Move(direction): self._move(direction)

            case InsertChar(ch):
                self.buffer.insert(self.buffer.get_offset(self.cursor), ch)
                self.cursor.col += 1

            case InsertNewLine(): self._insert_newline()
            case DeleteChar():    self._delete_char()

            case Save(): self.buffer.save()

            case OpenFile(path): self._open_file(path)

            case Resize(size):
                self.scroll.resize(size)
                self.scroll.scroll_to(self.cursor.row)

        return None

    # --- view -------------------------------------------------------------

    def view(self, focused: bool) -> View:
        lines = self.buffer.get_lines()
        top, height = self.scroll.offset, self.scroll.visible_height
        visible = lines[top : top + height]

        rows = []

        for row, line in enumerate(visible, top + 1):
            is_current = row == self.cursor.row
            number = row if is_current else abs(row - self.cursor.row)

            gutter = self.gutter.format(number, len(lines), is_current)
            text = line[: self.scroll.visible_width - self.gutter.len]

            rows.append(f"{self.bg_color}{gutter}{self.fg_color}{text}{ANSI.ERASE_LINE}{ANSI.CLEAR_STYLE}")

        rows += [f"{self.bg_color}▍{ANSI.ERASE_LINE}{ANSI.CLEAR_STYLE}"] * (height - len(visible))

        rows.append(self.status_bar.format(self.scroll.width, self.cursor, self.buffer.edited))

        cursor = None

        if focused:
            cursor = (self.cursor.col + self.gutter.width(len(lines)), self.cursor.row - top)

        return View(rows, cursor)
