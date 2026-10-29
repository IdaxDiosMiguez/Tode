from Tode.widgets._widget import Widget

from .cursor import Cursor

from Tode.utils import ANSI
from Tode.utils import Color


class Editor(Widget):

    def __init__(self, app):
        super().__init__(app=app)
        self.to_draw = True
        self.cursor = Cursor(1, 1)

        self._width, self._height = self.terminal.get_terminal_size()

        self.background_color = Color("#343434").to_ansi()

    def set_background(self):
        self.terminal.write(self.background_color)
        for row in range(1, self._height + 1):
            for col in range(1, self._width + 1):
                self.terminal.move_to(col, row)
                self.terminal.write(" ")

        self.terminal.move_to(
            self.cursor.col,
            self.cursor.row
        )

        self.terminal.write(ANSI.CLEAR_BACKGROUND)

    def render(self):
        if self.to_draw:
            self.set_background()
            self.to_draw = False