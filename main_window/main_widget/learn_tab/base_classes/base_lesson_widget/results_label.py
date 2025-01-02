from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QHBoxLayout, QLabel
from PyQt6.QtCore import Qt

from main_window.main_widget.learn_tab.base_classes.base_lesson_widget.answer_checker import (
    AnswerChecker,
)
from main_window.main_widget.learn_tab.base_classes.base_lesson_widget.go_back_button import (
    LessonGoBackButton,
)
from main_window.main_widget.learn_tab.base_classes.base_lesson_widget.resize_manager import (
    LessonResizeManager,
)
from ..base_answers_widget import BaseAnswersWidget
from .quiz_timer_manager import QuizTimerManager
from ..base_question_generator import BaseQuestionGenerator
from ..base_question_widget import BaseQuestionWidget
from ...indicator_label import LessonIndicatorLabel
from .results_widget import ResultsWidget

if TYPE_CHECKING:
    from ...learn_tab import LearnTab

    from main_window.main_widget.learn_tab.base_classes.base_lesson_widget.base_lesson_widget import BaseLessonWidget


class LessonResultLabel(QLabel):
    def __init__(self, lesson_widget: "BaseLessonWidget"):
        super().__init__(lesson_widget)
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lesson_widget = lesson_widget

    def resizeEvent(self,event):
        font_size = self.lesson_widget.main_widget.width() // 60
        font = self.lesson_widget.result_label.font()
        font.setPointSize(font_size)
        self.lesson_widget.result_label.setFont(font)