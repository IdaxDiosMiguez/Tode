from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .file_system import _Node

from pathlib import Path

from Tode.widgets._widget import Widget, View

from Tode.utils import ANSI
from Tode.utils import KEY
from Tode.utils import Color
from Tode.utils import Keybinds

from Tode.utils.ascii import get_file_icon
from Tode.utils.ascii import FOLDER

from Tode.core import Focus
from Tode.core import OpenFile, Resize

from .file_system import Tree
from .actions import *


class Explorer(Widget):

    TITLE = "Explorer"

    KEYBINDS: Keybinds = {
        ANSI.ARROW_UP:   Select(-1),
        ANSI.ARROW_DOWN: Select(+1),
        KEY.ENTER:       Activate(),
    }

    def __init__(self, root: Path) -> None:
        self.tree = Tree(root.expanduser().absolute())
        self.selected = 0

        self.focus = Focus.EXPLORER

        self.width, self.height = 25, 24
        self.margin = 2

        self.bg_title = Color("#793838").to_ansi(background=True)
        self.fg_title = Color("#e5e7eb").to_ansi(background=False)

        self.bg_explorer = Color("#282828").to_ansi(background=True)
        self.fg_explorer = Color("#e5e7eb").to_ansi(background=False)

        self.bg_selected = Color("#e5e7eb").to_ansi(background=True)
        self.fg_selected = Color("#282828").to_ansi(background=False)

        self.default_style  = f"{self.bg_explorer}{self.fg_explorer}"
        self.selected_style = f"{self.bg_selected}{self.fg_selected}"

    # --- update -----------------------------------------------------------

    def update(self, action):
        match action:
            case Select(delta):
                self.selected = max(0, min(self.selected + delta, self.tree.size - 1))

            case Activate():
                path = Path(self.tree.rows[self.selected][0].path)

                if path.is_dir():
                    self.tree.toggle(self.selected)
                else:
                    return OpenFile(path)

            case Resize(size):
                self.width, self.height = size

        return None

    # --- view -------------------------------------------------------------

    def _title(self) -> list[str]:
        w = self.width

        return [
            f"{self.bg_title}{self.fg_title}{ANSI.BOLD_FONT}{' ' * w}{ANSI.UNSET_BOLD_FONT}{ANSI.CLEAR_STYLE}",
            f"{self.bg_title}{self.fg_title}{ANSI.BOLD_FONT}{self.TITLE:^{w}}{ANSI.UNSET_BOLD_FONT}{ANSI.CLEAR_STYLE}",
            f"{self.bg_title}{' ' * w}{ANSI.CLEAR_STYLE}",
            f"{self.bg_explorer}{'▔' * w}{ANSI.CLEAR_STYLE}",
        ]

    def _entry(self, node: _Node, depth: int, selected: bool) -> str:
        if node.is_dir:
            icon = f"{FOLDER.OPEN} " if node.expanded else f"{FOLDER.CLOSED} "
        else:
            icon = f"{get_file_icon(node.name[node.name.rfind('.'):])} "

        style = self.selected_style if selected else self.default_style

        name = node.name[: max(self.width - 4 - depth, 0)]
        pad = " " * max(self.width - 4 - depth - len(name), 0)

        entry = f"{' ' * self.margin}{' ' * depth}{icon}{style}{name}{self.default_style}{pad}"

        return f"{self.default_style}{entry}{ANSI.CLEAR_STYLE}"

    def view(self, focused: bool) -> View:
        rows = self._title()

        visible = max(self.height - len(rows), 0)
        entries = self.tree.rows[:visible]

        for idx, (node, depth) in enumerate(entries):
            rows.append(self._entry(node, depth, focused and idx == self.selected))

        rows += [f"{self.default_style}{' ' * self.width}{ANSI.CLEAR_STYLE}"] * (visible - len(entries))

        return View(rows)
