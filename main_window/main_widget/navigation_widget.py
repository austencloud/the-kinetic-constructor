from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QWidget, QPushButton, QFrame, QHBoxLayout, QVBoxLayout
from PyQt6.QtGui import QCursor
from PyQt6.QtCore import Qt, pyqtSignal, pyqtSlot

if TYPE_CHECKING:
    from main_window.main_widget.main_widget import MainWidget


class NavigationWidget(QWidget):
    # Signal emits two integers: new_index and previous_index
    tab_changed = pyqtSignal(int, int)

    def __init__(self, main_widget: "MainWidget"):
        super().__init__(main_widget)
        self.main_widget = main_widget
        self.current_index = 0  # Initialize to the first tab

        self.container_frame = QFrame(self)
        self.container_layout = QVBoxLayout(self.container_frame)
        self.container_layout.setContentsMargins(0, 0, 0, 0)

        self.tab_buttons: dict[str, QPushButton] = {}
        self.tab_layout = QHBoxLayout()
        self.tab_layout.addStretch(1)
        self.tab_names = [
            "Construct ⚒️",
            "Generate 🤖",
            "Browse 🔍",
            "Learn 🧠",
            "Write ✍️",
        ]
        for index, name in enumerate(self.tab_names):
            button = QPushButton(name)
            button.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
            # Use default arguments to capture the current index correctly
            button.clicked.connect(lambda checked, idx=index: self.on_button_clicked(idx))
            self.tab_buttons[name] = button
            self.tab_layout.addWidget(button)
        self.tab_layout.addStretch(1)

        # Add the tab layout to the container layout
        self.container_layout.addLayout(self.tab_layout)
        
        # Set the main layout of the NavigationWidget
        main_layout = QVBoxLayout(self)
        main_layout.addWidget(self.container_frame)
        self.setLayout(main_layout)

        # Initialize active tab appearance
        self.set_active_tab(self.current_index)

    def on_button_clicked(self, index: int):
        if index == self.current_index:
            return  # No change
        previous_index = self.current_index
        self.current_index = index
        self.set_active_tab(index)
        self.tab_changed.emit(index, previous_index)

    def set_active_tab(self, index: int):
        for idx, (name, button) in enumerate(self.tab_buttons.items()):
            if idx == index:
                self.set_button_appearance(button, active=True)
            else:
                self.set_button_appearance(button, active=False)

    def set_button_appearance(self, button: "QPushButton", active: bool):
        font_size = self.main_widget.width() // 120
        if active:
            button.setStyleSheet(
                f"background-color: lightblue; font-size: {font_size}pt; font-family: Georgia;"
            )
        else:
            button.setStyleSheet(f"font-size: {font_size}pt; font-family: Georgia;")
        button.setMinimumWidth(self.main_widget.width() // 10)
        button.setMinimumHeight(self.main_widget.height() // 22)

    def select_tab(self, index: int):
        if index == self.current_index:
            return
        previous_index = self.current_index
        self.current_index = index
        self.set_active_tab(index)
        self.tab_changed.emit(index, previous_index)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.set_active_tab(self.current_index)
