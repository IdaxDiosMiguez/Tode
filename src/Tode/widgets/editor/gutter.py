from Tode.utils import ANSI, Color

from functools import lru_cache


class Gutter:

    def __init__(self):
        self.fg = Color("#F5B683").to_ansi(background=False) # #7d956d

        self._last_format = ""
        self._last_format_len = 0

    @staticmethod
    def _padding(line_count: int) -> int:
        return len(str(line_count)) + 1

    @lru_cache(maxsize=1024)
    def width(self, line_count: int) -> int:
        return self._padding(line_count) + 4

    @property
    def len(self):
        return self._last_format_len

    def format(self, number: int, line_count: int, is_current: bool) -> str:
        lead = "▍" if is_current else "▍ "
        trail = "  " + (" " if is_current else "")

        _padding = self._padding(line_count)

        self._last_format = (
            f"{lead}"
            f"{self.fg}{ANSI.BOLD_FONT}"
            f"{number:>{_padding}}"
            f"{ANSI.UNSET_BOLD_FONT}{ANSI.CLEAR_FOREGROUND}"
            f"{trail}"
        )
        self._last_format_len = len(lead) + _padding + len(trail)

        return self._last_format
