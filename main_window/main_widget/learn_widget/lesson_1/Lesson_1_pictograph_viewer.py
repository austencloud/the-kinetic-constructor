from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QWidget, QVBoxLayout
from PyQt6.QtCore import Qt

from main_window.main_widget.learn_widget.quiz_pictograph_factory import QuizPictographFactory

if TYPE_CHECKING:
    from main_window.main_widget.learn_widget.learn_widget import LearnWidget

class Lesson1PictographViewer(QWidget):
    """Widget for displaying the pictograph and managing its size and alignment."""

    def __init__(self, learn_widget: "LearnWidget"):
        super().__init__(learn_widget)
        self.learn_widget = learn_widget
        self.main_widget = learn_widget.main_widget
        self.pictograph_factory = QuizPictographFactory(self.main_widget)
        self.pictograph = None

        # Layout for centering the pictograph
        self.layout: QVBoxLayout = QVBoxLayout()
        self.layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setLayout(self.layout)

    def load_pictograph(self, pictograph_key, pictograph_dict):
        """Load and display the pictograph."""
        # Generate the pictograph using the factory
        self.pictograph = self.pictograph_factory.get_or_create_pictograph(
            pictograph_key, pictograph_dict, disable_gold_overlay=True
        )

        # Hide the letter from the pictograph
        self.pictograph.tka_glyph.setVisible(False)
        # remove the mouse event from the view
        self.pictograph.view.setCursor(Qt.CursorShape.ArrowCursor)
        # remove all mouse hover events
        self.pictograph.view.setMouseTracking(False)
        self.pictograph.container.styled_border_overlay.setMouseTracking(False)
        self.pictograph.container.setCursor(Qt.CursorShape.ArrowCursor)

        # Add pictograph view to the layout (centered)
        self.layout.addWidget(
            self.pictograph.view, alignment=Qt.AlignmentFlag.AlignCenter
        )
        self.resize_level_1_0_quiz_pictograph_viewer()

    def clear(self):
        """Remove the current pictograph view."""
        if self.pictograph:
            self.layout.removeWidget(self.pictograph.view)
            # self.pictograph.view.deleteLater()
            self.pictograph = None

    def resize_level_1_0_quiz_pictograph_viewer(self) -> None:
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
