from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QMenuBar, QMenu, QApplication
from PyQt6.QtCore import Qt, QEvent
from .user_profile_menu import UserProfileMenu
from .backgrounds_menu import BackgroundsMenu
from .prop_type_menu import PropTypeMenu
from .visibility_menu import VisibilityMenu

if TYPE_CHECKING:
    from main_window.menu_bar_widget.menu_bar_widget import MenuBarWidget


class MenuBar(QMenuBar):
    def __init__(self, menu_bar_widget: "MenuBarWidget") -> None:
        super().__init__()
        self.main_window = menu_bar_widget.main_window
        self.main_widget = self.main_window.main_widget

        self.user_profiles_menu = UserProfileMenu(self)
        self.backgrounds_menu = BackgroundsMenu(self)
        self.prop_type_menu = PropTypeMenu(self)
        self.visibility_menu = VisibilityMenu(self)

        self.addMenu(self.prop_type_menu)
        self.addMenu(self.visibility_menu)
        self.addMenu(self.backgrounds_menu)
        self.addMenu(self.user_profiles_menu)

        # Apply custom spacing and styles
        self._apply_stylesheet()

    def _apply_stylesheet(self):
        spacing = self.main_window.width() // 100
        background_color = "#F0F0F0"
        hover_color = "#D3D3D3"
        checkmark_size = self.main_window.width() // 100

        self.setStyleSheet(
            f"""
            QMenuBar {{
                background-color: {background_color};
            }}
            QMenuBar::item {{
                padding: 0px {spacing}px;
                background-color: {background_color};
                color: black;
            }}
            QMenuBar::item:selected {{
                background-color: {hover_color};  /* Change background on selection */
            }}
            QMenuBar::item:pressed {{
                background-color: {hover_color};  /* Change background on press */
            }}
            QMenuBar::item:hover {{
                background-color: {hover_color};  /* Change background on hover */
                cursor: pointer;  /* Change cursor to pointer on hover */
            }}
            QMenu {{
                background-color: {background_color};
            }}
            QMenu::item {{
                background-color: {background_color};
                padding: 5px 10px;
            }}
            QMenu::item:selected {{
                background-color: {hover_color};  /* Slightly darker gray for selected items */
            }}
            QMenu::indicator {{
                width: {checkmark_size}px;
                height: {checkmark_size}px;
            }}
            """
        )

    def resize_menu_bar(self):
        self._adjust_font_size()
        self._apply_stylesheet()  # Update styles on resize
        self.move(0, 0)
        self.show()

    def _adjust_font_size(self):
        font = self.font()
        font_size = self.main_window.width() // 120
        font.setPointSize(font_size)
        self.setFont(font)

        for menu in self.findChildren(QMenu):
            menu_font = menu.font()
            menu_font.setPointSize(font_size)
            menu.setFont(menu_font)
            for action in menu.actions():
                action_font = action.font()
                action_font.setPointSize(font_size)
                action.setFont(action_font)

    def enterEvent(self, event):
        QApplication.setOverrideCursor(Qt.CursorShape.PointingHandCursor)
        super().enterEvent(event)

    def leaveEvent(self, event):
        QApplication.restoreOverrideCursor()
        super().leaveEvent(event)

    # Override event handling to manually change the cursor for the menu bar items
    def event(self, event):
        if event.type() == QEvent.Type.HoverMove:
            self.setCursor(Qt.CursorShape.PointingHandCursor)
        elif event.type() in [QEvent.Type.Leave, QEvent.Type.HoverLeave]:
            self.setCursor(Qt.CursorShape.ArrowCursor)
        return super().event(event)
