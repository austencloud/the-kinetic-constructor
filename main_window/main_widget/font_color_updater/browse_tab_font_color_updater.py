from typing import TYPE_CHECKING
from .base_font_color_updater import BaseFontColorUpdater

if TYPE_CHECKING:
    from main_window.main_widget.main_widget import MainWidget


class BrowseTabFontColorUpdater(BaseFontColorUpdater):
    def __init__(self, main_widget: "MainWidget", font_color: str):
        super().__init__(font_color)
        self.main_widget = main_widget

    def update(self):
        self._update_sequence_picker()
        self._update_sequence_viewer()

    def _update_sequence_picker(self):
        self.sequence_picker = self.main_widget.browse_tab.sequence_picker
        self._update_filter_selector()

        sequence_picker_labels = [
            self.sequence_picker.sort_widget.sort_by_label,
            self.sequence_picker.progress_bar.loading_label,
            self.sequence_picker.progress_bar.percentage_label,
        ]
        self._apply_font_colors(sequence_picker_labels)

        self.sequence_picker.sort_widget.style_buttons()
        self.sequence_picker.sort_widget.style_labels()
        self.sequence_picker.nav_sidebar.set_styles()

        for (
            thumbnail_box
        ) in self.sequence_picker.scroll_widget.thumbnail_boxes.values():
            self._apply_font_color(thumbnail_box.word_label)
            thumbnail_box.word_label.reload_favorite_icon()
            self._apply_font_color(thumbnail_box.variation_number_label)

    def _update_filter_selector(self):
        filter_selector = self.sequence_picker.filter_selector
        filter_selector_labels = (
            [
                filter_selector.filter_choice_widget.description_label,
                filter_selector.starting_letter_section.sequence_tally_label,
                filter_selector.starting_letter_section.header_label,
                filter_selector.contains_letter_section.sequence_tally_label,
                filter_selector.contains_letter_section.header_label,
                filter_selector.length_section.header_label,
                filter_selector.level_section.header_label,
                filter_selector.starting_position_section.header_label,
                filter_selector.author_section.header_label,
                filter_selector.grid_mode_section.header_label,
            ]
            + [
                description_label
                for description_label in filter_selector.filter_choice_widget.description_labels.values()
            ]
            + [
                tally_label
                for tally_label in filter_selector.length_section.sequence_tally_labels.values()
            ]
            + [
                tally_label
                for tally_label in filter_selector.level_section.tally_labels.values()
            ]
            + [
                description_label
                for description_label in filter_selector.level_section.description_labels.values()
            ]
            + [
                description_label
                for description_label in filter_selector.starting_position_section.description_labels.values()
            ]
            + [
                tally_label
                for tally_label in filter_selector.starting_position_section.tally_labels.values()
            ]
            + [
                author_label
                for author_label in filter_selector.author_section.tally_labels.values()
            ]
            + [
                tally_label
                for tally_label in filter_selector.author_section.tally_labels.values()
            ]
            + [
                tally_label
                for tally_label in filter_selector.grid_mode_section.tally_labels.values()
            ]
            + [
                description_label
                for description_label in filter_selector.grid_mode_section.description_labels.values()
            ]
        )
        self._apply_font_colors(filter_selector_labels)

    def _update_sequence_viewer(self):
        sequence_viewer = self.main_widget.browse_tab.sequence_viewer
        viewer_labels = [
            sequence_viewer.word_label,
            sequence_viewer.variation_number_label,
        ]
        self._apply_font_colors(viewer_labels)
        sequence_viewer.image_label.resize_placeholder()
