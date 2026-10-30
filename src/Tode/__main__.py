#!/usr/bin/env python3

import argparse

from pathlib import Path

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

    tode = Tode(path=path)
    tode.run()


if __name__ == "__main__":
    main()
