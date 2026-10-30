from typing import TypeAlias, Literal
from enum import Enum

from Tode.widgets._widget import Widget

from .cursor import Cursor

from Tode.utils import ANSI
from Tode.utils import Color


class Direction(Enum):
    UP    = 1
    DOWN  = 2
    LEFT  = 3
    RIGHT = 4


class Editor(Widget):

    def __init__(self, app):
        super().__init__(app=app)

        self.to_draw = True
        self.is_active = True

        self.cursor = Cursor(1, 1)
        self._width, self._height = self.terminal.get_terminal_size()

        self.background_color = Color("#343434").to_ansi()

        self.bind(ANSI.ARROW_UP,   self._move, Direction.UP)
        self.bind(ANSI.ARROW_DOWN, self._move, Direction.DOWN)

    def _move(self, direction: Direction):
        match direction:
            case Direction.UP:
                self.cursor.row = max(1, self.cursor.row - 1)

            case Direction.DOWN:
                self.cursor.row = min(self._height, self.cursor.row + 1)

    def set_background_color(self, color: Color):
        self.background_color = color.to_ansi()

    def draw_background(self):
        self.terminal.write(ANSI.HIDE_CURSOR)
        self.terminal.write(self.background_color)

        _buffer = " " * self._width * self._height

        self.terminal.move_to(1, 1)
        self.terminal.write(_buffer)

        self.terminal.write(ANSI.CLEAR_BACKGROUND)
        self.terminal.write(ANSI.SHOW_CURSOR)

        self.to_draw = False

    def render(self):
        if self.to_draw:
            self.draw_background()

        self.terminal.move_to(
            self.cursor.col,
            self.cursor.row
        )
