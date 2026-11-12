from typing import Iterable

from pathlib import Path

from Tode.core import Bindable

from Tode.drivers._driver import Driver
from Tode.drivers import LinuxDriver

from Tode.buffer import PieceTable

from Tode.widgets._widget import Widget
from Tode.widgets import Editor
from Tode.widgets import Explorer

from Tode.utils import ANSI
from Tode.utils import Keybind
from Tode.utils import Size
from Tode.utils import Coord


class Tode(Bindable):

    def __init__(self, path: Path) -> None:
        super().__init__()

        self.path = path

        self.is_running = True
        self.cursor_on = True
        self._input = ""

        self.terminal = self._build_driver()

        self.set_widgets()

        self.bind(Keybind("CTRL+X"), self._stop)
        self.bind(Keybind("CTRL+E"), self.toggle_explorer)

    def _build_driver(self) -> Driver:
        return LinuxDriver()

    def _render(self):
        self.terminal.write(ANSI.START_SYNC)

        action_done = False

        for widget in (self.explorer, self.editor):
            if (widget.is_active or widget.draw_once):
                if not action_done:
                    widget.handle_input(self._input)
                    action_done = True
                widget.render()

        self.terminal.write(ANSI.END_SYNC)

    def _stop(self) -> None:
        self.is_running = False

    def set_widgets(self) -> None:
        self.editor = Editor(
            app=self,
            buffer=PieceTable(
                self.path
            ),
            position=Coord(25, 1),
        )

        self.explorer = Explorer(
            app=self,
            root=self.path,
            position=Coord(1, 1),
            size=Size(
                self.editor.position.col,
                -1
            )
        )

    def toggle_explorer(self):
        self.editor.is_active = not self.editor.is_active
        self.explorer.is_active = not self.explorer.is_active
        self.cursor_on = not self.cursor_on

        self.explorer._draw_explorer()
        self.editor.render()

        if self.cursor_on:
            self.terminal.write(ANSI.SHOW_CURSOR)

        else:
            self.terminal.write(ANSI.HIDE_CURSOR)

    def run(self) -> None:
        self.terminal.start_application_mode()

        self._render()

        while self.is_running:
            self._input = self.terminal.on_input()

            self.handle_input(self._input)
            self._render()

        self.terminal.stop_application_mode()
