# grid_mode_selector.py

from typing import TYPE_CHECKING
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


class GridModeSelector(QWidget):
    def __init__(self, menu_bar_widget: "MenuBarWidget"):
        super().__init__()
        self.menu_bar_widget = menu_bar_widget
        self.main_widget = menu_bar_widget.main_widget
        self.settings_manager = self.main_widget.settings_manager
        self.dialog = None
        current_grid_mode = (
            self.settings_manager.global_settings.get_grid_mode().capitalize()
        )

        self.label = ClickableLabel(current_grid_mode)
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
        self.show_grid_mode_dialog()

    def show_grid_mode_dialog(self):
        options = ["Diamond", "Box"]

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
        font.setPointSize(14)  # Adjust the font size as needed

        for grid_mode in options:
            button = QPushButton(grid_mode)
            button.setFont(font)
            button.setCursor(Qt.CursorShape.PointingHandCursor)
            button.clicked.connect(
                lambda _, gm=grid_mode: self.set_current_grid_mode(gm)
            )
            layout.addWidget(button)

        self.dialog.setLayout(layout)
        self.dialog.adjustSize()

        # Position the dialog below the label
        global_pos = self.label.mapToGlobal(self.label.rect().bottomLeft())
        self.dialog.move(global_pos)
        self.dialog.exec()

    def set_current_grid_mode(self, grid_mode: str):
        self.label.setText(grid_mode.capitalize())
        self.settings_manager.global_settings.set_grid_mode(grid_mode.lower())
        self.main_widget.manager.set_grid_mode(grid_mode.lower())
        if self.dialog:
            self.dialog.accept()
