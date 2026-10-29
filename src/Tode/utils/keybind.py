

class Keybind():
    r"""
    Keybind example:
    >>> Keybind("CTRL+Q") == '\x11'
    >>> True

    """

    def __init__(self, keybind: str):
        self.keybind = self._to_ansi(keybind)

    def _to_ansi(self, keybind) -> str:
        keybind = keybind.replace(" ", "").upper()
        keys = keybind.split("+")

        has_ctrl  = False
        has_shift = False

        if not (2 <= len(keys) <= 3):
            raise ValueError("Keybind wasn't formulated correctly!")

        if "CTRL" in keys:
            has_ctrl = True

        if "SHIFT" in keys:
            has_shift = True

        if has_ctrl:
            return self._get_ctrl_keybind(keys[-1])

        raise ValueError("Keybind wasn't formulated correctly!")

    def _get_ctrl_keybind(self, key: str) -> str:
        if "A" <= key <= "Z":
            return chr(ord(key) - 64)

        raise ValueError("Only letters A-Z are supported for CTRL keybinds")

    def __eq__(self, other: str) -> bool:
        return self.keybind == other if isinstance(other, str) else False

    def __hash__(self) -> int:
        return hash(self.keybind)

    def __str__(self) -> str:
        return self.keybind
