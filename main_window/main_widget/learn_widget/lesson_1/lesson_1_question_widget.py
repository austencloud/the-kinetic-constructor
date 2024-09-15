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
        self._setup_layout()

    def _setup_layout(self):
        self.layout: QVBoxLayout = QVBoxLayout()
        self.layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.question_label)
        self.layout.addStretch(3)
        self.setLayout(self.layout)

    def load_pictograph(self, pictograph_dict):
        """Load and display the pictograph."""
        self.pictograph = BasePictograph(self.main_widget, scroll_area=None)
        self.pictograph.disable_gold_overlay = True
        self.pictograph.updater.update_pictograph(pictograph_dict)

        self.pictograph.tka_glyph.setVisible(False)
        self.pictograph.view.setCursor(Qt.CursorShape.ArrowCursor)
        self.pictograph.view.setMouseTracking(False)
        self.pictograph.container.styled_border_overlay.setMouseTracking(False)
        self.pictograph.container.setCursor(Qt.CursorShape.ArrowCursor)

        self.layout.addWidget(
            self.pictograph.view, alignment=Qt.AlignmentFlag.AlignCenter
        )
        self.resize_lesson_1_question_widget()

    def clear(self):
        """Remove the current pictograph view."""
        if self.pictograph:
            self.layout.removeWidget(self.pictograph.view)
            self.pictograph.view.deleteLater()
            self.pictograph = None

    def resize_lesson_1_question_widget(self) -> None:
        if self.pictograph:
            self.resize(self.main_widget.height() // 2, self.main_widget.height() // 2)
            self.pictograph.view.resize(
                self.main_widget.height() // 2, self.main_widget.height() // 2
            )
            self._scale_pictograph()
            self.pictograph.container.styled_border_overlay.resize_styled_border_overlay()

    def _scale_pictograph(self):
        scene_size = self.pictograph.sceneRect().size()
        view_size = self.pictograph.view.size()
        scale_factor = min(
            view_size.width() / scene_size.width(),
            view_size.height() / scene_size.height(),
        )
        self.pictograph.view.resetTransform()
        self.pictograph.view.scale(scale_factor, scale_factor)
