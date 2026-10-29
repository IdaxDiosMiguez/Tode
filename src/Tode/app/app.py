from typing import Callable

from Tode.core import Bindable

from Tode.drivers import LinuxDriver
from Tode.drivers._driver import Driver

from Tode.widgets import Editor

from Tode.utils import Keybind
from Tode.utils import ANSI


class Tode(Bindable):

    def __init__(self) -> None:
        super().__init__()

        self.terminal = self._build_driver()
        self.widgets = [
            Editor(self)
        ]

        self.keybinds = {
            Keybind("CTRL+X"): self._stop
        }

        self.is_running = True

    def _build_driver(self) -> Driver:
        return LinuxDriver()

    def _render(self):
        self.terminal.write(ANSI.HIDE_CURSOR)
        self.terminal.write(ANSI.START_SYNC)

        for widget in self.widgets:
            widget.render()

        self.terminal.write(ANSI.END_SYNC)
        self.terminal.write(ANSI.SHOW_CURSOR)

    def _stop(self) -> None:
        self.is_running = False

    def run(self) -> None:
        self.terminal.start_application_mode()

        self._render()

        while self.is_running:
            _input = self.terminal.on_input()

            self.handle_input(_input)
            self._render()

        self.terminal.stop_application_mode()
