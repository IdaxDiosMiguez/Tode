from typing import Callable, Iterable, Any, TypedDict

from Tode.utils import Keybind


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
        bind = self.keybinds.get(input)

        if not bind:
            return False

        action = bind.get("action")
        args = bind.get("args")

        if not action:
            return False

        if args:
            action(args)
        else:
            action()

        return True
