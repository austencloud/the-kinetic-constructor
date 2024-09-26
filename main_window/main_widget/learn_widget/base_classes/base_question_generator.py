from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from main_window.main_widget.learn_widget.base_classes.base_lesson_widget.base_lesson_widget import BaseLessonWidget


class BaseQuestionGenerator:
    not_implemented_message = "This function should be implemented by the subclass."

    def __init__(self, lesson_widget: "BaseLessonWidget"):
        self.main_widget = lesson_widget.main_widget

    def generate_question(self):
        raise NotImplementedError(self.not_implemented_message)

    def generate_correct_answer(self):
        raise NotImplementedError(self.not_implemented_message)

    def generate_wrong_answers(self, correct_answer):
        raise NotImplementedError(self.not_implemented_message)

    def _get_random_correct_pictograph(self):
        raise NotImplementedError(self.not_implemented_message)
