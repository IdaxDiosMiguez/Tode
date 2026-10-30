from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from Tode.widgets.editor.cursor import Cursor

from abc import ABC, abstractmethod


class Buffer(ABC):

    @abstractmethod
    def get_text(self) -> str: ...

    @abstractmethod
    def get_lines(self) -> list[str]: ...

    @abstractmethod
    def get_offset(self, position: Cursor) -> int: ...

    @abstractmethod
    def insert(self, offset: int, text: str) -> None: ...

    @abstractmethod
    def delete(self, offset: int, length: int) -> None: ...

    @abstractmethod
    def save(self) -> None: ...