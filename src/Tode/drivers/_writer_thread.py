from __future__ import annotations

import threading
from queue import Queue
from typing import TextIO

from typing import Final


__all__ = (
    "WriterThread",
)


MAX_QUEUED_WRITES: Final[int] = 30


class WriterThread(threading.Thread):

    def __init__(self, file: TextIO) -> None:
        super().__init__(daemon=True)
        self._queue: Queue[str | None] = Queue(MAX_QUEUED_WRITES)
        self._file = file

    def write(self, text: str) -> None:
        self._queue.put(text)

    def fileno(self) -> int:
        return self._file.fileno()

    def run(self) -> None:
        while True:
            text: str | None = self._queue.get()

            if text is None:
                break

            self._file.write(text)

            if self._queue.qsize() == 0:
                self._file.flush()

        self._file.flush()

    def stop(self) -> None:
        self._queue.put(None)
        self.join()
