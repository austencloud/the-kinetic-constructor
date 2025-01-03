from typing import TYPE_CHECKING
from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QPushButton,
    QLabel,
    QSpacerItem,
    QSizePolicy,
)
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt

if TYPE_CHECKING:
    from main_window.main_widget.main_widget import MainWidget


class UserProfileTab(QWidget):
    def __init__(self, main_widget: "MainWidget"):
        super().__init__()
        self.main_widget = main_widget
        self._setup_ui()

    def _setup_ui(self):
        layout = QVBoxLayout(self)

        title = QLabel("User Profile Settings")
        title.setFont(self._get_title_font())
        layout.addWidget(title)

        user_manager = self.main_widget.settings_manager.users.user_manager
        users = user_manager.get_all_users()

        for user in users:
            button = QPushButton(user)
            button.setFont(self._get_default_font())
            button.setCursor(Qt.CursorShape.PointingHandCursor)
            button.setStyleSheet("margin: 5px;")
            button.clicked.connect(lambda _, u=user: self._set_current_user(u))
            layout.addWidget(button)

        edit_users_button = QPushButton("Edit Users")
        edit_users_button.setFont(self._get_default_font())
        edit_users_button.setCursor(Qt.CursorShape.PointingHandCursor)
        edit_users_button.clicked.connect(user_manager.open_edit_users_dialog)
        layout.addWidget(edit_users_button)

        layout.addSpacerItem(
            QSpacerItem(
                20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding
            )
        )

    def _set_current_user(self, user_name: str):
        user_manager = self.main_widget.settings_manager.users.user_manager
        user_manager.set_current_user(user_name)
        self.main_widget.sequence_properties_manager.update_sequence_properties()

    def _get_title_font(self):
        font = QFont()
        font.setPointSize(16)
        font.setBold(True)
        return font

    def _get_default_font(self):
        font = QFont()
        font.setPointSize(12)
        return font
