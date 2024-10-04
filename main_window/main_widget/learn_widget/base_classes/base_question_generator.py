from typing import TYPE_CHECKING

from Enums.letters import Letter


if TYPE_CHECKING:
    from main_window.main_widget.learn_widget.base_classes.base_lesson_widget.base_lesson_widget import BaseLessonWidget


class BaseQuestionGenerator:
    not_implemented_message = "This function should be implemented by the subclass."

    def __init__(self, lesson_widget: "BaseLessonWidget"):
        self.main_widget = lesson_widget.main_widget

    def filter_pictograph_dicts_by_grid_mode(self) -> dict[Letter, list[dict]]:
        """Filter pictograph dicts by grid mode."""
        valid_dicts: dict[Letter, list[dict]] = {}
        grid_mode = self.main_widget.settings_manager.global_settings.get_grid_mode()
        for letter in self.main_widget.pictograph_dicts:
            valid_dicts.setdefault(letter, [])
            for pictograph_dict in self.main_widget.pictograph_dicts[letter]:
                if (
                    self.main_widget.grid_mode_checker.check_grid_mode(pictograph_dict)
                    == grid_mode
                ):
                    valid_dicts[letter].append(pictograph_dict)
        return valid_dicts

    def generate_question(self):
        raise NotImplementedError(self.not_implemented_message)

    def generate_correct_answer(self):
        raise NotImplementedError(self.not_implemented_message)

    def generate_wrong_answers(self, correct_answer):
        raise NotImplementedError(self.not_implemented_message)

    def _get_random_correct_pictograph(self):
        raise NotImplementedError(self.not_implemented_message)
