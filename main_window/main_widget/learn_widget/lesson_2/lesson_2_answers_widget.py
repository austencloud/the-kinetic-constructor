from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QWidget, QHBoxLayout
from PyQt6.QtCore import Qt

from base_widgets.base_pictograph.base_pictograph import BasePictograph
from main_window.main_widget.learn_widget.base_classes.base_answers_widget import BaseAnswersWidget


if TYPE_CHECKING:
    from main_window.main_widget.learn_widget.lesson_2.lesson_2_widget import (
        Lesson2Widget,
    )


class Lesson2AnswersWidget(BaseAnswersWidget):
    """Widget responsible for displaying the pictograph answers."""

    def __init__(self, lesson_2_widget: "Lesson2Widget"):
        super().__init__(lesson_2_widget)
        self.lesson_2_widget = lesson_2_widget

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
            pictograph = BasePictograph(self.main_widget, scroll_area=None)
            pictograph.disable_gold_overlay = False
            pictograph.updater.update_pictograph(pictograph_dict)
            self.pictographs[pictograph_key] = pictograph
            pictograph.view.setCursor(Qt.CursorShape.PointingHandCursor)

            # Explicitly capture pictograph_dict as a default argument in the lambda
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
            view.deleteLater()
        self.pictograph_views.clear()
        self.pictographs.clear()

    def resize_answers_widget(self):
        """Resize the pictograph views based on window size."""
        for view in self.pictograph_views:
            view.setFixedSize(
                self.main_widget.height() // 4, self.main_widget.height() // 4
            )
