from Tode.utils import ANSI, Color

from functools import lru_cache


class Gutter:

    def __init__(self):
        self.fg = Color("#7d956d").to_ansi(background=False)

    @staticmethod
    def _padding(line_count: int) -> int:
        return len(str(line_count)) + 1

    @lru_cache(maxsize=1024)
    def width(self, line_count: int) -> int:
        return self._padding(line_count) + 4

    def format(self, number: int, line_count: int, is_current: bool) -> str:
        lead = "▍" if is_current else "▍ "
        trail = "  " + (" " if is_current else "")

        return (
            f"{lead}"
            f"{self.fg}{ANSI.BOLD_FONT}"
            f"{number:>{self._padding(line_count)}}"
            f"{ANSI.UNSET_BOLD_FONT}{ANSI.CLEAR_FOREGROUND}"
            f"{trail}"
        )
