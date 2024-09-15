from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel
from PyQt6.QtCore import Qt
from main_window.main_widget.learn_widget.lesson_pictograph_factory import (
    LessonPictographFactory,
)
if TYPE_CHECKING:
    from main_window.main_widget.learn_widget.lesson_1.lesson_1_widget import Lesson1Widget

class Lesson1QuestionWidget(QWidget):
    """Widget responsible for displaying the question in Lesson 1, including the pictograph."""

    def __init__(self, lesson_1_widget: "Lesson1Widget"):
        super().__init__(lesson_1_widget)
        self.lesson_1_widget = lesson_1_widget
        self.main_widget = lesson_1_widget.main_widget
        self.pictograph_factory = LessonPictographFactory(self.main_widget)

        # Layout to center the question and pictograph
        self.layout: QVBoxLayout = QVBoxLayout()
        self.setLayout(self.layout)

        # Question label (text prompt)
        self.question_label = QLabel()
        self.question_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.question_label)

        # Initialize a variable to hold the pictograph
        self.pictograph = None

    def display_question(self, question_text: str, pictograph_dict: dict):
        """Display the question prompt and the pictograph."""
        self.question_label.setText(question_text)

        # Generate and display the pictograph
        pictograph_key = self.main_widget.pictograph_key_generator.generate_pictograph_key(
            pictograph_dict
        )
        self.pictograph = self.pictograph_factory.get_or_create_pictograph(
            pictograph_key, pictograph_dict, disable_gold_overlay=True
        )
        
        # Hide the letter glyph from the pictograph
        self.pictograph.tka_glyph.setVisible(False)

        # Disable cursor interactions for the pictograph
        self.pictograph.view.setCursor(Qt.CursorShape.ArrowCursor)
        self.pictograph.view.setMouseTracking(False)
        self.pictograph.container.styled_border_overlay.setMouseTracking(False)
        self.pictograph.container.setCursor(Qt.CursorShape.ArrowCursor)

        # Add the pictograph to the layout
        self.layout.addWidget(self.pictograph.view, alignment=Qt.AlignmentFlag.AlignCenter)
        self.resize_question_widget()

    def clear(self):
        """Clear the question display and remove the pictograph."""
        self.question_label.clear()
        if self.pictograph:
            self.layout.removeWidget(self.pictograph.view)
            self.pictograph = None

    def resize_question_widget(self):
        """Resize the question and pictograph based on the window size."""
        # Resize question label
        font_size = self.lesson_1_widget.main_widget.width() // 50
        self.question_label.setStyleSheet(f"font-size: {font_size}px;")

        # Resize the pictograph if it's present
        if self.pictograph:
            self.pictograph.view.resize(
                self.main_widget.height() // 2, self.main_widget.height() // 2
            )
            self._scale_pictograph()
            self.pictograph.container.styled_border_overlay.resize_styled_border_overlay()

    def _scale_pictograph(self):
        """Scale the pictograph to fit the view size."""
        scene_size = self.pictograph.sceneRect().size()
        view_size = self.pictograph.view.size()
        scale_factor = min(
            view_size.width() / scene_size.width(),
            view_size.height() / scene_size.height(),
        )
        self.pictograph.view.resetTransform()
        self.pictograph.view.scale(scale_factor, scale_factor)
