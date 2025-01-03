from typing import TYPE_CHECKING
from PyQt6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QTabWidget,
)

from PyQt6.QtGui import QFont, QCursor
from PyQt6.QtCore import Qt

from main_window.main_widget.settings_dialog.action_buttons import (
    SettingsDialogActionButtons,
)
from main_window.main_widget.settings_dialog.settings_dialog_styler import (
    SettingsDialogStyler,
)
from .user_profile_tab import UserProfileTab
from .prop_type_tab import PropTypeTab
from .background_tab import BackgroundTab
from .visibility_tab import VisibilityTab

if TYPE_CHECKING:
    from main_window.main_widget.main_widget import MainWidget


class SettingsDialog(QDialog):
    def __init__(self, main_widget: "MainWidget"):
        super().__init__(main_widget)
        self.main_widget = main_widget
        self.setWindowTitle("Settings")
        self._setup_ui()
        self._apply_styles()

    def _setup_ui(self):
        self.styler = SettingsDialogStyler(self)
        self.action_btns = SettingsDialogActionButtons(self)
        self.tab_widget = QTabWidget(self)
        self.user_profile_tab = UserProfileTab(self)
        self.prop_type_tab = PropTypeTab(self)
        self.background_tab = BackgroundTab(self)
        self.visibility_tab = VisibilityTab(self)

        self.tab_widget.addTab(self.user_profile_tab, "User Profile")
        self.tab_widget.addTab(self.prop_type_tab, "Prop Type")
        self.tab_widget.addTab(self.background_tab, "Background")
        self.tab_widget.addTab(self.visibility_tab, "Visibility")

        main_layout = QVBoxLayout(self)
        main_layout.addWidget(self.tab_widget)
        main_layout.addWidget(self.action_btns)
        self.setLayout(main_layout)

    def _apply_styles(self):
        self.styler.style_tab_widget(self.tab_widget)

        # Style action buttons
        for button in [self.action_btns.save_button, self.action_btns.close_button]:
            self.styler.style_button(button)

    def get_default_font(self):
        font = QFont()
        font_size = self.main_widget.width() // 100
        font.setPointSize(font_size)
        return font

    def resizeEvent(self, event):
        size = self.main_widget.size()
        self.setFixedSize(size.width() // 2, size.height() // 2)
        font = QFont()
        font.setPointSize(size.width() // 100)
        self.tab_widget.tabBar().setFont(font)
        self.tab_widget.tabBar().setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        for button in [self.action_btns.save_button, self.action_btns.close_button]:
            button.setFont(font)
