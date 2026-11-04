from typing import TYPE_CHECKING, Iterable

if TYPE_CHECKING:
    from Tode.app import Tode

from pathlib import Path
from functools import lru_cache

from Tode.widgets._widget import Widget

from Tode.utils import ANSI
from Tode.utils import Size
from Tode.utils import Coord
from Tode.utils import Color


example_list = (
    "1. reporte_final_2026.pdf",
    "2. foto_vacaciones_010.jpg",
    "3. index.html",
    "4. analisis_datos.xlsx",
    "5. logo_empresa.png",
    "6. notas_reunion.txt",
    "7. cancion_favorita.mp3",
    "8. script_automatizacion.py",
    "9. presentacion_proyecto.pptx",
    "10. backup_sistema.zip"
)


class Explorer(Widget):

    TITLE = "Explorer"

    def __init__(self, app: Tode, root: Path, position: Coord, size: Size | None = None) -> None:
        super().__init__(app=app, size=size, position=position)

        self.root = root
        self.position = position

        self.to_draw = True
        self.draw_once = True

        self.padding = 4

        self.bg_title = Color("#793838").to_ansi(background=True)
        self.fg_title = Color("#e5e7eb").to_ansi(background=False)
        self.bg_explorer = Color("#282828").to_ansi(background=True)
        self.fg_explorer = Color("#e5e7eb").to_ansi(background=False)

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

    def _get_path_name(self, path: Path):
        # TODO work with dirs (File only for now)

        path_name = path.name

        if path_name.startswith("."):
            return False

        path_name_len = len(path_name)

        padded_len = self.size.width - self.padding

        if path_name_len <= padded_len:
            return path_name

        return f"{path_name[:padded_len - 3]}..."

    def get_file_names(self, file_system: Iterable[Path]):
        return filter(None, map(self._get_path_name, file_system))

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
        title_len = len(self.title)
        empty_line = " " * self.size.width
        idx = title_len

        if not self.root.is_dir():
            self.terminal.move_to(
                self.position.col,
                self.position.row + idx
            )

            self.terminal.write(
                f"{self.bg_explorer}"
                f"{self.fg_explorer}"
                f"  {self.root.name:<{self.size.width - 2}}"
                f"{ANSI.CLEAR_BACKGROUND}"
                f"{ANSI.CLEAR_FOREGROUND}"
            )

        else:
            files = self.get_file_names(self.root.iterdir())

            for idx, item in enumerate(files, title_len):

                self.terminal.move_to(
                    self.position.col,
                    self.position.row + idx
                )

                self.terminal.write(
                    f"{self.bg_explorer}"
                    f"{self.fg_explorer}"
                    f"  {item:<{self.size.width - 2}}"
                    f"{ANSI.CLEAR_BACKGROUND}"
                    f"{ANSI.CLEAR_FOREGROUND}"
                )

        for row in range(idx + 1, height + 1):
            self.terminal.move_to(
                self.position.col,
                self.position.row + row
            )

            self.terminal.write(f"{self.bg_explorer} {empty_line} {ANSI.CLEAR_BACKGROUND}")

        self.to_draw = False

    def render(self):

        if self.draw_once:
            self._draw_title()

        if self.to_draw:
            self._draw_explorer()
