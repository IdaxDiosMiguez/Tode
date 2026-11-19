from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from os import terminal_size
    from pathlib import Path

from dataclasses import dataclass
from Tode.utils import Action


@dataclass(frozen=True, slots=True)
class Key(Action):
    key: str            # one raw key, not yet interpreted

@dataclass(frozen=True, slots=True)
class Resize(Action):
    size: terminal_size

@dataclass(frozen=True, slots=True)
class OpenFile(Action):
    path: Path

class Quit(Action): ...
class ToggleEditor(Action): ...
