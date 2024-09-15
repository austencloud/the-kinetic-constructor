from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QHBoxLayout
from PyQt6.QtCore import Qt

if TYPE_CHECKING:
    from main_window.main_widget.learn_widget.learn_widget import LearnWidget


class Level1QuizSelector(QWidget):
    def __init__(self, learn_widget: "LearnWidget"):
        super().__init__(learn_widget)
        self.learn_widget = learn_widget
        self.main_widget = learn_widget.main_widget
        
        # Create the main layout and set its alignment
        self.main_layout: QVBoxLayout = QVBoxLayout()
        self.setLayout(self.main_layout)

        # Add back button at the top left
        self.add_back_button()

        # Title label
        self.title_label = QLabel("Select Level 1 Quiz:")
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.main_layout.addStretch(1)
        self.main_layout.addWidget(self.title_label)
        self.main_layout.addStretch(1)

        # Buttons for 1.0 and 1.1 quizzes
        self.quiz_buttons: dict[str, QPushButton] = {}
        self.quiz_button_layout = QVBoxLayout()
        # align center
        self.quiz_button_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.add_quiz_button(
            "1.0 - Pictograph to Letter", self.learn_widget.start_level_1_0_quiz
        )
        self.add_quiz_button(
            "1.1 - Letter to Pictograph", self.learn_widget.start_level_1_1_quiz
        )
        # add buttons to the main layout
        self.main_layout.addLayout(self.quiz_button_layout)
        self.main_layout.addStretch(1)

    def add_back_button(self):
        """Add a back button to go back to the main LearnWidget."""
        self.back_button = QPushButton("Back")
        self.back_button.clicked.connect(self.learn_widget.show_level_selection_widget)
        self.back_button.setCursor(Qt.CursorShape.PointingHandCursor)

        # Create an HBox layout for the back button and align it left
        back_layout = QHBoxLayout()
        back_layout.addWidget(self.back_button, alignment=Qt.AlignmentFlag.AlignLeft)
        
        # Ensure the back button is at the top of the layout
        self.main_layout.addLayout(back_layout)

    def add_quiz_button(self, text, callback):
        button = QPushButton(text)
        button.setCursor(Qt.CursorShape.PointingHandCursor)
        button.setFixedHeight(50)  # Adjust as necessary
        button.clicked.connect(callback)
        self.quiz_buttons[text] = button
        self.quiz_button_layout.addWidget(button)
        self.quiz_button_layout.addStretch(1)

    def resize_level_1_quiz_selector(self):
        # Set the button font and size and the label according to the main widget
        font_size = self.main_widget.width() // 60
        font = self.title_label.font()
        font.setPointSize(font_size)
        self.title_label.setFont(font)

        # Resize all quiz buttons
        for button in self.quiz_buttons.values():
            button.setFixedSize(
                self.main_widget.width() // 3, self.main_widget.height() // 8
            )
            button.setStyleSheet(f"font-size: {font_size}px;")

        # Resize the back button
        self.back_button.setFixedSize(
            self.main_widget.width() // 8, self.main_widget.height() // 12
        )
        # Set back button font size
        self.back_button.setStyleSheet(f"font-size: {font_size}px;")
