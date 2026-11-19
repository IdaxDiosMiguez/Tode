from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from Tode.core import Focus
    from Tode.utils import Action
    from Tode.utils import Keybinds

from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass(slots=True)
class View:
    """What a widget looks like right now: one string per row of its region."""

    lines: list[str]
    cursor: tuple[int, int] | None = None   # (col, row) inside the region, 1-based. None = hidden


class Widget(ABC):

    KEYBINDS: Keybinds = {}
    focus: Focus

    def keymap(self, key: str) -> Action | None:
        return self.KEYBINDS.get(key)

    @abstractmethod
    def update(self, action: Action) -> Action | None: ...

    @abstractmethod
    def view(self, focused: bool) -> View: ...
