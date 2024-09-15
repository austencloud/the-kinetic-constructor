from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QWidget, QGridLayout, QHBoxLayout, QApplication
from PyQt6.QtCore import Qt

from base_widgets.base_pictograph.base_pictograph import BasePictograph
from ...quiz_pictograph_factory import QuizPictographFactory

if TYPE_CHECKING:
    from main_window.main_widget.learn_widget.learn_widget import LearnWidget


class Level_1_1_QuizPictographButtonsWidget(QWidget):
    """Widget to manage pictograph views layout and actions."""

    def __init__(self, learn_widget: "LearnWidget"):
        super().__init__(learn_widget)
        self.learn_widget = learn_widget
        self.main_widget = learn_widget.main_widget
        self.pictograph_factory = QuizPictographFactory(self.main_widget)

        # Use a horizontal box layout to organize pictographs in a row
        self.layout: QHBoxLayout = QHBoxLayout()
        self.layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setLayout(self.layout)

        # Keep track of pictograph views for resizing purposes
        self.pictograph_views: list[QWidget] = []
        self.pictographs: dict[str, BasePictograph] = {}

    def create_pictograph_buttons(
        self, pictographs, correct_pictograph, check_answer_callback
    ):
        """Create the pictograph views and attach click events in a row."""
        self.clear()  # Clear existing pictographs before creating new ones

        # Loop through pictographs and add them to the layout
        for i, pictograph_dict in enumerate(pictographs):
            # Generate the pictograph using the factory
            pictograph_key = (
                self.main_widget.pictograph_key_generator.generate_pictograph_key(
                    pictograph_dict
                )
            )
            pictograph = self.pictograph_factory.get_or_create_pictograph(
                pictograph_key, pictograph_dict, disable_gold_overlay=False
            )
            self.pictographs[pictograph_key] = pictograph
            # Remove mouse tracking for the pictograph (to disable hover/mouse events)
            pictograph.view.setCursor(Qt.CursorShape.PointingHandCursor)

            # Connect click event directly to the view
            pictograph.view.mousePressEvent = (
                lambda event, opt=pictograph_dict: check_answer_callback(
                    opt, correct_pictograph
                )
            )

            # Add pictograph view to the layout
            self.pictograph_views.append(pictograph.view)

        for view in self.pictograph_views:
            self.layout.addWidget(view)

    def clear(self):
        """Clear all pictograph views."""
        for view in self.pictograph_views:
            self.layout.removeWidget(view)
        self.pictograph_views.clear()
        self.pictographs.clear()
        # QApplication.processEvents()

    def resize_level_1_1_pictograph_buttons_widget(self):
        """Resize the pictograph views based on window size."""
        for view in self.pictograph_views:
            view.setFixedSize(
                self.main_widget.height() // 3, self.main_widget.height() // 3
            )
        self._scale_pictographs()

    def _scale_pictographs(self):
        for pictograph in self.pictographs.values():
            scene_size = pictograph.sceneRect().size()
            view_size = pictograph.view.size()
            scale_factor = min(
                view_size.width() / scene_size.width(),
                view_size.height() / scene_size.height(),
            )
            pictograph.view.scale(scale_factor, scale_factor)
            pictograph.container.styled_border_overlay.resize_styled_border_overlay()
