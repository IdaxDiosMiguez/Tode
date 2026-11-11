from __future__ import annotations
from typing import TYPE_CHECKING, Callable

if TYPE_CHECKING:
    from pathlib import Path

from dataclasses import dataclass, field

import os


type Depth = int
type Entry = tuple[_Node, Depth]


@dataclass(slots=True, eq=False)
class _Node:
    path: str
    name: str
    is_dir: bool
    expanded: bool = False
    children: list[_Node] | None = field(default=None, repr=False)


class Tree:

    def __init__(self, root: Path | str, show_hidden: bool = False) -> None:
        root = os.fspath(root)

        self.root = _Node(root, os.path.basename(root) or root, True)
        self.show_hidden = show_hidden

        self.rows: list[Entry] = [(self.root, 0)]

        self.expand(0)

    @property
    def size(self):
        return len(self.rows)

    def _load(self, node: _Node) -> None:
        dirs, files = [], []

        try:
            with os.scandir(node.path) as entries:
                for entry in entries:

                    if not self.show_hidden and entry.name.startswith("."):
                        continue

                    try:
                        is_dir = entry.is_dir(follow_symlinks=False)

                    except OSError:
                        is_dir = False

                    child = _Node(entry.path, entry.name, is_dir)

                    (dirs if is_dir else files).append(child)
        except OSError:
            pass

        key: Callable[[_Node], str] = lambda n: n.name.lower()

        dirs.sort(key=key)
        files.sort(key=key)

        node.children = dirs + files

    def _flatten(self, children: list[_Node] | None, depth: int) -> list[Entry]:
        out = []

        if children is None:
            return out

        for child in children:
            out.append((child, depth))

            if child.is_dir and child.expanded and child.children:
                out.extend(self._flatten(child.children, depth + 1))

        return out

    def expand(self, row: int) -> None:
        node, depth = self.rows[row]

        if not node.is_dir or node.expanded:
            return

        node.expanded = True

        if node.children is None:
            self._load(node)


        self.rows[row + 1: row + 1] = self._flatten(node.children, depth + 1)

    def collapse(self, row: int) -> None:
        node, depth = self.rows[row]

        if not node.expanded:
            return

        node.expanded = False

        idx = row + 1

        rows_len = len(self.rows)

        while idx < rows_len and self.rows[idx][1] > depth:
            idx += 1

        del self.rows[row + 1 : idx]

    def toggle(self, row: int) -> None:
        node, _ = self.rows[row]

        if node.expanded:
            self.collapse(row)
        else:
            self.expand(row)
