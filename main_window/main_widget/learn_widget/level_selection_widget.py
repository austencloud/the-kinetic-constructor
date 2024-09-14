from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton
from PyQt6.QtCore import Qt

if TYPE_CHECKING:
    from main_window.main_widget.learn_widget.learn_widget import LearnWidget


class LevelSelectionWidget(QWidget):
    def __init__(self, learn_widget: "LearnWidget") -> None:
        super().__init__(learn_widget)
        self.learn_widget = learn_widget
        self.main_widget = learn_widget.main_widget

        self.layout: QVBoxLayout = QVBoxLayout()
        self.layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setLayout(self.layout)

        # Title label
        self.title_label = QLabel("Select Difficulty Level:")
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.addStretch(2)
        self.layout.addWidget(self.title_label)
        self.layout.addStretch(2)
        # Add buttons for each level
        self.add_level_button("Level 1", self.learn_widget.show_level_1_quiz_selector)
        self.add_level_button("Level 2", self.learn_widget.start_intermediate_module)
        self.add_level_button("Level 3", self.learn_widget.start_advanced_module)
        self.layout.addStretch(2)

    def add_level_button(self, text, callback) -> None:
        button = QPushButton(text)
        button.setCursor(Qt.CursorShape.PointingHandCursor)
        button.clicked.connect(callback)
        self.layout.addWidget(button)
        self.layout.addStretch(1)

    def resize_level_selection_widget(self) -> None:
        font_size = self.main_widget.width() // 40
        font = self.title_label.font()
        font.setFamily("Monotype Corsiva")  # Set font family to Monotype Corsiva
        font.setPointSize(font_size)
        self.title_label.setFont(font)
        for button in self.findChildren(QPushButton):
            button.setFixedSize(
                self.main_widget.width() // 4, self.main_widget.height() // 8
            )
            button.setStyleSheet(f"font-size: {font_size}px;")
