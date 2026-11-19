#!/usr/bin/env python3

import argparse

from pathlib import Path

from Tode.widgets import Editor
from Tode.widgets import Explorer

from Tode.app import Tode


def get_args():
    parser = argparse.ArgumentParser(
        prog="Tode", description="Terminal based code editor"
    )

    parser.add_argument(
        "path", help="Path to file/folder/workspace", nargs="?", default="untitled.txt"
    )

    return parser.parse_args()


def get_path(path: str | Path) -> Path:

    if isinstance(path, str):
        path = Path(path).expanduser()

    return path


def main():

    args = get_args()
    path = get_path(args.path)

    editor = Editor(path=path)
    explorer = Explorer(root=path if path.is_dir() else path.parent)

    tode = Tode()

    tode.add_widget(explorer)
    tode.add_widget(editor)

    tode.run()


if __name__ == "__main__":
    main()
