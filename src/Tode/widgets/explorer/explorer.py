from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from Tode.app import Tode

from enum import Enum, auto
from pathlib import Path

from Tode.widgets._widget import Widget
from Tode.widgets import Editor

from Tode.buffer import PieceTable

from Tode.utils import ANSI
from Tode.utils import KEY
from Tode.utils import Size
from Tode.utils import Coord
from Tode.utils import Color

from Tode.utils.ascii import get_file_icon
from Tode.utils.ascii import FOLDER

from .file_system import Tree


class Direction(Enum):
    UP    = auto()
    DOWN  = auto()
    LEFT  = auto()
    RIGHT = auto()


class Explorer(Widget):

    TITLE = "Explorer"

    def __init__(self, app: Tode, root: Path, position: Coord, size: Size | None = None) -> None:
        super().__init__(app=app, size=size, position=position)

        root = root.expanduser().absolute()
        self.app = app
        self.root = Tree(root)
        self.position = position

        self.to_draw = True
        self.draw_once = True

        self.selected = 0
        self.padding = 4
        self.margin = 2

        self.bg_title = Color("#793838").to_ansi(background=True)
        self.fg_title = Color("#e5e7eb").to_ansi(background=False)

        self.bg_explorer = Color("#282828").to_ansi(background=True)
        self.fg_explorer = Color("#e5e7eb").to_ansi(background=False)

        self.bg_selected = Color("#e5e7eb").to_ansi(background=True)
        self.fg_selected = Color("#282828").to_ansi(background=False)

        self.default_style  = f"{self.bg_explorer}{self.fg_explorer}"
        self.selected_style = f"{self.bg_selected}{self.fg_selected}"

        self.title = (
            f"{self.bg_title}"
            f"{self.fg_title}"
            f"{ANSI.BOLD_FONT}"
            " " * self.size.width,
            f"{self.TITLE:^{self.size.width}}"
            f"{ANSI.UNSET_BOLD_FONT}"
            f"{ANSI.CLEAR_FOREGROUND}",
            " " * self.size.width,
            f"{self.bg_explorer}"
            "▔" * self.size.width,
        )

        self._setup_keybinds()

    def _setup_keybinds(self):
        # Arrow binds
        self.bind(ANSI.ARROW_UP,    self._move, Direction.UP)
        self.bind(ANSI.ARROW_DOWN,  self._move, Direction.DOWN)

        self.bind(KEY.ENTER,        self._on_enter)

    def _open_dir(self):
        self.root.toggle(self.selected)
        self._draw_explorer()

    def _open_file(self, path: Path):

        editor = self.app.editor

        editor.buffer = PieceTable(path)
        editor.status_bar.file_name = path.name
        editor.status_bar

        editor.to_draw = True

        editor.render()

        editor.draw_once = False

        self.app.toggle_explorer()

    def _on_enter(self):
        path = Path(self.root.rows[self.selected][0].path)

        if path.is_dir():
            self._open_dir()

        else:
            self._open_file(path)


    def _move(self, direction: Direction):

        tree_size = self.root.size

        match direction:
            case Direction.UP:
                self.selected = max(self.selected - 1, 0)

            case Direction.DOWN:
                self.selected = min(self.selected + 1, tree_size - 1)

        self.to_draw = True

    def _draw_title(self):

        for idx, line in enumerate(self.title):

            self.terminal.move_to(
                self.position.col,
                self.position.row + idx
            )

            self.terminal.write(line)

        self.draw_once = False

    def _draw_explorer(self):
        _width, height = self.terminal.get_terminal_size()

        col = self.position.col
        top = self.position.row + len(self.title)

        visible = max(height - top + 1, 0)
        empty_line = " " * self.size.width

        rows = self.root.rows[:visible]

        for row, (node, depth) in enumerate(rows):
            self.terminal.move_to(col, top + row)

            if node.is_dir:
                icon = (f"{FOLDER.OPEN} " if node.expanded else f"{FOLDER.CLOSED} ")

            else:
                ext = node.name[node.name.rfind("."):]
                icon = f"{get_file_icon(ext)} "

            style = self.selected_style if (row == self.selected) and self.is_active else self.default_style

            name = node.name[: max(self.size.width - 4 - depth, 0)]
            pad = " " * max(self.size.width - 4 - depth - len(name), 0)

            entry = f"{" " * self.margin}{" " * depth}{icon}{style}{name}{self.default_style}{pad}"

            self.terminal.write(
                f"{self.default_style}{entry}{ANSI.CLEAR_STYLE}"
            )

        for row in range(len(rows), visible):
            self.terminal.move_to(col, top + row)
            self.terminal.write(f"{self.default_style}{empty_line}{ANSI.CLEAR_STYLE}")

        self.to_draw = False

    def render(self):

        if self.draw_once:
            self._draw_title()
            self._draw_explorer

        if self.to_draw:
            self._draw_explorer()
