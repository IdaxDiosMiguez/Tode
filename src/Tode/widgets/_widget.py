from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from Tode.app import Tode


from Tode.core import Bindable


class Widget(Bindable):

    def __init__(self, app: Tode) -> None:
        super().__init__()
        self.terminal = app.terminal
        self.is_active = False

    def render(self):
        ...