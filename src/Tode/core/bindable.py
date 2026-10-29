from typing import TYPE_CHECKING, Callable, Generic

from Tode.utils import Keybind


type Bind = Keybind | str

class Bindable:

    def __init__(self) -> None:
        self.keybinds: dict[Bind, Callable]

    def bind(self, keybind: Bind, action: Callable) -> None:
        self.keybinds[keybind] = action

    def handle_input(self, input: str) -> bool:
        action = self.keybinds.get(input)
        if action:
            action()
            return True
        return False