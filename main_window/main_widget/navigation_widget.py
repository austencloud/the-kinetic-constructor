# navigation_widget.py
from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QWidget, QHBoxLayout, QPushButton, QFrame, QVBoxLayout
from PyQt6.QtGui import QCursor
from PyQt6.QtCore import Qt, pyqtSignal


if TYPE_CHECKING:
    from main_window.main_widget.main_widget import MainWidget


class NavigationWidget(QWidget):
    tab_changed = pyqtSignal(int)

    def __init__(self, main_widget: "MainWidget"):
        super().__init__(main_widget)
        self.main_widget = main_widget

        # Create a container frame
        self.container_frame = QFrame(self)
        # self.container_frame.setStyleSheet(
        #     f"QFrame {{ background-color: rgba(0, 0, 0, 0.5); border-radius: {self.calculate_border_radius()}px; }}"
        # )

        # Create a layout for the container frame
        self.container_layout = QVBoxLayout(self.container_frame)
        self.container_layout.setContentsMargins(0, 0, 0, 0)

        self.tab_buttons: dict[str, QPushButton] = {}
        self.tab_layout = QHBoxLayout()
        self.tab_layout.addStretch(1)
        self.tab_names = [
            "Build ⚒️",
            "Generate 🤖",
            "Browse 🔍",
            "Learn 🧠",
            "Write ✍️",
        ]
        self.current_index = 0
        for index, name in enumerate(self.tab_names):
            button = QPushButton(name)
            button.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
            button.clicked.connect(lambda _, idx=index: self.on_button_clicked(idx))
            self.tab_buttons[name] = button
            self.tab_layout.addWidget(button)
        self.tab_layout.addStretch(1)

        # Add the tab layout to the container layout
        self.container_layout.addLayout(self.tab_layout)
        self.tab_changed.connect(self.main_widget.tabs_handler.on_tab_changed)
        # Set the main layout of the NavigationWidget
        main_layout = QVBoxLayout(self)
        main_layout.addWidget(self.container_frame)

    def on_button_clicked(self, index):
        self.set_active_tab(index)
        self.tab_changed.emit(index)

    def set_active_tab(self, index):
        self.current_index = index
        for idx, button in self.tab_buttons.items():
            self.set_button_appearance(index, idx, button)

    def set_button_appearance(self, index, idx, button: "QPushButton"):
        font_size = self.main_widget.width() // 100
        if idx == index:
            # Apply active style
            button.setStyleSheet(
                f"background-color: lightblue; font-size: {font_size}pt; font-family: Georgia;"
            )
        else:
            # Apply normal style
            button.setStyleSheet(f"font-size: {font_size}pt; font-family: Georgia;")
        button.setMinimumWidth(self.main_widget.width() // 8)
        button.setMinimumHeight(self.main_widget.height() // 20)

    def resize_navigation_widget(self):
        self.set_active_tab(self.current_index)
