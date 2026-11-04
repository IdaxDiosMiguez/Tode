from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from Tode.utils import Coord

from Tode.utils import ANSI
from Tode.utils import BOX
from Tode.utils import Color


class StatusBar:

    def __init__(self, branch_name: str, file_name: str):

        self.branch_name = branch_name
        self.file_name = file_name

        self.bg_status = Color("#343434").to_ansi(background=True)
        self.fg_status = Color("#343434").to_ansi(background=False)

        self.bg_branch = Color("#647C53").to_ansi(background=True)
        self.fg_branch = Color("#e5e7eb").to_ansi(background=False)

        self.bg_file = Color("#4A6E68").to_ansi(background=True)
        self.fg_file = Color("#e5e7eb").to_ansi(background=False)

        self.bg_position = Color("#647C53").to_ansi(background=True)

    def format(self, width: int, cursor: Coord, is_edited: bool) -> str:
        marker = "*" if is_edited else " "

        branch = f"{BOX.LEFT}  {self.branch_name}  {BOX.RIGHT}"
        file = f"{BOX.LEFT} {self.file_name} [{marker}] "
        position = f" Ln {cursor.row}, Col {cursor.col} "

        gap = self.bg_status + " " * max(0, width - len(branch) - len(file) - len(position))

        branch = (
            f"{self.bg_branch}"
            f"{BOX.LEFT}  {self.fg_branch}{self.branch_name}{self.fg_status}  {BOX.RIGHT}"
            f"{ANSI.CLEAR_FOREGROUND}"
        )

        file = (
            f"{self.bg_file}"
            f"{self.fg_status}{BOX.LEFT}{ANSI.CLEAR_FOREGROUND}"
            f" {self.fg_file}{self.file_name} [{marker}] "
            f"{ANSI.CLEAR_BACKGROUND}"
        )

        position = (
            f"{self.bg_position}"
            f"{position}"
        )

        return f"{ANSI.BOLD_FONT}{branch}{file}{gap}{position}{ANSI.UNSET_BOLD_FONT}{ANSI.CLEAR_BACKGROUND}{ANSI.CLEAR_FOREGROUND}"
