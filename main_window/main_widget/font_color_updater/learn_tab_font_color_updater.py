from typing import TYPE_CHECKING
from .base_font_color_updater import BaseFontColorUpdater
from main_window.main_widget.learn_tab.base_classes.base_lesson_widget.base_lesson_widget import (
    BaseLessonWidget,
)

if TYPE_CHECKING:
    from main_window.main_widget.main_widget import MainWidget


class LearnTabFontColorUpdater(BaseFontColorUpdater):
    def __init__(self, main_widget: "MainWidget", font_color: str):
        super().__init__(font_color)
        self.main_widget = main_widget

    def update(self):
        learn_tab = self.main_widget.learn_tab
        self._apply_font_color(learn_tab.lesson_selector.title_label)
        self._apply_font_colors(
            list(learn_tab.lesson_selector.description_labels.values())
        )
        learn_tab.lesson_selector.mode_toggle_widget.update_mode_label_styles()

        lesson_widgets: list[BaseLessonWidget] = [
            learn_tab.lesson_1_widget,
            learn_tab.lesson_2_widget,
            learn_tab.lesson_3_widget,
        ]
        for lesson_widget in lesson_widgets:
            self._apply_font_color(lesson_widget.question_widget)
            self._apply_font_color(lesson_widget.progress_label)
            self._apply_font_color(learn_tab.results_widget.result_label)

        self._apply_font_color(
            self.main_widget.learn_tab.codex.control_widget.ori_selector.start_ori_label
        )
