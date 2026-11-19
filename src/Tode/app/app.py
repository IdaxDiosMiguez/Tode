from typing import Any

import signal
import asyncio

from dataclasses import dataclass
from os import terminal_size

from Tode.drivers import LinuxDriver
from Tode.widgets._widget import Widget

from Tode.core import Model
from Tode.core import Focus
from Tode.core.actions import *

from Tode.utils import ANSI
from Tode.utils import Keybind
from Tode.utils import Keybinds
from Tode.utils import split_keys


@dataclass(slots=True)
class Frame:
    rows: list[str]
    cursor: tuple[int, int] | None = None


class Tode:

    EXPLORER_WIDTH = 25

    KEYBINDS: Keybinds = {
        Keybind("CTRL+X"): Quit(),
        Keybind("CTRL+E"): ToggleEditor()
    }

    def __init__(self):
        self.model  = Model()
        self.driver = LinuxDriver()
        self.queue  = asyncio.Queue()

        self._prev: list[str] = []

    def _layout(self) -> list[tuple[Focus, int, int]]:
        layout, col = [], 1

        if Focus.EXPLORER in self.model.widgets:
            layout.append((Focus.EXPLORER, col, self.EXPLORER_WIDTH))
            col += self.EXPLORER_WIDTH

        if Focus.EDITOR in self.model.widgets:
            layout.append((Focus.EDITOR, col, max(1, self.model.size.columns - col + 1)))

        return layout

    def _resize(self, size: terminal_size):
        self.model.size = size
        self._prev = []

        for focus, _col, width in self._layout():
            self._send(self.model.widgets[focus], Resize(terminal_size((width, size.lines))))

    def _on_input(self):
        for key in split_keys(self.driver.on_input()):
            self._dispatch(Key(key))

    def _spawn(self, cmd):
        async def run():
            if (msg := await cmd()) is not None:
                self._dispatch(msg)

        asyncio.create_task(run())

    def _view(self) -> Frame:
        height = self.model.size.lines
        rows = [""] * height
        cursor = None

        for focus, col, _width in self._layout():
            view = self.model.widgets[focus].view(focused=self.model.focus is focus)

            for i, line in enumerate(view.lines[:height]):
                rows[i] += f"{ANSI.ESC}[{col}G{line}"

            if view.cursor is not None:
                cursor = (view.cursor[0] + col - 1, view.cursor[1])

        return Frame(rows, cursor)

    def _draw(self):
        f = self._view()
        out: list[str] = [ANSI.START_SYNC, ANSI.HIDE_CURSOR]

        if not self._prev:
            out.append(ANSI.CLEAR)

        for i, row in enumerate(f.rows, 1):
            if i > len(self._prev) or row != self._prev[i - 1]:
                out.append(f"{ANSI.ESC}[{i};1H{row}")

        if f.cursor:
            out += [f"{ANSI.ESC}[{f.cursor[1]};{f.cursor[0]}H", ANSI.SHOW_CURSOR]

        out.append(ANSI.END_SYNC)
        self.driver.write("".join(out))
        self._prev = f.rows

    def _dispatch(self, msg):
        self.queue.put_nowait(msg)

    def _send(self, widget, action):
        if action is not None:
            self._update(widget.update(action))

    def _update(self, msg):
        match msg:
            case None: return
            case Key(key) if key in self.KEYBINDS:
                self._update(self.KEYBINDS[key])

            case Key(key):
                widget = self.model.focused
                if widget is None:
                    return
                self._send(widget, widget.keymap(key))

            case OpenFile():
                if (editor := self.model.widgets.get(Focus.EDITOR)) is not None:
                    self._send(editor, msg)
                    self.model.focus = Focus.EDITOR

            case Quit():          self.model.running = False
            case ToggleEditor():  self.model.toggle_editor()
            case Resize(size):    self._resize(size)

    async def _run(self):
        self.driver.start_application_mode()

        loop = asyncio.get_running_loop()

        loop.add_reader(self.driver.fileno, self._on_input)
        loop.add_signal_handler(signal.SIGWINCH, lambda: self._dispatch(Resize(self.driver.get_terminal_size())))

        self._resize(self.driver.get_terminal_size())
        self._draw()

        try:
            while self.model.running:
                self._update(await self.queue.get())

                while self.model.running and not self.queue.empty():
                    self._update(self.queue.get_nowait())

                if self.model.running:
                    self._draw()

        finally:
            loop.remove_reader(self.driver.fileno)
            self.driver.stop_application_mode()

    def add_widget(self, widget: Widget):
        self.model.add_widget(widget)

    def run(self):
        asyncio.run(self._run())
