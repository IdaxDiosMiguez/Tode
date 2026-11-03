from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from Tode.widgets.editor.cursor import Cursor

from Tode.utils import ANSI
from Tode.utils import BOX
from Tode.utils import Color


class StatusBar:

    def __init__(self, branch_name: str, file_name: str):

        self.branch_name = branch_name
        self.file_name = file_name

        self.cl_status = Color("#343434")
        self.bg_status = self.cl_status.to_ansi(background=True)
        self.fg_status = self.cl_status.to_ansi(background=False)

        self.cl_branch = Color("#6f583e")
        self.bg_branch = self.cl_branch.to_ansi(background=True)

        self.cl_file = Color("#4A6E68")
        self.bg_file = self.cl_file.to_ansi(background=True)


    def format(self, width: int, cursor: Cursor, is_edited: bool) -> str:
        marker = "*" if is_edited else " "

        branch = f"{BOX.LEFT}  {self.branch_name}  {BOX.RIGHT}"
        file = f"{BOX.LEFT} {self.file_name} [{marker}] "
        position = f"Ln {cursor.row}, Col {cursor.col} "

        gap = " " * max(0, width - len(branch) - len(file) - len(position))

        branch = (
            f"{self.bg_branch}"
            f"{BOX.LEFT}  {self.branch_name}  {self.fg_status}{BOX.RIGHT}"
            f"{ANSI.CLEAR_FOREGROUND}"
        )

        file = (
            f"{self.bg_file}"
            f"{self.fg_status}{BOX.LEFT}{ANSI.CLEAR_FOREGROUND}"
            f" {self.file_name} [{marker}] "
            f"{ANSI.CLEAR_BACKGROUND}"
        )

        return f"{branch}{file}{self.bg_status}{gap}{position}{ANSI.CLEAR_BACKGROUND}"
