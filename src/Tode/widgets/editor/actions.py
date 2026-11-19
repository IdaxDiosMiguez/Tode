from dataclasses import dataclass

from enum import Enum, auto

from Tode.utils import Action


class Direction(Enum):
    UP    = auto()
    DOWN  = auto()
    LEFT  = auto()
    RIGHT = auto()


@dataclass(frozen=True)
class Move(Action): direction: Direction

@dataclass(frozen=True)
class InsertChar(Action): ch: str

class InsertNewLine(Action): ...
class DeleteChar(Action):    ...
class MoveWord(Action):      ...
class Save(Action):          ...
