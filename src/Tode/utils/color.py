from __future__ import annotations
from typing import Sequence


__all__ = (
    "Color",
)


class Color(tuple):

    """A class to represent a color.

    Colors are stored as three values representing the degree of red, green, and blue in a color, and a
    fourth "alpha" value which defines where the color lies on a gradient of opaque to transparent.

    Example:
        ```python
        >>> color = Color(255, 0, 0)
        >>> color
        Color(255, 0, 0, 1.0)
        >>> color = Color("#FF000000")
        >>> color
        Color(255, 0, 0, 0.0)
        ```
    """

    def __new__(cls, *value: str | int | float):

        if len(value) == 1 and isinstance(value[0], str):
            _rgba: tuple[int, int, int, float] = cls._from_hex(value[0])

        elif 3 <= len(value) <= 4:
            _rgba = cls._from_rgba(value)

        else:
            raise TypeError("Color expects RGBA or a HEX string")


        return super().__new__(cls, _rgba)

    @property
    def red(self) -> int:
        return self[0]

    @property
    def green(self) -> int:
        return self[1]

    @property
    def blue(self) -> int:
        return self[2]

    @property
    def alpha(self) -> float:
        return self[3]

    def to_ansi(self, true_color: bool = True, background: bool = True):
        to_color = 48 if background else 38
        format = 2 if true_color else 2

        return f"\x1b[{to_color};{format};{self.red};{self.green};{self.blue}m"

    def __repr__(self) -> str:
        return f"Color(r={self.red}, g={self.green}, b={self.blue}, a={self.alpha})"

    @staticmethod
    def _from_rgba(value: Sequence) -> tuple[int, int, int, float]:
        if not all(isinstance(v, int) for v in value[:3]):
            raise ValueError("Color expects RGBA integers")

        r, g, b = value[:3]
        a = value[3] if len(value) == 4 else 1.0

        if not all(0 <= v <= 255 for v in (r, g, b)):
            raise ValueError("RGB values must be integers between 0 and 255")

        if not (0 <= a <= 1):
            raise ValueError("Alpha must be between 0.0 and 1.0")

        return (r, g, b, float(a))

    @staticmethod
    def _from_hex(value: str)  -> tuple[int, int, int, float]:

        RED   = slice(0, 2)
        GREEN = slice(2, 4)
        BLUE  = slice(4, 6)
        ALPHA = slice(6, 8)

        if not value.startswith("#"):
            raise ValueError("Hex colors must start with '#'")

        hex_val = value.lstrip('#')

        if len(hex_val) not in (6, 8):
            raise ValueError("Hex color must be #RRGGBB or #RRGGBBAA")

        try:
            r = int(hex_val[RED], 16)
            g = int(hex_val[GREEN], 16)
            b = int(hex_val[BLUE], 16)
            a = int(hex_val[ALPHA], 16) / 255 if len(hex_val) == 8 else 1.0

        except ValueError:
            raise ValueError(f"Invalid hexdecimal characters in color: '{value}'")

        return (r, g, b, a)
