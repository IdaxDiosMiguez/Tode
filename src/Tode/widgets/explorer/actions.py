from dataclasses import dataclass

from Tode.utils import Action


@dataclass(frozen=True)
class Select(Action): delta: int

class Activate(Action): ...
