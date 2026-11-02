from Tode.utils import ANSI, Color


class StatusBar:

    def __init__(self):
        self.bg = Color("#6f583e").to_ansi(background=True)

    def format(self, width: int, buffer, cursor) -> str:
        name = buffer.path.name if buffer.path else "unnamed"
        marker = "*" if buffer.edited else ""

        left = f" MAIN     {name}{marker}"
        right = f"Ln {cursor.row}, Col {cursor.col} "
        gap = " " * max(0, width - len(left) - len(right))

        return f"{self.bg}{left}{gap}{right}{ANSI.CLEAR_BACKGROUND}"
