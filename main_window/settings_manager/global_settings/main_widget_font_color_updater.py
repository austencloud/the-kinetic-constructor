from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QWidget, QCheckBox

from main_window.main_widget.generate_tab.circular.circular_sequence_generator_frame import (
    CircularSequenceGeneratorFrame,
)
from main_window.main_widget.generate_tab.freeform.freeform_sequence_generator_frame import (
    FreeformSequenceGeneratorFrame,
)
from main_window.main_widget.learn_tab.base_classes.base_lesson_widget.base_lesson_widget import (
    BaseLessonWidget,
)

if TYPE_CHECKING:

    from ...main_widget.main_widget import MainWidget


class MainWidgetFontColorUpdater:
    def __init__(self, main_widget: "MainWidget"):
        self.main_widget = main_widget

    def update_main_widget_font_colors(self, bg_type):
        self.font_color = self.get_font_color(bg_type)
        self._apply_main_widget_colors()

    @staticmethod
    def get_font_color(bg_type: str) -> str:
        """Return the appropriate font color based on the background type."""
        return (
            "black" if bg_type in ["Rainbow", "AuroraBorealis", "Aurora"] else "white"
        )

    def _apply_font_color(self, widget: QWidget) -> None:
        # If it's a QCheckBox, apply a more specific stylesheet
        if isinstance(widget, QCheckBox):
            # Apply rules to only the text, and separate rules for the indicator
            widget.setStyleSheet(
                f"""
                QCheckBox {{
                    color: {self.font_color}; /* Apply text color for the checkbox label */
                }}
                QCheckBox::indicator {{
                    background-color: white; /* Ensure a white background for clarity */
                    border: 2px solid #ccc;
                    width: 18px;
                    height: 18px;
                }}
                QCheckBox::indicator:checked {{
                    border: 2px solid #68d4ff;
                    background-color: white;
                }}
                """
            )
        else:
            # For other widgets, append the color rule to their existing stylesheet
            existing_style = widget.styleSheet()
            new_style = f"{existing_style} color: {self.font_color};"
            widget.setStyleSheet(new_style)

    def _apply_font_colors(self, widgets: list[QWidget]) -> None:
        for w in widgets:
            self._apply_font_color(w)

    def _apply_main_widget_colors(self) -> None:
        """Apply font colors to all relevant sections of the main widget."""
        self._update_menu_bar_widget()
        self._update_sequence_widget()
        self._update_construct_tab()
        self._update_generate_tab()
        self._update_browse_tab()
        self._update_learn_tab()
        self._update_act_tab()

    def _update_act_tab(self) -> None:
        act_tab = self.main_widget.write_tab
        act_sheet = self.main_widget.act_sheet
        self._apply_font_color(act_sheet.act_header)
        self._apply_font_color(act_sheet.act_container)
        for thumbnail_box in act_tab.act_browser.thumbnail_boxes:
            self._apply_font_color(thumbnail_box.word_label)
        for box in act_sheet.act_container.cue_scroll.cue_frame.cue_boxes.values():
            for widget in [box.timestamp, box.cue_label]:
                self._apply_font_color(widget)
            for edit in [box.timestamp.edit, box.cue_label.edit]:
                self._apply_font_color(edit)

            box.setStyleSheet(f"#cue_box {{border-top: 1px solid {self.font_color};}}")

    def _update_menu_bar_widget(self) -> None:
        menu_bar = self.main_widget.menu_bar_widget
        for label, _ in menu_bar.selectors_widget.sections:
            self._apply_font_color(label)

    def _update_sequence_widget(self) -> None:
        sequence_widget = self.main_widget.sequence_widget
        self._apply_font_colors(
            [
                sequence_widget.current_word_label,
                sequence_widget.difficulty_label,
                sequence_widget.indicator_label,
            ]
        )

    def _update_generate_tab(self) -> None:
        sequence_generator = self.main_widget.generate_tab
        freeform_labels = self._get_freeform_builder_labels(
            sequence_generator.freeform_generator_frame
        )
        circular_labels = self._get_circular_builder_labels(
            sequence_generator.circular_generator_frame
        )

        self._apply_font_colors(freeform_labels + circular_labels)
        sequence_generator.freeform_generator_frame.continuous_rotation_toggle.update_mode_label_styles()
        sequence_generator.circular_generator_frame.continuous_rotation_toggle.update_mode_label_styles()
        sequence_generator.overwrite_checkbox.set_label_color(self.font_color)

    def _update_construct_tab(self):
        construct_tab = self.main_widget.construct_tab
        construct_labels = [
            construct_tab.option_picker.reversal_filter.combo_box_label,
        ]
        self._apply_font_colors(construct_labels)

    def _get_freeform_builder_labels(
        self, freeform_generator_frame: "FreeformSequenceGeneratorFrame"
    ) -> list[QWidget]:
        return [
            freeform_generator_frame.level_selector.level_label,
            freeform_generator_frame.length_adjuster.length_label,
            freeform_generator_frame.length_adjuster.length_value_label,
            freeform_generator_frame.turn_intensity_adjuster.intensity_label,
            freeform_generator_frame.turn_intensity_adjuster.intensity_value_label,
            freeform_generator_frame.letter_type_picker.filter_label,
        ]

    def _get_circular_builder_labels(
        self, circular_generator_frame: "CircularSequenceGeneratorFrame"
    ) -> list[QWidget]:
        return [
            circular_generator_frame.level_selector.level_label,
            circular_generator_frame.length_adjuster.length_label,
            circular_generator_frame.length_adjuster.length_value_label,
            circular_generator_frame.turn_intensity_adjuster.intensity_label,
            circular_generator_frame.turn_intensity_adjuster.intensity_value_label,
        ]

    def _update_browse_tab(self) -> None:
        browse_tab = self.main_widget.browse_tab
        sort_widget = browse_tab.sort_widget

        browse_tab_labels = [
            sort_widget.sort_by_label,
            browse_tab.preview_area.word_label,
            browse_tab.preview_area.variation_number_label,
            browse_tab.progress_bar.loading_label,
            browse_tab.progress_bar.percentage_label,
            browse_tab.initial_selection_widget.filter_choice_widget.description_label,
        ] + [
            button_label
            for button_label in browse_tab.initial_selection_widget.filter_choice_widget.button_labels.values()
        ]
        self._apply_font_colors(browse_tab_labels)

        sort_widget.style_buttons()
        sort_widget.style_labels()
        browse_tab.nav_sidebar.set_styles()
        browse_tab.preview_area.image_label.resize_placeholder()

        for thumbnail_box in browse_tab.scroll_widget.thumbnail_boxes.values():
            self._apply_font_color(thumbnail_box.word_label)
            thumbnail_box.word_label.reload_favorite_icon()
            self._apply_font_color(thumbnail_box.variation_number_label)

    def _update_learn_tab(self) -> None:
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
            self._apply_font_color(lesson_widget.result_label)

        self._apply_font_color(
            self.main_widget.codex.control_widget.ori_selector.start_ori_label
        )
