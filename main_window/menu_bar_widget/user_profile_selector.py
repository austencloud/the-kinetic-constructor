# user_profile_selector.py

from typing import TYPE_CHECKING, List
from PyQt6.QtWidgets import QWidget, QLabel, QDialog, QPushButton, QVBoxLayout
from PyQt6.QtCore import pyqtSignal, Qt
from PyQt6.QtGui import QFont

if TYPE_CHECKING:
    from main_window.menu_bar_widget.menu_bar_widget import MenuBarWidget


class ClickableLabel(QLabel):
    clicked = pyqtSignal()

    def __init__(self, text: str):
        super().__init__(text)
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.clicked.emit()
        super().mousePressEvent(event)


class UserProfileSelector(QWidget):
    def __init__(self, menu_bar_widget: "MenuBarWidget"):
        super().__init__()
        self.menu_bar_widget = menu_bar_widget
        self.main_widget = menu_bar_widget.main_widget
        self.user_manager = self.main_widget.settings_manager.users.user_manager
        self.dialog = None
        current_user = self.user_manager.get_current_user()

        self.label = ClickableLabel(current_user)
        self.label.clicked.connect(self.on_label_clicked)

        # Set up layout
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.label)
        self.setLayout(layout)

        # self.style_widget()

    def style_widget(self):
        font_size = self.menu_bar_widget.menu_bar_font_size
        font = QFont("Georgia", font_size)
        self.label.setFont(font)

        style_sheet = """
            border: 1px solid black;
            padding: 4px;
            background-color: white;
            border-radius: 5px;
        """

        hover_style = """
            background-color: #F0F0F0;
        """

        # Set the cursor to pointing hand
        self.label.setCursor(Qt.CursorShape.PointingHandCursor)

        self.label.setStyleSheet(
            f"""
            QLabel {{
                {style_sheet}
            }}
            QLabel:hover {{
                {hover_style}
            }}
            """
        )

    def on_label_clicked(self):
        self.show_user_profile_dialog()

    def show_user_profile_dialog(self):
        self.refresh_options()

        self.dialog = QDialog(self)
        self.dialog.setWindowFlags(
            Qt.WindowType.FramelessWindowHint | Qt.WindowType.Popup
        )
        self.dialog.setStyleSheet(
            """
            QDialog {
                border: 2px solid black;
                border-radius: 5px;
                background-color: white;
            }
            QPushButton {
                padding: 5px 10px;
            }
            """
        )

        layout = QVBoxLayout(self.dialog)
        layout.setContentsMargins(5, 5, 5, 5)

        font = QFont()
        font.setPointSize(self.menu_bar_widget.menu_bar_font_size)

        for option in self.options:
            button = QPushButton(option)
            button.setFont(font)
            button.setCursor(Qt.CursorShape.PointingHandCursor)
            button.clicked.connect(
                lambda _, o=option: self.option_selected(o, self.dialog)
            )
            layout.addWidget(button)

        self.dialog.setLayout(layout)
        self.dialog.adjustSize()

        # Position the dialog below the label
        global_pos = self.label.mapToGlobal(self.label.rect().bottomLeft())
        self.dialog.move(global_pos)
        self.dialog.exec()

    def refresh_options(self):
        self.users = self.user_manager.get_all_users()
        self.options: list[str] = self.users + ["Edit Users"]

    def option_selected(self, option: str, dialog: QDialog):
        if option == "Edit Users":
            self.user_manager.open_edit_users_dialog()
            dialog.accept()
            # self.on_label_clicked()  # Reopen the dialog with updated options
        else:
            self.set_current_user(option)
            dialog.accept()

    def set_current_user(self, user_name: str):
        self.label.setText(user_name)
        self.user_manager.set_current_user(user_name)
        self.main_widget.sequence_properties_manager.update_sequence_properties()
