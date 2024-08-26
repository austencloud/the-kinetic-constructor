from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QMenu
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QCursor
from PyQt6.QtWidgets import QApplication

if TYPE_CHECKING:
    from .menu_bar import MenuBar


class HoverableMenu(QMenu):
    def __init__(self, title, menu_bar: "MenuBar"):
        super().__init__(title, menu_bar)
        self.menu_bar = menu_bar
        self._add_hover_effect_to_actions()

    def _add_hover_effect_to_actions(self):
        for action in self.actions():
            action.hovered.connect(self._on_action_hover)

    def _on_action_hover(self):
        QApplication.setOverrideCursor(Qt.CursorShape.PointingHandCursor)

    def enterEvent(self, event):
        QApplication.setOverrideCursor(Qt.CursorShape.PointingHandCursor)
        super().enterEvent(event)

    def leaveEvent(self, event):
        QApplication.restoreOverrideCursor()
        super().leaveEvent(event)

    # if an item is selected and the menu goes away, restore the cursor
    def hideEvent(self, event):
        QApplication.restoreOverrideCursor()
        super().hideEvent(event)