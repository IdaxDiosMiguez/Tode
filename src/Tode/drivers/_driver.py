from abc import ABC, abstractmethod


__all__ = (
    "Driver",
)


class Driver(ABC):

    @abstractmethod
    def start_application_mode(self):...

    @abstractmethod
    def stop_application_mode(self):...

    def suspend_application_mode(self):
        self.stop_application_mode()
        self.close()

    def resume_application_mode(self) -> None:
        self.start_application_mode()

    @abstractmethod
    def disable_input(self) -> None:...

    def close(self):...

    @abstractmethod
    def get_cursor_pos(self) -> tuple[int, int]: ...

    @abstractmethod
    def get_terminal_size(self) -> tuple[int, int]: ...

    @abstractmethod
    def on_input(self) -> str: ...

    @abstractmethod
    def write(self, data: str) -> None:...

    @abstractmethod
    def move_to(self, col: int, row: int): ...

    def flush(self) -> None:...
