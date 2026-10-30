from typing import TYPE_CHECKING, Literal

if TYPE_CHECKING:
    from Tode.widgets.editor.cursor import Cursor

from ._buffer import Buffer

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class _Piece:
    buffer_type: Literal["original", "add"]
    start_index: int
    length: int


class PieceTable(Buffer):
    def __init__(self, path: Path) -> None:

        self.path = path
        self.original_text: str = self.path.read_text() if self.path.exists() else ""
        self.add_buffer: str = ""
        self.edited: bool = False

        self._line_cache: list[str] | None = None

        self.pieces: list[_Piece] = (
            [_Piece("original", 0, len(self.original_text))]
            if self.original_text
            else []
        )

    def get_text(self) -> str:
        result = []
        for piece in self.pieces:
            buffer = (
                self.original_text
                if piece.buffer_type == "original"
                else self.add_buffer
            )
            result.append(buffer[piece.start_index : piece.start_index + piece.length])
        return "".join(result)

    def get_lines(self):
        if self._line_cache is None:
            self._line_cache = self.get_text().split("\n")

        return self._line_cache

    def get_offset(self, cursor: Cursor) -> int:
        if self._line_cache is None:
            self._line_cache = self.get_text().split("\n")

        lines = self._line_cache
        row_idx = cursor.row - 1
        col_idx = cursor.col - 1

        offset = sum(len(line) + 1 for line in lines[:row_idx])

        if row_idx < len(lines):
            line_len = len(lines[row_idx])
            col_idx = line_len if col_idx > line_len else col_idx

        return offset + col_idx

    def insert(self, offset: int, text: str) -> None:
        if not text:
            return

        self.edited = True
        self._line_cache = None

        add_start = len(self.add_buffer)
        self.add_buffer += text
        new_piece = _Piece("add", add_start, len(text))

        if offset == 0:
            self.pieces.insert(0, new_piece)
            return

        current_offset = 0
        for i, piece in enumerate(self.pieces):
            if current_offset <= offset <= current_offset + piece.length:
                left_len = offset - current_offset
                right_len = piece.length - left_len

                new_sequence: list[_Piece] = []

                if left_len > 0:
                    new_sequence.append(
                        _Piece(piece.buffer_type, piece.start_index, left_len)
                    )

                new_sequence.append(new_piece)

                if right_len > 0:
                    new_sequence.append(
                        _Piece(
                            piece.buffer_type,
                            piece.start_index + left_len,
                            right_len,
                        )
                    )

                self.pieces[i : i + 1] = new_sequence
                return

            current_offset += piece.length

        self.pieces.append(new_piece)

    def delete(self, offset: int, length: int) -> None:
        if length <= 0 or not self.pieces:
            return

        self.edited = True
        self._line_cache = None

        end_offset = offset + length
        current_offset = 0
        new_pieces: list[_Piece] = []

        for piece in self.pieces:
            piece_end = current_offset + piece.length

            if piece_end <= offset or current_offset >= end_offset:
                new_pieces.append(piece)
            else:
                if current_offset < offset:
                    left_len = offset - current_offset
                    new_pieces.append(
                        _Piece(piece.buffer_type, piece.start_index, left_len)
                    )

                if piece_end > end_offset:
                    right_len = piece_end - end_offset
                    right_start = piece.start_index + (end_offset - current_offset)
                    new_pieces.append(_Piece(piece.buffer_type, right_start, right_len))

            current_offset += piece.length

        self.pieces = new_pieces

    def save(self) -> None:
        text = self.get_text()

        if self.path.parent and not self.path.parent.exists():
            self.path.parent.mkdir(parents=True, exist_ok=True)

        self.path.write_text(text)

        self.original_text = text
        self.add_buffer = ""
        self.edited = False
        self._line_cache = None
        self.pieces = [_Piece("original", 0, len(text))] if text else []
