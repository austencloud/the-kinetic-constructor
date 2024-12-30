from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QPushButton, QSizePolicy
from PyQt6.QtCore import Qt

from main_window.main_widget.learn_tab.base_classes.base_lesson_widget.base_go_back_button import (
    BaseGoBackButton,
)


if TYPE_CHECKING:
    from main_window.main_widget.learn_tab.base_classes.base_lesson_widget.base_lesson_widget import (
        BaseLessonWidget,
    )


class LessonWidgetGoBackButton(BaseGoBackButton):
    def __init__(self, lesson_widget: "BaseLessonWidget"):
        super().__init__(lesson_widget.main_widget)
        self.lesson_widget = lesson_widget
        self.main_widget = self.lesson_widget.main_widget
        self.clicked.connect(
            lambda: self.lesson_widget.learn_widget.lesson_selector.show()
        )
