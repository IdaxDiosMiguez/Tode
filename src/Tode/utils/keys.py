import re
from enum import StrEnum


_KEY_RE = re.compile(r"\x1b\[[0-9;?]*[ -/]*[@-~]|\x1bO.|\x1b.|.", re.DOTALL)


class KEY(StrEnum):
    BACKSPACE = "\x7f"
    TAB       = "\t"
    ENTER     = "\r"


def split_keys(data: str) -> list[str]:
    return _KEY_RE.findall(data)
