from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel
from PyQt6.QtCore import Qt

from base_widgets.base_pictograph.base_pictograph import BasePictograph


if TYPE_CHECKING:
    from main_window.main_widget.learn_widget.learn_widget import LearnWidget


class Lesson1QuestionWidget(QWidget):
    """Widget for displaying the pictograph and managing its size and alignment."""

    def __init__(self, learn_widget: "LearnWidget"):
        super().__init__(learn_widget)
        self.learn_widget = learn_widget
        self.main_widget = learn_widget.main_widget
        self.pictograph = None
        self.question_label = QLabel("What letter matches the pictograph?")
        self.question_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._setup_layout()

    def _setup_layout(self) -> None:
        self.layout: QVBoxLayout = QVBoxLayout()
        self.layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.question_label)
        self.layout.addStretch(3)
        self.setLayout(self.layout)

    def load_pictograph(self, pictograph_dict) -> None:
        """Load and display the pictograph."""
        self.pictograph = BasePictograph(self.main_widget, scroll_area=None)
        self.pictograph.disable_gold_overlay = True
        self.pictograph.updater.update_pictograph(pictograph_dict)
        self.pictograph.view.leaveEvent = None
        self.layout.addWidget(
            self.pictograph.view, alignment=Qt.AlignmentFlag.AlignCenter
        )
        self.resize_lesson_1_question_widget()

    def clear(self) -> None:
        """Remove the current pictograph view."""
        if self.pictograph:
            self.layout.removeWidget(self.pictograph.view)
            self.pictograph.view.deleteLater()
            self.pictograph = None

    def resize_lesson_1_question_widget(self) -> None:
        self._resize_question_label()
        self._resize_pictograph()

    def _resize_question_label(self) -> None:
        question_label_font_size = self.main_widget.width() // 50
        font = self.question_label.font()
        font.setFamily("Monotype Corsiva")
        font.setPointSize(question_label_font_size)
        self.question_label.setFont(font)

    def _resize_pictograph(self) -> None:

        if self.pictograph:
            self.pictograph.view.setFixedSize(
                self.main_widget.height() // 2, self.main_widget.height() // 2
            )
