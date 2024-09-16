from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout
from PyQt6.QtCore import Qt
from base_widgets.base_pictograph.base_pictograph import BasePictograph

if TYPE_CHECKING:
    from ..base_classes.base_lesson_widget import BaseLessonWidget


class BaseQuestionWidget(QWidget):
    def __init__(self, lesson_widget: "BaseLessonWidget"):
        super().__init__(lesson_widget)
        self.lesson_widget = lesson_widget
        self.main_widget = lesson_widget.main_widget
        self.question_label: QLabel = None
        self.layout: QVBoxLayout = None

    def clear(self) -> None:
        raise NotImplementedError(
            "This function should be implemented by the subclass."
        )

    def _resize_question_label(self) -> None:
        question_label_font_size = self.main_widget.width() // 65
        font = self.question_label.font()
        font.setFamily("Georgia")
        font.setPointSize(question_label_font_size)
        self.question_label.setFont(font)

    def load_pictograph(self, pictograph_dict) -> None:
        """Load and display the pictograph."""
        self.pictograph: BasePictograph = BasePictograph(
            self.main_widget, scroll_area=None
        )
        self.pictograph.disable_gold_overlay = True
        self.pictograph.updater.update_pictograph(pictograph_dict)
        self.layout.addWidget(
            self.pictograph.view, alignment=Qt.AlignmentFlag.AlignCenter
        )
