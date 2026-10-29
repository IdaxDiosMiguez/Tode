from typing import Any

import re
import os
import sys
import tty
import shutil
import termios

from Tode.utils import ANSI

from Tode.drivers._driver import Driver
from Tode.drivers._writer_thread import WriterThread


__all__ = (
    "LinuxDriver",
)


class LinuxDriver(Driver):

    def __init__(self):

        if sys.__stdin__ is None:
            raise SystemError("App crashed due to terminal not being active!")

        self._file = sys.__stderr__
        self._fileno = sys.__stdin__.fileno()
        self._attrs_before: list[Any] | None = None
        self._writer_thread: WriterThread | None = None
        self._cursor_pos: tuple[int, int] = (1, 1)

        self._data: str = ""

    @classmethod
    def _patch_lflag(cls, attrs: int) -> int:
        return attrs & ~(
              termios.ECHO
            | termios.ICANON
            | termios.IEXTEN
            | termios.ISIG
        )

    @classmethod
    def _patch_iflag(cls, attrs: int) -> int:
        return attrs & ~(
              termios.IXON
            | termios.IXOFF
            | termios.ICRNL
            | termios.INLCR
            | termios.IGNCR
        )

    def _store_old_attributes(self) -> None:
        try:
            self._attrs_before = termios.tcgetattr(self._fileno)

        except termios.error:
            self._attrs_before = None

    def _define_new_attributes(self) -> None:
        try:
            newattr = termios.tcgetattr(self._fileno)

        except termios.error:
            pass

        else:
            newattr[tty.LFLAG] = self._patch_lflag(newattr[tty.LFLAG])
            newattr[tty.IFLAG] = self._patch_iflag(newattr[tty.IFLAG])

            newattr[tty.CC][termios.VMIN] = 1

            try:
                termios.tcsetattr(self._fileno, termios.TCSANOW, newattr)

            except termios.error:
                pass

    def _check_tty(self) -> None:
        if os.isatty(self._fileno):
            try:
                termios.tcsetattr(self._fileno, termios.TCSANOW, termios.tcgetattr(self._fileno))

            except termios.error:
                return

    def start_application_mode(self) -> None:

        self._check_tty()
        self._store_old_attributes()

        if not self._file:
            raise ValueError("Terminal doesn't exist!")

        self._writer_thread = WriterThread(self._file)
        self._writer_thread.start()

        self.write(ANSI.ENTER_ALT_SCREEN)
        self._define_new_attributes()
        self.write(ANSI.CLEAR)

        self.flush()

    def stop_application_mode(self) -> None:

        if self._writer_thread:
            self.write(ANSI.CLEAR)
            self.write(ANSI.EXIT_ALT_SCREEN)
            self.write(ANSI.SHOW_CURSOR)

            self._writer_thread.stop()
            self._writer_thread = None

        if self._attrs_before:
            termios.tcsetattr(self._fileno, termios.TCSAFLUSH, self._attrs_before)

    def on_input(self) -> str:
        try:
            data = os.read(self._fileno, 1024).decode("utf-8", errors="ignore")

            if not data:
                return ""

            cpr_match = re.search(r"\x1b\[(\d+);(\d+)R", data)

            if cpr_match:
                self._cursor_pos = (int(cpr_match.group(1)), int(cpr_match.group(2)))
                data = re.sub(r"\x1b\[\d+;\d+R", "", data)

            return data


        except Exception:
            self.stop_application_mode()
            return ""

    def write(self, data: str) -> None:
        assert self._writer_thread is not None, "Driver must be started before using the writer thread"
        self._writer_thread.write(data)

    def move_to(self, col: int, row: int) -> None:
        self.write(f"{ANSI.ESC}[{row};{col}H")

    def disable_input(self) -> None:
        "TODO"

    def get_cursor_pos(self) -> tuple[int, int]:
        return self._cursor_pos

    def get_terminal_size(self) -> tuple[int, int]:
        return shutil.get_terminal_size()
