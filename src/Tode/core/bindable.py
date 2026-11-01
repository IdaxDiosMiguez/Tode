from typing import Callable, Iterable, Any, TypedDict

from Tode.utils import Keybind
from Tode.utils import KEY


type Bind = Keybind | str
type Args = Any

class ActionMapping(TypedDict):
    action: Callable[..., Any]
    args: Args


class Bindable:

    def __init__(self) -> None:
        self.keybinds: dict[Bind, ActionMapping] = {}

    def bind(self, keybind: Bind, action: Callable[..., Any], args: Args = None) -> None:
        self.keybinds[keybind] = {"action": action, "args": args}

    def handle_input(self, input: str) -> bool:
        char = input
        bind = self.keybinds.get(char)

        if not bind and len(char) == 1 and char.isprintable():
            char = KEY.CHAR
            bind = self.keybinds.get(KEY.CHAR)

        if not bind:
            return False

        action = bind.get("action")
        args = bind.get("args")

        if not action:
            return False

        if char == KEY.CHAR:
            action(input)

        elif args:
            action(args)

        else:
            action()

        return True
