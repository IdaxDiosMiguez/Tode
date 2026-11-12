def _char_class(ch: str) -> int:
    if ch.isspace():
        return 0

    if ch.isalnum() or ch == "_":
        return 1

    return 2

def next_word(line: str, idx: int):
    n = len(line)

    if idx < n and (kind := _char_class(line[idx])):
        while idx < n and _char_class(line[idx]) == kind:
            idx += 1

    while idx < n and line[idx].isspace():
        idx += 1

    return idx

def prev_word(line: str, idx: int) -> int:

    if idx > 0 and (kind := _char_class(line[idx - 1])):
        while idx > 0 and _char_class(line[idx - 1]) == kind:
            idx -= 1

    while idx > 0 and line[idx - 1].isspace():
        idx -= 1
    return idx

def next_block(lines: list[str], idx: int) -> int:
    n = len(lines)
    while idx < n and lines[idx].strip():
        idx += 1
    while idx < n and not lines[idx].strip():
        idx += 1
    return min(idx, n - 1)


def prev_block(lines: list[str], idx: int) -> int:
    idx -= 1
    while idx >= 0 and not lines[idx].strip():
        idx -= 1
    while idx > 0 and lines[idx - 1].strip():
        idx -= 1
    return max(idx, 0)