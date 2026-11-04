from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from Tode.app import Tode

from abc import abstractmethod

from Tode.core import Bindable

from Tode.utils import Size
from Tode.utils import Coord


class Widget(Bindable):

    def __init__(self, app: Tode, position: Coord, size: Size | None = None) -> None:
        super().__init__()
        self.terminal = app.terminal
        self.is_active = False
        self.to_draw = False

        self.size = Size(1, 1) if (size is None) else size
        self.position = position

    @abstractmethod
    def render(self):...