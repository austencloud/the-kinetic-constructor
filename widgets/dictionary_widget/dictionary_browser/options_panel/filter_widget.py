from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QCheckBox, QLabel
from PyQt6.QtCore import Qt


if TYPE_CHECKING:
    from widgets.dictionary_widget.dictionary_browser.options_panel.dictionary_browser_options_panel import (
        DictionaryOptionsPanel,
    )


class FilterWidget(QWidget):
    def __init__(self, options_panel: "DictionaryOptionsPanel") -> None:
        super().__init__(options_panel)
        self.browser = options_panel.browser
        self.main_widget = self.browser.dictionary_widget.main_widget
        self.settings_manager = self.main_widget.main_window.settings_manager

        self.level_checkboxes = {}
        self.selected_levels = set()

        self._setup_layout()

    def _setup_layout(self):
        self.layout: QVBoxLayout = QVBoxLayout(self)
        self.layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        self.level_label = QLabel("Filter by Level:")
        self.level_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.layout.addWidget(self.level_label)

        # Get all levels from the dictionary metadata
        levels = self._get_all_levels()

        # Create checkboxes for each level
        for level in levels:
            checkbox = QCheckBox(f"Level {level}")
            checkbox.stateChanged.connect(self._on_level_checkbox_state_changed)
            self.level_checkboxes[level] = checkbox
            self.layout.addWidget(checkbox)

    def _get_all_levels(self):
        # Use DictionarySorter to get all sequences with metadata
        sequences_with_metadata = (
            self.main_widget.metadata_extractor.get_metadata_and_thumbnail_dict()
        )
        levels = set(
            metadata_and_thumbnails_dict["metadata"]["sequence"][0]["level"]
            for metadata_and_thumbnails_dict in sequences_with_metadata
            if "level" in metadata_and_thumbnails_dict["metadata"]["sequence"][0]
        )
        return sorted(levels)

    def _on_level_checkbox_state_changed(self, state):
        sender = self.sender()
        level = int(sender.text().replace("Level ", ""))

        if state == 2:
            self.selected_levels.add(level)
        else:
            self.selected_levels.discard(level)

        self._filter_sequences_by_level()

    def _filter_sequences_by_level(self):
        if not self.selected_levels:
            self.browser.reset_filters()  # Show all sequences if no filter is applied
        else:
            filtered_sequences = []
            list_of_sequences = (
                self.main_widget.metadata_extractor.get_metadata_and_thumbnail_dict()
            )
            for sequence in list_of_sequences:
                metadata = sequence["metadata"]
                if metadata["sequence"][0]["level"] in self.selected_levels:
                    filtered_sequences.append(sequence)

            self.browser.display_filtered_sequences(filtered_sequences)
