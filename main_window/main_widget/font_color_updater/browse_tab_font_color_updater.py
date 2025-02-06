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
        self._update_control_panel()
        self._update_nav_sidebar()
        self._update_thumbnail_boxes()

    def _update_control_panel(self):
        control_panel = self.sequence_picker.control_panel
        control_panel_labels = [
            control_panel.sort_widget.sort_by_label,
            control_panel.currently_displaying_label,
            control_panel.count_label,
        ]
        self._apply_font_colors(control_panel_labels)
        control_panel.sort_widget.style_buttons()
        control_panel.sort_widget.style_labels()

    def _update_progress_bar(self):
        progress_bar = self.sequence_picker.progress_bar
        progress_bar_labels = [
            progress_bar.loading_label,
            progress_bar.percentage_label,
        ]
        self._apply_font_colors(progress_bar_labels)

    def _update_nav_sidebar(self):
        nav_bar = self.sequence_picker.nav_sidebar
        nav_bar_labels = [
            nav_bar.length_label,
            nav_bar.letter_label,
        ] + [year_label for year_label in nav_bar.year_labels.values()]

        self._apply_font_colors(nav_bar_labels)

    def _update_thumbnail_boxes(self):
        for (
            thumbnail_box
        ) in self.sequence_picker.scroll_widget.thumbnail_boxes.values():
            self._apply_font_color(thumbnail_box.word_label)
            thumbnail_box.word_label.reload_favorite_icon()
            self._apply_font_color(thumbnail_box.variation_number_label)

    def _update_filter_selector(self):
        filter_selector = self.sequence_picker.filter_stack
        header_labels = [
            filter_selector.starting_letter_section.header_label,
            filter_selector.contains_letter_section.header_label,
            filter_selector.length_section.header_label,
            filter_selector.level_section.header_label,
            filter_selector.starting_position_section.header_label,
            filter_selector.author_section.header_label,
            filter_selector.grid_mode_section.header_label,
        ]

        description_labels = (
            [filter_selector.filter_choice_widget.header_label]
            + list(filter_selector.filter_choice_widget.description_labels.values())
            + list(filter_selector.level_section.description_labels.values())
            + list(
                filter_selector.starting_position_section.description_labels.values()
            )
            + list(filter_selector.grid_mode_section.description_labels.values())
        )

        tally_labels = (
            [filter_selector.starting_letter_section.sequence_tally_label]
            + [filter_selector.contains_letter_section.sequence_tally_label]
            + list(filter_selector.length_section.sequence_tally_labels.values())
            + list(filter_selector.level_section.tally_labels.values())
            + list(filter_selector.starting_position_section.tally_labels.values())
            + list(filter_selector.author_section.tally_labels.values())
            + list(filter_selector.grid_mode_section.tally_labels.values())
        )

        filter_selector_labels = header_labels + description_labels + tally_labels
        self._apply_font_colors(filter_selector_labels)

    def _update_sequence_viewer(self):
        sequence_viewer = self.main_widget.browse_tab.sequence_viewer
        viewer_labels = [
            sequence_viewer.word_label,
            sequence_viewer.variation_number_label,
            sequence_viewer.placeholder_label,
        ]
        self._apply_font_colors(viewer_labels)
