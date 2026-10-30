from typing import Generator

from pathlib import Path

from Tode.core import Bindable

from Tode.drivers._driver import Driver
from Tode.drivers import LinuxDriver

from Tode.buffer import PieceTable

from Tode.widgets._widget import Widget
from Tode.widgets import Editor

from Tode.utils import Keybind
from Tode.utils import ANSI
from Tode.utils import Color


class Tode(Bindable):

    def __init__(self, path: Path) -> None:
        super().__init__()

        self.path = path

        self.is_running = True
        self._input = ""

        self.terminal = self._build_driver()
        self.widgets = list(self.get_widgets())

        self.bind(Keybind("CTRL+X"), self._stop)

    def _build_driver(self) -> Driver:
        return LinuxDriver()

    def _render(self):
        self.terminal.write(ANSI.START_SYNC)

        for widget in self.widgets:
            if widget.is_active:
                widget.handle_input(self._input)
            widget.render()

        self.terminal.write(ANSI.END_SYNC)

    def _stop(self) -> None:
        self.is_running = False

    def get_widgets(self) -> Generator[Widget]:
        editor = Editor(
            app=self,
            buffer=PieceTable(
                self.path
            )
        )

        editor.set_background_color(Color("#292d34"))

        yield editor

    def run(self) -> None:
        self.terminal.start_application_mode()

        self._render()

        while self.is_running:
            self._input = self.terminal.on_input()

            self.handle_input(self._input)
            self._render()

        self.terminal.stop_application_mode()
