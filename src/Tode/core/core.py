from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from Tode.widgets._widget import Widget

from enum import Enum, auto
from dataclasses import dataclass, field
from os import get_terminal_size, terminal_size


class Focus(Enum):
    EDITOR = auto()
    EXPLORER = auto()


_TOGGLE = {
    Focus.EDITOR: Focus.EXPLORER,
    Focus.EXPLORER: Focus.EDITOR
}


@dataclass(slots=True)
class Model:
    widgets: dict[Focus, Widget] = field(default_factory=dict)
    size: terminal_size = get_terminal_size()
    focus: Focus = Focus.EDITOR
    running: bool = True

    @property
    def focused(self) -> Widget | None:
        return self.widgets.get(self.focus)

    def add_widget(self, widget: Widget):
        self.widgets[widget.focus] = widget

    def toggle_editor(self):
        target = _TOGGLE[self.focus]
        if target in self.widgets:
            self.focus = target
