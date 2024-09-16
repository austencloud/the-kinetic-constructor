from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QVBoxLayout, QLabel
from PyQt6.QtCore import Qt
from base_widgets.base_pictograph.base_pictograph import BasePictograph
from main_window.main_widget.learn_widget.base_classes.base_question_widget import (
    BaseQuestionWidget,
)

if TYPE_CHECKING:
    from main_window.main_widget.learn_widget.learn_widget import LearnWidget


class Lesson3QuestionWidget(BaseQuestionWidget):
    """Widget for displaying the initial pictograph in Lesson 3."""

    def __init__(self, learn_widget: "LearnWidget"):
        super().__init__(learn_widget)
        self.learn_widget = learn_widget
        self.main_widget = learn_widget.main_widget
        self.pictograph = None
        self._setup_layout()

    def _setup_layout(self) -> None:
        self.layout: QVBoxLayout = QVBoxLayout()
        self.layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setLayout(self.layout)

    def load_pictograph(self, pictograph_dict) -> None:
        """Load and display the pictograph."""
        self.pictograph = BasePictograph(self.main_widget, scroll_area=None)
        self.pictograph.disable_gold_overlay = True
        self.pictograph.updater.update_pictograph(pictograph_dict)
        self.layout.addWidget(
            self.pictograph.view, alignment=Qt.AlignmentFlag.AlignCenter
        )
        self.resize_question_widget()

    def clear(self) -> None:
        """Clear the current pictograph."""
        if self.pictograph:
            self.layout.removeWidget(self.pictograph.view)
            self.pictograph.view.deleteLater()
            self.pictograph = None

    def resize_question_widget(self) -> None:
        """Resize the question display based on window size."""
        if self.pictograph:
            self.pictograph.view.setFixedSize(
                self.main_widget.height() // 3, self.main_widget.height() // 3
            )
