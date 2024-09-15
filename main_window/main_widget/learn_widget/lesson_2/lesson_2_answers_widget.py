from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QWidget, QHBoxLayout
from PyQt6.QtCore import Qt

from base_widgets.base_pictograph.base_pictograph import BasePictograph
from main_window.main_widget.learn_widget.lesson_pictograph_factory import (
    LessonPictographFactory,
)

if TYPE_CHECKING:
    from main_window.main_widget.learn_widget.lesson_2.lesson_2_widget import (
        Lesson2Widget,
    )


class Lesson2AnswersWidget(QWidget):
    """Widget responsible for displaying the pictograph answers."""

    def __init__(self, lesson_2_widget: "Lesson2Widget"):
        super().__init__(lesson_2_widget)
        self.lesson_2_widget = lesson_2_widget
        self.main_widget = lesson_2_widget.main_widget
        self.pictograph_factory = LessonPictographFactory(self.main_widget)

        self.layout: QHBoxLayout = QHBoxLayout()
        self.layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setLayout(self.layout)

        self.pictograph_views: list[QWidget] = []
        self.pictographs: dict[str, BasePictograph] = {}

    def display_answers(self, pictographs, correct_pictograph, check_answer_callback):
        """Display the pictographs as answer options."""
        self.clear()

        for pictograph_dict in pictographs:
            pictograph_key = (
                self.main_widget.pictograph_key_generator.generate_pictograph_key(
                    pictograph_dict
                )
            )
            pictograph = self.pictograph_factory.get_or_create_pictograph(
                pictograph_key, pictograph_dict, disable_gold_overlay=False
            )
            self.pictographs[pictograph_key] = pictograph
            pictograph.view.setCursor(Qt.CursorShape.PointingHandCursor)

            pictograph.view.mousePressEvent = (
                lambda event, opt=pictograph_dict: check_answer_callback(
                    opt, correct_pictograph
                )
            )

            self.pictograph_views.append(pictograph.view)

        for view in self.pictograph_views:
            self.layout.addWidget(view)

    def clear(self):
        """Clear all the displayed pictographs."""
        for view in self.pictograph_views:
            self.layout.removeWidget(view)
        self.pictograph_views.clear()
        self.pictographs.clear()

    def resize_lesson_2_answers_widget(self):
        """Resize the pictograph views based on window size."""
        for view in self.pictograph_views:
            view.setFixedSize(
                self.main_widget.height() // 3, self.main_widget.height() // 3
            )
        self._scale_pictographs()

    def _scale_pictographs(self):
        """Scale the pictographs to fit properly in the view."""
        for pictograph in self.pictographs.values():
            scene_size = pictograph.sceneRect().size()
            view_size = pictograph.view.size()
            scale_factor = min(
                view_size.width() / scene_size.width(),
                view_size.height() / scene_size.height(),
            )
            pictograph.view.scale(scale_factor, scale_factor)
            pictograph.container.styled_border_overlay.resize_styled_border_overlay()
