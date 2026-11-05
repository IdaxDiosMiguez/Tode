from enum import StrEnum


class BOX(StrEnum):
    LEFT  = "🯏"
    RIGHT = "🮈"

class ARROW(StrEnum):
    RIGHT = ""

class FOLDER(StrEnum):
    CLOSED = "󰅂"
    OPEN   = "󰅀"

class FILES(StrEnum):
    DEFAULT = ""
    PYTHON  = "󰌠"

EXTENSIONS = {
    ".py": FILES.PYTHON,
    ".pyi": FILES.PYTHON
}

def get_file_icon(extension: str):
    icon = EXTENSIONS.get(extension, None)
    return FILES.DEFAULT if icon is None else icon